---
title: FUSE_SEGMENT
summary: 返回指定表快照的 segment 信息。有关 {{{ .lake }}} 中 segment 的更多信息，请参阅什么是 Snapshot、Segment 和 Block？。
---

# FUSE_SEGMENT

返回指定表快照的 segment 信息。有关 {{{ .lake }}} 中 segment 的更多信息，请参阅 [什么是 Snapshot、Segment 和 Block？](/tidb-cloud-lake/sql/optimize-table.md#-lake--data-storage-snapshot-segment-and-block)。

另请参阅：

- [FUSE_SNAPSHOT](/tidb-cloud-lake/sql/fuse-snapshot.md)
- [FUSE_BLOCK](/tidb-cloud-lake/sql/fuse-block.md)

## 语法 {#syntax}

```sql
FUSE_SEGMENT('<database_name>', '<table_name>','<snapshot_id>')
```

## 示例 {#examples}

```sql
CREATE TABLE mytable(c int);
INSERT INTO mytable values(1);
INSERT INTO mytable values(2);

-- Obtain a snapshot ID
SELECT snapshot_id FROM FUSE_SNAPSHOT('default', 'mytable') limit 1;

---
+----------------------------------+
| snapshot_id                      |
+----------------------------------+
| 82c572947efa476892bd7c0635158ba2 |
+----------------------------------+

SELECT * FROM FUSE_SEGMENT('default', 'mytable', '82c572947efa476892bd7c0635158ba2');

---
+----------------------------------------------------+----------------+-------------+-----------+--------------------+------------------+
| file_location                                      | format_version | block_count | row_count | bytes_uncompressed | bytes_compressed |
+----------------------------------------------------+----------------+-------------+-----------+--------------------+------------------+
| 1/319/_sg/d35fe7bf99584301b22e8f6a8a9c97f9_v1.json |              1 |           1 |         1 |                  4 |              184 |
| 1/319/_sg/c261059d47c840e1b749222dabb4b2bb_v1.json |              1 |           1 |         1 |                  4 |              184 |
+----------------------------------------------------+----------------+-------------+-----------+--------------------+------------------+
```