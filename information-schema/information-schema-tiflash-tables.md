---
title: TIFLASH_TABLES
summary: 了解 `TIFLASH_TABLES` information_schema 表格的信息。
---

# TIFLASH_TABLES

> **Warning:**
>
> 不要在生产环境中使用此表，因为表中的字段不稳定，可能在 TiDB 的新版本中发生变化，且不会提前通知。

`TIFLASH_TABLES` 表提供关于 TiFlash 中数据表的统计信息。

```sql
USE information_schema;
DESC tiflash_tables;
```

```sql
+-------------------------------------------+--------------+------+------+---------+-------+
| Field                                     | Type         | Null | Key  | Default | Extra |
+-------------------------------------------+--------------+------+------+---------+-------+
| DATABASE                                  | varchar(64)  | YES  |      | NULL    |       |
| TABLE                                     | varchar(64)  | YES  |      | NULL    |       |
| TIDB_DATABASE                             | varchar(64)  | YES  |      | NULL    |       |
| TIDB_TABLE                                | varchar(64)  | YES  |      | NULL    |       |
| TABLE_ID                                  | bigint(64)   | YES  |      | NULL    |       |
| IS_TOMBSTONE                              | bigint(64)   | YES  |      | NULL    |       |
| SEGMENT_COUNT                             | bigint(64)   | YES  |      | NULL    |       |
| TOTAL_ROWS                                | bigint(64)   | YES  |      | NULL    |       |
| TOTAL_SIZE                                | bigint(64)   | YES  |      | NULL    |       |
| TOTAL_DELETE_RANGES                       | bigint(64)   | YES  |      | NULL    |       |
| DELTA_RATE_ROWS                           | double       | YES  |      | NULL    |       |
| DELTA_RATE_SEGMENTS                       | double       | YES  |      | NULL    |       |
| DELTA_PLACED_RATE                         | double       | YES  |      | NULL    |       |
| DELTA_CACHE_SIZE                          | bigint(64)   | YES  |      | NULL    |       |
| DELTA_CACHE_RATE                          | double       | YES  |      | NULL    |       |
| DELTA_CACHE_WASTED_RATE                   | double       | YES  |      | NULL    |       |
| DELTA_INDEX_SIZE                          | bigint(64)   | YES  |      | NULL    |       |
| AVG_SEGMENT_ROWS                          | double       | YES  |      | NULL    |       |
| AVG_SEGMENT_SIZE                          | double       | YES  |      | NULL    |       |
| DELTA_COUNT                               | bigint(64)   | YES  |      | NULL    |       |
| TOTAL_DELTA_ROWS                          | bigint(64)   | YES  |      | NULL    |       |
| TOTAL_DELTA_SIZE                          | bigint(64)   | YES  |      | NULL    |       |
| AVG_DELTA_ROWS                            | double       | YES  |      | NULL    |       |
| AVG_DELTA_SIZE                            | double       | YES  |      | NULL    |       |
| AVG_DELTA_DELETE_RANGES                   | double       | YES  |      | NULL    |       |
| STABLE_COUNT                              | bigint(64)   | YES  |      | NULL    |       |
| TOTAL_STABLE_ROWS                         | bigint(64)   | YES  |      | NULL    |       |
| TOTAL_STABLE_SIZE                         | bigint(64)   | YES  |      | NULL    |       |
| TOTAL_STABLE_SIZE_ON_DISK                 | bigint(64)   | YES  |      | NULL    |       |
| AVG_STABLE_ROWS                           | double       | YES  |      | NULL    |       |
| AVG_STABLE_SIZE                           | double       | YES  |      | NULL    |       |
| TOTAL_PACK_COUNT_IN_DELTA                 | bigint(64)   | YES  |      | NULL    |       |
| MAX_PACK_COUNT_IN_DELTA                   | bigint(64)   | YES  |      | NULL    |       |
| AVG_PACK_COUNT_IN_DELTA                   | double       | YES  |      | NULL    |       |
| AVG_PACK_ROWS_IN_DELTA                    | double       | YES  |      | NULL    |       |
| AVG_PACK_SIZE_IN_DELTA                    | double       | YES  |      | NULL    |       |
| TOTAL_PACK_COUNT_IN_STABLE                | bigint(64)   | YES  |      | NULL    |       |
| AVG_PACK_COUNT_IN_STABLE                  | double       | YES  |      | NULL    |       |
| AVG_PACK_ROWS_IN_STABLE                   | double       | YES  |      | NULL    |       |
| AVG_PACK_SIZE_IN_STABLE                   | double       | YES  |      | NULL    |       |
| STORAGE_STABLE_NUM_SNAPSHOTS              | bigint(64)   | YES  |      | NULL    |       |
| STORAGE_STABLE_OLDEST_SNAPSHOT_LIFETIME   | double       | YES  |      | NULL    |       |
| STORAGE_STABLE_OLDEST_SNAPSHOT_THREAD_ID  | bigint(64)   | YES  |      | NULL    |       |
| STORAGE_STABLE_OLDEST_SNAPSHOT_TRACING_ID | varchar(128) | YES  |      | NULL    |       |
| STORAGE_DELTA_NUM_SNAPSHOTS               | bigint(64)   | YES  |      | NULL    |       |
| STORAGE_DELTA_OLDEST_SNAPSHOT_LIFETIME    | double       | YES  |      | NULL    |       |
| STORAGE_DELTA_OLDEST_SNAPSHOT_THREAD_ID   | bigint(64)   | YES  |      | NULL    |       |
| STORAGE_DELTA_OLDEST_SNAPSHOT_TRACING_ID  | varchar(128) | YES  |      | NULL    |       |
| STORAGE_META_NUM_SNAPSHOTS                | bigint(64)   | YES  |      | NULL    |       |
| STORAGE_META_OLDEST_SNAPSHOT_LIFETIME     | double       | YES  |      | NULL    |       |
| STORAGE_META_OLDEST_SNAPSHOT_THREAD_ID    | bigint(64)   | YES  |      | NULL    |       |
| STORAGE_META_OLDEST_SNAPSHOT_TRACING_ID   | varchar(128) | YES  |      | NULL    |       |
| BACKGROUND_TASKS_LENGTH                   | bigint(64)   | YES  |      | NULL    |       |
| TIFLASH_INSTANCE                          | varchar(64)  | YES  |      | NULL    |       |
+-------------------------------------------+--------------+------+------+---------+-------+
54 rows in set (0.00 sec)
```

`TIFLASH_TABLES` 表中的字段说明如下：

- `DATABASE`: TiFlash 中所属表的数据库名。
- `TABLE`: TiFlash 中的表名。
- `TIDB_DATABASE`: TiDB 中所属表的数据库名。
- `TIDB_TABLE`: TiDB 中的表名。
- `TABLE_ID`: 表的内部 ID，在 TiDB 集群中唯一。
- `IS_TOMBSTONE`: 表示该表是否可以回收。`1` 表示可以回收，`0` 表示处于正常状态。
- `SEGMENT_COUNT`: 表中的段数。段是 TiFlash 中的数据管理单元。
- `TOTAL_ROWS`: 表中的总行数。
- `TOTAL_SIZE`: 表的总大小（字节数）。
- `TOTAL_DELETE_RANGES`: 表中的删除范围总数。
- `DELTA_RATE_ROWS`: Delta 层中表的总行数占比。
- `DELTA_RATE_SEGMENTS`: 表中包含非空 Delta 层的段的比例。
- `DELTA_PLACED_RATE`: 在 Delta 层中已完成索引构建的行的比例。
- `DELTA_CACHE_SIZE`: 表在 Delta 层中的缓存大小（字节）。
- `DELTA_CACHE_RATE`: Delta 层中缓存数据的占比。
- `DELTA_CACHE_WASTED_RATE`: Delta 层中无效缓存数据的占比。
- `DELTA_INDEX_SIZE`: Delta 层中索引占用的内存大小（字节）。
- `AVG_SEGMENT_ROWS`: 表所有段的平均行数。
- `AVG_SEGMENT_SIZE`: 表所有段的平均大小（字节）。
- `DELTA_COUNT`: 表中包含非空 Delta 层的段数。
- `TOTAL_DELTA_ROWS`: Delta 层中的总行数。
- `TOTAL_DELTA_SIZE`: Delta 层中数据的总大小（字节）。
- `AVG_DELTA_ROWS`: 所有 Delta 层中数据的平均行数。
- `AVG_DELTA_SIZE`: 所有 Delta 层中数据的平均大小（字节）。
- `AVG_DELTA_DELETE_RANGES`: 所有 Delta 层中删除范围操作的平均数。
- `STABLE_COUNT`: 表中包含非空 Stable 层的段数。
- `TOTAL_STABLE_ROWS`: 所有 Stable 层中的总行数。
- `TOTAL_STABLE_SIZE`: 所有 Stable 层中数据的总大小（字节）。
- `TOTAL_STABLE_SIZE_ON_DISK`: 所有 Stable 层中数据在磁盘上的占用空间（字节）。
- `AVG_STABLE_ROWS`: 所有 Stable 层中数据的平均行数。
- `AVG_STABLE_SIZE`: 所有 Stable 层中数据的平均大小（字节）。
- `TOTAL_PACK_COUNT_IN_DELTA`: 所有 Delta 层中列文件（Column Files）总数。
- `MAX_PACK_COUNT_IN_DELTA`: 单个 Delta 层中的最大列文件数。
- `AVG_PACK_COUNT_IN_DELTA`: 所有 Delta 层中列文件的平均数。
- `AVG_PACK_ROWS_IN_DELTA`: 所有 Delta 层中列文件的平均行数。
- `AVG_PACK_SIZE_IN_DELTA`: 所有 Delta 层中列文件的平均大小（字节）。
- `TOTAL_PACK_COUNT_IN_STABLE`: 所有 Stable 层中的 Pack 数量。
- `AVG_PACK_COUNT_IN_STABLE`: 所有 Stable 层中 Pack 的平均数。
- `AVG_PACK_ROWS_IN_STABLE`: 所有 Stable 层中 Pack 的平均行数。
- `AVG_PACK_SIZE_IN_STABLE`: Stable 层中 Pack 的平均大小（字节）。
- `STORAGE_STABLE_NUM_SNAPSHOTS`: Stable 层中的快照数。
- `STORAGE_STABLE_OLDEST_SNAPSHOT_LIFETIME`: Stable 层中最早快照的存活时间（秒）。
- `STORAGE_STABLE_OLDEST_SNAPSHOT_THREAD_ID`: 最早快照的线程 ID。
- `STORAGE_STABLE_OLDEST_SNAPSHOT_TRACING_ID`: 最早快照的追踪 ID。
- `STORAGE_DELTA_NUM_SNAPSHOTS`: Delta 层中的快照数。
- `STORAGE_DELTA_OLDEST_SNAPSHOT_LIFETIME`: Delta 层中最早快照的存活时间（秒）。
- `STORAGE_DELTA_OLDEST_SNAPSHOT_THREAD_ID`: 最早快照的线程 ID。
- `STORAGE_DELTA_OLDEST_SNAPSHOT_TRACING_ID`: 最早快照的追踪 ID。
- `STORAGE_META_NUM_SNAPSHOTS`: 元信息中的快照数。
- `STORAGE_META_OLDEST_SNAPSHOT_LIFETIME`: 元信息中最早快照的存活时间（秒）。
- `STORAGE_META_OLDEST_SNAPSHOT_THREAD_ID`: 元信息中最早快照的线程 ID。
- `STORAGE_META_OLDEST_SNAPSHOT_TRACING_ID`: 元信息中最早快照的追踪 ID。
- `BACKGROUND_TASKS_LENGTH`: 后台任务队列长度。
- `TIFLASH_INSTANCE`: TiFlash 实例的地址。