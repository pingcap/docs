---
title: Data Migration Overview
summary: Learn the overview of data migration scenarios and the solutions.
---

# Data Migration Overview

This document gives an overview of the data migration solutions that you can use with TiDB. The data migration solutions are as follows:

- Full data migration.
    - To import Amazon Aurora snapshots, CSV files, or Mydumper SQL files into TiDB, you can use TiDB Lightning to perform the full migration.
    - To export all TiDB data as CSV files or Mydumper SQL files, you can use Dumpling to perform the full migration, which makes data migration from MySQL or MariaDB easier.
    - To migrate all data from a database with a small data size volume (for example, less than 1 TiB), you can also use TiDB Data Migration (DM).

- Quick initialization of TiDB. TiDB Lightning supports quickly importing data and can quickly initialize a specific table in TiDB. Before you use this feature, pay attention that the quick initialization has a great impact on TiDB and the cluster does not provide services during the initialization period.

- Incremental replication. You can use TiDB DM to replicate binlogs from MySQL, MariaDB, or Aurora to TiDB, which greatly reduces the window downtime during the replication period.

- Data replication between TiDB clusters. TiDB supports backup and restore. This feature can initialize a snapshot in an existing TiDB cluster to a new TiDB cluster.

You might choose different migration solutions according to the database type, deployment location, application data size, and application needs. The following sections introduce some common migration scenarios, and you can refer to these sections to determine the most suitable solution according to your needs.

## Migrate from Aurora MySQL to TiDB

When you migrate data from Aurora to a TiDB cluster deployed on AWS, your data migration takes two operations: full data migration and incremental replication. You can choose the corresponding operation according to your application needs.

- [Migrate Data from Amazon Aurora to TiDB](/data-migration/migrate-aurora-tidb-from-snapshot.md).

## Migrate from MySQL to TiDB

If cloud storage (S3) service is not used, the network connectivity is good, and the network latency is low, you can use the following method to migrate data from MySQL to TiDB.

- [Migrate MySQL of Small Datasets to TiDB](/data-migration/migrate-mysql-tidb-less-tb.md)

If you have a high demand on migration speed, or if the data size is large (for example, larger than 1 TiB), and you do not allow other applications to write to TiDB during the migration period, you can use TiDB Lightning to quickly import data. Then, you can use DM to replicate incremental data (binlog) based on your application needs.

- [Migrate MySQL of Large Datasets to TiDB](/data-migration/migrate-mysql-tidb-above-tb.md)

## Migrate and merge MySQL shards into TiDB

Suppose that your application uses MySQL shards for data storage, and you need to migrate these shards into TiDB as one table. In this case, you can use DM to perform the shard merge and migration.

- [Migrate and Merge MySQL Shards of Small Datasets to TiDB](/data-migration/migrate-sharding-mysql-tidb-less-tb.md)

If the data size of the sharded tables is large (for example, larger than 1 TiB), and you do not allow other applications to write to TiDB during the migration period, you can use TiDB Lightning to quickly merge and import the sharded tables. Then, you can use DM to replicate incremental sharding data (binlog) based on your application needs.

- [Migrate and Merge MySQL Shards of Large Datasets to TiDB](/data-migration/migrate-sharding-mysql-tidb-above-tb.md)

## Migrate data from files to TiDB

- [Migrate data from CSV files to TiDB](/data-migration/migrate-flat-file-tidb.md)
- [Migrate data from SQL files to TiDB](//data-migration/migrate-sql-file-tidb.md)

## More complex migration solutions

The following features can improve the migration process and might meet more needs in your application.

- [Migrate with pt/gh-host](/data-migration/migrate-with-pt-ghost.md)
- [Migrate with Binlog Event Filter](/data-migration/migrate-with-binlog-event-filter.md)
- [Migrate with Filter Binlog Events Using SQL Expressions](/data-migration/migrate-with-binlog-sql-expression-filter.md)
- [Migrate with More Columns in Downstream](/data-migration/migrate-with-more-columns-downstream.md)
