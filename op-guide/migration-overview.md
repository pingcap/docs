---
title: Migration Overview
summary: Learn how to migrate data into TiDB
category: operations
---

# Migration Overview

This document describes scenarios for migrating data into TiDB from either MySQL or another data source via CSV format.

## Tools overview

Migrations will often make use of the following tools. For a brief overview of their usage:

- [`mydumper`](../tools/mydumper.md) exports data from MySQL. It is recommended over using mysqldump.
- [`loader`](../tools/loader.md) imports data in mydumper format into TiDB.
- [`syncer`](../tools/syncer.md) acts like a MySQL replication slave and pushes data from MySQL into TiDB.
- [DM](../tools/dm/overview.md) (Data Migration) integrates the functions of mydumper, Loader and syncer to support the export and import of full-size data, as well as incremental synchronization of MySQL Binlog data, and supports data synchronization of a more complete pooled table scenario.
- [TiDB-Lightning](../tools/lightning/overview-architecture.md) imports data to TiDB in an optimized way.  For example, a 1TiB backup could take 10+ hours to import with loader, but may be complete in TiDB-Lightning in just 3 hours.

## Scenarios

The following example scenarios show how you can put to use the tools mentioned above.

#### Complete dump and restore from MySQL

The recommended method to perform a complete dump and restore from MySQL is to use the following tools:
  - `mydumper`: to export data from MySQL.
  - `Loader`: to import the data into TiDB.

For detailed operations, follow the steps in [Migrate Data from MySQL to TiDB](../op-guide/migration.md).

#### Complete dump and restore with replication

For databases that are large or frequently updated, it is recommended to use the following tools:
  - `mydumper`: to export data from MySQL.
  - `Loader`: to import data to TiDB.
  - `Syncer`: to replicate data from MySQL to TiDB.

Follow our [guide for more detailed information](../op-guide/migration-incremental.md).
    
  > **Note:** To replicate data from MySQL to TiDB, binary logging [must be enabled](http://dev.mysql.com/doc/refman/5.7/en/replication-howto-masterbaseconfig.html) with the [row format](https://dev.mysql.com/doc/refman/5.7/en/binary-log-formats.html) enabled.

#### Dump and restore from database other than MySQL

To import data from another database, it is recommended to:
  - Export the data as CSV format.
  - Import the data using TiDB-Lightning.

Read more on [CSV support for TiDB-Lightning](../tools/lightning/csv.md).
