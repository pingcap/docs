---
title: TiDB Features
summary: Learn about the basic features of TiDB.
---

# TiDB の機能 {#tidb-features}

このドキュメントでは、TiDB の各バージョンでサポートされている機能を一覧表示しています。実験的機能のサポートは、最終リリースの前に変更される可能性があることに注意してください。

## データ型、関数、および演算子 {#data-types-functions-and-operators}

| データ型、関数、および演算子                                                                 | **5.4**      |      5.3     |      5.2     |      5.1     |      5.0     |      4.0     |
| ------------------------------------------------------------------------------ | ------------ | :----------: | :----------: | :----------: | :----------: | :----------: |
| [数値型](/data-type-numeric.md)                                                   | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [日付と時刻の種類](/data-type-date-and-time.md)                                        | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [文字列型](/data-type-string.md)                                                   | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [JSON タイプ](/data-type-json.md)                                                 | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |
| [制御フロー関数](/functions-and-operators/control-flow-functions.md)                  | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [文字列関数](/functions-and-operators/string-functions.md)                          | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [数値関数と演算子](/functions-and-operators/numeric-functions-and-operators.md)        | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [日付と時刻関数](/functions-and-operators/date-and-time-functions.md)                 | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [ビット関数と演算子](/functions-and-operators/bit-functions-and-operators.md)           | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [キャスト関数と演算子](/functions-and-operators/cast-functions-and-operators.md)         | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [暗号化および圧縮関数](/functions-and-operators/encryption-and-compression-functions.md) | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [情報関数](/functions-and-operators/information-functions.md)                      | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [JSON関数](/functions-and-operators/json-functions.md)                           | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |
| [集計関数](/functions-and-operators/aggregate-group-by-functions.md)               | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [ウィンドウ関数](/functions-and-operators/window-functions.md)                        | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [その他の関数](/functions-and-operators/miscellaneous-functions.md)                  | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [オペレーター](/functions-and-operators/operators.md)                                | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [文字セットと照合](/character-set-and-collation.md) [^1]                               | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |

## 索引付けと制約 {#indexing-and-constraints}

| 索引付けと制約                                                                    | **5.4**      |    **5.3**   |    **5.2**   |    **5.1**   |    **5.0**   |    **4.0**   |
| -------------------------------------------------------------------------- | ------------ | :----------: | :----------: | :----------: | :----------: | :----------: |
| [発現インデックス](/sql-statements/sql-statement-create-index.md#expression-index) | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |
| [カラム型ストレージ (TiFlash)](/tiflash/tiflash-overview.md)                        | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [RocksDB エンジン](/storage-engine/rocksdb-overview.md)                        | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [タイタンプラグイン](/storage-engine/titan-overview.md)                             | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [見えないインデックス](/sql-statements/sql-statement-add-index.md)                   | Y            |       Y      |       Y      |       Y      |       Y      |       N      |
| [複合`PRIMARY KEY`](/constraints.md)                                         | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [一意のインデックス](/constraints.md)                                               | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [整数`PRIMARY KEY`のクラスター化インデックス](/constraints.md)                            | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [複合キーまたは非整数キーのクラスター化インデックス](/constraints.md)                               | Y            |       Y      |       Y      |       Y      |       Y      |       N      |

## SQL ステートメント {#sql-statements}

| **SQL ステートメント**[^2]                                                               | **5.4**      |    **5.3**   |    **5.2**   |    **5.1**   |    **5.0**   |    **4.0**   |
| --------------------------------------------------------------------------------- | ------------ | :----------: | :----------: | :----------: | :----------: | :----------: |
| 基本`SELECT` 、 `INSERT` 、 `UPDATE` 、 `DELETE` 、 `REPLACE`                           | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| `INSERT ON DUPLICATE KEY UPDATE`                                                  | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| `LOAD DATA INFILE`                                                                | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| `SELECT INTO OUTFILE`                                                             | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| `INNER JOIN` , `LEFT|RIGHT [OUTER] JOIN`                                          | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| `UNION` , `UNION ALL`                                                             | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [`EXCEPT`および<code>INTERSECT</code>演算子](/functions-and-operators/set-operators.md) | Y            |       Y      |       Y      |       Y      |       Y      |       N      |
| `GROUP BY` , `ORDER BY`                                                           | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [ウィンドウ関数](/functions-and-operators/window-functions.md)                           | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [共通テーブル式 (CTE)](/sql-statements/sql-statement-with.md)                            | Y            |       Y      |       Y      |       Y      |       N      |       N      |
| `START TRANSACTION` 、 `COMMIT` 、 `ROLLBACK`                                       | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [`EXPLAIN`](/sql-statements/sql-statement-explain.md)                             | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)             | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [ユーザー定義変数](/user-defined-variables.md)                                            | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |
| [テーブルロック](/sql-statements/sql-statement-lock-tables-and-unlock-tables.md)         | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |

## 高度な SQL 機能 {#advanced-sql-features}

| **高度な SQL 機能**                                         | **5.4**      |    **5.3**   |    **5.2**   |    **5.1**   |    **5.0**   |    **4.0**   |
| ------------------------------------------------------ | ------------ | :----------: | :----------: | :----------: | :----------: | :----------: |
| [プリペアド ステートメント キャッシュ](/sql-prepared-plan-cache.md)     | Y            |       Y      | Experimental | Experimental | Experimental | Experimental |
| [SQL 計画管理 (SPM)](/sql-plan-management.md)              | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [コプロセッサー・キャッシュ](/coprocessor-cache.md)                 | Y            |       Y      |       Y      |       Y      |       Y      | Experimental |
| [ステイル読み取り](/stale-read.md)                             | Y            |       Y      |       Y      |       Y      |       N      |       N      |
| [Followerが読む](/follower-read.md)                       | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [履歴データの読み取り (tidb_snapshot)](/read-historical-data.md) | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [オプティマイザーのヒント](/optimizer-hints.md)                    | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [MPP 実行エンジン](/explain-mpp.md)                          | Y            |       Y      |       Y      |       Y      |       Y      |       N      |
| [インデックス マージ](/explain-index-merge.md)                  | Y            | Experimental | Experimental | Experimental | Experimental | Experimental |
| [SQL の配置規則](/placement-rules-in-sql.md)                | Experimental | Experimental |       N      |       N      |       N      |       N      |

## データ定義言語 (DDL) {#data-definition-language-ddl}

| **データ定義言語 (DDL)**                                                        | **5.4**      |    **5.3**   |    **5.2**   |    **5.1**   |    **5.0**   |    **4.0**   |
| ------------------------------------------------------------------------ | ------------ | :----------: | :----------: | :----------: | :----------: | :----------: |
| 基本`CREATE` 、 `DROP` 、 `ALTER` 、 `RENAME` 、 `TRUNCATE`                    | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [生成された列](/generated-columns.md)                                          | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |
| [ビュー](/views.md)                                                         | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [シーケンス](/sql-statements/sql-statement-create-sequence.md)                | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [自動増加](/auto-increment.md)                                               | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [オートランダム](/auto-random.md)                                               | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [DDL アルゴリズム アサーション](/sql-statements/sql-statement-alter-table.md)        | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [マルチスキーマの変更: 列を追加](/system-variables.md#tidb_enable_change_multi_schema) | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |
| [列の種類を変更する](/sql-statements/sql-statement-modify-column.md)              | Y            |       Y      |       Y      |       Y      |       N      |       N      |
| [一時テーブル](/temporary-tables.md)                                           | Y            |       Y      |       N      |       N      |       N      |       N      |

## 取引 {#transactions}

| **取引**                                                                | **5.4** | **5.3** | **5.2** | **5.1** | **5.0** | **4.0** |
| --------------------------------------------------------------------- | ------- | :-----: | :-----: | :-----: | :-----: | :-----: |
| [非同期コミット](/system-variables.md#tidb_enable_async_commit-new-in-v50)   | Y       |    Y    |    Y    |    Y    |    Y    |    N    |
| [1個](/system-variables.md#tidb_enable_1pc-new-in-v50)                 | Y       |    Y    |    Y    |    Y    |    Y    |    N    |
| [大規模トランザクション (10GB)](/transaction-overview.md#transaction-size-limit) | Y       |    Y    |    Y    |    Y    |    Y    |    Y    |
| [悲観的な取引](/pessimistic-transaction.md)                                 | Y       |    Y    |    Y    |    Y    |    Y    |    Y    |
| [楽観的な取引](/optimistic-transaction.md)                                  | Y       |    Y    |    Y    |    Y    |    Y    |    Y    |
| [反復可能読み取り分離 (スナップショット分離)](/transaction-isolation-levels.md)           | Y       |    Y    |    Y    |    Y    |    Y    |    Y    |
| [読み取りコミット分離](/transaction-isolation-levels.md)                        | Y       |    Y    |    Y    |    Y    |    Y    |    Y    |

## パーティショニング {#partitioning}

| **パーティショニング**                                      | **5.4**      |    **5.3**   |    **5.2**   |    **5.1**   |    **5.0**   | **4.0** |
| -------------------------------------------------- | ------------ | :----------: | :----------: | :----------: | :----------: | :-----: |
| [範囲分割](/partitioned-table.md)                      | Y            |       Y      |       Y      |       Y      |       Y      |    Y    |
| [ハッシュパーティショニング](/partitioned-table.md)             | Y            |       Y      |       Y      |       Y      |       Y      |    Y    |
| [List パーティショニング](/partitioned-table.md)            | Experimental | Experimental | Experimental | Experimental | Experimental |    N    |
| [List COLUMNS パーティショニング](/partitioned-table.md)    | Experimental | Experimental | Experimental | Experimental | Experimental |    N    |
| [`EXCHANGE PARTITION`](/partitioned-table.md)      | Experimental | Experimental | Experimental | Experimental | Experimental |    N    |
| [動的剪定](/partitioned-table.md#dynamic-pruning-mode) | Experimental | Experimental | Experimental | Experimental |       N      |    N    |

## 統計 {#statistics}

| **統計**                                                | **5.4**      |    **5.3**   |    **5.2**   |    **5.1**   |    **5.0**   |    **4.0**   |
| ----------------------------------------------------- | ------------ | :----------: | :----------: | :----------: | :----------: | :----------: |
| [CMSketch](/statistics.md)                            | 非推奨          |      非推奨     |      非推奨     |      非推奨     |      非推奨     |       Y      |
| [ヒストグラム](/statistics.md)                              | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| 拡張統計 (複数列)                                            | Experimental | Experimental | Experimental | Experimental | Experimental |       N      |
| [統計フィードバック](/statistics.md#automatic-update)          | 非推奨          | Experimental | Experimental | Experimental | Experimental | Experimental |
| [高速分析](/system-variables.md#tidb_enable_fast_analyze) | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |

## 安全 {#security}

| **安全**                                                            | **5.4** | **5.3** | **5.2** | **5.1** | **5.0** | **4.0** |
| ----------------------------------------------------------------- | ------- | :-----: | :-----: | :-----: | :-----: | :-----: |
| [透過レイヤーセキュリティ (TLS)](/enable-tls-between-clients-and-servers.md)  | Y       |    Y    |    Y    |    Y    |    Y    |    Y    |
| [保存時の暗号化 (TDE)](/encryption-at-rest.md)                           | Y       |    Y    |    Y    |    Y    |    Y    |    Y    |
| [役割ベースの認証 (RBAC)](/role-based-access-control.md)                  | Y       |    Y    |    Y    |    Y    |    Y    |    Y    |
| [証明書ベースの認証](/certificate-authentication.md)                       | Y       |    Y    |    Y    |    Y    |    Y    |    Y    |
| `caching_sha2_password`認証                                         | Y       |    Y    |    Y    |    N    |    N    |    N    |
| [MySQL 互換の`GRANT`システム](/privilege-management.md)                  | Y       |    Y    |    Y    |    Y    |    Y    |    Y    |
| [動的権限](/privilege-management.md#dynamic-privileges)               | Y       |    Y    |    Y    |    Y    |    N    |    N    |
| [セキュリティ強化モード](/system-variables.md#tidb_enable_enhanced_security) | Y       |    Y    |    Y    |    Y    |    N    |    N    |
| [編集されたログ ファイル](/log-redaction.md)                                 | Y       |    Y    |    Y    |    Y    |    Y    |    N    |

## データのインポートとエクスポート {#data-import-and-export}

| **データのインポートとエクスポート**                                                    | **5.4** | **5.3** | **5.2** | **5.1** | **5.0** | **4.0** |
| ----------------------------------------------------------------------- | :-----: | :-----: | :-----: | :-----: | :-----: | :-----: |
| [高速インポーター (TiDB Lightning)](/tidb-lightning/tidb-lightning-overview.md) |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |
| mydumper 論理ダンパー                                                         |   非推奨   |   非推奨   |   非推奨   |   非推奨   |   非推奨   |   非推奨   |
| [Dumpling論理ダンパー](/dumpling-overview.md)                                 |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |
| [トランザクション`LOAD DATA`](/sql-statements/sql-statement-load-data.md)       |    Y    |    Y    |    Y    |    Y    |    Y    |  N [^3] |
| [データベース移行ツールキット (DM)](/migration-overview.md)                           |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |
| [TiDBBinlog](/tidb-binlog/tidb-binlog-overview.md)                      |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |
| [変更データ キャプチャ (CDC)](/ticdc/ticdc-overview.md)                           |    Y    |    Y    |    Y    |    Y    |    Y    |    Y    |

## 管理、可観測性、およびツール {#management-observability-and-tools}

| **管理、可観測性、およびツール**                                                   | **5.4**      |    **5.3**   |    **5.2**   |    **5.1**   |    **5.0**   |    **4.0**   |
| -------------------------------------------------------------------- | ------------ | :----------: | :----------: | :----------: | :----------: | :----------: |
| [TiDB ダッシュボード](/dashboard/dashboard-intro.md)                        | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [SQL 診断](/information-schema/information-schema-sql-diagnostics.md)  | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |
| [情報スキーマ](/information-schema/information-schema.md)                  | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [指標スキーマ](/metrics-schema.md)                                         | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [ステートメント要約表](/statement-summary-tables.md)                           | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [スロー クエリ ログ](/identify-slow-queries.md)                              | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [TiUP展開](/tiup/tiup-overview.md)                                     | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| アンシブル展開                                                              | N            |       N      |       N      |       N      |       N      |      非推奨     |
| [Kubernetes オペレーター](https://docs.pingcap.com/tidb-in-kubernetes/)    | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [組み込みの物理バックアップ](/br/backup-and-restore-use-cases.md)                 | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [グローバルキル](/sql-statements/sql-statement-kill.md)                     | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |
| [ビューをロック](/information-schema/information-schema-data-lock-waits.md) | Y            |       Y      |       Y      | Experimental | Experimental | Experimental |
| [`SHOW CONFIG`](/sql-statements/sql-statement-show-config.md)        | Y            |       Y      |       Y      |       Y      |       Y      |       Y      |
| [`SET CONFIG`](/dynamic-config.md)                                   | Experimental | Experimental | Experimental | Experimental | Experimental | Experimental |
| [継続的なプロファイリング](/dashboard/continuous-profiling.md)                   | Experimental | Experimental |       N      |       N      |       N      |       N      |
| [Top SQL](/dashboard/top-sql.md)                                     | Experimental |       N      |       N      |       N      |       N      |       N      |

[^1]: TiDB は、latin1 を utf8 のサブセットとして誤って扱います。詳細については[TiDB #18955](https://github.com/pingcap/tidb/issues/18955)参照してください。

[^2]: サポートされている SQL ステートメントの完全なリストについては、 [ステートメント リファレンス](/sql-statements/sql-statement-select.md)を参照してください。

[^3]: TiDB v4.0 の場合、 `LOAD DATA`トランザクションは原子性を保証しません。
