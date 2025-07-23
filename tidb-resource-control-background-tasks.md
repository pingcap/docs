---
title: 使用资源控制管理后台任务
summary: 介绍如何通过资源控制管理后台任务。
---

# 使用资源控制管理后台任务

> **Warning:**
>
> 该功能为实验性功能。不建议在生产环境中使用。此功能可能在未提前通知的情况下被更改或移除。如果你发现 bug，可以在 GitHub 上提交 [issue](https://docs.pingcap.com/tidb/stable/support)。
>
> 资源控制中的后台任务管理基于 TiKV 对 CPU/IO 利用率的动态资源配额调整。因此，它依赖于每个实例的可用资源配额。如果在一台服务器上部署多个组件或实例，必须通过 `cgroup` 为每个实例设置合适的资源配额。在使用 TiUP Playground 等共享资源的部署环境中，难以达到预期效果。

> **Note:**
>
> 该功能在 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

后台任务，例如数据备份和自动统计信息收集，优先级较低但会消耗大量资源。这些任务通常周期性或不定期触发。在执行过程中，它们会占用大量资源，从而影响线上高优先级任务的性能。

从 v7.4.0 版本开始，[TiDB 资源控制](/tidb-resource-control-ru-groups.md) 功能支持管理后台任务。当某个任务被标记为后台任务时，TiKV 会动态限制此类任务的资源使用，以避免影响其他前台任务的性能。TiKV 会实时监控所有前台任务的 CPU 和 IO 资源消耗，并根据实例的总资源限制计算后台任务可用的资源阈值。在任务执行期间，所有后台任务都受到此阈值的限制。

## `BACKGROUND` 参数

- `TASK_TYPES`：指定需要作为后台任务管理的任务类型。多个任务类型之间用逗号（`,`）分隔。
- `UTILIZATION_LIMIT`：限制后台任务在每个 TiKV 节点上最多可占用的资源百分比（0-100）。默认情况下，TiKV 会根据节点的总资源和当前被前台任务占用的资源，自动计算后台任务的可用资源。如果配置了 `UTILIZATION_LIMIT`，后台任务所分配的资源不会超过此限制。

TiDB 支持以下类型的后台任务：

<CustomContent platform="tidb">

- `lightning`：使用 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 进行导入任务。支持 TiDB Lightning 的物理和逻辑导入模式。
- `br`：使用 [BR](/br/backup-and-restore-overview.md) 进行备份和恢复任务。不支持 PITR。
- `ddl`：控制 Reorg DDL 执行过程中批量数据写回阶段的资源使用。
- `stats`：由 TiDB 手动执行或自动触发的 [收集统计信息](/statistics.md#collect-statistics) 任务。
- `background`：保留任务类型。你可以使用 [`tidb_request_source_type`](/system-variables.md#tidb_request_source_type-new-in-v740) 系统变量，将当前会话的任务类型指定为 `background`。

</CustomContent>

<CustomContent platform="tidb-cloud">

- `lightning`：使用 [TiDB Lightning](https://docs.pingcap.com/tidb/stable/tidb-lightning-overview) 进行导入任务。支持 TiDB Lightning 的物理和逻辑导入模式。
- `br`：使用 [BR](https://docs.pingcap.com/tidb/stable/backup-and-restore-overview) 进行备份和恢复任务。不支持 PITR。
- `ddl`：控制 Reorg DDL 执行过程中批量数据写回阶段的资源使用。
- `stats`：由 TiDB 手动执行或自动触发的 [收集统计信息](/statistics.md#collect-statistics) 任务。
- `background`：保留任务类型。你可以使用 [`tidb_request_source_type`](/system-variables.md#tidb_request_source_type-new-in-v740) 系统变量，将当前会话的任务类型指定为 `background`。

</CustomContent>

默认情况下，标记为后台任务的任务类型为 `""`，后台任务管理功能处于禁用状态。要启用后台任务管理，你需要手动修改 `default` 资源组的后台任务类型。当后台任务被识别并匹配后，资源控制会自动进行管理。这意味着当系统资源不足时，后台任务会自动降到最低优先级，以确保前台任务的正常执行。

> **Note:**
>
> 目前，所有资源组的后台任务都绑定到 `default` 资源组。你可以通过 `default` 全局管理后台任务类型，目前不支持将后台任务绑定到其他资源组。

## 示例

1. 修改 `default` 资源组，将 `br` 和 `ddl` 标记为后台任务，并将后台任务的资源限制设置为 30%。

    ```sql
    ALTER RESOURCE GROUP `default` BACKGROUND=(TASK_TYPES='br,ddl', UTILIZATION_LIMIT=30);
    ```

2. 将 `default` 资源组改回，恢复后台任务类型为默认值。

    ```sql
    ALTER RESOURCE GROUP `default` BACKGROUND=NULL;
    ```

3. 将 `default` 资源组改为将后台任务类型设置为空。在这种情况下，该资源组的所有任务都不作为后台任务处理。

    ```sql
    ALTER RESOURCE GROUP `default` BACKGROUND=(TASK_TYPES="");
    ```

4. 查看 `default` 资源组的后台任务类型。

    ```sql
    SELECT * FROM information_schema.resource_groups WHERE NAME="default";
    ```

    输出如下：

    ```
    +---------+------------+----------+-----------+-------------+-------------------------------------------+
    | NAME    | RU_PER_SEC | PRIORITY | BURSTABLE | QUERY_LIMIT | BACKGROUND                                |
    +---------+------------+----------+-----------+-------------+-------------------------------------------+
    | default | UNLIMITED  | MEDIUM   | YES       | NULL        | TASK_TYPES='br,ddl', UTILIZATION_LIMIT=30 |
    +---------+------------+----------+-----------+-------------+-------------------------------------------+
    ```

5. 若要在当前会话中明确将任务标记为后台类型，可以使用 `tidb_request_source_type` 显式指定任务类型。示例如下：

    ```sql
    SET @@tidb_request_source_type="background";
    /* 添加后台任务类型 */
    ALTER RESOURCE GROUP `default` BACKGROUND=(TASK_TYPES="background");
    /* 在当前会话中执行 LOAD DATA */
    LOAD DATA INFILE "s3://resource-control/Lightning/test.customer.aaaa.csv"
    ```