---
title: TIFLASH_SEGMENTS
summary: 了解 `TIFLASH_SEGMENTS` information_schema 表格。
---

# TIFLASH_SEGMENTS

> **Warning:**
>
> 不要在生产环境中使用此表，因为表中的字段不稳定，可能在 TiDB 的新版本中发生变化，且不会提前通知。

`TIFLASH_SEGMENTS` 表格提供关于 TiFlash 中数据表的统计信息。

```sql
USE information_schema;
DESC tiflash_segments;
```

```sql
+-------------------------------+-------------+------+------+---------+-------+
| Field                         | Type        | Null | Key  | Default | Extra |
+-------------------------------+-------------+------+------+---------+-------+
| DATABASE                      | varchar(64) | YES  |      | NULL    |       |
| TABLE                         | varchar(64) | YES  |      | NULL    |       |
| TIDB_DATABASE                 | varchar(64) | YES  |      | NULL    |       |
| TIDB_TABLE                    | varchar(64) | YES  |      | NULL    |       |
| TABLE_ID                      | bigint(64)  | YES  |      | NULL    |       |
| IS_TOMBSTONE                  | bigint(64)  | YES  |      | NULL    |       |
| SEGMENT_ID                    | bigint(64)  | YES  |      | NULL    |       |
| RANGE                         | varchar(64) | YES  |      | NULL    |       |
| EPOCH                         | bigint(64)  | YES  |      | NULL    |       |
| ROWS                          | bigint(64)  | YES  |      | NULL    |       |
| SIZE                          | bigint(64)  | YES  |      | NULL    |       |
| DELTA_RATE                    | double      | YES  |      | NULL    |       |
| DELTA_MEMTABLE_ROWS           | bigint(64)  | YES  |      | NULL    |       |
| DELTA_MEMTABLE_SIZE           | bigint(64)  | YES  |      | NULL    |       |
| DELTA_MEMTABLE_COLUMN_FILES   | bigint(64)  | YES  |      | NULL    |       |
| DELTA_MEMTABLE_DELETE_RANGES  | bigint(64)  | YES  |      | NULL    |       |
| DELTA_PERSISTED_PAGE_ID       | bigint(64)  | YES  |      | NULL    |       |
| DELTA_PERSISTED_ROWS          | bigint(64)  | YES  |      | NULL    |       |
| DELTA_PERSISTED_SIZE          | bigint(64)  | YES  |      | NULL    |       |
| DELTA_PERSISTED_COLUMN_FILES  | bigint(64)  | YES  |      | NULL    |       |
| DELTA_PERSISTED_DELETE_RANGES | bigint(64)  | YES  |      | NULL    |       |
| DELTA_CACHE_SIZE              | bigint(64)  | YES  |      | NULL    |       |
| DELTA_INDEX_SIZE              | bigint(64)  | YES  |      | NULL    |       |
| STABLE_PAGE_ID                | bigint(64)  | YES  |      | NULL    |       |
| STABLE_ROWS                   | bigint(64)  | YES  |      | NULL    |       |
| STABLE_SIZE                   | bigint(64)  | YES  |      | NULL    |       |
| STABLE_DMFILES                | bigint(64)  | YES  |      | NULL    |       |
| STABLE_DMFILES_ID_0           | bigint(64)  | YES  |      | NULL    |       |
| STABLE_DMFILES_ROWS           | bigint(64)  | YES  |      | NULL    |       |
| STABLE_DMFILES_SIZE           | bigint(64)  | YES  |      | NULL    |       |
| STABLE_DMFILES_SIZE_ON_DISK   | bigint(64)  | YES  |      | NULL    |       |
| STABLE_DMFILES_PACKS          | bigint(64)  | YES  |      | NULL    |       |
| TIFLASH_INSTANCE              | varchar(64) | YES  |      | NULL    |       |
+-------------------------------+-------------+------+------+---------+-------+
33 行结果（0.00 秒）
```

`TIFLASH_SEGMENTS` 表中的字段说明如下：

- `DATABASE`：TiFlash 中的数据库名。该段属于此数据库中的某个表。
- `TABLE`：TiFlash 中的表名。该段属于此表。
- `TIDB_DATABASE`：TiDB 中的数据库名。该段属于此数据库中的某个表。
- `TIDB_TABLE`：TiDB 中的表名。该段属于此表。
- `TABLE_ID`：该段所属表的内部ID。此ID在 TiDB 集群内唯一。
- `IS_TOMBSTONE`：指示该段所属的表是否可以被回收。`1` 表示可以回收，`0` 表示处于正常状态。
- `SEGMENT_ID`：段ID，在同一表内唯一。
- `RANGE`：段包含的数据范围。
- `EPOCH`：段的更新版本。每个段的版本号递增且单调。
- `ROWS`：段中的总行数。
- `SIZE`：段数据的总大小（字节）。
- `DELTA_RATE`：Delta 层中总行数与段中行数的比例。
- `DELTA_MEMTABLE_ROWS`：Delta 层中缓存的总行数。
- `DELTA_MEMTABLE_SIZE`：Delta 层中缓存的数据总大小（字节）。
- `DELTA_MEMTABLE_COLUMN_FILES`：Delta 层中缓存的 Column Files 数量。
- `DELTA_MEMTABLE_DELETE_RANGES`：Delta 层中缓存的 Delete Ranges 数量。
- `DELTA_PERSISTED_PAGE_ID`：存储在磁盘上的 Delta 层数据的 ID。
- `DELTA_PERSISTED_ROWS`：Delta 层中持久化数据的总行数。
- `DELTA_PERSISTED_SIZE`：Delta 层中持久化数据的总大小（字节）。
- `DELTA_PERSISTED_COLUMN_FILES`：Delta 层中持久化的 Column Files 数量。
- `DELTA_PERSISTED_DELETE_RANGES`：Delta 层中持久化的 Delete Ranges 数量。
- `DELTA_CACHE_SIZE`：Delta 层的缓存大小（字节）。
- `DELTA_INDEX_SIZE`：Delta 层中索引的大小（字节）。
- `STABLE_PAGE_ID`：Stable 层中数据的磁盘存储ID。
- `STABLE_ROWS`：Stable 层中的总行数。
- `STABLE_SIZE`：Stable 层中数据的总大小（字节）。
- `STABLE_DMFILES`：Stable 层中的 DMFile 数量。
- `STABLE_DMFILES_ID_0`：Stable 层中第一个 DMFile 的磁盘存储ID。
- `STABLE_DMFILES_ROWS`：Stable 层中 DMFile 的总行数。
- `STABLE_DMFILES_SIZE`：Stable 层中 DMFile 的数据总大小（字节）。
- `STABLE_DMFILES_SIZE_ON_DISK`：Stable 层中 DMFile 占用的磁盘空间（字节）。
- `STABLE_DMFILES_PACKS`：Stable 层中 DMFile 的 Pack 数量。
- `TIFLASH_INSTANCE`：TiFlash 实例的地址。