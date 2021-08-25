---
title: Migrate from Amazon Aurora MySQL to TiDB
summary: Learn how to migrate full data from Amazon Aurora MySQL to TiDB.
---

# Overview of migration from Aurora to TiDB

This document introduces how to migrate full data from Amazon Aurora MySQL to TiDB. Here is a list of tools that may be used and the differences

|Tool|Data Export|Data Import|Increment Sync|Export Speed| Import Speed|
|:-: |:-:|:-:|:-:|:-:|:-:|
|[Dumpling](https://github.com/pingcap/dumpling)|Yes|No|No|Very Fast|-|
|[Lightning](/tidb-lightning/tidb-lightning-overview.md)|No|Yes|No|-|Very Fast|
|[Data Migration](https://github.com/pingcap/dm) (DM)|Yes|Yes|Yes|Very Fast | Normal|

Using existing snapshot in Aurora is the most convenient way. However, [DM](https://github.com/pingcap/dm) does not yet support the parquet format, so you need to do the following:

1. Use Dumpling for schema export.
2. Use TiDB Lightning for full schema and data import. 
3. Use DM for incremental data replication.

***

## Topics

- [Migrate from Aurora snapshot to TiDB](/data-migration/aurora/from-snapshot.md)
- [Incrementally synchronize data to TiDB](/data-migration/aurora/increment-aurora.md)
