---
title: TiDB Features
summary: Learn about the feature overview of TiDB.
---

# TiDBの機能 {#tidb-features}

このドキュメントには、最新の LTS バージョン以降の[長期サポート (LTS)](/releases/versioning.md#long-term-support-releases)バージョンと[開発マイルストーン リリース (DMR)](/releases/versioning.md#development-milestone-releases)バージョンを含む、さまざまな TiDB バージョンでサポートされている機能がリストされています。

[TiDB プレイグラウンド](https://play.tidbcloud.com/?utm_source=docs&#x26;utm_medium=tidb_features)で TiDB 機能を試すことができます。

> **注記：**
>
> PingCAP は、DMR バージョンのパッチ リリースを提供しません。バグは将来のリリースで修正される予定です。一般的な目的では、 [最新のLTSバージョン](https://docs.pingcap.com/tidb/stable)を使用することをお勧めします。
>
> 以下の表の略語は次の意味を持ちます。
>
> -   Y: この機能は一般提供 (GA) されており、本番環境で使用できます。機能が DMR バージョンで GA であっても、本番環境では以降の LTS バージョンでその機能を使用することが推奨されることに注意してください。
> -   N: この機能はサポートされていません。
> -   E: この機能はまだ GA ではなく (実験的)、使用制限に注意する必要があります。Experimental機能は予告なく変更または削除される場合があります。構文と実装は、一般公開前に変更される可能性があります。問題が発生した場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)を報告してください。

## データ型、関数、および演算子 {#data-types-functions-and-operators}

| データ型、関数、および演算子                                                               | 7.1 | 6.5 | 6.1 | 5.4 | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 |
| ---------------------------------------------------------------------------- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| [数値型](/data-type-numeric.md)                                                 |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [日付と時刻のタイプ](/data-type-date-and-time.md)                                     |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [文字列型](/data-type-string.md)                                                 |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [JSONタイプ](/data-type-json.md)                                                |  Y  |  Y  |  E  |  E  |  E  |  E  |  E  |  E  |  E  |
| [制御フロー関数](/functions-and-operators/control-flow-functions.md)                |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [文字列関数](/functions-and-operators/string-functions.md)                        |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [数値関数と演算子](/functions-and-operators/numeric-functions-and-operators.md)      |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [日付と時刻の関数](/functions-and-operators/date-and-time-functions.md)              |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [ビット関数と演算子](/functions-and-operators/bit-functions-and-operators.md)         |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [キャスト関数と演算子](/functions-and-operators/cast-functions-and-operators.md)       |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [暗号化・圧縮関数](/functions-and-operators/encryption-and-compression-functions.md) |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [情報関数](/functions-and-operators/information-functions.md)                    |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [JSON関数](/functions-and-operators/json-functions.md)                         |  Y  |  Y  |  E  |  E  |  E  |  E  |  E  |  E  |  E  |
| [集計関数](/functions-and-operators/aggregate-group-by-functions.md)             |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [ウィンドウ関数](/functions-and-operators/window-functions.md)                      |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [その他の関数](/functions-and-operators/miscellaneous-functions.md)                |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [オペレーター](/functions-and-operators/operators.md)                              |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [文字セットと照合順序](/character-set-and-collation.md) [^1]                           |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [ユーザーレベルのロック](/functions-and-operators/locking-functions.md)                 |  Y  |  Y  |  Y  |  N  |  N  |  N  |  N  |  N  |  N  |

## インデックス作成と制約 {#indexing-and-constraints}

| インデックス作成と制約                                                                                 | 7.1 | 6.5 | 6.1 | 5.4 | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 |
| ------------------------------------------------------------------------------------------- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| [式インデックス](/sql-statements/sql-statement-create-index.md#expression-index) [^2]              |  Y  |  Y  |  E  |  E  |  E  |  E  |  E  |  E  |  E  |
| [カラムナ型storage(TiFlash)](/tiflash/tiflash-overview.md)                                       |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [FastScan を使用して OLAP シナリオでのクエリを高速化する](/tiflash/use-fastscan.md)                             |  Y  |  E  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [RocksDB エンジン](/storage-engine/rocksdb-overview.md)                                         |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [タイタンプラグイン](/storage-engine/titan-overview.md)                                              |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [タイタンレベルのマージ](/storage-engine/titan-configuration.md#level-merge-experimental)              |  E  |  E  |  E  |  E  |  E  |  E  |  E  |  E  |  E  |
| [バケットを使用してスキャンの同時実行性を向上させる](/tune-region-performance.md#use-bucket-to-increase-concurrency) |  E  |  E  |  E  |  N  |  N  |  N  |  N  |  N  |  N  |
| [非表示のインデックス](/sql-statements/sql-statement-add-index.md)                                    |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  N  |
| [複合`PRIMARY KEY`](/constraints.md)                                                          |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [固有のインデックス](/constraints.md)                                                                |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [整数`PRIMARY KEY`のクラスター化インデックス](/clustered-indexes.md)                                       |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [複合キーまたは非整数キーのクラスター化インデックス](/clustered-indexes.md)                                          |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  N  |
| [多値インデックス](/sql-statements/sql-statement-create-index.md#multi-valued-indexes)              |  Y  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [外部キー](/constraints.md#foreign-key)                                                         |  E  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [TiFlash後期実体化](/tiflash/tiflash-late-materialization.md)                                    |  Y  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |

## SQL文 {#sql-statements}

| SQL ステートメント[^3]                                                                                   | 7.1 | 6.5 | 6.1 | 5.4 | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 |
| ------------------------------------------------------------------------------------------------- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| 基本`SELECT` 、 `INSERT` 、 `UPDATE` 、 `DELETE` 、 `REPLACE`                                           |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| `INSERT ON DUPLICATE KEY UPDATE`                                                                  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| `LOAD DATA INFILE`                                                                                |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| `SELECT INTO OUTFILE`                                                                             |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| `INNER JOIN` , 左|右 [外側] 結合                                                                        |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| `UNION` `UNION ALL`                                                                               |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [`EXCEPT`演算子と`INTERSECT`演算子](/functions-and-operators/set-operators.md)                           |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  N  |
| `GROUP BY` `ORDER BY`                                                                             |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [ウィンドウ関数](/functions-and-operators/window-functions.md)                                           |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [共通テーブル式 (CTE)](/sql-statements/sql-statement-with.md)                                            |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  N  |  N  |
| `START TRANSACTION` `COMMIT` `ROLLBACK`                                                           |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [`EXPLAIN`](/sql-statements/sql-statement-explain.md)                                             |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)                             |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [ユーザー定義変数](/user-defined-variables.md)                                                            |  E  |  E  |  E  |  E  |  E  |  E  |  E  |  E  |  E  |
| [`BATCH [ON COLUMN] LIMIT INTEGER DELETE`](/sql-statements/sql-statement-batch.md)                |  Y  |  Y  |  Y  |  N  |  N  |  N  |  N  |  N  |  N  |
| [`BATCH [ON COLUMN] LIMIT INTEGER INSERT/UPDATE/REPLACE`](/sql-statements/sql-statement-batch.md) |  Y  |  Y  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [`ALTER TABLE ... COMPACT`](/sql-statements/sql-statement-alter-table-compact.md)                 |  Y  |  Y  |  E  |  N  |  N  |  N  |  N  |  N  |  N  |
| [テーブルロック](/sql-statements/sql-statement-lock-tables-and-unlock-tables.md)                         |  E  |  E  |  E  |  E  |  E  |  E  |  E  |  E  |  E  |
| [TiFlashクエリ結果の具体化](/tiflash/tiflash-results-materialization.md)                                   |  Y  |  E  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |

## 高度な SQL 機能 {#advanced-sql-features}

| 高度な SQL 機能                                                                                                   | 7.1 | 6.5 | 6.1 | 5.4 | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 |
| ------------------------------------------------------------------------------------------------------------ | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| [プリペアドステートメントキャッシュ](/sql-prepared-plan-cache.md)                                                             |  Y  |  Y  |  Y  |  Y  |  Y  |  E  |  E  |  E  |  E  |
| [非プリペアドステートメントキャッシュ](/sql-non-prepared-plan-cache.md)                                                        |  E  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [SQL 計画管理 (SPM)](/sql-plan-management.md)                                                                    |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [過去の実行計画に従ってバインディングを作成する](/sql-plan-management.md#create-a-binding-according-to-a-historical-execution-plan) |  Y  |  E  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [コプロセッサーキャッシュ](/coprocessor-cache.md)                                                                        |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  E  |
| [ステイル読み取り](/stale-read.md)                                                                                   |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  N  |  N  |
| [Followerが読む](/follower-read.md)                                                                             |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [履歴データの読み取り (tidb_snapshot)](/read-historical-data.md)                                                       |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [オプティマイザーのヒント](/optimizer-hints.md)                                                                          |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [MPP実行エンジン](/explain-mpp.md)                                                                                 |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  N  |
| [MPP 実行エンジン - 圧縮交換](/explain-mpp.md#mpp-version-and-exchange-data-compression)                               |  Y  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [インデックスのマージ](/explain-index-merge.md)                                                                        |  Y  |  Y  |  Y  |  Y  |  E  |  E  |  E  |  E  |  E  |
| [SQL の配置ルール](/placement-rules-in-sql.md)                                                                     |  Y  |  Y  |  Y  |  E  |  E  |  N  |  N  |  N  |  N  |
| [カスケード プランナー](/system-variables.md#tidb_enable_cascades_planner)                                             |  E  |  E  |  E  |  E  |  E  |  E  |  E  |  E  |  E  |

## データ定義言語 (DDL) {#data-definition-language-ddl}

| データ定義言語 (DDL)                                                                                 | 7.1 |  6.5  | 6.1 | 5.4 | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 |
| --------------------------------------------------------------------------------------------- | :-: | :---: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| 基本`CREATE` 、 `DROP` 、 `ALTER` 、 `RENAME` 、 `TRUNCATE`                                         |  Y  |   Y   |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [生成された列](/generated-columns.md)                                                               |  Y  |   E   |  E  |  E  |  E  |  E  |  E  |  E  |  E  |
| [ビュー](/views.md)                                                                              |  Y  |   Y   |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [シーケンス](/sql-statements/sql-statement-create-sequence.md)                                     |  Y  |   Y   |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [自動増加](/auto-increment.md)                                                                    |  Y  | Y[^4] |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [自動ランダム](/auto-random.md)                                                                     |  Y  |   Y   |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [TTL (生存時間)](/time-to-live.md)                                                                |  Y  |   E   |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [DDL アルゴリズム アサーション](/sql-statements/sql-statement-alter-table.md)                             |  Y  |   Y   |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| 複数のスキーマの変更: 列の追加                                                                              |  Y  |   Y   |  E  |  E  |  E  |  E  |  E  |  E  |  E  |
| [列の種類を変更する](/sql-statements/sql-statement-modify-column.md)                                   |  Y  |   Y   |  Y  |  Y  |  Y  |  Y  |  Y  |  N  |  N  |
| [一時テーブル](/temporary-tables.md)                                                                |  Y  |   Y   |  Y  |  Y  |  Y  |  N  |  N  |  N  |  N  |
| 同時実行の DDL ステートメント                                                                             |  Y  |   Y   |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [`ADD INDEX`と`CREATE INDEX`の高速化](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) |  Y  |   Y   |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [メタデータロック](/metadata-lock.md)                                                                 |  Y  |   Y   |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-to-timestamp.md)   |  Y  |   Y   |  N  |  N  |  N  |  N  |  N  |  N  |  N  |

## トランザクション {#transactions}

| トランザクション                                                              | 7.1 | 6.5 | 6.1 | 5.4 | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 |
| --------------------------------------------------------------------- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| [非同期コミット](/system-variables.md#tidb_enable_async_commit-new-in-v50)   |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  N  |
| [1個](/system-variables.md#tidb_enable_1pc-new-in-v50)                 |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  N  |
| [大規模トランザクション (10GB)](/transaction-overview.md#transaction-size-limit) |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [悲観的な取引](/pessimistic-transaction.md)                                 |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [楽観的な取引](/optimistic-transaction.md)                                  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [反復読み取り分離 (スナップショット分離)](/transaction-isolation-levels.md)             |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [読み取りコミット分離](/transaction-isolation-levels.md)                        |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |

## パーティショニング {#partitioning}

| パーティショニング                                                                       | 7.1 | 6.5 | 6.1 | 5.4 | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 |
| ------------------------------------------------------------------------------- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| [範囲分割](/partitioned-table.md#range-partitioning)                                |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [ハッシュ分割](/partitioned-table.md#hash-partitioning)                               |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [キーの分割](/partitioned-table.md#key-partitioning)                                 |  Y  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [List パーティショニング](/partitioned-table.md#list-partitioning)                       |  Y  |  Y  |  Y  |  E  |  E  |  E  |  E  |  E  |  N  |
| [List COLUMNS パーティショニング](/partitioned-table.md)                                 |  Y  |  Y  |  Y  |  E  |  E  |  E  |  E  |  E  |  N  |
| [`EXCHANGE PARTITION`](/partitioned-table.md)                                   |  Y  |  Y  |  E  |  E  |  E  |  E  |  E  |  E  |  N  |
| [`REORGANIZE PARTITION`](/partitioned-table.md#reorganize-partitions)           |  Y  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [`COALESCE PARTITION`](/partitioned-table.md#decrease-the-number-of-partitions) |  Y  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [動的枝刈り](/partitioned-table.md#dynamic-pruning-mode)                             |  Y  |  Y  |  Y  |  E  |  E  |  E  |  E  |  N  |  N  |
| [範囲COLUMNSパーティショニング](/partitioned-table.md#range-columns-partitioning)          |  Y  |  Y  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [範囲間隔パーティショニング](/partitioned-table.md#range-interval-partitioning)              |  Y  |  E  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |

## 統計 {#statistics}

| 統計                                                                                       |        7.1       |        6.5       |        6.1       |        6.0       |        5.4       |        5.3       | 5.2 | 5.1 | 5.0 |
| ---------------------------------------------------------------------------------------- | :--------------: | :--------------: | :--------------: | :--------------: | :--------------: | :--------------: | :-: | :-: | :-: |
| [CMSスケッチ](/statistics.md)                                                                | デフォルトでは無効になっています | デフォルトでは無効になっています | デフォルトでは無効になっています | デフォルトでは無効になっています | デフォルトでは無効になっています | デフォルトでは無効になっています |  Y  |  Y  |  Y  |
| [ヒストグラム](/statistics.md)                                                                 |         Y        |         Y        |         Y        |         Y        |         Y        |         Y        |  Y  |  Y  |  Y  |
| [拡張統計](/extended-statistics.md)                                                          |         E        |         E        |         E        |         E        |         E        |         E        |  E  |  E  |  E  |
| 統計フィードバック                                                                                |         N        |         N        |      廃止されました     |      廃止されました     |      廃止されました     |         E        |  E  |  E  |  E  |
| [統計を自動的に更新する](/statistics.md#automatic-update)                                           |         Y        |         Y        |         Y        |         Y        |         Y        |         Y        |  Y  |  Y  |  Y  |
| [高速分析](/system-variables.md#tidb_enable_fast_analyze)                                    |         E        |         E        |         E        |         E        |         E        |         E        |  E  |  E  |  E  |
| [動的枝刈り](/partitioned-table.md#dynamic-pruning-mode)                                      |         Y        |         Y        |         Y        |         E        |         E        |         E        |  E  |  E  |  N  |
| [`PREDICATE COLUMNS`の統計を収集する](/statistics.md#collect-statistics-on-some-columns)         |         E        |         E        |         E        |         E        |         E        |         N        |  N  |  N  |  N  |
| [統計を収集するためのメモリ割り当てを制御する](/statistics.md#the-memory-quota-for-collecting-statistics)      |         E        |         E        |         E        |         N        |         N        |         N        |  N  |  N  |  N  |
| [約 10,000 行のデータをランダムにサンプリングして統計を迅速に構築します](/system-variables.md#tidb_enable_fast_analyze) |         E        |         E        |         E        |         E        |         E        |         E        |  E  |  E  |  E  |
| [ロック統計](/statistics.md#lock-statistics)                                                  |         E        |         E        |         N        |         N        |         N        |         N        |  N  |  N  |  N  |
| [軽量統計の初期化](/statistics.md#load-statistics)                                               |         E        |         N        |         N        |         N        |         N        |         N        |  N  |  N  |  N  |

## Security {#security}

| Security                                                                             | 7.1 | 6.5 | 6.1 | 5.4 | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 |
| ------------------------------------------------------------------------------------ | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| [透過レイヤーセキュリティ (TLS)](/enable-tls-between-clients-and-servers.md)                     |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [保存時の暗号化 (TDE)](/encryption-at-rest.md)                                              |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [ロールベース認証 (RBAC)](/role-based-access-control.md)                                     |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [証明書ベースの認証](/certificate-authentication.md)                                          |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [`caching_sha2_password`認証](/system-variables.md#default_authentication_plugin)      |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  N  |  N  |  N  |
| [`tidb_sm3_password`認証](/system-variables.md#default_authentication_plugin)          |  Y  |  Y  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [`tidb_auth_token`認証](/system-variables.md#default_authentication_plugin)            |  Y  |  Y  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [`authentication_ldap_sasl`認証](/system-variables.md#default_authentication_plugin)   |  Y  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [`authentication_ldap_simple`認証](/system-variables.md#default_authentication_plugin) |  Y  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [パスワード管理](/password-management.md)                                                   |  Y  |  Y  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [MySQL互換の`GRANT`システム](/privilege-management.md)                                      |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [動的な権限](/privilege-management.md#dynamic-privileges)                                 |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  N  |  N  |
| [Security強化モード](/system-variables.md#tidb_enable_enhanced_security)                  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  N  |  N  |
| [編集されたログ ファイル](/log-redaction.md)                                                    |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  N  |

## データのインポートとエクスポート {#data-import-and-export}

| データのインポートとエクスポート                                                                                        |   7.1   |   6.5   |   6.1   |   5.4   |   5.3   |   5.2   |   5.1   |   5.0   |   4.0   |
| ------------------------------------------------------------------------------------------------------- | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: |
| [高速インポーター (TiDB Lightning)](/tidb-lightning/tidb-lightning-overview.md)                                 |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |
| mydumper 論理ダンパー                                                                                         | 廃止されました | 廃止されました | 廃止されました | 廃止されました | 廃止されました | 廃止されました | 廃止されました | 廃止されました | 廃止されました |
| [Dumpling論理ダンパー](/dumpling-overview.md)                                                                 |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |
| [トランザクション`LOAD DATA`](/sql-statements/sql-statement-load-data.md)                                       |  Y [^5] |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |   [^6]  |
| [データベース移行ツールキット (DM)](/migration-overview.md)                                                           |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |
| [TiDBBinlog](/tidb-binlog/tidb-binlog-overview.md)                                                      |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |
| [変更データキャプチャ (CDC)](/ticdc/ticdc-overview.md)                                                            |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |
| [TiCDC を介して Amazon S3、GCS、Azure Blob Storage、NFS にデータをストリーミングする](/ticdc/ticdc-sink-to-cloud-storage.md) |    Y    |    E    |    N    |    N    |    N    |    N    |    N    |    N    |    N    |
| [TiCDC は 2 つの TiDB クラスター間の双方向レプリケーションをサポートします](/ticdc/ticdc-bidirectional-replication.md)               |    Y    |    Y    |    N    |    N    |    N    |    N    |    N    |    N    |    N    |
| [TiCDC OpenAPI v2](/ticdc/ticdc-open-api-v2.md)                                                         |    Y    |    N    |    N    |    N    |    N    |    N    |    N    |    N    |    N    |

## 管理、可観測性、およびツール {#management-observability-and-tools}

| 管理、可観測性、およびツール                                                                                                | 7.1 | 6.5 | 6.1 | 5.4 | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 |
| ------------------------------------------------------------------------------------------------------------- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| [TiDB ダッシュボード UI](/dashboard/dashboard-intro.md)                                                              |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [TiDB ダッシュボードの継続的プロファイリング](/dashboard/continuous-profiling.md)                                                |  Y  |  Y  |  Y  |  E  |  E  |  N  |  N  |  N  |  N  |
| [TiDB ダッシュボードのTop SQL](/dashboard/top-sql.md)                                                                 |  Y  |  Y  |  Y  |  E  |  N  |  N  |  N  |  N  |  N  |
| [TiDB ダッシュボード SQL 診断](/information-schema/information-schema-sql-diagnostics.md)                              |  Y  |  Y  |  E  |  E  |  E  |  E  |  E  |  E  |  E  |
| [TiDB ダッシュボードのクラスタ診断](/dashboard/dashboard-diagnostics-access.md)                                             |  Y  |  Y  |  E  |  E  |  E  |  E  |  E  |  E  |  E  |
| [TiKV-FastTune ダッシュボード](/grafana-tikv-dashboard.md#tikv-fasttune-dashboard)                                   |  E  |  E  |  E  |  E  |  E  |  E  |  E  |  E  |  E  |
| [情報スキーマ](/information-schema/information-schema.md)                                                           |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [メトリクススキーマ](/metrics-schema.md)                                                                               |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [ステートメントの概要テーブル](/statement-summary-tables.md)                                                                |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [ステートメント概要テーブル - 概要の永続性](/statement-summary-tables.md#persist-statements-summary)                             |  E  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [スロークエリログ](/identify-slow-queries.md)                                                                         |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [TiUP導入](/tiup/tiup-overview.md)                                                                              |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [Kubernetes オペレーター](https://docs.pingcap.com/tidb-in-kubernetes/)                                             |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [内蔵の物理バックアップ](/br/backup-and-restore-use-cases.md)                                                            |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [グローバルキル](/sql-statements/sql-statement-kill.md)                                                              |  Y  |  Y  |  Y  |  E  |  E  |  E  |  E  |  E  |  E  |
| [ビューをロックする](/information-schema/information-schema-data-lock-waits.md)                                        |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  E  |  E  |  E  |
| [`SHOW CONFIG`](/sql-statements/sql-statement-show-config.md)                                                 |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [`SET CONFIG`](/dynamic-config.md)                                                                            |  Y  |  Y  |  Y  |  E  |  E  |  E  |  E  |  E  |  E  |
| [DM WebUI](/dm/dm-webui-guide.md)                                                                             |  E  |  E  |  E  |  N  |  N  |  N  |  N  |  N  |  N  |
| [フォアグラウンド クォータ リミッター](/tikv-configuration-file.md#foreground-quota-limiter)                                   |  Y  |  Y  |  E  |  N  |  N  |  N  |  N  |  N  |  N  |
| [バックグラウンド クォータ リミッター](/tikv-configuration-file.md#background-quota-limiter)                                   |  E  |  E  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [EBS ボリュームのスナップショットのバックアップと復元](https://docs.pingcap.com/tidb-in-kubernetes/v1.4/backup-to-aws-s3-by-snapshot) |  Y  |  Y  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [PITR](/br/backup-and-restore-overview.md)                                                                    |  Y  |  Y  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [グローバルメモリ制御](/configure-memory-usage.md#configure-the-memory-usage-threshold-of-a-tidb-server-instance)       |  Y  |  Y  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [クラスター間の RawKV レプリケーション](/tikv-configuration-file.md#api-version-new-in-v610)                                 |  E  |  E  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [グリーンGC](/system-variables.md#tidb_gc_scan_lock_mode-new-in-v50)                                              |  E  |  E  |  E  |  E  |  E  |  E  |  E  |  E  |  N  |
| [リソース制御](/tidb-resource-control.md)                                                                           |  Y  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [TiFlash の分散型ストレージとコンピューティングアーキテクチャおよび S3 サポート](/tiflash/tiflash-disaggregated-and-s3.md)                     |  E  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |

[^1]: TiDB は、latin1 を utf8 のサブセットとして誤って扱います。詳細については[TiDB #18955](https://github.com/pingcap/tidb/issues/18955)参照してください。

[^2]: v6.5.0 以降、 [`tidb_allow_function_for_expression_index`](/system-variables.md#tidb_allow_function_for_expression_index-new-in-v520)システム変数によってリストされた関数に対して作成された式インデックスはテストされており、本番環境で使用できるようになりました。将来のリリースでは、さらに多くの関数がサポートされる予定です。この変数にリストされていない関数については、対応する式インデックスを本番環境で使用することは推奨されません。詳細は[式インデックス](/sql-statements/sql-statement-create-index.md#expression-index)参照してください。

[^3]: サポートされている SQL ステートメントの完全なリストについては、 [ステートメントのリファレンス](/sql-statements/sql-statement-select.md)を参照してください。

[^4]: TiDB は[v6.4.0](/releases/release-6.4.0.md)から始まり[高性能でグローバルに単調な`AUTO_INCREMENT`カラム](/auto-increment.md#mysql-compatibility-mode)をサポートします

[^5]: [TiDB v7.0.0](/releases/release-7.0.0.md)の場合、新しいパラメータ`FIELDS DEFINED NULL BY`と S3 および GCS からのデータのインポートのサポートは実験的機能です。

[^6]: TiDB v4.0 の場合、 `LOAD DATA`トランザクションはアトミック性を保証しません。
