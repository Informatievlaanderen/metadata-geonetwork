--liquibase formatted sql
--changeset joachim:000058-dcat-ap-plugin

-- fix references to dcat2
update schematron set schemaname = 'dcat-ap' where schemaname = 'dcat2';
