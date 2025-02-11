package be.vlaanderen.geonet.kernel.security.openidconnect;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import net.minidev.json.JSONObject;
import org.apache.http.NameValuePair;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.protocol.HTTP;
import org.fao.geonet.constants.Geonet;
import org.fao.geonet.kernel.security.openidconnect.OidcUser2GeonetworkUser;
import org.fao.geonet.utils.GeonetHttpRequestFactory;
import org.fao.geonet.utils.Log;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.client.ClientHttpResponse;
import org.springframework.security.authentication.event.AuthenticationSuccessEvent;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.oauth2.core.OAuth2AccessToken;
import org.springframework.security.oauth2.core.oidc.OidcIdToken;
import org.springframework.security.oauth2.core.oidc.user.DefaultOidcUser;
import org.springframework.security.oauth2.server.resource.InvalidBearerTokenException;
import org.springframework.security.oauth2.server.resource.authentication.BearerTokenAuthentication;
import org.springframework.security.web.authentication.AbstractAuthenticationProcessingFilter;

import javax.servlet.FilterChain;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.*;

public class ACMIDMApiLoginAuthenticationFilter extends AbstractAuthenticationProcessingFilter {

    @Autowired
    protected GeonetHttpRequestFactory requestFactory;

    @Autowired
    OidcUser2GeonetworkUser oidcUser2GeonetworkUser;

    private String introspectUrl;
    private String clientId;
    private String clientSecret;
    private final ACMIDMTokenCache cache = new ACMIDMTokenCache();

    protected ACMIDMApiLoginAuthenticationFilter() {
        super("we don't use this parameter");
    }

    @Override
    protected void unsuccessfulAuthentication(HttpServletRequest request,
                                              HttpServletResponse response, AuthenticationException failed)
        throws IOException, ServletException {
        super.unsuccessfulAuthentication(request, response, failed);
    }

    @Override
    protected void successfulAuthentication(HttpServletRequest request,
                                            HttpServletResponse response,
                                            FilterChain chain,
                                            Authentication authResult) throws IOException {
        // all logic is handled in `attemptAuthentication`, as we want to be authenticated _before_ the rest of the chain finishes.
    }

    @Override
    public synchronized Authentication attemptAuthentication(HttpServletRequest request, HttpServletResponse response) throws AuthenticationException, IOException, ServletException {
        String bearerToken = getBearerToken(request).orElseThrow(() -> new InvalidBearerTokenException("No bearer token supplied."));

        // if we can return the Authentication straight from the cache, do it
        // this avoids having to introspect the token at ACM/IDM
        BearerTokenAuthentication item = cache.getItem(bearerToken);
        if(item!=null) {
            Log.debug(Geonet.SECURITY, "Bearer token found in cache, not introspecting.");
            saveAuthentication(item);
            return item;
        }

        // validate the token at ACM/IDM
        Log.debug(Geonet.SECURITY, "Introspecting bearer token ("+bearerToken+")");
        IntrospectedToken validationToken = introspectToken(bearerToken);
        if (validationToken.isActive) {
            OAuth2AccessToken oAuth2AccessToken = new OAuth2AccessToken(OAuth2AccessToken.TokenType.BEARER, validationToken.jwt, validationToken.issuedAt, validationToken.expiresAt, new HashSet<>(validationToken.scopes));
            if (validationToken.scopes.stream().noneMatch(s -> s != null && s.startsWith("dv_metadata"))) {
                throw new InvalidBearerTokenException("Did not find a metadata scope for this client.");
            }
            OidcIdToken oidcIdToken = new OidcIdToken(validationToken.jwt, validationToken.issuedAt, validationToken.expiresAt, validationToken.toMap());
            try {
                UserDetails userDetails = oidcUser2GeonetworkUser.getUserDetails(oidcIdToken, validationToken.toMap(), true);
                Collection<GrantedAuthority> authorities = (Collection<GrantedAuthority>) userDetails.getAuthorities();
                DefaultOidcUser principal = new DefaultOidcUser(authorities, oidcIdToken);
                BearerTokenAuthentication authentication = new BearerTokenAuthentication(principal, oAuth2AccessToken, authorities);

                // setting the authentication already here, instead of in 'successfulAuthentication', as we want it to be available in the following Filters
                saveAuthentication(authentication);

                // keep the authentication result in the cache
                cache.putItem(bearerToken, authentication);

                return authentication;
            } catch (Exception e) {
                throw new RuntimeException(e);
            }
        } else {
            throw new InvalidBearerTokenException("Invalid token.");
        }
    }

    private void saveAuthentication(BearerTokenAuthentication authentication) {
        SecurityContextHolder.getContext().setAuthentication(authentication);
        if (this.eventPublisher != null) {
            eventPublisher.publishEvent(new AuthenticationSuccessEvent(authentication));
        }
    }

    /**
     * Introspect the bearer token with ACM/IDM, thereby validating it and retrieving the necessary client information.
     *
     * @param bearerToken
     * @return
     */
    private IntrospectedToken introspectToken(String bearerToken) {
        try {
            Log.debug(Geonet.SECURITY, "Introspecting bearertoken at url "+introspectUrl);
            HttpPost introspectRequest = new HttpPost(introspectUrl);
            List<NameValuePair> nvps = new ArrayList<>();
            nvps.add(new BasicNameValuePair("client_id", clientId));
            nvps.add(new BasicNameValuePair("client_secret", clientSecret));
            nvps.add(new BasicNameValuePair("token_type_hint", "access_token"));
            nvps.add(new BasicNameValuePair("token", bearerToken));
            introspectRequest.setEntity(new UrlEncodedFormEntity(nvps, HTTP.UTF_8));
            introspectRequest.addHeader("Accept", "application/json");
            introspectRequest.addHeader("Content-type", "application/x-www-form-urlencoded");
            try (ClientHttpResponse introspectResponse = requestFactory.execute(introspectRequest)) {
                System.out.println("response = " + introspectResponse);
                ObjectMapper objectMapper = new ObjectMapper();
                return new IntrospectedToken(objectMapper.readTree(introspectResponse.getBody()));
            }
        } catch (Exception e) {
            Log.error(Geonet.SECURITY, "Could not introspect bearer token url " + introspectUrl + ": " + e);
            throw new InvalidBearerTokenException("Could not introspect the bearer token: " + e);
        }
    }

    /**
     * Retrieve the bearer token from a request.
     *
     * @param request
     * @return
     */
    private Optional<String> getBearerToken(HttpServletRequest request) {
        Optional<String> authorization = Optional.ofNullable(request.getHeader("Authorization"));
        String bearerPrefix = "bearer ".toLowerCase();
        if(authorization.isPresent() && authorization.get().toLowerCase().startsWith(bearerPrefix)) {
            return Optional.of(authorization.get().substring(bearerPrefix.length()));
        } else {
            return Optional.empty();
        }
    }

    /**
     * Here, we want to authenticate when there is a bearer token present - indicating an ACMIDM API client.
     * Otherwise, we fall through to the regular ACMIDM oidc authentication.
     *
     * @param request
     * @param response
     * @return
     */
    @Override
    protected boolean requiresAuthentication(HttpServletRequest request, HttpServletResponse response) {
        return getBearerToken(request).isPresent();
    }

    public void setIntrospectUrl(String introspectUrl) {
        this.introspectUrl = introspectUrl;
    }

    public void setClientId(String clientId) {
        this.clientId = clientId;
    }

    public void setClientSecret(String clientSecret) {
        this.clientSecret = clientSecret;
    }
}
