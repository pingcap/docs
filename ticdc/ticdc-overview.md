---
title: TiCDC Overview
summary: Learn what TiCDC is, what features TiCDC provides, and how to install and deploy TiCDC.
---

# TiCDC Overview

[TiCDC](https://github.com/pingcap/tiflow/tree/release-8.1/cdc) is a tool used to replicate incremental data from TiDB. Specifically, TiCDC pulls TiKV change logs, sorts captured data, and exports row-based incremental data to downstream databases.

## Usage scenarios

TiCDC has multiple usage scenarios, including:

- Providing high availability and disaster recovery solutions for multiple TiDB clusters. TiCDC ensures eventual data consistency between primary and secondary clusters in case of a disaster.
- Replicating real-time data changes to homogeneous systems. This provides data sources for various scenarios, such as monitoring, caching, global indexing, data analysis, and primary-secondary replication between heterogeneous databases.

## Major features

### Key capabilities

TiCDC has the following key capabilities:

- Replicating incremental data between TiDB clusters with second-level RPO and minute-level RTO.
- Bidirectional replication between TiDB clusters, allowing the creation of a multi-active TiDB solution using TiCDC.
- Replicating incremental data from a TiDB cluster to a MySQL database or other MySQL-compatible databases with low latency.
- Replicating incremental data from a TiDB cluster to a Kafka cluster. The recommended data format includes [Canal-JSON](/ticdc/ticdc-canal-json.md), [Avro](/ticdc/ticdc-avro-protocol.md), and [Debezium](/ticdc/ticdc-debezium.md).
- Replicating incremental data from a TiDB cluster to storage services, such as Amazon S3, GCS, Azure Blob Storage, and NFS.
- Replicating tables with the ability to filter databases, tables, DMLs, and DDLs.
- High availability with no single point of failure, supporting dynamically adding and deleting TiCDC nodes.
- Cluster management through [Open API](/ticdc/ticdc-open-api-v2.md), including querying task status, dynamically modifying task configuration, and creating or deleting tasks.

### Replication order

- For all DDL or DML statements, TiCDC outputs them **at least once**.
- When the TiKV or TiCDC cluster encounters a failure, TiCDC might send the same DDL/DML statement repeatedly. For duplicated DDL/DML statements:

    - The MySQL sink can execute DDL statements repeatedly. For DDL statements that can be executed repeatedly in the downstream, such as `TRUNCATE TABLE`, the statement is executed successfully. For those that cannot be executed repeatedly, such as `CREATE TABLE`, the execution fails, and TiCDC ignores the error and continues with the replication process.
    - The Kafka sink provides different strategies for data distribution.
        - You can distribute data to different Kafka partitions based on the table, primary key, or timestamp. This ensures that the updated data of a row is sent to the same partition in order.
        - All these distribution strategies send `Resolved TS` messages to all topics and partitions periodically. This indicates that all messages earlier than the `Resolved TS` have already been sent to the topics and partitions. The Kafka consumer can use the `Resolved TS` to sort the messages received.
        - The Kafka sink sometimes sends duplicated messages, but these duplicated messages do not affect the constraints of `Resolved Ts`. For example, if a changefeed is paused and then resumed, the Kafka sink might send `msg1`, `msg2`, `msg3`, `msg2`, and `msg3` in order. You can filter out the duplicated messages from Kafka consumers.

### Replication consistency

- MySQL sink

    - TiCDC enables the redo log to ensure eventual consistency of data replication.
    - TiCDC ensures that the order of single-row updates is consistent with the upstream.
    - TiCDC does not ensure that the downstream transactions are executed in the same order as the upstream transactions.

    > **Note:**
    >
    > Since v6.2, you can use the sink URI parameter [`transaction-atomicity`](/ticdc/ticdc-sink-to-mysql.md#configure-sink-uri-for-mysql-or-tidb) to control whether to split single-table transactions. Splitting single-table transactions can greatly reduce the latency and memory consumption of replicating large transactions.

## TiCDC architecture

TiCDC is an incremental data replication tool for TiDB, which is highly available through PD's etcd. The replication process consists of the following steps:

1. Multiple TiCDC processes pull data changes from TiKV nodes.
2. TiCDC sorts and merges the data changes.
3. TiCDC replicates the data changes to multiple downstream systems through multiple replication tasks (changefeeds).

The architecture of TiCDC is illustrated in the following figure:

![TiCDC architecture](/media/ticdc/cdc-architecture.png)

The components in the architecture diagram are described as follows:

- TiKV Server: TiKV nodes in a TiDB cluster. When data changes occur, TiKV nodes send the changes as change logs (KV change logs) to TiCDC nodes. If TiCDC nodes detect that the change logs are not continuous, they will actively request the TiKV nodes to provide change logs.
- TiCDC: TiCDC nodes where TiCDC processes run. Each node runs a TiCDC process. Each process pulls data changes from one or more tables in TiKV nodes and replicates the changes to the downstream system through the sink component.
- PD: The scheduling module in a TiDB cluster. This module is responsible for scheduling cluster data and usually consists of three PD nodes. PD provides high availability through the etcd cluster. In the etcd cluster, TiCDC stores its metadata, such as node status information and changefeed configurations.

As shown in the architecture diagram, TiCDC supports replicating data to TiDB, MySQL, Kafka, and storage services.

## Best practices

- When you use TiCDC to replicate data between two TiDB clusters, if the network latency between the two clusters is higher than 100 ms:

    - For TiCDC versions earlier than v6.5.2, it is recommended to deploy TiCDC in the region (IDC) where the downstream TiDB cluster is located.
    - With a series of improvements introduced starting from TiCDC v6.5.2, it is recommended to deploy TiCDC in the region (IDC) where the upstream TiDB cluster is located.

- TiCDC only replicates tables that have at least one valid index. A valid index is defined as follows:

    - A primary key (`PRIMARY KEY`) is a valid index.
    - A unique index (`UNIQUE INDEX`) is valid if every column of the index is explicitly defined as non-nullable (`NOT NULL`) and the index does not have a virtual generated column (`VIRTUAL GENERATED COLUMNS`).

- To ensure eventual consistency when using TiCDC for disaster recovery, you need to configure [redo log](/ticdc/ticdc-sink-to-mysql.md#eventually-consistent-replication-in-disaster-scenarios) and ensure that the storage system where the redo log is written can be read normally when a disaster occurs in the upstream.

## Implementation of data change processing

本小节主要描述 TiCDC 如何处理上游 DML 产生的数据变更。对于上游 DDL 产生的数据变更，TiCDC 会获取到完整的 DDL SQL 语句，根据下游的 Sink 类型，转换成对应的格式发送给下游，本小节不再赘述。

> **注意：**
>
> TiCDC 处理数据变更的逻辑可能会在后续版本发生调整。

MySQL binlog 直接记录了上游执行的所有 DML 操作的 SQL 语句。与 MySQL 不同，TiCDC 则实时监听上游 TiKV 各个 Region Raft Log 的信息，并根据每个事务前后数据的差异生成对应多条 SQL 语句的数据变更信息。TiCDC 只保证输出的变更事件和上游 TiDB 的变更是等价的，不保证能准确还原上游 TiDB 引起数据变更的 SQL 语句。

数据变更信息会包含数据变更类型，以及变更前后的数值。事务前后数据的差异一共可能产生三种事件：

1. `DELETE` 事件：对应会收到一条 `DELETE` 类型的数据变更信息，包含变更前的数据。

2. `INSERT` 事件：对应会收到一条 `PUT` 类型的数据变更信息，包含变更后的数据。

3. `UPDATE` 事件：对应会收到一条 `PUT` 类型的数据变更信息，包含变更前与变更后的数据。

TiCDC 会根据收到的这些数据变更信息，适配各个类型的下游来生成合适格式的数据传输给下游。例如，生成 Canal-JSON、Avro 等格式的数据写入 Kafka 中，或者重新转换成 SQL 语句发送给下游的 MySQL 或者 TiDB。

目前 TiCDC 将数据变更信息适配对应的协议时，对于特定的 `UPDATE` 事件，可能会将其拆成一条 `DELETE` 事件和一条 `INSERT` 事件。详见[将 Update 事件拆分为 Delete 和 Insert 事件](/ticdc/ticdc-behavior-change.md#将-update-事件拆分为-delete-和-insert-事件)。

当下游是 MySQL 或者 TiDB 时，因为 TiCDC 并非直接获取原生上游执行的 DML 语句，而是重新根据数据变更信息来生成 SQL 语句，因此不能保证写入下游的 SQL 语句和上游执行的 SQL 语句完全相同，但会保证最终结果的一致性。

For example, the following SQL statement is executed in the upstream:

```sql
Create Table t1 (A int Primary Key, B int);

BEGIN;
Insert Into t1 values(1,2);
Insert Into t1 values(2,2);
Insert Into t1 values(3,3);
Commit;

Update t1 set b = 4 where b = 2;
```

TiCDC generates the following two SQL statements based on the data change information, and writes them to the downstream:

```sql
INSERT INTO `test.t1` (`A`,`B`) VALUES (1,1),(2,2),(3,3);
UPDATE `test`.`t1`
SET `A` = CASE
        WHEN `A` = 1 THEN 1
        WHEN `A` = 2 THEN 2
END, `B` = CASE
        WHEN `A` = 1 THEN 4
        WHEN `A` = 2 THEN 4
END
WHERE `A` = 1 OR `A` = 2;
```

## Unsupported scenarios

Currently, the following scenarios are not supported:

- A TiKV cluster that uses RawKV alone.
- The [`CREATE SEQUENCE` DDL operation](/sql-statements/sql-statement-create-sequence.md) and the [`SEQUENCE` function](/sql-statements/sql-statement-create-sequence.md#sequence-function) in TiDB. When the upstream TiDB uses `SEQUENCE`, TiCDC ignores `SEQUENCE` DDL operations/functions performed upstream. However, DML operations using `SEQUENCE` functions can be correctly replicated.
- Currently, performing [BR data recovery](/br/backup-and-restore-overview.md) and [TiDB Lightning physical import](/tidb-lightning/tidb-lightning-physical-import-mode.md) imports on tables and databases that are being replicated by TiCDC is not supported. For more information, see [Why does replication using TiCDC stall or even stop after data restore using TiDB Lightning and BR from upstream](/ticdc/ticdc-faq.md#why-does-replication-using-ticdc-stall-or-even-stop-after-data-restore-using-tidb-lightning-physical-import-mode-and-br-from-upstream).

TiCDC only partially supports scenarios involving large transactions in the upstream. For details, refer to the [TiCDC FAQ](/ticdc/ticdc-faq.md#does-ticdc-support-replicating-large-transactions-is-there-any-risk), where you can find details on whether TiCDC supports replicating large transactions and any associated risks.
