--liquibase formatted sql
--changeset joachim:00065-temporal-config-history endDelimiter://

DO
$$
  DECLARE
    _source_tables           varchar[][] := array [
      array ['public', 'address'],
      array ['public', 'categories'],
      array ['public', 'categoriesdes'],
      array ['public', 'customelementset'],
      array ['public', 'doiservers'],
      array ['public', 'doiservers_group'],
      array ['public', 'email'],
      array ['public', 'files'],
      array ['public', 'group_category'],
      array ['public', 'groups'],
      array ['public', 'groupsdes'],
      array ['public', 'guf_keywords'],
      array ['public', 'guf_rating'],
      array ['public', 'guf_ratingcriteria'],
      array ['public', 'guf_ratingcriteriades'],
      array ['public', 'guf_userfeedback_keyword'],
      array ['public', 'guf_userfeedbacks'],
      array ['public', 'guf_userfeedbacks_guf_rating'],
      array ['public', 'harvesterdata'],
      array ['public', 'harvestersettings'],
      array ['public', 'harvesthistory'],
      array ['public', 'inspireatomfeed'],
      array ['public', 'inspireatomfeed_entrylist'],
      array ['public', 'isolanguages'],
      array ['public', 'isolanguagesdes'],
      array ['public', 'languages'],
      array ['public', 'links'],
      array ['public', 'linkstatus'],
      array ['public', 'mapservers'],
      array ['public', 'messageproducerentity'],
      array ['public', 'metadatacateg'],
      array ['public', 'metadatadraft'],
      array ['public', 'metadatafiledownloads'],
      array ['public', 'metadatafileuploads'],
      array ['public', 'metadataidentifiertemplate'],
      array ['public', 'metadatalink'],
      array ['public', 'metadatarating'],
      array ['public', 'metadatastatus'],
      array ['public', 'operationallowed'],
      array ['public', 'operations'],
      array ['public', 'operationsdes'],
      array ['public', 'relations'],
      array ['public', 'schematron'],
      array ['public', 'schematroncriteria'],
      array ['public', 'schematroncriteriagroup'],
      array ['public', 'schematrondes'],
      array ['public', 'selections'],
      array ['public', 'selectionsdes'],
      array ['public', 'settings'],
      array ['public', 'settings_cssstyle'],
      array ['public', 'settings_ui'],
      array ['public', 'sources'],
      array ['public', 'sourcesdes'],
      array ['public', 'spg_page'],
      array ['public', 'spg_sections'],
      array ['public', 'statusvalues'],
      array ['public', 'statusvalues'],
      array ['public', 'statusvaluesdes'],
      array ['public', 'translations'],
      array ['public', 'useraddress'],
      array ['public', 'usergroups'],
      array ['public', 'users'],
      array ['public', 'usersavedselections'],
      array ['public', 'usersearch'],
      array ['public', 'usersearch_group'],
      array ['public', 'usersearchdes'],
      array ['public', 'validation'],
      array ['public_augment', 'metadata'],
      array ['public_augment', 'metadata_data']
      ];
    _source_table            varchar[];
    _source_schema_name      varchar;
    _target_schema_name      varchar     := 'public_history';
    _source_table_name       varchar;
    _sys_period_column_name  varchar     := 'sys_period';
    -- settings for the history function
    _enforce_timestamps      bool        := true;
    _ignore_unchanged        bool        := false; -- disable when migrating existing data
    _include_current_version bool        := true;
    _migration_enabled       bool        := true; -- enable when migrating existing data
  BEGIN
    -- create schema to mirror `public` schema
    create schema if not exists public_history;

    -- loop over source tables, set them up
    foreach _source_table slice 1 in array _source_tables
      loop
        _source_schema_name := _source_table[1];
        _source_table_name := _source_table[2];
        -- add the necessary sys_period column
        execute 'alter table ' || quote_ident(_source_schema_name) || '.' || quote_ident(_source_table_name) ||
                ' add column if not exists ' || quote_ident(_sys_period_column_name) ||
                ' tstzrange not null default tstzrange(current_timestamp, null)';
        -- mark the table for temporal use
        execute 'create or replace trigger history before insert or update or delete ' ||
                ' on ' || quote_ident(_source_schema_name) || '.' || quote_ident(_source_table_name) ||
                ' for each row execute procedure temporal.versioning(' ||
                quote_literal(_sys_period_column_name) || ', ' ||
                quote_literal(_target_schema_name || '.' || _source_table_name) || ', ' ||
                _enforce_timestamps::varchar ||
                ', ' || _ignore_unchanged::varchar || ', ' || _include_current_version::varchar || ', ' || _migration_enabled::varchar ||  ')';
        -- create the history table
        execute
          'create table if not exists ' || quote_ident(_target_schema_name) || '.' || quote_ident(_source_table_name) ||
          ' (like ' || quote_ident(_source_schema_name) || '.' || quote_ident(_source_table_name) || ')';
      end loop;

    -- customize history tables
    alter table public_history.metadata drop column popularity;
  END
$$;
