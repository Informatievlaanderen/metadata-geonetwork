--liquibase formatted sql
--changeset joachim:00051-migrate-version-445-snapshot

-- see v442/migrate-default.sql
DELETE FROM Settings WHERE name = 'system/index/indexingTimeRecordLink';

-- see v443/migrate-default.sql
INSERT INTO Settings (name, value, datatype, position, internal) VALUES ('system/documentation/url', 'https://docs.geonetwork-opensource.org/{{version}}/{{lang}}', 0, 570, 'n');
INSERT INTO Settings (name, value, datatype, position, internal) VALUES ('system/userFeedback/metadata/enable', 'false', 2, 1913, 'n');

-- see v444/migrate-default.sql
UPDATE Metadata SET data = replace(data, 'http://standards.iso.org/iso/19115/-3/srv/2.1', 'http://standards.iso.org/iso/19115/-3/srv/2.0') WHERE data LIKE '%http://standards.iso.org/iso/19115/-3/srv/2.1%' AND schemaId = 'iso19115-3.2018';
UPDATE settings SET name='metadata/history/enabled' WHERE name='system/metadata/history/enabled';
INSERT INTO Settings (name, value, datatype, position, internal) SELECT distinct 'metadata/history/accesslevel', 'Editor', 0, 12021, 'n' from settings WHERE NOT EXISTS (SELECT name FROM Settings WHERE name = 'metadata/history/accesslevel');

-- current version
UPDATE Settings SET value='4.4.5' WHERE name='system/platform/version';
UPDATE Settings SET value='SNAPSHOT' WHERE name='system/platform/subVersion';
