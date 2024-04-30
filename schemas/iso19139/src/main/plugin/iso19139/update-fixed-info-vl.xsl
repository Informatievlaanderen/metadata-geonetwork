<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:gml="http://www.opengis.net/gml/3.2"
                xmlns:gml320="http://www.opengis.net/gml"
                xmlns:srv="http://www.isotc211.org/2005/srv"
                xmlns:gco="http://www.isotc211.org/2005/gco"
                xmlns:gmd="http://www.isotc211.org/2005/gmd"
                xmlns:gmx="http://www.isotc211.org/2005/gmx"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xmlns:xlink="http://www.w3.org/1999/xlink"
                xmlns:java="java:org.fao.geonet.util.XslUtil"
                version="2.0" exclude-result-prefixes="#all">

  <xsl:variable name="metadataStandardNameForDatasetAndSeries">ISO 19115/2003/Cor.1:2006/INSPIRE-TG2.0</xsl:variable>
  <xsl:variable name="metadataStandardNameForService">ISO 19119:2005/Amd 1:2008/INSPIRE-TG2.0</xsl:variable>
  <xsl:variable name="metadataStandardVersion">GDI-Vlaanderen Best Practices - versie 2.0</xsl:variable>


  <xsl:template match="gmd:MD_Metadata" priority="9000">
    <xsl:copy copy-namespaces="no">
      <xsl:call-template name="add-namespaces"/>
      <xsl:call-template name="handle-root-attributes"/>

      <gmd:fileIdentifier>
        <gco:CharacterString>
          <xsl:value-of select="/root/env/uuid"/>
        </gco:CharacterString>
      </gmd:fileIdentifier>

      <xsl:apply-templates select="gmd:language"/>
      <xsl:apply-templates select="gmd:characterSet"/>

      <xsl:choose>
        <xsl:when test="/root/env/parentUuid!=''">
          <gmd:parentIdentifier>
            <gco:CharacterString>
              <xsl:value-of select="/root/env/parentUuid"/>
            </gco:CharacterString>
          </gmd:parentIdentifier>
        </xsl:when>
        <xsl:when test="gmd:parentIdentifier">
          <xsl:apply-templates select="gmd:parentIdentifier"/>
        </xsl:when>
      </xsl:choose>

      <xsl:apply-templates select="
        gmd:hierarchyLevel|
        gmd:hierarchyLevelName|
        gmd:contact|
        gmd:dateStamp|
        gmd:metadataStandardName|
        gmd:metadataStandardVersion|
        gmd:dataSetURI"/>

      <!-- Copy existing locales and create an extra one for the default metadata language. -->
      <xsl:if test="$isMultilingual">
        <xsl:apply-templates select="gmd:locale[*/gmd:languageCode/*/@codeListValue != $mainLanguage]"/>
        <gmd:locale>
          <gmd:PT_Locale id="{$mainLanguageId}">
            <gmd:languageCode>
              <gmd:LanguageCode codeList="http://www.loc.gov/standards/iso639-2/"
                                codeListValue="{$mainLanguage}"/>
            </gmd:languageCode>
            <gmd:characterEncoding>
              <gmd:MD_CharacterSetCode codeList="http://standards.iso.org/iso/19139/resources/gmxCodelists.xml#MD_CharacterSetCode"
                codeListValue="{$defaultEncoding}"/>
            </gmd:characterEncoding>
            <!-- Apply country if it exists.  -->
            <xsl:apply-templates select="gmd:locale/gmd:PT_Locale[gmd:languageCode/*/@codeListValue = $mainLanguage]/gmd:country"/>
          </gmd:PT_Locale>
        </gmd:locale>
      </xsl:if>

      <xsl:apply-templates select="
        gmd:spatialRepresentationInfo|
        gmd:referenceSystemInfo|
        gmd:metadataExtensionInfo|
        gmd:identificationInfo|
        gmd:contentInfo|
        gmd:distributionInfo|
        gmd:dataQualityInfo|
        gmd:portrayalCatalogueInfo|
        gmd:metadataConstraints|
        gmd:applicationSchemaInfo|
        gmd:metadataMaintenance|
        gmd:series|
        gmd:describes|
        gmd:propertyType|
        gmd:featureType|
        gmd:featureAttribute"/>

      <!-- Handle ISO profiles extensions. -->
      <xsl:apply-templates select="
        *[namespace-uri()!='http://www.isotc211.org/2005/gmd' and
          namespace-uri()!='http://www.isotc211.org/2005/srv']"/>
    </xsl:copy>
  </xsl:template>


  <!--  only accept the pointOfContact role code for a gmd:contact element -->
  <xsl:template match="gmd:role[name(../..)='gmd:contact']" priority="9000">
    <gmd:role>
      <gmd:CI_RoleCode codeList="http://standards.iso.org/iso/19139/resources/gmxCodelists.xml#CI_RoleCode" codeListValue="pointOfContact"/>
    </gmd:role>
  </xsl:template>


  <xsl:template match="gmd:dateTime" priority="9000">
    <xsl:variable name="child" select="gco:Date|gco:DateTime"/>
    <xsl:copy copy-namespaces="no">
      <xsl:if test="normalize-space($child) = ''">
        <xsl:attribute name="gco:nilReason" select="'missing'"/>
      </xsl:if>
      <xsl:if test="not(normalize-space($child) = '')">
        <gco:DateTime>
          <xsl:value-of select="$child"/>
        </gco:DateTime>
      </xsl:if>
    </xsl:copy>
  </xsl:template>


  <!-- Only gmd:referenceSystemIdentifier can have a gmd:RS_Identifier child element, all other RS_Identifier elements
      must be transformed to a MD:Identifier and existing child elements gmd:codeSpace and gmd:version must be removed -->
  <xsl:template match="gmd:RS_Identifier[not(name(..)='gmd:referenceSystemIdentifier')]" priority="9000">
    <gmd:MD_Identifier>
      <xsl:apply-templates select="@*"/>
      <xsl:apply-templates select="*[not(name(.)='gmd:codeSpace' or name(.)='gmd:version')]"/>
    </gmd:MD_Identifier>
  </xsl:template>


  <xsl:template match="*[not(name() = ('gmd:dateStamp', 'gmd:dateTime')) and gco:DateTime]" priority="9000">
    <xsl:variable name="child" select="gco:DateTime"/>
    <xsl:copy copy-namespaces="no">
      <xsl:if test="normalize-space($child) = ''">
        <xsl:attribute name="gco:nilReason" select="'missing'"/>
      </xsl:if>
      <xsl:if test="not(normalize-space($child) = '')">
        <xsl:apply-templates select="@*|node()"/>
      </xsl:if>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="*[not(name() = ('gmd:dateStamp', 'gmd:dateTime')) and gco:Date]" priority="9000">
    <xsl:variable name="child" select="gco:Date"/>
    <xsl:copy copy-namespaces="no">
      <xsl:if test="normalize-space($child) = ''">
        <xsl:attribute name="gco:nilReason" select="'missing'"/>
      </xsl:if>
      <xsl:if test="not(normalize-space($child) = '')">
        <xsl:apply-templates select="@*|node()"/>
      </xsl:if>
    </xsl:copy>
  </xsl:template>


  <!-- @Override -->
  <!-- uuidref is always the dataset identifier and never the fileIdentifier. We should not use it for building the xlink:href -->
  <!-- Commit ref: 32ecb677b27ebfdfd709364acfc0e4cee4d57dd0 -->
  <!-- TODO: Check with François dataset-add.xsl "TODO" => issue to fix in the core ? -->
  <xsl:template match="srv:operatesOn|gmd:featureCatalogueCitation" priority="9000">
    <xsl:copy copy-namespaces="no">
      <xsl:copy-of select="@*[name() != 'xlink:href']"/>
      <xsl:choose>
        <xsl:when test="@uuidref or @xlink:href">
          <xsl:copy-of select="@xlink:href"/>
        </xsl:when>
        <xsl:otherwise>
          <xsl:apply-templates select="node()" />
        </xsl:otherwise>
      </xsl:choose>
      <xsl:for-each select="gmd:CI_Citation">
        <xsl:copy copy-namespaces="no">
          <xsl:apply-templates select="node()"/>
        </xsl:copy>
      </xsl:for-each>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="gmd:pass" priority="9000">
    <xsl:copy copy-namespaces="no">
      <xsl:choose>
        <xsl:when test="not(gco:Boolean) or normalize-space(gco:Boolean) = ''">
          <xsl:attribute name="gco:nilReason" select="'unknown'"/>
        </xsl:when>
        <xsl:otherwise>
          <xsl:apply-templates select="@*[not(name() = 'gco:nilReason')]|*"/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:copy>
  </xsl:template>


  <!-- Commit cdcb4310eb95f47de5be5fc35fb30a0482720376 not picked back for custom  -->
  <!-- Commit 52737e71bd72b3429a9a005965abf6bd78a91d28 not picked back for custom  -->

  <xsl:template match="gmd:dateStamp" priority="9000">
    <xsl:choose>
      <xsl:when test="/root/env/changeDate">
        <xsl:copy copy-namespaces="no">
          <gco:Date>
            <xsl:choose>
              <xsl:when test="contains(/root/env/changeDate, 'T')">
                <xsl:value-of select="format-dateTime(/root/env/changeDate, '[Y0001]-[M01]-[D01]')"/>
              </xsl:when>
              <xsl:otherwise>
                <xsl:value-of select="format-date(/root/env/changeDate, '[Y0001]-[M01]-[D01]')"/>
              </xsl:otherwise>
            </xsl:choose>
          </gco:Date>
        </xsl:copy>
      </xsl:when>
      <xsl:otherwise>
        <xsl:copy-of select="."/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <!-- Set the required hierarchyLevelName for dataset, service and series, see TG 2.0 -->
  <!-- Remove gmd:hierarchyLevelName for gmd:MD_ScopeCode with codeListValue dataset, series and service -->
  <xsl:template match="gmd:hierarchyLevelName[lower-case(../gmd:hierarchyLevel/gmd:MD_ScopeCode/@codeListValue) = ('dataset','series','service')]" priority="9000"/>

  <!-- Change gmd:hierarchyLevelName -->
  <xsl:template match="gmd:hierarchyLevel[lower-case(gmd:MD_ScopeCode/@codeListValue) = ('dataset','series','service')]" priority="9000">
    <xsl:copy copy-namespaces="no">
      <gmd:MD_ScopeCode codeList="http://standards.iso.org/iso/19139/resources/gmxCodelists.xml#MD_ScopeCode" codeListValue="{lower-case(gmd:MD_ScopeCode/@codeListValue)}"/>
    </xsl:copy>
    <xsl:variable name="hierarchyLevelNameValue">
      <xsl:choose>
        <xsl:when test="lower-case(gmd:MD_ScopeCode/@codeListValue) = 'dataset'">Dataset</xsl:when>
        <xsl:when test="lower-case(gmd:MD_ScopeCode/@codeListValue) = 'series'">Datasetserie</xsl:when>
        <xsl:when test="lower-case(gmd:MD_ScopeCode/@codeListValue) = 'service'">Dienst</xsl:when>
      </xsl:choose>
    </xsl:variable>
    <gmd:hierarchyLevelName>
      <gco:CharacterString>
        <xsl:value-of select="$hierarchyLevelNameValue"/>
      </gco:CharacterString>
    </gmd:hierarchyLevelName>
  </xsl:template>


  <!-- Change elements -->
  <xsl:template match="gmd:metadataStandardName[lower-case(../gmd:hierarchyLevel/gmd:MD_ScopeCode/@codeListValue) = ('series','dataset')]" priority="9000">
    <xsl:copy copy-namespaces="no">
      <gco:CharacterString>
        <xsl:value-of select="$metadataStandardNameForDatasetAndSeries"/>
      </gco:CharacterString>
    </xsl:copy>
    <xsl:if test="count(../gmd:metadataStandardVersion) = 0">
      <gmd:metadataStandardVersion>
        <gco:CharacterString>
          <xsl:value-of select="$metadataStandardVersion"/>
        </gco:CharacterString>
      </gmd:metadataStandardVersion>
    </xsl:if>
  </xsl:template>

  <xsl:template match="gmd:metadataStandardVersion[lower-case(../gmd:hierarchyLevel/gmd:MD_ScopeCode/@codeListValue) = ('series','dataset')]" priority="9000">
    <xsl:if test="count(../gmd:metadataStandardName) = 0">
      <gmd:metadataStandardName>
        <gco:CharacterString>
          <xsl:value-of select="$metadataStandardNameForDatasetAndSeries"/>
        </gco:CharacterString>
      </gmd:metadataStandardName>
    </xsl:if>
    <xsl:copy copy-namespaces="no">
      <gco:CharacterString>
        <xsl:value-of select="$metadataStandardVersion"/>
      </gco:CharacterString>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="gmd:metadataStandardName[lower-case(../gmd:hierarchyLevel/gmd:MD_ScopeCode/@codeListValue) = 'service']" priority="9000">
    <xsl:copy copy-namespaces="no">
      <gco:CharacterString>
        <xsl:value-of select="$metadataStandardNameForService"/>
      </gco:CharacterString>
    </xsl:copy>
    <xsl:if test="count(../gmd:metadataStandardVersion) = 0">
      <gmd:metadataStandardVersion>
        <gco:CharacterString>
          <xsl:value-of select="$metadataStandardVersion"/>
        </gco:CharacterString>
      </gmd:metadataStandardVersion>
    </xsl:if>
  </xsl:template>

  <xsl:template match="gmd:metadataStandardVersion[lower-case(../gmd:hierarchyLevel/gmd:MD_ScopeCode/@codeListValue) = 'service']" priority="9000">
    <xsl:if test="count(../gmd:metadataStandardName) = 0">
      <gmd:metadataStandardName>
        <gco:CharacterString>
          <xsl:value-of select="$metadataStandardNameForService"/>
        </gco:CharacterString>
      </gmd:metadataStandardName>
    </xsl:if>
    <xsl:copy copy-namespaces="no">
      <gco:CharacterString>
        <xsl:value-of select="$metadataStandardVersion"/>
      </gco:CharacterString>
    </xsl:copy>
  </xsl:template>



  <xsl:template match="gmd:metadataStandardName[@gco:nilReason='missing' or gco:CharacterString='']|gmd:metadataStandardVersion[@gco:nilReason='missing' or gco:CharacterString='']" priority="9000">
    <!-- Equivalent of commenting the core template by re-applying the default logic for unmatched elements -->
    <xsl:copy copy-namespaces="no">
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>


  <xsl:template match="gmd:LanguageCode[@codeListValue]" priority="9001">
    <gmd:LanguageCode codeList="http://www.loc.gov/standards/iso639-2/">
      <xsl:apply-templates select="@*[name(.)!='codeList']"/>
      <!-- Keep the translation for the codeListValue attribute in the xml if exists, see TG 2.0 -->
      <xsl:apply-templates select="node()"/>
    </gmd:LanguageCode>
  </xsl:template>


  <xsl:template match="gmd:*[@codeListValue]" priority="9000">
    <xsl:copy copy-namespaces="no">
      <xsl:apply-templates select="@*[name(.)!='codeList']"/>
      <xsl:attribute name="codeList">
        <xsl:value-of select="concat('http://standards.iso.org/iso/19139/resources/gmxCodelists.xml#', local-name(.))"/>
      </xsl:attribute>
      <!-- Keep the translation for the codeListValue attribute in the xml if exists and when required, see TG 2.0 -->
      <xsl:apply-templates select="node()"/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="@gml:id|@gml320:id" priority="9000">

    <xsl:variable name="value" select="if (normalize-space(.) = '') then generate-id(.) else normalize-space()"/>
    <xsl:variable name="namespace"
                  select="if($isUsing2005Schema)
                          then 'http://www.opengis.net/gml'
                          else 'http://www.opengis.net/gml/3.2'"/>
    <xsl:attribute name="gml:id" namespace="{$namespace}" select="$value"/>
  </xsl:template>


  <xsl:template match="gml:verticalCS|gml:verticalDatum|gml320:verticalCS|gml320:verticalDatum" priority="9000">
    <xsl:variable name="childExists" select="count(*[local-name(.)='VerticalCS']) + count(*[local-name(.)='VerticalDatum']) != 0"/>
    <xsl:copy copy-namespaces="no">
      <xsl:if test="$childExists">
        <xsl:apply-templates select="@*[local-name(.)!='nilReason']"/>
        <xsl:apply-templates select="node()"/>
      </xsl:if>
      <xsl:if test="not($childExists)">
        <xsl:attribute name="nilReason" select="'missing'"/>
      </xsl:if>
    </xsl:copy>
  </xsl:template>


  <xsl:template match="gmd:date[gmd:CI_Date]" priority="9000">
    <xsl:if test="count(gmd:CI_Date/gmd:date) > 0 and count(gmd:CI_Date/gmd:dateType/*) > 0">
      <xsl:copy copy-namespaces="no">
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
    </xsl:if>
  </xsl:template>

  <!-- Remove the conformity keywords after each update -->
   <xsl:template
     match="gmd:keyword[gmx:Anchor/@xlink:href= (
      'https://metadata.vlaanderen.be/id/GDI-Vlaanderen-Trefwoorden/MDINSPIRECONFORM',
      'https://metadata.vlaanderen.be/id/GDI-Vlaanderen-Trefwoorden/MDGDICONFORM'
     )]"
     priority="9001"/>


  <!-- Fix INSPIRE codelist still under HTTPS instead of HTTP -->
  <xsl:template match="@*[starts-with(string(), 'https://inspire.ec.europa.eu')]" priority="9000">
    <xsl:attribute name="{name()}" select="replace(., 'https://inspire.ec.europa.eu', 'http://inspire.ec.europa.eu')"/>
  </xsl:template>


  <xsl:template match="gmd:dateTime|gmd:plannedAvailableDateTime|gmd:usageDateTime"
                priority="9001">
    <xsl:variable name="value" select="gco:Date|gco:DateTime" />
    <xsl:choose>
      <xsl:when test="normalize-space($value) = '' or starts-with(normalize-space($value), 'null')">
        <xsl:copy copy-namespaces="no">
          <xsl:attribute name="gco:nilReason" select="'missing'"/>
        </xsl:copy>
      </xsl:when>
      <xsl:otherwise>
        <xsl:copy copy-namespaces="no">
          <gco:DateTime>
            <xsl:value-of select="$value" /><xsl:if test="string-length($value) = 10">T00:00:00</xsl:if>
          </gco:DateTime>
        </xsl:copy>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template match="gmd:date/gco:DateTime|gmd:date/gco:Date" priority="9000">
    <gco:Date>
      <xsl:choose>
        <xsl:when test="contains(string(), 'T')">
          <xsl:value-of select="format-dateTime(., '[Y0001]-[M01]-[D01]')"/>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="format-date(., '[Y0001]-[M01]-[D01]')"/>
        </xsl:otherwise>
      </xsl:choose>
    </gco:Date>
  </xsl:template>

  <xsl:template name="handle-root-attributes">
    <xsl:choose>
      <xsl:when test="java:getSettingValue('system/metadata/validation/removeSchemaLocation') = 'false'">
        <xsl:choose>
          <xsl:when test="$isUsing2005Schema">
            <xsl:apply-templates select="@*[name() != 'xsi:schemaLocation']"/>
            <xsl:attribute name="xsi:schemaLocation"
                           select="'http://www.isotc211.org/2005/gmx http://schemas.opengis.net/iso/19139/20060504/gmx/gmx.xsd http://www.isotc211.org/2005/srv http://schemas.opengis.net/iso/19139/20060504/srv/srv.xsd http://www.isotc211.org/2005/gmd http://schemas.opengis.net/iso/19139/20060504/gmd/gmd.xsd'"/>
          </xsl:when>
          <xsl:when test="$isUsing2007Schema">
            <xsl:apply-templates select="@*[name() != 'xsi:schemaLocation']"/>
            <xsl:attribute name="xsi:schemaLocation"
                           select="'http://www.isotc211.org/2005/gmx http://schemas.opengis.net/iso/19139/20070417/gmx/gmx.xsd http://www.isotc211.org/2005/srv http://schemas.opengis.net/iso/19139/20070417/srv/1.0/srv.xsd http://www.isotc211.org/2005/gmd http://schemas.opengis.net/iso/19139/20070417/gmd/gmd.xsd'"/>
          </xsl:when>
          <xsl:otherwise>
            <xsl:apply-templates select="@*"/>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:when>
      <xsl:otherwise>
        <xsl:apply-templates select="@*[name() != 'xsi:schemaLocation']"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>



  <!-- TODO: Continue incremental check on update-fixed-info diff: http://gitlab.gim.be/gim-geonetwork/core-geonetwork/-/commits/clients/aiv/main/schemas/iso19139/src/main/plugin/iso19139/update-fixed-info.xsl   -->
</xsl:stylesheet>
