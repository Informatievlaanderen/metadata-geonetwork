<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<!--GDI-Vlaanderen Metadata Best practices Schematron regels -->
<!-- 2013-01-30 Versie 0.9 -->
<sch:schema xmlns:sch="http://purl.oclc.org/dsdl/schematron" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" queryBinding="xslt2">
	<sch:title xmlns="http://www.w3.org/2001/XMLSchema">Technisch GDI Vlaanderen voorschrift voor metadata 3.0</sch:title>
	<sch:ns prefix="gml" uri="http://www.opengis.net/gml/3.2"/>
  <sch:ns prefix="gml320" uri="http://www.opengis.net/gml"/>
	<sch:ns prefix="gmd" uri="http://www.isotc211.org/2005/gmd"/>
	<sch:ns prefix="srv" uri="http://www.isotc211.org/2005/srv"/>
	<sch:ns prefix="gco" uri="http://www.isotc211.org/2005/gco"/>
	<sch:ns prefix="geonet" uri="http://www.fao.org/geonetwork"/>
  <sch:ns prefix="rdf" uri="http://www.w3.org/1999/02/22-rdf-syntax-ns#"/>
	<sch:ns prefix="skos" uri="http://www.w3.org/2004/02/skos/core#"/>
	<sch:ns prefix="xlink" uri="http://www.w3.org/1999/xlink"/>
	<!-- GDI-Vlaanderen SC1 -->
	<sch:pattern>
		<sch:title>GDI-Vlaanderen SC-1: gmd:MD_Metadata/gmd:fileIdentifier (Iso element nr. 2) is verplicht aanwezig en niet leeg.</sch:title>
		<sch:rule context="//gmd:MD_Metadata">
			<sch:let name="fileIdentifier" value="gmd:fileIdentifier and not(normalize-space(gmd:fileIdentifier) = '')"/>
			<sch:let name="fileIdentifierValue" value="gmd:fileIdentifier/*/text()"/>
			<sch:assert test="$fileIdentifier">gmd:fileIdentifier ontbreekt of is leeg</sch:assert>
			<sch:report test="$fileIdentifier">gmd:fileIdentifier is aanwezig: <sch:value-of select="$fileIdentifierValue"/>
			</sch:report>
		</sch:rule>
	</sch:pattern>
	<!-- GDI-Vlaanderen SC2 -->
	<sch:pattern>
		<sch:title>GDI-Vlaanderen SC-2: MD_Metadata.referenceSystemInfo/*/RS_identifier/code (ISO element nr 207) is aanwezig en niet leeg. </sch:title>

        <sch:rule context="//gmd:MD_Metadata[
             gmd:hierarchyLevel/gmd:MD_ScopeCode/@codeListValue/normalize-space(.) = 'series'
             or gmd:hierarchyLevel/gmd:MD_ScopeCode/@codeListValue/normalize-space(.) = 'dataset'
             or gmd:hierarchyLevel/gmd:MD_ScopeCode/@codeListValue/normalize-space(.) = '']">
                            <sch:let name="referenceSystemInfo" value="gmd:referenceSystemInfo"/>
             <sch:assert test="$referenceSystemInfo">
                   Referentie systeem ontbreekt Er dient een horizontaal of verticaal referentiesysteem gedocumenteerd te worden.
                  </sch:assert>
        </sch:rule>

		<sch:rule context="//gmd:MD_Metadata[
        			gmd:hierarchyLevel/gmd:MD_ScopeCode/@codeListValue/normalize-space(.) = 'series'
        			or gmd:hierarchyLevel/gmd:MD_ScopeCode/@codeListValue/normalize-space(.) = 'dataset'
        			or gmd:hierarchyLevel/gmd:MD_ScopeCode/@codeListValue/normalize-space(.) = '']/gmd:referenceSystemInfo">
                        <sch:let name="ReferenceSystemInfo" value="not(normalize-space(gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:code)= '')"/>
        			<sch:let name="ReferenceSystemInfoCodeValue" value="gmd:MD_ReferenceSystem/gmd:referenceSystemIdentifier/gmd:RS_Identifier/gmd:code/*/text()"/>
        			<sch:assert test="$ReferenceSystemInfo">
              		Referentie systeem code ontbreekt of is leeg.  Er dient een horizontaal of verticaal referentiesysteem gedocumenteerd te worden.
              </sch:assert>
        			<sch:report test="$ReferenceSystemInfo">Code van een horizontaal of verticaal referentiesysteem is aanwezig:  <sch:value-of select="$ReferenceSystemInfoCodeValue"/>
        			</sch:report>
        		</sch:rule>
	</sch:pattern>
	<!-- GDI-Vlaanderen SC3 -->
	<sch:pattern>
		<sch:title>GDI-Vlaanderen SC-3: organisationName (ISO-element 376) is aanwezig binnen elk voorkomen van CI_ResponsibleParty en is niet leeg.</sch:title>
		<sch:rule context="//*/gmd:CI_ResponsibleParty/gmd:organisationName">
			<sch:let name="organisationName" value=". and not(normalize-space(.)= '')"/>
			<sch:let name="organisationNameValue" value="./*/text()"/>
			<sch:assert test="$organisationName">Naam van de verantwoordelijke organisatie ontbreekt of is leeg.</sch:assert>
			<sch:report test="$organisationName">Naam van de verantwoordelijke organisatie is aanwezig : <sch:value-of select="$organisationNameValue"/>
			</sch:report>
		</sch:rule>
	</sch:pattern>
	<!-- GDI-Vlaanderen SC4 -->
	<sch:pattern>
		<sch:title>GDI-Vlaanderen SC-4: Objectencatalogus is onderdeel van de dataset (= aangevinkt) (ISO-element 236). Objectencatalogus identifier mag daarom niet leeg zijn.</sch:title>
		<sch:rule context="//gmd:contentInfo/gmd:MD_FeatureCatalogueDescription/gmd:includedWithDataset">
			<sch:let name="uuidrefValueArray" value="../gmd:featureCatalogueCitation/@uuidref"/>
			<sch:let name="uuidrefValue" value="normalize-space($uuidrefValueArray[1])"/>
			<sch:let name="uuidrefIsValid" value="not(normalize-space(gco:Boolean)='true') or $uuidrefValue!=''"/>
			<sch:assert test="$uuidrefIsValid">Het element 'Objectencatalogus identificator' ontbreekt of is leeg.</sch:assert>
			<sch:report test="$uuidrefIsValid">Het element 'Objectencatalogus identificator' is aanwezig : <sch:value-of select="$uuidrefValue"/>
			</sch:report>
		</sch:rule>
	</sch:pattern>
  <!-- Check time periods - do they have valid start / end dates? -->
  <sch:pattern>
    <sch:title>$loc/strings/M900</sch:title>
    <sch:rule context="/gmd:MD_Metadata//gmd:temporalElement/*/gmd:extent/gml320:TimePeriod|/gmd:MD_Metadata//gmd:temporalElement/*/gmd:extent/gml:TimePeriod">
      <sch:let name="begin-position" value=".//gml320:beginPosition/text()|.//gml:beginPosition/text()"/>
      <sch:let name="end-position" value=".//gml320:endPosition/text()|.//gml:endPosition/text()"/>
      <!-- check whether end is before begin -->
      <sch:let name="check-order" value="$begin-position &lt; $end-position"/>
      <!-- only interested when we filled in both fields: we want to check the order -->
      <sch:let name="check-presence" value="not(boolean($begin-position) and boolean($end-position))"/>
      <sch:assert test="$check-order or $check-presence"><sch:value-of select="$loc/strings/alert.M900.1"/>&#160;<sch:value-of select="$begin-position"/>&#160;<sch:value-of select="$loc/strings/alert.M900.2"/>&#160;<sch:value-of select="$end-position"/>.</sch:assert>
      <sch:report test="$check-order or $check-presence"><sch:value-of select="$loc/strings/alert.M900.1"/>&#160;<sch:value-of select="$begin-position"/>&#160;<sch:value-of select="$loc/strings/alert.M900.2"/>&#160;<sch:value-of select="$end-position"/>.</sch:report>
    </sch:rule>
  </sch:pattern>
</sch:schema>
