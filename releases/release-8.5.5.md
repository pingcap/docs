---
title: TiDB 8.5.5 Release Notes
summary: Learn about the features, compatibility changes, improvements, and bug fixes in TiDB 8.5.5.
---

# TiDB 8.5.5 Release Notes

Release date: xx xx, 2026

TiDB version: 8.5.5

Quick access: [Quick start](https://docs.pingcap.com/tidb/v8.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v8.5/production-deployment-using-tiup)

## Features

### Performance

* 大幅提升特定有损 DDL 操作的执行效率，例如 `BIGINT → INT`、`CHAR(120) → VARCHAR(60)`。在未发生数据截断的前提下，执行耗时可从数小时缩短至分钟级、秒级甚至毫秒级，性能提升可达到数十倍至数十万倍。  [#63366](https://github.com/pingcap/tidb/issues/63366)  [@wjhuang2016](https://github.com/wjhuang2016), [@tangenta](https://github.com/tangenta), [@fzzf678](https://github.com/fzzf678)**tw@qiancai** <!--2292-->

    优化策略包括：

    - 在严格 SQL 模式下，预先检查类型转换过程中是否存在数据截断风险；
    - 若不存在数据截断风险，则仅更新元数据，尽量避免索引重建；
    - 如需重建索引，则采用更高效的 Ingest 流程，大幅提升索引重建性能。

    性能提升示例（基于 100 GiB 表的基准测试）：

    | 场景 | 操作类型 | 优化前 | 优化后 | 性能提升 |
    |------|----------|--------|--------|----------|
    | 无索引列 | `BIGINT → INT` | 2 小时 34 分 | 1 分 5 秒 | 142× |
    | 有索引列 | `BIGINT → INT` | 6 小时 25 分 | 0.05 秒 | 460,000× |
    | 有索引列 | `CHAR(120) → VARCHAR(60)` | 7 小时 16 分 | 12 分 56 秒 | 34× |

    注：以上数据基于 DDL 执行过程中未发生数据截断的前提。以上优化对于有 TiFlash 副本的表，以及 sign <--> unsign 数据类型修改的场景不会生效。

    更多信息，请参考[用户文档](链接)。

* Improve DDL performance in scenarios with a large number of foreign keys, with up to a 25x increase in logical DDL performance [#61126](https://github.com/pingcap/tidb/issues/61126) @[GMHDBJD](https://github.com/GMHDBJD) **tw@hfxsd** <!--1896-->

    Before v8.5.5, in scenarios involving ultra-large-scale tables (for example, a cluster with 10 million tables in total, including hundreds of thousands of tables with foreign keys), the performance of logical DDL operations (such as creating tables or adding columns) can drop to approximately 4 QPS. This leads to low operational efficiency in multi-tenant SaaS environments.

    TiDB v8.5.5 optimizes these scenarios. Test results show that in an extreme environment with 10 million tables (including 200,000 tables with foreign keys), the logical DDL processing performance consistently maintains 100 QPS. Compared to previous versions, the performance is improved by 25 times, significantly enhancing the operational responsiveness of ultra-large-scale clusters.

* Support pushing index lookups down to TiKV to improve query performance [#62575](https://github.com/pingcap/tidb/issues/62575) @[lcwangchao](https://github.com/lcwangchao)

    Starting from v8.5.5, TiDB supports using optimizer hints to push the `IndexLookUp` operator down to TiKV nodes. This reduces the number of remote procedure calls (RPCs) and can improve query performance. The actual performance improvement varies depending on the specific workload and requires testing for verification.

    You can use the [`INDEX_LOOKUP_PUSHDOWN(t1_name, idx1_name [, idx2_name ...])`](https://docs.pingcap.com/tidb/stable/optimizer-hints#index_lookup_pushdownt1_name-idx1_name--idx2_name--new-in-v855) hint to explicitly instruct the optimizer to push index lookups down to TiKV for a specific table. It is recommended to combine this hint with the table's AFFINITY attribute. For example, set `AFFINITY="table"` for regular tables and `AFFINITY="partition"` for partitioned tables.

    To disable index lookup pushdown to TiKV for a specific table, use the [`NO_INDEX_LOOKUP_PUSHDOWN(t1_name)`](https://docs.pingcap.com/tidb/stable/optimizer-hints#no_index_lookup_pushdownt1_name--new-in-v855) hint.

    For more information, see [documentation](https://docs.pingcap.com/tidb/stable/optimizer-hints#index_lookup_pushdownt1_name-idx1_name--idx2_name--new-in-v855).

* 表级和分区级亲和性属性 AFFINITY [#9764](https://github.com/tikv/pd/issues/9764) @[lhy1024](https://github.com/lhy1024) **tw@qiancai** <!--2317-->

    为表或者分区表新增亲和性属性，设置亲和性属性后，PD会将表或分区的Region归为相同的一个亲和性分组中，这些Region的Leader、Voter 会被优先调度到指定TiKV Store上。有AFFNITY属性的表和分区在查询时，由于索引、表数据的Region都在一个TiKV Store上，因此优化器可结合 hint INDEX_LOOKUP_PUSHDOWN 指定将对应索引查询下推，减少跨节点分散查询带来的延迟，根据测试数据对比性能可约提升20%。

    更多信息，请参考[table-affinity.md](table-affinity.md)。

* Point-in-time recovery (PITR) supports recovery from compacted log backups for faster restores [#56522](https://github.com/pingcap/tidb/issues/56522) @[YuJuncen](https://github.com/YuJuncen) **tw@lilin90** <!--2001-->

    Starting from v8.5.5, the log backup compaction feature provides offline compaction capabilities, converting unstructured log backup data into structured SST files. This results in the following improvements:

    - **Improved recovery performance** - SST files can be more quickly imported into the cluster.
    - **Reduced storage space consumption** - redundant data is removed during compaction.
    - **Reduced impact on applications** - RPOs can be amintained with less frequent full snapshot-based backups.

  For more information, see [documentation](/br/br-compact-log-backup.md).

* Accelerated recovery of system tables from backups [#58757](https://github.com/pingcap/tidb/issues/58757) @[Leavrth](https://github.com/Leavrth) **tw@lilin90** <!--2109-->

    When restoring system tables from a backup, BR now introduces a new `--fast-load-sys-tables` parameter to use physical restoration instead of logical restoration. This option completely overwrites/replaces the existing tables, instead of restoring into them, for faster restoration for large scale deployments.

    For more information, see [Documentation](/br/br-snapshot-guide.md#restore-tables-in-the-mysql-schema).

### Reliability

* Improved store scheduling in presence of network jitter [#9359](https://github.com/tikv/pd/issues/9359) @[okJiang](https://github.com/okJiang) **tw@qiancai** <!--2260-->

    Provides a network status feedback mechanism to PD to avoid re-scheduling the leaders back to a problematic node (experiencing network jitter) after the leaders had been transferred off the node by TiKV raft mechanism. If the network continues to jitter, PD will actively evict leader from jittering node.

### Availability

* Introduce the client circuit breaker pattern for PD [#8678](https://github.com/tikv/pd/issues/8678) @[Tema](https://github.com/Tema) **tw@hfxsd** <!--2051-->

    To protect the PD leader from overloading during retry storms or similar feedback loops, TiDB now implements a circuit breaker pattern. When the error rate reaches a predefined threshold, the circuit breaker limits incoming traffic to allow the system to recover and stabilize. You can use the `tidb_cb_pd_metadata_error_rate_threshold_ratio` system variable to control the circuit breaker.

    For more information, see [Documentation](/system-variables.md#tidb_cb_pd_metadata_error_rate_threshold_ratio-new-in-v855).

### SQL

* 支持在线修改分布式 ADD Index 任务的并发和吞吐 [#62120](https://github.com/pingcap/tidb/pull/62120) @[joechenrh](https://github.com/joechenrh) **tw@qiancai** <!--2326-->

   在 v8.5.5 版本之前，当集群开启了分布式执行框架 [tidb_enable_dist_task](/system-variables/#tidb_enable_dist_task-从-v710-版本开始引入) ，在 ADD Index 任务执行期间，是无法修改该任务的 `THREAD`， `BATCH_SIZE`，`MAX_WRITE_SPEED`  参数。需要取消该 DDL 任务，重新设置参数后再提交，效率较低。支持该功能后，用户可以根据业务负载和对 ADD Index 的性能要求，在线灵活调整这些参数。

    更多信息，请参考[ADMIN ALTER DDL JOBS](/sql-statement-admin-alter-ddl/#admin-alter-ddl-jobs)。

### DB operations

* TiKV 支持优雅关闭 (graceful shutdown) [#17221](https://github.com/tikv/tikv/issues/17221) @[hujiatao0](https://github.com/hujiatao0) **tw@qiancai** <!--2297-->

    在关闭 TiKV 服务器时，TiKV 会尽量将其上的 leader 副本转移到其他 TiKV 节点，然后再关闭。该等待期默认为 20 秒，可通过 [`server.graceful-shutdown-timeout`](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#graceful-shutdown-timeout-从-v855-版本开始引入) 配置项进行调整。若达到该超时时间后仍有 leader 未完成转移，TiKV 将跳过剩余 leader 的转移，直接进入关闭流程。

    更多信息，请参考[用户文档](https://docs.pingcap.com/zh/tidb/v8.5/tikv-configuration-file#graceful-shutdown-timeout-从-v855-版本开始引入)。

* Improve the compatibility between ongoing log backup and snapshot restore [#58685](https://github.com/pingcap/tidb/issues/58685) @[BornChanger](https://github.com/BornChanger) **tw@lilin90** <!--2000-->

    Starting from v8.5.5, log backups can continue to run when performing a snapshot restore (when prerequisite conditions are met). This enables ongoing log backups to proceed without having to stop them during the restore procedure. The newly restored data will also be recorded in the ongoing log backup.

    For more information, see [documentation](https://docs.pingcap.com/tidb/v8.5/br-pitr-manual#compatibility-between-ongoing-log-backup-and-snapshot-restore).

* Table level restores from Log Backups [#57613](https://github.com/pingcap/tidb/issues/57613) @[Tristan1900](https://github.com/Tristan1900) **tw@lilin90** <!--2005-->

    Starting from v8.5.5, individual table level point in time recoveries can now be performed from log backups using filters. Being able to restore individual tables, instead of the full cluster, to a specific point in time enables much more flexible, and less impactful, recovery options.

    For more information, see [documentation](/br/br-pitr-manual.md#restore-data-using-filters).

### Observability

* Placeholder for feature summary [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link) **tw@xxx** <!--1234-->

    Provide a concise overview of what the feature is, the value it offers to users, and include a brief sentence on how to use it effectively. If there are any particularly important aspects of this feature, be sure to mention them as well.

    For more information, see [Documentation](link).

### Security

* Enable Azure Managed Identity (MI) authentication for Backup & Restore (BR) to Azure Blob Storage [#19006](https://github.com/tikv/tikv/issues/19006) @[RidRisR](https://github.com/RidRisR) **tw@qiancai** <!--2308-->

    Starting from v8.5.5, TiDB Backup & Restore supports Azure Managed Identity (MI) for authenticating to Azure Blob Storage, eliminating the need for static SAS tokens. This enables secure, keyless, and ephemeral authentication aligned with Azure best practices.

    With this feature, BR and the embedded BR worker in TiKV can acquire access tokens directly from Azure Instance Metadata Service (IMDS), reducing credential leakage risk and simplifying credential rotation for self-managed and cloud deployments on Azure.

    This enhancement is particularly useful for enterprise customers running TiDB on Azure Kubernetes Service (AKS) or other Azure environments that require strict security controls for backup and restore workflows.

    For more information, see [Documentation](link).

## Compatibility changes

### Behavior changes

* When using [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) with [Global Sort](/tidb-global-sort.md) enabled, primary key or unique index conflicts are now automatically resolved by removing all conflicting rows (none of the conflicting rows are preserved), instead of causing the task to fail. The number of conflicted rows appears in the `Result_Message` column of `SHOW IMPORT JOBS` output, and detailed conflict information is stored in cloud storage. For more information, see [`IMPORT INTO` conflict resolution](/sql-statements/sql-statement-import-into.md#conflict-resolution).

### MySQL compatibility

### System variables

| Variable name | Change type | Description |
|--------|------------------------------|------|
|  |  |  |
|  |  |  |
|  |  |  |

### Configuration parameters

| Configuration file or component | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

### System tables

### Other changes

## Improvements

+ TiDB

    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
    - (dup): release-9.0.0.md > Improvements> TiDB - Optimize the CPU usage of internal SQL statements in the Distributed eXecution Framework (DXF) [#59344](https://github.com/pingcap/tidb/issues/59344) @[D3Hunter](https://github.com/D3Hunter)

+ TiKV

    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
    - (dup): release-9.0.0.md > Improvements> TiKV - Throttle BR log restore requests when TiKV memory usage is high to prevent TiKV OOM [#18124](https://github.com/tikv/tikv/issues/18124) @[3pointer](https://github.com/3pointer)

+ PD

    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

+ TiFlash

    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

+ Tools

    + Backup & Restore (BR)

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

    + TiCDC

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

    + TiDB Data Migration (DM)

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

    + TiDB Lightning

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

    + Dumpling

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

    + TiUP

        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

## Bug fixes

+ TiDB

    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
    - (dup): release-9.0.0.md > Bug fixes> TiDB - Fix the potential OOM issue when querying `information_schema.tables` by improving memory usage monitoring when quering system tables [#58985](https://github.com/pingcap/tidb/issues/58985) @[tangenta](https://github.com/tangenta)

+ TiKV

    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/tikv/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

+ PD

    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/tikv/pd/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

+ TiFlash

    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
    - note [#issue](https://github.com/pingcap/tiflash/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

+ Tools

    + Backup & Restore (BR)

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

    + TiCDC

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

    + TiDB Data Migration (DM)

        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiflow/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

    + TiDB Lightning

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

    + Dumpling

        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tidb/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

    + TiUP

        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})
        - note [#issue](https://github.com/pingcap/tiup/issues/${issue-id}) @[Contributor GitHub ID](https://github.com/${github-id})

## Other dup notes

- (dup): release-9.0.0.md > # Observability * Add storage engine identifiers to statement summary tables and slow query logs [#61736](https://github.com/pingcap/tidb/issues/61736) @[henrybw](https://github.com/henrybw) **tw@Oreoxmt**<!--2034 beta.2-->
