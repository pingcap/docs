---
title: sys Schema
summary: Learn about the system tables in the `sys` schema.
---

# `sys` Schema

Starting from v8.0.0, TiDB provides the `sys` schema. You can use the views in `sys` schema to understand the data in the system tables, [`INFORMATION_SCHEMA`](/information-schema/information-schema.md), and [`PERFORMANCE SCHEMA`](/performance-schema/performance-schema.md) of TiDB.

## Manually create the `sys` schema and views

For clusters upgraded from versions earlier than v8.0.0, the `sys` schema and the views in it are not created automatically. You can manually create them using the following SQL statements:

```sql
CREATE DATABASE IF NOT EXISTS sys;
CREATE OR REPLACE VIEW sys.schema_unused_indexes AS
  SELECT
    table_schema as object_schema,
    table_name as object_name,
    index_name
  FROM information_schema.cluster_tidb_index_usage
  WHERE
    table_schema not in ('sys', 'mysql', 'INFORMATION_SCHEMA', 'PERFORMANCE_SCHEMA') and
    index_name != 'PRIMARY'
  GROUP BY table_schema, table_name, index_name
  HAVING
    sum(last_access_time) is null;
```

## `schema_unused_index`

`schema_unused_index` records indexes that have not been used since the last start of TiDB. It includes the following columns:

- `OBJECT_SCHEMA`: The name of the database to which the table containing the index belongs.
- `OBJECT_NAME`: The name of the table containing the index.
- `INDEX_NAME`: The name of the index.

```sql
USE SYS;
DESC SCHEMA_UNUSED_INDEXES;
```

The output is as follows:

```sql
+---------------+-------------+------+------+---------+-------+
| Field         | Type        | Null | Key  | Default | Extra |
+---------------+-------------+------+------+---------+-------+
| object_schema | varchar(64) | YES  |      | NULL    |       |
| object_name   | varchar(64) | YES  |      | NULL    |       |
| index_name    | varchar(64) | YES  |      | NULL    |       |
+---------------+-------------+------+------+---------+-------+
3 rows in set (0.00 sec)
```