--liquibase formatted sql
--changeset joachim:00066-migrate-version-448-449

-- bump the version
UPDATE Settings
SET value='4.4.9'
WHERE name = 'system/platform/version';
UPDATE Settings
SET value='SNAPSHOT'
WHERE name = 'system/platform/subVersion';

-- 4.4.8-0 updates
INSERT INTO Settings (name, value, datatype, position, internal)
VALUES ('metadata/delete/backupOptions', 'UseAPIParameter', 0, 12012, 'n');

-- 4.4.9-SNAPSHOT updates (nothing so far)
