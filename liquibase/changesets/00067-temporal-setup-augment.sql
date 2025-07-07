--liquibase formatted sql
--changeset joachim:00067-temporal-setup-augment endDelimiter://

DO
$$
  BEGIN
    -- create schema to hold augmented public tables
    create schema if not exists public_augment;

    -- create augmented tables
    -- public_augment.metadata_data
    create sequence if not exists public_augment.metadata_data_id;
    create table public_augment.metadata_data
    (
      data_id serial not null primary key,
      data    text   not null
    );
    -- index the data column - can't use btree here
    create index metadata_data_data ON public_augment.metadata_data USING HASH (data);
    -- public_augment.metadata
    create table public_augment.metadata
    (
      like public.metadata
    );
    alter table public_augment.metadata
      drop column data;
    alter table public_augment.metadata
      add column data_id integer not null references public_augment.metadata_data (data_id);
  END
$$;

-- function that serves to map public.metadata to public_augment
create or replace function public_augment.augment_metadata() returns trigger
  language plpgsql as
$$
declare
  _data_id         int;
  _desired_columns text[];
  _update_setters  varchar;
begin
  -- columns that should be copied over
  SELECT array_agg(quote_ident(attname))
  INTO _desired_columns
  FROM pg_attribute
  WHERE attrelid = TG_RELID
    AND attnum > 0
    AND NOT attisdropped
    and attname not in ('data');
  -- new record to consider (insert / update): NEW
  -- check if metadata.data has to be inserted in cache metadata_data
  if TG_OP = 'INSERT' or TG_OP = 'UPDATE' then
    -- first make sure we have stored 'data' in the metadata_data table so we can reference it
    select data_id into _data_id from public_augment.metadata_data where data = NEW.data;
    if _data_id is null then
      insert into public_augment.metadata_data (data) values (NEW.data) returning data_id into _data_id;
    end if;
  end if;
  -- deal with inserts: mirror the insert to the augmented table
  -- this case also deals with updates on metadata rows that were never copied to public_augment
  if TG_OP = 'INSERT' or
     (TG_OP = 'UPDATE' and not exists (select id from public_augment.metadata where id = NEW.id)) then
    EXECUTE ('INSERT INTO public_augment.metadata ' ||
             '(' || array_to_string(_desired_columns, ',') ||
             ',' || quote_ident('data_id') ||
             ') VALUES ($1.' ||
             array_to_string(_desired_columns, ',$1.') ||
             ', $2)')
      USING NEW, _data_id;
  end if;
  -- deal with updates: mirror the update to the augmented table
  if TG_OP = 'UPDATE' then
    with unnested as (select unnest(_desired_columns) p)
    select array_to_string(array_agg(p || '=$1.' || p), ',')
    into _update_setters
    from unnested
    where p <> 'id';
    EXECUTE (
      'UPDATE public_augment.metadata' ||
      ' SET ' || _update_setters || ',data_id=$2' ||
      ' WHERE id = $1.id '
      ) USING NEW, _data_id;
  end if;
  -- check if we need to purge old data
  if TG_OP = 'UPDATE' or TG_OP = 'DELETE' then
    -- remove orphaned data records
    with to_delete as (select md.data_id
                       from public_augment.metadata_data md
                              left join public_augment.metadata m using (data_id)
                       where m.id is null)
    delete
    from public_augment.metadata_data md using to_delete td
    where md.data_id = td.data_id;
  end if;
  return null;
end;
$$;

-- each time something happens to the metadata table, mirror that to public_augment
create or replace trigger augment
  after insert or update or delete
  on public.metadata
  for each row
execute procedure public_augment.augment_metadata();

-- trigger a fake update so all records are processed by the augment function at least once
update public.metadata
set popularity = popularity
where id > -1;
