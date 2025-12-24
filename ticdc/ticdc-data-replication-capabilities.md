---
title: TiCDC Data Replication Capabilities
summary: Learn the data replication capabilities of TiCDC.
---

# TiCDC Data Replication Capabilities

[TiCDC](/ticdc/ticdc-overview.md) (TiDB Change Data Capture) is a core component in the TiDB ecosystem for real-time data replication. This document provides a detailed explanation of TiCDC data replication capabilities.

## How TiCDC works

- TiCDC listens to TiKV change logs (Raft logs) and converts row-level data changes (`INSERT`, `UPDATE`, and `DELETE` operations) into downstream-compatible SQL statements. TiCDC does not rely on the original SQL statements executed on the upstream database. For details, see [how TiCDC processes data changes](/ticdc/ticdc-overview.md#implementation-of-processing-data-changes).

- TiCDC generates logical operations (such as `INSERT`, `UPDATE`, and `DELETE`) equivalent to SQL semantics, rather than restoring the original SQL statements executed on the upstream database one by one. For details, see [how TiCDC processes data changes](/ticdc/ticdc-overview.md#implementation-of-processing-data-changes).

- TiCDC ensures eventual consistency of transactions. With [redo log](/ticdc/ticdc-sink-to-mysql.md#eventually-consistent-replication-in-disaster-scenarios) enabled, TiCDC can guarantee eventual consistency in disaster recovery scenarios. With [Syncpoint](/ticdc/ticdc-upstream-downstream-check.md#enable-syncpoint) enabled, TiCDC supports consistent snapshot reads and data consistency validation.

## Supported downstream systems

TiCDC supports replicating data to various downstream systems, including the following:

- [TiDB database or other MySQL-compatible databases](/ticdc/ticdc-sink-to-mysql.md)
- [Apache Kafka](/ticdc/ticdc-sink-to-kafka.md)
- Message Queue (MQ)-type sinks, such as [Pulsar](/ticdc/ticdc-sink-to-pulsar.md)
- [Storage services (Amazon S3, GCS, Azure Blob Storage, and NFS)](/ticdc/ticdc-sink-to-cloud-storage.md)
- [Snowflake, ksqlDB, SQL Server via Confluent Cloud integration](/ticdc/integrate-confluent-using-ticdc.md)
- [Apache Flink for consuming Kafka-replicated data](/replicate-data-to-kafka.md)

## Scope of data replication

TiCDC supports the following types of upstream data changes:

+ **Supported:**

    - DDL and DML statements (excluding system tables).
    - Index operations (`ADD INDEX`, `CREATE INDEX`): to reduce the impact on changefeed replication latency, if the downstream is TiDB, TiCDC [asynchronously executes the `ADD INDEX` and `CREATE INDEX` DDL operations](/ticdc/ticdc-ddl.md#asynchronous-execution-of-add-index-and-create-index-ddls).
    - Foreign key constraint DDL statements (`ADD FOREIGN KEY`): TiCDC does **not** replicate upstream system variable settings. You need to manually configure [`foreign_key_checks`](/system-variables.md#foreign_key_checks) in the downstream to determine whether the downstream foreign key constraint check is enabled. Additionally, when writing data to the downstream, TiCDC automatically enables the session-level setting `SET SESSION foreign_key_checks = OFF;`. Therefore, even if global foreign key checks are enabled in the downstream, the data written by TiCDC will not trigger foreign key constraint validation.

+ **Not supported**:

    - DDL and DML statements executed in upstream system tables (including `mysql.*` and `information_schema.*`).
    - DDL and DML statements executed in upstream temporary tables.
    - DQL (Data Query Language) and DCL (Data Control Language) statements.

## Limitations

- TiCDC does not support certain scenarios. For details, see [unsupported scenarios](/ticdc/ticdc-overview.md#unsupported-scenarios).
- TiCDC only verifies the integrity of upstream data changes. It does not validate whether the changes conform to upstream or downstream constraints. If the data violates downstream constraints, TiCDC will return an error when writing to the downstream.

    For example: When a changefeed is configured to filter out all DDL events, if the upstream executes a `DROP COLUMN` operation but continues to write `INSERT` statements involving that column, TiCDC will fail to replicate these DML changes to the downstream because of table schema mismatches.

- For the TiCDC [classic architecture](https://docs.pingcap.com/tidb/stable/ticdc-classic-architecture/), when the number of tables replicated by a single TiCDC cluster exceeds the following recommended values, TiCDC might not work stably:

    | TiCDC version | Recommended number of tables to be replicated |
    |---|:---:|
    | v5.4.0 - v6.4.x | 2000 |
    | v6.5.x - v7.4.x | 4000 |
    | v7.5.x - v8.5.x | 40000 |

    > **Note:**
    >
    > When replicating partitioned tables, TiCDC treats each partition as a separate table. Therefore, the partition count is included when TiCDC calculates the total number of tables to be replicated.

    If the number of tables to be replicated exceeds the preceding recommended values, it is recommended to use the [TiCDC new architecture](https://docs.pingcap.com/tidb/stable/ticdc-architecture/). The new architecture supports replicating more than one million tables per changefeed, making it suitable for large-scale replication scenarios.
