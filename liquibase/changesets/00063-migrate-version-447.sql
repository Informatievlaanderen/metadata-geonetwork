--liquibase formatted sql
--changeset joachim:00063-migrate-version-447

-- bump the version
update settings
set value='4.4.7'
where name = 'system/platform/version';
update settings
set value='0'
where name = 'system/platform/subVersion';

-- sourced from v447/migrate-default.sql
INSERT INTO Settings (name, value, datatype, position, internal) VALUES ('system/banner/enable', 'false', 2, 1920, 'n') ON CONFLICT (name) DO NOTHING;
INSERT INTO Settings (name, value, datatype, position, internal) VALUES ('system/auditable/enable', 'false', 2, 12010, 'n') ON CONFLICT (name) DO NOTHING;

ALTER TABLE Sources ADD COLUMN datahubEnabled BOOLEAN DEFAULT FALSE;
ALTER TABLE Sources ADD COLUMN datahubConfiguration TEXT DEFAULT '';
