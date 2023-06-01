---
title: TiDB Features
summary: Learn about the feature overview of TiDB.
---

# TiDBの機能 {#tidb-features}

このドキュメントには、最新の LTS バージョン以降の[<a href="/releases/versioning.md#long-term-support-releases">長期サポート (LTS)</a>](/releases/versioning.md#long-term-support-releases)バージョンと[<a href="/releases/versioning.md#development-milestone-releases">開発マイルストーン リリース (DMR)</a>](/releases/versioning.md#development-milestone-releases)バージョンを含む、さまざまな TiDB バージョンでサポートされている機能がリストされています。

> **ノート：**
>
> PingCAP は、DMR バージョンのパッチ リリースを提供しません。バグは将来のリリースで修正される予定です。一般的な目的では、 [<a href="https://docs.pingcap.com/tidb/stable">最新のLTSバージョン</a>](https://docs.pingcap.com/tidb/stable)を使用することをお勧めします。
>
> 以下の表の略語は次の意味を持ちます。
>
> -   Y: この機能は一般提供 (GA) されており、本番環境で使用できます。機能が DMR バージョンで GA であっても、本番環境では以降の LTS バージョンでその機能を使用することが推奨されることに注意してください。
> -   N: この機能はサポートされていません。
> -   E: この機能はまだ GA ではなく (実験的)、使用制限に注意する必要があります。Experimental機能は予告なく変更または削除される場合があります。構文と実装は、一般公開前に変更される可能性があります。問題が発生した場合は、GitHub で[<a href="https://github.com/pingcap/tidb/issues">問題</a>](https://github.com/pingcap/tidb/issues)を報告してください。

## データ型、関数、および演算子 {#data-types-functions-and-operators}

| データ型、関数、および演算子                                                                                                                                              | 7.1 | 6.5 | 6.1 | 5.4 | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| [<a href="/data-type-numeric.md">数値型</a>](/data-type-numeric.md)                                                                                            |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/data-type-date-and-time.md">日付と時刻のタイプ</a>](/data-type-date-and-time.md)                                                                          |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/data-type-string.md">文字列型</a>](/data-type-string.md)                                                                                             |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/data-type-json.md">JSONタイプ</a>](/data-type-json.md)                                                                                              |  Y  |  Y  |  E  |  E  |  E  |  E  |  E  |  E  |  E  |
| [<a href="/functions-and-operators/control-flow-functions.md">制御フロー関数</a>](/functions-and-operators/control-flow-functions.md)                              |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/functions-and-operators/string-functions.md">文字列関数</a>](/functions-and-operators/string-functions.md)                                            |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/functions-and-operators/numeric-functions-and-operators.md">数値関数と演算子</a>](/functions-and-operators/numeric-functions-and-operators.md)           |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/functions-and-operators/date-and-time-functions.md">日付と時刻の関数</a>](/functions-and-operators/date-and-time-functions.md)                           |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/functions-and-operators/bit-functions-and-operators.md">ビット関数と演算子</a>](/functions-and-operators/bit-functions-and-operators.md)                  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/functions-and-operators/cast-functions-and-operators.md">キャスト関数と演算子</a>](/functions-and-operators/cast-functions-and-operators.md)               |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/functions-and-operators/encryption-and-compression-functions.md">暗号化・圧縮関数</a>](/functions-and-operators/encryption-and-compression-functions.md) |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/functions-and-operators/information-functions.md">情報関数</a>](/functions-and-operators/information-functions.md)                                   |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/functions-and-operators/json-functions.md">JSON関数</a>](/functions-and-operators/json-functions.md)                                               |  Y  |  Y  |  E  |  E  |  E  |  E  |  E  |  E  |  E  |
| [<a href="/functions-and-operators/aggregate-group-by-functions.md">集計関数</a>](/functions-and-operators/aggregate-group-by-functions.md)                     |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/functions-and-operators/window-functions.md">ウィンドウ関数</a>](/functions-and-operators/window-functions.md)                                          |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/functions-and-operators/miscellaneous-functions.md">その他の関数</a>](/functions-and-operators/miscellaneous-functions.md)                             |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/functions-and-operators/operators.md">オペレーター</a>](/functions-and-operators/operators.md)                                                         |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/character-set-and-collation.md">文字セットと照合順序</a>](/character-set-and-collation.md) [^1]                                                            |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/functions-and-operators/locking-functions.md">ユーザーレベルのロック</a>](/functions-and-operators/locking-functions.md)                                    |  Y  |  Y  |  Y  |  N  |  N  |  N  |  N  |  N  |  N  |

## インデックス作成と制約 {#indexing-and-constraints}

| インデックス作成と制約                                                                                                                                                              | 7.1 | 6.5 | 6.1 | 5.4 | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| [<a href="/sql-statements/sql-statement-create-index.md#expression-index">式インデックス</a>](/sql-statements/sql-statement-create-index.md#expression-index) [^2]              |  Y  |  Y  |  E  |  E  |  E  |  E  |  E  |  E  |  E  |
| [<a href="/tiflash/tiflash-overview.md">カラムナ型storage(TiFlash)</a>](/tiflash/tiflash-overview.md)                                                                         |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/tiflash/use-fastscan.md">FastScan を使用して OLAP シナリオでのクエリを高速化する</a>](/tiflash/use-fastscan.md)                                                                   |  Y  |  E  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [<a href="/storage-engine/rocksdb-overview.md">RocksDB エンジン</a>](/storage-engine/rocksdb-overview.md)                                                                    |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/storage-engine/titan-overview.md">タイタンプラグイン</a>](/storage-engine/titan-overview.md)                                                                           |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/storage-engine/titan-configuration.md#level-merge-experimental">タイタンレベルのマージ</a>](/storage-engine/titan-configuration.md#level-merge-experimental)             |  E  |  E  |  E  |  E  |  E  |  E  |  E  |  E  |  E  |
| [<a href="/tune-region-performance.md#use-bucket-to-increase-concurrency">バケットを使用してスキャンの同時実行性を向上させる</a>](/tune-region-performance.md#use-bucket-to-increase-concurrency) |  E  |  E  |  E  |  N  |  N  |  N  |  N  |  N  |  N  |
| [<a href="/sql-statements/sql-statement-add-index.md">非表示のインデックス</a>](/sql-statements/sql-statement-add-index.md)                                                        |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  N  |
| [<a href="/constraints.md">複合`PRIMARY KEY`</a>](/constraints.md)                                                                                                         |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/constraints.md">固有のインデックス</a>](/constraints.md)                                                                                                               |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/constraints.md">整数`PRIMARY KEY`のクラスター化インデックス</a>](/constraints.md)                                                                                            |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/constraints.md">複合キーまたは非整数キーのクラスター化インデックス</a>](/constraints.md)                                                                                               |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  N  |
| [<a href="/sql-statements/sql-statement-create-index.md#multi-valued-index">多値インデックス</a>](/sql-statements/sql-statement-create-index.md#multi-valued-index)              |  Y  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [<a href="/constraints.md#foreign-key">外部キー</a>](/constraints.md#foreign-key)                                                                                            |  Y  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [<a href="/tiflash/tiflash-late-materialization.md">TiFlash後期実体化</a>](/tiflash/tiflash-late-materialization.md)                                                          |  Y  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |

## SQL文 {#sql-statements}

| SQL ステートメント[^3]                                                                                                                                        | 7.1 | 6.5 | 6.1 | 5.4 | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 |
| ------------------------------------------------------------------------------------------------------------------------------------------------------ | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| 基本`SELECT` 、 `INSERT` 、 `UPDATE` 、 `DELETE` 、 `REPLACE`                                                                                                |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| `INSERT ON DUPLICATE KEY UPDATE`                                                                                                                       |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| `LOAD DATA INFILE`                                                                                                                                     |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| `SELECT INTO OUTFILE`                                                                                                                                  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| `INNER JOIN` , 左|右 [外側] 結合                                                                                                                             |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| `UNION` `UNION ALL`                                                                                                                                    |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/functions-and-operators/set-operators.md">`EXCEPT`演算子と`INTERSECT`演算子</a>](/functions-and-operators/set-operators.md)                        |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  N  |
| `GROUP BY` `ORDER BY`                                                                                                                                  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/functions-and-operators/window-functions.md">ウィンドウ関数</a>](/functions-and-operators/window-functions.md)                                     |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/sql-statements/sql-statement-with.md">共通テーブル式 (CTE)</a>](/sql-statements/sql-statement-with.md)                                             |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  N  |  N  |
| `START TRANSACTION` `COMMIT` `ROLLBACK`                                                                                                                |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/sql-statements/sql-statement-explain.md">`EXPLAIN`</a>](/sql-statements/sql-statement-explain.md)                                           |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/sql-statements/sql-statement-explain-analyze.md">`EXPLAIN ANALYZE`</a>](/sql-statements/sql-statement-explain-analyze.md)                   |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/user-defined-variables.md">ユーザー定義変数</a>](/user-defined-variables.md)                                                                        |  E  |  E  |  E  |  E  |  E  |  E  |  E  |  E  |  E  |
| [<a href="/sql-statements/sql-statement-batch.md">`BATCH [ON COLUMN] LIMIT INTEGER DELETE`</a>](/sql-statements/sql-statement-batch.md)                |  Y  |  Y  |  Y  |  N  |  N  |  N  |  N  |  N  |  N  |
| [<a href="/sql-statements/sql-statement-batch.md">`BATCH [ON COLUMN] LIMIT INTEGER INSERT/UPDATE/REPLACE`</a>](/sql-statements/sql-statement-batch.md) |  Y  |  Y  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [<a href="/sql-statements/sql-statement-alter-table-compact.md">`ALTER TABLE ... COMPACT`</a>](/sql-statements/sql-statement-alter-table-compact.md)   |  Y  |  Y  |  E  |  N  |  N  |  N  |  N  |  N  |  N  |
| [<a href="/sql-statements/sql-statement-lock-tables-and-unlock-tables.md">テーブルロック</a>](/sql-statements/sql-statement-lock-tables-and-unlock-tables.md) |  E  |  E  |  E  |  E  |  E  |  E  |  E  |  E  |  E  |
| [<a href="/tiflash/tiflash-results-materialization.md">TiFlashクエリ結果の具体化</a>](/tiflash/tiflash-results-materialization.md)                              |  Y  |  E  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |

## 高度な SQL 機能 {#advanced-sql-features}

| 高度な SQL 機能                                                                                                                                                                                                   | 7.1 | 6.5 | 6.1 | 5.4 | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| [<a href="/sql-prepared-plan-cache.md">プリペアドステートメントキャッシュ</a>](/sql-prepared-plan-cache.md)                                                                                                                   |  Y  |  Y  |  Y  |  Y  |  Y  |  E  |  E  |  E  |  E  |
| [<a href="/sql-non-prepared-plan-cache.md">非プリペアドステートメントキャッシュ</a>](/sql-non-prepared-plan-cache.md)                                                                                                          |  E  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [<a href="/sql-plan-management.md">SQL 計画管理 (SPM)</a>](/sql-plan-management.md)                                                                                                                              |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/sql-plan-management.md#create-a-binding-according-to-a-historical-execution-plan">過去の実行計画に従ってバインディングを作成する</a>](/sql-plan-management.md#create-a-binding-according-to-a-historical-execution-plan) |  Y  |  E  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [<a href="/coprocessor-cache.md">コプロセッサーキャッシュ</a>](/coprocessor-cache.md)                                                                                                                                    |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  E  |
| [<a href="/stale-read.md">ステイル読み取り</a>](/stale-read.md)                                                                                                                                                      |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  N  |  N  |
| [<a href="/follower-read.md">Followerが読む</a>](/follower-read.md)                                                                                                                                             |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/read-historical-data.md">履歴データの読み取り (tidb_snapshot)</a>](/read-historical-data.md)                                                                                                                |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/optimizer-hints.md">オプティマイザーのヒント</a>](/optimizer-hints.md)                                                                                                                                        |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/explain-mpp.md">MPP実行エンジン</a>](/explain-mpp.md)                                                                                                                                                   |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  N  |
| [<a href="/explain-mpp.md#mpp-version-and-exchange-data-compression">MPP 実行エンジン - 圧縮交換</a>](/explain-mpp.md#mpp-version-and-exchange-data-compression)                                                       |  Y  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [<a href="/explain-index-merge.md">インデックスのマージ</a>](/explain-index-merge.md)                                                                                                                                  |  Y  |  Y  |  Y  |  Y  |  E  |  E  |  E  |  E  |  E  |
| [<a href="/placement-rules-in-sql.md">SQL の配置ルール</a>](/placement-rules-in-sql.md)                                                                                                                            |  Y  |  Y  |  Y  |  E  |  E  |  N  |  N  |  N  |  N  |
| [<a href="/system-variables.md#tidb_enable_cascades_planner">カスケード プランナー</a>](/system-variables.md#tidb_enable_cascades_planner)                                                                             |  E  |  E  |  E  |  E  |  E  |  E  |  E  |  E  |  E  |

## データ定義言語 (DDL) {#data-definition-language-ddl}

| データ定義言語 (DDL)                                                                                                                                                           | 7.1 |  6.5  | 6.1 | 5.4 | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-: | :---: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| 基本`CREATE` 、 `DROP` 、 `ALTER` 、 `RENAME` 、 `TRUNCATE`                                                                                                                   |  Y  |   Y   |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/generated-columns.md">生成された列</a>](/generated-columns.md)                                                                                                     |  Y  |   E   |  E  |  E  |  E  |  E  |  E  |  E  |  E  |
| [<a href="/views.md">ビュー</a>](/views.md)                                                                                                                                |  Y  |   Y   |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/sql-statements/sql-statement-create-sequence.md">シーケンス</a>](/sql-statements/sql-statement-create-sequence.md)                                                |  Y  |   Y   |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/auto-increment.md">自動増加</a>](/auto-increment.md)                                                                                                             |  Y  | Y[^4] |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/auto-random.md">自動ランダム</a>](/auto-random.md)                                                                                                                 |  Y  |   Y   |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/time-to-live.md">TTL (生存時間)</a>](/time-to-live.md)                                                                                                           |  Y  |   E   |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [<a href="/sql-statements/sql-statement-alter-table.md">DDL アルゴリズム アサーション</a>](/sql-statements/sql-statement-alter-table.md)                                            |  Y  |   Y   |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| 複数のスキーマの変更: 列の追加                                                                                                                                                        |  Y  |   Y   |  E  |  E  |  E  |  E  |  E  |  E  |  E  |
| [<a href="/sql-statements/sql-statement-modify-column.md">列の種類を変更する</a>](/sql-statements/sql-statement-modify-column.md)                                                |  Y  |   Y   |  Y  |  Y  |  Y  |  Y  |  Y  |  N  |  N  |
| [<a href="/temporary-tables.md">一時テーブル</a>](/temporary-tables.md)                                                                                                       |  Y  |   Y   |  Y  |  Y  |  Y  |  N  |  N  |  N  |  N  |
| 同時実行の DDL ステートメント                                                                                                                                                       |  Y  |   Y   |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [<a href="/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630">`ADD INDEX`と`CREATE INDEX`の高速化</a>](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) |  Y  |   Y   |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [<a href="/metadata-lock.md">メタデータロック</a>](/metadata-lock.md)                                                                                                           |  Y  |   Y   |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [<a href="/sql-statements/sql-statement-flashback-to-timestamp.md">`FLASHBACK CLUSTER TO TIMESTAMP`</a>](/sql-statements/sql-statement-flashback-to-timestamp.md)       |  Y  |   Y   |  N  |  N  |  N  |  N  |  N  |  N  |  N  |

## 取引 {#transactions}

| 取引                                                                                                                                         | 7.1 | 6.5 | 6.1 | 5.4 | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 |
| ------------------------------------------------------------------------------------------------------------------------------------------ | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| [<a href="/system-variables.md#tidb_enable_async_commit-new-in-v50">非同期コミット</a>](/system-variables.md#tidb_enable_async_commit-new-in-v50) |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  N  |
| [<a href="/system-variables.md#tidb_enable_1pc-new-in-v50">1個</a>](/system-variables.md#tidb_enable_1pc-new-in-v50)                        |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  N  |
| [<a href="/transaction-overview.md#transaction-size-limit">大規模トランザクション (10GB)</a>](/transaction-overview.md#transaction-size-limit)        |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/pessimistic-transaction.md">悲観的な取引</a>](/pessimistic-transaction.md)                                                            |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/optimistic-transaction.md">楽観的な取引</a>](/optimistic-transaction.md)                                                              |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/transaction-isolation-levels.md">反復読み取り分離 (スナップショット分離)</a>](/transaction-isolation-levels.md)                                   |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/transaction-isolation-levels.md">読み取りコミット分離</a>](/transaction-isolation-levels.md)                                              |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |

## パーティショニング {#partitioning}

| パーティショニング                                                                                                                                             | 7.1 | 6.5 | 6.1 | 5.4 | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 |
| ----------------------------------------------------------------------------------------------------------------------------------------------------- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| [<a href="/partitioned-table.md#range-partitioning">範囲分割</a>](/partitioned-table.md#range-partitioning)                                               |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/partitioned-table.md#hash-partitioning">ハッシュ分割</a>](/partitioned-table.md#hash-partitioning)                                               |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/partitioned-table.md#key-partitioning">キーの分割</a>](/partitioned-table.md#key-partitioning)                                                  |  Y  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [<a href="/partitioned-table.md#list-partitioning">List パーティショニング</a>](/partitioned-table.md#list-partitioning)                                       |  Y  |  Y  |  Y  |  E  |  E  |  E  |  E  |  E  |  N  |
| [<a href="/partitioned-table.md">List COLUMNS パーティショニング</a>](/partitioned-table.md)                                                                   |  Y  |  Y  |  Y  |  E  |  E  |  E  |  E  |  E  |  N  |
| [<a href="/partitioned-table.md">`EXCHANGE PARTITION`</a>](/partitioned-table.md)                                                                     |  Y  |  Y  |  E  |  E  |  E  |  E  |  E  |  E  |  N  |
| [<a href="/partitioned-table.md#reorganize-partitions">`REORGANIZE PARTITION`</a>](/partitioned-table.md#reorganize-partitions)                       |  Y  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [<a href="/partitioned-table.md#decrease-the-number-of-partitions">`COALESCE PARTITION`</a>](/partitioned-table.md#decrease-the-number-of-partitions) |  Y  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [<a href="/partitioned-table.md#dynamic-pruning-mode">動的枝刈り</a>](/partitioned-table.md#dynamic-pruning-mode)                                          |  Y  |  Y  |  Y  |  E  |  E  |  E  |  E  |  N  |  N  |
| [<a href="/partitioned-table.md#range-columns-partitioning">範囲COLUMNSパーティショニング</a>](/partitioned-table.md#range-columns-partitioning)                 |  Y  |  Y  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [<a href="/partitioned-table.md#range-interval-partitioning">範囲間隔パーティショニング</a>](/partitioned-table.md#range-interval-partitioning)                    |  Y  |  E  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |

## 統計 {#statistics}

| 統計                                                                                                                                                          |        7.1       |        6.5       |        6.1       |        6.0       |        5.4       |        5.3       | 5.2 | 5.1 | 5.0 |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------: | :--------------: | :--------------: | :--------------: | :--------------: | :--------------: | :-: | :-: | :-: |
| [<a href="/statistics.md">CMSスケッチ</a>](/statistics.md)                                                                                                      | デフォルトでは無効になっています | デフォルトでは無効になっています | デフォルトでは無効になっています | デフォルトでは無効になっています | デフォルトでは無効になっています | デフォルトでは無効になっています |  Y  |  Y  |  Y  |
| [<a href="/statistics.md">ヒストグラム</a>](/statistics.md)                                                                                                       |         Y        |         Y        |         Y        |         Y        |         Y        |         Y        |  Y  |  Y  |  Y  |
| [<a href="/extended-statistics.md">拡張統計</a>](/extended-statistics.md)                                                                                       |         E        |         E        |         E        |         E        |         E        |         E        |  E  |  E  |  E  |
| 統計フィードバック                                                                                                                                                   |         N        |         N        |      廃止されました     |      廃止されました     |      廃止されました     |         E        |  E  |  E  |  E  |
| [<a href="/statistics.md#automatic-update">統計を自動的に更新する</a>](/statistics.md#automatic-update)                                                                |         Y        |         Y        |         Y        |         Y        |         Y        |         Y        |  Y  |  Y  |  Y  |
| [<a href="/system-variables.md#tidb_enable_fast_analyze">高速分析</a>](/system-variables.md#tidb_enable_fast_analyze)                                           |         E        |         E        |         E        |         E        |         E        |         E        |  E  |  E  |  E  |
| [<a href="/partitioned-table.md#dynamic-pruning-mode">動的枝刈り</a>](/partitioned-table.md#dynamic-pruning-mode)                                                |         Y        |         Y        |         Y        |         E        |         E        |         E        |  E  |  E  |  N  |
| [<a href="/statistics.md#collect-statistics-on-some-columns">`PREDICATE COLUMNS`の統計を収集する</a>](/statistics.md#collect-statistics-on-some-columns)            |         E        |         E        |         E        |         E        |         E        |         N        |  N  |  N  |  N  |
| [<a href="/statistics.md#the-memory-quota-for-collecting-statistics">統計を収集するためのメモリ割り当てを制御する</a>](/statistics.md#the-memory-quota-for-collecting-statistics) |         E        |         E        |         E        |         N        |         N        |         N        |  N  |  N  |  N  |
| [<a href="/system-variables.md#tidb_enable_fast_analyze">約 10,000 行のデータをランダムにサンプリングして統計を迅速に構築します</a>](/system-variables.md#tidb_enable_fast_analyze)        |         E        |         E        |         E        |         E        |         E        |         E        |  E  |  E  |  E  |
| [<a href="/statistics.md#lock-statistics">ロック統計</a>](/statistics.md#lock-statistics)                                                                        |         E        |         E        |         N        |         N        |         N        |         N        |  N  |  N  |  N  |
| [<a href="/statistics.md#load-statistics">軽量統計の初期化</a>](/statistics.md#load-statistics)                                                                     |         E        |         N        |         N        |         N        |         N        |         N        |  N  |  N  |  N  |

## Security {#security}

| Security                                                                                                                                              | 7.1 | 6.5 | 6.1 | 5.4 | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 |
| ----------------------------------------------------------------------------------------------------------------------------------------------------- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| [<a href="/enable-tls-between-clients-and-servers.md">透過レイヤーセキュリティ (TLS)</a>](/enable-tls-between-clients-and-servers.md)                             |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/encryption-at-rest.md">保存時の暗号化 (TDE)</a>](/encryption-at-rest.md)                                                                          |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/role-based-access-control.md">ロールベース認証 (RBAC)</a>](/role-based-access-control.md)                                                          |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/certificate-authentication.md">証明書ベースの認証</a>](/certificate-authentication.md)                                                              |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/system-variables.md#default_authentication_plugin">`caching_sha2_password`認証</a>](/system-variables.md#default_authentication_plugin)      |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  N  |  N  |  N  |
| [<a href="/system-variables.md#default_authentication_plugin">`tidb_sm3_password`認証</a>](/system-variables.md#default_authentication_plugin)          |  Y  |  Y  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [<a href="/system-variables.md#default_authentication_plugin">`tidb_auth_token`認証</a>](/system-variables.md#default_authentication_plugin)            |  Y  |  Y  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [<a href="/system-variables.md#default_authentication_plugin">`authentication_ldap_sasl`認証</a>](/system-variables.md#default_authentication_plugin)   |  Y  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [<a href="/system-variables.md#default_authentication_plugin">`authentication_ldap_simple`認証</a>](/system-variables.md#default_authentication_plugin) |  Y  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [<a href="/password-management.md">パスワード管理</a>](/password-management.md)                                                                              |  Y  |  Y  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [<a href="/privilege-management.md">MySQL互換の`GRANT`システム</a>](/privilege-management.md)                                                                |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/privilege-management.md#dynamic-privileges">動的な権限</a>](/privilege-management.md#dynamic-privileges)                                        |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  N  |  N  |
| [<a href="/system-variables.md#tidb_enable_enhanced_security">Security強化モード</a>](/system-variables.md#tidb_enable_enhanced_security)                  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  N  |  N  |
| [<a href="/log-redaction.md">編集されたログ ファイル</a>](/log-redaction.md)                                                                                     |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  N  |

## データのインポートとエクスポート {#data-import-and-export}

| データのインポートとエクスポート                                                                                                                                            |   7.1   |   6.5   |   6.1   |   5.4   |   5.3   |   5.2   |   5.1   |   5.0   |   4.0   |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------- | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: |
| [<a href="/tidb-lightning/tidb-lightning-overview.md">高速インポーター (TiDB Lightning)</a>](/tidb-lightning/tidb-lightning-overview.md)                            |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |
| mydumper 論理ダンパー                                                                                                                                             | 廃止されました | 廃止されました | 廃止されました | 廃止されました | 廃止されました | 廃止されました | 廃止されました | 廃止されました | 廃止されました |
| [<a href="/dumpling-overview.md">Dumpling論理ダンパー</a>](/dumpling-overview.md)                                                                                 |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |
| [<a href="/sql-statements/sql-statement-load-data.md">トランザクション`LOAD DATA`</a>](/sql-statements/sql-statement-load-data.md)                                  |  Y [^5] |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |   [^6]  |
| [<a href="/migration-overview.md">データベース移行ツールキット (DM)</a>](/migration-overview.md)                                                                          |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |
| [<a href="/tidb-binlog/tidb-binlog-overview.md">TiDBBinlog</a>](/tidb-binlog/tidb-binlog-overview.md)                                                       |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |
| [<a href="/ticdc/ticdc-overview.md">変更データキャプチャ (CDC)</a>](/ticdc/ticdc-overview.md)                                                                         |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |
| [<a href="/ticdc/ticdc-sink-to-cloud-storage.md">TiCDC を介して Amazon S3、GCS、Azure Blob Storage、NFS にデータをストリーミングする</a>](/ticdc/ticdc-sink-to-cloud-storage.md) |    Y    |    E    |    N    |    N    |    N    |    N    |    N    |    N    |    N    |
| [<a href="/ticdc/ticdc-bidirectional-replication.md">TiCDC は 2 つの TiDB クラスター間の双方向レプリケーションをサポートします</a>](/ticdc/ticdc-bidirectional-replication.md)           |    Y    |    Y    |    N    |    N    |    N    |    N    |    N    |    N    |    N    |
| [<a href="/ticdc/ticdc-open-api-v2.md">TiCDC OpenAPI v2</a>](/ticdc/ticdc-open-api-v2.md)                                                                   |    Y    |    N    |    N    |    N    |    N    |    N    |    N    |    N    |    N    |

## 管理、可観測性、ツール {#management-observability-and-tools}

| 管理、可観測性、ツール                                                                                                                                                                                                     | 7.1 | 6.5 | 6.1 | 5.4 | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| [<a href="/dashboard/dashboard-intro.md">TiDB ダッシュボード UI</a>](/dashboard/dashboard-intro.md)                                                                                                                    |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/dashboard/continuous-profiling.md">TiDB ダッシュボードの継続的プロファイリング</a>](/dashboard/continuous-profiling.md)                                                                                                 |  Y  |  Y  |  Y  |  E  |  E  |  N  |  N  |  N  |  N  |
| [<a href="/dashboard/top-sql.md">TiDB ダッシュボードのTop SQL</a>](/dashboard/top-sql.md)                                                                                                                               |  Y  |  Y  |  Y  |  E  |  N  |  N  |  N  |  N  |  N  |
| [<a href="/information-schema/information-schema-sql-diagnostics.md">TiDB ダッシュボード SQL 診断</a>](/information-schema/information-schema-sql-diagnostics.md)                                                        |  Y  |  Y  |  E  |  E  |  E  |  E  |  E  |  E  |  E  |
| [<a href="/dashboard/dashboard-diagnostics-access.md">TiDB ダッシュボードのクラスタ診断</a>](/dashboard/dashboard-diagnostics-access.md)                                                                                      |  Y  |  Y  |  E  |  E  |  E  |  E  |  E  |  E  |  E  |
| [<a href="/grafana-tikv-dashboard.md#tikv-fasttune-dashboard">TiKV-FastTune ダッシュボード</a>](/grafana-tikv-dashboard.md#tikv-fasttune-dashboard)                                                                    |  E  |  E  |  E  |  E  |  E  |  E  |  E  |  E  |  E  |
| [<a href="/information-schema/information-schema.md">情報スキーマ</a>](/information-schema/information-schema.md)                                                                                                     |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/metrics-schema.md">メトリクススキーマ</a>](/metrics-schema.md)                                                                                                                                                |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/statement-summary-tables.md">ステートメントの概要テーブル</a>](/statement-summary-tables.md)                                                                                                                       |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/statement-summary-tables.md#persist-statements-summary">ステートメント概要テーブル - 概要の永続性</a>](/statement-summary-tables.md#persist-statements-summary)                                                         |  E  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [<a href="/identify-slow-queries.md">スロークエリログ</a>](/identify-slow-queries.md)                                                                                                                                   |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/tiup/tiup-overview.md">TiUP導入</a>](/tiup/tiup-overview.md)                                                                                                                                           |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="https://docs.pingcap.com/tidb-in-kubernetes/">Kubernetes オペレーター</a>](https://docs.pingcap.com/tidb-in-kubernetes/)                                                                                    |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/br/backup-and-restore-use-cases.md">内蔵の物理バックアップ</a>](/br/backup-and-restore-use-cases.md)                                                                                                            |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/sql-statements/sql-statement-kill.md">グローバルキル</a>](/sql-statements/sql-statement-kill.md)                                                                                                            |  Y  |  Y  |  Y  |  E  |  E  |  E  |  E  |  E  |  E  |
| [<a href="/information-schema/information-schema-data-lock-waits.md">ビューをロックする</a>](/information-schema/information-schema-data-lock-waits.md)                                                                  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  E  |  E  |  E  |
| [<a href="/sql-statements/sql-statement-show-config.md">`SHOW CONFIG`</a>](/sql-statements/sql-statement-show-config.md)                                                                                        |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |
| [<a href="/dynamic-config.md">`SET CONFIG`</a>](/dynamic-config.md)                                                                                                                                             |  Y  |  Y  |  Y  |  E  |  E  |  E  |  E  |  E  |  E  |
| [<a href="/dm/dm-webui-guide.md">DM WebUI</a>](/dm/dm-webui-guide.md)                                                                                                                                           |  E  |  E  |  E  |  N  |  N  |  N  |  N  |  N  |  N  |
| [<a href="/tikv-configuration-file.md#foreground-quota-limiter">フォアグラウンド クォータ リミッター</a>](/tikv-configuration-file.md#foreground-quota-limiter)                                                                  |  Y  |  Y  |  E  |  N  |  N  |  N  |  N  |  N  |  N  |
| [<a href="/tikv-configuration-file.md#background-quota-limiter">バックグラウンド クォータ リミッター</a>](/tikv-configuration-file.md#background-quota-limiter)                                                                  |  E  |  E  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [<a href="https://docs.pingcap.com/tidb-in-kubernetes/v1.4/backup-to-aws-s3-by-snapshot">EBS ボリュームのスナップショットのバックアップと復元</a>](https://docs.pingcap.com/tidb-in-kubernetes/v1.4/backup-to-aws-s3-by-snapshot)       |  Y  |  Y  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [<a href="/br/backup-and-restore-overview.md">PITR</a>](/br/backup-and-restore-overview.md)                                                                                                                     |  Y  |  Y  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [<a href="/configure-memory-usage.md#configure-the-memory-usage-threshold-of-a-tidb-server-instance">グローバルメモリ制御</a>](/configure-memory-usage.md#configure-the-memory-usage-threshold-of-a-tidb-server-instance) |  Y  |  Y  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [<a href="/tikv-configuration-file.md#api-version-new-in-v610">クラスター間の RawKV レプリケーション</a>](/tikv-configuration-file.md#api-version-new-in-v610)                                                                 |  E  |  E  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [<a href="/system-variables.md#tidb_gc_scan_lock_mode-new-in-v50">グリーンGC</a>](/system-variables.md#tidb_gc_scan_lock_mode-new-in-v50)                                                                           |  E  |  E  |  E  |  E  |  E  |  E  |  E  |  E  |  N  |
| [<a href="/tidb-resource-control.md">リソース制御</a>](/tidb-resource-control.md)                                                                                                                                     |  Y  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [<a href="/tiflash/tiflash-disaggregated-and-s3.md">TiFlash の分散型ストレージとコンピューティングアーキテクチャおよび S3 サポート</a>](/tiflash/tiflash-disaggregated-and-s3.md)                                                                |  E  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |

[^1]: TiDB は、latin1 を utf8 のサブセットとして誤って扱います。詳細については[<a href="https://github.com/pingcap/tidb/issues/18955">TiDB #18955</a>](https://github.com/pingcap/tidb/issues/18955)参照してください。

[^2]: v6.5.0 以降、 [<a href="/system-variables.md#tidb_allow_function_for_expression_index-new-in-v520">`tidb_allow_function_for_expression_index`</a>](/system-variables.md#tidb_allow_function_for_expression_index-new-in-v520)システム変数によってリストされた関数に対して作成された式インデックスはテストされており、本番環境で使用できるようになりました。将来のリリースでは、さらに多くの関数がサポートされる予定です。この変数にリストされていない関数については、対応する式インデックスを本番環境で使用することは推奨されません。詳細は[<a href="/sql-statements/sql-statement-create-index.md#expression-index">式インデックス</a>](/sql-statements/sql-statement-create-index.md#expression-index)参照してください。

[^3]: サポートされている SQL ステートメントの完全なリストについては、 [<a href="/sql-statements/sql-statement-select.md">ステートメントのリファレンス</a>](/sql-statements/sql-statement-select.md)を参照してください。

[^4]: TiDB は[<a href="/releases/release-6.4.0.md">v6.4.0</a>](/releases/release-6.4.0.md)から始まり[<a href="/auto-increment.md#mysql-compatibility-mode">高性能でグローバルに単調な`AUTO_INCREMENT`カラム</a>](/auto-increment.md#mysql-compatibility-mode)をサポートします

[^5]: [<a href="/releases/release-7.0.0.md">TiDB v7.0.0</a>](/releases/release-7.0.0.md)の場合、新しいパラメータ`FIELDS DEFINED NULL BY`と S3 および GCS からのデータのインポートのサポートは実験的機能です。

[^6]: TiDB v4.0 の場合、 `LOAD DATA`トランザクションはアトミック性を保証しません。
