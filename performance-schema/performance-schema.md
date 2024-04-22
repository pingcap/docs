---
title: Performance Schema
summary: TiDBはMySQLとの互換性のためにパフォーマンススキーマテーブルを実装しています。パフォーマンススキーマにはMySQLの互換性に関するテーブルとTiDB拡張機能であるテーブルが含まれています。MySQLの互換性に関するテーブルには様々なテーブルがありますが、TiDB拡張機能であるテーブルにも複数のテーブルが含まれています。
---

# パフォーマンススキーマ {#performance-schema}

TiDB は、MySQL との互換性のためにパフォーマンス スキーマ テーブルを実装しています。

## MySQL の互換性に関するテーブル {#tables-for-mysql-compatibility}

| テーブル名                                                                                      | 説明                |
| ------------------------------------------------------------------------------------------ | ----------------- |
| `events_stages_current`                                                                    |                   |
| `events_stages_history`                                                                    |                   |
| `events_stages_history_long`                                                               |                   |
| `events_statements_current`                                                                |                   |
| `events_statements_history`                                                                |                   |
| `events_statements_history_long`                                                           |                   |
| `events_statements_summary_by_digest`                                                      |                   |
| `events_transactions_current`                                                              |                   |
| `events_transactions_history`                                                              |                   |
| `events_transactions_history_long`                                                         |                   |
| `global_status`                                                                            |                   |
| `prepared_statements_instances`                                                            |                   |
| [`session_connect_attrs`](/performance-schema/performance-schema-session-connect-attrs.md) | セッションの接続属性を提供します。 |
| `session_status`                                                                           |                   |
| `session_variables`                                                                        |                   |
| `setup_actors`                                                                             |                   |
| `setup_consumers`                                                                          |                   |
| `setup_instruments`                                                                        |                   |
| `setup_objects`                                                                            |                   |

## TiDB 拡張機能であるテーブル {#tables-that-are-tidb-extensions}

| テーブル名                     | 説明 |
| ------------------------- | -- |
| `pd_profile_allocs`       |    |
| `pd_profile_block`        |    |
| `pd_profile_cpu`          |    |
| `pd_profile_goroutines`   |    |
| `pd_profile_memory`       |    |
| `pd_profile_mutex`        |    |
| `tidb_profile_allocs`     |    |
| `tidb_profile_block`      |    |
| `tidb_profile_cpu`        |    |
| `tidb_profile_goroutines` |    |
| `tidb_profile_memory`     |    |
| `tidb_profile_mutex`      |    |
| `tikv_profile_cpu`        |    |
