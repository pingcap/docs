---
title: TiDB Features
summary: TiDB の機能の概要について説明します。
---

# TiDB の機能 {#tidb-features}

このドキュメントでは、最新の LTS バージョン以降の[長期サポート (LTS)](/releases/versioning.md#long-term-support-releases)バージョンおよび[開発マイルストーンリリース (DMR)](/releases/versioning.md#development-milestone-releases)バージョンを含む、さまざまな TiDB バージョンでサポートされている機能をリストします。

[TiDB プレイグラウンド](https://play.tidbcloud.com/?utm_source=docs&#x26;utm_medium=tidb_features)で TiDB の機能を試すことができます。

> **注記：**
>
> PingCAP は、DMR バージョン用のパッチ リリースを提供していません。バグは将来のリリースで修正されます。一般的な目的では、 [最新のLTSバージョン](https://docs.pingcap.com/tidb/stable)使用することをお勧めします。
>
> 以下の表の略語の意味は次のとおりです。
>
> -   Y: 機能は一般提供 (GA) されており、本番環境で使用できます。機能が DMR バージョンで GA であっても、以降の LTS バージョンでは本番環境でその機能を使用することをお勧めします。
> -   N: 機能はサポートされていません。
> -   E: この機能はまだ GA ではありません (実験的)。使用上の制限に注意する必要があります。Experimental機能は、予告なしに変更または削除されることがあります。構文と実装は、一般公開前に変更される可能性があります。問題が発生した場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)報告できます。

## データ型、関数、演算子 {#data-types-functions-and-operators}

| データ型、関数、演算子                                                                  | 8.1 | 7.5 | 7.1 | 6.5 | 6.1 | 5.4 | 5.3 | 5.2 | 5.1 |
| ---------------------------------------------------------------------------- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| [数値型](/data-type-numeric.md)                                                 |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [日付と時刻の種類](/data-type-date-and-time.md)                                      |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [文字列型](/data-type-string.md)                                                 |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [JSON型](/data-type-json.md)                                                  |  Y  |  Y  |  Y  |  Y  |  え  |  え  |  え  |  え  |  え  |
| [制御フロー関数](/functions-and-operators/control-flow-functions.md)                |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [文字列関数](/functions-and-operators/string-functions.md)                        |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [数値関数と演算子](/functions-and-operators/numeric-functions-and-operators.md)      |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [日付と時刻関数](/functions-and-operators/date-and-time-functions.md)               |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [ビット関数と演算子](/functions-and-operators/bit-functions-and-operators.md)         |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [キャスト関数と演算子](/functions-and-operators/cast-functions-and-operators.md)       |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [暗号化と圧縮関数](/functions-and-operators/encryption-and-compression-functions.md) |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [情報関数](/functions-and-operators/information-functions.md)                    |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [JSON関数](/functions-and-operators/json-functions.md)                         |  Y  |  Y  |  Y  |  Y  |  え  |  え  |  え  |  え  |  え  |
| [集計関数](/functions-and-operators/aggregate-group-by-functions.md)             |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [ウィンドウ関数](/functions-and-operators/window-functions.md)                      |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [その他の関数](/functions-and-operators/miscellaneous-functions.md)                |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [オペレーター](/functions-and-operators/operators.md)                              |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [文字セットと照合順序](/character-set-and-collation.md) [^1]                           |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [ユーザーレベルのロック](/functions-and-operators/locking-functions.md)                 |  Y  |  Y  |  Y  |  Y  |  Y  | いいえ | いいえ | いいえ | いいえ |

## インデックスと制約 {#indexing-and-constraints}

| インデックスと制約                                                                                   | 8.1 | 7.5 | 7.1 | 6.5 | 6.1 | 5.4 | 5.3 | 5.2 | 5.1 |
| ------------------------------------------------------------------------------------------- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| [表現インデックス](/sql-statements/sql-statement-create-index.md#expression-index) [^2]             |  Y  |  Y  |  Y  |  Y  |  え  |  え  |  え  |  え  |  え  |
| [列型storage(TiFlash)](/tiflash/tiflash-overview.md)                                          |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [FastScan を使用して OLAP シナリオでのクエリを高速化する](/tiflash/use-fastscan.md)                             |  Y  |  Y  |  Y  |  え  | いいえ | いいえ | いいえ | いいえ | いいえ |
| [RocksDBエンジン](/storage-engine/rocksdb-overview.md)                                          |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [Titanプラグイン](/storage-engine/titan-overview.md)                                             |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [タイタンレベルマージ](/storage-engine/titan-configuration.md#level-merge-experimental)               |  え  |  え  |  え  |  え  |  え  |  え  |  え  |  え  |  え  |
| [バケットを使用してスキャンの同時実行性を向上させる](/tune-region-performance.md#use-bucket-to-increase-concurrency) |  え  |  え  |  え  |  え  |  え  | いいえ | いいえ | いいえ | いいえ |
| [目に見えないインデックス](/sql-statements/sql-statement-create-index.md#invisible-index)               |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [複合`PRIMARY KEY`](/constraints.md)                                                          |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [`CHECK`制約](/constraints.md#check)                                                          |  Y  |  Y  | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ |
| [ユニークなインデックス](/constraints.md)                                                              |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [整数`PRIMARY KEY`のクラスター化インデックス](/clustered-indexes.md)                                       |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [複合キーまたは非整数キーのクラスター化インデックス](/clustered-indexes.md)                                          |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [多値インデックス](/sql-statements/sql-statement-create-index.md#multi-valued-indexes)              |  Y  |  Y  |  Y  | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ |
| [外部キー](/constraints.md#foreign-key)                                                         |  え  |  え  |  え  | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ |
| [TiFlash の遅い実体化](/tiflash/tiflash-late-materialization.md)                                  |  Y  |  Y  |  Y  | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ |

## SQL文 {#sql-statements}

| SQL文[^3]                                                                                          | 8.1 | 7.5 | 7.1 | 6.5 | 6.1 | 5.4 | 5.3 | 5.2 | 5.1 |
| ------------------------------------------------------------------------------------------------- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| `REPLACE` `SELECT` `INSERT` `UPDATE` `DELETE`                                                     |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| `INSERT ON DUPLICATE KEY UPDATE`                                                                  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| `LOAD DATA INFILE`                                                                                |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| `SELECT INTO OUTFILE`                                                                             |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| `INNER JOIN` 、 `LEFT|RIGHT [OUTER] JOIN`                                                          |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| `UNION` , `UNION ALL`                                                                             |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [`EXCEPT`および`INTERSECT`演算子](/functions-and-operators/set-operators.md)                            |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| `GROUP BY` , `ORDER BY`                                                                           |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [ウィンドウ関数](/functions-and-operators/window-functions.md)                                           |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [共通テーブル式 (CTE)](/sql-statements/sql-statement-with.md)                                            |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| `START TRANSACTION` `COMMIT` `ROLLBACK`                                                           |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [`EXPLAIN`](/sql-statements/sql-statement-explain.md)                                             |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)                             |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [ユーザー定義変数](/user-defined-variables.md)                                                            |  え  |  え  |  え  |  え  |  え  |  え  |  え  |  え  |  え  |
| [`BATCH [ON COLUMN] LIMIT INTEGER DELETE`](/sql-statements/sql-statement-batch.md)                |  Y  |  Y  |  Y  |  Y  |  Y  | いいえ | いいえ | いいえ | いいえ |
| [`BATCH [ON COLUMN] LIMIT INTEGER INSERT/UPDATE/REPLACE`](/sql-statements/sql-statement-batch.md) |  Y  |  Y  |  Y  |  Y  | いいえ | いいえ | いいえ | いいえ | いいえ |
| [`ALTER TABLE ... COMPACT`](/sql-statements/sql-statement-alter-table-compact.md)                 |  Y  |  Y  |  Y  |  Y  |  え  | いいえ | いいえ | いいえ | いいえ |
| [テーブルロック](/sql-statements/sql-statement-lock-tables-and-unlock-tables.md)                         |  え  |  え  |  え  |  え  |  え  |  え  |  え  |  え  |  え  |
| [TiFlashクエリ結果のマテリアライゼーション](/tiflash/tiflash-results-materialization.md)                           |  Y  |  Y  |  Y  |  え  | いいえ | いいえ | いいえ | いいえ | いいえ |

## 高度なSQL機能 {#advanced-sql-features}

| 高度なSQL機能                                                                                                     | 8.1 | 7.5 | 7.1 | 6.5 | 6.1 | 5.4 | 5.3 | 5.2 | 5.1 |
| ------------------------------------------------------------------------------------------------------------ | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| [準備されたステートメントのキャッシュ](/sql-prepared-plan-cache.md)                                                            |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  え  |  え  |
| [非プリペアドステートメントキャッシュ](/sql-non-prepared-plan-cache.md)                                                        |  Y  |  Y  |  え  | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ |
| [SQLバインディング](/sql-plan-management.md#sql-binding)                                                            |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [データベース間のバインディング](/sql-plan-management.md#cross-database-binding)                                            |  Y  | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ |
| [過去の実行計画に従ってバインディングを作成する](/sql-plan-management.md#create-a-binding-according-to-a-historical-execution-plan) |  Y  |  Y  |  Y  |  え  | いいえ | いいえ | いいえ | いいえ | いいえ |
| [コプロセッサーキャッシュ](/coprocessor-cache.md)                                                                        |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [ステイル読み取り](/stale-read.md)                                                                                   |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [Followerが読む](/follower-read.md)                                                                             |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [履歴データを読み取る (tidb_snapshot)](/read-historical-data.md)                                                       |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [オプティマイザーのヒント](/optimizer-hints.md)                                                                          |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [MPP実行エンジン](/explain-mpp.md)                                                                                 |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [MPP 実行エンジン - 圧縮交換](/explain-mpp.md#mpp-version-and-exchange-data-compression)                               |  Y  |  Y  |  Y  | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ |
| [TiFlashパイプライン モデル](/tiflash/tiflash-pipeline-model.md)                                                      |  Y  |  Y  | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ |
| [TiFlashレプリカ選択戦略](/system-variables.md#tiflash_replica_read-new-in-v730)                                     |  Y  |  Y  | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ |
| [インデックスの結合](/explain-index-merge.md)                                                                         |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  え  |  え  |  え  |
| [SQL の配置ルール](/placement-rules-in-sql.md)                                                                     |  Y  |  Y  |  Y  |  Y  |  Y  |  え  |  え  | いいえ | いいえ |
| [カスケードプランナー](/system-variables.md#tidb_enable_cascades_planner)                                              |  え  |  え  |  え  |  え  |  え  |  え  |  え  |  え  |  え  |
| [ランタイムフィルター](/runtime-filter.md)                                                                             |  Y  |  Y  | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ |

## データ定義言語 (DDL) {#data-definition-language-ddl}

| データ定義言語 (DDL)                                                                                                                | 8.1 | 7.5 | 7.1 |  6.5  | 6.1 | 5.4 | 5.3 | 5.2 | 5.1 |
| ---------------------------------------------------------------------------------------------------------------------------- | :-: | :-: | :-: | :---: | :-: | :-: | :-: | :-: | :-: |
| `TRUNCATE` `CREATE` `DROP` `ALTER` `RENAME`                                                                                  |  Y  |  Y  |  Y  |   Y   |  Y  |  Y  |  Y  |  Y  |  Y  |
| [生成された列](/generated-columns.md)                                                                                              |  Y  |  Y  |  Y  |   え   |  え  |  え  |  え  |  え  |  え  |
| [ビュー](/views.md)                                                                                                             |  Y  |  Y  |  Y  |   Y   |  Y  |  Y  |  Y  |  Y  |  Y  |
| [シーケンス](/sql-statements/sql-statement-create-sequence.md)                                                                    |  Y  |  Y  |  Y  |   Y   |  Y  |  Y  |  Y  |  Y  |  Y  |
| [自動増加](/auto-increment.md)                                                                                                   |  Y  |  Y  |  Y  | Y[^4] |  Y  |  Y  |  Y  |  Y  |  Y  |
| [自動ランダム](/auto-random.md)                                                                                                    |  Y  |  Y  |  Y  |   Y   |  Y  |  Y  |  Y  |  Y  |  Y  |
| [TTL (存続時間)](/time-to-live.md)                                                                                               |  Y  |  Y  |  Y  |   え   | いいえ | いいえ | いいえ | いいえ | いいえ |
| [DDLアルゴリズムアサーション](/sql-statements/sql-statement-alter-table.md)                                                              |  Y  |  Y  |  Y  |   Y   |  Y  |  Y  |  Y  |  Y  |  Y  |
| マルチスキーマの変更: 列の追加                                                                                                             |  Y  |  Y  |  Y  |   Y   |  え  |  え  |  え  |  え  |  え  |
| [列の種類を変更する](/sql-statements/sql-statement-modify-column.md)                                                                  |  Y  |  Y  |  Y  |   Y   |  Y  |  Y  |  Y  |  Y  |  Y  |
| [一時テーブル](/temporary-tables.md)                                                                                               |  Y  |  Y  |  Y  |   Y   |  Y  |  Y  |  Y  | いいえ | いいえ |
| 同時実行DDLステートメント                                                                                                               |  Y  |  Y  |  Y  |   Y   | いいえ | いいえ | いいえ | いいえ | いいえ |
| [`ADD INDEX`と`CREATE INDEX`の高速化](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)                                |  Y  |  Y  |  Y  |   Y   | いいえ | いいえ | いいえ | いいえ | いいえ |
| [メタデータロック](/metadata-lock.md)                                                                                                |  Y  |  Y  |  Y  |   Y   | いいえ | いいえ | いいえ | いいえ | いいえ |
| [`FLASHBACK CLUSTER`](/sql-statements/sql-statement-flashback-cluster.md)                                                    |  Y  |  Y  |  Y  |   Y   | いいえ | いいえ | いいえ | いいえ | いいえ |
| [一時停止](/sql-statements/sql-statement-admin-pause-ddl.md) / [再開する](/sql-statements/sql-statement-admin-resume-ddl.md)デイリー     |  Y  |  Y  | いいえ |  いいえ  | いいえ | いいえ | いいえ | いいえ | いいえ |
| [TiDB 高速テーブル作成](/accelerated-table-creation.md)                                                                              |  え  | いいえ | いいえ |  いいえ  | いいえ | いいえ | いいえ | いいえ | いいえ |
| [BDR モードで DDL ステートメントをレプリケートするように BDR ロールを構成する](/sql-statements/sql-statement-admin-bdr-role.md#admin-setshowunset-bdr-role) |  え  | いいえ | いいえ |  いいえ  | いいえ | いいえ | いいえ | いいえ | いいえ |

## 取引 {#transactions}

| 取引                                                                                             | 8.1 | 7.5 | 7.1 | 6.5 | 6.1 | 5.4 | 5.3 | 5.2 | 5.1 |
| ---------------------------------------------------------------------------------------------- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| [非同期コミット](/system-variables.md#tidb_enable_async_commit-new-in-v50)                            |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [1個](/system-variables.md#tidb_enable_1pc-new-in-v50)                                          |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [大規模トランザクション（10GB）](/transaction-overview.md#transaction-size-limit)                           |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [悲観的な取引](/pessimistic-transaction.md)                                                          |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [楽観的な取引](/optimistic-transaction.md)                                                           |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [繰り返し読み取り分離（スナップショット分離）](/transaction-isolation-levels.md)                                     |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [コミット読み取り分離](/transaction-isolation-levels.md)                                                 |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [長時間実行中のアイドルトランザクションを自動的に終了する](/system-variables.md#tidb_idle_transaction_timeout-new-in-v760) |  Y  | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ |

## パーティショニング {#partitioning}

| パーティショニング                                                                                                     | 8.1 | 7.5 | 7.1 | 6.5 | 6.1 | 5.4 | 5.3 | 5.2 | 5.1 |
| ------------------------------------------------------------------------------------------------------------- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| [範囲分割](/partitioned-table.md#range-partitioning)                                                              |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [ハッシュパーティショニング](/partitioned-table.md#hash-partitioning)                                                      |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [キーの分割](/partitioned-table.md#key-partitioning)                                                               |  Y  |  Y  |  Y  | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ |
| [List パーティショニング](/partitioned-table.md#list-partitioning)                                                     |  Y  |  Y  |  Y  |  Y  |  Y  |  え  |  え  |  え  |  え  |
| [List COLUMNS パーティショニング](/partitioned-table.md)                                                               |  Y  |  Y  |  Y  |  Y  |  Y  |  え  |  え  |  え  |  え  |
| [リストおよびリスト列パーティションテーブルのデフォルトパーティション](/partitioned-table.md#default-list-partition)                            |  Y  |  Y  | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ |
| [`EXCHANGE PARTITION`](/partitioned-table.md)                                                                 |  Y  |  Y  |  Y  |  Y  |  え  |  え  |  え  |  え  |  え  |
| [`REORGANIZE PARTITION`](/partitioned-table.md#reorganize-partitions)                                         |  Y  |  Y  |  Y  | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ |
| [`COALESCE PARTITION`](/partitioned-table.md#decrease-the-number-of-partitions)                               |  Y  |  Y  |  Y  | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ |
| [動的剪定](/partitioned-table.md#dynamic-pruning-mode)                                                            |  Y  |  Y  |  Y  |  Y  |  Y  |  え  |  え  |  え  |  え  |
| [範囲列パーティション分割](/partitioned-table.md#range-columns-partitioning)                                              |  Y  |  Y  |  Y  |  Y  | いいえ | いいえ | いいえ | いいえ | いいえ |
| [範囲INTERVALパーティション分割](/partitioned-table.md#range-interval-partitioning)                                      |  Y  |  Y  |  Y  |  え  | いいえ | いいえ | いいえ | いいえ | いいえ |
| [パーティションテーブルを非パーティションテーブルに変換する](/partitioned-table.md#convert-a-partitioned-table-to-a-non-partitioned-table) |  Y  |  Y  | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ |
| [既存のテーブルをパーティション分割する](/partitioned-table.md#partition-an-existing-table)                                      |  Y  |  Y  | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ |

## 統計 {#statistics}

| 統計                                                                                    | 8.1       | 7.5       | 7.1       | 6.5       | 6.1       | 5.4       | 5.3       | 5.2 | 5.1 |
| ------------------------------------------------------------------------------------- | --------- | --------- | --------- | --------- | --------- | --------- | --------- | --- | --- |
| [CMSketch](/statistics.md)                                                            | デフォルトでは無効 | デフォルトでは無効 | デフォルトでは無効 | デフォルトでは無効 | デフォルトでは無効 | デフォルトでは無効 | デフォルトでは無効 | Y   | Y   |
| [ヒストグラム](/statistics.md)                                                              | Y         | Y         | Y         | Y         | Y         | Y         | Y         | Y   | Y   |
| [拡張統計](/extended-statistics.md)                                                       | え         | え         | え         | え         | え         | え         | え         | え   | え   |
| 統計フィードバック                                                                             | いいえ       | いいえ       | いいえ       | いいえ       | 非推奨       | 非推奨       | え         | え   | え   |
| [統計を自動的に更新する](/statistics.md#automatic-update)                                        | Y         | Y         | Y         | Y         | Y         | Y         | Y         | Y   | Y   |
| [高速分析](/system-variables.md#tidb_enable_fast_analyze)                                 | 非推奨       | 非推奨       | え         | え         | え         | え         | え         | え   | え   |
| [動的剪定](/partitioned-table.md#dynamic-pruning-mode)                                    | Y         | Y         | Y         | Y         | Y         | え         | え         | え   | え   |
| [`PREDICATE COLUMNS`の統計情報を収集する](/statistics.md#collect-statistics-on-some-columns)    | え         | え         | え         | え         | え         | え         | いいえ       | いいえ | いいえ |
| [統計情報を収集するためのメモリクォータを制御する](/statistics.md#the-memory-quota-for-collecting-statistics) | え         | え         | え         | え         | いいえ       | いいえ       | いいえ       | いいえ | いいえ |
| [約10000行のデータをランダムにサンプリングして統計を素早く構築する](/system-variables.md#tidb_enable_fast_analyze)  | 非推奨       | 非推奨       | え         | え         | え         | え         | え         | え   | え   |
| [ロック統計](/statistics.md#lock-statistics)                                               | Y         | Y         | え         | え         | いいえ       | いいえ       | いいえ       | いいえ | いいえ |
| [軽量な統計初期化](/statistics.md#load-statistics)                                            | Y         | Y         | え         | いいえ       | いいえ       | いいえ       | いいえ       | いいえ | いいえ |
| [統計収集の進行状況を表示する](/sql-statements/sql-statement-show-analyze-status.md)                | Y         | Y         | いいえ       | いいえ       | いいえ       | いいえ       | いいえ       | いいえ | いいえ |

## Security {#security}

| Security                                                                                 | 8.1 | 7.5 | 7.1 | 6.5 | 6.1 | 5.4 | 5.3 | 5.2 | 5.1 |
| ---------------------------------------------------------------------------------------- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| [透過レイヤーセキュリティ (TLS)](/enable-tls-between-clients-and-servers.md)                         |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [保存時の暗号化 (TDE)](/encryption-at-rest.md)                                                  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [ロールベース認証 (RBAC)](/role-based-access-control.md)                                         |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [証明書ベースの認証](/certificate-authentication.md)                                              |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [`caching_sha2_password`認証](/system-variables.md#default_authentication_plugin)          |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  | いいえ |
| [`tidb_sm3_password`認証](/system-variables.md#default_authentication_plugin)              |  Y  |  Y  |  Y  |  Y  | いいえ | いいえ | いいえ | いいえ | いいえ |
| [`tidb_auth_token`認証](/security-compatibility-with-mysql.md#tidb_auth_token)             |  Y  |  Y  |  Y  |  Y  | いいえ | いいえ | いいえ | いいえ | いいえ |
| [`authentication_ldap_sasl`認証](/system-variables.md#default_authentication_plugin)       |  Y  |  Y  | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ |
| [`authentication_ldap_simple`シンプル認証](/system-variables.md#default_authentication_plugin) |  Y  |  Y  |  Y  | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ |
| [パスワード管理](/password-management.md)                                                       |  Y  |  Y  |  Y  |  Y  | いいえ | いいえ | いいえ | いいえ | いいえ |
| [MySQL互換`GRANT`システム](/privilege-management.md)                                           |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [動的権限](/privilege-management.md#dynamic-privileges)                                      |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [Security強化モード](/system-variables.md#tidb_enable_enhanced_security)                      |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [編集されたログファイル](/log-redaction.md)                                                         |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |

## データのインポートとエクスポート {#data-import-and-export}

| データのインポートとエクスポート                                                                                        | 8.1 | 7.5 | 7.1 | 6.5 | 6.1 | 5.4 | 5.3 | 5.2 | 5.1 |
| ------------------------------------------------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [TiDB Lightningを使用した高速インポート](/tidb-lightning/tidb-lightning-overview.md)                                | Y   | Y   | Y   | Y   | Y   | Y   | Y   | Y   | Y   |
| [`IMPORT INTO`ステートメントを使用した高速インポート](/sql-statements/sql-statement-import-into.md)                        | Y   | Y   | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ |
| mydumper 論理ダンパー                                                                                         | 非推奨 | 非推奨 | 非推奨 | 非推奨 | 非推奨 | 非推奨 | 非推奨 | 非推奨 | 非推奨 |
| [Dumpling論理ダンパー](/dumpling-overview.md)                                                                 | Y   | Y   | Y   | Y   | Y   | Y   | Y   | Y   | Y   |
| [トランザクション`LOAD DATA`](/sql-statements/sql-statement-load-data.md) [^5]                                  | Y   | Y   | Y   | Y   | Y   | Y   | Y   | Y   | Y   |
| [データベース移行ツールキット (DM)](/migration-overview.md)                                                           | Y   | Y   | Y   | Y   | Y   | Y   | Y   | Y   | Y   |
| [TiDBBinlog](/tidb-binlog/tidb-binlog-overview.md) [^6]                                                 | Y   | Y   | Y   | Y   | Y   | Y   | Y   | Y   | Y   |
| [変更データキャプチャ (CDC)](/ticdc/ticdc-overview.md)                                                            | Y   | Y   | Y   | Y   | Y   | Y   | Y   | Y   | Y   |
| [TiCDC を介して Amazon S3、GCS、Azure Blob Storage、NFS にデータをストリーミングする](/ticdc/ticdc-sink-to-cloud-storage.md) | Y   | Y   | Y   | え   | いいえ | いいえ | いいえ | いいえ | いいえ |
| [TiCDCは2つのTiDBクラスタ間の双方向レプリケーションをサポートします](/ticdc/ticdc-bidirectional-replication.md)                     | Y   | Y   | Y   | Y   | いいえ | いいえ | いいえ | いいえ | いいえ |
| [TiCDC オープン API v2](/ticdc/ticdc-open-api-v2.md)                                                        | Y   | Y   | Y   | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ |
| [DM](/dm/dm-overview.md) MySQL 8.0への移行をサポート                                                             | Y   | え   | え   | え   | え   | いいえ | いいえ | いいえ | いいえ |

## 管理、可観測性、ツール {#management-observability-and-tools}

| 管理、可観測性、ツール                                                                                                                                                                                                                                                        | 8.1 | 7.5 | 7.1 | 6.5 | 6.1 | 5.4 | 5.3 | 5.2 | 5.1 |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| [TiDBダッシュボードUI](/dashboard/dashboard-intro.md)                                                                                                                                                                                                                     |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [TiDBダッシュボード継続的プロファイリング](/dashboard/continuous-profiling.md)                                                                                                                                                                                                       |  Y  |  Y  |  Y  |  Y  |  Y  |  え  |  え  | いいえ | いいえ |
| [TiDBダッシュボードTop SQL](/dashboard/top-sql.md)                                                                                                                                                                                                                        |  Y  |  Y  |  Y  |  Y  |  Y  |  え  | いいえ | いいえ | いいえ |
| [TiDBダッシュボードSQL診断](/information-schema/information-schema-sql-diagnostics.md)                                                                                                                                                                                      |  Y  |  Y  |  Y  |  Y  |  え  |  え  |  え  |  え  |  え  |
| [TiDBダッシュボードクラスタ診​​断](/dashboard/dashboard-diagnostics-access.md)                                                                                                                                                                                                  |  Y  |  Y  |  Y  |  Y  |  え  |  え  |  え  |  え  |  え  |
| [TiKV-FastTuneダッシュボード](/grafana-tikv-dashboard.md#tikv-fasttune-dashboard)                                                                                                                                                                                         |  え  |  え  |  え  |  え  |  え  |  え  |  え  |  え  |  え  |
| [情報スキーマ](/information-schema/information-schema.md)                                                                                                                                                                                                                |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [メトリクススキーマ](/metrics-schema.md)                                                                                                                                                                                                                                    |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [ステートメント要約表](/statement-summary-tables.md)                                                                                                                                                                                                                         |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [ステートメント要約テーブル - 要約の永続性](/statement-summary-tables.md#persist-statements-summary)                                                                                                                                                                                  |  え  |  え  |  え  | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ |
| [スロークエリログ](/identify-slow-queries.md)                                                                                                                                                                                                                              |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [TiUP の展開](/tiup/tiup-overview.md)                                                                                                                                                                                                                                 |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [Kubernetes オペレーター](https://docs.pingcap.com/tidb-in-kubernetes/)                                                                                                                                                                                                  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [組み込みの物理バックアップ](/br/backup-and-restore-use-cases.md)                                                                                                                                                                                                               |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [グローバルキル](/sql-statements/sql-statement-kill.md)                                                                                                                                                                                                                   |  Y  |  Y  |  Y  |  Y  |  Y  |  え  |  え  |  え  |  え  |
| [ビューをロック](/information-schema/information-schema-data-lock-waits.md)                                                                                                                                                                                               |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  え  |
| [`SHOW CONFIG`](/sql-statements/sql-statement-show-config.md)                                                                                                                                                                                                      |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [`SET CONFIG`](/dynamic-config.md)                                                                                                                                                                                                                                 |  Y  |  Y  |  Y  |  Y  |  Y  |  え  |  え  |  え  |  え  |
| [DM WebUI](/dm/dm-webui-guide.md)                                                                                                                                                                                                                                  |  え  |  え  |  え  |  え  |  え  | いいえ | いいえ | いいえ | いいえ |
| [フォアグラウンドクォータリミッター](/tikv-configuration-file.md#foreground-quota-limiter)                                                                                                                                                                                          |  Y  |  Y  |  Y  |  Y  |  え  | いいえ | いいえ | いいえ | いいえ |
| [バックグラウンドクォータリミッター](/tikv-configuration-file.md#background-quota-limiter)                                                                                                                                                                                          |  え  |  え  |  え  |  え  | いいえ | いいえ | いいえ | いいえ | いいえ |
| [EBS ボリューム スナップショットのバックアップと復元](https://docs.pingcap.com/tidb-in-kubernetes/v1.4/backup-to-aws-s3-by-snapshot)                                                                                                                                                      |  Y  |  Y  |  Y  |  Y  | いいえ | いいえ | いいえ | いいえ | いいえ |
| [ピトル](/br/backup-and-restore-overview.md)                                                                                                                                                                                                                          |  Y  |  Y  |  Y  |  Y  | いいえ | いいえ | いいえ | いいえ | いいえ |
| [グローバルメモリ制御](/configure-memory-usage.md#configure-the-memory-usage-threshold-of-a-tidb-server-instance)                                                                                                                                                            |  Y  |  Y  |  Y  |  Y  | いいえ | いいえ | いいえ | いいえ | いいえ |
| [クラスタ間RawKVレプリケーション](/tikv-configuration-file.md#api-version-new-in-v610)                                                                                                                                                                                          |  え  |  え  |  え  |  え  | いいえ | いいえ | いいえ | いいえ | いいえ |
| [グリーンGC](/system-variables.md#tidb_gc_scan_lock_mode-new-in-v50)                                                                                                                                                                                                   |  え  |  え  |  え  |  え  |  え  |  え  |  え  |  え  |  え  |
| [リソース管理](/tidb-resource-control.md)                                                                                                                                                                                                                                |  Y  |  Y  |  Y  | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ |
| [ランナウェイクエリ管理](/tidb-resource-control.md#manage-queries-that-consume-more-resources-than-expected-runaway-queries)                                                                                                                                                  |  Y  |  え  | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ |
| [バックグラウンドタスク管理](/tidb-resource-control.md#manage-background-tasks)                                                                                                                                                                                                 |  え  |  え  | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ |
| [TiFlash分散ストレージおよびコンピューティングアーキテクチャと S3 サポート](/tiflash/tiflash-disaggregated-and-s3.md)                                                                                                                                                                             |  Y  |  Y  |  え  | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ |
| [分散実行フレームワーク (DXF) タスク用の TiDB ノードの選択](/system-variables.md#tidb_service_scope-new-in-v740)                                                                                                                                                                         |  Y  |  Y  | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ |
| PDFollowerプロキシ（ [`tidb_enable_tso_follower_proxy`](/system-variables.md#tidb_enable_tso_follower_proxy-new-in-v530)によって制御）                                                                                                                                         |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  | いいえ | いいえ |
| [アクティブPDFollower](/tune-region-performance.md#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pds-region-information-query-service) ( [`pd_enable_follower_handle_region`](/system-variables.md#pd_enable_follower_handle_region-new-in-v760)で制御) |  え  | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ |
| [PDマイクロサービス](/pd-microservices.md)                                                                                                                                                                                                                                 |  え  | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ |
| [TiDB 分散実行フレームワーク (DXF)](/tidb-distributed-execution-framework.md)                                                                                                                                                                                                 |  Y  |  Y  |  え  | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ |
| [グローバルソート](/tidb-global-sort.md)                                                                                                                                                                                                                                   |  Y  |  え  | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ |

[^1]: TiDB は latin1 を utf8 のサブセットとして誤って扱います。詳細については[TiDB #18955](https://github.com/pingcap/tidb/issues/18955)参照してください。

[^2]: v6.5.0 以降、 [`tidb_allow_function_for_expression_index`](/system-variables.md#tidb_allow_function_for_expression_index-new-in-v520)システム変数でリストされている関数で作成された式インデックスはテスト済みで、本番環境で使用できます。将来のリリースでは、さらに多くの関数がサポートされる予定です。この変数でリストされていない関数については、対応する式インデックスを本番環境で使用することは推奨されません。詳細については、 [表現インデックス](/sql-statements/sql-statement-create-index.md#expression-index)を参照してください。

[^3]: サポートされている SQL ステートメントの完全なリストについては、 [ステートメント参照](/sql-statements/sql-statement-select.md)参照してください。

[^4]: [バージョン6.4.0](/releases/release-6.4.0.md)から始まり、TiDBは[高性能かつ全体的に単調な`AUTO_INCREMENT`列](/auto-increment.md#mysql-compatibility-mode)サポートします

[^5]: [TiDB v7.0.0](/releases/release-7.0.0.md)以降、新しいパラメータ`FIELDS DEFINED NULL BY`と、S3 および GCS からのデータのインポートのサポートは実験的機能です。 [バージョン7.6.0](/releases/release-7.6.0.md)以降、TiDB は MySQL と同じようにトランザクションで`LOAD DATA`を処理します。トランザクション内の`LOAD DATA`文は、現在のトランザクションを自動的にコミットしたり、新しいトランザクションを開始したりしなくなりました。さらに、トランザクション内の`LOAD DATA`文を明示的にコミットまたはロールバックできます。さらに、 `LOAD DATA`文は TiDB トランザクション モード設定 (楽観的トランザクションまたは悲観的トランザクション) の影響を受けます。

[^6]: TiDB v7.5.0 以降、 [TiDBBinlog](/tidb-binlog/tidb-binlog-overview.md)のデータ レプリケーション機能のテクニカル サポートは提供されなくなりました。データ レプリケーションの代替ソリューションとして[ティCDC](/ticdc/ticdc-overview.md)を使用することを強くお勧めします。TiDB Binlog v7.5.0 では、ポイントインタイム リカバリ (PITR) シナリオが引き続きサポートされていますが、このコンポーネントは将来のバージョンでは完全に廃止される予定です。データ復旧の代替ソリューションとして[ピトル](/br/br-pitr-guide.md)を使用することを推奨します。
