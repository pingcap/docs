---
title: Migrate from Amazon Aurora MySQL to TiDB
summary: Learn how to migrate full data from Amazon Aurora MySQL to TiDB.
---

# Overview of migration from Aurora to TiDB

This document describes how to migrate full data from Amazon Aurora MySQL to TiDB. Here is a list of tools that you can use:

|Tool|Data Export|Data Import|Increment Sync|Export Speed| Import Speed|
|:-: |:-:|:-:|:-:|:-:|:-:|
|[Dumpling](https://github.com/pingcap/dumpling)|Yes|No|No|Fast|-|
|[Lightning](/tidb-lightning/tidb-lightning-overview.md)|No|Yes|No|-|Fast|
|[Data Migration](https://github.com/pingcap/dm) (DM)|Yes|Yes|Yes|Fast| Normal|

Using the existing snapshot in Aurora is the most convenient way. However, [DM](https://github.com/pingcap/dm) does not yet support the parquet format, so for different task mode, you need to use different tools as follows:

1. Use Dumpling for schema export.
2. Use TiDB Lightning for full schema and data import. 
3. Use DM for incremental data replication.

***

## Topics

- [Migrate from Aurora snapshot to TiDB](/data-migration/aurora/from-snapshot.md)
- [Incrementally synchronize data to TiDB](/data-migration/aurora/increment-aurora.md)
