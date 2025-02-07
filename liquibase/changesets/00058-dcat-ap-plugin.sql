--liquibase formatted sql
--changeset joachim:00058-dcat-ap-plugin

-- fix references to dcat2
update schematron set schemaname = 'dcat-ap' where schemaname = 'dcat2';
update metadata set schemaid = 'dcat-ap' where schemaid = 'dcat2';
update metadatadraft set schemaid = 'dcat-ap' where schemaid = 'dcat2';
update harvestersettings set value = 'schema:dcat-ap:convert/fromSPARQL-DCAT-with-open-keywords' where value = 'schema:dcat2:convert/fromSPARQL-DCAT-with-open-keywords';
