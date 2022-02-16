psql -U postgres -d postgres
1024
DROP DATABASE IF EXISTS libdb;
DROP ROLE IF EXISTS Kevin;
CREATE ROLE kevin WITH LOGIN SUPERUSER INHERIT CREATEDB CREATEROLE REPLICATION
 ENCRYPTED PASSWORD 'SCRAM-SHA-256$4096:f4mkqNI2Lz9Jp4iqmynKgw==$B1JA513dicd80i21xmYJpUCGycprqt50kybIth+Ba1c=:KGbFj9e+nZUWcC5Xkjxug8XkP67GlRcIIftT3NBQny8=';

DROP DATABASE IF EXISTS libdb;
CREATE DATABASE libdb WITH OWNER = Kevin;

\c libdb kevin
2048

CREATE TABLE IF NOT EXISTS public.staff (ID CHARACTER varying NOT NULL PRIMARY KEY, name CHARACTER varying NOT NULL,
 Mobilenumber numeric(10), age integer NOT NULL, doj date, dept_id numeric(7, 0));
ALTER TABLE IF EXISTS public.staff OWNER TO kevin;

CREATE TABLE IF NOT EXISTS public.readers (ID CHARACTER varying NOT NULL PRIMARY KEY, name CHARACTER varying NOT NULL,
 Mobilenumber numeric(10), doj date, dept_id numeric(7, 0), image character VARYING);
ALTER TABLE IF EXISTS public.staff OWNER TO kevin;

DROP TABLE IF EXISTS books CASCADE;
CREATE TABLE public.books (isbn numeric(13) PRIMARY KEY NOT NULL, title CHARACTER varying NOT NULL,
 author CHARACTER varying, publisher CHARACTER varying,category CHARACTER varying,  number integer, dop date, image character VARYING);
ALTER TABLE IF EXISTS public.books OWNER TO kevin;

DROP TABLE IF EXISTS issuebook;
CREATE TABLE public.issuebook (rid CHARACTER varying, isbn numeric(13), doi date, dor date, fine integer);
ALTER TABLE IF EXISTS public.issuebook OWNER TO kevin;

DROP TABLE IF EXISTS authentication CASCADE;
CREATE TABLE IF NOT EXISTS public.Authentication (id CHARACTER varying NOT NULL REFERENCES staff(id) ON UPDATE CASCADE ON DELETE CASCADE,
 password CHARACTER varying COLLATE pg_catalog.DEFAULT ) TABLESPACE pg_default;
ALTER TABLE IF EXISTS public. Authentication OWNER TO kevin;

  create or replace function f2() returns trigger as
  $$
  begin
  INSERT INTO authentication(id) VALUES (new.ID);
  RETURN NEW;
  end;
  $$
  language plpgsql;
  create trigger t2 after insert on staff for each row execute procedure f2();

\q

exit
