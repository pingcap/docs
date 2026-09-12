---
title: FUSE_COLUMN
summary: 返回表的最新或指定快照的列信息。有关 {{{ .lake }}} 中 block 的更多信息，请参阅什么是 Snapshot、Segment 和 Block？。
---

# FUSE_COLUMN

返回表的最新或指定快照的列信息。有关 {{{ .lake }}} 中 block 的更多信息，请参阅[什么是 Snapshot、Segment 和 Block？](/tidb-cloud-lake/sql/optimize-table.md#-lake--data-storage-snapshot-segment-and-block)。

另请参阅：

- [FUSE_SNAPSHOT](/tidb-cloud-lake/sql/fuse-snapshot.md)
- [FUSE_SEGMENT](/tidb-cloud-lake/sql/fuse-segment.md)
- [FUSE_BLOCK](/tidb-cloud-lake/sql/fuse-block.md)

## 语法 {#syntax}

```sql
FUSE_COLUMN('<database_name>', '<table_name>'[, '<snapshot_id>'])
```

## 示例 {#examples}

```sql
CREATE TABLE mytable(c int);
INSERT INTO mytable values(1);
INSERT INTO mytable values(2);

SELECT * FROM FUSE_COLUMN('default', 'mytable');

---
+----------------------------------+----------------------------+---------------------------------------------------------+------------+-----------+-----------+-------------+-------------+-----------+--------------+------------------+
| snapshot_id                      | timestamp                  | block_location                                          | block_size | file_size | row_count | column_name | column_type | column_id | block_offset | bytes_compressed |
+----------------------------------+----------------------------+---------------------------------------------------------+------------+-----------+-----------+-------------+-------------+-----------+--------------+------------------+
| 3faefc1a9b6a48f388a8b59228dd06c1 | 2023-07-18 03:06:30.276502 | 1/118746/_b/44df130c207745cb858928135d39c1c0_v2.parquet |          4 |       196 |         1 | c           | Int32       |         0 |            8 |               14 |
| 3faefc1a9b6a48f388a8b59228dd06c1 | 2023-07-18 03:06:30.276502 | 1/118746/_b/b6f8496d7e3f4f62a89c09572840cf70_v2.parquet |          4 |       196 |         1 | c           | Int32       |         0 |            8 |               14 |
+----------------------------------+----------------------------+---------------------------------------------------------+------------+-----------+-----------+-------------+-------------+-----------+--------------+------------------+
```