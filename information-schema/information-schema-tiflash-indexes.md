---
title: TIFLASH_INDEXES
summary: Learn about the `TIFLASH_INDEXES` table in `INFORMATION_SCHEMA`.
---

# TIFLASH_INDEXES

> **Warning:**
>
> Currently, this table is experimental. It is not recommended that you use it in production environments. The fields of this table are not yet stable and might change in future TiDB versions. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

The `TIFLASH_INDEXES` table provides statistics about index building on TiFlash replicas.

```sql
USE INFORMATION_SCHEMA;
DESC TIFLASH_INDEXES;
```

The output is as follows:

```sql
+-------------------------+---------------+------+------+---------+-------+
| Field                   | Type          | Null | Key  | Default | Extra |
+-------------------------+---------------+------+------+---------+-------+
| TIDB_DATABASE           | varchar(64)   | YES  |      | NULL    |       |
| TIDB_TABLE              | varchar(64)   | YES  |      | NULL    |       |
| TABLE_ID                | bigint        | YES  |      | NULL    |       |
| COLUMN_NAME             | varchar(64)   | YES  |      | NULL    |       |
| INDEX_NAME              | varchar(64)   | YES  |      | NULL    |       |
| COLUMN_ID               | bigint        | YES  |      | NULL    |       |
| INDEX_ID                | bigint        | YES  |      | NULL    |       |
| INDEX_KIND              | varchar(64)   | YES  |      | NULL    |       |
| ROWS_STABLE_INDEXED     | bigint        | YES  |      | NULL    |       |
| ROWS_STABLE_NOT_INDEXED | bigint        | YES  |      | NULL    |       |
| ROWS_DELTA_INDEXED      | bigint        | YES  |      | NULL    |       |
| ROWS_DELTA_NOT_INDEXED  | bigint        | YES  |      | NULL    |       |
| ERROR_MESSAGE           | varchar(1024) | YES  |      | NULL    |       |
| TIFLASH_INSTANCE        | varchar(64)   | YES  |      | NULL    |       |
+-------------------------+---------------+------+------+---------+-------+
```

Fields in the `TIFLASH_INDEXES` table are described as follows:

- `TIDB_DATABASE`: the name of the database to which the table belongs.
- `TIDB_TABLE`: the name of the table.
- `TABLE_ID`: the internal ID of the table, which is unique within a TiDB cluster.
- `COLUMN_NAME`: the name of the column on which the index is built.
- `INDEX_NAME`: the name of the index.
- `COLUMN_ID`: the ID of the column on which the index is built.
- `INDEX_ID`: the ID of the index.
- `INDEX_KIND`: the type of index.
- `ROWS_STABLE_INDEXED`: the number of rows in the TiFlash replica for which the Stable layer has completed index building.
- `ROWS_STABLE_NOT_INDEXED`: the number of rows in the TiFlash replica for which the Stable layer has not completed index building.
- `ROWS_DELTA_INDEXED`: the number of rows in the TiFlash replica for which the Delta layer has completed index building.
- `ROWS_DELTA_NOT_INDEXED`: the number of rows in the TiFlash replica for which the Delta layer has not completed index building.
- `ERROR_MESSAGE`: details about any unrecoverable errors encountered during index building.
- `TIFLASH_INSTANCE`: the address of the TiFlash instance that performs the index building task.