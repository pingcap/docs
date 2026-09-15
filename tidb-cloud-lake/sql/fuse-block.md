---
title: FUSE_BLOCK
summary: 返回表的最新或指定快照的 block 信息。有关 {{{ .lake }}} 中 block 的更多信息，请参阅 What are Snapshot, Segment, and Block?。
---

# FUSE_BLOCK

返回表的最新或指定快照的 block 信息。有关 {{{ .lake }}} 中 block 的更多信息，请参阅 [Snapshot、Segment 和 Block 是什么？](/tidb-cloud-lake/sql/optimize-table.md#-lake--data-storage-snapshot-segment-and-block)。

该命令返回某个快照所引用的每个 parquet 文件的位置信息。这使下游应用能够访问并使用存储在这些文件中的数据。

另请参阅：

- [FUSE_SNAPSHOT](/tidb-cloud-lake/sql/fuse-snapshot.md)
- [FUSE_SEGMENT](/tidb-cloud-lake/sql/fuse-segment.md)

## 语法 {#syntax}

```sql
FUSE_BLOCK('<database_name>', '<table_name>'[, '<snapshot_id>'])
```

## 示例 {#examples}

```sql
CREATE TABLE mytable(c int);
INSERT INTO mytable values(1);
INSERT INTO mytable values(2);

SELECT * FROM FUSE_BLOCK('default', 'mytable');

---
+----------------------------------+----------------------------+----------------------------------------------------+------------+----------------------------------------------------+-------------------+
| snapshot_id                      | timestamp                  | block_location                                     | block_size | bloom_filter_location                              | bloom_filter_size |
+----------------------------------+----------------------------+----------------------------------------------------+------------+----------------------------------------------------+-------------------+
| 51e84b56458f44269b05a059b364a659 | 2022-09-15 07:14:14.137268 | 1/7/_b/39a6dbbfd9b44ad5a8ec8ab264c93cf5_v0.parquet |          4 | 1/7/_i/39a6dbbfd9b44ad5a8ec8ab264c93cf5_v1.parquet |               221 |
| 51e84b56458f44269b05a059b364a659 | 2022-09-15 07:14:14.137268 | 1/7/_b/d0ee9688c4d24d6da86acd8b0d6f4fad_v0.parquet |          4 | 1/7/_i/d0ee9688c4d24d6da86acd8b0d6f4fad_v1.parquet |               219 |
+----------------------------------+----------------------------+----------------------------------------------------+------------+----------------------------------------------------+-------------------+
```