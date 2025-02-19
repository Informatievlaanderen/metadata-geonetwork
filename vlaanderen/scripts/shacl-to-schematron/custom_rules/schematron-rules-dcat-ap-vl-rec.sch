<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<sch:schema xmlns:sch="http://purl.oclc.org/dsdl/schematron">
  <sch:pattern>
    <sch:title>At least one theme from the data.gov.be vocabulary is required</sch:title>
    <sch:rule context="//dcat:Dataset[$profile]|//dcat:DataService[$profile]">
      <sch:let name="dataThemes" value="count(dcat:theme[starts-with(skos:Concept/@rdf:about, 'http://vocab.belgif.be/auth/datatheme')])"/>
      <sch:assert test="$dataThemes > 0">The dcat:Resource doesn't have a data.gov.be theme</sch:assert>
      <sch:report test="$dataThemes > 0">The dcat:Resource have a data.gov.be theme</sch:report>
    </sch:rule>
  </sch:pattern>
</sch:schema>
