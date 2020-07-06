---
title: Information Schema
summary: TiDB implements the ANSI-standard information_schema for viewing system metadata.
category: reference
aliases: ['/docs/dev/information-schema/information-schema-information-schema/','/docs/dev/reference/system-databases/information-schema/']
---

# Information Schema

Information Schema provides an ANSI-standard way of viewing system metadata. TiDB also provides a number of custom `INFORMATION_SCHEMA` tables, in addition to the tables included for MySQL compatibility.

Many `INFORMATION_SCHEMA` tables have a corresponding `SHOW` command. The benefit of querying `INFORMATION_SCHEMA` is that it is possible to join between tables.

| Table Name                                                                              | TiDB Extension | Description |
|-----------------------------------------------------------------------------------------|----------------|-------------|
| [`ANALYZE_STATUS`](/information-schema/information-schema-analyze-status.md)            | Yes            | Provides information about tasks to collect statistics. |
| [`CHARACTER_SETS`](/information-schema/information-schema-character-sets.md)            | No             | Provides a list of character sets the server supports. |
| [`CLUSTER_CONFIG`](/information-schema/information-schema-cluster-config.md)            | Yes            | Provides details about configuration settings for the entire TiDB cluster. |
| [`CLUSTER_HARDWARE`](/information-schema/information-schema-cluster-info.md)            | Yes            | Provides details on the underlying physical hardware discovered on each TiDB component. |
| [`CLUSTER_INFO`](/information-schema/information-schema-cluster-info.md)                | Yes            | Provides details on the current cluster topology. |
| [`CLUSTER_LOAD`](/information-schema/information-schema-cluster-load.md)                | Yes            | Provides current load information for TiDB servers in the cluster. |
| [`CLUSTER_LOG`](/information-schema/information-schema-cluster-log.md)                  | Yes            | Provides a log for the entire TiDB cluster |
| `CLUSTER_PROCESSLIST`                                                                   | Yes            | Provides a cluster-level view of the `PROCESSLIST` table. |
| `CLUSTER_SLOW_QUERY`                                                                    | Yes            | Provides a cluster-level view of the `SLOW_QUERY` table. |
| `CLUSTER_STATEMENTS_SUMMARY`                                                            | Yes            | Provides a cluster-level view of the `STATEMENTS_SUMMARY` table. |
| `CLUSTER_STATEMENTS_SUMMARY_HISTORY`                                                    | Yes            | Provides a cluster-level view of the `CLUSTER_STATEMENTS_SUMMARY_HISTORY` table. |
| [`CLUSTER_SYSTEMINFO`](/information-schema/information-schema-cluster-systeminfo.md)    | Yes            | Provides details about kernel parameter configuration for servers in the cluster. |
| [`COLLATIONS`](/information-schema/information-schema-collations.md)                    | No             | Provides a list of collations that the server supports. |
| [`COLLATION_CHARACTER_SET_APPLICABILITY`](/information-schema/information-schema-collation-character-set-applicability.md) | No | Explains which collations apply to which character sets. |
| [`COLUMNS`](/information-schema/information-schema-columns.md)                          | No             | Provides a list of columns for all tables. |
| `COLUMN_PRIVILEGES`                                                                     | No             | Not implemented by TiDB. Returns zero rows. |
| `COLUMN_STATISTICS`                                                                     | No             | Not implemented by TiDB. Returns zero rows. |
| [`DDL_JOBS`](/information-schema/information-schema-ddl-jobs.md)                        | Yes            | Provides similar output to `ADMIN SHOW DDL JOBS` |
| [`ENGINES`](/information-schema/information-schema-engines.md)                          | No             | Provides a list of supported storage engines. |
| `EVENTS`                                                                                | No             | Not implemented by TiDB. Returns zero rows. |
| `FILES`                                                                                 | No             | Not implemented by TiDB. Returns zero rows. |
| `GLOBAL_STATUS`                                                                         | No             | Not implemented by TiDB. Returns zero rows. |
| `GLOBAL_VARIABLES`                                                                      | No             | Not implemented by TiDB. Returns zero rows. |
| [`INSPECTION_RESULT`](/information-schema/information-schema-inspection-result.md)      | Yes            | Triggers internal diagnostics checks. |
| [`INSPECTION_RULES`](/information-schema/information-schema-inspection-rules.md)        | Yes            | A list of internal diagnostic checks performed. |
| [`INSPECTION_SUMMARY`](/information-schema/information-schema-inspection-summary.md)    | Yes            | A summarized report of important monitoring metrics. |
| [`KEY_COLUMN_USAGE`](/information-schema/information-schema-key-column-usage.md)        | No             | Describes the key constraints of the columns, such as the primary key constraint. |
| [`METRICS_SUMMARY`](/information-schema/information-schema-metrics-summary.md)          | Yes            | A summary of metrics extracted from Prometheus. |
| `METRICS_SUMMARY_BY_LABEL`                                                              | Yes            | See `METRICS_SUMAMARY` table. |
| [`METRICS_TABLES`](/information-schema/information-schema-metrics-tables.md)            | Yes            | Provides the PromQL definitions for tables in `METRICS_SCHEMA`. |
| `OPTIMIZER_TRACE`                                                                       | No             | Not implemented by TiDB. Returns zero rows. |
| `PARAMETERS`                                                                            | No             | Not implemented by TiDB. Returns zero rows. |
| [`PARTITIONS`](/information-schema/information-schema-partitions.md)                    | No             | Provides a list of table partitions. |
| `PLUGINS`                                                                               | No             | Not implemented by TiDB. Returns zero rows. |
| [`PROCESSLIST`](/information-schema/information-schema-processlist.md)                  | No             | Provides similar information to the command `SHOW PROCESSLIST`. |
| `PROFILING`                                                                             | No             | Not implemented by TiDB. Returns zero rows. |
| `REFERENTIAL_CONSTRAINTS`                                                               | No             | Not implemented by TiDB. Returns zero rows. |
| `ROUTINES`                                                                              | No             | Not implemented by TiDB. Returns zero rows. |
| [`SCHEMATA`](/information-schema/information-schema-schemata.md)                        | No             | Provides similar information to `SHOW DATABASES`. |
| `SCHEMA_PRIVILEGES`                                                                     | No             | Not implemented by TiDB. Returns zero rows. |
| [`SEQUENCES`](/information-schema/information-schema-sequences.md)                      | Yes            | The TiDB implementation of sequences is based on MariaDB. |
| `SESSION_STATUS`                                                                        | No             | Not implemented by TiDB. Returns zero rows. |
| [`SESSION_VARIABLES`](/information-schema/information-schema-session-variables.md)      | No             | Provides similar functionality to the command `SHOW SESSION VARIABLES` |
| [`SLOW_QUERY`](/information-schema/information-schema-slow-query.md)                    | Yes            | Provides information on slow queries on the current TiDB server. |
| [`STATEMENTS_SUMMARY`](/statement-summary-tables.md)                                    | Yes            | Similar to performance_schema statement summary in MySQL. |
| [`STATEMENTS_SUMMARY_HISTORY`](/statement-summary-tables.md)                            | Yes            | Similar to performance_schema statement summary history in MySQL. |
| [`STATISTICS`](/information-schema/information-schema-statistics.md)                    | No             | Provides information on table indexes. |
| [`TABLES`](/information-schema/information-schema-tables.md)                            | No             | Provides a list of tables that the current user has visibility of. Similar to `SHOW TABLES`. |
| `TABLESPACES`                                                                           | No             | Not implemented by TiDB. Returns zero rows. |
| [`TABLE_CONSTRAINTS`](/information-schema/information-schema-table-constraints.md)      | No             | Provides information on primary keys, unique indexes and foreign keys. |
| `TABLE_PRIVILEGES`                                                                      | No             | Not implemented by TiDB. Returns zero rows. |
| [`TABLE_STORAGE_STATS`](/information-schema/information-schema-table-storage-stats.md)  | Yes            | Provides details about table sizes in storage. |
| [`TIDB_HOT_REGIONS`](/information-schema/information-schema-tidb-hot-regions.md)        | Yes            | Provides statistics about which regions are hot. |
| [`TIDB_INDEXES`](/information-schema/information-schema-tidb-indexes.md)                | Yes            | Provides index information about TiDB tables. |
| [`TIDB_SERVERS_INFO`](/information-schema/information-schema-tidb-servers-info.md)      | Yes            | Provides a list of TiDB servers (i.e. tidb-server component) |
| [`TIFLASH_REPLICA`](/information-schema/information-schema-tiflash-replica.md)          | Yes            | Provides details about TiFlash replicas. |
| [`TIKV_REGION_PEERS`](/information-schema/information-schema-tikv-region-peers.md)      | Yes            | Provides details about where regions are stored. |
| [`TIKV_REGION_STATUS`](/information-schema/information-schema-tikv-region-status.md)    | Yes            | Provides statistics about regions. |
| [`TIKV_STORE_STATUS`](/information-schema/information-schema-tikv-store-status.md)      | Yes            | Provides basic information about TiKV servers. |
| `TRIGGERS`                                                                              | No             | Not implemented by TiDB. Returns zero rows. |
| [`USER_PRIVILEGES`](/information-schema/information-schema-user-privileges.md)          | No             | Summarizes the privileges associated with the current user. |
| [`VIEWS`](/information-schema/information-schema-views.md)                              | No             | Provides a list of views that the current user has visibility of. Similar to running `SHOW FULL TABLES WHERE table_type = 'VIEW'` |
