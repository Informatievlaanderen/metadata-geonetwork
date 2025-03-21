--liquibase formatted sql
--changeset joachim:00061-schematron-criteria-metadata-dcat

-- make sure the xpaths can be longer than currently supported
ALTER TABLE public.schematroncriteria ALTER COLUMN uivalue TYPE varchar USING uivalue::varchar;
ALTER TABLE public.schematroncriteria ALTER COLUMN value TYPE varchar USING value::varchar;

-- clean up before inserting new data
delete
from schematron
where filename in ('schematron-rules-mdcat.xsl', 'schematron-rules-mdcat-rec.xsl');
-- create schematron entries
insert into schematron (filename, displaypriority, schemaname) values ('schematron-rules-mdcat.xsl', 0, 'dcat-ap');
insert into schematron (filename, displaypriority, schemaname) values ('schematron-rules-mdcat-rec.xsl', 0, 'dcat-ap');
-- create groups
insert into schematroncriteriagroup (name, schematronid, requirement) (select 'Liquibase', s.id, 'REQUIRED'
                                                                       from schematron s where filename in ('schematron-rules-mdcat.xsl', 'schematron-rules-mdcat-rec.xsl'));
-- create the criteria
with raw as (select '//dcat:CatalogRecord/dct:conformsTo/dct:Standard[@rdf:about=''https://data.vlaanderen.be/doc/applicatieprofiel/DCAT-AP-VL/erkendestandaard/2019-10-03'' or @rdf:about=''https://data.vlaanderen.be/doc/applicatieprofiel/metadata-dcat/erkendestandaard/2021-04-22'']' xpath, s.id sid
             from schematron s where filename in ('schematron-rules-mdcat.xsl', 'schematron-rules-mdcat-rec.xsl'))
insert into schematroncriteria (type, uitype, uivalue, value, group_name, group_schematronid)
  (select 'XPATH', 'XPATH', xpath, xpath, 'Liquibase', sid
    from raw);

-- update the displaypriorities for all files to make it consistent again
with calculated as (
  select row_number() over (partition by schemaname order by replace(replace(filename, '-cardinalities.xsl', '.xsl'), '-rec.xsl', '.xsl'), filename) newdisplaypriority, id from schematron
)
update schematron set displaypriority = newdisplaypriority-1 from calculated where calculated.id = schematron.id;
