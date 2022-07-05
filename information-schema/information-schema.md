---
title: Information Schema
summary: TiDB implements the ANSI-standard information_schema for viewing system metadata.
---

# 情報スキーマ {#information-schema}

情報スキーマは、システムメタデータを表示するANSI標準の方法を提供します。 TiDBは、MySQLとの互換性のために含まれているテーブルに加えて、いくつかのカスタム`INFORMATION_SCHEMA`テーブルも提供します。

多くの`INFORMATION_SCHEMA`テーブルには、対応する`SHOW`コマンドがあります。 `INFORMATION_SCHEMA`を照会する利点は、テーブル間で結合できることです。

## MySQL互換性のテーブル {#tables-for-mysql-compatibility}

| テーブル名                                                                                                                      | 説明                                                                                 |
| -------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| [`CHARACTER_SETS`](/information-schema/information-schema-character-sets.md)                                               | サーバーがサポートする文字セットのリストを提供します。                                                        |
| [`COLLATIONS`](/information-schema/information-schema-collations.md)                                                       | サーバーがサポートする照合のリストを提供します。                                                           |
| [`COLLATION_CHARACTER_SET_APPLICABILITY`](/information-schema/information-schema-collation-character-set-applicability.md) | どの照合がどの文字セットに適用されるかを説明します。                                                         |
| [`COLUMNS`](/information-schema/information-schema-columns.md)                                                             | すべてのテーブルの列のリストを提供します。                                                              |
| `COLUMN_PRIVILEGES`                                                                                                        | TiDBでは実装されていません。ゼロ行を返します。                                                          |
| `COLUMN_STATISTICS`                                                                                                        | TiDBでは実装されていません。ゼロ行を返します。                                                          |
| [`ENGINES`](/information-schema/information-schema-engines.md)                                                             | サポートされているストレージエンジンのリストを提供します。                                                      |
| `EVENTS`                                                                                                                   | TiDBでは実装されていません。ゼロ行を返します。                                                          |
| `FILES`                                                                                                                    | TiDBでは実装されていません。ゼロ行を返します。                                                          |
| `GLOBAL_STATUS`                                                                                                            | TiDBでは実装されていません。ゼロ行を返します。                                                          |
| `GLOBAL_VARIABLES`                                                                                                         | TiDBでは実装されていません。ゼロ行を返します。                                                          |
| [`KEY_COLUMN_USAGE`](/information-schema/information-schema-key-column-usage.md)                                           | 主キー制約など、列のキー制約について説明します。                                                           |
| `OPTIMIZER_TRACE`                                                                                                          | TiDBでは実装されていません。ゼロ行を返します。                                                          |
| `PARAMETERS`                                                                                                               | TiDBでは実装されていません。ゼロ行を返します。                                                          |
| [`PARTITIONS`](/information-schema/information-schema-partitions.md)                                                       | テーブルパーティションのリストを提供します。                                                             |
| `PLUGINS`                                                                                                                  | TiDBでは実装されていません。ゼロ行を返します。                                                          |
| [`PROCESSLIST`](/information-schema/information-schema-processlist.md)                                                     | コマンド`SHOW PROCESSLIST`と同様の情報を提供します。                                                |
| `PROFILING`                                                                                                                | TiDBでは実装されていません。ゼロ行を返します。                                                          |
| `REFERENTIAL_CONSTRAINTS`                                                                                                  | `FOREIGN KEY`の制約に関する情報を提供します。                                                      |
| `ROUTINES`                                                                                                                 | TiDBでは実装されていません。ゼロ行を返します。                                                          |
| [`SCHEMATA`](/information-schema/information-schema-schemata.md)                                                           | `SHOW DATABASES`と同様の情報を提供します。                                                      |
| `SCHEMA_PRIVILEGES`                                                                                                        | TiDBでは実装されていません。ゼロ行を返します。                                                          |
| `SESSION_STATUS`                                                                                                           | TiDBでは実装されていません。ゼロ行を返します。                                                          |
| [`SESSION_VARIABLES`](/information-schema/information-schema-session-variables.md)                                         | コマンド`SHOW SESSION VARIABLES`と同様の機能を提供します                                           |
| [`STATISTICS`](/information-schema/information-schema-statistics.md)                                                       | テーブルインデックスに関する情報を提供します。                                                            |
| [`TABLES`](/information-schema/information-schema-tables.md)                                                               | 現在のユーザーが表示できるテーブルのリストを提供します。 `SHOW TABLES`に似ています。                                  |
| `TABLESPACES`                                                                                                              | TiDBでは実装されていません。ゼロ行を返します。                                                          |
| [`TABLE_CONSTRAINTS`](/information-schema/information-schema-table-constraints.md)                                         | 主キー、一意のインデックス、および外部キーに関する情報を提供します。                                                 |
| `TABLE_PRIVILEGES`                                                                                                         | TiDBでは実装されていません。ゼロ行を返します。                                                          |
| `TRIGGERS`                                                                                                                 | TiDBでは実装されていません。ゼロ行を返します。                                                          |
| [`USER_PRIVILEGES`](/information-schema/information-schema-user-privileges.md)                                             | 現在のユーザーに関連付けられている特権を要約します。                                                         |
| [`VIEWS`](/information-schema/information-schema-views.md)                                                                 | 現在のユーザーが表示できるビューのリストを提供します。ランニング`SHOW FULL TABLES WHERE table_type = 'VIEW'`に似ています |

## TiDB拡張機能であるテーブル {#tables-that-are-tidb-extensions}

| テーブル名                                                                                              | 説明                                                                 |
| -------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| [`ANALYZE_STATUS`](/information-schema/information-schema-analyze-status.md)                       | 統計を収集するためのタスクに関する情報を提供します。                                         |
| [`CLIENT_ERRORS_SUMMARY_BY_HOST`](/information-schema/client-errors-summary-by-host.md)            | クライアント要求によって生成され、クライアントに返されるエラーと警告の要約を提供します。                       |
| [`CLIENT_ERRORS_SUMMARY_BY_USER`](/information-schema/client-errors-summary-by-user.md)            | クライアントによって生成されたエラーと警告の要約を提供します。                                    |
| [`CLIENT_ERRORS_SUMMARY_GLOBAL`](/information-schema/client-errors-summary-global.md)              | クライアントによって生成されたエラーと警告の要約を提供します。                                    |
| [`CLUSTER_CONFIG`](https://docs.pingcap.com/tidb/stable/information-schema-cluster-config)         | TiDBクラスタ全体の構成設定に関する詳細を提供します。この表はTiDB Cloudには適用されません。               |
| `CLUSTER_DEADLOCKS`                                                                                | `DEADLOCKS`のテーブルのクラスターレベルのビューを提供します。                               |
| [`CLUSTER_HARDWARE`](https://docs.pingcap.com/tidb/stable/information-schema-cluster-hardware)     | 各TiDBコンポーネントで検出された基盤となる物理ハードウェアの詳細を提供します。この表はTiDB Cloudには適用されません。  |
| [`CLUSTER_INFO`](/information-schema/information-schema-cluster-info.md)                           | 現在のクラスタトポロジの詳細を提供します。                                              |
| [`CLUSTER_LOAD`](https://docs.pingcap.com/tidb/stable/information-schema-cluster-load)             | クラスタのTiDBサーバーの現在の負荷情報を提供します。この表はTiDB Cloudには適用されません。               |
| [`CLUSTER_LOG`](https://docs.pingcap.com/tidb/stable/information-schema-cluster-log)               | TiDBクラスタ全体のログを提供します。この表はTiDB Cloudには適用されません。                       |
| `CLUSTER_PROCESSLIST`                                                                              | `PROCESSLIST`のテーブルのクラスターレベルのビューを提供します。                             |
| `CLUSTER_SLOW_QUERY`                                                                               | `SLOW_QUERY`のテーブルのクラスターレベルのビューを提供します。                              |
| `CLUSTER_STATEMENTS_SUMMARY`                                                                       | `STATEMENTS_SUMMARY`のテーブルのクラスターレベルのビューを提供します。                      |
| `CLUSTER_STATEMENTS_SUMMARY_HISTORY`                                                               | `STATEMENTS_SUMMARY_HISTORY`のテーブルのクラスターレベルのビューを提供します。              |
| `CLUSTER_TIDB_TRX`                                                                                 | `TIDB_TRX`のテーブルのクラスターレベルのビューを提供します。                                |
| [`CLUSTER_SYSTEMINFO`](https://docs.pingcap.com/tidb/stable/information-schema-cluster-systeminfo) | クラスタのサーバーのカーネルパラメータ構成に関する詳細を提供します。この表はTiDB Cloudには適用されません。         |
| [`DATA_LOCK_WAITS`](/information-schema/information-schema-data-lock-waits.md)                     | TiKVサーバーのロック待機情報を提供します。                                            |
| [`DDL_JOBS`](/information-schema/information-schema-ddl-jobs.md)                                   | `ADMIN SHOW DDL JOBS`と同様の出力を提供します                                  |
| [`DEADLOCKS`](/information-schema/information-schema-deadlocks.md)                                 | 最近発生したいくつかのデッドロックエラーの情報を提供します。                                     |
| [`INSPECTION_RESULT`](https://docs.pingcap.com/tidb/stable/information-schema-inspection-result)   | 内部診断チェックをトリガーします。この表はTiDB Cloudには適用されません。                          |
| [`INSPECTION_RULES`](https://docs.pingcap.com/tidb/stable/information-schema-inspection-rules)     | 実行された内部診断チェックのリスト。この表はTiDB Cloudには適用されません。                         |
| [`INSPECTION_SUMMARY`](https://docs.pingcap.com/tidb/stable/information-schema-inspection-summary) | 重要な監視メトリックの要約レポート。この表はTiDB Cloudには適用されません。                         |
| [`METRICS_SUMMARY`](https://docs.pingcap.com/tidb/stable/information-schema-metrics-summary)       | Prometheusから抽出されたメトリックの要約。この表はTiDB Cloudには適用されません。                 |
| `METRICS_SUMMARY_BY_LABEL`                                                                         | `METRICS_SUMMARY`の表を参照してください。                                      |
| [`METRICS_TABLES`](https://docs.pingcap.com/tidb/stable/information-schema-metrics-tables)         | `METRICS_SCHEMA`のテーブルのPromQL定義を提供します。この表はTiDB Cloudには適用されません。      |
| [`PLACEMENT_RULES`](https://docs.pingcap.com/tidb/stable/information-schema-placement-rules)       | 明示的な配置ルールが割り当てられているすべてのオブジェクトに関する情報を提供します。この表はTiDB Cloudには適用されません。 |
| [`SEQUENCES`](/information-schema/information-schema-sequences.md)                                 | シーケンスのTiDB実装は、MariaDBに基づいています。                                     |
| [`SLOW_QUERY`](/information-schema/information-schema-slow-query.md)                               | 現在のTiDBサーバーでの低速クエリに関する情報を提供します。                                    |
| [`STATEMENTS_SUMMARY`](/statement-summary-tables.md)                                               | MySQLのperformance_schemaステートメントの要約に似ています。                          |
| [`STATEMENTS_SUMMARY_HISTORY`](/statement-summary-tables.md)                                       | MySQLのperformance_schemaステートメントの要約履歴に似ています。                        |
| [`TABLE_STORAGE_STATS`](/information-schema/information-schema-table-storage-stats.md)             | ストレージ内のテーブルサイズに関する詳細を提供します。                                        |
| [`TIDB_HOT_REGIONS`](https://docs.pingcap.com/tidb/stable/information-schema-tidb-hot-regions)     | どの地域が暑いかについての統計を提供します。この表はTiDB Cloudには適用されません。                     |
| [`TIDB_HOT_REGIONS_HISTORY`](/information-schema/information-schema-tidb-hot-regions-history.md)   | どのリージョンがホットであるかに関する履歴統計を提供します。                                     |
| [`TIDB_INDEXES`](/information-schema/information-schema-tidb-indexes.md)                           | TiDBテーブルに関するインデックス情報を提供します。                                        |
| [`TIDB_SERVERS_INFO`](/information-schema/information-schema-tidb-servers-info.md)                 | TiDBサーバー（つまり、tidb-serverコンポーネント）のリストを提供します                         |
| [`TIDB_TRX`](/information-schema/information-schema-tidb-trx.md)                                   | TiDBノードで実行されているトランザクションの情報を提供します。                                  |
| [`TIFLASH_REPLICA`](/information-schema/information-schema-tiflash-replica.md)                     | TiFlashレプリカに関する詳細を提供します。                                           |
| [`TIKV_REGION_PEERS`](/information-schema/information-schema-tikv-region-peers.md)                 | リージョンが保存されている場所に関する詳細を提供します。                                       |
| [`TIKV_REGION_STATUS`](/information-schema/information-schema-tikv-region-status.md)               | 地域に関する統計を提供します。                                                    |
| [`TIKV_STORE_STATUS`](/information-schema/information-schema-tikv-store-status.md)                 | TiKVサーバーに関する基本情報を提供します。                                            |
