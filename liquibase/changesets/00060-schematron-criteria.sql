--liquibase formatted sql
--changeset joachim:000060-schematron-criteria

-- create temporary table to loop over - plpgsql is a paid feature in liquibase so couldn't use that here :(
create schema "00060_temp";
select *
into "00060_temp".file
from ((values ('schematron-rules-dcat-ap-vl-cardinalities.xsl', 'dcat-ap-vl'),
              ('schematron-rules-dcat-ap-vl-rec.xsl', 'dcat-ap-vl'),
              ('schematron-rules-dcat-ap-vl.xsl', 'dcat-ap-vl'),
              ('schematron-rules-dcat-ap-hvd-cardinalities.xsl', 'dcat-ap-hvd'),
              ('schematron-rules-dcat-ap-hvd-rec.xsl', 'dcat-ap-hvd'),
              ('schematron-rules-dcat-ap-hvd.xsl', 'dcat-ap-hvd')))
       as t (filename, profile);
select *
into "00060_temp".xpath
from ((values ('dcat-ap-vl',
               '//dcat:CatalogRecord/dct:conformsTo/dct:Standard[@rdf:about=''https://data.vlaanderen.be/doc/applicatieprofiel/DCAT-AP-VL/erkendestandaard/2019-10-03'']'),
              ('dcat-ap-hvd',
               '//dcatap:applicableLegislation[@rdf:resource=''http://data.europa.eu/eli/reg_impl/2023/138/oj'']')))
       as t (profile, xpath);
-- clean up before inserting new data
delete
from schematron s
where exists (select * from "00060_temp".file f where f.filename = s.filename);
-- create schematron entries
insert into schematron (filename, displaypriority, schemaname) (select filename, 0, 'dcat-ap' from "00060_temp".file);
-- create groups
insert into schematroncriteriagroup (name, schematronid, requirement) (select 'Liquibase', s.id, 'REQUIRED'
                                                                       from schematron s
                                                                              inner join "00060_temp".file f using (filename));
-- create the criteria
insert into schematroncriteria (type, uitype, uivalue, value, group_name, group_schematronid)
  (select 'XPATH', 'XPATH', x.xpath, x.xpath, 'Liquibase', s.id
   from "00060_temp".file f
          inner join schematron s using (filename)
   inner join "00060_temp".xpath x using (profile));
-- clean up
drop schema "00060_temp" cascade;
