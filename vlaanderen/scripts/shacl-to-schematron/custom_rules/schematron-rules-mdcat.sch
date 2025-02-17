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
    <sch:title>At least one of vcard:hasEmail or vcard:hasURL is a required for a contactpoint.</sch:title>
    <sch:rule context="//dcat:contactPoint[$profile]">
      <sch:let name="hasEmail" value="normalize-space(vcard:Organization/vcard:hasEmail/@rdf:resource) != ''"/>
      <sch:let name="hasUrl" value="normalize-space(vcard:Organization/vcard:hasURL/@rdf:resource) != ''"/>
      <sch:assert test="$hasEmail or $hasUrl">A vcard:Organization does not have a vcard:hasEmail or a vcard:hasURL property.</sch:assert>
      <sch:report test="$hasEmail or $hasUrl">A vcard:Organization has a vcard:hasEmail or a vcard:hasURL property.</sch:report>
    </sch:rule>
  </sch:pattern>
</sch:schema>
