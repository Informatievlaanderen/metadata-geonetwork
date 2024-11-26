--liquibase formatted sql
--changeset mathieu:00057-migrate-version-446

-- bump the version
UPDATE Settings
SET value='4.4.6'
WHERE name = 'system/platform/version';
UPDATE Settings
SET value='0'
WHERE name = 'system/platform/subVersion';

-- forgot these in v445/migrate-default.sql, included here instead
INSERT INTO Settings (name, value, datatype, position, internal)
SELECT distinct 'system/feedback/languages', '', 0, 646, 'n'
from settings
WHERE NOT EXISTS (SELECT name FROM Settings WHERE name = 'system/feedback/languages');
INSERT INTO Settings (name, value, datatype, position, internal)
SELECT distinct 'system/feedback/translationFollowsText', '', 0, 647, 'n'
from settings
WHERE NOT EXISTS (SELECT name FROM Settings WHERE name = 'system/feedback/translationFollowsText');

-- from v446/migrate-default.sql
INSERT INTO Settings (name, value, datatype, position, internal)
VALUES ('system/userSelfRegistration/domainsAllowed', '', 0, 1911, 'y');

-- doi servers were introduced in v445 (see DoiServerDatabaseMigration) but tables were not created
-- DDL below makes sure we are mirrorring Hibernate's assumptions
CREATE TABLE doiservers
(
  id                  int4         NOT NULL,
  description         varchar(255) NULL,
  landingpagetemplate varchar(255) NOT NULL,
  "name"              varchar(32)  NOT NULL,
  "password"          varchar(128) NULL,
  pattern             varchar(255) NOT NULL,
  prefix              varchar(15)  NOT NULL,
  publicurl           varchar(255) NOT NULL,
  url                 varchar(255) NOT NULL,
  username            varchar(128) NULL,
  CONSTRAINT doiservers_pkey PRIMARY KEY (id)
);
CREATE TABLE doiservers_group
(
  doiserver_id int4 NOT NULL,
  group_id     int4 NOT NULL,
  CONSTRAINT doiservers_group_pkey PRIMARY KEY (doiserver_id, group_id),
  CONSTRAINT fk_doiservers_group_doiservers FOREIGN KEY (doiserver_id) REFERENCES doiservers (id),
  CONSTRAINT fk_doiservers_group_groups FOREIGN KEY (group_id) REFERENCES groups (id)
);
-- no doi servers are configured at this point so migrating them makes no sense - just delete the related settings
DELETE FROM Settings WHERE name LIKE 'system/publication/doi%' and name != 'system/publication/doi/doienabled';
