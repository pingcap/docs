---
title: TiDB Global Sort
summary: 了解 TiDB Global Sort 的使用场景、限制、用法和实现原理。
---

<!-- markdownlint-disable MD029 -->
<!-- markdownlint-disable MD046 -->

# TiDB Global Sort

> **Note:**
>
> - 目前，Global Sort 过程会消耗 TiDB 节点大量的计算和内存资源。在如在用户业务应用运行时在线添加索引等场景中，建议向集群中添加新的 TiDB 节点，配置这些节点的 [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740) 变量，并连接到这些节点以创建任务。这样，分布式框架会调度任务到这些节点，隔离工作负载，减少执行后台任务（如 `ADD INDEX` 和 `IMPORT INTO`）对用户业务应用的影响。
> - 使用 Global Sort 功能时，建议使用 CPU 至少为 16 核、内存为 32 GiB 的 TiDB 节点，以避免 OOM。

> **Note:**
>
> 该功能在 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

## 概述

TiDB Global Sort 功能增强了数据导入和 DDL（数据定义语言）操作的稳定性和效率。它作为 [TiDB 分布式执行框架（DXF）](/tidb-distributed-execution-framework.md) 的通用操作器，为云端提供全局排序服务。

目前，Global Sort 功能支持使用 Amazon S3 作为云存储。

## 使用场景

Global Sort 功能提升了 `IMPORT INTO` 和 `CREATE INDEX` 的稳定性和效率。通过对任务处理的数据进行全局排序，改善了写入 TiKV 的稳定性、可控性和可扩展性。这为数据导入和 DDL 任务提供了更优的用户体验和更高质量的服务。

Global Sort 功能在统一的 DXF 中执行任务，确保数据在全球范围内高效、并行地排序。

## 限制

目前，Global Sort 功能尚未作为排序查询结果的查询执行过程中的组件使用。

## 用法

启用 Global Sort，请按照以下步骤操作：

1. 通过将 [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710) 设置为 `ON` 来启用 DXF。从 v8.1.0 版本开始，该变量默认启用。对于新创建的 v8.1.0 或更高版本的集群，可以跳过此步骤。

    ```sql
    SET GLOBAL tidb_enable_dist_task = ON;
    ```

<CustomContent platform="tidb">

2. 将 [`tidb_cloud_storage_uri`](/system-variables.md#tidb_cloud_storage_uri-new-in-v740) 设置为正确的云存储路径。参见 [示例](/br/backup-and-restore-storages.md)。

    ```sql
    SET GLOBAL tidb_cloud_storage_uri = 's3://my-bucket/test-data?role-arn=arn:aws:iam::888888888888:role/my-role'
    ```

</CustomContent>
<CustomContent platform="tidb-cloud">

2. 将 [`tidb_cloud_storage_uri`](/system-variables.md#tidb_cloud_storage_uri-new-in-v740) 设置为正确的云存储路径。参见 [示例](https://docs.pingcap.com/tidb/stable/backup-and-restore-storages)。

    ```sql
    SET GLOBAL tidb_cloud_storage_uri = 's3://my-bucket/test-data?role-arn=arn:aws:iam::888888888888:role/my-role'
    ```

</CustomContent>

> **Note:**
>
> 对于 [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)，你也可以使用 [`CLOUD_STORAGE_URI`](/sql-statements/sql-statement-import-into.md#withoptions) 选项指定云存储路径。如果同时配置了 [`tidb_cloud_storage_uri`](/system-variables.md#tidb_cloud_storage_uri-new-in-v740) 和 `CLOUD_STORAGE_URI`，且两者都指向有效的云存储路径，则以 `CLOUD_STORAGE_URI` 的配置为准。

## 实现原理

Global Sort 功能的算法如下：

![Algorithm of Global Sort](/media/dist-task/global-sort.jpeg)

详细的实现原理如下：

### Step 1: 扫描和准备数据

1. 在 TiDB 节点扫描特定范围的数据后（数据源可以是 CSV 数据或 TiKV 中的表数据）：

    1. TiDB 节点将其编码为 Key-Value 对。
    2. TiDB 节点将 Key-Value 对排序成多个块数据段（数据段在本地排序），每个段为一个文件，并上传到云存储。

2. 同时，TiDB 节点还会为每个段记录一个连续的实际 Key-Value 范围（称为统计文件），这是实现可扩展排序的关键准备。这些文件会与实际数据一同上传到云存储。

### Step 2: 排序和分发数据

从步骤 1，Global Sort 程序获得已排序块列表及其对应的统计文件，这些文件提供了本地排序块的数量。程序还拥有一个实际数据范围，可供 PD 用于拆分和分散。接下来执行：

1. 将统计文件中的记录排序，划分为几乎相等的范围，这些范围作为子任务，将在并行中执行。
2. 将子任务分发到 TiDB 节点进行执行。
3. 每个 TiDB 节点独立地将子任务中的数据排序到范围内，并无重叠地导入到 TiKV。