---
title: TiDB Features
summary: TiDBの機能概要について学びましょう。
---

# TiDBの機能 {#tidb-features}

このドキュメントでは、最新 LTS バージョン以降の[長期サポート（LTS）](/releases/versioning.md#long-term-support-releases)バージョンや[開発マイルストーンリリース（DMR）](/releases/versioning.md#development-milestone-releases)バージョンを含む、さまざまな TiDB バージョンでサポートされている機能をリストします。

[TiDB Playground](https://play.tidbcloud.com/?utm_source=docs&#x26;utm_medium=tidb_features)でTiDBの機能を試すことができます。

> **注記：**
>
> PingCAP は、DMR バージョンのパッチ リリースを提供しません。バグは将来のリリースで修正される予定です。一般的な用途には、[最新のLTSバージョン](https://docs.pingcap.com/tidb/stable)使用することをお勧めします。
>
> 下記の表の略語は、それぞれ以下の意味を持ちます。
>
> -   Y：この機能は一般提供（GA）されており、本番環境で使用できます。ただし、DMRバージョンで機能がGAになった場合でも、本番環境ではより新しいLTSバージョンでその機能を使用することをお勧めします。
> -   N: この機能はサポートされていません。
> -   E: この機能はまだ一般提供されていません（実験的）。使用上の制限事項にご注意ください。Experimental機能は予告なく変更または削除される場合があります。構文や実装は一般提供開始前に変更される可能性があります。問題が発生した場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)を報告してください。

## データ型、関数、演算子 {#data-types-functions-and-operators}

| データ型、関数、演算子                                                                    | 8.5 | 8.1 | 7.5 | 7.1 | 6.5 | 6.1 | 5.4 |
| ------------------------------------------------------------------------------ | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| [数値型](/data-type-numeric.md)                                                   |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [日付と時刻の種類](/data-type-date-and-time.md)                                        |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [文字列型](/data-type-string.md)                                                   |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [JSONタイプ](/data-type-json.md)                                                  |  Y  |  Y  |  Y  |  Y  |  Y  |  E  |  E  |
| [ベクタータイプ](/ai/reference/vector-search-data-types.md)                           |  E  |  N  |  N  |  N  |  N  |  N  |  N  |
| [制御フロー関数](/functions-and-operators/control-flow-functions.md)                  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [文字列関数](/functions-and-operators/string-functions.md)                          |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [数値関数と数値演算子](/functions-and-operators/numeric-functions-and-operators.md)      |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [日付と時刻の関数](/functions-and-operators/date-and-time-functions.md)                |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [ビット関数と演算子](/functions-and-operators/bit-functions-and-operators.md)           |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [キャスト関数と演算子](/functions-and-operators/cast-functions-and-operators.md)         |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [暗号化および圧縮関数](/functions-and-operators/encryption-and-compression-functions.md) |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [ベクトル関数と演算子](/ai/reference/vector-search-functions-and-operators.md)           |  E  |  N  |  N  |  N  |  N  |  N  |  N  |
| [情報関数](/functions-and-operators/information-functions.md)                      |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [JSON関数](/functions-and-operators/json-functions.md)                           |  Y  |  Y  |  Y  |  Y  |  Y  |  E  |  E  |
| [集計関数](/functions-and-operators/aggregate-group-by-functions.md)               |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [ウィンドウ関数](/functions-and-operators/window-functions.md)                        |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [その他の関数](/functions-and-operators/miscellaneous-functions.md)                  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [オペレーター](/functions-and-operators/operators.md)                                |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [文字セットと照合](/character-set-and-collation.md)[^1]                                |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [ユーザーレベルのロック](/functions-and-operators/locking-functions.md)                   |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  N  |

## インデックスと制約 {#indexing-and-constraints}

| インデックスと制約                                                                                   | 8.5 | 8.1 | 7.5 | 7.1 | 6.5 | 6.1 | 5.4 |
| ------------------------------------------------------------------------------------------- | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| [発現インデックス](/sql-statements/sql-statement-create-index.md#expression-index)[^2]              |  Y  |  Y  |  Y  |  Y  |  Y  |  E  |  E  |
| [カラム型storage（TiFlash）](/tiflash/tiflash-overview.md)                                        |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [FastScanを使用してOLAPシナリオにおけるクエリを高速化する](/tiflash/use-fastscan.md)                              |  Y  |  Y  |  Y  |  Y  |  E  |  N  |  N  |
| [RocksDBエンジン](/storage-engine/rocksdb-overview.md)                                          |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [Titanプラグイン](/storage-engine/titan-overview.md)                                             |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [タイタンレベルマージ](/storage-engine/titan-configuration.md#level-merge-experimental)               |  E  |  E  |  E  |  E  |  E  |  E  |  E  |
| [バケットを使用してスキャンの同時実行性を向上させる](/tune-region-performance.md#use-bucket-to-increase-concurrency) |  E  |  E  |  E  |  E  |  E  |  E  |  N  |
| [見えないインデックス](/sql-statements/sql-statement-create-index.md#invisible-index)                 |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [複合`PRIMARY KEY`](/constraints.md)                                                          |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [`CHECK`制約](/constraints.md#check)                                                          |  Y  |  Y  |  Y  |  N  |  N  |  N  |  N  |
| [一意のインデックス](/constraints.md)                                                                |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [整数型の`PRIMARY KEY`に対するクラスタ化インデックス](/clustered-indexes.md)                                   |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [複合キーまたは非整数キーに対するクラスタ化インデックス](/clustered-indexes.md)                                        |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [多値インデックス](/sql-statements/sql-statement-create-index.md#multi-valued-indexes)              |  Y  |  Y  |  Y  |  Y  |  N  |  N  |  N  |
| [外部キー](/foreign-key.md)                                                                     |  Y  |  E  |  E  |  E  |  N  |  N  |  N  |
| [TiFlashの遅延実現](/tiflash/tiflash-late-materialization.md)                                    |  Y  |  Y  |  Y  |  Y  |  N  |  N  |  N  |
| [グローバルインデックス](/global-indexes.md)                                                           |  Y  |  N  |  N  |  N  |  N  |  N  |  N  |
| [ベクトルインデックス](/ai/reference/vector-search-index.md)                                          |  E  |  N  |  N  |  N  |  N  |  N  |  N  |

## SQL文 {#sql-statements}

| SQL文[^3]                                                                                          | 8.5 | 8.1 | 7.5 | 7.1 | 6.5 | 6.1 | 5.4 |
| ------------------------------------------------------------------------------------------------- | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| 基本`SELECT` 、 `INSERT` 、 `UPDATE` 、 `DELETE` 、 `REPLACE`                                           |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| `INSERT ON DUPLICATE KEY UPDATE`                                                                  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| `LOAD DATA INFILE`                                                                                |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| `SELECT INTO OUTFILE`                                                                             |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| `INNER JOIN` 、 `LEFT|RIGHT [OUTER] JOIN`                                                          |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| `UNION` 、 `UNION ALL`                                                                             |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [`EXCEPT`演算子と`INTERSECT`演算子](/functions-and-operators/set-operators.md)                           |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| `GROUP BY` 、 `ORDER BY`                                                                           |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [`GROUP BY`修飾子](/functions-and-operators/group-by-modifier.md)                                    |  Y  |  Y  |  Y  |  N  |  N  |  N  |  N  |
| [ウィンドウ関数](/functions-and-operators/window-functions.md)                                           |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [共通テーブル式（CTE）](/sql-statements/sql-statement-with.md)                                             |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| `START TRANSACTION` 、 `COMMIT` 、 `ROLLBACK`                                                       |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [`EXPLAIN`](/sql-statements/sql-statement-explain.md)                                             |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)                             |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [ユーザー定義変数](/user-defined-variables.md)                                                            |  E  |  E  |  E  |  E  |  E  |  E  |  E  |
| [`BATCH [ON COLUMN] LIMIT INTEGER DELETE`](/sql-statements/sql-statement-batch.md)                |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  N  |
| [`BATCH [ON COLUMN] LIMIT INTEGER INSERT/UPDATE/REPLACE`](/sql-statements/sql-statement-batch.md) |  Y  |  Y  |  Y  |  Y  |  Y  |  N  |  N  |
| [`ALTER TABLE ... COMPACT`](/sql-statements/sql-statement-alter-table-compact.md)                 |  Y  |  Y  |  Y  |  Y  |  Y  |  E  |  N  |
| [テーブルロック](/sql-statements/sql-statement-lock-tables-and-unlock-tables.md)                         |  E  |  E  |  E  |  E  |  E  |  E  |  E  |
| [TiFlashクエリ結果の具体化](/tiflash/tiflash-results-materialization.md)                                   |  Y  |  Y  |  Y  |  Y  |  E  |  N  |  N  |

## 高度なSQL機能 {#advanced-sql-features}

| 高度なSQL機能                                                                                                     | 8.5 | 8.1 | 7.5 | 7.1 | 6.5 | 6.1 | 5.4 |
| ------------------------------------------------------------------------------------------------------------ | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| [ベクトル検索](/ai/concepts/vector-search-overview.md)                                                             |  E  |  N  |  N  |  N  |  N  |  N  |  N  |
| [準備済みステートメントキャッシュ](/sql-prepared-plan-cache.md)                                                              |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [プリペアドステートメントキャッシュ](/sql-non-prepared-plan-cache.md)                                                         |  Y  |  Y  |  Y  |  E  |  N  |  N  |  N  |
| [インスタンスレベルの実行プランキャッシュ](/system-variables.md#tidb_enable_instance_plan_cache-new-in-v840)                     |  E  |  N  |  N  |  N  |  N  |  N  |  N  |
| [SQLバインディング](/sql-plan-management.md#sql-binding)                                                            |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [クロスデータベースバインディング](/sql-plan-management.md#cross-database-binding)                                           |  Y  |  Y  |  N  |  N  |  N  |  N  |  N  |
| [過去の実行計画に従ってバインディングを作成する](/sql-plan-management.md#create-a-binding-according-to-a-historical-execution-plan) |  Y  |  Y  |  Y  |  Y  |  E  |  N  |  N  |
| [コプロセッサーキャッシュ](/coprocessor-cache.md)                                                                        |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [ステイル読み取り](/stale-read.md)                                                                                   |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [Followerが読む](/follower-read.md)                                                                             |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [過去のデータ（tidb_snapshot）を読み込む](/read-historical-data.md)                                                       |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [オプティマイザのヒント](/optimizer-hints.md)                                                                           |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [MPP実行エンジン](/explain-mpp.md)                                                                                 |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [MPP実行エンジン - 圧縮交換](/explain-mpp.md#mpp-version-and-exchange-data-compression)                                |  Y  |  Y  |  Y  |  Y  |  N  |  N  |  N  |
| [TiFlashパイプラインモデル](/tiflash/tiflash-pipeline-model.md)                                                       |  Y  |  Y  |  Y  |  N  |  N  |  N  |  N  |
| [TiFlashレプリカ選択戦略](/system-variables.md#tiflash_replica_read-new-in-v730)                                     |  Y  |  Y  |  Y  |  N  |  N  |  N  |  N  |
| [インデックスマージ](/explain-index-merge.md)                                                                         |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [SQLにおける配置ルール](/placement-rules-in-sql.md)                                                                   |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  E  |
| [カスケードプランナー](/system-variables.md#tidb_enable_cascades_planner)                                              |  E  |  E  |  E  |  E  |  E  |  E  |  E  |
| [ランタイムフィルタ](/runtime-filter.md)                                                                              |  Y  |  Y  |  Y  |  N  |  N  |  N  |  N  |

## データ定義言語（DDL） {#data-definition-language-ddl}

| データ定義言語（DDL）                                                                                                             | 8.5 | 8.1 | 7.5 | 7.1 |  6.5  | 6.1 | 5.4 |
| ------------------------------------------------------------------------------------------------------------------------ | :-: | :-: | :-: | :-: | :---: | :-: | :-: |
| 基本`CREATE` 、 `DROP` 、 `ALTER` 、 `RENAME` 、 `TRUNCATE`                                                                    |  Y  |  Y  |  Y  |  Y  |   Y   |  Y  |  Y  |
| [生成された列](/generated-columns.md)                                                                                          |  Y  |  Y  |  Y  |  Y  |   E   |  E  |  E  |
| [閲覧数](/views.md)                                                                                                         |  Y  |  Y  |  Y  |  Y  |   Y   |  Y  |  Y  |
| [シーケンス](/sql-statements/sql-statement-create-sequence.md)                                                                |  Y  |  Y  |  Y  |  Y  |   Y   |  Y  |  Y  |
| [自動インクリメント](/auto-increment.md)                                                                                          |  Y  |  Y  |  Y  |  Y  | Y[^4] |  Y  |  Y  |
| [自動ランダム](/auto-random.md)                                                                                                |  Y  |  Y  |  Y  |  Y  |   Y   |  Y  |  Y  |
| [TTL（Time to Live：生きる時間）](/time-to-live.md)                                                                              |  Y  |  Y  |  Y  |  Y  |   E   |  N  |  N  |
| [DDLアルゴリズムのアサーション](/sql-statements/sql-statement-alter-table.md)                                                         |  Y  |  Y  |  Y  |  Y  |   Y   |  Y  |  Y  |
| マルチスキーマの変更：列の追加                                                                                                          |  Y  |  Y  |  Y  |  Y  |   Y   |  E  |  E  |
| [列の型を変更する](/sql-statements/sql-statement-modify-column.md)                                                               |  Y  |  Y  |  Y  |  Y  |   Y   |  Y  |  Y  |
| [一時テーブル](/temporary-tables.md)                                                                                           |  Y  |  Y  |  Y  |  Y  |   Y   |  Y  |  Y  |
| 同時実行DDLステートメント                                                                                                           |  Y  |  Y  |  Y  |  Y  |   Y   |  N  |  N  |
| [`ADD INDEX`および`CREATE INDEX`の処理速度向上](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)                       |  Y  |  Y  |  Y  |  Y  |   Y   |  N  |  N  |
| [メタデータロック](/metadata-lock.md)                                                                                            |  Y  |  Y  |  Y  |  Y  |   Y   |  N  |  N  |
| [`FLASHBACK CLUSTER`](/sql-statements/sql-statement-flashback-cluster.md)                                                |  Y  |  Y  |  Y  |  Y  |   Y   |  N  |  N  |
| [一時停止](/sql-statements/sql-statement-admin-pause-ddl.md)/ [再開する](/sql-statements/sql-statement-admin-resume-ddl.md)DDL   |  Y  |  Y  |  Y  |  N  |   N   |  N  |  N  |
| [TiDB高速テーブル作成](/accelerated-table-creation.md)                                                                           |  Y  |  E  |  N  |  N  |   N   |  N  |  N  |
| [BDRロールを構成して、BDRモードでDDLステートメントを複製するようにします。](/sql-statements/sql-statement-admin-bdr-role.md#admin-setshowunset-bdr-role) |  Y  |  E  |  N  |  N  |   N   |  N  |  N  |

## 取引 {#transactions}

| 取引                                                                                                   | 8.5 | 8.1 | 7.5 | 7.1 | 6.5 | 6.1 | 5.4 |
| ---------------------------------------------------------------------------------------------------- | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| [非同期コミット](/system-variables.md#tidb_enable_async_commit-new-in-v50)                                  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [1個](/system-variables.md#tidb_enable_1pc-new-in-v50)                                                |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [大規模トランザクション（1 TiB）](/transaction-overview.md#transaction-size-limit)                                |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [悲観的な取引](/pessimistic-transaction.md)                                                                |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [楽観的な取引](/optimistic-transaction.md)                                                                 |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [反復読み取り分離（スナップショット分離）](/transaction-isolation-levels.md)                                             |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [リードコミット隔離](/transaction-isolation-levels.md)                                                        |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [長時間実行されているアイドル状態のトランザクションを自動的に終了する](/system-variables.md#tidb_idle_transaction_timeout-new-in-v760) |  Y  |  Y  |  N  |  N  |  N  |  N  |  N  |
| [一括DML実行モード（ `tidb_dml_type = &quot;bulk&quot;` ）](/system-variables.md#tidb_dml_type-new-in-v800)   |  E  |  E  |  N  |  N  |  N  |  N  |  N  |

## パーティショニング {#partitioning}

| パーティショニング                                                                                                    | 8.5 | 8.1 | 7.5 | 7.1 | 6.5 | 6.1 | 5.4 |
| ------------------------------------------------------------------------------------------------------------ | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| [範囲分割](/partitioned-table.md#range-partitioning)                                                             |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [ハッシュパーティショニング](/partitioned-table.md#hash-partitioning)                                                     |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [キーパーティショニング](/partitioned-table.md#key-partitioning)                                                        |  Y  |  Y  |  Y  |  Y  |  N  |  N  |  N  |
| [List パーティショニング](/partitioned-table.md#list-partitioning)                                                    |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  E  |
| [List COLUMNS パーティショニング](/partitioned-table.md)                                                              |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  E  |
| [リストおよびリスト列パーティションテーブルのデフォルトパーティション](/partitioned-table.md#default-list-partition)                           |  Y  |  Y  |  Y  |  N  |  N  |  N  |  N  |
| [`EXCHANGE PARTITION`](/partitioned-table.md)                                                                |  Y  |  Y  |  Y  |  Y  |  Y  |  E  |  E  |
| [`REORGANIZE PARTITION`](/partitioned-table.md#reorganize-partitions)                                        |  Y  |  Y  |  Y  |  Y  |  N  |  N  |  N  |
| [`COALESCE PARTITION`](/partitioned-table.md#decrease-the-number-of-partitions)                              |  Y  |  Y  |  Y  |  Y  |  N  |  N  |  N  |
| [動的剪定](/partitioned-table.md#dynamic-pruning-mode)                                                           |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  E  |
| [範囲列パーティショニング](/partitioned-table.md#range-columns-partitioning)                                             |  Y  |  Y  |  Y  |  Y  |  Y  |  N  |  N  |
| [範囲 INTERVAL 分割](/partitioned-table.md#range-interval-partitioning)                                          |  Y  |  Y  |  Y  |  Y  |  E  |  N  |  N  |
| [パーティションテーブルをパーティションテーブルに変換する](/partitioned-table.md#convert-a-partitioned-table-to-a-non-partitioned-table) |  Y  |  Y  |  Y  |  N  |  N  |  N  |  N  |
| [既存のテーブルをパーティション分割する](/partitioned-table.md#partition-an-existing-table)                                     |  Y  |  Y  |  Y  |  N  |  N  |  N  |  N  |
| [グローバルインデックス](/global-indexes.md)                                                                            |  Y  |  N  |  N  |  N  |  N  |  N  |  N  |

## 統計 {#statistics}

| 統計                                                                                        | 8.5              | 8.1              | 7.5              | 7.1              | 6.5              | 6.1              | 5.4              |
| ----------------------------------------------------------------------------------------- | ---------------- | ---------------- | ---------------- | ---------------- | ---------------- | ---------------- | ---------------- |
| [CMSketch](/statistics.md)                                                                | デフォルトでは無効になっています | デフォルトでは無効になっています | デフォルトでは無効になっています | デフォルトでは無効になっています | デフォルトでは無効になっています | デフォルトでは無効になっています | デフォルトでは無効になっています |
| [ヒストグラム](/statistics.md)                                                                  | Y                | Y                | Y                | Y                | Y                | Y                | Y                |
| [拡張統計](/extended-statistics.md)                                                           | E                | E                | E                | E                | E                | E                | E                |
| 統計フィードバック                                                                                 | N                | N                | N                | N                | N                | 非推奨              | 非推奨              |
| [統計情報を自動的に更新する](/statistics.md#automatic-update)                                          | Y                | Y                | Y                | Y                | Y                | Y                | Y                |
| [動的剪定](/partitioned-table.md#dynamic-pruning-mode)                                        | Y                | Y                | Y                | Y                | Y                | Y                | E                |
| [`PREDICATE COLUMNS`の統計情報を収集する](/statistics.md#collect-statistics-on-some-columns)        | Y                | E                | E                | E                | E                | E                | E                |
| [統計情報を収集するためのメモリ割り当て量を制御する](/statistics.md#the-memory-quota-for-collecting-statistics)    | E                | E                | E                | E                | E                | E                | N                |
| [約10000行のデータをランダムにサンプリングして、統計情報を素早く構築します。](/system-variables.md#tidb_enable_fast_analyze) | 非推奨              | 非推奨              | 非推奨              | E                | E                | E                | E                |
| [ロック統計](/statistics.md#lock-statistics)                                                   | Y                | Y                | Y                | E                | E                | N                | N                |
| [軽量統計初期化](/statistics.md#load-statistics)                                                 | Y                | Y                | Y                | E                | N                | N                | N                |
| [統計情報の収集状況を表示する](/sql-statements/sql-statement-show-analyze-status.md)                    | Y                | Y                | Y                | N                | N                | N                | N                |

## Security {#security}

| Security                                                                             | 8.5 | 8.1 | 7.5 | 7.1 | 6.5 | 6.1 | 5.4 |
| ------------------------------------------------------------------------------------ | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| [透過型レイヤーセキュリティ（TLS）](/enable-tls-between-clients-and-servers.md)                     |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [保存時の暗号化（TDE）](/encryption-at-rest.md)                                               |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [役割ベース認証（RBAC）](/role-based-access-control.md)                                       |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [証明書ベースの認証](/certificate-authentication.md)                                          |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [`caching_sha2_password`認証](/system-variables.md#default_authentication_plugin)      |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [`tidb_sm3_password`認証](/system-variables.md#default_authentication_plugin)          |  Y  |  Y  |  Y  |  Y  |  Y  |  N  |  N  |
| [`tidb_auth_token`認証](/security-compatibility-with-mysql.md#tidb_auth_token)         |  Y  |  Y  |  Y  |  Y  |  Y  |  N  |  N  |
| [`authentication_ldap_sasl`認証](/system-variables.md#default_authentication_plugin)   |  Y  |  Y  |  Y  |  N  |  N  |  N  |  N  |
| [`authentication_ldap_simple`認証](/system-variables.md#default_authentication_plugin) |  Y  |  Y  |  Y  |  Y  |  N  |  N  |  N  |
| [パスワード管理](/password-management.md)                                                   |  Y  |  Y  |  Y  |  Y  |  Y  |  N  |  N  |
| [MySQL互換の`GRANT`システム](/privilege-management.md)                                      |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [動的権限](/privilege-management.md#dynamic-privileges)                                  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [Security強化モード](/system-variables.md#tidb_enable_enhanced_security)                  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [編集済みログファイル](/log-redaction.md)                                                      |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |

## データのインポートとエクスポート {#data-import-and-export}

| データのインポートとエクスポート                                                                                     | 8.5  | 8.1 | 7.5 | 7.1 | 6.5 | 6.1 | 5.4 |
| ---------------------------------------------------------------------------------------------------- | ---- | --- | --- | --- | --- | --- | --- |
| [TiDB Lightningを使用した高速インポート](/tidb-lightning/tidb-lightning-overview.md)                             | Y    | Y   | Y   | Y   | Y   | Y   | Y   |
| [`IMPORT INTO`ステートメントを使用した高速インポート](/sql-statements/sql-statement-import-into.md)                     | Y    | Y   | Y   | N   | N   | N   | N   |
| mydumper 論理ダンプツール                                                                                    | 非推奨  | 非推奨 | 非推奨 | 非推奨 | 非推奨 | 非推奨 | 非推奨 |
| [Dumpling論理ダンプ](/dumpling-overview.md)                                                               | Y    | Y   | Y   | Y   | Y   | Y   | Y   |
| [トランザクション`LOAD DATA`](/sql-statements/sql-statement-load-data.md) [^5]                               | Y    | Y   | Y   | Y   | Y   | Y   | Y   |
| [データベース移行ツールキット（DM）](/migration-overview.md)                                                         | Y    | Y   | Y   | Y   | Y   | Y   | Y   |
| [TiDBBinlog](https://docs.pingcap.com/tidb/v8.3/tidb-binlog-overview) [^6]                           | 削除済み | Y   | Y   | Y   | Y   | Y   | Y   |
| [変更データキャプチャ（CDC）](/ticdc/ticdc-overview.md)                                                          | Y    | Y   | Y   | Y   | Y   | Y   | Y   |
| [TiCDCを介してAmazon S3、GCS、Azure Blob Storage、NFSにデータをストリーミングする](/ticdc/ticdc-sink-to-cloud-storage.md) | Y    | Y   | Y   | Y   | E   | N   | N   |
| [TiCDCは、2つのTiDBクラスタ間での双方向レプリケーションをサポートしています。](/ticdc/ticdc-bidirectional-replication.md)             | Y    | Y   | Y   | Y   | Y   | N   | N   |
| [TiCDC OpenAPI v2](/ticdc/ticdc-open-api-v2.md)                                                      | Y    | Y   | Y   | Y   | N   | N   | N   |
| [DM](/dm/dm-overview.md) MySQL 8.0の移行をサポートしています                                                      | Y    | Y   | E   | E   | E   | E   | N   |

## 管理、可観測性、およびツール {#management-observability-and-tools}

| 管理、可観測性、およびツール                                                                                                                                                                                                                                                         | 8.5 | 8.1 | 7.5 | 7.1 | 6.5 | 6.1 | 5.4 |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| [TiDBダッシュボードUI](/dashboard/dashboard-intro.md)                                                                                                                                                                                                                         |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [TiDBダッシュボードの継続的プロファイリング](/dashboard/continuous-profiling.md)                                                                                                                                                                                                          |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  E  |
| [TiDBダッシュボードのTop SQL](/dashboard/top-sql.md)                                                                                                                                                                                                                           |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  E  |
| [TiDBダッシュボードのSQL診断](/information-schema/information-schema-sql-diagnostics.md)                                                                                                                                                                                         |  Y  |  Y  |  Y  |  Y  |  Y  |  E  |  E  |
| [TiDBダッシュボードクラスタ診​​断](/dashboard/dashboard-diagnostics-access.md)                                                                                                                                                                                                      |  Y  |  Y  |  Y  |  Y  |  Y  |  E  |  E  |
| [TiKV-FastTuneダッシュボード](/grafana-tikv-dashboard.md#tikv-fasttune-dashboard)                                                                                                                                                                                             |  E  |  E  |  E  |  E  |  E  |  E  |  E  |
| [情報スキーマ](/information-schema/information-schema.md)                                                                                                                                                                                                                    |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [メトリクススキーマ](/metrics-schema.md)                                                                                                                                                                                                                                        |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [明細書の要約表](/statement-summary-tables.md)                                                                                                                                                                                                                                |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [ステートメントの要約テーブル - 要約の永続化](/statement-summary-tables.md#persist-statements-summary)                                                                                                                                                                                     |  E  |  E  |  E  |  E  |  N  |  N  |  N  |
| [スロークエリログ](/identify-slow-queries.md)                                                                                                                                                                                                                                  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [TiUPの展開](/tiup/tiup-overview.md)                                                                                                                                                                                                                                      |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [Kubernetes オペレーター](https://docs.pingcap.com/tidb-in-kubernetes/)                                                                                                                                                                                                      |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [内蔵の物理バックアップ](/br/backup-and-restore-use-cases.md)                                                                                                                                                                                                                     |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [グローバルキル](/sql-statements/sql-statement-kill.md)                                                                                                                                                                                                                       |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  E  |
| [ロックビュー](/information-schema/information-schema-data-lock-waits.md)                                                                                                                                                                                                    |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [`SHOW CONFIG`](/sql-statements/sql-statement-show-config.md)                                                                                                                                                                                                          |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [`SET CONFIG`](/dynamic-config.md)                                                                                                                                                                                                                                     |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  E  |
| [DM WebUI](/dm/dm-webui-guide.md)                                                                                                                                                                                                                                      |  E  |  E  |  E  |  E  |  E  |  E  |  N  |
| [フォアグラウンドクォータリミッター](/tikv-configuration-file.md#foreground-quota-limiter)                                                                                                                                                                                              |  Y  |  Y  |  Y  |  Y  |  Y  |  E  |  N  |
| [バックグラウンドクォータリミッター](/tikv-configuration-file.md#background-quota-limiter)                                                                                                                                                                                              |  E  |  E  |  E  |  E  |  E  |  N  |  N  |
| [EBSボリュームのスナップショットバックアップと復元](https://docs.pingcap.com/tidb-in-kubernetes/v1.4/backup-to-aws-s3-by-snapshot)                                                                                                                                                            |  Y  |  Y  |  Y  |  Y  |  Y  |  N  |  N  |
| [PITR](/br/backup-and-restore-overview.md)                                                                                                                                                                                                                             |  Y  |  Y  |  Y  |  Y  |  Y  |  N  |  N  |
| [グローバルメモリ制御](/configure-memory-usage.md#configure-the-memory-usage-threshold-of-a-tidb-server-instance)                                                                                                                                                                |  Y  |  Y  |  Y  |  Y  |  Y  |  N  |  N  |
| [クラスター間RawKV複製](/tikv-configuration-file.md#api-version-new-in-v610)                                                                                                                                                                                                   |  E  |  E  |  E  |  E  |  E  |  N  |  N  |
| [グリーンGC](/system-variables.md#tidb_gc_scan_lock_mode-new-in-v50)                                                                                                                                                                                                       |  E  |  E  |  E  |  E  |  E  |  E  |  E  |
| [リソース制御](/tidb-resource-control-ru-groups.md)                                                                                                                                                                                                                          |  Y  |  Y  |  Y  |  Y  |  N  |  N  |  N  |
| [暴走クエリの管理](/tidb-resource-control-runaway-queries.md)                                                                                                                                                                                                                  |  Y  |  Y  |  E  |  N  |  N  |  N  |  N  |
| [バックグラウンドタスクの管理](/tidb-resource-control-background-tasks.md)                                                                                                                                                                                                           |  Y  |  E  |  E  |  N  |  N  |  N  |  N  |
| [TiFlashの分散型ストレージおよびコンピューティングアーキテクチャとS3サポート](/tiflash/tiflash-disaggregated-and-s3.md)                                                                                                                                                                                 |  Y  |  Y  |  Y  |  E  |  N  |  N  |  N  |
| [分散実行フレームワーク（DXF）タスク用のTiDBノードの選択](/system-variables.md#tidb_service_scope-new-in-v740)                                                                                                                                                                                 |  Y  |  Y  |  Y  |  N  |  N  |  N  |  N  |
| PDFollowerプロキシ（ [`tidb_enable_tso_follower_proxy`](/system-variables.md#tidb_enable_tso_follower_proxy-new-in-v530)によって制御されます）                                                                                                                                         |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [アクティブなPDFollower](/tune-region-performance.md#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pds-region-information-query-service) ( [`pd_enable_follower_handle_region`](/system-variables.md#pd_enable_follower_handle_region-new-in-v760)によって制御) |  Y  |  E  |  N  |  N  |  N  |  N  |  N  |
| [PDマイクロサービス](/pd-microservices.md)                                                                                                                                                                                                                                     |  E  |  E  |  N  |  N  |  N  |  N  |  N  |
| [TiDB分散実行フレームワーク（DXF）](/tidb-distributed-execution-framework.md)                                                                                                                                                                                                       |  Y  |  Y  |  Y  |  E  |  N  |  N  |  N  |
| [グローバルソート](/tidb-global-sort.md)                                                                                                                                                                                                                                       |  Y  |  Y  |  E  |  N  |  N  |  N  |  N  |
| [TiProxy](/tiproxy/tiproxy-overview.md)                                                                                                                                                                                                                                |  Y  |  Y  |  N  |  N  |  N  |  N  |  N  |
| [スキーマキャッシュ](/schema-cache.md)                                                                                                                                                                                                                                          |  Y  |  N  |  N  |  N  |  N  |  N  |  N  |

[^1]: TiDBはlatin1をutf8のサブセットとして誤って扱っています。詳細は[TiDB #18955](https://github.com/pingcap/tidb/issues/18955)を参照してください。

[^2]: バージョン6.5.0以降、 [`tidb_allow_function_for_expression_index`](/system-variables.md#tidb_allow_function_for_expression_index-new-in-v520)システム変数にリストされている関数に対して作成された式インデックスはテスト済みであり、本番環境で使用できます。今後のリリースでは、さらに多くの関数がサポートされる予定です。この変数にリストされていない関数については、対応する式インデックスは本番環境での使用は推奨されません。詳細については、 [発現指数](/sql-statements/sql-statement-create-index.md#expression-index)参照してください。

[^3]: サポートされている SQL ステートメントの完全なリストについては[ステートメント参照](/sql-statements/sql-statement-select.md)てください。

[^4]: [v6.4.0](/releases/release-6.4.0.md)以降、TiDB は[高性能かつグローバルに単調な`AUTO_INCREMENT`列](/auto-increment.md#mysql-compatibility-mode)をサポートします

[^5]: [TiDB v7.0.0](/releases/release-7.0.0.md)以降、新しいパラメータ`FIELDS DEFINED NULL BY`と S3 および GCS からのデータインポートのサポートは実験的機能です[v7.6.0](/releases/release-7.6.0.md)以降、TiDB は`LOAD DATA`トランザクションで MySQL と同じように処理します。トランザクション内の`LOAD DATA`ステートメントは、現在のトランザクションを自動的にコミットしたり、新しいトランザクションを開始したりしなくなりました。さらに、トランザクション内の`LOAD DATA`ステートメントを明示的にコミットまたはロールバックできます。また、 `LOAD DATA`ステートメントは、TiDB トランザクション モード設定 (楽観的トランザクションまたは悲観的トランザクション) の影響を受けます。

[^6]: バージョン 7.5.0 以降、 [TiDBBinlog](https://docs.pingcap.com/tidb/v8.3/tidb-binlog-overview)レプリケーションは非推奨となりました。バージョン 8.3.0 以降、TiDB Binlogは完全に非推奨となりました。バージョン 8.4.0 以降、TiDB Binlogは削除されました。増分データレプリケーションには、代わりに[TiCDC](/ticdc/ticdc-overview.md)を使用してください。ポイントインタイムリカバリ(PITR) には、 [PITR](/br/br-pitr-guide.md)を使用してください。TiDB クラスタをバージョン 8.4.0 以降にアップグレードする前に、必ず TiCDC と PITR に切り替えてください。
