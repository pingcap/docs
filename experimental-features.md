---
title: TiDB Experimental Features
summary: Learn the experimental features of TiDB.
---

# TiDB Experimental Features

This document introduces the experimental features of TiDB in different versions. It is **NOT** recommended to use these features in the production environment.

## Stability

+ Improve the stability of the optimizer's choice of indexes (Introduced in v5.0)
    + Extend the statistics feature by collecting the multi-column order dependency information.
<<<<<<< HEAD
    + Refactor the statistics module, including deleting the `TopN` value from `CMSKetch` and the histogram, and adding NDV information for histogram buckets of each table index.
=======
    + Refactor the statistics module, including deleting the `TopN` value from `CMSKetch` and the histogram, and adding NDV information for histogram buckets of each table index. For details, see descriptions about [Statistics - `tidb_analyze_version = 2`](/statistics.md).
+ When TiKV is deployed with limited resources, if the foreground of TiKV processes too many read and write requests, the CPU resources used by the background are occupied to help process such requests, which affects the performance stability of TiKV. To avoid this situation, you can use the [Quota Limiter](/tikv-configuration-file.md#quota) to limit the CPU resources to be used by the foreground. (Introduced in v6.0)
>>>>>>> 714ef9dfa (Remove GA features from experimental doc (#9622))

## Scheduling

+ Cascading Placement Rules feature. It is a replica rule system that guides PD to generate corresponding schedules for different types of data. By combining different scheduling rules, you can finely control the attributes of any continuous data range, such as the number of replicas, the storage location, the host type, whether to participate in Raft election, and whether to act as the Raft leader. See [Cascading Placement Rules](/configure-placement-rules.md) for details. (Introduced in v4.0)
+ Elastic scheduling feature. It enables the TiDB cluster to dynamically scale out and in on Kubernetes based on real-time workloads, which effectively reduces the stress during your application's peak hours and saves overheads. See [Enable TidbCluster Auto-scaling](https://docs.pingcap.com/tidb-in-kubernetes/stable/enable-tidb-cluster-auto-scaling) for details. (Introduced in v4.0)

## SQL

+ List Partition (Introduced in v5.0)
+ List COLUMNS Partition (Introduced in v5.0)
+ [Dynamic Pruning Mode for Partitioned Tables](/partitioned-table.md#dynamic-pruning-mode). (Introduced in v5.1)
+ The expression index feature. The expression index is also called the function-based index. When you create an index, the index fields do not have to be a specific column but can be an expression calculated from one or more columns. This feature is useful for quickly accessing the calculation-based tables. See [Expression index](/sql-statements/sql-statement-create-index.md) for details. (Introduced in v4.0)
+ [Generated Columns](/generated-columns.md).
+ [User-Defined Variables](/user-defined-variables.md).
+ [JSON data type](/data-type-json.md) and [JSON functions](/functions-and-operators/json-functions.md).
+ [View](/information-schema/information-schema-views.md).
+ [Prepare Plan cache](/sql-prepare-plan-cache.md). (Introduced in v4.0)

## Configuration management

+ Persistently store configuration parameters in PD, and support dynamically modifying configuration items. (Introduced in v4.0)
+ [SHOW CONFIG](/sql-statements/sql-statement-show-config.md) (Introduced in v4.0)

## Data sharing and subscription

+ [Integrate TiCDC with Kafka Connect (Confluent Platform)](/ticdc/integrate-confluent-using-ticdc.md) (Introduced in v5.0)
+ [The cyclic replication feature of TiCDC](/ticdc/manage-ticdc.md#cyclic-replication) (Introduced in v5.0)

## Storage

<<<<<<< HEAD
+ [Disable Titan](/storage-engine/titan-configuration.md#disable-titan-experimental).
+ [Titan Level Merge](/storage-engine/titan-configuration.md#level-merge-experimental).
+ TiFlash supports distributing the new data of the storage engine on multiple hard drives to share the I/O pressure. (Introduced in v4.0)
=======
+ [Disable Titan](/storage-engine/titan-configuration.md#disable-titan-experimental) (Introduced in v4.0)
+ [Titan Level Merge](/storage-engine/titan-configuration.md#level-merge-experimental) (Introduced in v4.0)
+ Divide Regions are divided into buckets. [Buckets are used as the unit of concurrent query](/tune-region-performance.md#use-bucket-to-increase-concurrency) to improve the scan concurrency. (Introduced in v6.1.0)
+ TiKV introduces [API V2](/tikv-configuration-file.md#api-version-new-in-v610). (Introduced in v6.1.0)
>>>>>>> 714ef9dfa (Remove GA features from experimental doc (#9622))

## Backup and restoration

+ [Back up Raw KV](/br/use-br-command-line-tool.md#back-up-raw-kv-experimental-feature).

## Garbage collection

+ [Green GC](/system-variables.md#tidb_gc_scan_lock_mode-new-in-v50).

## Diagnostics

+ [SQL diagnostics](/information-schema/information-schema-sql-diagnostics.md).
+ [Cluster diagnostics](/dashboard/dashboard-diagnostics-access.md).
