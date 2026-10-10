---
title: VACUUM TABLE
summary: VACUUM TABLE コマンドは、テーブルから履歴データファイルを完全に削除してストレージ領域を解放することで、システムパフォーマンスの最適化に役立ちます。これには以下が含まれます。
---

# VACUUM TABLE

VACUUM TABLE コマンドは、テーブルから履歴データファイルを完全に削除してストレージ領域を解放することで、システムパフォーマンスの最適化に役立ちます。これには以下が含まれます。

- テーブルに関連付けられたスナップショット、およびそれに対応する segment と block。

- 孤立ファイル。{{{ .lake }}} における孤立ファイルとは、テーブルに関連付けられなくなった snapshot、segment、block を指します。孤立ファイルは、データのバックアップやリストアの実行中など、さまざまな操作やエラーによって生成されることがあり、貴重なディスク領域を消費し、時間の経過とともにシステムパフォーマンスを低下させる可能性があります。

関連情報: [VACUUM DROP TABLE](/tidb-cloud-lake/sql/vacuum-drop-table.md)

## 構文と例 {#syntax-and-examples}

```sql
VACUUM TABLE <table_name> [ DRY RUN [SUMMARY] ]
```

- `DRY RUN [SUMMARY]`: このパラメータを指定すると、Candidate orphan files は削除されません。代わりに、最大 1,000 件の Candidate file とそのサイズ（バイト単位）の一覧が返され、このオプションを使用しなかった場合に削除される内容を確認できます。オプションの `SUMMARY` パラメータを含めると、削除対象となるファイルの総数と、それらの合計サイズ（バイト単位）が返されます。

### 出力 {#output}

VACUUM TABLE コマンド（`DRY RUN` なし）は、vacuum 対象ファイルの重要な統計情報を要約したテーブルを返します。このテーブルには次のカラムが含まれます。

| カラム | 説明 |
| -------------- | ----------------------------------------- |
| snapshot_files | スナップショットファイル数                  |
| snapshot_size  | スナップショットファイルの合計サイズ（バイト）     |
| segments_files | セグメントファイル数                   |
| segments_size  | セグメントファイルの合計サイズ（バイト）      |
| block_files    | ブロックファイル数                     |
| block_size     | ブロックファイルの合計サイズ（バイト）        |
| index_files    | インデックスファイル数                     |
| index_size     | インデックスファイルの合計サイズ（バイト）        |
| total_files    | すべての種類のファイルの総数        |
| total_size     | すべての種類のファイルの合計サイズ（バイト） |

```sql title='Example:'
// highlight-next-line
VACUUM TABLE c;

┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ snapshot_files │ snapshot_size │ segments_files │ segments_size │ block_files │ block_size │ index_files │ index_size │ total_files │ total_size │
├────────────────┼───────────────┼────────────────┼───────────────┼─────────────┼────────────┼─────────────┼────────────┼─────────────┼────────────┤
│              3 │          1954 │              9 │          4802 │           9 │       1890 │           9 │       3060 │          30 │      11706 │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

VACUUM TABLE コマンドで `DRY RUN` パラメータを指定すると、最大 1,000 件の Candidate file とそのサイズ（バイト単位）の一覧が返されます。`DRY RUN SUMMARY` を指定すると、削除対象となるファイルの総数と、それらの合計サイズが返されます。

```sql title='Example:'
// highlight-next-line
VACUUM TABLE c DRY RUN;

┌──────────────────────────────────────────────────────────────┐
│                       file                       │ file_size │
├──────────────────────────────────────────────────┼───────────┤
│ 1/67/_ss/61aaf678b9af41568b539099b4b09908_v4.mpk │       543 │
│ 1/67/_ss/dd149d21151c459d8c87076f9412c12c_v4.mpk │       516 │
│ 1/67/_ss/7ba0b2e2f63c4d42897a48830027dcf3_v4.mpk │       462 │
│ 1/67/_ss/db55dac72b29452db976cf0af0f8d962_v4.mpk │       588 │
│ 1/67/_ss/d8055967298f478d97cddaa66cf67e11_v4.mpk │       563 │
│ 1/67/_ss/00c4288dac014760808006f821f1ecbe_v4.mpk │       609 │
└──────────────────────────────────────────────────────────────┘
// highlight-next-line
VACUUM TABLE c DRY RUN SUMMARY;

┌──────────────────────────┐
│ total_files │ total_size │
├─────────────┼────────────┤
│           6 │       3281 │
└──────────────────────────┘
```

### データ保持期間の調整 {#adjusting-data-retention-time}

VACUUM TABLE コマンドは、`data_retention_time_in_days` 設定より古いデータファイルを削除します。この保持期間は必要に応じて調整できます。たとえば、2 日に設定するには次のようにします。

```sql
SET GLOBAL data_retention_time_in_days = 2;
```

`data_retention_time_in_days` のデフォルト値は 1 日（24 時間）で、最大値は {{{ .lake }}} のエディションによって異なります。

| エディション | デフォルト保持期間 | 最大保持期間 |
| ---------------------------------------- | ----------------- | ---------------- |
| {{{ .lake }}} Community & Enterprise エディション | 1日 (24時間)  | 90日          |
| {{{ .lake }}} (Personal)                | 1日 (24時間)  | 1日 (24時間) |
| {{{ .lake }}} (Business)                | 1日 (24時間)  | 90日          |

現在の `data_retention_time_in_days` の値を確認するには、次のようにします。

```sql
SHOW SETTINGS LIKE 'data_retention_time_in_days';
```

### VACUUM TABLE と OPTIMIZE TABLE の比較 {#vacuum-table-vs-optimize-table}

{{{ .lake }}} では、テーブルから履歴データファイルを削除するために 2 つのコマンドが提供されています。VACUUM TABLE と、PURGE オプション付きの [OPTIMIZE TABLE](/tidb-cloud-lake/sql/optimize-table.md) です。どちらのコマンドもデータファイルを完全に削除できますが、孤立ファイルの扱い方に違いがあります。OPTIMIZE TABLE は、孤立した snapshot と、それに対応する segment および block を削除できます。ただし、関連付けられた snapshot を持たない孤立した segment や block が存在する可能性があります。このような場合、それらをクリーンアップできるのは VACUUM TABLE だけです。

VACUUM TABLE と OPTIMIZE TABLE はどちらも、どの履歴データファイルを削除するかを決定するための期間を指定できます。ただし、OPTIMIZE TABLE では事前にクエリから snapshot ID または timestamp を取得する必要があります。一方、VACUUM TABLE では、データファイルを保持する時間数を直接指定できます。さらに VACUUM TABLE では、DRY RUN オプションを使用して、コマンドを実行する前に削除対象のデータファイルをプレビューできるため、削除前後の履歴データファイルをより細かく制御できます。これにより、安全に削除を実行でき、意図しないデータ損失を回避するのに役立ちます。

|                                                  | VACUUM TABLE | OPTIMIZE TABLE |
| ------------------------------------------------ | ------------ | -------------- |
| 関連付けられた snapshots（segments と blocks を含む） | Yes          | Yes            |
| 孤立した snapshots（segments と blocks を含む）     | Yes          | Yes            |
| 孤立した segments と blocks のみ                  | Yes          | No             |
| DRY RUN                                          | Yes          | No             |