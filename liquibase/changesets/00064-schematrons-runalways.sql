--liquibase formatted sql run
--changeset joachim:00064-schematron-runalways runAlways:true runOnChange:true

-- this changeset always runs, resetting schematron configuration to sane defaults that mirror the file setup

-- steps:
-- 1. remove all schematrons
-- 2. this script will manually set up the expected overrides
-- 3. the rest is automatically provisioned by geonetwork at startup with default values

-- define input to be used below
create temporary table _schematron on commit drop as (select *
                                       from (values ('dcat-ap-vl',
                                                     'schematron-rules-dcat-ap-vl-cardinalities.xsl',
                                                     'dcat-ap',
                                                     'REQUIRED'),
                                                    ('dcat-ap-vl',
                                                     'schematron-rules-dcat-ap-vl-rec.xsl',
                                                     'dcat-ap',
                                                     'REPORT_ONLY'),
                                                    ('dcat-ap-vl',
                                                     'schematron-rules-dcat-ap-vl.xsl',
                                                     'dcat-ap',
                                                     'REQUIRED'),
                                                    ('dcat-ap-hvd',
                                                     'schematron-rules-dcat-ap-hvd-cardinalities.xsl',
                                                     'dcat-ap',
                                                     'REQUIRED'),
                                                    ('dcat-ap-hvd',
                                                     'schematron-rules-dcat-ap-hvd-rec.xsl',
                                                     'dcat-ap',
                                                     'REPORT_ONLY'),
                                                    ('dcat-ap-hvd',
                                                     'schematron-rules-dcat-ap-hvd.xsl',
                                                     'dcat-ap',
                                                     'REQUIRED'),
                                                    ('iso-hvd',
                                                     'schematron-rules-dcat-ap-hvd.xsl',
                                                     'iso19139',
                                                     'REQUIRED'),
                                                    ('mdcat',
                                                     'schematron-rules-mdcat.xsl',
                                                     'dcat-ap',
                                                     'REQUIRED'),
                                                    ('mdcat',
                                                     'schematron-rules-mdcat-rec.xsl',
                                                     'dcat-ap',
                                                     'REPORT_ONLY'))
                                              as t (xpathtarget, filename, schemaname, requirement));

create temporary table _xpaths on commit drop as (select *
                                   from (values ('dcat-ap-vl',
                                                 '//dcat:CatalogRecord/dct:conformsTo/dct:Standard[@rdf:about=''https://data.vlaanderen.be/doc/applicatieprofiel/DCAT-AP-VL/erkendestandaard/2019-10-03'']'),
                                                ('dcat-ap-hvd',
                                                 '//dcatap:applicableLegislation[@rdf:resource=''http://data.europa.eu/eli/reg_impl/2023/138/oj'']'),
                                                ('iso-hvd',
                                                 '//gmd:descriptiveKeywords/*/gmd:keyword/gmx:Anchor[@xlink:href=''http://data.europa.eu/eli/reg_impl/2023/138/oj'']'),
                                                ('mdcat',
                                                 '//dcat:CatalogRecord/dct:conformsTo/dct:Standard[@rdf:about=''https://data.vlaanderen.be/doc/applicatieprofiel/DCAT-AP-VL/erkendestandaard/2019-10-03'' or @rdf:about=''https://data.vlaanderen.be/doc/applicatieprofiel/metadata-dcat/erkendestandaard/2021-04-22'']'))
                                          as t (xpathtarget, xpath));

-- remove schematrons
delete
from schematron s
where true;

-- restart sequences
alter sequence schematron_id_seq restart with 1;
alter sequence schematron_criteria_id_seq restart with 1;

-- create the schematron entries
insert into schematron (displaypriority, filename, schemaname)
select 0, filename, schemaname
from _schematron;

-- set up 'Liquibase' groups for each of the schematron files, replacing the default *generated* groups
insert into schematroncriteriagroup (name, schematronid, requirement)
  (select 'Liquibase', schematron.id, requirement
   from _schematron
          inner join schematron using (filename, schemaname));

-- we're only dealing with xpath based criteria at this point
insert into schematroncriteria
  ("type", uitype, uivalue, value, group_name, group_schematronid)
select 'XPATH', 'XPATH', xpath, xpath, g.name, g.schematronid
from _schematron
       inner join _xpaths using (xpathtarget)
       inner join schematron s using (filename, schemaname)
       inner join schematroncriteriagroup g on g.schematronid = s.id;

-- update the displaypriorities for all files to make it consistent again
with calculated
       as (select row_number()
                  over (partition by schemaname order by replace(replace(filename, '-cardinalities.xsl', '.xsl'),
                                                                 '-rec.xsl', '.xsl'), filename) newdisplaypriority,
                  id
           from schematron)
update schematron
set displaypriority = newdisplaypriority - 1
from calculated
where calculated.id = schematron.id;
