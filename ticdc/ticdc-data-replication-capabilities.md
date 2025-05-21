---
title: TiCDC Data Replication Capabilities
summary: Learn the data replication capabilities of TiCDC.
---

# TiCDC Data Replication Capabilities

TiCDC (TiDB Change Data Capture) is a core component for real-time data synchronization in the TiDB ecosystem. This doc provides a detailed explanation of TiCDC's data replication capabilities.

## Working Pinciples of TiCDC

+ TiCDC monitors TiKV's Raft Log to convert row-level data changes (insert/update/delete) into downstream-compatible SQL statements. Unlike Binlog, TiCDC does not rely on parsing SQL statements. Refer to [TiCDC's Implementation Principles for Processing Data Changes](/ticdc/ticdc-overview.md#implementation-of-processing-data-changes).


+ TiCDC generates logical operations (such as INSERT/UPDATE/DELETE) that are equivalent to SQL semantics, rather than restoring the original SQL executed upstream one by one. Refer to [TiCDC's Implementation Principles for Processing Data Changes](/ticdc/ticdc-overview.md#implementation-of-processing-data-changes).

+ TiCDC guarantees eventual consistency of transactions. [redo log](/ticdc/ticdc-sink-to-mysql.md#eventually-consistent-replication-in-disaster-scenarios) provides the final consistency guarantee in disaster recovery scenarios. [Syncpoint](/ticdc/ticdc-upstream-downstream-check.md#enable-syncpoint) provides consistent snapshot reads and data consistency checks.

## Downstream Systems Supported by TiCDC

TiCDC supports replication data to multiple downstreams, including:

- [TiDB and MySQL-compatible databases](/ticdc/ticdc-sink-to-mysql.md)
- [Message Queue(MQ) Sink](/ticdc/ticdc-changefeed-config.md#sink), such as [Kafka](/ticdc/ticdc-sink-to-kafka.md), [Pulsar](/ticdc/ticdc-sink-to-pulsar.md)
- [Cloud Storage Sink](/ticdc/ticdc-sink-to-cloud-storage.md), such as Amazon S3, GCS, Azure Blob Storage, and NFS.
- [Integrate Data with Confluent Cloud and Snowflake](/ticdc/integrate-confluent-using-ticdc.md)
- [Integrate Data with Apache Kafka and Apache Flink](/ticdc/replicate-data-to-kafka-and-flink.md)


# Data Replication Scope of TiCDC

TiCDC supports the following upstream data changes:

- Support
  - DDL and DML statements(exclude system tables).
  - Index Action(`ADD INDEX`, `CREATE INDEX`): to reduce the impact on the replication delay of Changefeed, if the downstream is TiDB, TiCDC will [asynchronously execute the DDL operations of creating and adding indexes](/ticdc/ticdc-ddl.md#asynchronous-execution-of-add-index-and-create-index-ddls)
  - Foreign Key Constraints DDL(`ADD FOREIGN KEY`): TiCDC is not responsible for synchronizing the settings of upstream system variables, such as [foreign_key_checks](/system-variables.md#foreign_key_checks). Therefore, you need to set appropriate system variables in the downstream to determine whether the downstream foreign key constraint check is enabled.

- Not Support:
  - DDL and DML statements executed in upstream system tables (including `mysql.*` and `information_schema.*`).
  - DDL and DML statements executed in upstream temporary tables.
  - DQL (Data Query Language) and DCL (Data Control Language) statements.

## TiCDC Usage Limitations​

- TiCDC does not support some scenarios. For details, see [Unsupported scenarios](/ticdc/ticdc-overview.md#unsupported-scenarios).
- TiCDC only checks the integrity of the upstream changes received internally, and does not participate in checking whether the data changes meet the various downstream constraints. If a data change that does not meet the downstream constraints is encountered, TiCDC will report an error when writing to the downstream.