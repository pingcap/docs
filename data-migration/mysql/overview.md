# How to migrate from MySQL to TiDB

This document introduces how to migrate full data from  MySQL to TiDB using Dumpling and Lightning.

[Dumpling](https://github.com/pingcap/dumpling) exports data stored in TiDB/MySQL as SQL or CSV data files and can be used to make a logical full backup or export.

[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) is a tool used for fast full import of large amounts of data into a TiDB cluster. 

[TiDB Data Migration](https://github.com/pingcap/dm) (DM) is an integrated data migration task management platform, which supports the full data migration and the incremental data replication from MySQL-compatible databases (such as MySQL, MariaDB, and Aurora MySQL) into TiDB. It can help to reduce the operation cost of data migration and simplify the troubleshooting process. 

[DM](https://github.com/pingcap/dm) supports the full data migration and the incremental data replication, However, the data import speed of DM in the current version is not fast.

Therefore, it is recommended to use [Dumpling](https://github.com/pingcap/dumpling) and [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) in large data import scenarios, and [DM](https://github.com/pingcap/dm) in small and incremental data synchronization scenarios.

## Topics

- [Origin MySQL ≥ 1TB](/data-migration/mysql/huge-data.md)
- [Origin MySQL ＜ 1TB](/data-migration/mysql/small-data.md)
- [Incrementally synchronize data to TiDB](/data-migration/mysql/increment.md)
