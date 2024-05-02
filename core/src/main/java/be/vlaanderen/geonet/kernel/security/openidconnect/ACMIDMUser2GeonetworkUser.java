package be.vlaanderen.geonet.kernel.security.openidconnect;

import org.fao.geonet.constants.Geonet;
import org.fao.geonet.domain.*;
import org.fao.geonet.kernel.security.openidconnect.OidcUser2GeonetworkUser;
import org.fao.geonet.kernel.security.openidconnect.SimpleOidcUser;
import org.fao.geonet.repository.UserGroupRepository;
import org.fao.geonet.repository.specification.UserGroupSpecs;
import org.fao.geonet.utils.Log;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.oauth2.core.oidc.OidcIdToken;
import org.springframework.security.oauth2.server.resource.InvalidBearerTokenException;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.util.StringUtils;

import java.util.*;
import java.util.stream.Collectors;

public class ACMIDMUser2GeonetworkUser extends OidcUser2GeonetworkUser {

    private String dpPrefix = "DataPublicatie ";
    private static String applicationNameAttribute = "vo_applicatienaam";
    private static String clientIdAttribute = "client_id";

    @Override
    @Transactional
    public UserDetails getUserDetails(OidcIdToken idToken, Map attributes, boolean withDbUpdate) throws Exception {
        SimpleOidcUser simpleUser = simpleOidcUserFactory.create(idToken, attributes);
        if (!StringUtils.hasText(simpleUser.getUsername()))
            return null;

        // it seems like vo_email is equal to sub (a uuid) for API clients, but let's not take any chances
        String userName;
        if (isClient(idToken)) {
            userName = idToken.getClaimAsString("sub");
        } else {
            userName = simpleUser.getUsername();
        }

        User user;
        boolean newUserFlag = false;
        try {
            user = (User) geonetworkAuthenticationProvider.loadUserByUsername(userName);
        } catch (UsernameNotFoundException e) {
            user = new User();
            user.setUsername(userName);
            newUserFlag = true;
            Log.debug(Geonet.SECURITY, "Adding a new user: " + user);
        }

        simpleUser.updateUser(user); // copy attributes from the IDToken to the GN user

        if (isClient(idToken)) {
            // name is missing in the case of clients > use vo_applicatienaam instead. for regular clients, the name is already set
            user.setName(idToken.getClaimAsString(applicationNameAttribute));
            // handle profiles for clients in a custom way, can't use the oidcRoleProcessor as that would conflict with the default user setup
            Set<String> scopes = clientScopes(idToken);
            Profile profile = getClientProfile(scopes);
            user.setProfile(profile);
            // save changes to database
            if (withDbUpdate) {
                userRepository.save(user);
                updateUserGroupsForClient(user, profile);
            }
        } else {
            // profiles are handled by the default oidc setup, modified to our liking
            Map<Profile, List<String>> profileGroups = oidcRoleProcessor.getProfileGroups(idToken);
            user.setProfile(oidcRoleProcessor.getProfile(idToken));
            //Apply changes to database is required.
            if (withDbUpdate) {
                if (newUserFlag || oidcConfiguration.isUpdateProfile()) {
                    userRepository.save(user);
                }
                if (newUserFlag || oidcConfiguration.isUpdateGroup()) {
                    // ACM/IDM specific modification: pass the idtoken
                    updateGroups(profileGroups, user, idToken);
                }
            }
        }

        return user;
    }

    /**
     * Set the user-group profile for a specific user, for _all_ groups. To be used for API clients.
     *
     * @param user    the service account user
     * @param profile the desired profile
     */
    private void updateUserGroupsForClient(User user, Profile profile) {
        userGroupRepository.deleteAll(UserGroupSpecs.hasUserId(user.getId()));
        if (profile.equals(Profile.Administrator)) {
            // As we are assigning to a group, it is UserAdmin instead
            profile = Profile.UserAdmin;
        }
        Profile finalProfile = profile;
        groupRepository.findAll().stream()
            .filter(g -> g.getId() >= 100)
            .forEach(g -> {
                UserGroup usergroup = new UserGroup();
                usergroup.setGroup(g);
                usergroup.setUser(user);
                usergroup.setProfile(finalProfile);
                userGroupRepository.save(usergroup);

                if(finalProfile.equals(Profile.Reviewer)) {
                    // when you are a Reviewer, GeoNetwork expects you to have the Editor role as well
                    UserGroup editorUserGroup = new UserGroup();
                    editorUserGroup.setGroup(g);
                    editorUserGroup.setUser(user);
                    editorUserGroup.setProfile(Profile.Editor);
                    userGroupRepository.save(editorUserGroup);
                }
            });
    }

    private Profile getClientProfile(Set<String> scopes) {
        if (scopes.contains("dv_metadata_write")) {
            return Profile.Reviewer;
        } else if (scopes.contains("dv_metadata_read")) {
            return Profile.Guest;
        } else {
            // This should not occur here, as we check in ACMIDMApiLoginAuthenticationFilter as well. Can't hurt to test twice though.
            throw new InvalidBearerTokenException("Could not find one of the expected metadata client scopes.");
        }
    }

    private Set<String> clientScopes(OidcIdToken idToken) {
        return Arrays.stream(idToken.getClaimAsString("scope").split(" "))
            .filter(s -> !s.isEmpty())
            .filter(s -> s.startsWith("dv_metadata"))
            .collect(Collectors.toSet());
    }

    /**
     * Check whether the token indicates we are dealing with an API Client or a regular end user.
     *
     * @param idToken
     * @return
     */
    private boolean isClient(OidcIdToken idToken) {
        return idToken.hasClaim("token_type") &&
            idToken.getClaimAsString("token_type").equalsIgnoreCase("bearer") &&
            idToken.hasClaim(applicationNameAttribute) &&
            idToken.hasClaim(clientIdAttribute);
    }

    @Transactional
    public void updateGroups(Map<Profile, List<String>> profileGroups, User user, OidcIdToken idToken) {
        // First we remove all previous groups
        userGroupRepository.deleteAll(userGroupRepository.findAll(UserGroupSpecs.hasUserId(user.getId())));

        // ACM/IDM specific claims
        String userOrgCode = idToken.getClaimAsString("vo_orgcode");
        String userOrgName = idToken.getClaimAsString("vo_orgnaam");

        // Now we add the groups
        for (Profile p : profileGroups.keySet()) {
            List<String> groups = profileGroups.get(p);
            for (String technicalGroupName : groups) {

                String roleOrgCode = technicalGroupName.replaceFirst("(dp|mdv)-", "");
                boolean isDp = technicalGroupName.startsWith("dp-");
                // figure out the 'groupOwner' type, eventually used as a filter for the geonetwork portals
                String vlType = null;
                if (technicalGroupName.startsWith("mdv-")) {
                    vlType = "metadatavlaanderen";
                } else if (technicalGroupName.startsWith("dp-")) {
                    vlType = "datapublicatie";
                }

                String groupName = computeGroupName(userOrgCode, userOrgName, roleOrgCode, isDp);
                Group group = groupRepository.findByOrgCodeAndVlType(roleOrgCode, vlType);

                if (group == null) {
                    group = new Group();
                    group.setOrgCode(roleOrgCode);
                    group.setName(groupName);
                    // Populate languages for the group
                    for (Language l : langRepository.findAll()) {
                        group.getLabelTranslations().put(l.getId(), group.getName());
                    }
                }

                if (userOrgCode.equals(group.getOrgCode()) && !groupName.equals(group.getName())) {
                    // check if we need to modify the group name
                    group.setName(groupName);
                    // Populate languages for the group
                    for (Language l : langRepository.findAll()) {
                        group.getLabelTranslations().put(l.getId(), group.getName());
                    }
                }

                group.setVlType(vlType);
                groupRepository.save(group);

                UserGroup usergroup = new UserGroup();
                usergroup.setGroup(group);
                usergroup.setUser(user);

                Profile profile = p;
                if (profile.equals(Profile.Administrator)) {
                    // As we are assigning to a group, it is UserAdmin instead
                    profile = Profile.UserAdmin;
                }
                usergroup.setProfile(profile);

                //Todo - It does not seem necessary to add the user to the editor profile
                // since the reviewer is the parent of the editor
                // Seems like the permission checks should be smart enough to know that if a user
                // is a reviewer then they are also an editor.  Need to test and fix if necessary
                if (profile.equals(Profile.Reviewer)) {
                    UserGroup ug = new UserGroup();
                    ug.setGroup(group);
                    ug.setUser(user);
                    ug.setProfile(Profile.Editor);
                    userGroupRepository.save(ug);
                }

                userGroupRepository.save(usergroup);
            }
        }
    }

    private String computeGroupName(String userOrgCode,
                                    String userOrgName,
                                    String roleOrgCode,
                                    boolean isDp) {
        String dpPrefix = this.dpPrefix;
        String result = "";
        if (roleOrgCode.equals(userOrgCode)) {
            result = (isDp ? dpPrefix + userOrgName : userOrgName);
        } else {
            result = (isDp ? dpPrefix + roleOrgCode : roleOrgCode);
        }
        return result;
    }


}
