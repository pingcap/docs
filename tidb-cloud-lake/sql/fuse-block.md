---
title: FUSE_BLOCK
summary: テーブルの最新または指定したスナップショットの block 情報を返します。{{{ .lake }}} における block について詳しくは、What are Snapshot, Segment, and Block? を参照してください。
---

# FUSE_BLOCK

テーブルの最新または指定したスナップショットの block 情報を返します。{{{ .lake }}} における block について詳しくは、[What are Snapshot, Segment, and Block?](/tidb-cloud-lake/sql/optimize-table.md#-lake--data-storage-snapshot-segment-and-block) を参照してください。

このコマンドは、スナップショットによって参照される各 parquet ファイルのロケーション情報を返します。これにより、下流アプリケーションはファイルに保存されたデータへアクセスし、利用できます。

関連情報:

- [FUSE_SNAPSHOT](/tidb-cloud-lake/sql/fuse-snapshot.md)
- [FUSE_SEGMENT](/tidb-cloud-lake/sql/fuse-segment.md)

## 構文 {#syntax}

```sql
FUSE_BLOCK('<database_name>', '<table_name>'[, '<snapshot_id>'])
```

## 例 {#examples}

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