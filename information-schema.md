---
title: Information Schema
summary: TiDB implements the ANSI-standard information_schema for viewing system metadata.
category: reference
aliases: ['/docs/dev/system-tables/system-table-information-schema/','/docs/dev/reference/system-databases/information-schema/']
---

# Information Schema

Information Schema provides an ANSI-standard way of viewing system metadata. TiDB also provides a number of custom `INFORMATION_SCHEMA` tables, in addition to the tables included for MySQL compatibility.

Many `INFORMATION_SCHEMA` tables have a corresponding `SHOW` command. The benefit of querying `INFORMATION_SCHEMA` is that it is possible to join between tables.

| Table Name                                                                              | TiDB Extension | Description |
|-----------------------------------------------------------------------------------------|----------------|-------------|
| [`ANALYZE_STATUS`](#analyze_status-table)                                               | Yes            | Provides information about tasks to collect statistics. |
| [`CHARACTER_SETS`](#character_sets-table)                                               | No             | Provides a list of character sets the server supports. |
| [`CLUSTER_CONFIG`](/system-tables/system-table-cluster-config.md)                       | Yes            | Provides details about configuration settings for the entire TiDB cluster. |
| [`CLUSTER_HARDWARE`](/system-tables/system-table-cluster-info.md)                       | Yes            | Provides details on the underlying physical hardware discovered on each TiDB component. |
| [`CLUSTER_INFO`](/system-tables/system-table-cluster-info.md)                           | Yes            | Provides details on the current cluster topology. |
| [`CLUSTER_LOAD`](/system-tables/system-table-cluster-load.md)                           | Yes            | Provides current load information for TiDB servers in the cluster. |
| [`CLUSTER_LOG`](/system-tables/system-table-cluster-log.md)                             | Yes            | Provides a log for the entire TiDB cluster |
| `CLUSTER_PROCESSLIST`                                                                   | Yes            | Provides a cluster-level view of the "PROCESSLIST" table. |
| `CLUSTER_SLOW_QUERY`                                                                    | Yes            | Provides a cluster-level view of the "SLOW_QUERY" table. |
| `CLUSTER_STATEMENTS_SUMMARY`                                                            | Yes            | Provides a cluster-level view of the "STATEMENTS_SUMMARY" table. |
| `CLUSTER_STATEMENTS_SUMMARY_HISTORY`                                                    | Yes            | Provides a cluster-level view of the "CLUSTER_STATEMENTS_SUMMARY_HISTORY" table. |
| [`CLUSTER_SYSTEMINFO`](/system-tables/system-table-cluster-systeminfo.md)               | Yes            | Provides details about kernel parameter configuration for servers in the cluster. |
| [`COLLATIONS`](#collations-table)                                                       | No             | Provides a list of collations that the server supports. |
| [`COLLATION_CHARACTER_SET_APPLICABILITY`](#collation_character_set_applicability-table) | No             | Explains which collations apply to which character sets. |
| [`COLUMNS`](#columns-table)                                                             | No             | Provides a list of columns for all tables. |
| `COLUMN_PRIVILEGES`                                                                     | No             | Not implemented by TiDB. Returns zero rows. |
| `COLUMN_STATISTICS`                                                                     | No             | Not implemented by TiDB. Returns zero rows. |
| [`DDL_JOBS`](#todo)                                                                     | Yes            | Provides similar output to `ADMIN SHOW DDL JOBS` |
| [`ENGINES`](#engines-table)                                                             | No             | Provides a list of supported storage engines. |
| `EVENTS`                                                                                | No             | Not implemented by TiDB. Returns zero rows. |
| `FILES`                                                                                 | No             | Not implemented by TiDB. Returns zero rows. |
| `GLOBAL_STATUS`                                                                         | No             | Not implemented by TiDB. Returns zero rows. |
| `GLOBAL_VARIABLES`                                                                      | No             | Not implemented by TiDB. Returns zero rows. |
| [`INSPECTION_RESULT`](/system-tables/system-table-cluster-inspection-result.md)         | Yes            | Triggers internal diagnostics checks. |
| [`INSPECTION_RULES`](#todo)                                                             | Yes            | TODO |
| [`INSPECTION_SUMMARY`](/system-tables/system-table-cluster-inspection-summary.md)       | Yes            | TODO |
| [`KEY_COLUMN_USAGE`](#key_column_usage_table)                                           | No             | TODO |
| [`METRICS_SUMMARY`](/system-tables/system-table-cluster-metrics-summary.md)             | Yes            | TODO |
| [`METRICS_SUMMARY_BY_LABEL`](#todo)                                                     | Yes            | TODO |
| [`METRICS_TABLES`](/system-tables/system-table-cluster-metrics-tables.md)               | Yes            | TODO |
| `OPTIMIZER_TRACE`                                                                       | No             | Not implemented by TiDB. Returns zero rows. |
| `PARAMETERS`                                                                            | No             | Not implemented by TiDB. Returns zero rows. |
| [`PARTITIONS`](#partitions-table)                                                       | No             | Provides a list of table partitions. |
| `PLUGINS`                                                                               | No             | Not implemented by TiDB. Returns zero rows. |
| [`PROCESSLIST`](#processlist-table)                                                     | No             | Provides similar information to the command `SHOW PROCESSLIST`. |
| `PROFILING`                                                                             | No             | Not implemented by TiDB. Returns zero rows. |
| `REFERENTIAL_CONSTRAINTS`                                                               | No             | Not implemented by TiDB. Returns zero rows. |
| `ROUTINES`                                                                              | No             | Not implemented by TiDB. Returns zero rows. |
| [`SCHEMATA`](#schemata-table)                                                           | No             | Provides similar information to `SHOW DATABASES`. |
| `SCHEMA_PRIVILEGES`                                                                     | No             | Not implemented by TiDB. Returns zero rows. |
| [`SEQUENCES`](#sequences-table)                                                         | Yes            | The TiDB implementation of sequences is based on MariaDB. |
| `SESSION_STATUS`                                                                        | No             | Not implemented by TiDB. Returns zero rows. |
| [`SESSION_VARIABLES`](#session_variables-table)                                         | No             | Provides similar functionality to the command `SHOW SESSION VARIABLES` |
| [`SLOW_QUERY`](#todo)                                                                   | Yes            | Provides information on slow queries on the current TiDB server. |
| [`STATEMENTS_SUMMARY`](/statement-summary-tables.md)                                    | Yes            | Similar to performance_schema statement summary in MySQL. |
| [`STATEMENTS_SUMMARY_HISTORY`](/statement-summary-tables.md)                            | Yes            | Similar to performance_schema statement summary history in MySQL. |
| [`STATISTICS`](#statistics-table)                                                       | No             | Provides information on table indexes. |
| [`TABLES`](#tables-table)                                                               | No             | Provides a list of tables that the current user has visibility of. Similar to `SHOW TABLES`. |
| `TABLESPACES`                                                                           | No             | Not implemented by TiDB. Returns zero rows. |
| [`TABLE_CONSTRAINTS`](#table_constraints-table)                                         | No             | Provides information on primary keys, unique indexes and foreign keys. |
| `TABLE_PRIVILEGES`                                                                      | No             | Not implemented by TiDB. Returns zero rows. |
| [`TIDB_HOT_REGIONS`](#todo)                                                             | Yes            | TODO |
| [`TIDB_INDEXES`](#todo)                                                                 | Yes            | TODO |
| [`TIDB_SERVERS_INFO`](#todo)                                                            | Yes            | TODO |
| [`TIFLASH_REPLICA`](#todo)                                                              | Yes            | TODO |
| [`TIKV_REGION_PEERS`](#todo)                                                            | Yes            | TODO |
| [`TIKV_REGION_STATUS`](#todo)                                                           | Yes            | TODO |
| [`TIKV_STORE_STATUS`](#todo)                                                            | Yes            | TODO |
| `TRIGGERS`                                                                              | No             | Not implemented by TiDB. Returns zero rows. |
| `USER_PRIVILEGES`                                                                       | No             | TODO Need to check - it looks like it might be implemented?? |
| [`VIEWS`](#views-table)                                                                 | No             | Provides a list of views that the current user has visibility of. Similar to running `SHOW FULL TABLES WHERE table_type = 'VIEW'` |
