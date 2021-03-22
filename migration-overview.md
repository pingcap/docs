---
title: Migration Overview
summary: This document describes how to migrate data from databases or data formats (CSV/SQL).
aliases: ['/docs/stable/migration-overview/','/docs/v4.0/migration-overview/','/docs/op-guide/migration-overview/']
---

# Migration Overview

This document describes how to migrate data to TiDB, including migrating data from MySQL and from CSV/SQL files.

## Migrate from Aurora to TiDB

In a cloud environment, you can directly migrate full data to TiDB by exporting snapshot from Aurora. For details, see [Migrate from Amazon Aurora MySQL Using TiDB Lightning](/migrate-from-aurora-using-lightning.md).

## Migrate from MySQL to TiDB

To migrate data from MySQL to TiDB, it is recommended to use one of the following methods:

- [Use Dumpling and TiDB Lightning](#use-dumpling-and-tidb-lightning-full-data) to migrate full data.
- [Use TiDB Data Migration (DM)](#use-dm) to migrate full and incremental data.

### Use Dumpling and TiDB Lightning (full data)

#### Scenarios

You can use Dumpling and TiDB Lightning to migrate full data when the data size is greater than 1 TB. If you need to replicate incremental data, it is recommended to [use DM](#use-dm) to create an incremental replication task.

#### Migration method

1. Use Dumpling to export the full MySQL data.
2. Use TiDB Lightning to import the full data to TiDB. For details, refer to [Migrate data using Dumpling and TiDB Lightning](/migrate-from-mysql-dumpling-files.md).

### Use DM

#### Scenarios

You can use DM to migrate full MySQL data and to replicate incremental data. It is suggested that the size of the full data is less than 1 TB. Otherwise, it is recommended to use Dumpling and TiDB Lightning to import the full data, and then use DM to replicate the incremental data.

#### Migration method

For details, refer to [Migrate from MySQL (Amazon Aurora)](https://docs.pingcap.com/tidb-data-migration/v2.0/migrate-from-mysql-aurora).

## Migrate data from files to TiDB

You can migrate data from CSV/SQL files to TiDB.

### Migrate data from CSV files to TiDB

#### Scenarios

You can migrate data from heterogeneous databases that are not compatible with the MySQL protocol to TiDB.

#### Migration method

1. Export full data to CSV files.
2. Import CSV files to TiDB using one of the following methods:

    - Use TiDB Lightning.

        Its import speed is fast. It is recommended to use TiDB Lightning in the case of large amounts of data in CSV files. For details, refer to [TiDB Lightning CSV Support](/tidb-lightning/migrate-from-csv-using-tidb-lightning.md).

    - Use the `LOAD DATA` statement.

        Execute the `LOAD DATA` statement in TiDB to import CSV files. This is more convenient, but if an error or interruption occurs during the import, manual intervention is required to check the consistency and integrity of the data. Therefore, it is **not recommended** to use this method in the production environment. For details, refer to [LOAD DATA](/sql-statements/sql-statement-load-data.md).

### Migrate data from SQL files to TiDB

Use Mydumper and TiDB Lightning to migrate data from SQL files to TiDB. For details, refer to [Use Dumpling and TiDB Lightning](#use-dumpling-and-tidb-lightning-full-data).
