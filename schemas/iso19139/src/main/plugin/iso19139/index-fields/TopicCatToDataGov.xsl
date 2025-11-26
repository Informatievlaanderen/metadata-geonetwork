<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet xmlns:xs="http://www.w3.org/2001/XMLSchema"
                xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                xmlns:skos="http://www.w3.org/2004/02/skos/core#"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:geonet="http://www.fao.org/geonetwork"
                xmlns:util="java:org.fao.geonet.util.XslUtil"
                exclude-result-prefixes="#all"
                version="2.0">

  <xsl:variable name="dataTheme" select="document('./thesauri/belgif-datatheme.rdf')"/>

  <xsl:template name="mapTopicCatToKeywordElement">
    <xsl:param name="topicCategories" as="node()*"/>
    <xsl:variable name="themeURIs">
      <xsl:for-each select="$topicCategories/*/string()">
        <uri>
          <xsl:value-of select="geonet:mapTopicCatToDataGovThemeURI(.)"/>
        </uri>
      </xsl:for-each>
    </xsl:variable>
    <xsl:variable name="concepts">
      <xsl:for-each select="$themeURIs/uri[normalize-space() != '']">
        <xsl:variable name="uri" select="string()"/>
        <xsl:copy-of select="$dataTheme/rdf:RDF/skos:Concept[@rdf:about = $uri]"/>
      </xsl:for-each>
    </xsl:variable>
    <xsl:for-each select="$concepts/*">
      <keyword>
        <xsl:attribute name="uri" select="string(@rdf:about)"/>
        <values>
          <value>"default":"<xsl:value-of select="skos:prefLabel[@xml:lang = 'nl']"/>"</value>
          <xsl:for-each select="skos:prefLabel">
            <value>"<xsl:value-of select="concat('lang', geonet:twoCharToThreeCharLangCode(string(@xml:lang)))"/>":"<xsl:value-of select="normalize-space()"/>"</value>
          </xsl:for-each>
          <value>"link":"<xsl:value-of select="util:escapeForJson(string(@rdf:about))"/>"</value>
        </values>
        <tree>
          <defaults>
            <value>
              <xsl:value-of select="skos:prefLabel[@xml:lang = 'nl']"/>
            </value>
          </defaults>
          <keys>
            <value>
              <xsl:value-of select="string(@rdf:about)"/>
            </value>
          </keys>
        </tree>
      </keyword>
    </xsl:for-each>
  </xsl:template>

  <xsl:function name="geonet:twoCharToThreeCharLangCode">
    <xsl:param name="twoCharLangCode"/>
    <xsl:choose>
      <xsl:when test="$twoCharLangCode = 'nl'">dut</xsl:when>
      <xsl:when test="$twoCharLangCode = 'fr'">fre</xsl:when>
      <xsl:when test="$twoCharLangCode = 'en'">eng</xsl:when>
      <xsl:when test="$twoCharLangCode = 'de'">ger</xsl:when>
      <xsl:otherwise>dut</xsl:otherwise>
    </xsl:choose>
  </xsl:function>

  <xsl:function name="geonet:mapTopicCatToDataGovThemeURI">
    <xsl:param name="topicCategory" as="xs:string"/>

    <xsl:variable name="theme">
      <xsl:choose>
        <xsl:when test="$topicCategory = 'farming'">
          <xsl:value-of select="'AGRI'"/>
        </xsl:when>
        <xsl:when test="$topicCategory = 'biota'">
          <xsl:value-of select="'ENVI'"/>
        </xsl:when>
        <xsl:when test="$topicCategory = 'boundaries'">
          <xsl:value-of select="''"/>
        </xsl:when>
        <xsl:when test="$topicCategory = 'climatologyMeteorologyAtmosphere'">
          <xsl:value-of select="'ENVI'"/>
        </xsl:when>
        <xsl:when test="$topicCategory = 'economy'">
          <xsl:value-of select="'ECON'"/>
        </xsl:when>
        <xsl:when test="$topicCategory = 'elevation'">
          <xsl:value-of select="'ENVI'"/>
        </xsl:when>
        <xsl:when test="$topicCategory = 'environment'">
          <xsl:value-of select="'ENVI'"/>
        </xsl:when>
        <xsl:when test="$topicCategory = 'geoscientificInformation'">
          <xsl:value-of select="'TECH'"/>
        </xsl:when>
        <xsl:when test="$topicCategory = 'health'">
          <xsl:value-of select="'HEAL'"/>
        </xsl:when>
        <xsl:when test="$topicCategory = 'imageryBaseMapsEarthCover'">
          <xsl:value-of select="'ENVI'"/>
        </xsl:when>
        <xsl:when test="$topicCategory = 'intelligenceMilitary'">
          <xsl:value-of select="''"/>
        </xsl:when>
        <xsl:when test="$topicCategory = 'inlandWaters'">
          <xsl:value-of select="'ENVI'"/>
        </xsl:when>
        <xsl:when test="$topicCategory = 'location'">
          <xsl:value-of select="'ENVI'"/>
        </xsl:when>
        <xsl:when test="$topicCategory = 'oceans'">
          <xsl:value-of select="'ENVI'"/>
        </xsl:when>
        <xsl:when test="$topicCategory = 'planningCadastre'">
          <xsl:value-of select="'ENVI'"/>
        </xsl:when>
        <xsl:when test="$topicCategory = 'society'">
          <xsl:value-of select="'SOCI'"/>
        </xsl:when>
        <xsl:when test="$topicCategory = 'structure'">
          <xsl:value-of select="''"/>
        </xsl:when>
        <xsl:when test="$topicCategory = 'transportation'">
          <xsl:value-of select="'TRAN'"/>
        </xsl:when>
        <xsl:when test="$topicCategory = 'utilitiesCommunication'">
          <xsl:value-of select="''"/>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="''"/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:variable>
    <xsl:if test="$theme != ''">
      <xsl:value-of select="concat('http://vocab.belgif.be/auth/datatheme/' , $theme)"/>
    </xsl:if>
  </xsl:function>
</xsl:stylesheet>
