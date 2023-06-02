---
title: TiDB Backend Task Distributed Execution Framework
summary: Learn the use cases, limitations, usage, and implementation principles of the TiDB backend task distributed execution framework.
---

# TiDB Backend Task Distributed Execution Framework

> **Warning:**
>
> This feature is an experimental feature. It is not recommended to use it in production environments.

<CustomContent platform="tidb-cloud">

> **Note:**
>
> Currently, this feature is only applicable to TiDB Dedicated clusters. You cannot use it on TiDB Serverless clusters.

</CustomContent>

TiDB adopts a computing-storage separation architecture with excellent scalability and elasticity. Starting from v7.1.0, TiDB introduces a backend task distributed execution framework to further leverage the resource advantages of the distributed architecture. The goal of this framework is to implement unified scheduling and distributed execution of all backend tasks, and to provide unified resource management capabilities for both overall and individual backend tasks, which better meets users' expectations for resource usage.

This document describes the use cases, limitations, usage, and implementation principles of the TiDB backend task distributed execution framework.

> **Note:**
>
> This framework does not support the distributed execution of SQL queries.

## Use cases and limitations

In a database management system, in addition to the core transactional processing (TP) and analytical processing (AP) workloads, there are other important tasks, such as DDL operations, Load Data, TTL, Analyze, and Backup/Restore, which are called **backend tasks**. These backend tasks need to process a large amount of data in database objects (tables), so they typically have the following characteristics:

- Need to process all data in a schema or a database object (table).
- Might need to be executed periodically, but at a low frequency.
- If the resources are not properly controlled, they are prone to affect TP and AP tasks, lowering the database service quality.

Enabling the TiDB backend task distributed execution framework can solve the above problems and has the following three advantages:

- The framework provides unified capabilities for high scalability, high availability, and high performance.
- The framework supports distributed execution of backend tasks, which can flexibly schedule the available computing resources of the entire TiDB cluster, thereby better utilizing the computing resources in a TiDB cluster.
- The framework provides unified resource usage and management capabilities for both overall and individual backend tasks.

Currently, the TiDB backend task distributed execution framework only supports the distributed execution of `ADD INDEX` statements, that is, the DDL statements for creating indexes. For example, the following SQL statements are supported:

```sql
ALTER TABLE t1 ADD INDEX idx1(c1);
CREATE INDEX idx1 ON table t1(c1);
```

## Prerequisites

Before using the distributed framework, you need to enable the [Fast Online DDL](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630) mode.

<CustomContent platform="tidb">

1. Adjust the following system variables related to Fast Online DDL:

    * [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630): used to enable Fast Online DDL mode. It is enabled by default starting from TiDB v6.5.0.
    * [`tidb_ddl_disk_quota`](/system-variables.md#tidb_ddl_disk_quota-new-in-v630): used to control the maximum quota of local disks that can be used in Fast Online DDL mode.

2. Adjust the following configuration item related to Fast Online DDL:

    * [`temp-dir`](/tidb-configuration-file.md#temp-dir-new-in-v630): specifies the local disk path that can be used in Fast Online DDL mode.

> **Note:**
>
> Before you upgrade TiDB to v6.5.0 or later, it is recommended that you check whether the [`temp-dir`](/tidb-configuration-file.md#temp-dir-new-in-v630) path of TiDB is correctly mounted to an SSD disk. This path is a TiDB configuration item, which takes effect after TiDB is restarted. Therefore, setting this configuration item in advance before upgrading can avoid another restart.

</CustomContent>

<CustomContent platform="tidb-cloud">

Adjust the following system variables related to Fast Online DDL:

* [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630): used to enable Fast Online DDL mode. It is enabled by default starting from TiDB v6.5.0.
* [`tidb_ddl_disk_quota`](/system-variables.md#tidb_ddl_disk_quota-new-in-v630): used to control the maximum quota of local disks that can be used in Fast Online DDL mode.

</CustomContent>

## Usage

1. To enable the distributed framework, set the value of [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710) to `ON`:

    ```sql
    SET GLOBAL tidb_enable_dist_task = ON;
    ```

    When backend tasks are running, the DDL statements supported by the framework are executed in a distributed manner.

2. Adjust the following system variables that might affect the distributed execution of DDL tasks according to your needs:

    * [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt): use the default value `4`. The recommended maximum value is `16`.
    * [`tidb_ddl_reorg_priority`](/system-variables.md#tidb_ddl_reorg_priority)
    * [`tidb_ddl_error_count_limit`](/system-variables.md#tidb_ddl_error_count_limit)
    * [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size): use the default value. The recommended maximum value is `1024`.

> **Tip:**
>
> For distributed execution of `ADD INDEX` statements, you only need to set `tidb_ddl_reorg_worker_cnt`.

## Implementation principles

The architecture of the TiDB backend task distributed execution framework is as follows:

![Architecture of the TiDB backend task distributed execution framework](/media/dist-task/dist-task-architect.jpg)

As shown in the preceding diagram, the execution of backend tasks in the distributed framework is mainly handled by the following modules:

- Dispatcher: generates the distributed execution plan for each task, manages the execution process, converts the task status, and collects and feeds back the runtime task information.
- Scheduler: replicates the execution of distributed tasks among TiDB nodes to improve the efficiency of backend task execution.
- Subtask Executor: the actual executor of distributed subtasks. In addition, the Subtask Executor returns the execution status of subtasks to the Scheduler, and the Scheduler updates the execution status of subtasks in a unified manner.
- Resource pool: provides the basis for quantifying resource usage and management by pooling computing resources of the above modules.

## See also

<CustomContent platform="tidb">

* [Execution Principles and Best Practices of DDL Statements](/ddl-introduction.md)

</CustomContent>
<CustomContent platform="tidb-cloud">

* [Execution Principles and Best Practices of DDL Statements](https://docs.pingcap.com/tidb/stable/ddl-introduction)

</CustomContent>
