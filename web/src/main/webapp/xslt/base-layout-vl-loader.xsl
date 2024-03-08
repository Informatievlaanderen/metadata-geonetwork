<?xml version="1.0" encoding="UTF-8"?>
<!--
  ~ Copyright (C) 2001-2016 Food and Agriculture Organization of the
  ~ United Nations (FAO-UN), United Nations World Food Programme (WFP)
  ~ and United Nations Environment Programme (UNEP)
  ~
  ~ This program is free software; you can redistribute it and/or modify
  ~ it under the terms of the GNU General Public License as published by
  ~ the Free Software Foundation; either version 2 of the License, or (at
  ~ your option) any later version.
  ~
  ~ This program is distributed in the hope that it will be useful, but
  ~ WITHOUT ANY WARRANTY; without even the implied warranty of
  ~ MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
  ~ General Public License for more details.
  ~
  ~ You should have received a copy of the GNU General Public License
  ~ along with this program; if not, write to the Free Software
  ~ Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA
  ~
  ~ Contact: Jeroen Ticheler - FAO - Viale delle Terme di Caracalla 2,
  ~ Rome - Italy. email: geonetwork@osgeo.org
  -->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version="2.0"
                exclude-result-prefixes="#all">
  <xsl:import href="common/base-variables.xsl"/>

  <!-- have easy access to the vl-specific database settings -->
  <xsl:variable name="vlEnv" select="$env/system/vlaanderen/env"/>
  <xsl:variable name="headerWidgetId" select="$env/system/vlaanderen/header-widget-id"/>
  <xsl:variable name="footerWidgetId" select="$env/system/vlaanderen/footer-widget-id"/>

  <xsl:variable name="widget-host">
    <xsl:choose>
      <xsl:when test="$vlEnv = 'prd'">
        <xsl:value-of select="'https://prod.widgets.burgerprofiel.vlaanderen.be'"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="'https://tni.widgets.burgerprofiel.dev-vlaanderen.be'"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:variable>

  <xsl:template name="define-libraries">
    <script src="{concat($widget-host, '/api/v1/node_modules/%40govflanders/vl-widget-polyfill/dist/index.js')}"/>
    <script src="{concat($widget-host, '/api/v1/node_modules/%40govflanders/vl-widget-client/dist/index.js')}"/>
  </xsl:template>

  <xsl:template name="load-header">
    <script
      src="{concat('https://tni.widgets.burgerprofiel.dev-vlaanderen.be/api/v1/widget/', $headerWidgetId, '/embed')}"/>
  </xsl:template>

  <xsl:template name="load-footer">
    <script
      src="{concat('https://tni.widgets.burgerprofiel.dev-vlaanderen.be/api/v1/widget/', $footerWidgetId, '/embed')}"/>
  </xsl:template>

</xsl:stylesheet>
