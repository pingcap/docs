---
title: Information Schema
summary: TiDB 实现了 ANSI 标准的 information_schema，用于查看系统元数据。
---

# Information Schema

Information Schema 提供了一种符合 ANSI 标准的方式来查看系统元数据。除了为兼容 MySQL 而包含的表之外，TiDB 还提供了许多自定义的 `INFORMATION_SCHEMA` 表。

许多 `INFORMATION_SCHEMA` 表都有对应的 `SHOW` 语句。查询 `INFORMATION_SCHEMA` 的好处在于可以在表之间进行关联查询。

## 兼容 MySQL 的表

<CustomContent platform="tidb">

| 表名                                                                              | 描述                 |
|-----------------------------------------------------------------------------------|----------------------|
| [`CHARACTER_SETS`](/information-schema/information-schema-character-sets.md)            | 提供服务器支持的字符集列表。 |
| [`CHECK_CONSTRAINTS`](/information-schema/information-schema-check-constraints.md)            | 提供关于表上 [`CHECK` 约束](/constraints.md#check) 的信息。 |
| [`COLLATIONS`](/information-schema/information-schema-collations.md)                    | 提供服务器支持的排序规则列表。 |
| [`COLLATION_CHARACTER_SET_APPLICABILITY`](/information-schema/information-schema-collation-character-set-applicability.md) | 说明哪些排序规则适用于哪些字符集。 |
| [`COLUMNS`](/information-schema/information-schema-columns.md)                          | 提供所有表的列信息列表。 |
| `COLUMN_PRIVILEGES`                                                                     | TiDB 未实现。返回零行。 |
| `COLUMN_STATISTICS`                                                                     | TiDB 未实现。返回零行。 |
| [`ENGINES`](/information-schema/information-schema-engines.md)                          | 提供支持的存储引擎列表。 |
| `EVENTS`                                                                                | TiDB 未实现。返回零行。 |
| `FILES`                                                                                 | TiDB 未实现。返回零行。 |
| `GLOBAL_STATUS`                                                                         | TiDB 未实现。返回零行。 |
| `GLOBAL_VARIABLES`                                                                      | TiDB 未实现。返回零行。 |
| [`KEYWORDS`](/information-schema/information-schema-keywords.md)                        | 提供完整的关键字列表。                |
| [`KEY_COLUMN_USAGE`](/information-schema/information-schema-key-column-usage.md)        | 描述列的键约束，例如主键约束。 |
| `OPTIMIZER_TRACE`                                                                       | TiDB 未实现。返回零行。 |
| `PARAMETERS`                                                                            | TiDB 未实现。返回零行。 |
| [`PARTITIONS`](/information-schema/information-schema-partitions.md)                    | 提供表分区列表。 |
| `PLUGINS`                                                                               | TiDB 未实现。返回零行。 |
| [`PROCESSLIST`](/information-schema/information-schema-processlist.md)                  | 提供与命令 `SHOW PROCESSLIST` 类似的信息。 |
| `PROFILING`                                                                             | TiDB 未实现。返回零行。 |
| `REFERENTIAL_CONSTRAINTS`                                                               | 提供 `FOREIGN KEY` 约束的信息。 |
| `ROUTINES`                                                                              | TiDB 未实现。返回零行。 |
| [`SCHEMATA`](/information-schema/information-schema-schemata.md)                        | 提供与 `SHOW DATABASES` 类似的信息。 |
| `SCHEMA_PRIVILEGES`                                                                     | TiDB 未实现。返回零行。 |
| `SESSION_STATUS`                                                                        | TiDB 未实现。返回零行。 |
| [`SESSION_VARIABLES`](/information-schema/information-schema-session-variables.md)      | 提供与命令 `SHOW SESSION VARIABLES` 类似的功能。 |
| [`STATISTICS`](/information-schema/information-schema-statistics.md)                    | 提供表索引的信息。 |
| [`TABLES`](/information-schema/information-schema-tables.md)                            | 提供当前用户可见的表列表。类似于 `SHOW TABLES`。 |
| `TABLESPACES`                                                                           | TiDB 未实现。返回零行。 |
| [`TABLE_CONSTRAINTS`](/information-schema/information-schema-table-constraints.md)      | 提供主键、唯一索引和外键的信息。 |
| `TABLE_PRIVILEGES`                                                                      | TiDB 未实现。返回零行。 |
| `TRIGGERS`                                                                              | TiDB 未实现。返回零行。 |
| [`USER_ATTRIBUTES`](/information-schema/information-schema-user-attributes.md) | 汇总用户注释和用户属性的信息。 |
| [`USER_PRIVILEGES`](/information-schema/information-schema-user-privileges.md)          | 汇总与当前用户相关的权限。 |
| [`VARIABLES_INFO`](/information-schema/information-schema-variables-info.md)            | 提供 TiDB 系统变量的信息。 |
| [`VIEWS`](/information-schema/information-schema-views.md)                              | 提供当前用户可见的视图列表。类似于执行 `SHOW FULL TABLES WHERE table_type = 'VIEW'`。 |

</CustomContent>

<CustomContent platform="tidb-cloud">

| 表名                                                                              | 描述                 |
|-----------------------------------------------------------------------------------|----------------------|
| [`CHARACTER_SETS`](/information-schema/information-schema-character-sets.md)            | 提供服务器支持的字符集列表。 |
| [`CHECK_CONSTRAINTS`](/information-schema/information-schema-check-constraints.md)            | 提供关于表上 [`CHECK` 约束](/constraints.md#check) 的信息。 |
| [`COLLATIONS`](/information-schema/information-schema-collations.md)                    | 提供服务器支持的排序规则列表。 |
| [`COLLATION_CHARACTER_SET_APPLICABILITY`](/information-schema/information-schema-collation-character-set-applicability.md) | 说明哪些排序规则适用于哪些字符集。 |
| [`COLUMNS`](/information-schema/information-schema-columns.md)                          | 提供所有表的列信息列表。 |
| `COLUMN_PRIVILEGES`                                                                     | TiDB 未实现。返回零行。 |
| `COLUMN_STATISTICS`                                                                     | TiDB 未实现。返回零行。 |
| [`ENGINES`](/information-schema/information-schema-engines.md)                          | 提供支持的存储引擎列表。 |
| `EVENTS`                                                                                | TiDB 未实现。返回零行。 |
| `FILES`                                                                                 | TiDB 未实现。返回零行。 |
| `GLOBAL_STATUS`                                                                         | TiDB 未实现。返回零行。 |
| `GLOBAL_VARIABLES`                                                                      | TiDB 未实现。返回零行。 |
| [`KEY_COLUMN_USAGE`](/information-schema/information-schema-key-column-usage.md)        | 描述列的键约束，例如主键约束。 |
| `OPTIMIZER_TRACE`                                                                       | TiDB 未实现。返回零行。 |
| `PARAMETERS`                                                                            | TiDB 未实现。返回零行。 |
| [`PARTITIONS`](/information-schema/information-schema-partitions.md)                    | 提供表分区列表。 |
| `PLUGINS`                                                                               | TiDB 未实现。返回零行。 |
| [`PROCESSLIST`](/information-schema/information-schema-processlist.md)                  | 提供与命令 `SHOW PROCESSLIST` 类似的信息。 |
| `PROFILING`                                                                             | TiDB 未实现。返回零行。 |
| `REFERENTIAL_CONSTRAINTS`                                                               | 提供 `FOREIGN KEY` 约束的信息。 |
| `ROUTINES`                                                                              | TiDB 未实现。返回零行。 |
| [`SCHEMATA`](/information-schema/information-schema-schemata.md)                        | 提供与 `SHOW DATABASES` 类似的信息。 |
| `SCHEMA_PRIVILEGES`                                                                     | TiDB 未实现。返回零行。 |
| `SESSION_STATUS`                                                                        | TiDB 未实现。返回零行。 |
| [`SESSION_VARIABLES`](/information-schema/information-schema-session-variables.md)      | 提供与命令 `SHOW SESSION VARIABLES` 类似的功能。 |
| [`STATISTICS`](/information-schema/information-schema-statistics.md)                    | 提供表索引的信息。 |
| [`TABLES`](/information-schema/information-schema-tables.md)                            | 提供当前用户可见的表列表。类似于 `SHOW TABLES`。 |
| `TABLESPACES`                                                                           | TiDB 未实现。返回零行。 |
| [`TABLE_CONSTRAINTS`](/information-schema/information-schema-table-constraints.md)      | 提供主键、唯一索引和外键的信息。 |
| `TABLE_PRIVILEGES`                                                                      | TiDB 未实现。返回零行。 |
| `TRIGGERS`                                                                              | TiDB 未实现。返回零行。 |
| [`USER_ATTRIBUTES`](/information-schema/information-schema-user-attributes.md) | 汇总用户注释和用户属性的信息。 |
| [`USER_PRIVILEGES`](/information-schema/information-schema-user-privileges.md)          | 汇总与当前用户相关的权限。 |
| [`VARIABLES_INFO`](/information-schema/information-schema-variables-info.md)            | 提供 TiDB 系统变量的信息。 |
| [`VIEWS`](/information-schema/information-schema-views.md)                              | 提供当前用户可见的视图列表。类似于执行 `SHOW FULL TABLES WHERE table_type = 'VIEW'`。 |

</CustomContent>

## TiDB 扩展的表

<CustomContent platform="tidb">

> **注意：**
>
> 下列部分表仅支持 TiDB 自建版，不支持 TiDB Cloud。如需获取 TiDB Cloud 上不支持的系统表完整列表，请参见 [System tables](https://docs.pingcap.com/tidbcloud/limited-sql-features#system-tables)。

| 表名                                                                              | 描述 |
|-----------------------------------------------------------------------------------|------|
| [`ANALYZE_STATUS`](/information-schema/information-schema-analyze-status.md)            | 提供收集统计信息任务的信息。 |
| [`CLIENT_ERRORS_SUMMARY_BY_HOST`](/information-schema/client-errors-summary-by-host.md)  | 汇总客户端请求产生并返回给客户端的错误和警告信息。 |
| [`CLIENT_ERRORS_SUMMARY_BY_USER`](/information-schema/client-errors-summary-by-user.md)  | 汇总客户端产生的错误和警告信息。 |
| [`CLIENT_ERRORS_SUMMARY_GLOBAL`](/information-schema/client-errors-summary-global.md)   | 汇总客户端产生的错误和警告信息。 |
| [`CLUSTER_CONFIG`](/information-schema/information-schema-cluster-config.md)            | 提供整个 TiDB 集群的配置信息。该表不适用于 TiDB Cloud。 |
| `CLUSTER_DEADLOCKS` | 提供 `DEADLOCKS` 表的集群级视图。 |
| [`CLUSTER_HARDWARE`](/information-schema/information-schema-cluster-hardware.md)            | 提供在每个 TiDB 组件上发现的底层物理硬件详情。该表不适用于 TiDB Cloud。 |
| [`CLUSTER_INFO`](/information-schema/information-schema-cluster-info.md)                | 提供当前集群拓扑的详细信息。该表在 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群中不可用。 |
| [`CLUSTER_LOAD`](/information-schema/information-schema-cluster-load.md)                | 提供集群中 TiDB 服务器的当前负载信息。该表不适用于 TiDB Cloud。 |
| [`CLUSTER_LOG`](/information-schema/information-schema-cluster-log.md)                  | 提供整个 TiDB 集群的日志。该表不适用于 TiDB Cloud。 |
| `CLUSTER_MEMORY_USAGE`                                                                  | 提供 `MEMORY_USAGE` 表的集群级视图。 |
| `CLUSTER_MEMORY_USAGE_OPS_HISTORY`                                                      | 提供 `MEMORY_USAGE_OPS_HISTORY` 表的集群级视图。 |
| `CLUSTER_PROCESSLIST`                                                                   | 提供 `PROCESSLIST` 表的集群级视图。 |
| `CLUSTER_SLOW_QUERY`                                                                    | 提供 `SLOW_QUERY` 表的集群级视图。该表在 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群中不可用。 |
| `CLUSTER_STATEMENTS_SUMMARY`                                                            | 提供 `STATEMENTS_SUMMARY` 表的集群级视图。该表在 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群中不可用。 |
| `CLUSTER_STATEMENTS_SUMMARY_HISTORY`                                                    | 提供 `STATEMENTS_SUMMARY_HISTORY` 表的集群级视图。该表在 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群中不可用。 |
| `CLUSTER_TIDB_INDEX_USAGE` | 提供 `TIDB_INDEX_USAGE` 表的集群级视图。 |
| `CLUSTER_TIDB_TRX` | 提供 `TIDB_TRX` 表的集群级视图。 |
| [`CLUSTER_SYSTEMINFO`](/information-schema/information-schema-cluster-systeminfo.md)    | 提供集群中服务器内核参数配置信息。该表不适用于 TiDB Cloud。 |
| [`DATA_LOCK_WAITS`](/information-schema/information-schema-data-lock-waits.md) | 提供 TiKV 服务器上的锁等待信息。 |
| [`DDL_JOBS`](/information-schema/information-schema-ddl-jobs.md)                        | 提供与 `ADMIN SHOW DDL JOBS` 类似的输出。 |
| [`DEADLOCKS`](/information-schema/information-schema-deadlocks.md) | 提供最近发生的若干死锁错误的信息。 |
| [`INSPECTION_RESULT`](/information-schema/information-schema-inspection-result.md)      | 触发内部诊断检查。该表不适用于 TiDB Cloud。 |
| [`INSPECTION_RULES`](/information-schema/information-schema-inspection-rules.md)        | 已执行的内部诊断检查列表。该表不适用于 TiDB Cloud。 |
| [`INSPECTION_SUMMARY`](/information-schema/information-schema-inspection-summary.md)    | 重要监控指标的汇总报告。该表不适用于 TiDB Cloud。 |
| [`MEMORY_USAGE`](/information-schema/information-schema-memory-usage.md)                |  当前 TiDB 实例的内存使用情况。 |
| [`MEMORY_USAGE_OPS_HISTORY`](/information-schema/information-schema-memory-usage-ops-history.md)    | 当前 TiDB 实例内存相关操作的历史及执行依据。 |
| [`METRICS_SUMMARY`](/information-schema/information-schema-metrics-summary.md)          | 从 Prometheus 提取的监控指标汇总。该表不适用于 TiDB Cloud。 |
| `METRICS_SUMMARY_BY_LABEL`                                                              | 参见 `METRICS_SUMMARY` 表。该表不适用于 TiDB Cloud。 |
| [`METRICS_TABLES`](/information-schema/information-schema-metrics-tables.md)            | 提供 `METRICS_SCHEMA` 中表的 PromQL 定义。该表不适用于 TiDB Cloud。 |
| [`PLACEMENT_POLICIES`](/information-schema/information-schema-placement-policies.md)    | 提供所有放置策略的信息。该表在 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群中不可用。 |
| [`SEQUENCES`](/information-schema/information-schema-sequences.md)                      | TiDB 的序列实现基于 MariaDB。 |
| [`SLOW_QUERY`](/information-schema/information-schema-slow-query.md)                    | 提供当前 TiDB 服务器上的慢查询信息。该表在 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群中不可用。 |
| [`STATEMENTS_SUMMARY`](/statement-summary-tables.md)                                    | 类似于 MySQL 的 performance_schema statement summary。该表在 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群中不可用。 |
| [`STATEMENTS_SUMMARY_HISTORY`](/statement-summary-tables.md)                            | 类似于 MySQL 的 performance_schema statement summary history。该表在 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群中不可用。 |
| [`TABLE_STORAGE_STATS`](/information-schema/information-schema-table-storage-stats.md)  | 提供存储中表大小的详细信息。 |
| [`TIDB_HOT_REGIONS`](/information-schema/information-schema-tidb-hot-regions.md)        | 提供哪些 Region 为热点的统计信息。 |
| [`TIDB_HOT_REGIONS_HISTORY`](/information-schema/information-schema-tidb-hot-regions-history.md) | 提供哪些 Region 为热点的历史统计信息。 |
| [`TIDB_INDEXES`](/information-schema/information-schema-tidb-indexes.md)                | 提供 TiDB 表的索引信息。 |
| [`TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md)        | 提供 TiDB 节点上索引使用统计信息。 ｜
| [`TIDB_SERVERS_INFO`](/information-schema/information-schema-tidb-servers-info.md)      | 提供 TiDB 服务器（即 tidb-server 组件）列表。 |
| [`TIDB_TRX`](/information-schema/information-schema-tidb-trx.md) | 提供 TiDB 节点上正在执行的事务信息。 |
| [`TIFLASH_REPLICA`](/information-schema/information-schema-tiflash-replica.md)          | 提供 TiFlash 副本的详细信息。 |
| [`TIKV_REGION_PEERS`](/information-schema/information-schema-tikv-region-peers.md)      | 提供 Region 存储位置的详细信息。 |
| [`TIKV_REGION_STATUS`](/information-schema/information-schema-tikv-region-status.md)    | 提供 Region 的统计信息。 |
| [`TIKV_STORE_STATUS`](/information-schema/information-schema-tikv-store-status.md)      | 提供 TiKV 服务器的基本信息。 |

</CustomContent>

<CustomContent platform="tidb-cloud">

| 表名                                                                              | 描述 |
|-----------------------------------------------------------------------------------|------|
| [`ANALYZE_STATUS`](/information-schema/information-schema-analyze-status.md)            | 提供收集统计信息任务的信息。 |
| [`CLIENT_ERRORS_SUMMARY_BY_HOST`](/information-schema/client-errors-summary-by-host.md)  | 汇总客户端请求产生并返回给客户端的错误和警告信息。 |
| [`CLIENT_ERRORS_SUMMARY_BY_USER`](/information-schema/client-errors-summary-by-user.md)  | 汇总客户端产生的错误和警告信息。 |
| [`CLIENT_ERRORS_SUMMARY_GLOBAL`](/information-schema/client-errors-summary-global.md)   | 汇总客户端产生的错误和警告信息。 |
| [`CLUSTER_CONFIG`](https://docs.pingcap.com/tidb/stable/information-schema-cluster-config)            | 提供整个 TiDB 集群的配置信息。该表不适用于 TiDB Cloud。 |
| `CLUSTER_DEADLOCKS` | 提供 `DEADLOCKS` 表的集群级视图。 |
| [`CLUSTER_HARDWARE`](https://docs.pingcap.com/tidb/stable/information-schema-cluster-hardware)            | 提供在每个 TiDB 组件上发现的底层物理硬件详情。该表不适用于 TiDB Cloud。 |
| [`CLUSTER_INFO`](/information-schema/information-schema-cluster-info.md)                | 提供当前集群拓扑的详细信息。该表在 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群中不可用。 |
| [`CLUSTER_LOAD`](https://docs.pingcap.com/tidb/stable/information-schema-cluster-load)                | 提供集群中 TiDB 服务器的当前负载信息。该表不适用于 TiDB Cloud。 |
| [`CLUSTER_LOG`](https://docs.pingcap.com/tidb/stable/information-schema-cluster-log)                  | 提供整个 TiDB 集群的日志。该表不适用于 TiDB Cloud。 |
| `CLUSTER_MEMORY_USAGE`                                                                  | 提供 `MEMORY_USAGE` 表的集群级视图。该表不适用于 TiDB Cloud。 |
| `CLUSTER_MEMORY_USAGE_OPS_HISTORY`                                                      | 提供 `MEMORY_USAGE_OPS_HISTORY` 表的集群级视图。该表不适用于 TiDB Cloud。 |
| `CLUSTER_PROCESSLIST`                                                                   | 提供 `PROCESSLIST` 表的集群级视图。 |
| `CLUSTER_SLOW_QUERY`                                                                    | 提供 `SLOW_QUERY` 表的集群级视图。该表在 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群中不可用。  |
| `CLUSTER_STATEMENTS_SUMMARY`                                                            | 提供 `STATEMENTS_SUMMARY` 表的集群级视图。该表在 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群中不可用。 |
| `CLUSTER_STATEMENTS_SUMMARY_HISTORY`                                                    | 提供 `STATEMENTS_SUMMARY_HISTORY` 表的集群级视图。该表在 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群中不可用。 |
| `CLUSTER_TIDB_TRX` | 提供 `TIDB_TRX` 表的集群级视图。 |
| [`CLUSTER_SYSTEMINFO`](https://docs.pingcap.com/tidb/stable/information-schema-cluster-systeminfo)    | 提供集群中服务器内核参数配置信息。该表不适用于 TiDB Cloud。 |
| [`DATA_LOCK_WAITS`](/information-schema/information-schema-data-lock-waits.md) | 提供 TiKV 服务器上的锁等待信息。 |
| [`DDL_JOBS`](/information-schema/information-schema-ddl-jobs.md)                        | 提供与 `ADMIN SHOW DDL JOBS` 类似的输出。 |
| [`DEADLOCKS`](/information-schema/information-schema-deadlocks.md) | 提供最近发生的若干死锁错误的信息。 |
| [`INSPECTION_RESULT`](https://docs.pingcap.com/tidb/stable/information-schema-inspection-result)      | 触发内部诊断检查。该表不适用于 TiDB Cloud。 |
| [`INSPECTION_RULES`](https://docs.pingcap.com/tidb/stable/information-schema-inspection-rules)        | 已执行的内部诊断检查列表。该表不适用于 TiDB Cloud。 |
| [`INSPECTION_SUMMARY`](https://docs.pingcap.com/tidb/stable/information-schema-inspection-summary)    | 重要监控指标的汇总报告。该表不适用于 TiDB Cloud。 |
| [`MEMORY_USAGE`](/information-schema/information-schema-memory-usage.md)                |  当前 TiDB 实例的内存使用情况。 |
| [`MEMORY_USAGE_OPS_HISTORY`](/information-schema/information-schema-memory-usage-ops-history.md)    | 当前 TiDB 实例内存相关操作的历史及执行依据。 |
| [`METRICS_SUMMARY`](https://docs.pingcap.com/tidb/stable/information-schema-metrics-summary)          | 从 Prometheus 提取的监控指标汇总。该表不适用于 TiDB Cloud。 |
| `METRICS_SUMMARY_BY_LABEL`                                                              | 参见 `METRICS_SUMMARY` 表。该表不适用于 TiDB Cloud。 |
| [`METRICS_TABLES`](https://docs.pingcap.com/tidb/stable/information-schema-metrics-tables)            | 提供 `METRICS_SCHEMA` 中表的 PromQL 定义。该表不适用于 TiDB Cloud。 |
| [`PLACEMENT_POLICIES`](https://docs.pingcap.com/tidb/stable/information-schema-placement-policies)    | 提供所有放置策略的信息。该表在 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群中不可用。 |
| [`SEQUENCES`](/information-schema/information-schema-sequences.md)                      | TiDB 的序列实现基于 MariaDB。 |
| [`SLOW_QUERY`](/information-schema/information-schema-slow-query.md)                    | 提供当前 TiDB 服务器上的慢查询信息。该表在 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群中不可用。 |
| [`STATEMENTS_SUMMARY`](/statement-summary-tables.md)                                    | 类似于 MySQL 的 performance_schema statement summary。该表在 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群中不可用。 |
| [`STATEMENTS_SUMMARY_HISTORY`](/statement-summary-tables.md)                            | 类似于 MySQL 的 performance_schema statement summary history。该表在 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群中不可用。|
| [`TABLE_STORAGE_STATS`](/information-schema/information-schema-table-storage-stats.md)  | 提供存储中表大小的详细信息。 |
| [`TIDB_HOT_REGIONS`](https://docs.pingcap.com/tidb/stable/information-schema-tidb-hot-regions)        | 提供哪些 Region 为热点的统计信息。该表不适用于 TiDB Cloud。 |
| [`TIDB_HOT_REGIONS_HISTORY`](/information-schema/information-schema-tidb-hot-regions-history.md) | 提供哪些 Region 为热点的历史统计信息。 |
| [`TIDB_INDEXES`](/information-schema/information-schema-tidb-indexes.md)                | 提供 TiDB 表的索引信息。 |
| [`TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md)        | 提供 TiDB 节点上索引使用统计信息。 ｜
| [`TIDB_SERVERS_INFO`](/information-schema/information-schema-tidb-servers-info.md)      | 提供 TiDB 服务器（即 tidb-server 组件）列表。 |
| [`TIDB_TRX`](/information-schema/information-schema-tidb-trx.md) | 提供 TiDB 节点上正在执行的事务信息。 |
| [`TIFLASH_REPLICA`](/information-schema/information-schema-tiflash-replica.md)          | 提供 TiFlash 副本的详细信息。 |
| [`TIKV_REGION_PEERS`](/information-schema/information-schema-tikv-region-peers.md)      | 提供 Region 存储位置的详细信息。 |
| [`TIKV_REGION_STATUS`](/information-schema/information-schema-tikv-region-status.md)    | 提供 Region 的统计信息。 |
| [`TIKV_STORE_STATUS`](/information-schema/information-schema-tikv-store-status.md)      | 提供 TiKV 服务器的基本信息。 |

</CustomContent>