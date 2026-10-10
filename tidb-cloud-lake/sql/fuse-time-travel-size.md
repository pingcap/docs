---
title: FUSE_TIME_TRAVEL_SIZE
summary: テーブルの履歴データ（Time Travel 用）のストレージサイズを計算します。
---

# FUSE_TIME_TRAVEL_SIZE

テーブルの履歴データ（Time Travel 用）のストレージサイズを計算します。

## 構文 {#syntax}

```sql
-- Calculate historical data size for all tables in all databases
SELECT ...
FROM fuse_time_travel_size();

-- Calculate historical data size for all tables in a specified database
SELECT ...
FROM fuse_time_travel_size('<database_name>');

-- Calculate historical data size for a specified table in a specified database
SELECT ...
FROM fuse_time_travel_size('<database_name>', '<table_name>');
```

## 出力 {#output}

この関数は、次のカラムを含む結果セットを返します。

| カラム                           | 説明                                                                                           |
|----------------------------------|-------------------------------------------------------------------------------------------------------|
| `database_name`                  | テーブルが存在するデータベースの名前。                                                  |
| `table_name`                     | テーブルの名前。                                                                                |
| `is_dropped`                     | テーブルが削除されているかどうかを示します（削除済みテーブルは `true`、それ以外は `false`）。          |
| `time_travel_size`               | テーブルの履歴データ（Time Travel 用）の合計ストレージサイズ（バイト単位）。                  |
| `latest_snapshot_size`           | テーブルの最新スナップショットのストレージサイズ（バイト単位）。                                       |
| `data_retention_period_in_hours` | Time Travel データの保持期間（時間単位）です（`NULL` はデフォルトの保持ポリシーを使用することを意味します）。 |
| `error`                          | ストレージサイズの取得中に発生したエラー（エラーが発生しなかった場合は `NULL`）。               |

## 例 {#examples}

この例では、`default` データベース内のすべてのテーブルについて履歴データを計算します。

```sql
SELECT * FROM fuse_time_travel_size('default')

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ database_name │ table_name │ is_dropped │ time_travel_size │ latest_snapshot_size │ data_retention_period_in_hours │       error      │
├───────────────┼────────────┼────────────┼──────────────────┼──────────────────────┼────────────────────────────────┼──────────────────┤
│ default       │ books      │ true       │             2810 │                 1490 │                           NULL │ NULL             │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```