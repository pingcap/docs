---
title: Execution Principles and Best Practices of DDL Statements
summary: Learn about how DDL statements are implemented in TiDB, the online change process, and best practices.
---

# Execution Principles and Best Practices of DDL Statements

This document provides an overview of the execution principles and best practices related to DDL statements in TiDB. The topics covered include the DDL Owner module and the online DDL change process.

## DDL execution principles

TiDB uses an online and asynchronous approach to executing DDL statements. This means that DML statements in other sessions are not blocked while DDL statements are being executed. In other words, you can change the definition of database objects using online and asynchronous DDL statements while your applications are running.

### Types of DDL statements

Based on whether a DDL statement blocks the user application during execution, DDL statements can be divided into the following types:

- **Offline DDL statements**: When the database receives a DDL statement from the user, it first locks the database object to be modified, executes the metadata change, and blocks the user application from modifying data during the DDL execution.

- **Online DDL statements**: When a DDL statement is executed in the database, a specific method is used to ensure that the statement does not block the user application. This allows the user to submit modifications during the DDL execution. The method also ensures the correctness and consistency of the corresponding database object during the execution process.

Based on whether to operate the data included in the target DDL object, DDL statements can be divided into the following types:

- **Logical DDL statements**: This type of DDL statements usually only modify the metadata of the database object, without processing the data stored in the object. For example, changing the table name or changing the column name.

    In TiDB, logical DDL statements are also referred to as "general DDL". These statements typically have a short execution time, often taking only a few tens of milliseconds or seconds to complete. As a result, they do not consume much system resource and do not affect the load on the application.

- **Physical DDL statements**: This type of DDL statements not only modifies the metadata of the object to be changed, but also modifies the user data stored in the object. For example, when TiDB creates an index for a table, it not only changes the definition of the table, but also performs a full table scan to build the newly added index.

    In TiDB, physical DDL statements are also referred to as "reorg DDL", which stands for reorganization. Currently, physical DDL statements only include `ADD INDEX` and lossy column type changes (such as changing from an `INT` type to a `CHAR` type). These statements take a long time to execute, and the execution time is influenced by the amount of data in the table, the machine configuration, and the application load.

    Executing physical DDL statements can have an impact on the load of the application for two reasons. On the one hand, it requires CPU and I/O resources from TiKV to read data and write new data. On the other hand, the TiDB node where the DDL Owner is located needs to perform the corresponding computations, which consumes more CPU resources. Because TiDB does not currently support distributed execution of DDL statements, other TiDB nodes do not consume additional system resources during this process.

    > **Note:**
    >
    > The execution of physical DDL tasks is typically what causes the greatest impact on the user application. Therefore, to minimize this impact, the focus is on optimizing the design of physical DDL statements during execution. This helps to reduce the impact on the user application.

### TiDB DDL module

The TiDB DDL module incorporates the role of the DDL Owner (or Owner), which serves as a proxy for executing all DDL statements within the TiDB cluster. In the current implementation, only one TiDB node in the entire cluster can be elected as the Owner at any given time. Once elected, the worker started in that TiDB node can handle the DDL tasks in the cluster.

TiDB uses the election mechanism of etcd to elect a node to host the Owner from multiple TiDB nodes. By default, each TiDB node can potentially be elected as the Owner (you can configure `run-ddl` to manage node participation in the election). The elected Owner node has a term, which it actively maintains by renewing the term. When the Owner node is down, another node can be re-elected as the new Owner through etcd and continue executing DDL tasks in the cluster.

A simple illustration of the DDL Owner is as follows:

![DDL Owner](/media/ddl-owner.png)

You can use the `ADMIN SHOW DDL` statement to view the current DDL owner:

```sql
ADMIN SHOW DDL;
```

```sql
+------------+--------------------------------------+---------------+--------------+--------------------------------------+-------+
| SCHEMA_VER | OWNER_ID                             | OWNER_ADDRESS | RUNNING_JOBS | SELF_ID                              | QUERY |
+------------+--------------------------------------+---------------+--------------+--------------------------------------+-------+
|         26 | 2d1982af-fa63-43ad-a3d5-73710683cc63 | 0.0.0.0:4000  |              | 2d1982af-fa63-43ad-a3d5-73710683cc63 |       |
+------------+--------------------------------------+---------------+--------------+--------------------------------------+-------+
1 row in set (0.00 sec)
```

### How the Online DDL Asynchronous Change Works in TiDB

From the beginning of its design, the TiDB DDL module has opted for an online asynchronous change mode, which enables users to modify their applications without experiencing any downtime.

DDL changes involve transitioning from one state to another, typically from a "before change" state to an "after change" state. With online DDL changes, this transition occurs by introducing multiple small version states that are mutually compatible. During the execution of a DDL statement, TiDB nodes in the same cluster are allowed to have different small version changes, as long as the difference between the small versions of the change objects is not more than two versions. This is possible because adjacent small versions can be mutually compatible.

In this way, evolving through multiple small versions ensures that metadata can be correctly synchronized across multiple TiDB nodes. This helps maintain the correctness and consistency of user transactions that involve changing data during the process.

Taking `ADD INDEX` as an example, the entire process of state change is as follows:

```
absent -> delete only -> write only -> write reorg -> public
```

For users, the newly created index is unavailable before the `public` state.

<SimpleTab>
<div label="Online DDL asychronous change before TiDB v6.2">

Before v6.2.0, the process of handling asynchronous schema changes in the TiDB SQL layer is as follows:

1. MySQL Client sends a DDL request to the TiDB server.

2. After receiving the request, a TiDB server parses and optimizes the request at the MySQL Protocol layer, and then sends it to the TiDB SQL layer for execution.

    Once the SQL layer of TiDB receives the DDL request, it starts the `start job` module to encapsulate the request into a specific DDL Job (that is, a DDL task), and then stores this Job in the corresponding DDL Job queue in the KV layer based on the statement type. The corresponding worker is notified of the Job that requires processing.

3. When receiving the notification to process the Job, the worker determines whether it is the role of the DDL Owner. If it is the Owner role, it directly processes the Job. Otherwise, it exits without performing any processing.

    If a TiDB server is not the Owner role, then another node must be the Owner. The worker of the node in the Owner role periodically checks whether there is an available Job that can be executed. If such a Job is identified, the worker will process the Job.

4. After the worker processes the Job, it removes the Job from the Job queue in the KV layer and places it in the `job history queue`. The `start job` module that encapsulated the Job will periodically check the ID of the Job in the `job history queue` to see whether it has been processed. If so, the entire DDL operation corresponding to the Job ends.

5. TiDB server returns the DDL processing result to the MySQL Client.

Before TiDB v6.2.0, the DDL execution framework had the following limitations:

- The TiKV cluster only has two queues: `general job queue` and `add index job queue`, which handle logical DDL and physical DDL, respectively.
- The DDL Owner always processes DDL Jobs in a first-in-first-out way.
- The DDL Owner can only execute one DDL task of the same type (logical or physical) at a time, which is relatively strict.

These limitations might lead to some "unintended" DDL blocking behavior. For more details, see [SQL FAQ - DDL Execution](/faq/sql-faq.md#ddl-execution).

</div>
<div label="Parallel DDL framework starting from v6.2">

Before TiDB v6.2, because the Owner can only execute one DDL task of the same type (logical or physical) at a time, which is relatively strict, and affects the user experience.

If there is no dependency between DDL tasks, parallel execution does not affect data correctness and consistency. For example, user A adds an index to the `T1` table, while user B deletes a column from the `T2` table. These two DDL statements can be executed in parallel.

To improve the user experience of DDL execution, starting from v6.2.0, TiDB enables the Owner to determine the relevance of DDL tasks. The logic is as follows:

+ DDL statements to be performed on the same table are mutually blocked.
+ `DROP DATABASE` and DDL statements that affect all objects in the database are mutually blocked.
+ Adding indexes and column type changes on different tables can be executed concurrently.
+ A logical DDL statement must wait for the previous logical DDL statement to be executed before it can be executed.
+ In other cases, DDL can be executed based on the level of availability for concurrent DDL execution.

In specific, TiDB has upgraded the DDL execution framework in v6.2.0 in the following aspects:

+ The DDL Owner can execute DDL tasks in parallel based on the preceding logic.
+ The first-in-first-out issue in the DDL Job queue has been addressed. The DDL Owner no longer selects the first Job in the queue, but instead selects the Job that can be executed at the current time.
+ The number of workers that handle physical DDL has been increased, enabling multiple physical DDLs to be executed in parallel.

    Because all DDL tasks in TiDB are implemented using an online change approach, TiDB can determine the relevance of new DDL Jobs through the Owner, and schedule DDL tasks based on this information. This approach enables the distributed database to achieve the same level of DDL concurrency as traditional databases.

The concurrent DDL framework enhances the execution capability of DDL statements in TiDB, making it more compatible with the usage patterns of commercial databases.

</div>
</SimpleTab>

## 最佳实践

### 通过系统变量来平衡物理 DDL 的执行速度与对业务负载的影响

执行物理 DDL（包括添加索引或列类型变更）时，适当调整以下系统变量可以平衡 DDL 执行速度与对业务负载的影响：

- [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)：这个变量用来设置 DDL 操作 reorg worker 的数量，控制回填的并发度。

- [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size)：这个变量用来设置 DDL 操作 `re-organize` 阶段的 batch size，以控制回填的数据量。

    推荐值：

    - 在无其他负载情况下，如需让 `ADD INDEX` 尽快完成，可以将 `tidb_ddl_reorg_worker_cnt` 和 `tidb_ddl_reorg_batch_size` 的值适当调大，例如将两个变量值分别调为 `20` 和 `2048`。
    - 在有其他负载情况下，如需让 `ADD INDEX` 尽量不影响其他业务，可以将 `tidb_ddl_reorg_worker_cnt` 和 `tidb_ddl_reorg_batch_size` 适当调小，例如将两个变量值分别调为 `4` 和 `256`。

> **建议：**
>
> - 以上两个变量均可以在 DDL 任务执行过程中动态调整，并且在下一个 batch 生效。
> - 根据 DDL 操作的类型，并结合业务负载压力，选择合适的时间点执行，例如建议在业务负载比较低的情况运行 `ADD INDEX` 操作。
> - 由于添加索引的时间跨度较长，发送相关的指令后，TiDB 会在后台执行任务，TiDB server 挂掉不会影响继续执行。

### 并发发送 DDL 请求实现快速建大量表

一个建表的操作耗时大约 50 毫秒。受框架的限制，建表耗时可能更长。

为了更快地建表，推荐通过并发发送多个 DDL 请求以达到最快建表速度。如果串行地发送 DDL 请求，并且没有发给 Owner 节点，则建表速度会很慢。

### 在一条 `ALTER` 语句中进行多次变更

自 v6.2.0 起，TiDB 支持在一条 `ALTER` 语句中修改一张表的多个模式对象（如列、索引），同时保证整个语句的原子性。因此推荐在一条 `ALTER` 语句中进行多次变更。

### 检查读写性能

在添加索引时，回填数据阶段会对集群造成一定的读写压力。在 `ADD INDEX` 的命令发送成功后，并且在 `write reorg` 阶段，建议检查 Grafana 面板上 TiDB 和 TiKV 读写相关的性能指标，以及业务响应时间，来确定 `ADD INDEX` 操作对集群是否造成影响。

## DDL 相关的命令介绍

- `ADMIN SHOW DDL`：用于查看 TiDB DDL 的状态，包括当前 schema 版本号、DDL Owner 的 DDL ID 和地址、正在执行的 DDL 任务和 SQL、当前 TiDB 实例的 DDL ID。详情参阅 [`ADMIN SHOW DDL`](/sql-statements/sql-statement-admin-show-ddl.md#admin-show-ddl)。

- `ADMIN SHOW DDL JOBS`：查看集群环境中的 DDL 任务运行中详细的状态。详情参阅 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md#admin-show-ddl-jobs)。

- `ADMIN SHOW DDL JOB QUERIES job_id [, job_id]`：用于查看 job_id 对应的 DDL 任务的原始 SQL 语句。详情参阅 [`ADMIN SHOW DDL JOB QUERIES`](/sql-statements/sql-statement-admin-show-ddl.md#admin-show-ddl-job-queries)。

- `ADMIN CANCEL DDL JOBS job_id, [, job_id]`：用于取消已经提交但未执行完成的 DDL 任务。取消完成后，执行 DDL 任务的 SQL 语句会返回 `ERROR 8214 (HY000): Cancelled DDL job` 错误。

    取消一个已经执行完成的 DDL 任务会在 RESULT 列看到 `DDL Job:90 not found` 的错误，表示该任务已从 DDL 等待队列中被移除。

## 常见问题

DDL 语句执行相关的常见问题，参考 [SQL FAQ - DDL 执行](/faq/sql-faq.md#ddl-执行)。
