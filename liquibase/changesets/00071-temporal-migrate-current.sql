--liquibase formatted sql
--changeset joachim:00071-temporal-migrate-current endDelimiter://

-- single startup migration: include the current version in history for all rows in all tables
DO
$$
  DECLARE
    _source_tables      varchar[][] := array [
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
    _source_table       varchar[];
    _source_schema_name varchar;
    _source_table_name  varchar;
  BEGIN
    foreach _source_table slice 1 in array _source_tables
      loop
        _source_schema_name := _source_table[1];
        _source_table_name := _source_table[2];
        raise notice 'doing table %', _source_table_name;
        execute format('update %s.%s set sys_period = sys_period', _source_schema_name, _source_table_name);
        execute format('delete from public_history.%s where upper(sys_period) is not null', _source_table_name);
      end loop;
  END
$$;
