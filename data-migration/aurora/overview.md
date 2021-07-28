---
title: Migrate from Amazon Aurora MySQL to TiDB
summary: Learn how to migrate full data from Amazon Aurora MySQL to TiDB using TiDB Lightning.
---

# How to migrate from Aurora to TiDB

This document introduces how to migrate full data from Amazon Aurora MySQL to TiDB using TiDB Lightning and DM.

[TiDB Lightning](https://docs.pingcap.com/tidb/stable/tidb-lightning-overview) is a tool used for fast full import of large amounts of data into a TiDB cluster. 

[TiDB Data Migration](https://github.com/pingcap/dm) (DM) is an integrated data migration task management platform, which supports the full data migration and the incremental data replication from MySQL-compatible databases (such as MySQL, MariaDB, and Aurora MySQL) into TiDB. It can help to reduce the operation cost of data migration and simplify the troubleshooting process. 

Using Aurora's existing snapshot mechanism is the most convenient way, but beacuse [DM](https://github.com/pingcap/dm) does not yet support the parquet format, so we need to use Lighting for full data import first, and then use DM for incremental data synchronization.


***

## Topics

- [Migrate from Aurora snapshot to TiDB](/data-migration/aurora/from-snapshot.md)
- [Incrementally synchronize data to TiDB](/data-migration/aurora/increment.md)
