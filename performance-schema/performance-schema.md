---
title: Performance Schema
summary: TiDB は、システム メタデータを表示するための performance_schema を実装します。
---

# パフォーマンススキーマ {#performance-schema}

TiDB は、MySQL との互換性のためにパフォーマンス スキーマ テーブルを実装します。

## MySQL 互換性のためのテーブル {#tables-for-mysql-compatibility}

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

## TiDB拡張のテーブル {#tables-that-are-tidb-extensions}

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
