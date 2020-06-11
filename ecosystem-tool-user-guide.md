---
title: TiDB Ecosystem Tools Overview
category: reference
aliases: ['/docs/v3.1/reference/tools/user-guide/','/docs/v3.1/how-to/migrate/from-mysql/','/docs/v3.1/how-to/migrate/incrementally-from-mysql/','/docs/v3.1/how-to/migrate/overview/']
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
> The Loader tool is no longer maintained. For scenarios related to Loader, it is recommended that you use the `tidb` mode of TiDB Lighting instead.

## Backup and restore

[Backup & Restore](/br/backup-and-restore-tool.md) (BR) is a command-line tool for distributed backup and restore of the TiDB cluster data. BR can effectively back up and restore TiDB clusters of huge data volume.

The following are the basics of BR:

- [Input and output data source](/br/backup-and-restore-tool.md#types-of-backup-files): SST + `backupmeta` file
- Supported TiDB versions: v3.1 and v4.0
- Kubernetes support: Yes. See [Back up Data to S3-Compatible Storage Using BR](https://pingcap.com/docs/tidb-in-kubernetes/stable/backup-to-aws-s3-using-br/) and [Restore Data from S3-Compatible Storage Using BR](https://pingcap.com/docs/tidb-in-kubernetes/stable/restore-from-aws-s3-using-br/) for details.

## Incremental data replication

[TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md) is a tool that collects binlog for TiDB clusters and provides near real-time sync and backup. It can be used for incremental data replication between TiDB clusters, such as making a TiDB cluster the secondary cluster of the primary TiDB cluster.

The following are the basics of TiDB Binlog:

- Input/Output:
    - Input: TiDB cluster
    - Output: TiDB cluster, MySQL, Kafka or incremental backup files
- Supported TiDB versions: v2.1 or later
- Kubernetes support: Yes. See [TiDB Binlog Cluster Operations](https://pingcap.com/docs/tidb-in-kubernetes/stable/deploy-tidb-binlog/) and [TiDB Binlog Drainer Configurations in Kubernetes](https://pingcap.com/docs/tidb-in-kubernetes/stable/configure-tidb-binlog-drainer/) for details.

<<<<<<< HEAD
#### CDC (Beta, under development, ETA May/June 2020 with TiDB 4.0)

[CDC](https://pingcap.com/docs/dev/reference/tools/ticdc/overview/) (Change Data Capture) is a system that collects changelog for key value pairs in TiKV and outputs to downstream systems in row changed order.

- Input/Output: 
    - Input: TiDB Cluster
    - Output: MySQL, TiDB, Kafka or incremental backup files
- Supported TiDB versions: v4.0
- Kubernetes support: On the development road map, ETA Q2 2020

## Recommended tools for TiDB 3.1

- MySQL full data backup: use Mydumper
- MySQL full data import to TiDB:
    - TB scale: use TiDB Lightning
    - Sub-TB scale: use DM
- MySQL incremental data sync to TiDB: use DM
- TiDB full data backup: use BR
- TiDB full data restore: use BR
- TiDB incremental backup & restore: use TiDB-Binlog

For the recommended tools for other TiDB versions, see [Recommended tools for TiDB versions](https://pingcap.com/docs/dev/reference/tools/user-guide/#recommended-tools-for-tidb-versions).

## Tools evolution roadmap 

- TiDB Full Data Backup:
    - Mydumper -> BR
    - Mydumper -> [dumpling](https://github.com/pingcap/dumpling) (under development, replace Lighting in lightweight scenarios)
- TiDB Full Data Restore:
    - Loader -> Lightning -> BR
- MySQL Data Migration:
    - Mydumper/Loader + Syncer  -> DM (in the next step, we will integrate Lightning into DM)
- TiDB Incremental Data Migration:
    - TiDB Binlog -> CDC

## Full-path data migration solution for TiDB 3.1

For TiDB 3.1 versions, this section covers how to migrate data from MySQL to TiDB, between TiDB clusters, and from TiDB to MySQL for each version, as well as how to back up and restore data.

### Migrating MySQL data to TiDB

If the MySQL data volume is in TBs:

- Use Mydumper to export MySQL full data as a backup
- Use Lightning to import the full MySQL backup data into TiDB cluster
- Use DM to replicate incremental MySQL data to TiDB

If the MySQL data volume is in GBs:

- Use DM to migrate MySQL data to TiDB for both full and incremental data import

### Data replication between TiDB/MySQL clusters

You can use TiDB Binlog to replicate data between TiDB clusters. You can also use TiDB Binlog to replicate data to the downstream MySQL cluster.

### Full backup and restore of the data in TiDB/MySQL clusters
=======
### Data migration

[TiDB Data Migration](https://pingcap.com/docs/tidb-data-migration/stable/) (DM) is an integrated data replication task management platform that supports the full data migration and the incremental data migration from MySQL/MariaDB to TiDB.

The following are the basics of DM:

- Input: MySQL/MariaDB
- Output: TiDB cluster
- Supported TiDB versions: all versions
- Kubernetes support: No, under development
>>>>>>> 37cbeea... reference: refine the ecosystem tools user guide (#2759)

If the data volume is below the TB level, it is recommended to migrate data from MySQL/MariaDB to TiDB directly using DM. The migration process includes the full data import and export and the incremental data replication.

If the data volume is at the TB level, take the following steps:

1. Use [Dumpling](/export-or-backup-using-dumpling.md) to export the full data from MySQL/MariaDB.
2. Use [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) to import the data exported in Step 1 to the TiDB cluster.
3. Use DM to migrate the incremental data from MySQL/MariaDB to TiDB.

> **Note:**
>
> The Syncer tool is no longer maintained. For scenarios related to Syncer, it is recommended that you use DM's incremental task mode instead.
