--liquibase formatted sql
--changeset joachim:00073-temporal-config-remove-noise endDelimiter://

-- settings were causing noise: system/feedback/mailServer/password is updated every time the value is accessed
drop trigger if exists history on public.settings;
drop table if exists public_history.settings;
