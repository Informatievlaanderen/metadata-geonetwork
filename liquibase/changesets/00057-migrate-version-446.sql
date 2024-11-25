--liquibase formatted sql
--changeset mathieu:00057

INSERT INTO Settings (name, value, datatype, position, internal)
SELECT distinct 'system/feedback/languages', '', 0, 646, 'n'
from settings
WHERE NOT EXISTS (SELECT name FROM Settings WHERE name = 'system/feedback/languages');
INSERT INTO Settings (name, value, datatype, position, internal)
SELECT distinct 'system/feedback/translationFollowsText', '', 0, 647, 'n'
from settings
WHERE NOT EXISTS (SELECT name FROM Settings WHERE name = 'system/feedback/translationFollowsText');
INSERT INTO Settings (name, value, datatype, position, internal)
VALUES ('system/userSelfRegistration/domainsAllowed', '', 0, 1911, 'y');

UPDATE Settings
SET value='4.4.6'
WHERE name = 'system/platform/version';
UPDATE Settings
SET value='0'
WHERE name = 'system/platform/subVersion';

TODO: Create DOISERVER table;

CREATE TABLE public.doiservers
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

CREATE TABLE public.doiservers_group
(
  doiserver_id int4 NOT NULL,
  group_id     int4 NOT NULL,
  CONSTRAINT doiservers_group_pkey PRIMARY KEY (doiserver_id, group_id),
  CONSTRAINT fk68kkdbdvxs6np07y6p3gfff5b FOREIGN KEY (doiserver_id) REFERENCES public.doiservers (id),
  CONSTRAINT fkk9nywysss6bm8hgccdqoqqyti FOREIGN KEY (group_id) REFERENCES public."groups" (id)
);
