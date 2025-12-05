---
title: TIFLASH_INDEXES
summary: 了解 `INFORMATION_SCHEMA` 中的 `TIFLASH_INDEXES` 表。
---

# TIFLASH_INDEXES

> **Warning:**
>
> 当前，该表为实验性功能。不建议在生产环境中使用。该表的字段尚不稳定，未来 TiDB 版本中可能会发生变化。如果你发现了 bug，可以在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues)。

`TIFLASH_INDEXES` 表提供了关于 TiFlash 副本上索引构建的统计信息。

```sql
USE INFORMATION_SCHEMA;
DESC TIFLASH_INDEXES;
```

输出如下：

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

`TIFLASH_INDEXES` 表中的字段说明如下：

- `TIDB_DATABASE`：表所属的数据库名称。
- `TIDB_TABLE`：表名。
- `TABLE_ID`：表的内部 ID，在 TiDB 集群内唯一。
- `COLUMN_NAME`：构建索引的列名。
- `INDEX_NAME`：索引名称。
- `COLUMN_ID`：构建索引的列的 ID。
- `INDEX_ID`：索引的 ID。
- `INDEX_KIND`：索引类型。
- `ROWS_STABLE_INDEXED`：TiFlash 副本中 Stable 层已完成索引构建的行数。
- `ROWS_STABLE_NOT_INDEXED`：TiFlash 副本中 Stable 层未完成索引构建的行数。
- `ROWS_DELTA_INDEXED`：TiFlash 副本中 Delta 层已完成索引构建的行数。
- `ROWS_DELTA_NOT_INDEXED`：TiFlash 副本中 Delta 层未完成索引构建的行数。
- `ERROR_MESSAGE`：索引构建过程中遇到的不可恢复错误的详细信息。
- `TIFLASH_INSTANCE`：执行索引构建任务的 TiFlash 实例地址。