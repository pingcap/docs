---
title: sys Schema
summary: Learn about the system tables in the `sys` schema.
---

# `sys` Schema

> **Note:**
>
> The cluster upgrades from lower version than v8.0.0 will not have `sys` Schema and the views in it. `sys` and the view inside can be created by the following SQLs:
>
> {{< copyable "sql" >}}
>
> ```sql
> CREATE DATABASE IF NOT EXISTS sys;
> CREATE OR REPLACE VIEW sys.schema_unused_indexes AS
>   SELECT
>     table_schema as object_schema,
>     table_name as object_name,
>     index_name
>   FROM information_schema.cluster_tidb_index_usage
>   WHERE
>     table_schema not in ('sys', 'mysql', 'INFORMATION_SCHEMA', 'PERFORMANCE_SCHEMA') and
>     index_name != 'PRIMARY'
>   GROUP BY table_schema, table_name, index_name
>   HAVING
>     sum(last_access_time) is null;
> ```

Tables and views in the `sys` schema are used to help users understand the data in TiDB's system tables, `INFORMATION_SCHEMA` database, and `PERFORMANCE_SCHEMA` database.

- `schema_unused_index` is used to record indexes that have not been used since the last restart of TiDB.
    - `OBJECT_SCHEMA`: The name of the database to which the table containing the index belongs.
    - `OBJECT_NAME`: The name of the table containing the index.
    - `INDEX_NAME`: The name of the index.