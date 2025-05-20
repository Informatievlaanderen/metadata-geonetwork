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
INSERT INTO Settings (name, value, datatype, position, internal)
VALUES ('system/banner/enable', 'false', 2, 1920, 'n')
ON CONFLICT (name) DO NOTHING;
INSERT INTO Settings (name, value, datatype, position, internal)
VALUES ('system/auditable/enable', 'false', 2, 12010, 'n')
ON CONFLICT (name) DO NOTHING;

ALTER TABLE Sources
    ADD COLUMN datahubEnabled BOOLEAN DEFAULT FALSE;
ALTER TABLE Sources
    ADD COLUMN datahubConfiguration TEXT DEFAULT '';

-- added column in Group.java
ALTER TABLE "groups"
    ADD minimumprofileforprivileges varchar(255) NULL;
ALTER TABLE "groups"
    ALTER COLUMN minimumprofileforprivileges SET STORAGE EXTENDED;

-- added new tables related to the audit PR
CREATE TABLE userauditable
(
    id                   int4         NOT NULL,
    createdby            varchar(255) NULL,
    createddate          timestamp    NULL,
    lastmodifiedby       varchar(255) NULL,
    lastmodifieddate     timestamp    NULL,
    address              varchar(255) NULL,
    city                 varchar(255) NULL,
    country              varchar(255) NULL,
    emailaddress         varchar(255) NULL,
    enabled              bool         NOT NULL,
    groupseditor         varchar(255) NULL,
    groupsregistereduser varchar(255) NULL,
    groupsreviewer       varchar(255) NULL,
    groupsuseradmin      varchar(255) NULL,
    kind                 varchar(255) NULL,
    "name"               varchar(255) NULL,
    organisation         varchar(255) NULL,
    profile              varchar(255) NULL,
    state                varchar(255) NULL,
    surname              varchar(255) NULL,
    username             varchar(255) NULL,
    zip                  varchar(255) NULL,
    CONSTRAINT userauditable_pkey PRIMARY KEY (id)
);

CREATE TABLE userauditable_aud
(
    id                       int4         NOT NULL,
    rev                      int4         NOT NULL,
    revtype                  int2         NULL,
    createdby                varchar(255) NULL,
    createddate              timestamp    NULL,
    lastmodifiedby           varchar(255) NULL,
    lastmodifieddate         timestamp    NULL,
    address                  varchar(255) NULL,
    address_mod              bool         NULL,
    city                     varchar(255) NULL,
    city_mod                 bool         NULL,
    country                  varchar(255) NULL,
    country_mod              bool         NULL,
    emailaddress             varchar(255) NULL,
    emailaddress_mod         bool         NULL,
    enabled                  bool         NULL,
    enabled_mod              bool         NULL,
    groupseditor             varchar(255) NULL,
    groupseditor_mod         bool         NULL,
    groupsregistereduser     varchar(255) NULL,
    groupsregistereduser_mod bool         NULL,
    groupsreviewer           varchar(255) NULL,
    groupsreviewer_mod       bool         NULL,
    groupsuseradmin          varchar(255) NULL,
    groupsuseradmin_mod      bool         NULL,
    kind                     varchar(255) NULL,
    kind_mod                 bool         NULL,
    "name"                   varchar(255) NULL,
    name_mod                 bool         NULL,
    organisation             varchar(255) NULL,
    organisation_mod         bool         NULL,
    profile                  varchar(255) NULL,
    profile_mod              bool         NULL,
    state                    varchar(255) NULL,
    state_mod                bool         NULL,
    surname                  varchar(255) NULL,
    surname_mod              bool         NULL,
    username                 varchar(255) NULL,
    username_mod             bool         NULL,
    zip                      varchar(255) NULL,
    zip_mod                  bool         NULL,
    CONSTRAINT userauditable_aud_pkey PRIMARY KEY (id, rev)
);

CREATE TABLE revinfo
(
    rev      int4 NOT NULL,
    revtstmp int8 NULL,
    CONSTRAINT revinfo_pkey PRIMARY KEY (rev)
);

CREATE TABLE spg_page_group
(
    "language" varchar(255) NOT NULL,
    linktext   varchar(255) NOT NULL,
    groupid    int4         NOT NULL,
    CONSTRAINT spg_page_group_pkey PRIMARY KEY (language, linktext, groupid)
);

ALTER TABLE userauditable_aud
    ADD CONSTRAINT fk_userauditable_aud_revinfo FOREIGN KEY (rev) REFERENCES revinfo (rev);
ALTER TABLE spg_page_group
    ADD CONSTRAINT fk_spg_page_group_spg_page FOREIGN KEY ("language", linktext) REFERENCES spg_page ("language", linktext);
ALTER TABLE spg_page_group
    ADD CONSTRAINT fk_spg_page_group_groups FOREIGN KEY (groupid) REFERENCES "groups" (id);
