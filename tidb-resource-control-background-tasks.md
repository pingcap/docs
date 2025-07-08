---
title: Use Resource Control to Manage Background Tasks
summary: Introduces how to control background tasks through Resource Control.
---

# Use Resource Control to Manage Background Tasks

> **Warning:**
>
> This feature is experimental. It is not recommended that you use it in the production environment. This feature might be changed or removed without prior notice. If you find a bug, you can report an [issue](https://docs.pingcap.com/tidb/stable/support) on GitHub.
> 
> The background task management in resource control is based on TiKV's dynamic adjustment of resource quotas for CPU/IO utilization. Therefore, it relies on the available resource quota of each instance. If multiple components or instances are deployed on a single server, it is mandatory to set the appropriate resource quota for each instance through `cgroup`. It is difficult to achieve the expected effect in deployment with shared resources such as TiUP Playground.

Background tasks, such as data backup and automatic statistics collection, are low-priority but consume many resources. These tasks are usually triggered periodically or irregularly. During execution, they consume a lot of resources, thus affecting the performance of online high-priority tasks.

Starting from v7.4.0, the [TiDB resource control](/tidb-resource-control-ru-groups.md) feature supports managing background tasks. When a task is marked as a background task, TiKV dynamically limits the resources used by this type of task to avoid the impact on the performance of other foreground tasks. TiKV monitors the CPU and IO resources consumed by all foreground tasks in real time, and calculates the resource threshold that can be used by background tasks based on the total resource limit of the instance. All background tasks are restricted by this threshold during execution.

## `BACKGROUND` parameters

- `TASK_TYPES`: specifies the task types that need to be managed as background tasks. Use commas (`,`) to separate multiple task types.
- `UTILIZATION_LIMIT`: limits the maximum percentage (0-100) of resources that background tasks can consume on each TiKV node. By default, TiKV calculates the available resources for background tasks based on the total resources of the node and the resources currently occupied by the foreground tasks. If `UTILIZATION_LIMIT` is configured, the resource allocated to background tasks will not exceed this limit.

TiDB supports the following types of background tasks:

<CustomContent platform="tidb">

- `lightning`: perform import tasks using [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md). Both physical and logical import modes of TiDB Lightning are supported.
- `br`: perform backup and restore tasks using [BR](/br/backup-and-restore-overview.md). PITR is not supported.
- `ddl`: control the resource usage during the batch data write back phase of Reorg DDLs.
- `stats`: the [collect statistics](/statistics.md#collect-statistics) tasks that are manually executed or automatically triggered by TiDB.
- `background`: a reserved task type. You can use the [`tidb_request_source_type`](/system-variables.md#tidb_request_source_type-new-in-v740) system variable to specify the task type of the current session as `background`.

</CustomContent>

<CustomContent platform="tidb-cloud">

- `lightning`: perform import tasks using [TiDB Lightning](https://docs.pingcap.com/tidb/stable/tidb-lightning-overview). Both physical and logical import modes of TiDB Lightning are supported.
- `br`: perform backup and restore tasks using [BR](https://docs.pingcap.com/tidb/stable/backup-and-restore-overview). PITR is not supported.
- `ddl`: control the resource usage during the batch data write back phase of Reorg DDLs.
- `stats`: the [collect statistics](/statistics.md#collect-statistics) tasks that are manually executed or automatically triggered by TiDB.
- `background`: a reserved task type. You can use the [`tidb_request_source_type`](/system-variables.md#tidb_request_source_type-new-in-v740) system variable to specify the task type of the current session as `background`.

</CustomContent>

By default, the task types that are marked as background tasks are `""`, and the management of background tasks is disabled. To enable background task management, you need to manually modify the background task type of the `default` resource group. After a background task is identified and matched, Resource Control is automatically performed. This means that when system resources are insufficient, the background tasks are automatically reduced to the lowest priority to ensure the execution of foreground tasks.

> **Note:**
>
> Currently, background tasks for all resource groups are bound to the `default` resource group. You can manage background task types globally through `default`. Binding background tasks to other resource groups is currently not supported.

## Examples

1. Modify the `default` resource group by marking `br` and `ddl` as background tasks and setting the resource limit of background tasks to 30%.

    ```sql
    ALTER RESOURCE GROUP `default` BACKGROUND=(TASK_TYPES='br,ddl', UTILIZATION_LIMIT=30);
    ```

2. Change the `default` resource group to revert the background task type to its default value.

    ```sql
    ALTER RESOURCE GROUP `default` BACKGROUND=NULL;
    ```

3. Change the `default` resource group to set the background task type to empty. In this case, all tasks of this resource group are not treated as background tasks.

    ```sql
    ALTER RESOURCE GROUP `default` BACKGROUND=(TASK_TYPES="");
    ```

4. View the background task type of the `default` resource group.

    ```sql
    SELECT * FROM information_schema.resource_groups WHERE NAME="default";
    ```

    The output is as follows:

    ```
    +---------+------------+----------+-----------+-------------+-------------------------------------------+
    | NAME    | RU_PER_SEC | PRIORITY | BURSTABLE | QUERY_LIMIT | BACKGROUND                                |
    +---------+------------+----------+-----------+-------------+-------------------------------------------+
    | default | UNLIMITED  | MEDIUM   | YES       | NULL        | TASK_TYPES='br,ddl', UTILIZATION_LIMIT=30 |
    +---------+------------+----------+-----------+-------------+-------------------------------------------+
    ```

5. To explicitly mark tasks in the current session as the background type, you can use `tidb_request_source_type` to explicitly specify the task type. The following is an example:

    ``` sql
    SET @@tidb_request_source_type="background";
    /* Add background task type */
    ALTER RESOURCE GROUP `default` BACKGROUND=(TASK_TYPES="background");
    /* Execute LOAD DATA in the current session */
    LOAD DATA INFILE "s3://resource-control/Lightning/test.customer.aaaa.csv"
    ```
