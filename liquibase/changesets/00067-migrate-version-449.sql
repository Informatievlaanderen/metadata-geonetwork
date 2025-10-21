--liquibase formatted sql
--changeset joachim:00067-migrate-version-449

-- bump the version
update settings
set value='4.4.9'
where name = 'system/platform/version';
update settings
set value='0'
where name = 'system/platform/subVersion';

-- sourced from v449/migrate-default.sql

INSERT INTO Settings (name, value, datatype, position, internal) VALUES ('system/publication/doi/doimailnotification', 'false', 2, 100192, 'n');

-- Migration to 4.4.5 only removed the old DOI settings, when the DOI server was defined.
-- Related to https://github.com/geonetwork/core-geonetwork/pull/8098
DELETE FROM Settings WHERE name LIKE 'system/publication/doi%' and name != 'system/publication/doi/doienabled';
