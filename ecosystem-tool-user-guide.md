---
title: TiDB Ecosystem Tools Overview
category: reference
aliases: ['/docs/v2.1/reference/tools/user-guide/','/docs/v2.1/how-to/migrate/from-mysql/','/docs/v2.1/how-to/migrate/incrementally-from-mysql/','/docs/v2.1/how-to/migrate/overview/']
---

# TiDB Ecosystem Tools Overview

This document introduces the functionalities of TiDB ecosystem tools and their relationship.

## Full data export 

[Dumpling](/export-or-backup-using-dumpling.md) is a tool for the logical full data export from MySQL or TiDB.

The following are the basics of Dumpling:

- Input: MySQL/TiDB cluster
- Output: SQL/CSV file
- Supported TiDB versions: all versions
- Kubernetes support: No

## Full data import

[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) (Lightning) is a tool used for the full import of large amounts of data into a TiDB cluster. Currently, TiDB Lightning supports reading SQL dump exported via Dumpling or CSV data source.

TiDB Lightning supports two modes:

- `importer`: This mode uses tikv-importer as the backend, which is usually for importing a large amount of data (at the TB level). During the import, the cluster cannot provide services.
- `tidb`: This mode uses TiDB/MySQL as the backend, which is slower than the `importer` mode but can be performed online. It also supports importing data to MySQL.

The following are the basics of TiDB Lightning:

- Input data source:
    - The output file of Dumpling
    - Other compatible CSV file
- Supported TiDB versions: v2.1 or later
- Kubernetes support: Yes. See [Quickly restore data into a TiDB cluster in Kubernetes using TiDB Lightning](https://pingcap.com/docs/tidb-in-kubernetes/stable/restore-data-using-tidb-lightning/) for details.

> **Note:**
>
> The Loader tool is no longer maintained. For scenarios related to Loader, it is recommended that you use the [`tidb` mode of TiDB Lighting](/tidb-lightning/tidb-lightning-overview.md) instead.

## Backup and restore

[Dumpling](/export-or-backup-using-dumpling.md) can be used to back up the TiDB cluster to SQL/CSV files. See [Full data export](#full-data-export).

[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) can be used to restore the SQL/CSV files exported by Dumpling to the TiDB cluster. See [Full data import](#full-data-import).

## Incremental data replication

[TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md) is a tool that collects binlog for TiDB clusters and provides near real-time sync and backup. It can be used for incremental data replication between TiDB clusters, such as making a TiDB cluster the secondary cluster of the primary TiDB cluster.

The following are the basics of TiDB Binlog:

- Input: TiDB cluster
- Output: TiDB cluster, MySQL, Kafka or incremental backup files
- Supported TiDB versions: v2.1 or later
- Kubernetes support: Yes. See [TiDB Binlog Cluster Operations](https://pingcap.com/docs/tidb-in-kubernetes/stable/deploy-tidb-binlog/) and [TiDB Binlog Drainer Configurations in Kubernetes](https://pingcap.com/docs/tidb-in-kubernetes/stable/configure-tidb-binlog-drainer/) for details.

## Data migration

[TiDB Data Migration](https://pingcap.com/docs/tidb-data-migration/stable/) (DM) is an integrated data replication task management platform that supports the full data migration and the incremental data migration from MySQL/MariaDB to TiDB.

The following are the basics of DM:

- Input: MySQL/MariaDB
- Output: TiDB cluster
- Supported TiDB versions: all versions
- Kubernetes support: No, under development

If the data volume is below the TB level, it is recommended to migrate data from MySQL/MariaDB to TiDB directly using DM. The migration process includes the full data import and export and the incremental data replication.

If the data volume is at the TB level, take the following steps:

1. Use [Dumpling](/export-or-backup-using-dumpling.md) to export the full data from MySQL/MariaDB.
2. Use [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) to import the data exported in Step 1 to the TiDB cluster.
3. Use DM to migrate the incremental data from MySQL/MariaDB to TiDB.

> **Note:**
>
> The Syncer tool is no longer maintained. For scenarios related to Syncer, it is recommended that you use DM's incremental task mode instead.
