---
title: TiCDC Overview
summary: Learn what TiCDC is, what features TiCDC provides, and how to install and deploy TiCDC.
aliases: ['/docs/dev/ticdc/ticdc-overview/','/docs/dev/reference/tools/ticdc/overview/']
---

# TiCDC Overview

[TiCDC](https://github.com/pingcap/tiflow/tree/master/cdc) is a tool used for replicating incremental data of TiDB. Specifically, TiCDC pulls TiKV change logs, sorts captured data, and exports row-based incremental data to downstream databases.

## Usage scenarios

- Database disaster recovery: TiCDC can be used for disaster recovery between homogeneous databases to ensure eventual data consistency of primary and secondary databases after a disaster event. This function works only with TiDB primary and secondary clusters.
- Data integration: TiCDC provides [TiCDC Canal-JSON Protocol](/ticdc/ticdc-canal-json.md), which allows other systems to subscribe data changes from TiCDC. In this way, TiCDC provides data sources for various scenarios such as monitoring, caching, global indexing, data analysis, and primary-secondary replication between heterogeneous databases.

- Provides data high availability and disaster recovery solutions for multiple TiDB clusters, ensuring eventual data consistency between primary and secondary clusters in case of disaster.
- Replicates real-time data changes to homogeneous systems so as to provide data sources for various scenarios such as monitoring, caching, global indexing, data analysis, and primary-secondary replication between heterogeneous databases.

## TiCDC 主要特性

### 核心能力

- 提供 TiDB -> TiDB 之间数据容灾复制的能力，实现秒级别 RPO 和分钟级别 RTO
- 提供 TiDB -> MySQL（或其他兼容 MySQL 协议的数据库）的低延迟的增量数据同步能力
- 提供 TiDB -> Kafka 增量数据同步能力，推荐的数据格式包含 [Canal-JSON](/ticdc/ticdc-canal-json.md)，[Avro](/ticdc/ticdc-avro-protocol.md) 等
- 提供表级别数据同步能力，支持同步过程中过滤数据库、表、DML、DDL 的能力
- 高可用架构，无单点故障；支持动态添加、删除 TiCDC 节点
- 支持通过 [Open API](/ticdc/ticdc-open-api.md) 进行集群管理，包括查询任务状态；动态修改任务配置；动态创建、删除任务等

### Replication order

- For all DDL or DML statements, TiCDC outputs them **at least once**.
- When the TiKV or TiCDC cluster encounters failure, TiCDC might send the same DDL/DML statement repeatedly. For duplicated DDL/DML statements:

    - MySQL sink can execute DDL statements repeatedly. For DDL statements that can be executed repeatedly in the downstream, such as `truncate table`, the statement is executed successfully. For those that cannot be executed repeatedly, such as `create table`, the execution fails, and TiCDC ignores the error and continues the replication.
    - Kafka sink
        - Kafka sink provides different strategies for data distribution. You can distribute data to different Kafka partitions based on the table, primary key, or timestamp. This ensures that the update data of a row is sent to the same partition in order.
        - All these distribution strategies send Resolved TS messages to all topics and partitions periodically. This indicates that all messages earlier than the Resolved TS have been sent to the topics and partitions. The consumer can use the Resolved TS to sort the messages received.
        - Kafka sink sends messages repeatedly, but the duplicate messages do not affect the constraints of `Resolved Ts`. For example, if a changefeed is paused and then resumed, msg1, msg2, msg3, msg2, and msg3 will be sent in order. You can filter the duplicated messages from Kafka consumers.

### Replication consistency

- MySQL sink

    - TiCDC 开启 redo log 后保证数据复制的最终一致性
    - TiCDC **ensures** that the order of single-row updates is consistent with that in the upstream.
    - TiCDC does **not ensure** that the execution order of downstream transactions is the same as that of upstream transactions.

     > **Note:**
    >
    > Since v6.2, you can use the sink uri parameter [`transaction-atomicity`](/ticdc/ticdc-sink-to-mysql.md.md#configure-sink-uri-with-mysqltidb) to control whether to split single-table transactions. Splitting single-table transactions can greatly reduce the latency and memory consumption of replicating large transactions.

## TiCDC architecture

TiCDC 作为 TiDB 的增量数据同步工具，通过 PD 内部的 etcd 实现高可用，通过多个 TiCDC 进程获取 TiKV 节点上的数据改变，在内部进行排序、合并等处理之后，通过多个同步任务 (Changefeed)，同时向多个下游系统进行数据同步。

The architecture of TiCDC is shown in the following figure:

![TiCDC architecture](/media/ticdc/cdc-architecture.png)

在以上架构图中：

- TiKV Server：代表 TiDB 集群中的 TiKV 节点，当数据发生改变时 TiKV 节点会主动将发生的数据改变以变更日志（KV change logs，简称 change logs）的方式发送给 TiCDC 节点。当然，当 TiCDC 节点发现收到的 change logs 并不是连续的，也会主动发起请求，获得需要的 change logs。
- TiCDC：代表运行了运行 TiCDC 进程的各个节点。每个节点都运行一个 TiCDC 进程，每个进程会从 TiKV 节点中拉取一个或者多个表中的数据改变，并通过 Sink 模块同步到下游系统。
- PD：代表 TiDB 集群中的调度模块，负责集群数据的事实调度，这个模块通常是由 3 个 PD 节点构成的，内部通过 etcd 集群来实现选举等高可用相关的能力。 TiCDC 集群使用了 PD 集群内置的 etcd 集群来保存自己的元数据信息，例如：节点的状态信息，changefeed 配置信息等。

另外，从上面的架构图中也可以看到，目前 TiCDC 支持将数据同步到 TiDB，MySQL 数据库，以及 Kafka 等。

## Restrictions

There are some restrictions when using TiCDC.

### Requirements for valid index

TiCDC only replicates the table that has at least one **valid index**. A **valid index** is defined as follows:

- The primary key (`PRIMARY KEY`) is a valid index.
- The unique index (`UNIQUE INDEX`) that meets the following conditions at the same time is a valid index:
    - Every column of the index is explicitly defined as non-nullable (`NOT NULL`).
    - The index does not have the virtual generated column (`VIRTUAL GENERATED COLUMNS`).

Since v4.0.8, TiCDC supports replicating tables **without a valid index** by modifying the task configuration. However, this compromises the guarantee of data consistency to some extent. For more details, see [Replicate tables without a valid index](/ticdc/ticdc-manage-changefeed.md#replicate-tables-without-a-valid-index).

### Unsupported scenarios

Currently, the following scenarios are not supported:

- The TiKV cluster that uses RawKV alone.
- The [DDL operation `CREATE SEQUENCE`](/sql-statements/sql-statement-create-sequence.md) and the [SEQUENCE function](/sql-statements/sql-statement-create-sequence.md#sequence-function) in TiDB. When the upstream TiDB uses `SEQUENCE`, TiCDC ignores `SEQUENCE` DDL operations/functions performed upstream. However, DML operations using `SEQUENCE` functions can be correctly replicated.

TiCDC only provides partial support for scenarios of large transactions in the upstream. For details, refer to [Does TiCDC support replicating large transactions? Is there any risk?](/ticdc/ticdc-faq.md#does-ticdc-support-replicating-large-transactions-is-there-any-risk).

> **Note:**
>
> Since v5.3.0, TiCDC no longer supports the cyclic replication feature.
