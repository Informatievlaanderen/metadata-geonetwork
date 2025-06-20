--liquibase formatted sql
--changeset  fxprunayre:00065-portal-filter-as-text

ALTER TABLE Sources
  ALTER COLUMN filter TYPE text USING filter::text;
