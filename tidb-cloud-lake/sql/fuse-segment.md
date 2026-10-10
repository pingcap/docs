---
title: FUSE_SEGMENT
summary: 指定したテーブルスナップショットのセグメント情報を返します。{{{ .lake }}} における segment について詳しくは、What are Snapshot, Segment, and Block? を参照してください。
---

# FUSE_SEGMENT

指定したテーブルスナップショットのセグメント情報を返します。{{{ .lake }}} における segment について詳しくは、[What are Snapshot, Segment, and Block?](/tidb-cloud-lake/sql/optimize-table.md#-lake--data-storage-snapshot-segment-and-block) を参照してください。

関連情報:

- [FUSE_SNAPSHOT](/tidb-cloud-lake/sql/fuse-snapshot.md)
- [FUSE_BLOCK](/tidb-cloud-lake/sql/fuse-block.md)

## 構文 {#syntax}

```sql
FUSE_SEGMENT('<database_name>', '<table_name>','<snapshot_id>')
```

## 例 {#examples}

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