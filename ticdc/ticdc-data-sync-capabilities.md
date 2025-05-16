---
title: TiCDC's Data Synchronization Capability
summary: Learn the TiCDC's data synchronization capabilities.
---

# TiCDC's Data Synchronization Capability

## Backgroud

TiCDC (TiDB Change Data Capture) is a core component for real-time data synchronization in the TiDB ecosystem.

1. TiCDC monitors TiKV's Raft Log to convert row-level data changes (insert/update/delete) into downstream-compatible SQL statements. Unlike Binlog, TiCDC does not rely on parsing SQL statements. Refer to [TiCDC's Implementation Principles for Processing Data Changes](/ticdc/ticdc-overview.md#implementation-of-processing-data-changes).


2. TiCDC generates logical operations (such as INSERT/UPDATE/DELETE) that are equivalent to SQL semantics, rather than restoring the original SQL executed upstream one by one. Refer to [TiCDC's Implementation Principles for Processing Data Changes](/ticdc/ticdc-overview.md#implementation-of-processing-data-changes).

3. TiCDC provides the guarantee of eventual consistency of transactions. [redo log](/ticdc/ticdc-sink-to-mysql.md#eventually-consistent-replication-in-disaster-scenarios) provides the final consistency guarantee in disaster recovery scenarios. [Syncpoint](/ticdc/ticdc-upstream-downstream-check.md#enable-syncpoint) provides consistent snapshot reads and data consistency checks.

4. TiCDC supports synchronizing data to multiple downstreams, including [TiDB and MySQL-compatible databases](/ticdc/ticdc-sink-to-mysql.md), [Kafka](/ticdc/ticdc-sink-to-kafka.md), [Pulsar](/ticdc/ticdc-sink-to-pulsar), [storage services (Amazon S3, GCS, Azure Blob Storage, and NFS](/ticdc/ticdc-sink-to-cloud-storage.md).

## Data synchronization capabilities of TiCDC

1. TiCDC supports synchronizing DDL and DML statements executed upstream, but does not synchronize DDL and DML executed in upstream system tables (including `mysql.*` and `information_schema.*`), nor does it synchronize temporary tables created in the upstream.

2. TiCDC does not support synchronizing DQL (Data Query Language) statements, nor does it support synchronizing DCL (Data Control Language) statements.

3. TiCDC supports synchronizing the settings of the index in the upstream table through DDL (`add index`, `create index`), and in order to reduce the impact on the synchronization delay of Changefeed, if the downstream is TiDB, TiCDC will [asynchronously execute the DDL operations of creating and adding indexes](/ticdc/ticdc-ddl.md#asynchronous-execution-of-add-index-and-create-index-ddls).

4. For the foreign key constraints set in the table, TiCDC will synchronize the corresponding DDL (`add foreign key`) statements, but TiCDC is not responsible for synchronizing the settings of upstream system variables, such as [foreign_key_checks](/system-variables.md#foreign_key_checks). Therefore, customers need to set appropriate system variables in the downstream to determine whether the downstream foreign key constraint check is enabled.

5. TiCDC only checks the integrity of the upstream changes received internally, and does not participate in checking whether the data changes meet the various downstream constraints. If a data change that does not meet the downstream constraints is encountered, TiCDC will report an error when writing downstream.