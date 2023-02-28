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

在 v6.2.0 之前，TiDB SQL 层中处理异步 Schema 变更的基本流程如下：

1. MySQL Client 发送给 TiDB server 一个 DDL 操作请求。
1. MySQL Client sends a DDL request to TiDB server.

2. 某个 TiDB server 收到请求（即 TiDB server 的 MySQL Protocol 层对请求进行解析优化），然后发送到 TiDB SQL 层进行执行。
2. A TiDB server receives the request (that is, the MySQL Protocol layer of the TiDB server parses and optimizes the request), and then sends it to the TiDB SQL layer for execution.

    TiDB SQL 层接到 DDL 请求后，会启动 `start job` 模块根据请求将请求封装成特定的 DDL Job（即 DDL 任务），然后将此 Job 按语句类型分类，分别存储到 KV 层的对应 DDL Job 队列，并通知自身对应的 worker 有 Job 需要处理。

    After the SQL layer of TiDB receives the DDL request, it starts the `start job` module to encapsulate the request into a specific DDL Job (that is, a DDL task), and then stores this Job in the corresponding DDL Job queue in the KV layer according to the statement type, and notifies the corresponding worker that there is a Job that needs to be processed.

3. 接收到处理 Job 通知的 worker，会判断自身是否处于 DDL Owner 的角色。如果是 Owner 角色则直接处理此 Job。如果没有处于 Owner 角色则退出不做任何处理。
3. When receiving the notification to process the Job, the worker determines whether it is in the role of the DDL Owner. If it is the Owner role, it directly processes the Job. If it is not the Owner role, it exits without performing any processing.

    假设某台 TiDB server 不是 Owner 角色，那么其他某个节点一定有一个是 Owner。处于 Owner 角色的节点的 worker 通过定期检测机制来检查是否有 Job 可以被执行。如果发现有 Job ，那么 worker 就会处理该 Job。

    If a TiDB server is not the Owner role, then another node must be the Owner. The worker of the node in the Owner role periodically checks whether there is a Job that can be executed. If such a Job is found, the worker will process the Job.

4. Worker 处理完 Job 后，会将此 Job 从 KV 层对应的 Job queue 中移除，并放入 `job history queue`。之前封装 Job 的 `start job` 模块会定期在 `job history queue` 中查看是否有已经处理完成的 Job 的 ID。如果有，则这个 Job 对应的整个 DDL 操作结束执行。
4. 

5. TiDB server 将 DDL 处理结果返回至 MySQL Client。

在 TiDB v6.2.0 前，该 DDL 执行框架存在以下限制：

- TiKV 集群中只有 `general job queue` 和 `add index job queue` 两个队列，分别处理逻辑 DDL 和物理 DDL。
- DDL Owner 总是以先入先出的方式处理 DDL Job。
- DDL Owner 每次只能执行一个同种类型（逻辑或物理）的 DDL 任务，这个约束较为严格。

这些限制可能会导致一些“非预期”的 DDL 阻塞行为。具体可以参考 [SQL FAQ - DDL 执行](/faq/sql-faq.md#ddl-执行)。

</div>
<div label="并发 DDL 框架（TiDB v6.2 及以上）">

在 TiDB v6.2 之前，由于 Owner 每次只能执行一个同种类型（逻辑或物理）的 DDL 任务，这个约束较为严格，同时影响用户体验。

当 DDL 任务之间不存在相关依赖时，并行执行并不会影响数据正确性和一致性。例如：用户 A 在 `T1` 表上增加一个索引，同时用户 B 从 `T2` 表删除一列。这两条 DDL 语句可以并行执行。

为了提升 DDL 执行的用户体验，从 v6.2.0 起，TiDB 对原有的 DDL Owner 角色进行了升级，使得 Owner 能对 DDL 任务做相关性判断，判断逻辑如下：

+ 涉及同一张表的 DDL 相互阻塞。
+ `DROP DATABASE` 和数据库内所有对象的 DDL 互相阻塞。
+ 涉及不同表的加索引和列类型变更可以并发执行。
+ 逻辑 DDL 需要等待之前正在执行的逻辑 DDL 执行完才能执行。
+ 其他情况下 DDL 可以根据 Concurrent DDL 并行度可用情况确定是否可以执行。

具体来说，TiDB 在 v6.2.0 中对 DDL 执行框架进行了如下升级：

+ DDL Owner 能够根据以上判断逻辑并行执行 DDL 任务。
+ 改善了 DDL Job 队列先入先出的问题。DDL Owner 不再选择当前队列最前面的 DDL Job，而是选择当前可以执行的 DDL Job。
+ 扩充了处理物理 DDL 的 worker 数量，使得能够并行地添加多个物理 DDL。

    因为 TiDB 中所有支持的 DDL 任务都是以在线变更的方式来实现的，TiDB 通过 Owner 即可对新的 DDL Job 进行相关性判断，并根据相关性结果进行 DDL 任务的调度，从而使分布式数据库实现了和传统数据库中 DDL 并发相同的效果。

并发 DDL 框架的实现进一步加强了 TiDB 中 DDL 语句的执行能力，并更符合商用数据库的使用习惯。

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
