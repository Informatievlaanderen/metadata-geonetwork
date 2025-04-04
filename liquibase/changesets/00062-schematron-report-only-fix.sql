--liquibase formatted sql
--changeset joachim:00062-schematron-report-only-fix

-- previous liquibase updates left -rec files as REQUIRED, this is now fixed to their correct REPORT_ONLY value
with reportonly as (select scg.name, scg.schematronid
                    from schematron s
                           inner join schematroncriteria sc on s.id = sc.id
                           inner join schematroncriteriagroup scg on scg.schematronid = sc.id
                    where filename like '%schematron-rules%-rec.xsl%'
                      and scg.name = 'Liquibase')
update schematroncriteriagroup
set requirement = 'REPORT_ONLY'
from reportonly
where schematroncriteriagroup.name = reportonly.name
  and schematroncriteriagroup.schematronid = reportonly.schematronid;
