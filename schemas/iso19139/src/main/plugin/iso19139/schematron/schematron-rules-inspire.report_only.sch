<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<sch:schema xmlns:sch="http://purl.oclc.org/dsdl/schematron" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" queryBinding="xslt2">
	<sch:title xmlns="http://www.w3.org/2001/XMLSchema">INSPIRE</sch:title>
	<sch:ns prefix="gml" uri="http://www.opengis.net/gml/3.2"/>
  <sch:ns prefix="gml320" uri="http://www.opengis.net/gml"/>
	<sch:ns prefix="gmd" uri="http://www.isotc211.org/2005/gmd"/>
	<sch:ns prefix="srv" uri="http://www.isotc211.org/2005/srv"/>
	<sch:ns prefix="gco" uri="http://www.isotc211.org/2005/gco"/>
	<sch:ns prefix="geonet" uri="http://www.fao.org/geonetwork"/>
  <sch:ns prefix="rdf" uri="http://www.w3.org/1999/02/22-rdf-syntax-ns#"/>
	<sch:ns prefix="skos" uri="http://www.w3.org/2004/02/skos/core#"/>
	<sch:ns prefix="xlink" uri="http://www.w3.org/1999/xlink"/>

	<sch:pattern>
		<sch:title>Er moet minstens één Nederlandstalig trefwoord aanwezig zijn uit de thesaurus ‘GEMET - INSPIRE themes, version 1.0’ met als datum 2008-06-01 indien de MD_Metadata.language gelijk is aan NL (ISO-element 55)</sch:title>
		<sch:rule context="//gmd:MD_DataIdentification[/gmd:MD_Metadata/gmd:language/*/text()='dut' or /gmd:MD_Metadata/gmd:language/gmd:LanguageCode/@codeListValue='dut']">
			<sch:let name="inspire-thesaurus" value="document(concat('file:///', replace($thesaurusDir, '\\', '/'), '/external/thesauri/theme/inspire-theme.rdf'))"/>
			<sch:let name="inspire-theme" value="$inspire-thesaurus//skos:Concept"/>
			<sch:assert test="count($inspire-theme) > 0">
				INSPIRE Thema thesaurus niet gevonden.
			</sch:assert>
      <sch:let name="thesaurus_name" value="gmd:descriptiveKeywords/*/gmd:thesaurusName/*/gmd:title/*/text()"/>
      <sch:let name="thesaurus_date" value="gmd:descriptiveKeywords/*/gmd:thesaurusName/*/gmd:date/*/gmd:date/*/text()"/>
      <sch:let name="thesaurus_dateType" value="gmd:descriptiveKeywords/*/gmd:thesaurusName/*/gmd:date/*/gmd:dateType/*/@codeListValue/normalize-space(.)"/>
			<sch:let name="keyword" value="gmd:descriptiveKeywords/*/gmd:keyword/*[name()='gco:CharacterString' or name()='gmx:Anchor']
					[../../gmd:thesaurusName/*/gmd:title/*/text()='GEMET - INSPIRE themes, version 1.0' and
					../../gmd:thesaurusName/*/gmd:date/*/gmd:date/gco:Date/text()='2008-06-01' and
					../../gmd:thesaurusName/*/gmd:date/*/gmd:dateType/gmd:CI_DateTypeCode/@codeListValue='publication']"/>
			<sch:let name="inspire-theme-selected" value="count($inspire-thesaurus//skos:Concept[skos:prefLabel[@xml:lang='nl'] = $keyword])"/>
			<sch:assert test="$inspire-theme-selected >0">
				Er werd geen Nederlandstalig sleutelwoord gevonden afkomstig uit de GEMET - INSPIRE themes, version 1.0 thesaurus gedateerd op 2008-06-01.
			</sch:assert>
			<sch:report test="$inspire-theme-selected > 0">
				Er werd een Nederlandstalig sleutelwoord: <sch:value-of select="$keyword"/> gevonden dat afkomstig is uit de GEMET - INSPIRE themes, version 1.0 thesaurus gedateerd op 2008-06-01.
			</sch:report>
		</sch:rule>
	</sch:pattern>

  <sch:pattern>
    <sch:let name="thesaurusName" value="'INSPIRE - Spatial scope'" />
    <sch:let name="thesaurusDate" value="'2019-05-22'" />
    <sch:let name="thesaurusNameWithDate" value="concat('''',$thesaurusName,''' thesaurus gedateerd op ',$thesaurusDate)" />
    <sch:title>Er moet minstens één Nederlandstalig trefwoord aanwezig zijn uit de thesaurus ‘INSPIRE - Spatial scope’ met als datum 2019-05-22 indien de MD_Metadata.language gelijk is aan NL (ISO-element 55)</sch:title>
    <!--sch:title><sch:value-of select="concat('Er moet minstens één Nederlandstalig trefwoord aanwezig zijn uit de ',' indien de MD_Metadata.language gelijk is aan NL (ISO-element 55)')"/></sch:title-->
    <sch:rule context="//gmd:MD_DataIdentification[/gmd:MD_Metadata/gmd:language/*/text()='dut' or /gmd:MD_Metadata/gmd:language/gmd:LanguageCode/@codeListValue='dut']">
      <sch:let name="spatial-scope-thesaurus" value="document(concat('file:///', replace($thesaurusDir, '\\', '/'), '/external/thesauri/theme/SpatialScope.rdf'))"/>
      <sch:let name="spatial-scope" value="$spatial-scope-thesaurus//skos:Concept"/>
      <sch:assert test="count($spatial-scope) > 0">
        <sch:value-of select="$thesaurusName"/> niet gevonden.
      </sch:assert>
      <sch:let name="thesaurus_name" value="gmd:descriptiveKeywords/*/gmd:thesaurusName/*/gmd:title/*/text()"/>
      <sch:let name="thesaurus_date" value="gmd:descriptiveKeywords/*/gmd:thesaurusName/*/gmd:date/*/gmd:date/*/text()"/>
      <sch:let name="thesaurus_dateType" value="gmd:descriptiveKeywords/*/gmd:thesaurusName/*/gmd:date/*/gmd:dateType/*/@codeListValue/normalize-space(.)"/>
      <sch:let name="keyword" value="gmd:descriptiveKeywords/*/gmd:keyword/*[name()='gco:CharacterString' or name()='gmx:Anchor']
					[../../gmd:thesaurusName/*/gmd:title/*/text()='INSPIRE - Spatial scope' and
					../../gmd:thesaurusName/*/gmd:date/*/gmd:date/gco:Date/text()=$thesaurusDate and
					../../gmd:thesaurusName/*/gmd:date/*/gmd:dateType/gmd:CI_DateTypeCode/@codeListValue='publication']"/>
      <sch:let name="spatial-scope-found" value="count($spatial-scope-thesaurus//skos:Concept[skos:prefLabel[@xml:lang='nl'] = $keyword])"/>
      <sch:assert test="$spatial-scope-found >0">
        Er werd geen Nederlandstalig sleutelwoord gevonden afkomstig uit de <sch:value-of select="$thesaurusNameWithDate"/>.
      </sch:assert>
      <sch:report test="$spatial-scope-found > 0">
        Er werd een Nederlandstalig sleutelwoord: <sch:value-of select="$keyword"/> gevonden dat afkomstig is uit de <sch:value-of select="$thesaurusNameWithDate"/>.
      </sch:report>
    </sch:rule>
  </sch:pattern>
</sch:schema>
