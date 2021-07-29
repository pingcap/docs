---
title: Migrate from MySQL to TiDB
summary: Learn how to migrate full data from  MySQL to TiDB.
---

# Overview of migration from MySQL to TiDB

This document introduces how to migrate full data from  MySQL to TiDB.

[Dumpling](https://github.com/pingcap/dumpling) exports data stored in TiDB/MySQL as SQL or CSV data files and can be used to make a logical full backup or export.

[Lightning](/tidb-lightning/tidb-lightning-overview.md) is a tool used for fast full import of large amounts of data into a TiDB cluster. 

[Data Migration](https://github.com/pingcap/dm) (DM) is an data migration task management platform, supports the full data migration and incremental data replication into TiDB. 

It is recommended to use [Dumpling](https://github.com/pingcap/dumpling) and [Lightning](/tidb-lightning/tidb-lightning-overview.md) in large data import scenarios, [DM](https://github.com/pingcap/dm) in small and incremental data synchronization scenarios because of the data import speed of DM is not fast.

## Topics

- [MySQL ≥ 1TB](/data-migration/mysql/huge-data.md)
- [MySQL ＜ 1TB](/data-migration/mysql/small-data.md)
- [Incrementally synchronize data to TiDB](/data-migration/mysql/increment.md)
