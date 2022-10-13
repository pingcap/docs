---
title: TiDB Features
summary: Learn about the basic features of TiDB.
---

# TiDB の機能 {#tidb-features}

このドキュメントでは、TiDB の各バージョンでサポートされている機能を一覧表示しています。実験的機能のサポートは、最終リリースの前に変更される可能性があることに注意してください。

## データ型、関数、および演算子 {#data-types-functions-and-operators}

| データ型、関数、および演算子                                                                 | 6.3 | 6.2 | 6.1 | 6.0 | 5.4 | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 |
| ------------------------------------------------------------------------------ | :-: | :-: | :-: | :-: | --- | :-: | :-: | :-: | :-: | :-: |
| [数値型](/data-type-numeric.md)                                                   |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [日付と時刻の種類](/data-type-date-and-time.md)                                        |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [文字列型](/data-type-string.md)                                                   |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [JSON タイプ](/data-type-json.md)                                                 |  よ  | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 |
| [制御フロー関数](/functions-and-operators/control-flow-functions.md)                  |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [文字列関数](/functions-and-operators/string-functions.md)                          |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [数値関数と演算子](/functions-and-operators/numeric-functions-and-operators.md)        |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [日付と時刻関数](/functions-and-operators/date-and-time-functions.md)                 |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [ビット関数と演算子](/functions-and-operators/bit-functions-and-operators.md)           |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [キャスト関数と演算子](/functions-and-operators/cast-functions-and-operators.md)         |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [暗号化および圧縮関数](/functions-and-operators/encryption-and-compression-functions.md) |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [情報関数](/functions-and-operators/information-functions.md)                      |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [JSON関数](/functions-and-operators/json-functions.md)                           |  よ  | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 |
| [集計関数](/functions-and-operators/aggregate-group-by-functions.md)               |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [ウィンドウ関数](/functions-and-operators/window-functions.md)                        |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [その他の関数](/functions-and-operators/miscellaneous-functions.md)                  |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [オペレーター](/functions-and-operators/operators.md)                                |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [文字セットと照合](/character-set-and-collation.md) [^1]                               |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [ユーザーレベルのロック](/functions-and-operators/locking-functions.md)                   |  よ  |  よ  |  よ  |  N  | N   |  N  |  N  |  N  |  N  |  N  |

## 索引付けと制約 {#indexing-and-constraints}

| 索引付けと制約                                                                    | 6.3 | 6.2 | 6.1 | 6.0 | 5.4 | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 |
| -------------------------------------------------------------------------- | :-: | :-: | :-: | :-: | --- | :-: | :-: | :-: | :-: | :-: |
| [発現インデックス](/sql-statements/sql-statement-create-index.md#expression-index) | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 |     |
| [カラム型ストレージ (TiFlash)](/tiflash/tiflash-overview.md)                        |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [RocksDB エンジン](/storage-engine/rocksdb-overview.md)                        |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [タイタンプラグイン](/storage-engine/titan-overview.md)                             |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [見えないインデックス](/sql-statements/sql-statement-add-index.md)                   |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  N  |
| [複合`PRIMARY KEY`](/constraints.md)                                         |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [一意のインデックス](/constraints.md)                                               |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [整数`PRIMARY KEY`のクラスター化インデックス](/constraints.md)                            |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [複合キーまたは非整数キーのクラスター化インデックス](/constraints.md)                               |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  N  |

## SQL ステートメント {#sql-statements}

| SQL ステートメント[^2]                                                                    | 6.3 | 6.2 | 6.1 | 6.0 | 5.4 | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 |
| ---------------------------------------------------------------------------------- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| `REPLACE` `SELECT` `INSERT` `UPDATE` `DELETE`                                      |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |
| `INSERT ON DUPLICATE KEY UPDATE`                                                   |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |
| `LOAD DATA INFILE`                                                                 |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |
| `SELECT INTO OUTFILE`                                                              |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |
| `INNER JOIN` , `LEFT|RIGHT [OUTER] JOIN`                                           |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |
| `UNION` 、 `UNION ALL`                                                              |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |
| [`EXCEPT`および<code>INTERSECT</code>演算子](/functions-and-operators/set-operators.md)  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  N  |
| `GROUP BY` 、 `ORDER BY`                                                            |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |
| [ウィンドウ関数](/functions-and-operators/window-functions.md)                            |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |
| [共通テーブル式 (CTE)](/sql-statements/sql-statement-with.md)                             |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  N  |  N  |
| `START TRANSACTION` 、 `COMMIT` 、 `ROLLBACK`                                        |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |
| [`EXPLAIN`](/sql-statements/sql-statement-explain.md)                              |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |
| [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)              |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |
| [ユーザー定義変数](/user-defined-variables.md)                                             | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 |
| [`BATCH [ON COLUMN] LIMIT INTEGER DELETE`](/sql-statements/sql-statement-batch.md) |  よ  |  よ  |  よ  |  N  |  N  |  N  |  N  |  N  |  N  |  N  |
| [`ALTER TABLE ... COMPACT`](/sql-statements/sql-statement-alter-table-compact.md)  |  よ  |  よ  | 実験的 |  N  |  N  |  N  |  N  |  N  |  N  |  N  |

## 高度な SQL 機能 {#advanced-sql-features}

| 高度な SQL 機能                                             | 6.3 | 6.2 | 6.1 | 6.0 | 5.4 | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 |
| ------------------------------------------------------ | :-: | :-: | :-: | :-: | --- | :-: | :-: | :-: | :-: | :-: |
| [プリペアド ステートメント キャッシュ](/sql-prepared-plan-cache.md)     |  よ  |  よ  |  よ  |  よ  | よ   |  よ  | 実験的 | 実験的 | 実験的 | 実験的 |
| [SQL 計画管理 (SPM)](/sql-plan-management.md)              |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [コプロセッサー・キャッシュ](/coprocessor-cache.md)                 |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  | 実験的 |
| [ステイル読み取り](/stale-read.md)                             |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  N  |  N  |
| [フォロワーが読む](/follower-read.md)                          |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [履歴データの読み取り (tidb_snapshot)](/read-historical-data.md) |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [オプティマイザーのヒント](/optimizer-hints.md)                    |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [MPP 実行エンジン](/explain-mpp.md)                          |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  N  |
| [インデックス マージ](/explain-index-merge.md)                  |  よ  |  よ  |  よ  |  よ  | よ   | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 |
| [SQL の配置規則](/placement-rules-in-sql.md)                |  よ  |  よ  |  よ  |  よ  | 実験的 | 実験的 |  N  |  N  |  N  |  N  |

## データ定義言語 (DDL) {#data-definition-language-ddl}

| データ定義言語 (DDL)                                                     | 6.3 | 6.2 | 6.1 | 6.0 | 5.4 | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 |
| ----------------------------------------------------------------- | :-: | :-: | :-: | :-: | --- | :-: | :-: | :-: | :-: | :-: |
| `TRUNCATE` `CREATE` `DROP` `ALTER` `RENAME`                       |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [生成された列](/generated-columns.md)                                   | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 |
| [ビュー](/views.md)                                                  |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [シーケンス](/sql-statements/sql-statement-create-sequence.md)         |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [自動増加](/auto-increment.md)                                        |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [オートランダム](/auto-random.md)                                        |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [DDL アルゴリズム アサーション](/sql-statements/sql-statement-alter-table.md) |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| マルチスキーマの変更: 列を追加                                                  |  よ  |  よ  | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 |
| [列の種類を変更する](/sql-statements/sql-statement-modify-column.md)       |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  N  |  N  |
| [一時テーブル](/temporary-tables.md)                                    |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  N  |  N  |  N  |  N  |

## 取引 {#transactions}

| 取引                                                                    | 6.3 | 6.2 | 6.1 | 6.0 | 5.4 | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 |
| --------------------------------------------------------------------- | :-: | :-: | :-: | :-- | --- | :-: | :-: | :-: | :-: | :-: |
| [非同期コミット](/system-variables.md#tidb_enable_async_commit-new-in-v50)   |  よ  |  よ  |  よ  | よ   | よ   |  よ  |  よ  |  よ  |  よ  |  N  |
| [1個](/system-variables.md#tidb_enable_1pc-new-in-v50)                 |  よ  |  よ  |  よ  | よ   | よ   |  よ  |  よ  |  よ  |  よ  |  N  |
| [大規模トランザクション (10GB)](/transaction-overview.md#transaction-size-limit) |  よ  |  よ  |  よ  | よ   | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [悲観的な取引](/pessimistic-transaction.md)                                 |  よ  |  よ  |  よ  | よ   | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [楽観的な取引](/optimistic-transaction.md)                                  |  よ  |  よ  |  よ  | よ   | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [反復可能読み取り分離 (スナップショット分離)](/transaction-isolation-levels.md)           |  よ  |  よ  |  よ  | よ   | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [読み取りコミット分離](/transaction-isolation-levels.md)                        |  よ  |  よ  |  よ  | よ   | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |

## パーティショニング {#partitioning}

| パーティショニング                                                                  | 6.3 | 6.2 | 6.1 | 6.0 | 5.4 | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 |   |
| -------------------------------------------------------------------------- | :-: | :-: | :-: | :-: | --- | :-: | :-: | :-: | :-: | :-: | - |
| [範囲分割](/partitioned-table.md)                                              |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |   |
| [ハッシュパーティショニング](/partitioned-table.md)                                     |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |   |
| [List パーティショニング](/partitioned-table.md)                                    |  よ  |  よ  |  よ  | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 |  N  |   |
| [List COLUMNS パーティショニング](/partitioned-table.md)                            |  よ  |  よ  |  よ  | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 |  N  |   |
| [`EXCHANGE PARTITION`](/partitioned-table.md)                              |  よ  | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 |  N  |   |
| [動的剪定](/partitioned-table.md#dynamic-pruning-mode)                         |  よ  |  よ  |  よ  | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 |  N  |  N  |   |
| [範囲 COLUMNS パーティショニング](/partitioned-table.md#range-columns-partitioning)   |  よ  |  N  |  N  |  N  | N   |  N  |  N  |  N  |  N  |  N  | N |
| [範囲 INTERVAL パーティショニング](/partitioned-table.md#range-interval-partitioning) | 実験的 |  N  |  N  |  N  | N   |  N  |  N  |  N  |  N  |  N  | N |

## 統計 {#statistics}

| 統計                                                    |    6.3   |    6.2   |    6.1   |    6.0   | 5.4      |    5.3   | 5.2 | 5.1 | 5.0 | 4.0 |
| ----------------------------------------------------- | :------: | :------: | :------: | :------: | -------- | :------: | :-: | :-: | :-: | :-: |
| [CMSketch](/statistics.md)                            | デフォルトで無効 | デフォルトで無効 | デフォルトで無効 | デフォルトで無効 | デフォルトで無効 | デフォルトで無効 |  よ  |  よ  |  よ  |  よ  |
| [ヒストグラム](/statistics.md)                              |     よ    |     よ    |     よ    |     よ    | よ        |     よ    |  よ  |  よ  |  よ  |  よ  |
| [拡張統計](/extended-statistics.md)                       |    実験的   |    実験的   |    実験的   |    実験的   | 実験的      |    実験的   | 実験的 | 実験的 | 実験的 |  N  |
| [統計フィードバック](/statistics.md#automatic-update)          |    非推奨   |    非推奨   |    非推奨   |    非推奨   | 非推奨      |    実験的   | 実験的 | 実験的 | 実験的 | 実験的 |
| [統計を自動的に更新する](/statistics.md#automatic-update)        |     よ    |     よ    |     よ    |     よ    | よ        |     よ    |  よ  |  よ  |  よ  |  よ  |
| [高速分析](/system-variables.md#tidb_enable_fast_analyze) |    実験的   |    実験的   |    実験的   |    実験的   | 実験的      |    実験的   | 実験的 | 実験的 | 実験的 | 実験的 |
| [動的剪定](/partitioned-table.md#dynamic-pruning-mode)    |     よ    |     よ    |     よ    |    実験的   | 実験的      |    実験的   | 実験的 | 実験的 |  N  |  N  |

## 安全 {#security}

| 安全                                                                              | 6.3 | 6.2 | 6.1 | 6.0 | 5.4 | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 |
| ------------------------------------------------------------------------------- | :-: | :-: | :-: | :-: | --- | :-: | :-: | :-: | :-: | :-: |
| [透過レイヤーセキュリティ (TLS)](/enable-tls-between-clients-and-servers.md)                |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [保存時の暗号化 (TDE)](/encryption-at-rest.md)                                         |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [役割ベースの認証 (RBAC)](/role-based-access-control.md)                                |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [証明書ベースの認証](/certificate-authentication.md)                                     |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [`caching_sha2_password`認証](/system-variables.md#default_authentication_plugin) |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  N  |  N  |  N  |
| [`tidb_sm3_password`認証](/system-variables.md#default_authentication_plugin)     |  よ  |  N  |  N  |  N  | N   |  N  |  N  |  N  |  N  |  N  |
| [MySQL 互換`GRANT`システム](/privilege-management.md)                                 |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [動的権限](/privilege-management.md#dynamic-privileges)                             |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  N  |  N  |
| [セキュリティ強化モード](/system-variables.md#tidb_enable_enhanced_security)               |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  N  |  N  |
| [編集されたログ ファイル](/log-redaction.md)                                               |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  N  |

## データのインポートとエクスポート {#data-import-and-export}

| データのインポートとエクスポート                                                        | 6.3 | 6.2 | 6.1 | 6.0 | 5.4 | 5.3 | 5.2 | 5.1 | 5.0 |   4.0  |
| ----------------------------------------------------------------------- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :----: |
| [高速インポーター (TiDB Lightning)](/tidb-lightning/tidb-lightning-overview.md) |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |    よ   |
| mydumper 論理ダンパー                                                         | 非推奨 | 非推奨 | 非推奨 | 非推奨 | 非推奨 | 非推奨 | 非推奨 | 非推奨 | 非推奨 |   非推奨  |
| [Dumpling論理ダンパー](/dumpling-overview.md)                                 |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |    よ   |
| [トランザクション`LOAD DATA`](/sql-statements/sql-statement-load-data.md)       |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  | N [^3] |
| [データベース移行ツールキット (DM)](/migration-overview.md)                           |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |    よ   |
| [Binlog](/tidb-binlog/tidb-binlog-overview.md)                          |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |    よ   |
| [変更データ キャプチャ (CDC)](/ticdc/ticdc-overview.md)                           |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |  よ  |    よ   |

## 管理、可観測性、およびツール {#management-observability-and-tools}

| 管理、可観測性、およびツール                                                                   | 6.3 | 6.2 | 6.1 | 6.0 | 5.4 | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 |
| -------------------------------------------------------------------------------- | :-: | :-: | :-: | :-: | --- | :-: | :-: | :-: | :-: | :-: |
| [TiDB ダッシュボード UI](/dashboard/dashboard-intro.md)                                 |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [TiDB ダッシュボードの継続的なプロファイリング](/dashboard/continuous-profiling.md)                  |  よ  |  よ  |  よ  |  よ  | 実験的 | 実験的 |  N  |  N  |  N  |  N  |
| [TiDB ダッシュボードTop SQL](/dashboard/top-sql.md)                                     |  よ  |  よ  |  よ  |  よ  | 実験的 |  N  |  N  |  N  |  N  |  N  |
| [TiDB ダッシュボード SQL 診断](/information-schema/information-schema-sql-diagnostics.md) | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 |
| [情報スキーマ](/information-schema/information-schema.md)                              |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [指標スキーマ](/metrics-schema.md)                                                     |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [ステートメント要約表](/statement-summary-tables.md)                                       |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [スロー クエリ ログ](/identify-slow-queries.md)                                          |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [TiUP展開](/tiup/tiup-overview.md)                                                 |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| アンシブル展開                                                                          |  N  |  N  |  N  |  N  | N   |  N  |  N  |  N  |  N  | 非推奨 |
| [Kubernetes オペレーター](https://docs.pingcap.com/tidb-in-kubernetes/)                |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [組み込みの物理バックアップ](/br/backup-and-restore-use-cases.md)                             |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [グローバルキル](/sql-statements/sql-statement-kill.md)                                 |  よ  |  よ  |  よ  | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 |
| [ビューをロック](/information-schema/information-schema-data-lock-waits.md)             |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  | 実験的 | 実験的 | 実験的 |
| [`SHOW CONFIG`](/sql-statements/sql-statement-show-config.md)                    |  よ  |  よ  |  よ  |  よ  | よ   |  よ  |  よ  |  よ  |  よ  |  よ  |
| [`SET CONFIG`](/dynamic-config.md)                                               |  よ  |  よ  |  よ  | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 |
| [DM WebUI](/dm/dm-webui-guide.md)                                                | 実験的 | 実験的 | 実験的 | 実験的 | N   |  N  |  N  |  N  |  N  |  N  |
| [フォアグラウンド クォータ リミッター](/tikv-configuration-file.md#foreground-quota-limiter)      |  よ  |  よ  | 実験的 | 実験的 | N   |  N  |  N  |  N  |  N  |  N  |

[^1]: TiDB は、latin1 を utf8 のサブセットとして誤って扱います。詳細については、 [TiDB #18955](https://github.com/pingcap/tidb/issues/18955)を参照してください。

[^2]: サポートされている SQL ステートメントの完全なリストについては、 [ステートメント リファレンス](/sql-statements/sql-statement-select.md)を参照してください。

[^3]: TiDB v4.0 の場合、 `LOAD DATA`トランザクションは原子性を保証しません。
