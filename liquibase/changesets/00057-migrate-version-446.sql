--liquibase formatted sql
--changeset mathieu:00057

INSERT INTO Settings (name, value, datatype, position, internal) SELECT distinct 'system/feedback/languages', '', 0, 646, 'n' from settings WHERE NOT EXISTS (SELECT name FROM Settings WHERE name = 'system/feedback/languages');
INSERT INTO Settings (name, value, datatype, position, internal) SELECT distinct 'system/feedback/translationFollowsText', '', 0, 647, 'n' from settings WHERE NOT EXISTS (SELECT name FROM Settings WHERE name = 'system/feedback/translationFollowsText');
INSERT INTO Settings (name, value, datatype, position, internal) VALUES ('system/userSelfRegistration/domainsAllowed', '', 0, 1911, 'y');

UPDATE Settings SET value='4.4.6' WHERE name='system/platform/version';
UPDATE Settings SET value='0' WHERE name='system/platform/subVersion';

TODO: Create DOISERVER table;
