---
title: TiDB Features
summary: Learn about the basic features of TiDB.
---

# TiDB の機能 {#tidb-features}

このドキュメントでは、TiDB の各バージョンでサポートされている機能を一覧表示しています。実験的機能のサポートは、最終リリースの前に変更される可能性があることに注意してください。

## データ型、関数、および演算子 {#data-types-functions-and-operators}

| データ型、関数、および演算子                                                                 | 6.5 | 6.4 | 6.3 |      6.2     |      6.1     |      6.0     | 5.4          |      5.3     |      5.2     |      5.1     |      5.0     |      4.0     |
| ------------------------------------------------------------------------------ | :-: | :-: | :-: | :----------: | :----------: | :----------: | ------------ | :----------: | :----------: | :----------: | :----------: | :----------: |
| [数値型](/data-type-numeric.md)                                                   |  Y  |  Y  |  Y  |       Y      |       Y      |       Y      | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [日付と時刻の種類](/data-type-date-and-time.md)                                        |  Y  |  Y  |  Y  |       Y      |       Y      |       Y      | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [文字列型](/data-type-string.md)                                                   |  Y  |  Y  |  Y  |       Y      |       Y      |       Y      | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [JSON タイプ](/data-type-json.md)                                                 |  Y  |  Y  |  Y  | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |
| [制御フロー関数](/functions-and-operators/control-flow-functions.md)                  |  Y  |  Y  |  Y  |       Y      |       Y      |       Y      | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [文字列関数](/functions-and-operators/string-functions.md)                          |  Y  |  Y  |  Y  |       Y      |       Y      |       Y      | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [数値関数と演算子](/functions-and-operators/numeric-functions-and-operators.md)        |  Y  |  Y  |  Y  |       Y      |       Y      |       Y      | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [日付と時刻関数](/functions-and-operators/date-and-time-functions.md)                 |  Y  |  Y  |  Y  |       Y      |       Y      |       Y      | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [ビット関数と演算子](/functions-and-operators/bit-functions-and-operators.md)           |  Y  |  Y  |  Y  |       Y      |       Y      |       Y      | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [キャスト関数と演算子](/functions-and-operators/cast-functions-and-operators.md)         |  Y  |  Y  |  Y  |       Y      |       Y      |       Y      | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [暗号化および圧縮関数](/functions-and-operators/encryption-and-compression-functions.md) |  Y  |  Y  |  Y  |       Y      |       Y      |       Y      | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [情報関数](/functions-and-operators/information-functions.md)                      |  Y  |  Y  |  Y  |       Y      |       Y      |       Y      | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [JSON関数](/functions-and-operators/json-functions.md)                           |  Y  |  Y  |  Y  | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |
| [集計関数](/functions-and-operators/aggregate-group-by-functions.md)               |  Y  |  Y  |  Y  |       Y      |       Y      |       Y      | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [ウィンドウ関数](/functions-and-operators/window-functions.md)                        |  Y  |  Y  |  Y  |       Y      |       Y      |       Y      | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [その他の関数](/functions-and-operators/miscellaneous-functions.md)                  |  Y  |  Y  |  Y  |       Y      |       Y      |       Y      | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [オペレーター](/functions-and-operators/operators.md)                                |  Y  |  Y  |  Y  |       Y      |       Y      |       Y      | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [文字セットと照合](/character-set-and-collation.md) [^1]                               |  Y  |  Y  |  Y  |       Y      |       Y      |       Y      | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [ユーザーレベルのロック](/functions-and-operators/locking-functions.md)                   |  Y  |  Y  |  Y  |       Y      |       Y      |       N      | N            |       N      |       N      |       N      |       N      |       N      |

## 索引付けと制約 {#indexing-and-constraints}

| 索引付けと制約                                                                         | 6.5 |      6.4     |      6.3     |      6.2     |      6.1     |      6.0     | 5.4          |      5.3     |      5.2     |      5.1     |      5.0     | 4.0 |
| ------------------------------------------------------------------------------- | :-: | :----------: | :----------: | :----------: | :----------: | :----------: | ------------ | :----------: | :----------: | :----------: | :----------: | :-: |
| [発現インデックス](/sql-statements/sql-statement-create-index.md#expression-index) [^2] |  Y  | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |     |
| [カラム型ストレージ (TiFlash)](/tiflash/tiflash-overview.md)                             |  Y  |       Y      |       Y      |       Y      |       Y      |       Y      | Y            |       Y      |       Y      |       Y      |       Y      |  Y  |
| [RocksDB エンジン](/storage-engine/rocksdb-overview.md)                             |  Y  |       Y      |       Y      |       Y      |       Y      |       Y      | Y            |       Y      |       Y      |       Y      |       Y      |  Y  |
| [タイタンプラグイン](/storage-engine/titan-overview.md)                                  |  Y  |       Y      |       Y      |       Y      |       Y      |       Y      | Y            |       Y      |       Y      |       Y      |       Y      |  Y  |
| [見えないインデックス](/sql-statements/sql-statement-add-index.md)                        |  Y  |       Y      |       Y      |       Y      |       Y      |       Y      | Y            |       Y      |       Y      |       Y      |       Y      |  N  |
| [複合`PRIMARY KEY`](/constraints.md)                                              |  Y  |       Y      |       Y      |       Y      |       Y      |       Y      | Y            |       Y      |       Y      |       Y      |       Y      |  Y  |
| [一意のインデックス](/constraints.md)                                                    |  Y  |       Y      |       Y      |       Y      |       Y      |       Y      | Y            |       Y      |       Y      |       Y      |       Y      |  Y  |
| [整数`PRIMARY KEY`のクラスター化インデックス](/constraints.md)                                 |  Y  |       Y      |       Y      |       Y      |       Y      |       Y      | Y            |       Y      |       Y      |       Y      |       Y      |  Y  |
| [複合キーまたは非整数キーのクラスター化インデックス](/constraints.md)                                    |  Y  |       Y      |       Y      |       Y      |       Y      |       Y      | Y            |       Y      |       Y      |       Y      |       Y      |  N  |

## SQL ステートメント {#sql-statements}

| SQL ステートメント[^3]                                                                                   |      6.5     |      6.4     |      6.3     |      6.2     |      6.1     |      6.0     |      5.4     |      5.3     |      5.2     |      5.1     |      5.0     |      4.0     |
| ------------------------------------------------------------------------------------------------- | :----------: | :----------: | :----------: | :----------: | :----------: | :----------: | :----------: | :----------: | :----------: | :----------: | :----------: | :----------: |
| `REPLACE` `SELECT` `INSERT` `UPDATE` `DELETE`                                                     |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |
| `INSERT ON DUPLICATE KEY UPDATE`                                                                  |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |
| `LOAD DATA INFILE`                                                                                |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |
| `SELECT INTO OUTFILE`                                                                             |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |
| `INNER JOIN` , `LEFT|RIGHT [OUTER] JOIN`                                                          |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |
| `UNION` 、 `UNION ALL`                                                                             |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |
| [`EXCEPT`および<code>INTERSECT</code>演算子](/functions-and-operators/set-operators.md)                 |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       N      |
| `GROUP BY` 、 `ORDER BY`                                                                           |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |
| [ウィンドウ関数](/functions-and-operators/window-functions.md)                                           |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |
| [共通テーブル式 (CTE)](/sql-statements/sql-statement-with.md)                                            |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       N      |       N      |
| `START TRANSACTION` 、 `COMMIT` 、 `ROLLBACK`                                                       |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |
| [`EXPLAIN`](/sql-statements/sql-statement-explain.md)                                             |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |
| [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)                             |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      |
| [ユーザー定義変数](/user-defined-variables.md)                                                            | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |
| [`BATCH [ON COLUMN] LIMIT INTEGER DELETE`](/sql-statements/sql-statement-batch.md)                |       Y      |       Y      |       Y      |       Y      |       Y      |       N      |       N      |       N      |       N      |       N      |       N      |       N      |
| [`BATCH [ON COLUMN] LIMIT INTEGER INSERT/UPDATE/REPLACE`](/sql-statements/sql-statement-batch.md) |       Y      |       N      |       N      |       N      |       N      |       N      |       N      |       N      |       N      |       N      |       N      |       N      |
| [`ALTER TABLE ... COMPACT`](/sql-statements/sql-statement-alter-table-compact.md)                 |       Y      |       Y      |       Y      |       Y      | Experimental |       N      |       N      |       N      |       N      |       N      |       N      |       N      |

## 高度な SQL 機能 {#advanced-sql-features}

| 高度な SQL 機能                                             | 6.5 | 6.4 | 6.3 | 6.2 | 6.1 | 6.0 | 5.4          |      5.3     |      5.2     |      5.1     |      5.0     |      4.0     |
| ------------------------------------------------------ | :-: | :-: | :-: | :-: | :-: | :-: | ------------ | :----------: | :----------: | :----------: | :----------: | :----------: |
| [プリペアド ステートメント キャッシュ](/sql-prepared-plan-cache.md)     |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  | Y            |       Y      | Experimental | Experimental | Experimental | Experimental |
| [SQL 計画管理 (SPM)](/sql-plan-management.md)              |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [コプロセッサー・キャッシュ](/coprocessor-cache.md)                 |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  | Y            |       Y      |       Y      |       Y      |       Y      | Experimental |
| [ステイル読み取り](/stale-read.md)                             |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  | Y            |       Y      |       Y      |       Y      |       N      |       N      |
| [Followerが読む](/follower-read.md)                       |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [履歴データの読み取り (tidb_snapshot)](/read-historical-data.md) |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [オプティマイザーのヒント](/optimizer-hints.md)                    |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [MPP 実行エンジン](/explain-mpp.md)                          |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  | Y            |       Y      |       Y      |       Y      |       Y      |       N      |
| [インデックス マージ](/explain-index-merge.md)                  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  | Y            | Experimental | Experimental | Experimental | Experimental | Experimental |
| [SQL の配置規則](/placement-rules-in-sql.md)                |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  | Experimental | Experimental |       N      |       N      |       N      |       N      |

## データ定義言語 (DDL) {#data-definition-language-ddl}

| データ定義言語 (DDL)                                                                                            |      6.5     |      6.4     |      6.3     |      6.2     |      6.1     |      6.0     | 5.4          |      5.3     |      5.2     |      5.1     |      5.0     |      4.0     |
| -------------------------------------------------------------------------------------------------------- | :----------: | :----------: | :----------: | :----------: | :----------: | :----------: | ------------ | :----------: | :----------: | :----------: | :----------: | :----------: |
| `TRUNCATE` `CREATE` `DROP` `ALTER` `RENAME`                                                              |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [生成された列](/generated-columns.md)                                                                          | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |
| [ビュー](/views.md)                                                                                         |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [シーケンス](/sql-statements/sql-statement-create-sequence.md)                                                |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [自動増加](/auto-increment.md)                                                                               |       Y      |     Y[^4]    |       Y      |       Y      |       Y      |       Y      | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [オートランダム](/auto-random.md)                                                                               |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [TTL (存続可能時間)](/time-to-live.md)                                                                         | Experimental |       N      |       N      |       N      |       N      |       N      | N            |       N      |       N      |       N      |       N      |       N      |
| [DDL アルゴリズム アサーション](/sql-statements/sql-statement-alter-table.md)                                        |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| マルチスキーマの変更: 列を追加                                                                                         |       Y      |       Y      |       Y      |       Y      | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |
| [列の種類を変更する](/sql-statements/sql-statement-modify-column.md)                                              |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      | Y            |       Y      |       Y      |       Y      |       N      |       N      |
| [一時テーブル](/temporary-tables.md)                                                                           |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      | Y            |       Y      |       N      |       N      |       N      |       N      |
| [同時 DDL ステートメント](/system-variables.md#tidb_enable_concurrent_ddl-new-in-v620)                            |       Y      |       Y      |       Y      |       Y      |       N      |       N      | N            |       N      |       N      |       N      |       N      |       N      |
| [`ADD INDEX`と<code>CREATE INDEX</code>の高速化](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) |       Y      | Experimental | Experimental |       N      |       N      |       N      | N            |       N      |       N      |       N      |       N      |       N      |
| [メタデータ ロック](/metadata-lock.md)                                                                           |       Y      | Experimental | Experimental |       N      |       N      |       N      | N            |       N      |       N      |       N      |       N      |       N      |
| [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-to-timestamp.md)              |       Y      | Experimental |       N      |       N      |       N      |       N      | N            |       N      |       N      |       N      |       N      |       N      |

## 取引 {#transactions}

| 取引                                                                    | 6.5 | 6.4 | 6.3 | 6.2 | 6.1 | 6.0 | 5.4 | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 |
| --------------------------------------------------------------------- | :-: | :-: | :-: | :-: | :-: | :-- | --- | :-: | :-: | :-: | :-: | :-: |
| [非同期コミット](/system-variables.md#tidb_enable_async_commit-new-in-v50)   |  Y  |  Y  |  Y  |  Y  |  Y  | Y   | Y   |  Y  |  Y  |  Y  |  Y  |  N  |
| [1個](/system-variables.md#tidb_enable_1pc-new-in-v50)                 |  Y  |  Y  |  Y  |  Y  |  Y  | Y   | Y   |  Y  |  Y  |  Y  |  Y  |  N  |
| [大規模トランザクション (10GB)](/transaction-overview.md#transaction-size-limit) |  Y  |  Y  |  Y  |  Y  |  Y  | Y   | Y   |  Y  |  Y  |  Y  |  Y  |  Y  |
| [悲観的な取引](/pessimistic-transaction.md)                                 |  Y  |  Y  |  Y  |  Y  |  Y  | Y   | Y   |  Y  |  Y  |  Y  |  Y  |  Y  |
| [楽観的な取引](/optimistic-transaction.md)                                  |  Y  |  Y  |  Y  |  Y  |  Y  | Y   | Y   |  Y  |  Y  |  Y  |  Y  |  Y  |
| [反復可能読み取り分離 (スナップショット分離)](/transaction-isolation-levels.md)           |  Y  |  Y  |  Y  |  Y  |  Y  | Y   | Y   |  Y  |  Y  |  Y  |  Y  |  Y  |
| [読み取りコミット分離](/transaction-isolation-levels.md)                        |  Y  |  Y  |  Y  |  Y  |  Y  | Y   | Y   |  Y  |  Y  |  Y  |  Y  |  Y  |

## パーティショニング {#partitioning}

| パーティショニング                                                                  |      6.5     |      6.4     |      6.3     |      6.2     |      6.1     |      6.0     | 5.4          |      5.3     |      5.2     |      5.1     |      5.0     | 4.0 |   |
| -------------------------------------------------------------------------- | :----------: | :----------: | :----------: | :----------: | :----------: | :----------: | ------------ | :----------: | :----------: | :----------: | :----------: | :-: | - |
| [範囲分割](/partitioned-table.md)                                              |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      | Y            |       Y      |       Y      |       Y      |       Y      |  Y  |   |
| [ハッシュパーティショニング](/partitioned-table.md)                                     |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      | Y            |       Y      |       Y      |       Y      |       Y      |  Y  |   |
| [List パーティショニング](/partitioned-table.md)                                    |       Y      |       Y      |       Y      |       Y      |       Y      | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |  N  |   |
| [List COLUMNS パーティショニング](/partitioned-table.md)                            |       Y      |       Y      |       Y      |       Y      |       Y      | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |  N  |   |
| [`EXCHANGE PARTITION`](/partitioned-table.md)                              |       Y      |       Y      |       Y      | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |  N  |   |
| [動的剪定](/partitioned-table.md#dynamic-pruning-mode)                         |       Y      |       Y      |       Y      |       Y      |       Y      | Experimental | Experimental | Experimental | Experimental | Experimental |       N      |  N  |   |
| [範囲 COLUMNS パーティショニング](/partitioned-table.md#range-columns-partitioning)   |       Y      |       Y      |       Y      |       N      |       N      |       N      | N            |       N      |       N      |       N      |       N      |  N  | N |
| [範囲 INTERVAL パーティショニング](/partitioned-table.md#range-interval-partitioning) | Experimental | Experimental | Experimental |       N      |       N      |       N      | N            |       N      |       N      |       N      |       N      |  N  | N |

## 統計 {#statistics}

| 統計                                                    |      6.5     |      6.4     |      6.3     |      6.2     |      6.1     |      6.0     | 5.4          |      5.3     |      5.2     |      5.1     |      5.0     |      4.0     |
| ----------------------------------------------------- | :----------: | :----------: | :----------: | :----------: | :----------: | :----------: | ------------ | :----------: | :----------: | :----------: | :----------: | :----------: |
| [CMSketch](/statistics.md)                            |   デフォルトで無効   |   デフォルトで無効   |   デフォルトで無効   |   デフォルトで無効   |   デフォルトで無効   |   デフォルトで無効   | デフォルトで無効     |   デフォルトで無効   |       Y      |       Y      |       Y      |       Y      |
| [ヒストグラム](/statistics.md)                              |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [拡張統計](/extended-statistics.md)                       | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |       N      |
| 統計フィードバック                                             |       N      |       N      |       N      |       N      |      非推奨     |      非推奨     | 非推奨          | Experimental | Experimental | Experimental | Experimental | Experimental |
| [統計を自動的に更新する](/statistics.md#automatic-update)        |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [高速分析](/system-variables.md#tidb_enable_fast_analyze) | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |
| [動的剪定](/partitioned-table.md#dynamic-pruning-mode)    |       Y      |       Y      |       Y      |       Y      |       Y      | Experimental | Experimental | Experimental | Experimental | Experimental |       N      |       N      |

## 安全 {#security}

| 安全                                                                              | 6.5 | 6.4 | 6.3 | 6.2 | 6.1 | 6.0 | 5.4 | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 |
| ------------------------------------------------------------------------------- | :-: | :-: | :-: | :-: | :-: | :-: | --- | :-: | :-: | :-: | :-: | :-: |
| [透過レイヤーセキュリティ (TLS)](/enable-tls-between-clients-and-servers.md)                |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |  Y  |
| [保存時の暗号化 (TDE)](/encryption-at-rest.md)                                         |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |  Y  |
| [役割ベースの認証 (RBAC)](/role-based-access-control.md)                                |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |  Y  |
| [証明書ベースの認証](/certificate-authentication.md)                                     |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |  Y  |
| [`caching_sha2_password`認証](/system-variables.md#default_authentication_plugin) |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  | Y   |  Y  |  Y  |  N  |  N  |  N  |
| [`tidb_sm3_password`認証](/system-variables.md#default_authentication_plugin)     |  Y  |  Y  |  Y  |  N  |  N  |  N  | N   |  N  |  N  |  N  |  N  |  N  |
| [`tidb_auth_token`認証](/system-variables.md#default_authentication_plugin)       |  Y  |  Y  |  N  |  N  |  N  |  N  | N   |  N  |  N  |  N  |  N  |  N  |
| [パスワード管理](/password-management.md)                                              |  Y  |  N  |  N  |  N  |  N  |  N  | N   |  N  |  N  |  N  |  N  |  N  |
| [MySQL 互換`GRANT`システム](/privilege-management.md)                                 |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |  Y  |
| [動的権限](/privilege-management.md#dynamic-privileges)                             |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  N  |  N  |
| [セキュリティ強化モード](/system-variables.md#tidb_enable_enhanced_security)               |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  N  |  N  |
| [編集されたログ ファイル](/log-redaction.md)                                               |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |  N  |

## データのインポートとエクスポート {#data-import-and-export}

| データのインポートとエクスポート                                                                                    |      6.5     | 6.4 | 6.3 | 6.2 | 6.1 | 6.0 | 5.4 | 5.3 | 5.2 | 5.1 | 5.0 |   4.0  |
| --------------------------------------------------------------------------------------------------- | :----------: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :----: |
| [高速インポーター (TiDB Lightning)](/tidb-lightning/tidb-lightning-overview.md)                             |       Y      |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |    Y   |
| mydumper 論理ダンパー                                                                                     |      非推奨     | 非推奨 | 非推奨 | 非推奨 | 非推奨 | 非推奨 | 非推奨 | 非推奨 | 非推奨 | 非推奨 | 非推奨 |   非推奨  |
| [Dumpling論理ダンパー](/dumpling-overview.md)                                                             |       Y      |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |    Y   |
| [トランザクション`LOAD DATA`](/sql-statements/sql-statement-load-data.md)                                   |       Y      |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  | N [^5] |
| [データベース移行ツールキット (DM)](/migration-overview.md)                                                       |       Y      |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |    Y   |
| [Binlog](/tidb-binlog/tidb-binlog-overview.md)                                                      |       Y      |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |    Y   |
| [変更データ キャプチャ (CDC)](/ticdc/ticdc-overview.md)                                                       |       Y      |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |    Y   |
| [TiCDC を介して Amazon S3、Azure Blob Storage、NFS にデータをストリーミングする](/ticdc/ticdc-sink-to-cloud-storage.md) | Experimental |  N  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |    N   |
| [TiCDC は、2 つの TiDB クラスター間の双方向レプリケーションをサポートします](/ticdc/ticdc-bidirectional-replication.md)           |       Y      |  N  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |    N   |

## 管理、可観測性、およびツール {#management-observability-and-tools}

| 管理、可観測性、およびツール                                                                                                |      6.5     |      6.4     |      6.3     |      6.2     |      6.1     |      6.0     | 5.4          |      5.3     |      5.2     |      5.1     |      5.0     |      4.0     |
| ------------------------------------------------------------------------------------------------------------- | :----------: | :----------: | :----------: | :----------: | :----------: | :----------: | ------------ | :----------: | :----------: | :----------: | :----------: | :----------: |
| [TiDB ダッシュボード UI](/dashboard/dashboard-intro.md)                                                              |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [TiDB ダッシュボードの継続的なプロファイリング](/dashboard/continuous-profiling.md)                                               |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      | Experimental | Experimental |       N      |       N      |       N      |       N      |
| [TiDB ダッシュボードTop SQL](/dashboard/top-sql.md)                                                                  |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      | Experimental |       N      |       N      |       N      |       N      |       N      |
| [TiDB ダッシュボード SQL 診断](/information-schema/information-schema-sql-diagnostics.md)                              |       Y      |       Y      | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |
| [TiDB ダッシュボードクラスタ診断](/dashboard/dashboard-diagnostics-access.md)                                              |       Y      |       Y      | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |
| [情報スキーマ](/information-schema/information-schema.md)                                                           |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [指標スキーマ](/metrics-schema.md)                                                                                  |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [ステートメント要約表](/statement-summary-tables.md)                                                                    |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [スロー クエリ ログ](/identify-slow-queries.md)                                                                       |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [TiUP展開](/tiup/tiup-overview.md)                                                                              |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [Kubernetes オペレーター](https://docs.pingcap.com/tidb-in-kubernetes/)                                             |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [組み込みの物理バックアップ](/br/backup-and-restore-use-cases.md)                                                          |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [グローバルキル](/sql-statements/sql-statement-kill.md)                                                              |       Y      |       Y      |       Y      |       Y      |       Y      | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |
| [ビューをロック](/information-schema/information-schema-data-lock-waits.md)                                          |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      | Y            |       Y      |       Y      | Experimental | Experimental | Experimental |
| [`SHOW CONFIG`](/sql-statements/sql-statement-show-config.md)                                                 |       Y      |       Y      |       Y      |       Y      |       Y      |       Y      | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [`SET CONFIG`](/dynamic-config.md)                                                                            |       Y      |       Y      |       Y      |       Y      |       Y      | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |
| [DM WebUI](/dm/dm-webui-guide.md)                                                                             | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental | N            |       N      |       N      |       N      |       N      |       N      |
| [フォアグラウンド クォータ リミッター](/tikv-configuration-file.md#foreground-quota-limiter)                                   |       Y      |       Y      |       Y      |       Y      | Experimental | Experimental | N            |       N      |       N      |       N      |       N      |       N      |
| [EBS ボリュームのスナップショットのバックアップと復元](https://docs.pingcap.com/tidb-in-kubernetes/v1.4/backup-to-aws-s3-by-snapshot) |       Y      |       Y      |       N      |       N      |       N      |       N      | N            |       N      |       N      |       N      |       N      |       N      |
| [PITR](/br/backup-and-restore-overview.md)                                                                    |       Y      |       Y      |       Y      |       Y      |       N      |       N      | N            |       N      |       N      |       N      |       N      |       N      |
| [グローバルメモリ制御](/configure-memory-usage.md#configure-the-memory-usage-threshold-of-a-tidb-server-instance)       |       Y      | Experimental |       N      |       N      |       N      |       N      | N            |       N      |       N      |       N      |       N      |       N      |

[^1]: TiDB は、latin1 を utf8 のサブセットとして誤って扱います。詳細については、 [TiDB #18955](https://github.com/pingcap/tidb/issues/18955)を参照してください。

[^2]: v6.5.0 以降、 [`tidb_allow_function_for_expression_index`](/system-variables.md#tidb_allow_function_for_expression_index-new-in-v520)システム変数によってリストされた関数で作成された式インデックスがテストされ、本番環境で使用できます。今後のリリースでは、より多くの関数がサポートされる予定です。この変数によってリストされていない関数については、対応する式インデックスを本番環境で使用することはお勧めしません。詳細は[式インデックス](/sql-statements/sql-statement-create-index.md#expression-index)を参照してください。

[^3]: サポートされている SQL ステートメントの完全なリストについては、 [ステートメント リファレンス](/sql-statements/sql-statement-select.md)を参照してください。

[^4]: v6.4.0 以降、TiDB は[高パフォーマンスでグローバルに単調な`AUTO_INCREMENT`列](/auto-increment.md#mysql-compatibility-mode)をサポートします。

[^5]: TiDB v4.0 の場合、 `LOAD DATA`トランザクションは原子性を保証しません。
