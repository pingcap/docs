---
title: TiDB 中 DDL 执行的最佳实践
summary: 了解 TiDB 中 DDL 语句的实现方式、在线变更流程以及最佳实践。
---

# TiDB 中 DDL 执行的最佳实践

本文档概述了 TiDB 中与 DDL 语句相关的执行原理和最佳实践。原理包括 DDL Owner 模块和在线 DDL 变更流程。

## DDL 执行原理

TiDB 采用在线异步方式执行 DDL 语句。这意味着在执行 DDL 语句时，其他会话中的 DML 语句不会被阻塞。换句话说，你可以在应用程序运行时，使用在线异步的 DDL 语句修改数据库对象的定义。

### DDL 语句类型

TiDB 支持在线 DDL，这意味着在数据库中执行 DDL 语句时，采用特定的方法确保该操作不会阻塞用户应用。你可以在 DDL 执行期间提交数据修改，数据库保证数据的一致性和正确性。

相比之下，离线 DDL 会锁定数据库对象，阻塞用户的修改，直到 DDL 操作完成。TiDB 不支持离线 DDL。

根据是否操作目标 DDL 对象中的数据，DDL 语句可以分为以下类型：

- **Logical DDL 语句**：逻辑 DDL 语句通常只修改数据库对象的元数据，不处理存储在对象中的数据，例如更改表名或列名。

    在 TiDB 中，逻辑 DDL 也称为“通用 DDL”。这些语句的执行时间通常较短，常常只需几十毫秒或几秒即可完成。因此，它们消耗的系统资源较少，不会影响应用的工作负载。

- **Physical DDL 语句**：物理 DDL 语句不仅修改被变更对象的元数据，还会修改存储在对象中的用户数据。例如，当 TiDB 为一张表创建索引时，不仅会改变表的定义，还会进行全表扫描以构建新添加的索引。

    在 TiDB 中，物理 DDL 也称为“reorg DDL”，代表重组。目前，物理 DDL 仅包括 `ADD INDEX` 和有损列类型变更（如从 `INT` 类型变更为 `CHAR` 类型）。这些操作的执行时间较长，受表中数据量、机器配置和应用负载的影响。

    执行物理 DDL 可能对应用的工作负载产生影响，原因有二：一方面，它会消耗 TiKV 的 CPU 和 I/O 资源，用于读取和写入数据；另一方面，**作为 DDL Owner 的 TiDB 节点** 或 **由 TiDB 分布式执行框架（DXF）调度执行 `ADD INDEX` 任务的 TiDB 节点**，会消耗 CPU 资源进行相应的计算。

    > **Note:**
    >
    > 执行物理 DDL 任务通常对用户应用的影响最大。因此，为了最小化影响，关键在于在执行过程中优化物理 DDL 语句的设计。这有助于减少对用户应用的影响。

### TiDB DDL 模块

TiDB 的 DDL 模块引入了 DDL Owner（或 Owner）角色，作为在 TiDB 集群中执行所有 DDL 语句的代理。在当前实现中，整个集群中最多只有一个 TiDB 节点可以被选举为 Owner。一旦某个 TiDB 节点当选为 Owner，该节点启动的工作线程就可以处理集群中的 DDL 任务。

TiDB 使用 etcd 的选举机制，从多个 TiDB 节点中选举出一个节点作为 Owner。默认情况下，每个 TiDB 节点都可能被选举为 Owner（你可以配置 `run-ddl` 来管理节点参与选举）。当选的 Owner 节点有一个任期（term），它会通过续期主动维护该任期。当 Owner 节点宕机时，其他节点可以通过 etcd 选举出新的 Owner，继续在集群中执行 DDL 任务。

一个简单的 DDL Owner 示意图如下：

![DDL Owner](/media/ddl-owner.png)

你可以使用 `ADMIN SHOW DDL` 语句查看当前的 DDL Owner：

```sql
ADMIN SHOW DDL;
```

```sql
+------------+--------------------------------------+---------------+--------------+--------------------------------------+-------+
| SCHEMA_VER | OWNER_ID                             | OWNER_ADDRESS | RUNNING_JOBS | SELF_ID                              | QUERY |
+------------+--------------------------------------+---------------+--------------+--------------------------------------+-------+
|         26 | 2d1982af-fa63-43ad-a3d5-73710683cc63 | 0.0.0.0:4000  |              | 2d1982af-fa63-43ad-a3d5-73710683cc63 |       |
+------------+--------------------------------------+---------------+--------------+--------------------------------------+-------+
```

### TiDB 中在线 DDL 异步变更的工作原理

从设计之初，TiDB 的 DDL 模块就采用了在线异步变更模式，允许你在不影响应用的情况下修改。

DDL 变更涉及状态的转换，通常从“变更前”状态到“变更后”状态。采用在线 DDL 时，这一转换通过引入多个相互兼容的小版本状态实现。在执行 DDL 语句期间，TiDB 集群中的节点可以拥有不同的小版本变更，只要相邻的小版本之间的差异不超过两个版本。这是因为相邻的小版本可以相互兼容。

这样，通过多个小版本的演进，确保元数据可以在多个 TiDB 节点间正确同步，有助于在变更过程中保持涉及数据变更的用户事务的正确性和一致性。

以 `ADD INDEX` 为例，整个状态变更过程如下：

```
absent -> delete only -> write only -> write reorg -> public
```

对于用户而言，直到进入 `public` 状态之前，新创建的索引都是不可用的。

<SimpleTab>
<div label="从 v6.2.0 开始的并行 DDL 框架">

在 TiDB v6.2.0 之前，由于 Owner 一次只能执行一种类型（逻辑或物理）的 DDL 任务，限制较为严格，影响用户体验。

如果 DDL 任务之间没有依赖关系，并行执行不会影响数据的正确性和一致性。例如，用户 A 给 `T1` 表添加索引，而用户 B 删除 `T2` 表中的列，这两个 DDL 语句可以并行执行。

为了改善 DDL 执行的用户体验，从 v6.2.0 开始，TiDB 允许 Owner 根据 DDL 任务的相关性进行判断，逻辑如下：

+ 对同一张表的 DDL 语句相互阻塞。
+ `DROP DATABASE` 和影响数据库中所有对象的 DDL 语句相互阻塞。
+ 在不同表上添加索引和列类型变更可以并发执行。
+ 从 v8.2.0 开始，不同表的 [逻辑 DDL 语句](/ddl-introduction.md#types-of-ddl-statements) 可以并行执行。
+ 在其他情况下，DDL 可以根据可用性等级进行并发执行。

具体而言，TiDB 6.2.0 在以下方面增强了 DDL 执行框架：

+ DDL Owner 可以根据上述逻辑并行执行 DDL 任务。
+ 解决 DDL 任务队列中的先进先出问题。DDL Owner 不再只选择队列中的第一个任务，而是选择当前可以执行的任务。
+ 增加处理物理 DDL 语句的工作线程数，支持多个物理 DDL 并行执行。

    由于 TiDB 中所有 DDL 任务都采用在线变更方式实现，Owner 可以根据新 DDL 任务的相关性进行调度，从而实现与传统数据库相同的 DDL 并发水平。

并发 DDL 框架提升了 TiDB 中 DDL 语句的执行能力，使其更好地适应商业数据库的使用场景。

</div>
<div label="TiDB v6.2.0 之前的在线 DDL 异步变更流程">

在 v6.2.0 之前，TiDB SQL 层处理异步模式变更的流程如下：

1. MySQL 客户端向 TiDB 服务器发送 DDL 请求。

2. TiDB 服务器收到请求后，在 MySQL 协议层解析和优化请求，然后将其发送到 TiDB SQL 层执行。

    一旦 TiDB 的 SQL 层收到 DDL 请求，它会启动 `start job` 模块，将请求封装成特定的 DDL 任务（即 DDL Job），然后根据语句类型将其存入对应的 DDL 任务队列（在 KV 层）。相关工作线程会被通知处理该任务。

3. 当工作线程收到处理任务的通知时，会判断自己是否为 DDL Owner。如果是，则直接处理任务；否则不进行任何处理。

    如果 TiDB 服务器不是 Owner 角色，则必须由其他节点担任 Owner。Owner 角色的工作线程会定期检查是否有可执行的任务。如果发现有，则会处理该任务。

4. 工作线程处理完 Job 后，会将任务从 KV 层的任务队列中移除，并放入 `job history queue`。封装 Job 的 `start job` 模块会定期检查 `job history queue` 中任务的 ID，确认是否已处理完毕。如果已完成，整个 DDL 操作也就结束了。

5. TiDB 服务器将 DDL 处理结果返回给 MySQL 客户端。

在 v6.2.0 之前，TiDB 的 DDL 执行框架存在以下限制：

- TiKV 集群只有两个队列：`general job queue` 和 `add index job queue`，分别处理逻辑 DDL 和物理 DDL。
- DDL Owner 始终以先进先出方式处理 DDL 任务。
- DDL Owner 一次只能执行一个相同类型（逻辑或物理）的 DDL 任务，限制较为严格，影响用户体验。

这些限制可能导致一些“非预期”的 DDL 阻塞行为。更多详情请参见 [SQL FAQ - DDL Execution](https://docs.pingcap.com/tidb/stable/sql-faq#ddl-execution)。

</div>
</SimpleTab>

## 最佳实践

### 通过系统变量平衡物理 DDL 执行速度与应用负载影响

在执行物理 DDL 语句（包括添加索引或列类型变更）时，可以调整以下系统变量的值，以平衡 DDL 执行速度和对应用负载的影响：

- [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)：设置 DDL 操作的重组织工作线程数，控制回填的并发度。

- [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size)：设置 `re-organize` 阶段的批量大小，控制回填的数据量。

    推荐值：

    - 如果没有其他负载，可以增大 `tidb_ddl_reorg_worker_cnt` 和 `tidb_ddl_reorg_batch_size` 的值，加快 `ADD INDEX` 的速度。例如，将两个变量的值分别设置为 `20` 和 `2048`。
    - 如果存在其他负载，可以减小这两个变量的值，以最小化对其他应用的影响。例如，将它们的值设置为 `4` 和 `256`。

> **Tip:**
>
> - 以上两个变量可以在 DDL 任务执行过程中动态调整，并在下一批事务中生效。
> - 根据操作类型和应用负载压力选择合适的时间执行 DDL 操作。例如，建议在应用负载较低时执行 `ADD INDEX`。
> - 由于添加索引的时间较长，TiDB 会在命令发出后在后台执行任务。如果 TiDB 服务器宕机，执行不会受到影响。

### 通过并发发送 DDL 请求快速创建大量表

创建一张表大约需要 50 毫秒。实际耗时可能更长，原因在于框架限制。

为了更快地创建表，建议同时发送多个 DDL 请求，以实现最快的创建速度。如果串行发送 DDL 请求且不在 Owner 节点，表创建速度会非常慢。

### 在单个 `ALTER` 语句中进行多项变更

从 v6.2.0 开始，TiDB 支持在单个 `ALTER` 语句中修改多个表结构对象（如列和索引），同时保证整个语句的原子性。因此，建议在单个 `ALTER` 语句中进行多项变更。

### 检查读写性能

当 TiDB 添加索引时，回填数据阶段会对集群造成读写压力。发出 `ADD INDEX` 命令并开始 `write reorg` 阶段后，建议通过 Grafana 仪表盘监控 TiDB 和 TiKV 的读写性能指标，以及应用响应时间，以判断 `ADD INDEX` 操作是否影响集群。

## 与 DDL 相关的命令

- `ADMIN SHOW DDL`：用于查看 TiDB DDL 操作的状态，包括当前的 schema 版本号、DDL Owner 的 ID 和地址、正在执行的 DDL 任务和 SQL，以及当前 TiDB 实例的 DDL ID。详情请参见 [`ADMIN SHOW DDL`](/sql-statements/sql-statement-admin-show-ddl.md#admin-show-ddl)。

- `ADMIN SHOW DDL JOBS`：用于查看集群中正在运行的 DDL 任务的详细状态。详情请参见 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md#admin-show-ddl-jobs)。

- `ADMIN SHOW DDL JOB QUERIES job_id [, job_id]`：用于查看对应 `job_id` 的 DDL 任务的原始 SQL 语句。详情请参见 [`ADMIN SHOW DDL JOB QUERIES`](/sql-statements/sql-statement-admin-show-ddl.md#admin-show-ddl-job-queries)。

- `ADMIN CANCEL DDL JOBS job_id [, job_id]`：用于取消已提交但未完成的 DDL 任务。取消完成后，执行 DDL 任务的 SQL 语句会返回 `ERROR 8214 (HY000): Cancelled DDL job` 错误。

    如果取消已完成的 DDL 任务，可以在 `RESULT` 列看到 `DDL Job:90 not found` 错误，表示该任务已从 DDL 等待队列中移除。

- `ADMIN PAUSE DDL JOBS job_id [, job_id]`：用于暂停正在执行的 DDL 任务。执行后，执行 DDL 任务的 SQL 语句显示为正在执行，而后台任务已暂停。详情请参见 [`ADMIN PAUSE DDL JOBS`](/sql-statements/sql-statement-admin-pause-ddl.md)。

    只能暂停进行中或在队列中的 DDL 任务，否则在 `RESULT` 列会显示 `Job 3 can't be paused now` 错误。

- `ADMIN RESUME DDL JOBS job_id [, job_id]`：用于恢复已暂停的 DDL 任务。执行后，执行 DDL 任务的 SQL 语句显示为正在执行，后台任务恢复。详情请参见 [`ADMIN RESUME DDL JOBS`](/sql-statements/sql-statement-admin-resume-ddl.md)。

    只能恢复已暂停的 DDL 任务，否则在 `RESULT` 列会显示 `Job 3 can't be resumed` 错误。

## 与 DDL 相关的表

- [`information_schema.DDL_JOBS`](/information-schema/information-schema-ddl-jobs.md)：当前正在运行和已完成的 DDL 任务信息。
- [`mysql.tidb_mdl_view`](/mysql-schema/mysql-schema-tidb-mdl-view.md)：关于 [metadata lock](/metadata-lock.md) 视图的信息，可帮助识别阻塞 DDL 进展的查询。

## 常见问题

关于 DDL 执行的常见问题，参见 [SQL FAQ - DDL execution](https://docs.pingcap.com/tidb/stable/sql-faq)。