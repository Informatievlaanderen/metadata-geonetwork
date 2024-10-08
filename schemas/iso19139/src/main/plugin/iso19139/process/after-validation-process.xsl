<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0"
                xmlns:gmd="http://www.isotc211.org/2005/gmd"
                xmlns:srv="http://www.isotc211.org/2005/srv"
                xmlns:gco="http://www.isotc211.org/2005/gco"
                xmlns:gmx="http://www.isotc211.org/2005/gmx"
                xmlns:xlink="http://www.w3.org/1999/xlink"
                xmlns:xs="http://www.w3.org/2001/XMLSchema"
                xmlns:util="java:org.fao.geonet.util.XslUtil"
                exclude-result-prefixes="#all">

  <xsl:param name="mdId" />

  <xsl:variable name="thesaurusTitle"
                select="'GDI-Vlaanderen Trefwoorden'"/>

  <xsl:variable name="metadataUuid"
                select="//gmd:MD_Metadata/gmd:fileIdentifier/gco:CharacterString"
                as="xs:string"/>

  <xsl:variable name="isVlValid"
                select="util:getRecordValidationStatus(
                          $metadataUuid, 'schematron-rules-GDI-Vlaanderen', $mdId) = '1'"
                as="xs:boolean"/>
  <xsl:variable name="isInspireValid"
                select="util:getRecordValidationStatus(
                          $metadataUuid, 'inspire', $mdId) = '1'"
                as="xs:boolean"/>
  <xsl:variable name="isXsdValid"
                select="util:getRecordValidationStatus(
                          $metadataUuid, 'xsd', $mdId) = '1'"
                as="xs:boolean"/>
  <xsl:variable name="isIsoValid"
                select="util:getRecordValidationStatus(
                          $metadataUuid, 'schematron-rules-iso', $mdId) = '1'"
                as="xs:boolean"/>
  <xsl:variable name="isGeonetworkValid"
                select="util:getRecordValidationStatus(
                          $metadataUuid, 'schematron-rules-geonetwork', $mdId) = '1'"
                as="xs:boolean"/>



  <xsl:template match="/root">
    <xsl:apply-templates select="gmd:MD_Metadata"/>
  </xsl:template>

  <xsl:template match="gmd:MD_Metadata">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="@*|node()">
    <xsl:copy copy-namespaces="no">
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

  <!-- We suppose one keyword block exists. -->
  <xsl:template match="gmd:descriptiveKeywords[1]">
    <xsl:variable name="hasValidationFlagThesaurus"
                  select="count(../gmd:descriptiveKeywords[
                                  gmd:MD_Keywords/gmd:thesaurusName/*/
                                          gmd:title/(gco:CharacterString|gmx:Anchor)
                                          = $thesaurusTitle]) = 1"
                  as="xs:boolean"/>

    <xsl:for-each select="../gmd:descriptiveKeywords">
      <xsl:variable name="isValidationFlagThesaurus"
                    select="gmd:MD_Keywords/gmd:thesaurusName/*/
                          gmd:title/(gco:CharacterString|gmx:Anchor)
                          = $thesaurusTitle"
                    as="xs:boolean"/>
      <xsl:copy>
        <gmd:MD_Keywords>
          <xsl:choose>
            <xsl:when test="$isValidationFlagThesaurus">
              <xsl:apply-templates select="*/gmd:keyword[normalize-space(gco:CharacterString|gmx:Anchor)
                          != 'Metadata GDI-Vl-conform'
                                     and normalize-space(gco:CharacterString|gmx:Anchor)
                          != 'Metadata INSPIRE-conform']"/>

              <xsl:if test="$isInspireValid">
                <gmd:keyword>
                  <gmx:Anchor
                    xlink:href="https://metadata.vlaanderen.be/id/GDI-Vlaanderen-Trefwoorden/MDINSPIRECONFORM">Metadata
                    INSPIRE-conform
                  </gmx:Anchor>
                </gmd:keyword>
              </xsl:if>

              <xsl:if test="$isVlValid and $isGeonetworkValid and $isIsoValid and $isXsdValid">
                <gmd:keyword>
                  <gmx:Anchor xlink:href="https://metadata.vlaanderen.be/id/GDI-Vlaanderen-Trefwoorden/MDGDICONFORM">
                    Metadata GDI-Vl-conform
                  </gmx:Anchor>
                </gmd:keyword>
              </xsl:if>
            </xsl:when>
            <xsl:otherwise>
              <xsl:apply-templates select="*/gmd:keyword"/>
            </xsl:otherwise>
          </xsl:choose>
          <xsl:apply-templates select="*/gmd:type|*/gmd:thesaurusName"/>
        </gmd:MD_Keywords>
      </xsl:copy>
    </xsl:for-each>

    <xsl:if test="not($hasValidationFlagThesaurus)
                  and ($isInspireValid or $isVlValid)">

      <xsl:variable name="thesaurusTitleAnchor"
                    select="'https://metadata.vlaanderen.be/id/GDI-Vlaanderen-Trefwoorden'"/>
      <xsl:variable name="thesaurusTitleString"
                    select="'GDI-Vlaanderen Trefwoorden'"/>
      <xsl:variable name="thesaurusDate"
                    select="'2014-02-26'"/>

      <gmd:descriptiveKeywords>
        <gmd:MD_Keywords>
          <xsl:if test="$isInspireValid">
            <gmd:keyword>
              <gmx:Anchor xlink:href="https://metadata.vlaanderen.be/id/GDI-Vlaanderen-Trefwoorden/MDINSPIRECONFORM">
                Metadata INSPIRE-conform
              </gmx:Anchor>
            </gmd:keyword>
          </xsl:if>
          <xsl:if test="$isVlValid">
            <gmd:keyword>
              <gmx:Anchor xlink:href="https://metadata.vlaanderen.be/id/GDI-Vlaanderen-Trefwoorden/MDGDICONFORM">
                Metadata GDI-Vl-conform
              </gmx:Anchor>
            </gmd:keyword>
          </xsl:if>
          <gmd:type>
            <gmd:MD_KeywordTypeCode
              codeList="http://standards.iso.org/iso/19139/resources/gmxCodelists.xml#MD_KeywordTypeCode"
              codeListValue="theme"/>
          </gmd:type>
          <gmd:thesaurusName>
            <gmd:CI_Citation>
              <gmd:title>
                <gmx:Anchor xlink:href="{$thesaurusTitleAnchor}">
                  <xsl:value-of select="$thesaurusTitleString"/>
                </gmx:Anchor>
              </gmd:title>
              <gmd:date>
                <gmd:CI_Date>
                  <gmd:date>
                    <gco:Date>
                      <xsl:value-of select="$thesaurusDate"/>
                    </gco:Date>
                  </gmd:date>
                  <gmd:dateType>
                    <gmd:CI_DateTypeCode
                      codeList="http://standards.iso.org/iso/19139/resources/gmxCodelists.xml#CI_DateTypeCode"
                      codeListValue="publication"/>
                  </gmd:dateType>
                </gmd:CI_Date>
              </gmd:date>
            </gmd:CI_Citation>
          </gmd:thesaurusName>
        </gmd:MD_Keywords>
      </gmd:descriptiveKeywords>
    </xsl:if>
  </xsl:template>

  <xsl:template match="gmd:descriptiveKeywords"/>

</xsl:stylesheet>
