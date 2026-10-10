---
title: VACUUM DROP TABLE
summary: VACUUM DROP TABLE コマンドは、削除されたテーブルのデータファイルを完全に削除することでストレージ容量を節約し、ストレージ領域を解放し、この処理を効率的に管理できるようにします。特定のデータベースを対象にする、プレビューする、vacuum 対象のデータファイル数を制限するといったオプションパラメータを提供します。データベース内の削除済みテーブルを一覧表示するには、SHOW DROP TABLES を使用します。
---

# VACUUM DROP TABLE

VACUUM DROP TABLE コマンドは、削除されたテーブルのデータファイルを完全に削除することでストレージ容量を節約し、ストレージ領域を解放し、この処理を効率的に管理できるようにします。特定のデータベースを対象にする、プレビューする、vacuum 対象のデータファイル数を制限するといったオプションパラメータを提供します。データベース内の削除済みテーブルを一覧表示するには、[SHOW DROP TABLES](/tidb-cloud-lake/sql/show-drop-tables.md) を使用します。

関連情報: [VACUUM TABLE](/tidb-cloud-lake/sql/vacuum-table.md)

## 構文 {#syntax}

```sql
VACUUM DROP TABLE
    [ FROM <database_name> ]
    [ DRY RUN [SUMMARY] ]
    [ LIMIT <file_count> ]
```

- `FROM <database_name>`: このパラメータは、削除されたテーブルの検索対象を特定のデータベースに限定します。指定しない場合、コマンドは削除済みのデータベースを含むすべてのデータベースをスキャンします。

  ```sql title="Example:"
  -- Remove dropped tables from the "default" database
  // highlight-next-line
  VACUUM DROP TABLE FROM default;

  -- Remove dropped tables from all databases
  // highlight-next-line
  VACUUM DROP TABLE;
  ```

- `DRY RUN [SUMMARY]`: このパラメータを指定すると、データファイルは削除されません。代わりに、このパラメータを指定しなかった場合に削除されるデータファイルを示す結果が返されます。例については、[出力](#output) セクションを参照してください。

- `LIMIT <file_count>`: このパラメータは、DRY RUN パラメータの有無にかかわらず使用できます。DRY RUN とともに使用した場合、`DRY RUN` の結果に表示されるデータファイル数を制限します。`DRY RUN` なしで使用した場合、vacuum 対象のデータファイル数を制限します。

### 出力 {#output}

VACUUM DROP TABLE コマンドは、`DRY RUN` または `DRY RUN SUMMARY` パラメータが指定されている場合に結果を返します。

- `DRY RUN`: 各削除済みテーブルについて、最大 1,000 個の Candidate ファイルとそのサイズ（バイト単位）の一覧を返します。
- `DRY RUN SUMMARY`: 各削除済みテーブルについて、削除対象ファイルの総数と合計サイズを返します。

```sql title='Example:'
// highlight-next-line
VACUUM DROP TABLE DRY RUN;

┌──────────────────────────────────────────────────────────────────┐
│  table │                     file                    │ file_size │
├────────┼─────────────────────────────────────────────┼───────────┤
│ b      │ 313ebd4da5cc493f9a7d491da8253ce2_v2.parquet │       210 │
│ b      │ 737f2215b8ac4a268d5b7f2218273358_v2.parquet │       210 │
│ b      │ 737f2215b8ac4a268d5b7f2218273358_v4.parquet │       340 │
│ b      │ 313ebd4da5cc493f9a7d491da8253ce2_v4.parquet │       340 │
│ b      │ last_snapshot_location_hint                 │        72 │
│ b      │ 7e01fa5c2e0a495298942671447dc8cb_v4.mpk     │       515 │
│ b      │ 2bc90e5be55c44258a736d27e5f7ac9e_v4.mpk     │       459 │
│ b      │ 85e73803aabc4eb48774db3d932312dd_v4.mpk     │       534 │
│ b      │ f0e507d0b825428dbfe57c8d8b620a15_v4.mpk     │       533 │
│ c      │ cee790e76f6e4e92bc9dab3b9e873dcf_v2.parquet │       210 │
│ c      │ 4bcb2cef3b6344cb951908ebee5ceb36_v2.parquet │       210 │
│ c      │ cee790e76f6e4e92bc9dab3b9e873dcf_v4.parquet │       340 │
│ c      │ 4bcb2cef3b6344cb951908ebee5ceb36_v4.parquet │       340 │
│ c      │ last_snapshot_location_hint                 │        71 │
│ c      │ 414fc6a8dc6746afbc576cf8fddfcdf3_v4.mpk     │       516 │
│ c      │ 8d0d115c438244c295e3bfd50d556e39_v4.mpk     │       458 │
│ c      │ 28e4f551cc634d3d8d7e648c3baa5f5c_v4.mpk     │       534 │
│ c      │ 007b57e08eda419fbb451a3a3ed71de8_v4.mpk     │       533 │
└──────────────────────────────────────────────────────────────────┘
// highlight-next-line
VACUUM DROP TABLE DRY RUN SUMMARY;

┌───────────────────────────────────┐
│  table │ total_files │ total_size │
├────────┼─────────────┼────────────┤
│ b      │           9 │       3213 │
│ c      │           9 │       3212 │
└───────────────────────────────────┘
```

### データ保持期間の調整 {#adjusting-data-retention-time}

VACUUM DROP TABLE コマンドは、`DATA_RETENTION_TIME_IN_DAYS` 設定より古いデータファイルを削除します。この保持期間は必要に応じて調整でき、たとえば 2 日に設定できます。

```sql
SET GLOBAL DATA_RETENTION_TIME_IN_DAYS = 2;
```

`DATA_RETENTION_TIME_IN_DAYS` のデフォルト値は 1 日（24 時間）で、最大値は {{{ .lake }}} のエディションによって異なります。

| エディション                                  | デフォルト保持期間 | 最大保持期間     |
| ---------------------------------------- | ----------------- | ---------------- |
| {{{ .lake }}} Community および Enterprise エディション | 1 日（24 時間）   | 90 日            |
| {{{ .lake }}} (Personal)                | 1 日（24 時間）   | 1 日（24 時間）  |
| {{{ .lake }}} (Business)                | 1 日（24 時間）   | 90 日            |

現在の `DATA_RETENTION_TIME_IN_DAYS` の値を確認するには、次を実行します。

```sql
SHOW SETTINGS LIKE 'DATA_RETENTION_TIME_IN_DAYS';
```