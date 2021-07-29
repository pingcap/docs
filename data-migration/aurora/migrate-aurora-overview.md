---
title: Migrate from Amazon Aurora MySQL to TiDB
summary: Learn how to migrate full data from Amazon Aurora MySQL to TiDB.
---

# Overview of migration from Aurora to TiDB

This document introduces how to migrate full data from Amazon Aurora MySQL to TiDB.

[Dumpling](https://github.com/pingcap/dumpling) exports data stored in TiDB/MySQL as SQL or CSV data files and can be used to make a logical full backup or export.

[Lightning](/tidb-lightning/tidb-lightning-overview.md) is a tool used for fast full import of large amounts of data into a TiDB cluster. 

[Data Migration](https://github.com/pingcap/dm) (DM) is an  data migration task management platform, supports the full data migration and  incremental data replication into TiDB. 

Using Aurora's existing snapshot mechanism is the most convenient way, but beacuse [DM](https://github.com/pingcap/dm) does not yet support the parquet format, so we need to use [Lightning](https://docs.pingcap.com/tidb/stable/tidb-lightning-overview) for full data import first, and then use [DM](https://github.com/pingcap/dm) for incremental data synchronization.

***

## Topics

- [Migrate from Aurora snapshot to TiDB](/data-migration/aurora/from-snapshot.md)
- [Incrementally synchronize data to TiDB](/data-migration/aurora/increment-aurora.md)
