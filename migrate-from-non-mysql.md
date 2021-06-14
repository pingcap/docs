---
title: Migrate from MySQL databases that are not MySQL-compatible
summary: Learn how to migrate data from database that don't support the MySQL protocol
---

# Migrate from Non-MySQL databases

For MySQL and MySQL compatible databases like Aurora and MariaDB we can use tools like dumpling and TiDB DM but this requires support for the MySQL protocol, which won't work for Oracle RDBMS, Microsoft SQL-Server and other relational databases.

Where MySQL and TiDB have data types that are compatible this is not the case with other databases. This means that there needs to be a mapping of data types. There might also be cases where there is no good match for the data types.

After the data is migrated the SQL statements from your application may also need more adjustment than for a MySQL to TiDB migration. And you need to switch to a different database driver.

This document is limited to migration from relational databases that support SQL.

## One-time data migration

With most databases you can run a backup or otherwise get a dump of the stucture of a table. If this is the case you now need to modify the statement to be compatible with TiDB. Once you have created the table you can dump the data as tab seperated or CSV and use `LOAD DATA INFILE` or TiDB Lightning to load the data into TiDB.

Once the data has been loaded into the target database you may want to verify that everything is ok. This can be done by looking at a sample of the data, row counts, etc. One specific thing to watch out for is character set issues. Using UTF-8 everywhere is a good way of avoiding this.

1. Get the `CREATE TABLE` statements from your source database
2. Modify these statements to be TiDB/MySQL compatible.
3. Dump the data from your source database in tab separated or CSV format.
4. Create the tables on TiDB based on the statements you created.
5. Load the data with `LOAD DATA INFILE` or TiDB Lightning into the tables.
6. Verify the migrated data.

### Example migration with PostgreSQL

This is the table we want to migrate:

```
test=# TABLE t1;
 id | name 
----+------
  1 | foo
  2 | bar
  3 | baz
(3 rows)
```

To get the `CREATE TABLE` statement we use `pg_dump` like this:

```
$ sudo -u postgres pg_dump --schema-only --table t1 --no-owner test
--
-- PostgreSQL database dump
--

-- Dumped from database version 11.12 (Debian 11.12-0+deb10u1)
-- Dumped by pg_dump version 11.12 (Debian 11.12-0+deb10u1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: t1; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.t1 (
    id integer NOT NULL,
    name character varying(255)
);


--
-- Name: t1_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.t1_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: t1_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.t1_id_seq OWNED BY public.t1.id;


--
-- Name: t1 id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t1 ALTER COLUMN id SET DEFAULT nextval('public.t1_id_seq'::regclass);


--
-- Name: t1 t1_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t1
    ADD CONSTRAINT t1_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

```

So we need to filter out the `CREATE TABLE` statement and modify it to:

- Use `AUTO_INCREMENT` or `AUTO_RANDOM` instead of the sequence
- Set the `id` column to be the `PRIMARY KEY`
- Replace the `character varying` with `VARCHAR`
- Change the name from `public.t1` to `t1`.

```
CREATE TABLE t1 (
    id integer NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255)
)
```

Now we dump the data to a tab separated file

```
test=# COPY t1 TO '/tmp/t1.dump' WITH (FORMAT CSV, DELIMITER E'\t');
COPY 3
test=# \! cat /tmp/t1.dump
1   foo
2   bar
3   baz
```

Now we create the schema, load the data and finally verify the content:

```
tidb> CREATE TABLE t1 (
   ->     id integer NOT NULL AUTO_INCREMENT PRIMARY KEY,
   ->     name VARCHAR(255)
   -> );
Query OK, 0 rows affected (0.2136 sec)
tidb> LOAD DATA LOCAL INFILE '/tmp/t1.dump' INTO TABLE t1;
Query OK, 3 rows affected (0.0509 sec)

Records: 3  Deleted: 0  Skipped: 0  Warnings: 0
tidb> TABLE t1;
+----+------+
| id | name |
+----+------+
|  1 | foo  |
|  2 | bar  |
|  3 | baz  |
+----+------+
3 rows in set (0.0037 sec)
```

## Continuous migration

Continues migration means that changes that happen over time on the source database are applied on the target database. This means that the source and target databases stay in sync, but there can be a delay with applying the changes on the target database.

There are multiple situations where this is useful:

- When migrating a large database you dump all data and then import the data on the target. This may take many hours or even days. If you now setup continues migration you can bring back this time to less than an hour. This allows you to compare the results and performance of your read-only queries between the source and target databases. And when you are ready to switch to the target database it takes less time to sync reducing the downtime your application may have during migration.

- When combining data from multiple database systems into one. By combining data from multiple systems or multiple instances of an application it allows you to run analytical queries against them. You may also be able to delete this data from the source system once it is archived into the target system if you setup the migration to filter out deletes or otherwise prevent these from reaching your target database.

There are multiple tools that can be used for continues migration:

- Apache Flink
- Apache Kafka with Kafka Connect

Both Flink and Kafka Connect rely on [Debezium](https://debezium.io) for most of the database streaming implementations.

> **Note:**
> When using continues migration DML (`INSERT`, `UPDATE`, `DELETE`, etc) is usually fine but schema changes are likely to be problematic. Depending on the tools and configuration the tool could stop to apply changes on the target database and require an operator to step in.

### Example migration with Microsoft SQL Server

For this demonstration we run Microsoft SQL Server 2019 in a docker container.
```
docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=SFhdafaDFSjh42" -p 1433:1433 --name sql1 -h sql1 -d mcr.microsoft.com/mssql/server:2019-latest
```

We setup Kafka with the Debezium connector by following the procedure on https://debezium.io/documentation/reference/tutorial.html

You need these components:
* zookeeper
* kafka
* debezium

