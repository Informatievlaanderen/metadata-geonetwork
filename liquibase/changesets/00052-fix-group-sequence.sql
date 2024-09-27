--liquibase formatted sql
--changeset joachim:00052-fix-group-sequence

-- missing sequence on the group.id column
alter table groups alter column id set default nextval('group_id_seq'::regclass);
-- update the sequence with the correct value
SELECT setval('group_id_seq', (select max(id) from groups), true);
