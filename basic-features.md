---
title: TiDB Features
summary: Learn about the basic features of TiDB.
---

# TiDBの機能 {#tidb-features}

このドキュメントには、各TiDBバージョンでサポートされている機能がリストされています。実験的機能のサポートは、最終リリースの前に変更される可能性があることに注意してください。

## データ型、関数、および演算子 {#data-types-functions-and-operators}

| データ型、関数、および演算子                                                                 | 6.1 | 6.0 | 5.4 | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 4.0 |
| ------------------------------------------------------------------------------ | :-: | :-: | --- | :-: | :-: | :-: | :-: | :-----: |
| [数値タイプ](/data-type-numeric.md)                                                 |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [日付と時刻のタイプ](/data-type-date-and-time.md)                                       |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [文字列型](/data-type-string.md)                                                   |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [JSONタイプ](/data-type-json.md)                                                  | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 |   実験的   |
| [制御フロー関数](/functions-and-operators/control-flow-functions.md)                  |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [文字列関数](/functions-and-operators/string-functions.md)                          |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [数値関数と演算子](/functions-and-operators/numeric-functions-and-operators.md)        |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [日付と時刻の関数](/functions-and-operators/date-and-time-functions.md)                |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [ビット関数と演算子](/functions-and-operators/bit-functions-and-operators.md)           |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [キャスト関数と演算子](/functions-and-operators/cast-functions-and-operators.md)         |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [暗号化および圧縮関数](/functions-and-operators/encryption-and-compression-functions.md) |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [情報関数](/functions-and-operators/information-functions.md)                      |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [JSON関数](/functions-and-operators/json-functions.md)                           | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 |   実験的   |
| [集計関数](/functions-and-operators/aggregate-group-by-functions.md)               |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [ウィンドウ関数](/functions-and-operators/window-functions.md)                        |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [その他の関数](/functions-and-operators/miscellaneous-functions.md)                  |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [演算子](/functions-and-operators/operators.md)                                   |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [^1] [文字セットと照合](/character-set-and-collation.md)                               |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [ユーザーレベルのロック](/functions-and-operators/locking-functions.md)                   |  Y  |  N  | N   |  N  |  N  |  N  |  N  |    N    |

## 索引付けと制約 {#indexing-and-constraints}

| 索引付けと制約                                                                   | 6.1 | 6.0 | 5.4 | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 4.0 |
| ------------------------------------------------------------------------- | :-: | :-: | --- | :-: | :-: | :-: | :-: | :-----: |
| [式インデックス](/sql-statements/sql-statement-create-index.md#expression-index) | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 |   実験的   |
| [列型ストレージ（TiFlash）](/tiflash/tiflash-overview.md)                          |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [RocksDBエンジン](/storage-engine/rocksdb-overview.md)                        |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [Titanプラグイン](/storage-engine/titan-overview.md)                           |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [見えないインデックス](/sql-statements/sql-statement-add-index.md)                  |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    N    |
| [複合`PRIMARY KEY`](/constraints.md)                                        |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [一意のインデックス](/constraints.md)                                              |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [整数の`PRIMARY KEY`のクラスター化インデックス](/constraints.md)                          |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [複合キーまたは非整数キーのクラスター化されたインデックス](/constraints.md)                           |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    N    |

## SQLステートメント {#sql-statements}

| SQLステートメント[^2]                                                                     | 6.1 | 6.0 | 5.4 | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 4.0 |
| ---------------------------------------------------------------------------------- | :-: | :-: | --- | :-: | :-: | :-: | :-: | :-----: |
| `REPLACE` `SELECT` `INSERT` `UPDATE` `DELETE`                                      |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| `INSERT ON DUPLICATE KEY UPDATE`                                                   |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| `LOAD DATA INFILE`                                                                 |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| `SELECT INTO OUTFILE`                                                              |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| `INNER JOIN` `LEFT\|RIGHT [OUTER] JOIN`                                            |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| `UNION` `UNION ALL`                                                                |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [`EXCEPT`および<code>INTERSECT</code>演算子](/functions-and-operators/set-operators.md)  |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    N    |
| `GROUP BY` `ORDER BY`                                                              |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [ウィンドウ関数](/functions-and-operators/window-functions.md)                            |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [共通テーブル式（CTE）](/sql-statements/sql-statement-with.md)                              |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  N  |    N    |
| `START TRANSACTION` `COMMIT` `ROLLBACK`                                            |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [`EXPLAIN`](/sql-statements/sql-statement-explain.md)                              |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)              |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [ユーザー定義変数](/user-defined-variables.md)                                             | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 |   実験的   |
| [`BATCH [ON COLUMN] LIMIT INTEGER DELETE`](/sql-statements/sql-statement-batch.md) |  Y  |  N  | N   |  N  |  N  |  N  |  N  |    N    |

## 高度なSQL機能 {#advanced-sql-features}

| 高度なSQL機能                                              | 6.1 | 6.0 | 5.4 | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 4.0 |
| ----------------------------------------------------- | :-: | :-: | --- | :-: | :-: | :-: | :-: | :-----: |
| [プリペアドステートメントキャッシュ](/sql-prepared-plan-cache.md)      |  Y  |  Y  | Y   |  Y  | 実験的 | 実験的 | 実験的 |   実験的   |
| [SQL計画管理（SPM）](/sql-plan-management.md)               |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [コプロセッサーキャッシュ](/coprocessor-cache.md)                 |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |   実験的   |
| [古い読み取り](/stale-read.md)                              |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  N  |    N    |
| [フォロワーの読み取り](/follower-read.md)                       |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [履歴データの読み取り（tidb_snapshot）](/read-historical-data.md) |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [オプティマイザーのヒント](/optimizer-hints.md)                   |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [MPP実行エンジン](/explain-mpp.md)                          |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    N    |
| [インデックスマージ](/explain-index-merge.md)                  |  Y  |  Y  | Y   | 実験的 | 実験的 | 実験的 | 実験的 |   実験的   |
| [SQLの配置ルール](/placement-rules-in-sql.md)               |  Y  |  Y  | 実験的 | 実験的 |  N  |  N  |  N  |    N    |

## データ定義言語（DDL） {#data-definition-language-ddl}

| データ定義言語（DDL）                                                    | 6.1 | 6.0 | 5.4 | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 4.0 |
| --------------------------------------------------------------- | :-: | :-: | --- | :-: | :-: | :-: | :-: | :-----: |
| `TRUNCATE` `CREATE` `DROP` `ALTER` `RENAME`                     |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [生成された列](/generated-columns.md)                                 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 |   実験的   |
| [ビュー](/views.md)                                                |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [シーケンス](/sql-statements/sql-statement-create-sequence.md)       |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [自動増加](/auto-increment.md)                                      |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [自動ランダム](/auto-random.md)                                       |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [DDLアルゴリズムアサーション](/sql-statements/sql-statement-alter-table.md) |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| マルチスキーマの変更：列を追加                                                 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 |   実験的   |
| [列タイプを変更する](/sql-statements/sql-statement-modify-column.md)     |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  N  |    N    |
| [一時テーブル](/temporary-tables.md)                                  |  Y  |  Y  | Y   |  Y  |  N  |  N  |  N  |    N    |

## トランザクション {#transactions}

| トランザクション                                                              | 6.1 | 6.0 | 5.4 | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 4.0 |
| --------------------------------------------------------------------- | :-: | :-- | --- | :-: | :-: | :-: | :-: | :-----: |
| [非同期コミット](/system-variables.md#tidb_enable_async_commit-new-in-v50)   |  Y  | Y   | Y   |  Y  |  Y  |  Y  |  Y  |    N    |
| [1個](/system-variables.md#tidb_enable_1pc-new-in-v50)                 |  Y  | Y   | Y   |  Y  |  Y  |  Y  |  Y  |    N    |
| [大規模なトランザクション（10GB）](/transaction-overview.md#transaction-size-limit) |  Y  | Y   | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [悲観的なトランザクション](/pessimistic-transaction.md)                           |  Y  | Y   | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [楽観的な取引](/optimistic-transaction.md)                                  |  Y  | Y   | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [繰り返し可能-読み取り分離（スナップショット分離）](/transaction-isolation-levels.md)         |  Y  | Y   | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [読み取り-コミットされた分離](/transaction-isolation-levels.md)                    |  Y  | Y   | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |

## パーティショニング {#partitioning}

| パーティショニング                                          | 6.1 | 6.0 | 5.4 | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 4.0 |
| -------------------------------------------------- | :-: | :-: | --- | :-: | :-: | :-: | :-: | :-----: |
| [範囲分割](/partitioned-table.md)                      |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [ハッシュ分割](/partitioned-table.md)                    |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [List パーティショニング](/partitioned-table.md)            |  Y  | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 |    N    |
| [List COLUMNS パーティショニング](/partitioned-table.md)    |  Y  | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 |    N    |
| [`EXCHANGE PARTITION`](/partitioned-table.md)      | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 |    N    |
| [動的剪定](/partitioned-table.md#dynamic-pruning-mode) |  Y  | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 |  N  |    N    |

## 統計 {#statistics}

| 統計                                                    |    6.1    |    6.0    | 5.4       |    5.3    | 5.2 | 5.1 | 5.0 | 4.0 4.0 |
| ----------------------------------------------------- | :-------: | :-------: | --------- | :-------: | :-: | :-: | :-: | :-----: |
| [CMSketch](/statistics.md)                            | デフォルトでは無効 | デフォルトでは無効 | デフォルトでは無効 | デフォルトでは無効 |  Y  |  Y  |  Y  |    Y    |
| [ヒストグラム](/statistics.md)                              |     Y     |     Y     | Y         |     Y     |  Y  |  Y  |  Y  |    Y    |
| [拡張統計（複数の列）](/statistics.md)                          |    実験的    |    実験的    | 実験的       |    実験的    | 実験的 | 実験的 | 実験的 |    N    |
| [統計フィードバック](/statistics.md#automatic-update)          |    非推奨    |    非推奨    | 非推奨       |    実験的    | 実験的 | 実験的 | 実験的 |   実験的   |
| [統計を自動的に更新する](/statistics.md#automatic-update)        |     Y     |     Y     | Y         |     Y     |  Y  |  Y  |  Y  |    Y    |
| [高速分析](/system-variables.md#tidb_enable_fast_analyze) |    実験的    |    実験的    | 実験的       |    実験的    | 実験的 | 実験的 | 実験的 |   実験的   |
| [動的剪定](/partitioned-table.md#dynamic-pruning-mode)    |     Y     |    実験的    | 実験的       |    実験的    | 実験的 | 実験的 |  N  |    N    |

## 安全 {#security}

| 安全                                                                     | 6.1 | 6.0 | 5.4 | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 4.0 |
| ---------------------------------------------------------------------- | :-: | :-: | --- | :-: | :-: | :-: | :-: | :-----: |
| [トランスペアレントレイヤーセキュリティ（TLS）](/enable-tls-between-clients-and-servers.md) |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [保管時の暗号化（TDE）](/encryption-at-rest.md)                                 |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [役割ベースの認証（RBAC）](/role-based-access-control.md)                        |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [証明書ベースの認証](/certificate-authentication.md)                            |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| `caching_sha2_password`認証                                              |  Y  |  Y  | Y   |  Y  |  Y  |  N  |  N  |    N    |
| [MySQL互換`GRANT`システム](/privilege-management.md)                         |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [動的権限](/privilege-management.md#dynamic-privileges)                    |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  N  |    N    |
| [セキュリティ強化モード](/system-variables.md#tidb_enable_enhanced_security)      |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  N  |    N    |
| [編集されたログファイル](/log-redaction.md)                                       |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    N    |

## データのインポートとエクスポート {#data-import-and-export}

| データのインポートとエクスポート                                                            | 6.1 | 6.0 | 5.4 | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 4.0 |
| --------------------------------------------------------------------------- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-----: |
| [Fast Importer（TiDB Lightning）](/tidb-lightning/tidb-lightning-overview.md) |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |    Y    |
| mydumper論理ダンパー                                                              | 非推奨 | 非推奨 | 非推奨 | 非推奨 | 非推奨 | 非推奨 | 非推奨 |   非推奨   |
| [Dumpling論理ダンパー](/dumpling-overview.md)                                     |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |    Y    |
| [トランザクション`LOAD DATA`](/sql-statements/sql-statement-load-data.md)           |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  N [^3] |
| [データベース移行ツールキット（DM）](/migration-overview.md)                                |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |    Y    |
| [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md)                         |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |    Y    |
| [変更データキャプチャ（CDC）](/ticdc/ticdc-overview.md)                                 |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |  Y  |    Y    |

## 管理、可観測性、およびツール {#management-observability-and-tools}

| 管理、可観測性、およびツール                                                                | 6.1 | 6.0 | 5.4 | 5.3 | 5.2 | 5.1 | 5.0 | 4.0 4.0 |
| ----------------------------------------------------------------------------- | :-: | :-: | --- | :-: | :-: | :-: | :-: | :-----: |
| [TiDBダッシュボードUI](/dashboard/dashboard-intro.md)                                |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [TiDBダッシュボードの継続的なプロファイリング](/dashboard/continuous-profiling.md)                |  Y  |  Y  | 実験的 | 実験的 |  N  |  N  |  N  |    N    |
| [TiDBダッシュボードTop SQL](/dashboard/top-sql.md)                                   |  Y  |  Y  | 実験的 |  N  |  N  |  N  |  N  |    N    |
| [TiDBダッシュボードSQL診断](/information-schema/information-schema-sql-diagnostics.md) | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 |   実験的   |
| [情報スキーマ](/information-schema/information-schema.md)                           |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [メトリクススキーマ](/metrics-schema.md)                                               |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [ステートメント要約表](/statement-summary-tables.md)                                    |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [遅いクエリログ](/identify-slow-queries.md)                                          |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [TiUPの展開](/tiup/tiup-overview.md)                                             |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| Ansibleデプロイメント                                                                |  N  |  N  | N   |  N  |  N  |  N  |  N  |   非推奨   |
| [Kubernetesオペレーター](https://docs.pingcap.com/tidb-in-kubernetes/)              |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [組み込みの物理バックアップ](/br/backup-and-restore-use-cases.md)                          |  Y  |  Y  | Y   |  Y  |  Y  |  Y  |  Y  |    Y    |
| [グローバルキル](/sql-statements/sql-statement-kill.md)                              |  Y  | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 |   実験的   |
| [ビューをロックする](/information-schema/information-schema-data-lock-waits.md)        |  Y  |  Y  | Y   |  Y  |  Y  | 実験的 | 実験的 |   実験的   |
| [`SHOW CONFIG`](/sql-statements/sql-statement-show-config.md)                 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 |   実験的   |
| [`SET CONFIG`](/dynamic-config.md)                                            |  Y  | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 | 実験的 |   実験的   |
| [DM WebUI](/dm/dm-webui-guide.md)                                             | 実験的 | 実験的 | N   |  N  |  N  |  N  |  N  |    N    |

[^1]: TiDBは、latin1をutf8のサブセットとして誤って扱います。詳細については、 [TiDB＃18955](https://github.com/pingcap/tidb/issues/18955)を参照してください。

[^2]: サポートされているSQLステートメントの完全なリストについては、 [ステートメントリファレンス](/sql-statements/sql-statement-select.md)を参照してください。

[^3]: TiDB v4.0の場合、 `LOAD DATA`トランザクションはアトミック性を保証しません。
