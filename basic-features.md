---
title: TiDB Features
summary: TiDB の機能の概要について説明します。
---

# TiDBの機能 {#tidb-features}

このドキュメントでは、最新の LTS バージョン以降の[長期サポート（LTS）](/releases/versioning.md#long-term-support-releases)バージョンおよび[開発マイルストーンリリース（DMR）](/releases/versioning.md#development-milestone-releases)バージョンを含む、さまざまな TiDB バージョンでサポートされている機能をリストします。

[TiDB プレイグラウンド](https://play.tidbcloud.com/?utm_source=docs&#x26;utm_medium=tidb_features)で TiDB の機能を試すことができます。

> **注記：**
>
> PingCAPはDMRバージョン向けのパッチリリースを提供していません。バグは将来のリリースで修正される予定です。一般的な用途では、 [最新のLTSバージョン](https://docs.pingcap.com/tidb/stable)を使用することをお勧めします。
>
> 以下の表の略語の意味は次のとおりです。
>
> -   Y: 機能は一般提供（GA）されており、本番環境で使用できます。DMRバージョンでGAとなっている機能であっても、後続のLTSバージョンで本番環境で使用することを推奨します。
> -   N: 機能はサポートされていません。
> -   E: この機能はまだ一般公開（実験的）ではありませんので、使用上の制限事項にご注意ください。Experimental機能は予告なく変更または削除される場合があります。構文と実装は一般公開前に変更される可能性があります。問題が発生した場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)報告してください。

## データ型、関数、演算子 {#data-types-functions-and-operators}

| データ型、関数、演算子                                                                  | 8.5 | 8.1 | 7.5 | 7.1 | 6.5 | 6.1 | 5.4 |
| ---------------------------------------------------------------------------- | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| [数値型](/data-type-numeric.md)                                                 |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [日付と時刻の種類](/data-type-date-and-time.md)                                      |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [文字列型](/data-type-string.md)                                                 |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [JSON型](/data-type-json.md)                                                  |  Y  |  Y  |  Y  |  Y  |  Y  |  E  |  E  |
| [ベクトル型](/vector-search/vector-search-data-types.md)                          |  E  |  北  |  北  |  北  |  北  |  北  |  北  |
| [制御フロー関数](/functions-and-operators/control-flow-functions.md)                |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [文字列関数](/functions-and-operators/string-functions.md)                        |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [数値関数と演算子](/functions-and-operators/numeric-functions-and-operators.md)      |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [日付と時刻関数](/functions-and-operators/date-and-time-functions.md)               |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [ビット関数と演算子](/functions-and-operators/bit-functions-and-operators.md)         |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [キャスト関数と演算子](/functions-and-operators/cast-functions-and-operators.md)       |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [暗号化と圧縮関数](/functions-and-operators/encryption-and-compression-functions.md) |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [ベクトル関数と演算子](/vector-search/vector-search-functions-and-operators.md)        |  E  |  北  |  北  |  北  |  北  |  北  |  北  |
| [情報関数](/functions-and-operators/information-functions.md)                    |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [JSON関数](/functions-and-operators/json-functions.md)                         |  Y  |  Y  |  Y  |  Y  |  Y  |  E  |  E  |
| [集計関数](/functions-and-operators/aggregate-group-by-functions.md)             |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [ウィンドウ関数](/functions-and-operators/window-functions.md)                      |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [その他の関数](/functions-and-operators/miscellaneous-functions.md)                |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [オペレーター](/functions-and-operators/operators.md)                              |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [文字セットと照合順序](/character-set-and-collation.md) [^1]                           |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [ユーザーレベルロック](/functions-and-operators/locking-functions.md)                  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  北  |

## インデックスと制約 {#indexing-and-constraints}

| インデックスと制約                                                                                   | 8.5 | 8.1 | 7.5 | 7.1 | 6.5 | 6.1 | 5.4 |
| ------------------------------------------------------------------------------------------- | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| [表現インデックス](/sql-statements/sql-statement-create-index.md#expression-index) [^2]             |  Y  |  Y  |  Y  |  Y  |  Y  |  E  |  E  |
| [列指向storage（TiFlash）](/tiflash/tiflash-overview.md)                                         |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [FastScan を使用して OLAP シナリオでのクエリを高速化します](/tiflash/use-fastscan.md)                            |  Y  |  Y  |  Y  |  Y  |  E  |  北  |  北  |
| [RocksDBエンジン](/storage-engine/rocksdb-overview.md)                                          |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [Titanプラグイン](/storage-engine/titan-overview.md)                                             |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [タイタンレベルマージ](/storage-engine/titan-configuration.md#level-merge-experimental)               |  E  |  E  |  E  |  E  |  E  |  E  |  E  |
| [バケットを使用してスキャンの同時実行性を向上させる](/tune-region-performance.md#use-bucket-to-increase-concurrency) |  E  |  E  |  E  |  E  |  E  |  E  |  北  |
| [目に見えないインデックス](/sql-statements/sql-statement-create-index.md#invisible-index)               |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [複合`PRIMARY KEY`](/constraints.md)                                                          |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [`CHECK`制約](/constraints.md#check)                                                          |  Y  |  Y  |  Y  |  北  |  北  |  北  |  北  |
| [ユニークインデックス](/constraints.md)                                                               |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [整数`PRIMARY KEY`のクラスター化インデックス](/clustered-indexes.md)                                       |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [複合キーまたは非整数キーのクラスター化インデックス](/clustered-indexes.md)                                          |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [多値インデックス](/sql-statements/sql-statement-create-index.md#multi-valued-indexes)              |  Y  |  Y  |  Y  |  Y  |  北  |  北  |  北  |
| [外部キー](/foreign-key.md)                                                                     |  Y  |  E  |  E  |  E  |  北  |  北  |  北  |
| [TiFlashの遅い実体化](/tiflash/tiflash-late-materialization.md)                                   |  Y  |  Y  |  Y  |  Y  |  北  |  北  |  北  |
| [グローバルインデックス](/global-indexes.md)                                                           |  Y  |  北  |  北  |  北  |  北  |  北  |  北  |
| [ベクトルインデックス](/vector-search/vector-search-index.md)                                         |  E  |  北  |  北  |  北  |  北  |  北  |  北  |

## SQL文 {#sql-statements}

| SQL文[^3]                                                                                          | 8.5 | 8.1 | 7.5 | 7.1 | 6.5 | 6.1 | 5.4 |
| ------------------------------------------------------------------------------------------------- | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| `DELETE` `SELECT` `INSERT` `UPDATE` `REPLACE`                                                     |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| `INSERT ON DUPLICATE KEY UPDATE`                                                                  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| `LOAD DATA INFILE`                                                                                |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| `SELECT INTO OUTFILE`                                                                             |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| `INNER JOIN` 、 `LEFT|RIGHT [OUTER] JOIN`                                                          |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| `UNION` `UNION ALL`                                                                               |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [`EXCEPT`演算子と`INTERSECT`演算子](/functions-and-operators/set-operators.md)                           |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| `GROUP BY` `ORDER BY`                                                                             |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [`GROUP BY`修飾子](/functions-and-operators/group-by-modifier.md)                                    |  Y  |  Y  |  Y  |  北  |  北  |  北  |  北  |
| [ウィンドウ関数](/functions-and-operators/window-functions.md)                                           |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [共通テーブル式（CTE）](/sql-statements/sql-statement-with.md)                                             |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| `START TRANSACTION` `COMMIT` `ROLLBACK`                                                           |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [`EXPLAIN`](/sql-statements/sql-statement-explain.md)                                             |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)                             |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [ユーザー定義変数](/user-defined-variables.md)                                                            |  E  |  E  |  E  |  E  |  E  |  E  |  E  |
| [`BATCH [ON COLUMN] LIMIT INTEGER DELETE`](/sql-statements/sql-statement-batch.md)                |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  北  |
| [`BATCH [ON COLUMN] LIMIT INTEGER INSERT/UPDATE/REPLACE`](/sql-statements/sql-statement-batch.md) |  Y  |  Y  |  Y  |  Y  |  Y  |  北  |  北  |
| [`ALTER TABLE ... COMPACT`](/sql-statements/sql-statement-alter-table-compact.md)                 |  Y  |  Y  |  Y  |  Y  |  Y  |  E  |  北  |
| [テーブルロック](/sql-statements/sql-statement-lock-tables-and-unlock-tables.md)                         |  E  |  E  |  E  |  E  |  E  |  E  |  E  |
| [TiFlashクエリ結果のマテリアライゼーション](/tiflash/tiflash-results-materialization.md)                           |  Y  |  Y  |  Y  |  Y  |  E  |  北  |  北  |

## 高度なSQL機能 {#advanced-sql-features}

| 高度なSQL機能                                                                                                     | 8.5 | 8.1 | 7.5 | 7.1 | 6.5 | 6.1 | 5.4 |
| ------------------------------------------------------------------------------------------------------------ | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| [ベクトル検索](/vector-search/vector-search-overview.md)                                                           |  E  |  北  |  北  |  北  |  北  |  北  |  北  |
| [準備されたステートメントキャッシュ](/sql-prepared-plan-cache.md)                                                             |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [非プリペアドステートメントキャッシュ](/sql-non-prepared-plan-cache.md)                                                        |  Y  |  Y  |  Y  |  E  |  北  |  北  |  北  |
| [インスタンスレベルの実行プランキャッシュ](/system-variables.md#tidb_enable_instance_plan_cache-new-in-v840)                     |  E  |  北  |  北  |  北  |  北  |  北  |  北  |
| [SQLバインディング](/sql-plan-management.md#sql-binding)                                                            |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [データベース間のバインディング](/sql-plan-management.md#cross-database-binding)                                            |  Y  |  Y  |  北  |  北  |  北  |  北  |  北  |
| [過去の実行計画に従ってバインディングを作成する](/sql-plan-management.md#create-a-binding-according-to-a-historical-execution-plan) |  Y  |  Y  |  Y  |  Y  |  E  |  北  |  北  |
| [コプロセッサーキャッシュ](/coprocessor-cache.md)                                                                        |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [ステイル読み取り](/stale-read.md)                                                                                   |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [Followerが読む](/follower-read.md)                                                                             |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [履歴データを読み取る (tidb_snapshot)](/read-historical-data.md)                                                       |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [オプティマイザーヒント](/optimizer-hints.md)                                                                           |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [MPP実行エンジン](/explain-mpp.md)                                                                                 |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [MPP実行エンジン - 圧縮交換](/explain-mpp.md#mpp-version-and-exchange-data-compression)                                |  Y  |  Y  |  Y  |  Y  |  北  |  北  |  北  |
| [TiFlashパイプライン モデル](/tiflash/tiflash-pipeline-model.md)                                                      |  Y  |  Y  |  Y  |  北  |  北  |  北  |  北  |
| [TiFlashレプリカ選択戦略](/system-variables.md#tiflash_replica_read-new-in-v730)                                     |  Y  |  Y  |  Y  |  北  |  北  |  北  |  北  |
| [インデックスの結合](/explain-index-merge.md)                                                                         |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [SQLの配置ルール](/placement-rules-in-sql.md)                                                                      |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  E  |
| [カスケードプランナー](/system-variables.md#tidb_enable_cascades_planner)                                              |  E  |  E  |  E  |  E  |  E  |  E  |  E  |
| [ランタイムフィルター](/runtime-filter.md)                                                                             |  Y  |  Y  |  Y  |  北  |  北  |  北  |  北  |

## データ定義言語（DDL） {#data-definition-language-ddl}

| データ定義言語（DDL）                                                                                                                 | 8.5 | 8.1 | 7.5 | 7.1 |  6.5  | 6.1 | 5.4 |
| ---------------------------------------------------------------------------------------------------------------------------- | :-: | :-: | :-: | :-: | :---: | :-: | :-: |
| `RENAME` `CREATE` `DROP` `ALTER` `TRUNCATE`                                                                                  |  Y  |  Y  |  Y  |  Y  |   Y   |  Y  |  Y  |
| [生成された列](/generated-columns.md)                                                                                              |  Y  |  Y  |  Y  |  Y  |   E   |  E  |  E  |
| [ビュー](/views.md)                                                                                                             |  Y  |  Y  |  Y  |  Y  |   Y   |  Y  |  Y  |
| [シーケンス](/sql-statements/sql-statement-create-sequence.md)                                                                    |  Y  |  Y  |  Y  |  Y  |   Y   |  Y  |  Y  |
| [自動増分](/auto-increment.md)                                                                                                   |  Y  |  Y  |  Y  |  Y  | Y[^4] |  Y  |  Y  |
| [自動ランダム](/auto-random.md)                                                                                                    |  Y  |  Y  |  Y  |  Y  |   Y   |  Y  |  Y  |
| [TTL (存続時間)](/time-to-live.md)                                                                                               |  Y  |  Y  |  Y  |  Y  |   E   |  北  |  北  |
| [DDLアルゴリズムアサーション](/sql-statements/sql-statement-alter-table.md)                                                              |  Y  |  Y  |  Y  |  Y  |   Y   |  Y  |  Y  |
| マルチスキーマの変更: 列の追加                                                                                                             |  Y  |  Y  |  Y  |  Y  |   Y   |  E  |  E  |
| [列の種類を変更する](/sql-statements/sql-statement-modify-column.md)                                                                  |  Y  |  Y  |  Y  |  Y  |   Y   |  Y  |  Y  |
| [一時テーブル](/temporary-tables.md)                                                                                               |  Y  |  Y  |  Y  |  Y  |   Y   |  Y  |  Y  |
| 同時実行DDLステートメント                                                                                                               |  Y  |  Y  |  Y  |  Y  |   Y   |  北  |  北  |
| [`ADD INDEX`と`CREATE INDEX`の高速化](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)                                |  Y  |  Y  |  Y  |  Y  |   Y   |  北  |  北  |
| [メタデータロック](/metadata-lock.md)                                                                                                |  Y  |  Y  |  Y  |  Y  |   Y   |  北  |  北  |
| [`FLASHBACK CLUSTER`](/sql-statements/sql-statement-flashback-cluster.md)                                                    |  Y  |  Y  |  Y  |  Y  |   Y   |  北  |  北  |
| [一時停止](/sql-statements/sql-statement-admin-pause-ddl.md) / [再開する](/sql-statements/sql-statement-admin-resume-ddl.md) DDL     |  Y  |  Y  |  Y  |  北  |   北   |  北  |  北  |
| [TiDB 高速テーブル作成](/accelerated-table-creation.md)                                                                              |  Y  |  E  |  北  |  北  |   北   |  北  |  北  |
| [BDR モードで DDL ステートメントをレプリケートするように BDR ロールを構成する](/sql-statements/sql-statement-admin-bdr-role.md#admin-setshowunset-bdr-role) |  Y  |  E  |  北  |  北  |   北   |  北  |  北  |

## 取引 {#transactions}

| 取引                                                                                                  | 8.5 | 8.1 | 7.5 | 7.1 | 6.5 | 6.1 | 5.4 |
| --------------------------------------------------------------------------------------------------- | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| [非同期コミット](/system-variables.md#tidb_enable_async_commit-new-in-v50)                                 |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [1個](/system-variables.md#tidb_enable_1pc-new-in-v50)                                               |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [大規模トランザクション（1 TiB）](/transaction-overview.md#transaction-size-limit)                               |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [悲観的な取引](/pessimistic-transaction.md)                                                               |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [楽観的な取引](/optimistic-transaction.md)                                                                |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [繰り返し読み取り分離（スナップショット分離）](/transaction-isolation-levels.md)                                          |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [コミット読み取り分離](/transaction-isolation-levels.md)                                                      |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [長時間実行されているアイドルトランザクションを自動的に終了する](/system-variables.md#tidb_idle_transaction_timeout-new-in-v760)   |  Y  |  Y  |  北  |  北  |  北  |  北  |  北  |
| [バルクDML実行モード（ `tidb_dml_type = &quot;bulk&quot;` ）](/system-variables.md#tidb_dml_type-new-in-v800) |  E  |  E  |  北  |  北  |  北  |  北  |  北  |

## パーティショニング {#partitioning}

| パーティショニング                                                                                                     | 8.5 | 8.1 | 7.5 | 7.1 | 6.5 | 6.1 | 5.4 |
| ------------------------------------------------------------------------------------------------------------- | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| [範囲分割](/partitioned-table.md#range-partitioning)                                                              |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [ハッシュパーティショニング](/partitioned-table.md#hash-partitioning)                                                      |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [キーパーティショニング](/partitioned-table.md#key-partitioning)                                                         |  Y  |  Y  |  Y  |  Y  |  北  |  北  |  北  |
| [List パーティショニング](/partitioned-table.md#list-partitioning)                                                     |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  E  |
| [List COLUMNS パーティショニング](/partitioned-table.md)                                                               |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  E  |
| [リストおよびリスト列パーティションテーブルのデフォルトパーティション](/partitioned-table.md#default-list-partition)                            |  Y  |  Y  |  Y  |  北  |  北  |  北  |  北  |
| [`EXCHANGE PARTITION`](/partitioned-table.md)                                                                 |  Y  |  Y  |  Y  |  Y  |  Y  |  E  |  E  |
| [`REORGANIZE PARTITION`](/partitioned-table.md#reorganize-partitions)                                         |  Y  |  Y  |  Y  |  Y  |  北  |  北  |  北  |
| [`COALESCE PARTITION`](/partitioned-table.md#decrease-the-number-of-partitions)                               |  Y  |  Y  |  Y  |  Y  |  北  |  北  |  北  |
| [動的剪定](/partitioned-table.md#dynamic-pruning-mode)                                                            |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  E  |
| [範囲列パーティション](/partitioned-table.md#range-columns-partitioning)                                                |  Y  |  Y  |  Y  |  Y  |  Y  |  北  |  北  |
| [範囲INTERVALパーティション分割](/partitioned-table.md#range-interval-partitioning)                                      |  Y  |  Y  |  Y  |  Y  |  E  |  北  |  北  |
| [パーティションテーブルを非パーティションテーブルに変換する](/partitioned-table.md#convert-a-partitioned-table-to-a-non-partitioned-table) |  Y  |  Y  |  Y  |  北  |  北  |  北  |  北  |
| [既存のテーブルをパーティション分割する](/partitioned-table.md#partition-an-existing-table)                                      |  Y  |  Y  |  Y  |  北  |  北  |  北  |  北  |
| [グローバルインデックス](/global-indexes.md)                                                                             |  Y  |  北  |  北  |  北  |  北  |  北  |  北  |

## 統計 {#statistics}

| 統計                                                                                    | 8.5       | 8.1       | 7.5       | 7.1       | 6.5       | 6.1       | 5.4       |
| ------------------------------------------------------------------------------------- | --------- | --------- | --------- | --------- | --------- | --------- | --------- |
| [CMSketch](/statistics.md)                                                            | デフォルトでは無効 | デフォルトでは無効 | デフォルトでは無効 | デフォルトでは無効 | デフォルトでは無効 | デフォルトでは無効 | デフォルトでは無効 |
| [ヒストグラム](/statistics.md)                                                              | Y         | Y         | Y         | Y         | Y         | Y         | Y         |
| [拡張統計](/extended-statistics.md)                                                       | E         | E         | E         | E         | E         | E         | E         |
| 統計フィードバック                                                                             | 北         | 北         | 北         | 北         | 北         | 非推奨       | 非推奨       |
| [統計を自動更新する](/statistics.md#automatic-update)                                          | Y         | Y         | Y         | Y         | Y         | Y         | Y         |
| [動的剪定](/partitioned-table.md#dynamic-pruning-mode)                                    | Y         | Y         | Y         | Y         | Y         | Y         | E         |
| [`PREDICATE COLUMNS`の統計情報を収集する](/statistics.md#collect-statistics-on-some-columns)    | Y         | E         | E         | E         | E         | E         | E         |
| [統計情報を収集するためのメモリクォータを制御する](/statistics.md#the-memory-quota-for-collecting-statistics) | E         | E         | E         | E         | E         | E         | 北         |
| [約10000行のデータをランダムにサンプリングして統計を素早く構築する](/system-variables.md#tidb_enable_fast_analyze)  | 非推奨       | 非推奨       | 非推奨       | E         | E         | E         | E         |
| [ロック統計](/statistics.md#lock-statistics)                                               | Y         | Y         | Y         | E         | E         | 北         | 北         |
| [軽量統計初期化](/statistics.md#load-statistics)                                             | Y         | Y         | Y         | E         | 北         | 北         | 北         |
| [統計収集の進行状況を表示する](/sql-statements/sql-statement-show-analyze-status.md)                | Y         | Y         | Y         | 北         | 北         | 北         | 北         |

## Security {#security}

| Security                                                                             | 8.5 | 8.1 | 7.5 | 7.1 | 6.5 | 6.1 | 5.4 |
| ------------------------------------------------------------------------------------ | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| [透過レイヤーセキュリティ（TLS）](/enable-tls-between-clients-and-servers.md)                      |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [保存時の暗号化（TDE）](/encryption-at-rest.md)                                               |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [ロールベース認証（RBAC）](/role-based-access-control.md)                                      |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [証明書ベースの認証](/certificate-authentication.md)                                          |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [`caching_sha2_password`認証](/system-variables.md#default_authentication_plugin)      |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [`tidb_sm3_password`認証](/system-variables.md#default_authentication_plugin)          |  Y  |  Y  |  Y  |  Y  |  Y  |  北  |  北  |
| [`tidb_auth_token`認証](/security-compatibility-with-mysql.md#tidb_auth_token)         |  Y  |  Y  |  Y  |  Y  |  Y  |  北  |  北  |
| [`authentication_ldap_sasl`認証](/system-variables.md#default_authentication_plugin)   |  Y  |  Y  |  Y  |  北  |  北  |  北  |  北  |
| [`authentication_ldap_simple`認証](/system-variables.md#default_authentication_plugin) |  Y  |  Y  |  Y  |  Y  |  北  |  北  |  北  |
| [パスワード管理](/password-management.md)                                                   |  Y  |  Y  |  Y  |  Y  |  Y  |  北  |  北  |
| [MySQL互換の`GRANT`システム](/privilege-management.md)                                      |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [動的権限](/privilege-management.md#dynamic-privileges)                                  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [Security強化モード](/system-variables.md#tidb_enable_enhanced_security)                  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [編集されたログファイル](/log-redaction.md)                                                     |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |

## データのインポートとエクスポート {#data-import-and-export}

| データのインポートとエクスポート                                                                                        | 8.5     | 8.1 | 7.5 | 7.1 | 6.5 | 6.1 | 5.4 |
| ------------------------------------------------------------------------------------------------------- | ------- | --- | --- | --- | --- | --- | --- |
| [TiDB Lightningを使用した高速インポート](/tidb-lightning/tidb-lightning-overview.md)                                | Y       | Y   | Y   | Y   | Y   | Y   | Y   |
| [`IMPORT INTO`ステートメントを使用した高速インポート](/sql-statements/sql-statement-import-into.md)                        | Y       | Y   | Y   | 北   | 北   | 北   | 北   |
| mydumper 論理ダンパー                                                                                         | 非推奨     | 非推奨 | 非推奨 | 非推奨 | 非推奨 | 非推奨 | 非推奨 |
| [Dumpling論理ダンパー](/dumpling-overview.md)                                                                 | Y       | Y   | Y   | Y   | Y   | Y   | Y   |
| [トランザクション`LOAD DATA`](/sql-statements/sql-statement-load-data.md) [^5]                                  | Y       | Y   | Y   | Y   | Y   | Y   | Y   |
| [データベース移行ツールキット (DM)](/migration-overview.md)                                                           | Y       | Y   | Y   | Y   | Y   | Y   | Y   |
| [TiDBBinlog](https://docs.pingcap.com/tidb/v8.3/tidb-binlog-overview) [^6]                              | 削除されました | Y   | Y   | Y   | Y   | Y   | Y   |
| [変更データキャプチャ（CDC）](/ticdc/ticdc-overview.md)                                                             | Y       | Y   | Y   | Y   | Y   | Y   | Y   |
| [TiCDC を介して Amazon S3、GCS、Azure Blob Storage、NFS にデータをストリーミングする](/ticdc/ticdc-sink-to-cloud-storage.md) | Y       | Y   | Y   | Y   | E   | 北   | 北   |
| [TiCDCは2つのTiDBクラスタ間の双方向レプリケーションをサポートします。](/ticdc/ticdc-bidirectional-replication.md)                    | Y       | Y   | Y   | Y   | Y   | 北   | 北   |
| [TiCDC オープンAPI v2](/ticdc/ticdc-open-api-v2.md)                                                         | Y       | Y   | Y   | Y   | 北   | 北   | 北   |
| [DM](/dm/dm-overview.md) MySQL 8.0への移行をサポート                                                             | Y       | Y   | E   | E   | E   | E   | 北   |

## 管理、可観測性、ツール {#management-observability-and-tools}

| 管理、可観測性、ツール                                                                                                                                                                                                                                                        | 8.5 | 8.1 | 7.5 | 7.1 | 6.5 | 6.1 | 5.4 |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| [TiDBダッシュボードUI](/dashboard/dashboard-intro.md)                                                                                                                                                                                                                     |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [TiDBダッシュボードの継続的なプロファイリング](/dashboard/continuous-profiling.md)                                                                                                                                                                                                     |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  E  |
| [TiDBダッシュボードのTop SQL](/dashboard/top-sql.md)                                                                                                                                                                                                                       |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  E  |
| [TiDBダッシュボードSQL診断](/information-schema/information-schema-sql-diagnostics.md)                                                                                                                                                                                      |  Y  |  Y  |  Y  |  Y  |  Y  |  E  |  E  |
| [TiDBダッシュボードクラスタ診​​断](/dashboard/dashboard-diagnostics-access.md)                                                                                                                                                                                                  |  Y  |  Y  |  Y  |  Y  |  Y  |  E  |  E  |
| [TiKV-FastTuneダッシュボード](/grafana-tikv-dashboard.md#tikv-fasttune-dashboard)                                                                                                                                                                                         |  E  |  E  |  E  |  E  |  E  |  E  |  E  |
| [情報スキーマ](/information-schema/information-schema.md)                                                                                                                                                                                                                |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [メトリクススキーマ](/metrics-schema.md)                                                                                                                                                                                                                                    |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [ステートメント要約表](/statement-summary-tables.md)                                                                                                                                                                                                                         |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [ステートメント要約表 - 要約の永続性](/statement-summary-tables.md#persist-statements-summary)                                                                                                                                                                                     |  E  |  E  |  E  |  E  |  北  |  北  |  北  |
| [スロークエリログ](/identify-slow-queries.md)                                                                                                                                                                                                                              |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [TiUPの展開](/tiup/tiup-overview.md)                                                                                                                                                                                                                                  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [Kubernetesオペレーター](https://docs.pingcap.com/tidb-in-kubernetes/)                                                                                                                                                                                                   |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [組み込みの物理バックアップ](/br/backup-and-restore-use-cases.md)                                                                                                                                                                                                               |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [グローバルキル](/sql-statements/sql-statement-kill.md)                                                                                                                                                                                                                   |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  E  |
| [ビューをロック](/information-schema/information-schema-data-lock-waits.md)                                                                                                                                                                                               |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [`SHOW CONFIG`](/sql-statements/sql-statement-show-config.md)                                                                                                                                                                                                      |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [`SET CONFIG`](/dynamic-config.md)                                                                                                                                                                                                                                 |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  E  |
| [DM WebUI](/dm/dm-webui-guide.md)                                                                                                                                                                                                                                  |  E  |  E  |  E  |  E  |  E  |  E  |  北  |
| [フォアグラウンドクォータリミッター](/tikv-configuration-file.md#foreground-quota-limiter)                                                                                                                                                                                          |  Y  |  Y  |  Y  |  Y  |  Y  |  E  |  北  |
| [バックグラウンドクォータリミッター](/tikv-configuration-file.md#background-quota-limiter)                                                                                                                                                                                          |  E  |  E  |  E  |  E  |  E  |  北  |  北  |
| [EBS ボリューム スナップショットのバックアップと復元](https://docs.pingcap.com/tidb-in-kubernetes/v1.4/backup-to-aws-s3-by-snapshot)                                                                                                                                                      |  Y  |  Y  |  Y  |  Y  |  Y  |  北  |  北  |
| [PITR](/br/backup-and-restore-overview.md)                                                                                                                                                                                                                         |  Y  |  Y  |  Y  |  Y  |  Y  |  北  |  北  |
| [グローバルメモリ制御](/configure-memory-usage.md#configure-the-memory-usage-threshold-of-a-tidb-server-instance)                                                                                                                                                            |  Y  |  Y  |  Y  |  Y  |  Y  |  北  |  北  |
| [クラスタ間RawKVレプリケーション](/tikv-configuration-file.md#api-version-new-in-v610)                                                                                                                                                                                          |  E  |  E  |  E  |  E  |  E  |  北  |  北  |
| [グリーンGC](/system-variables.md#tidb_gc_scan_lock_mode-new-in-v50)                                                                                                                                                                                                   |  E  |  E  |  E  |  E  |  E  |  E  |  E  |
| [リソース管理](/tidb-resource-control-ru-groups.md)                                                                                                                                                                                                                      |  Y  |  Y  |  Y  |  Y  |  北  |  北  |  北  |
| [ランナウェイクエリ管理](/tidb-resource-control-runaway-queries.md)                                                                                                                                                                                                           |  Y  |  Y  |  E  |  北  |  北  |  北  |  北  |
| [バックグラウンドタスク管理](/tidb-resource-control-background-tasks.md)                                                                                                                                                                                                        |  E  |  E  |  E  |  北  |  北  |  北  |  北  |
| [TiFlash分散ストレージおよびコンピューティングアーキテクチャと S3 サポート](/tiflash/tiflash-disaggregated-and-s3.md)                                                                                                                                                                             |  Y  |  Y  |  Y  |  E  |  北  |  北  |  北  |
| [分散実行フレームワーク (DXF) タスク用の TiDB ノードの選択](/system-variables.md#tidb_service_scope-new-in-v740)                                                                                                                                                                         |  Y  |  Y  |  Y  |  北  |  北  |  北  |  北  |
| PDFollowerプロキシ（ [`tidb_enable_tso_follower_proxy`](/system-variables.md#tidb_enable_tso_follower_proxy-new-in-v530)によって制御）                                                                                                                                         |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [アクティブPDFollower](/tune-region-performance.md#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pds-region-information-query-service) （ [`pd_enable_follower_handle_region`](/system-variables.md#pd_enable_follower_handle_region-new-in-v760)で制御） |  Y  |  E  |  北  |  北  |  北  |  北  |  北  |
| [PDマイクロサービス](/pd-microservices.md)                                                                                                                                                                                                                                 |  E  |  E  |  北  |  北  |  北  |  北  |  北  |
| [TiDB 分散実行フレームワーク (DXF)](/tidb-distributed-execution-framework.md)                                                                                                                                                                                                 |  Y  |  Y  |  Y  |  E  |  北  |  北  |  北  |
| [グローバルソート](/tidb-global-sort.md)                                                                                                                                                                                                                                   |  Y  |  Y  |  E  |  北  |  北  |  北  |  北  |
| [TiProxy](/tiproxy/tiproxy-overview.md)                                                                                                                                                                                                                            |  Y  |  Y  |  北  |  北  |  北  |  北  |  北  |
| [スキーマキャッシュ](/schema-cache.md)                                                                                                                                                                                                                                      |  Y  |  北  |  北  |  北  |  北  |  北  |  北  |

[^1]: TiDBはlatin1をutf8のサブセットとして誤って扱います。詳細は[TiDB #18955](https://github.com/pingcap/tidb/issues/18955)参照してください。

[^2]: v6.5.0以降、システム変数[`tidb_allow_function_for_expression_index`](/system-variables.md#tidb_allow_function_for_expression_index-new-in-v520)でリストされている関数で作成された式インデックスはテスト済みであり、本番環境で使用できます。今後のリリースでは、さらに多くの関数がサポートされる予定です。この変数にリストされていない関数については、対応する式インデックスを本番環境で使用することは推奨されません。詳細は[表現インデックス](/sql-statements/sql-statement-create-index.md#expression-index)ご覧ください。

[^3]: サポートされている SQL ステートメントの完全なリストについては、 [ステートメント参照](/sql-statements/sql-statement-select.md)参照してください。

[^4]: [バージョン6.4.0](/releases/release-6.4.0.md)から始まり、TiDBは[高性能でグローバルに単調な`AUTO_INCREMENT`列](/auto-increment.md#mysql-compatibility-mode)サポートします

[^5]: [TiDB v7.0.0](/releases/release-7.0.0.md)以降、新しいパラメータ`FIELDS DEFINED NULL BY`と S3 および GCS からのデータインポートのサポートは実験的機能です。5 以降、TiDB は MySQL と同様にトランザクション内の`LOAD DATA`処理します。トランザクション内の[バージョン7.6.0](/releases/release-7.6.0.md)番目の文は、現在のトランザクションを自動的にコミットしたり、新しいトランザクションを開始したりしなくなりました。また、トランザクション内の`LOAD DATA` `LOAD DATA`の文は明示的にコミットまたはロールバックできます。さらに、 `LOAD DATA`の文は TiDB のトランザクションモード設定（楽観的トランザクションまたは悲観的トランザクション）の影響を受けます。

[^6]: v7.5.0以降、 [TiDBBinlog](https://docs.pingcap.com/tidb/v8.3/tidb-binlog-overview)レプリ​​ケーションは非推奨です。v8.3.0以降、TiDB Binlogは完全に非推奨です。v8.4.0以降、TiDB Binlogは削除されました。増分データレプリケーションの場合は、代わりに[TiCDC](/ticdc/ticdc-overview.md)使用してください。ポイントインタイムリカバリ（PITR）の場合は、 [PITR](/br/br-pitr-guide.md)使用してください。TiDBクラスターをv8.4.0以降のバージョンにアップグレードする前に、必ずTiCDCとPITRに切り替えてください。
