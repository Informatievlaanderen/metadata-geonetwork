/*
 * Copyright (C) 2022 Food and Agriculture Organization of the
 * United Nations (FAO-UN), United Nations World Food Programme (WFP)
 * and United Nations Environment Programme (UNEP)
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or (at
 * your option) any later version.
 *
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA
 *
 * Contact: Jeroen Ticheler - FAO - Viale delle Terme di Caracalla 2,
 * Rome - Italy. email: geonetwork@osgeo.org
 */
package be.vlaanderen.geonet.kernel.security.openidconnect;

import com.google.common.collect.Lists;
import org.fao.geonet.domain.Profile;
import org.fao.geonet.kernel.security.openidconnect.OIDCRoleProcessor;

import java.util.List;
import java.util.stream.Collectors;


/**
 * Custom implementation (ACM-IDM for Metadata Vlaanderen) for the OIDCRoleProcessor.
 */
public class ACMIDMRoleProcessor extends OIDCRoleProcessor {

    public List<String> simpleConvertRoles(List<String> originalRoleNames) {
        String roleGroupSeparator = oidcConfiguration.groupPermissionSeparator;
        String prefix = "DVMetadataVlaanderenGebruiker-";
        return originalRoleNames.stream()
                .filter(s -> s.startsWith(prefix) && s.contains(roleGroupSeparator))
                .map(s -> s.replaceFirst(prefix, ""))
                .flatMap(s -> {
                    String[] split = s.split(roleGroupSeparator);
                    String orgCode = split[1];
                    String idmProfile = convertProfile(split[0]);
                    return getProfiles(orgCode, idmProfile).stream();
                })
                .collect(Collectors.toList());
    }

    /**
     *
     * @param group example: OVO016979
     * @param profile example: Reviewer
     * @return
     */
    private List<String> getProfiles(String group, String profile) {
        // if the group is not identified with an OVO code, do not allow further processing
        if(!group.startsWith("OVO")) {
            return Lists.newArrayList();
        }
        String roleGroupSeparator = oidcConfiguration.groupPermissionSeparator;
        String dpPrefix = "dp-" + group + roleGroupSeparator;
        String mdvPrefix = "mdv-" + group + roleGroupSeparator;
        if (profile.equals(Profile.Administrator.name())) {
            return Lists.newArrayList(dpPrefix + profile,
                    mdvPrefix + profile);
        } else if (profile.equals(Profile.Reviewer.name())) {
            return Lists.newArrayList(dpPrefix + Profile.Editor.name(),
                    mdvPrefix + Profile.Reviewer.name());
        }
        return Lists.newArrayList();
    }

    private String convertProfile(String s) {
        switch (s) {
            case "hoofdeditor":
                return "Reviewer";
            case "editor":
                return "Editor";
            case "admin":
                return "Administrator";
            default:
                return s;
        }
    }
}
