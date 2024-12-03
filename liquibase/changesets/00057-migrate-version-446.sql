--liquibase formatted sql
--changeset mathieu:00057-migrate-version-446

-- bump the version
update settings
set value='4.4.6'
where name = 'system/platform/version';
update settings
set value='0'
where name = 'system/platform/subVersion';

-- forgot these in v445/migrate-default.sql, included here instead
insert into settings (name, value, datatype, position, internal)
select distinct 'system/feedback/languages', '', 0, 646, 'n'
from settings
where not exists (select name from settings where name = 'system/feedback/languages');
insert into settings (name, value, datatype, position, internal)
select distinct 'system/feedback/translationFollowsText', '', 0, 647, 'n'
from settings
where not exists (select name from settings where name = 'system/feedback/translationFollowsText');

-- from v446/migrate-default.sql
insert into settings (name, value, datatype, position, internal)
values ('system/userSelfRegistration/domainsAllowed', '', 0, 1911, 'y');

-- doi servers were introduced in v445 (see DoiServerDatabaseMigration) but tables were not created
-- DDL below makes sure we are mirrorring Hibernate's assumptions
create table doiservers
(
  id                  int4         not null,
  description         varchar(255) null,
  landingpagetemplate varchar(255) not null,
  "name"              varchar(32)  not null,
  "password"          varchar(128) null,
  pattern             varchar(255) not null,
  prefix              varchar(15)  not null,
  publicurl           varchar(255) not null,
  url                 varchar(255) not null,
  username            varchar(128) null,
  constraint doiservers_pkey primary key (id)
);
create table doiservers_group
(
  doiserver_id int4 NOT NULL,
  group_id     int4 NOT NULL,
  constraint doiservers_group_pkey primary key (doiserver_id, group_id),
  constraint fk_doiservers_group_doiservers foreign key (doiserver_id) references doiservers (id),
  constraint fk_doiservers_group_groups foreign key (group_id) references groups (id)
);
create sequence doiserver_id_seq start with 1 increment by 1;
alter table doiservers alter column id set default nextval('doiserver_id_seq'::regclass);

-- no doi servers are configured at this point so migrating them makes no sense - just delete the related settings
delete from settings where name like 'system/publication/doi%' and name != 'system/publication/doi/doienabled';
