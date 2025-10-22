---
title: TiDB 分布式执行框架（DXF）
summary: 了解 TiDB 分布式执行框架（DXF）的使用场景、限制、用法和实现原理。
---

# TiDB 分布式执行框架（DXF）

> **Note:**
>
> 该功能不适用于 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群。

TiDB 采用计算与存储分离的架构，具备出色的可扩展性和弹性。从 v7.1.0 开始，TiDB 引入了 **分布式执行框架（DXF）**，以进一步发挥分布式架构的资源优势。DXF 的目标是实现任务的统一调度与分布式执行，并为整体和单个任务提供统一的资源管理能力，更好地满足用户对资源使用的预期。

本文档介绍了 DXF 的使用场景、限制、用法和实现原理。

## 使用场景

在数据库管理系统中，除了核心的事务处理（TP）和分析处理（AP）负载外，还有其他重要任务，例如 DDL 操作、[`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)、[TTL](/time-to-live.md)、[`ANALYZE`](/sql-statements/sql-statement-analyze-table.md) 以及备份/恢复。这些任务需要处理数据库对象（表）中的大量数据，因此通常具有以下特点：

- 需要处理某个 schema 或数据库对象（表）中的全部数据。
- 可能需要周期性执行，但频率较低。
- 如果资源控制不当，容易影响 TP 和 AP 任务，降低数据库服务质量。

启用 DXF 可以解决上述问题，并具备以下三大优势：

- 框架提供统一的高扩展性、高可用性和高性能能力。
- DXF 支持任务的分布式执行，可以灵活调度整个 TiDB 集群的可用计算资源，从而更好地利用 TiDB 集群中的计算资源。
- DXF 为整体和单个任务提供统一的资源使用和管理能力。

目前，DXF 支持 [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) 和 [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) 语句的分布式执行。

- [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) 是用于创建索引的 DDL 语句。例如：

    ```sql
    ALTER TABLE t1 ADD INDEX idx1(c1);
    CREATE INDEX idx1 ON table t1(c1);
    ```

- [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) 用于将 CSV、SQL、Parquet 等格式的数据导入到空表中。

## 限制

DXF 最多只能同时调度 16 个任务（包括 [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) 任务和 [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) 任务）。

## 前置条件

在使用 DXF 执行 [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) 任务前，你需要开启 [Fast Online DDL](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) 模式。

<CustomContent platform="tidb">

1. 调整以下与 Fast Online DDL 相关的系统变量：

    * [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)：用于开启 Fast Online DDL 模式。从 TiDB v6.5.0 起默认开启。
    * [`tidb_ddl_disk_quota`](/system-variables.md#tidb_ddl_disk_quota-new-in-v630)：用于控制 Fast Online DDL 模式下可使用的本地磁盘最大配额。

2. 调整以下与 Fast Online DDL 相关的配置项：

    * [`temp-dir`](/tidb-configuration-file.md#temp-dir-new-in-v630)：指定 Fast Online DDL 模式下可使用的本地磁盘路径。

> **Note:**
>
> 建议你为 TiDB 的 `temp-dir` 目录预留至少 100 GiB 的可用空间。

</CustomContent>

<CustomContent platform="tidb-cloud">

调整以下与 Fast Online DDL 相关的系统变量：

* [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)：用于开启 Fast Online DDL 模式。从 TiDB v6.5.0 起默认开启。
* [`tidb_ddl_disk_quota`](/system-variables.md#tidb_ddl_disk_quota-new-in-v630)：用于控制 Fast Online DDL 模式下可使用的本地磁盘最大配额。

</CustomContent>

## 使用方法

1. 要启用 DXF，请将 [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710) 的值设置为 `ON`。从 v8.1.0 起，该变量默认开启。对于 v8.1.0 及以上版本新建的集群，可以跳过此步骤。

    ```sql
    SET GLOBAL tidb_enable_dist_task = ON;
    ```

    当 DXF 任务运行时，框架支持的语句（如 [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) 和 [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)）将以分布式方式执行。所有 TiDB 节点默认都会运行 DXF 任务。

2. 通常，对于以下可能影响 DDL 任务分布式执行的系统变量，建议你使用默认值：

    * [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)：使用默认值 `4`，推荐最大值为 `16`。
    * [`tidb_ddl_reorg_priority`](/system-variables.md#tidb_ddl_reorg_priority)
    * [`tidb_ddl_error_count_limit`](/system-variables.md#tidb_ddl_error_count_limit)
    * [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size)：使用默认值，推荐最大值为 `1024`。

## 任务调度

默认情况下，DXF 会调度所有 TiDB 节点执行分布式任务。从 v7.4.0 起，对于 TiDB 自建集群，你可以通过配置 [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740) 控制哪些 TiDB 节点可以被 DXF 调度执行分布式任务。

- 在 v7.4.0 到 v8.0.0 版本中，[`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740) 的可选值为 `''` 或 `background`。如果当前集群中存在 `tidb_service_scope = 'background'` 的 TiDB 节点，DXF 会将任务调度到这些节点执行。如果当前集群没有 `tidb_service_scope = 'background'` 的 TiDB 节点（无论是由于故障还是正常缩容），DXF 会将任务调度到 `tidb_service_scope = ''` 的节点执行。

- 从 v8.1.0 起，你可以将 [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740) 设置为任意有效值。当分布式任务提交时，任务会绑定到当前连接 TiDB 节点的 [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740) 值，DXF 只会将任务调度到具有相同 [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740) 值的 TiDB 节点执行。但为了兼容早期版本的配置，如果在 `tidb_service_scope = ''` 的节点上提交分布式任务，且当前集群存在 `tidb_service_scope = 'background'` 的 TiDB 节点，DXF 会将任务调度到 `tidb_service_scope = 'background'` 的 TiDB 节点执行。

从 v8.1.0 起，如果在任务执行期间新增节点，DXF 会根据上述规则判断是否将任务调度到新节点执行。如果你不希望新增节点参与任务执行，建议提前为这些新节点设置不同的 [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740)。

> **Note:**
>
> - 在 v7.4.0 到 v8.0.0 版本中，对于多 TiDB 节点的集群，强烈建议在两个及以上 TiDB 节点上将 [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740) 设置为 `background`。如果只在单个 TiDB 节点上设置该变量，当该节点重启或故障时，任务会被重新调度到 `tidb_service_scope = ''` 的 TiDB 节点，进而影响这些节点上运行的应用。
> - 分布式任务执行期间，[`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740) 配置的变更不会影响当前任务，但会在下一个任务生效。

## 实现原理

DXF 的架构如下所示：

![Architecture of the DXF](/media/dist-task/dist-task-architect.jpg)

如上图所示，DXF 中任务的执行主要由以下模块负责：

- Dispatcher：为每个任务生成分布式执行计划，管理执行流程，转换任务状态，并收集和反馈运行时任务信息。
- Scheduler：在 TiDB 节点间复制分布式任务的执行，以提升任务执行效率。
- Subtask Executor：分布式子任务的实际执行者。此外，Subtask Executor 会将子任务的执行状态返回给 Scheduler，由 Scheduler 统一更新子任务的执行状态。
- 资源池：通过对上述模块的计算资源进行池化，为资源使用量化和管理提供基础。

## 参考

<CustomContent platform="tidb">

* [DDL 语句的执行原理与最佳实践](/ddl-introduction.md)

</CustomContent>
<CustomContent platform="tidb-cloud">

* [DDL 语句的执行原理与最佳实践](https://docs.pingcap.com/tidb/stable/ddl-introduction)

</CustomContent>