---
title: TiDB Distributed eXecution Framework (DXF)
summary: Learn the use cases, limitations, usage, and implementation principles of the TiDB Distributed eXecution Framework (DXF).
---

# TiDB Distributed eXecution Framework (DXF)

> **Note:**
>
> This feature is not available on [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) clusters.

TiDB adopts a computing-storage separation architecture with excellent scalability and elasticity. Starting from v7.1.0, TiDB introduces a **Distributed eXecution Framework (DXF)** to further leverage the resource advantages of the distributed architecture. The goal of the DXF is to implement unified scheduling and distributed execution of tasks, and to provide unified resource management capabilities for both overall and individual tasks, which better meets users' expectations for resource usage.

This document describes the use cases, limitations, usage, and implementation principles of the DXF.

## Use cases

In a database management system, in addition to the core transactional processing (TP) and analytical processing (AP) workloads, there are other important tasks, such as DDL operations, [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md), [TTL](/time-to-live.md), [`ANALYZE`](/sql-statements/sql-statement-analyze-table.md), and Backup/Restore. These tasks need to process a large amount of data in database objects (tables), so they typically have the following characteristics:

- Need to process all data in a schema or a database object (table).
- Might need to be executed periodically, but at a low frequency.
- If the resources are not properly controlled, they are prone to affect TP and AP tasks, lowering the database service quality.

Enabling the DXF can solve the above problems and has the following three advantages:

- The framework provides unified capabilities for high scalability, high availability, and high performance.
- The DXF supports distributed execution of tasks, which can flexibly schedule the available computing resources of the entire TiDB cluster, thereby better utilizing the computing resources in a TiDB cluster.
- The DXF provides unified resource usage and management capabilities for both overall and individual tasks.

Currently, the DXF supports the distributed execution of the [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) and [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) statements.

- [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) is a DDL statement used to create indexes. For example:

    ```sql
    ALTER TABLE t1 ADD INDEX idx1(c1);
    CREATE INDEX idx1 ON table t1(c1);
    ```

- [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) is used to import data in formats such as CSV, SQL, and Parquet into an empty table.

## Limitation

The DXF can only schedule up to 16 tasks (including [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) tasks and [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) tasks) simultaneously.

## Prerequisites

Before using the DXF to execute [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) tasks, you need to enable the [Fast Online DDL](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) mode.

<CustomContent platform="tidb">

1. Adjust the following system variables related to Fast Online DDL:

    * [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630): used to enable Fast Online DDL mode. It is enabled by default starting from TiDB v6.5.0.
    * [`tidb_ddl_disk_quota`](/system-variables.md#tidb_ddl_disk_quota-new-in-v630): used to control the maximum quota of local disks that can be used in Fast Online DDL mode.

2. Adjust the following configuration item related to Fast Online DDL:

    * [`temp-dir`](/tidb-configuration-file.md#temp-dir-new-in-v630): specifies the local disk path that can be used in Fast Online DDL mode.

> **Note:**
>
> It is recommended that you prepare at least 100 GiB of free space for the TiDB `temp-dir` directory.

</CustomContent>

<CustomContent platform="tidb-cloud">

Adjust the following system variables related to Fast Online DDL:

* [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630): used to enable Fast Online DDL mode. It is enabled by default starting from TiDB v6.5.0.
* [`tidb_ddl_disk_quota`](/system-variables.md#tidb_ddl_disk_quota-new-in-v630): used to control the maximum quota of local disks that can be used in Fast Online DDL mode.

</CustomContent>

## Usage

1. To enable the DXF, set the value of [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710) to `ON`. Starting from v8.1.0, this variable is enabled by default. For newly created clusters of v8.1.0 or later versions, you can skip this step.

    ```sql
    SET GLOBAL tidb_enable_dist_task = ON;
    ```

    When the DXF tasks are running, the statements supported by the framework (such as [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) and [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)) are executed in a distributed manner. All TiDB nodes run DXF tasks by default.

2. In general, for the following system variables that might affect the distributed execution of DDL tasks, it is recommended that you use their default values:

    * [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt): use the default value `4`. The recommended maximum value is `16`.
    * [`tidb_ddl_reorg_priority`](/system-variables.md#tidb_ddl_reorg_priority)
    * [`tidb_ddl_error_count_limit`](/system-variables.md#tidb_ddl_error_count_limit)
    * [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size): use the default value. The recommended maximum value is `1024`.

## Task scheduling

By default, the DXF schedules all TiDB nodes to execute distributed tasks. Starting from v7.4.0, for TiDB Self-Managed clusters, you can control which TiDB nodes can be scheduled by the DXF to execute distributed tasks by configuring [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740).

- For versions from v7.4.0 to v8.0.0, the optional values of [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740) are `''` or `background`. If the current cluster has TiDB nodes with `tidb_service_scope = 'background'`, the DXF schedules tasks to these nodes for execution. If the current cluster does not have TiDB nodes with `tidb_service_scope = 'background'`, whether due to faults or normal scaling in, the DXF schedules tasks to nodes with `tidb_service_scope = ''` for execution.

- Starting from v8.1.0, you can set [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740) to any valid value. When a distributed task is submitted, the task binds to the [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740) value of the currently connected TiDB node, and the DXF only schedules the task to the TiDB nodes with the same [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740) value for execution. However, for configuration compatibility with earlier versions, if a distributed task is submitted on a node with `tidb_service_scope = ''` and the current cluster has TiDB nodes with `tidb_service_scope = 'background'`, the DXF schedules the task to TiDB nodes with `tidb_service_scope = 'background'` for execution.

Starting from v8.1.0, if new nodes are added during task execution, the DXF determines whether to schedule tasks to the new nodes for execution based on the preceding rules. If you do not want newly added nodes to execute tasks, it is recommended to set a different [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740) for those newly added nodes in advance.

> **Note:**
>
> - For versions from v7.4.0 to v8.0.0, in clusters with multiple TiDB nodes, it is strongly recommended to set [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740) to `background` on two or more TiDB nodes. If this variable is set only on a single TiDB node, when that node restarts or fails, tasks will be rescheduled to TiDB nodes with `tidb_service_scope = ''`, which affects applications running on these TiDB nodes.
> - During the execution of a distributed task, changes to the [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740) configuration do not take effect for the current task, but take effect from the next task.

## Implementation principles

The architecture of the DXF is as follows:

![Architecture of the DXF](/media/dist-task/dist-task-architect.jpg)

As shown in the preceding diagram, the execution of tasks in the DXF is mainly handled by the following modules:

- Dispatcher: generates the distributed execution plan for each task, manages the execution process, converts the task status, and collects and feeds back the runtime task information.
- Scheduler: replicates the execution of distributed tasks among TiDB nodes to improve the efficiency of task execution.
- Subtask Executor: the actual executor of distributed subtasks. In addition, the Subtask Executor returns the execution status of subtasks to the Scheduler, and the Scheduler updates the execution status of subtasks in a unified manner.
- Resource pool: provides the basis for quantifying resource usage and management by pooling computing resources of the above modules.

## See also

<CustomContent platform="tidb">

* [Execution Principles and Best Practices of DDL Statements](/ddl-introduction.md)

</CustomContent>
<CustomContent platform="tidb-cloud">

* [Execution Principles and Best Practices of DDL Statements](https://docs.pingcap.com/tidb/stable/ddl-introduction)

</CustomContent>