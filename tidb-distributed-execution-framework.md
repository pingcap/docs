---
title: TiDB 分布式执行框架（DXF）
summary: 了解 TiDB 分布式执行框架（DXF）的使用场景、限制、用法和实现原理。
---

# TiDB 分布式执行框架（DXF）

> **Note:**
>
> 该功能在 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

TiDB 采用计算与存储分离的架构，具有出色的可扩展性和弹性。从 v7.1.0 版本开始，TiDB 引入了 **Distributed eXecution Framework (DXF)**，以进一步发挥分布式架构的资源优势。DXF 的目标是实现任务的统一调度和分布式执行，并为整体和单个任务提供统一的资源管理能力，更好地满足用户对资源使用的预期。

本文档描述了 DXF 的使用场景、限制、用法和实现原理。

## 使用场景

在数据库管理系统中，除了核心的事务处理（TP）和分析处理（AP）工作负载外，还有其他重要任务，例如 DDL 操作、[`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)、[TTL](/time-to-live.md)、[`ANALYZE`](/sql-statements/sql-statement-analyze-table.md) 和备份/恢复。这些任务需要处理数据库对象（表）中的大量数据，因此通常具有以下特征：

- 需要处理某个 schema 或数据库对象（表）中的所有数据。
- 可能需要定期执行，但频率较低。
- 如果资源控制不当，容易影响 TP 和 AP 任务，降低数据库服务质量。

启用 DXF 可以解决上述问题，具有以下三大优势：

- 框架提供高扩展性、高可用性和高性能的统一能力。
- DXF 支持任务的分布式执行，能够灵活调度整个 TiDB 集群的可用计算资源，从而更好地利用 TiDB 集群中的计算资源。
- DXF 为整体和单个任务提供统一的资源使用和管理能力。

目前，DXF 支持 [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) 和 [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) 语句的分布式执行。

- [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) 是用于创建索引的 DDL 语句。例如：

    ```sql
    ALTER TABLE t1 ADD INDEX idx1(c1);
    CREATE INDEX idx1 ON table t1(c1);
    ```

- [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) 用于将 CSV、SQL、Parquet 等格式的数据导入空表。

## 限制

DXF 只能同时调度最多 16 个任务（包括 [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) 任务和 [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) 任务）。

## 前提条件

在使用 DXF 执行 [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) 任务之前，需要启用 [Fast Online DDL](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) 模式。

<CustomContent platform="tidb">

1. 调整以下与 Fast Online DDL 相关的系统变量：

    * [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)：用于启用 Fast Online DDL 模式。从 TiDB v6.5.0 开始默认启用。
    * [`tidb_ddl_disk_quota`](/system-variables.md#tidb_ddl_disk_quota-new-in-v630)：用于控制在 Fast Online DDL 模式下可使用的本地磁盘最大配额。

2. 调整以下与 Fast Online DDL 相关的配置项：

    * [`temp-dir`](/tidb-configuration-file.md#temp-dir-new-in-v630)：指定在 Fast Online DDL 模式下可用的本地磁盘路径。

> **Note:**
>
> 建议为 TiDB 的 `temp-dir` 目录准备至少 100 GiB 的空闲空间。

</CustomContent>

<CustomContent platform="tidb-cloud">

调整以下与 Fast Online DDL 相关的系统变量：

* [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)：用于启用 Fast Online DDL 模式。从 TiDB v6.5.0 开始默认启用。
* [`tidb_ddl_disk_quota`](/system-variables.md#tidb_ddl_disk_quota-new-in-v630)：用于控制在 Fast Online DDL 模式下可使用的本地磁盘最大配额。

</CustomContent>

## 用法

1. 要启用 DXF，将 [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710) 的值设置为 `ON`。从 v8.1.0 版本开始，该变量默认启用。对于新创建的 v8.1.0 或更高版本的集群，可以跳过此步骤。

    ```sql
    SET GLOBAL tidb_enable_dist_task = ON;
    ```

    当 DXF 任务运行时，框架支持的语句（如 [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) 和 [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)）会以分布式方式执行。所有 TiDB 节点默认运行 DXF 任务。

2. 一般情况下，建议使用以下可能影响 DDL 任务分布式执行的系统变量的默认值：

    * [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)：使用默认值 `4`。建议最大值为 `16`。
    * [`tidb_ddl_reorg_priority`](/system-variables.md#tidb_ddl_reorg_priority)
    * [`tidb_ddl_error_count_limit`](/system-variables.md#tidb_ddl_error_count_limit)
    * [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size)：使用默认值。建议最大值为 `1024`。

## 任务调度

默认情况下，DXF 调度所有 TiDB 节点执行分布式任务。从 v7.4.0 版本开始，对于 TiDB 自管理集群，可以通过配置 [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740) 来控制哪些 TiDB 节点可以被 DXF 调度执行分布式任务。

- 从 v7.4.0 到 v8.0.0 版本，`tidb_service_scope` 的可选值为 `''` 或 `background`。如果当前集群中存在 `tidb_service_scope = 'background'` 的 TiDB 节点，DXF 会调度任务到这些节点执行。如果没有，或者由于故障或正常扩容，DXF 会调度任务到 `tidb_service_scope = ''` 的节点。

- 从 v8.1.0 开始，可以将 [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740) 设置为任何有效值。当提交分布式任务时，任务会绑定到当前连接的 TiDB 节点的 [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740) 值，DXF 只会调度任务到具有相同 [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740) 值的 TiDB 节点执行。然而，为了与早期版本的配置兼容，如果在 `tidb_service_scope = ''` 的节点上提交分布式任务，且当前集群中存在 `tidb_service_scope = 'background'` 的 TiDB 节点，DXF 会调度任务到 `tidb_service_scope = 'background'` 的节点执行。

从 v8.1.0 开始，如果在任务执行过程中新增节点，DXF 会根据之前的规则判断是否调度任务到新节点。如果不希望新加入的节点执行任务，建议提前为这些新加入的节点设置不同的 [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740)。

> **Note:**
>
> - 从 v7.4.0 到 v8.0.0 版本，在拥有多个 TiDB 节点的集群中，强烈建议在两个或更多 TiDB 节点上将 [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740) 设置为 `background`。如果只在单个 TiDB 节点上设置该变量，当该节点重启或故障时，任务会被重新调度到 [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740) 为 `''` 的节点，影响在这些节点上运行的应用。
> - 在分布式任务执行期间，修改 [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740) 配置不会影响当前任务，但会在下一个任务中生效。

## 实现原理

DXF 的架构如下：

![Architecture of the DXF](/media/dist-task/dist-task-architect.jpg)

如上图所示，DXF 中任务的执行主要由以下模块负责：

- Dispatcher：生成每个任务的分布式执行计划，管理执行过程，转换任务状态，收集并反馈运行时任务信息。
- Scheduler：在 TiDB 节点之间复制分布式任务的执行，以提高任务执行效率。
- Subtask Executor：分布式子任务的实际执行者。此外，子任务执行器会返回子任务的执行状态，调度器统一更新子任务的执行状态。
- Resource pool：通过池化上述模块的计算资源，为资源使用和管理提供基础。

## 相关链接

<CustomContent platform="tidb">

* [Execution Principles and Best Practices of DDL Statements](/ddl-introduction.md)

</CustomContent>
<CustomContent platform="tidb-cloud">

* [Execution Principles and Best Practices of DDL Statements](https://docs.pingcap.com/tidb/stable/ddl-introduction)

</CustomContent>