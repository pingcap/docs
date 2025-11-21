---
title: TIFLASH_INDEXES
summary: Learn about the `TIFLASH_INDEXES` table in `INFORMATION_SCHEMA`.
---

# TIFLASH_INDEXES

> **Warning:**
>
> This table is currently an experimental feature and is not recommended for use in production environments. The fields of this table are not yet stable and may change in future versions of TiDB. If you find a bug, please submit an [issue](https://github.com/pingcap/tidb/issues) on GitHub for feedback.

The `TIFLASH_INDEXES` table provides statistical information about index building on TiFlash replicas.

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

The meaning of each column in the `TIFLASH_INDEXES` table is as follows:

- `TIDB_DATABASE`: The name of the database to which the table belongs.
- `TIDB_TABLE`: The name of the table.
- `TABLE_ID`: The internal ID of the table, which is unique within a TiDB cluster.
- `COLUMN_NAME`: The name of the column on which the index is located.
- `INDEX_NAME`: The name of the index.
- `COLUMN_ID`: The ID of the column on which the index is located.
- `INDEX_ID`: The ID of the index.
- `INDEX_KIND`: The type of index.
- `ROWS_STABLE_INDEXED`: The number of rows in the Stable layer of the TiFlash replica that have completed index construction.
- `ROWS_STABLE_NOT_INDEXED`: The number of rows in the Stable layer of the TiFlash replica that have not yet been indexed.
- `ROWS_DELTA_INDEXED`: The number of rows in the Delta layer of the TiFlash replica that have completed index construction.
- `ROWS_DELTA_NOT_INDEXED`: The number of rows in the Delta layer of the TiFlash replica that have not yet been indexed.
- `ERROR_MESSAGE`: Information about unrecoverable errors that occurred during index construction.
- `TIFLASH_INSTANCE`: The TiFlash instance address that executes the index building task.