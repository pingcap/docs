---
title: TiDB Experimental Features
summary: Learn the experimental features of TiDB.
---

# TiDB Experimental Features

This document introduces the experimental features of TiDB in different versions. It is **NOT** recommended to use these features in the production environment.

## Performance

+ [Support collecting statistics for `PREDICATE COLUMNS`](/statistics.md#collect-statistics-on-some-columns) (Introduced in v5.4)
+ [Support synchronously loading statistics](/statistics.md#load-statistics). (Introduced in v5.4)
+ [Control the memory quota for collecting statistics](/statistics.md#the-memory-quota-for-collecting-statistics). (Introduced in v6.1.0)
+ [Extended statistics](/extended-statistics.md). (Introduced in v5.0.0)
+ [Randomly sample about 10000 rows of data to quickly build statistics](/system-variables.md#tidb_enable_fast_analyze) (Introduced in v3.0)

## Stability

+ Improve the stability of the optimizer's choice of indexes: extend the statistics feature by collecting the multi-column order dependency information (Introduced in v5.0).
+ When TiKV is deployed with limited resources, if the foreground of TiKV processes too many read and write requests, the CPU resources used by the background are occupied to help process such requests, which affects the performance stability of TiKV. To avoid this situation, you can use the [Quota Limiter](/tikv-configuration-file.md#quota) to limit the CPU resources to be used by the foreground. (Introduced in v6.0)

## Scheduling

Elastic scheduling feature. It enables the TiDB cluster to dynamically scale out and in on Kubernetes based on real-time workloads, which effectively reduces the stress during your application's peak hours and saves overheads. See [Enable TidbCluster Auto-scaling](https://docs.pingcap.com/tidb-in-kubernetes/stable/enable-tidb-cluster-auto-scaling) for details. (Introduced in v4.0)

## SQL

+ The expression index feature. The expression index is also called the function-based index. When you create an index, the index fields do not have to be a specific column but can be an expression calculated from one or more columns. This feature is useful for quickly accessing the calculation-based tables. See [Expression index](/sql-statements/sql-statement-create-index.md) for details. (Introduced in v4.0)
+ [Generated Columns](/generated-columns.md) (Introduced in v2.1)
+ [User-Defined Variables](/user-defined-variables.md) (Introduced in v2.1)
+ [JSON data type](/data-type-json.md) and [JSON functions](/functions-and-operators/json-functions.md) (Introduced in v2.1)
+ [Cascades Planner](/system-variables.md#tidb_enable_cascades_planner): a cascades framework-based top-down query optimizer (Introduced in v3.0)
+ [`ALTER TABLE ... COMPACT`](/sql-statements/sql-statement-alter-table-compact.md) (Introduced in v6.1.0)
+ [Using `ALTER TABLE` to modify multiple columns or indexes](/system-variables.md#tidb_enable_change_multi_schema) (Introduced in v5.0.0)

## Storage

+ [Disable Titan](/storage-engine/titan-configuration.md#disable-titan-experimental) (Introduced in v4.0)
+ [Titan Level Merge](/storage-engine/titan-configuration.md#level-merge-experimental) (Introduced in v4.0)
+ Divide Regions are divided into buckets. [Buckets are used as the unit of concurrent query](/tune-region-performance.md#use-bucket-to-increase-concurrency) to improve the scan concurrency. (Introduced in v6.1.0)
+ TiKV introduces [API V2](/tikv-configuration-file.md#api-version-new-in-v610). (Introduced in v6.1.0)

## Backup and restoration

+ [Back up and restore RawKV](/br/rawkv-backup-and-restore.md) (Introduced in v3.1)

## Data migration

+ [Use WebUI](/dm/dm-webui-guide.md) to manage migration tasks in DM. (Introduced in v6.0)

## Garbage collection

+ [Green GC](/system-variables.md#tidb_gc_scan_lock_mode-new-in-v50) (Introduced in v5.0)

## Diagnostics

+ [SQL diagnostics](/information-schema/information-schema-sql-diagnostics.md) (Introduced in v4.0)
+ [Cluster diagnostics](/dashboard/dashboard-diagnostics-access.md) (Introduced in v4.0)
+ [TiKV-FastTune dashboard](/grafana-tikv-dashboard.md#tikv-fasttune-dashboard) (Introduced in v4.0)
