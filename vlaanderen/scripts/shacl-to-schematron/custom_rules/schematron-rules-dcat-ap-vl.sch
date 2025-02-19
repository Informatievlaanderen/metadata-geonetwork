<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<sch:schema xmlns:sch="http://purl.oclc.org/dsdl/schematron">
  <sch:pattern>
    <sch:title>vcard:hasEmail is a URI with the mailto protocol.</sch:title>
    <sch:rule context="//vcard:hasEmail[$profile]">
      <sch:let name="mailto" value="starts-with(@rdf:resource,'mailto:')"/>
      <sch:assert test="$mailto = true()">vcard:hasEmail property is not a URI with the mailto: protocol.</sch:assert>
      <sch:report test="$mailto = true()">vcard:hasEmail property is a URI with the mailto: protocol.</sch:report>
    </sch:rule>
  </sch:pattern>
  <sch:pattern>
    <sch:title>dct:license is CC0</sch:title>
    <sch:rule context="//dcat:Catalog/dct:license[$profile]">
      <sch:let name="cc0" value="./@rdf:resource = 'https://data.vlaanderen.be/id/licentie/creative-commons-zero-verklaring/v1.0' or ./dct:LicenseDocument/@rdf:about = 'https://data.vlaanderen.be/id/licentie/creative-commons-zero-verklaring/v1.0'"/>
      <sch:assert test="$cc0 = true()">The dcat:Catalog does not have a dct:license property with value 'https://data.vlaanderen.be/id/licentie/creative-commons-zero-verklaring/v1.0'.</sch:assert>
      <sch:report test="$cc0 = true()">The dcat:Catalog has a dct:license property with value 'https://data.vlaanderen.be/id/licentie/creative-commons-zero-verklaring/v1.0'.</sch:report>
    </sch:rule>
  </sch:pattern>
  <sch:pattern>
    <sch:title>At least one keyword is required.</sch:title>
    <sch:rule context="//dcat:Dataset[$profile]|//dcat:DataService[$profile]">
      <sch:let name="hasKeyword" value="count(dcat:keyword[normalize-space(.) != '']) > 0"/>
      <sch:assert test="$hasKeyword">The dcat:Resource doesn't have any keyword.</sch:assert>
      <sch:report test="$hasKeyword">The dcat:Resource have at least one keyword.</sch:report>
    </sch:rule>
  </sch:pattern>
  <sch:pattern>
    <sch:title>At least one of vcard:hasEmail or vcard:hasURL is a required for a contactpoint.</sch:title>
    <sch:rule context="//dcat:contactPoint[$profile]">
      <sch:let name="hasEmail" value="normalize-space(vcard:Organization/vcard:hasEmail/@rdf:resource) != ''"/>
      <sch:let name="hasUrl" value="normalize-space(vcard:Organization/vcard:hasURL/@rdf:resource) != ''"/>
      <sch:assert test="$hasEmail or $hasUrl">A vcard:Organization does not have a vcard:hasEmail or a vcard:hasURL property.</sch:assert>
      <sch:report test="$hasEmail or $hasUrl">A vcard:Organization has a vcard:hasEmail or a vcard:hasURL property.</sch:report>
    </sch:rule>
  </sch:pattern>
</sch:schema>
