---
title: ICEBERG_SNAPSHOT
summary: データ変更、操作、要約統計情報など、Iceberg テーブルのスナップショットに関するメタデータを返します。
---

# ICEBERG_SNAPSHOT

データ変更、操作、要約統計情報など、Iceberg テーブルのスナップショットに関するメタデータを返します。

## 構文 {#syntax}

```sql
ICEBERG_SNAPSHOT('<database_name>', '<table_name>');
```

## 出力 {#output}

この関数は、次のカラムを持つテーブルを返します。

- `committed_at` (`TIMESTAMP`): スナップショットがコミットされた時刻のタイムスタンプ。
- `snapshot_id` (`BIGINT`): スナップショットの一意識別子。
- `parent_id` (`BIGINT`): 該当する場合の親スナップショット ID。
- `operation` (`STRING`): 実行された操作の種類（例: append、overwrite、delete）。
- `manifest_list` (`STRING`): スナップショットに関連付けられた manifest list のファイルパス。
- `summary` (`MAP<STRING, STRING>`): 次のような追加メタデータを含む JSON ライクな構造:
    - `added-data-files`: 新たに追加されたデータファイル数。
    - `added-records`: 新たに追加されたレコード数。
    - `total-records`: スナップショット内のレコード総数。
    - `total-files-size`: すべてのデータファイルの合計サイズ（バイト単位）。
    - `total-data-files`: スナップショット内のデータファイル総数。
    - `total-delete-files`: スナップショット内の delete ファイル総数。

## 例 {#examples}

```sql
SELECT * FROM ICEBERG_SNAPSHOT('tpcds', 'catalog_returns');

╭───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│        committed_at        │     snapshot_id     │ parent_id │ operation │                     manifest_list                    │                       summary                       │
├────────────────────────────┼─────────────────────┼───────────┼───────────┼──────────────────────────────────────────────────────┼─────────────────────────────────────────────────────┤
│ 2025-03-12 23:18:26.626000 │ 7565767416590411866 │         0 │ append    │ s3://warehouse/catalog_returns/metadata/snap-7565767 │ {'spark.app.id':'local-1741821433430','added-data-f │
│                            │                     │           │           │ 416590411866-1-fa1ea4d5-a382-497a-9f22-1acb9a74a346. │ iles':'2','added-records':'144067','total-equality- │
│                            │                     │           │           │ avro                                                 │ deletes':'0','changed-partition-count':'1','total-r │
│                            │                     │           │           │                                                      │ ecords':'144067','total-files-size':'7679811','tota │
│                            │                     │           │           │                                                      │ l-data-files':'2','added-files-size':'7679811','tot │
│                            │                     │           │           │                                                      │ al-delete-files':'0','total-position-deletes':'0'}  │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```