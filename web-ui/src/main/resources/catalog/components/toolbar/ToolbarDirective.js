/*
 * Copyright (C) 2001-2023 Food and Agriculture Organization of the
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

(function () {
  goog.provide("gn_toolbar_directive");

  var module = angular.module("gn_toolbar_directive", []);

  module.constant("GN_DEFAULT_MENU", [
    "gn-site-name-menu",
    "gn-portal-switcher",
    "gn-search-menu",
    "gn-map-menu",
    "gn-contribute-menu",
    "gn-admin-menu",
    "gn-static-pages-list-viewer"
  ]);

  module.directive("gnToolbar", [
    "GN_DEFAULT_MENU",
    "gnGlobalSettings",
    function (GN_DEFAULT_MENU, gnGlobalSettings) {
      return {
        templateUrl: "../../catalog/views/default/templates/aiv-header.html",
        link: function ($scope) {
          $scope.toolbarMenu =
            gnGlobalSettings.gnCfg.mods.header.topCustomMenu &&
            gnGlobalSettings.gnCfg.mods.header.topCustomMenu.length > 0
              ? gnGlobalSettings.gnCfg.mods.header.topCustomMenu
              : GN_DEFAULT_MENU;

          $scope.isPage = function (page) {
            return angular.isObject(page) || page.indexOf("gn-") === -1;
          };
        }
      };
    }
  ]);
  module.directive("gnSiteNameMenu", [
    function () {
      return {
        replace: true,
        templateUrl: "../../catalog/components/toolbar/partials/menu-sitename.html"
      };
    }
  ]);
  module.directive("gnSearchMenu", [
    function () {
      return {
        replace: true,
        templateUrl: "../../catalog/components/toolbar/partials/menu-search.html"
      };
    }
  ]);
  module.directive("gnMapMenu", [
    function () {
      return {
        replace: true,
        templateUrl: "../../catalog/components/toolbar/partials/menu-map.html"
      };
    }
  ]);
  module.directive("gnContributeMenu", [
    function () {
      return {
        replace: true,
        templateUrl: "../../catalog/components/toolbar/partials/menu-contribute.html"
      };
    }
  ]);
  module.directive("gnAdminMenu", [
    function () {
      return {
        replace: true,
        templateUrl: "../../catalog/components/toolbar/partials/menu-admin.html"
      };
    }
  ]);
  module.directive("gnSigninMenu", [
    "$http",
    function ($http) {
      return {
        replace: true,
        templateUrl: "../../catalog/views/default/templates/aiv-signin.html",
        link: function ($scope) {
          $scope.$watch("$parent.user.id", function (newValue, oldValue) {
            if (newValue && newValue !== oldValue) {
              return $http
                .get("../api/users/" + newValue + "/groups", { cache: true })
                .then(function (response) {
                  var uniqueGroupNames = [];
                  response.data.forEach(function (g) {
                    var name = g.group.label[$scope.lang];
                    if (uniqueGroupNames.indexOf(name) === -1) {
                      uniqueGroupNames.push(name);
                    }
                  });
                  $scope.userGroups = uniqueGroupNames;
                });
            }
          });

          $scope.initials = function (user) {
            var result = "";
            if (user) {
              if (user.name && user.name.length > 0) {
                result += user.name.charAt(0) + ".";
              }
              if (user.surname && user.surname.length > 0) {
                result += user.surname.charAt(0) + ".";
              }
              if (result.length === 0 && user.username && user.username.length > 0) {
                result += user.username.charAt(0) + ".";
              }
            }
            if (result.length === 0) {
              result = "?";
            }
            return result.toUpperCase();
          };
        }
      };
    }
  ]);
  module.directive("gnLanguagesMenu", [
    function () {
      return {
        replace: true,
        templateUrl: "../../catalog/views/default/templates/aiv-menu-languages.html"
      };
    }
  ]);
})();
