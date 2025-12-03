---
title: TIFLASH_SEGMENTS
summary: 了解 `TIFLASH_SEGMENTS` information_schema 表。
---

# TIFLASH_SEGMENTS

> **Warning:**
>
> 不要在生产环境中使用此表，因为该表的字段不稳定，并且在 TiDB 的新版本中可能会发生变更，且不会提前通知。

`TIFLASH_SEGMENTS` 表提供了关于 TiFlash 中数据表分段（segment）的统计信息。

```sql
USE information_schema;
DESC tiflash_segments;
```

```sql
+-------------------------------+-------------+------+------+---------+-------+
| Field                         | Type        | Null | Key  | Default | Extra |
+-------------------------------+-------------+------+------+---------+-------+
| TIDB_DATABASE                 | varchar(64) | YES  |      | NULL    |       |
| TIDB_TABLE                    | varchar(64) | YES  |      | NULL    |       |
| TABLE_ID                      | bigint      | YES  |      | NULL    |       |
| IS_TOMBSTONE                  | bigint      | YES  |      | NULL    |       |
| SEGMENT_ID                    | bigint      | YES  |      | NULL    |       |
| RANGE                         | varchar(64) | YES  |      | NULL    |       |
| EPOCH                         | bigint      | YES  |      | NULL    |       |
| ROWS                          | bigint      | YES  |      | NULL    |       |
| SIZE                          | bigint      | YES  |      | NULL    |       |
| DELTA_RATE                    | double      | YES  |      | NULL    |       |
| DELTA_MEMTABLE_ROWS           | bigint      | YES  |      | NULL    |       |
| DELTA_MEMTABLE_SIZE           | bigint      | YES  |      | NULL    |       |
| DELTA_MEMTABLE_COLUMN_FILES   | bigint      | YES  |      | NULL    |       |
| DELTA_MEMTABLE_DELETE_RANGES  | bigint      | YES  |      | NULL    |       |
| DELTA_PERSISTED_PAGE_ID       | bigint      | YES  |      | NULL    |       |
| DELTA_PERSISTED_ROWS          | bigint      | YES  |      | NULL    |       |
| DELTA_PERSISTED_SIZE          | bigint      | YES  |      | NULL    |       |
| DELTA_PERSISTED_COLUMN_FILES  | bigint      | YES  |      | NULL    |       |
| DELTA_PERSISTED_DELETE_RANGES | bigint      | YES  |      | NULL    |       |
| DELTA_CACHE_SIZE              | bigint      | YES  |      | NULL    |       |
| DELTA_INDEX_SIZE              | bigint      | YES  |      | NULL    |       |
| STABLE_PAGE_ID                | bigint      | YES  |      | NULL    |       |
| STABLE_ROWS                   | bigint      | YES  |      | NULL    |       |
| STABLE_SIZE                   | bigint      | YES  |      | NULL    |       |
| STABLE_DMFILES                | bigint      | YES  |      | NULL    |       |
| STABLE_DMFILES_ID_0           | bigint      | YES  |      | NULL    |       |
| STABLE_DMFILES_ROWS           | bigint      | YES  |      | NULL    |       |
| STABLE_DMFILES_SIZE           | bigint      | YES  |      | NULL    |       |
| STABLE_DMFILES_SIZE_ON_DISK   | bigint      | YES  |      | NULL    |       |
| STABLE_DMFILES_PACKS          | bigint      | YES  |      | NULL    |       |
| TIFLASH_INSTANCE              | varchar(64) | YES  |      | NULL    |       |
+-------------------------------+-------------+------+------+---------+-------+
```

`TIFLASH_SEGMENTS` 表中的字段说明如下：

- `TIDB_DATABASE`：TiDB 中的数据库名。该分段属于此数据库下的某个表。
- `TIDB_TABLE`：TiDB 中的表名。该分段属于此表。
- `TABLE_ID`：该分段所属表的内部 ID。该 ID 在 TiDB 集群内唯一。
- `IS_TOMBSTONE`：表示该分段所属的表是否可以被回收。`1` 表示该表可以被回收，`0` 表示该表处于正常状态。
- `SEGMENT_ID`：分段 ID，在同一张表内唯一。
- `RANGE`：该分段包含的数据范围。
- `EPOCH`：分段的更新版本号。每个分段的版本号单调递增。
- `ROWS`：该分段中的总行数。
- `SIZE`：该分段数据的总大小（字节数）。
- `DELTA_RATE`：Delta 层中总行数与该分段总行数的比例。
- `DELTA_MEMTABLE_ROWS`：Delta 层中缓存的总行数。
- `DELTA_MEMTABLE_SIZE`：Delta 层中缓存数据的总大小（字节数）。
- `DELTA_MEMTABLE_COLUMN_FILES`：Delta 层中缓存的 Column File 数量。
- `DELTA_MEMTABLE_DELETE_RANGES`：Delta 层中缓存的 Delete Range 数量。
- `DELTA_PERSISTED_PAGE_ID`：Delta 层中持久化到磁盘的数据的 ID。
- `DELTA_PERSISTED_ROWS`：Delta 层中持久化数据的总行数。
- `DELTA_PERSISTED_SIZE`：Delta 层中持久化数据的总大小（字节数）。
- `DELTA_PERSISTED_COLUMN_FILES`：Delta 层中持久化的 Column File 数量。
- `DELTA_PERSISTED_DELETE_RANGES`：Delta 层中持久化的 Delete Range 数量。
- `DELTA_CACHE_SIZE`：Delta 层中缓存的大小（字节数）。
- `DELTA_INDEX_SIZE`：Delta 层中索引的大小（字节数）。
- `STABLE_PAGE_ID`：Stable 层中数据的磁盘存储 ID。
- `STABLE_ROWS`：Stable 层中的总行数。
- `STABLE_SIZE`：Stable 层中数据的总大小（字节数）。
- `STABLE_DMFILES`：Stable 层中的 DMFile 数量。
- `STABLE_DMFILES_ID_0`：Stable 层中第一个 DMFile 的磁盘存储 ID。
- `STABLE_DMFILES_ROWS`：Stable 层中 DMFile 的总行数。
- `STABLE_DMFILES_SIZE`：Stable 层中 DMFile 的总数据大小（字节数）。
- `STABLE_DMFILES_SIZE_ON_DISK`：Stable 层中 DMFile 占用的磁盘空间（字节数）。
- `STABLE_DMFILES_PACKS`：Stable 层中 DMFile 的 Pack 数量。
- `TIFLASH_INSTANCE`：TiFlash 实例的地址。