---
title: Migrate Data from Vitess to TiDB
summary: Learn about the tools to migrate data from Vitess to TiDB. 
---

# Migrate Data from Vitess to TiDB

This document describes the tools that you can use to migrate data from [Vitess](https://vitess.io/) to TiDB. 

As the backend of Vitess is based on MySQL, when migrating data from Vitess to TiDB, you can use the same migration tools that are applicable to MySQL, such as [Dumpling](/dumpling-overview.md), [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md), and [TiDB Data Migration (DM)](/dm/dm-overview.md). Note that these tools should be set up for each shard in Vitess for data migration.

In addition to these tools, you can also use [Debezium connector for Vitess](https://debezium.io/documentation/reference/connectors/vitess.html). This connector enables you to use [Kafka Connect](https://kafka.apache.org/documentation/#connect) or [Apache Flink](https://nightlies.apache.org/flink/flink-docs-stable/) to stream changes from Vitess to TiDB.

Because both Vitess and TiDB support the MySQL protocol and SQL dialect, changes at the application level are expected to be small. For tasks directly managing sharding or other implementation-specific aspects, however, the changes might be larger. To facilitate the data migration from Vitess to TiDB, TiDB introduces the [`VITESS_HASH()`](/functions-and-operators/tidb-functions.md) function, which returns the hash of a string that is compatible with Vitess' HASH function.

## Examples

### Dumpling and TiDB Lightning

The following two examples show how Dumpling and TiDB Lightning work together to migrate data from Vitess to TiDB.

- In this example, TiDB Lightning uses the [logical import mode](/tidb-lightning/tidb-lightning-logical-import-mode.md), which first encodes data into SQL statements and then runs the SQL statements to import data.

    ![Vitess to TiDB Migration with TiDB backend](/media/vitess_to_tidb.png)

- In this example, TiDB Lightning uses the [physical import mode](/tidb-lightning/tidb-lightning-physical-import-mode.md) to directly ingest data into TiKV.

    ![Vitess to TiDB Migration with local backend](/media/vitess_to_tidb_dumpling_local.png)

### DM

The following example shows how DM migrates data from Vitess to TiDB.

![Vitess to TiDB with DM](/media/vitess_to_tidb_dm.png)
