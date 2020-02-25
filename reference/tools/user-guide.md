---
title: TiDB Ecosystem Tools User Guide
category: reference
aliases: ['/docs-cn/how-to/migrate/from-mysql/', '/docs-cn/how-to/migrate/incrementally-from-mysql/', '/docs-cn/how-to/migrate/overview/', '/docs-cn/reference/tools/use-guide/']
---

# TiDB Ecosystem Tools User Guide

Currently TiDB contains multiple ecosystem tools. Some of these have overlapping functionality, and some are different versions of same tools. This document gives introductions of each tools, illustrates the relationships between the tools, and describes the applicable tools specified for each scenarios and each TiDB versions.

## TiDB ecosystem tools overview

TiDB ecosystem tools can be divided into:

- Data import tools, including full import tools, backup and restore tools, incremental import tools, and so forth.
- Data export tools, including full export tools. incremental export tools, and so forth.

The two types of tools are discussed in some details below.

### Data import tools

#### Full import tool loader (Stop maintenance, not recommended)

[Loader](/reference/tools/loader.md) is a lightweight full data import tool. Data in the form of SQL is imported into TiDB. Currently this tool is gradually replaced by [TiDB Lightning](#full-import-tool-tidb-lightning), see [TiDB Lightning TiDB-backend Document](/reference/tools/tidb-lightning/tidb-backend.md#migrating-from-loader-to-tidb-lightning-tidb-backend).

The following is the basics of Loader:

- Input: Files output on the Mydumper.
- Output: SQL written to TiDB.
- Applicable version of TiDB: All.
- Kubernetes: Supported. See [Backup and restore](/tidb-in-kubernetes/maintain/backup-and-restore.md).

#### Full import tool TiDB Lightning

[TiDB Lightning](/reference/tools/tidb-lightning/overview.md) is a tool used for fast full import of data into a TiDB cluster.

> **Note:**
>
> When you import data into TiDB using TiDB Lightning, there are two modes:
>
> - The default mode: Use `tikv-importer` as the backend. In this mode, the cluster can not provide normal services during the data import process. It is used when you import large amounts (TBs) of data.
> - The second mode: Use `TiDB` as the backend (similar to Loader). The  import speed is slower than that of the default mode. However, the second mode supports online import.

The following is the basics of TiDB Lightning:

- Input:
    - Files output by Mydumper;
    - CSV-formatted files.
- Applicable version of TiDB: v2.1 and later versions.
- Kubernetes: Supported. See [Quick restore data into a TiDB cluster in Kubernetes using TiDB Lightning](/tidb-in-kubernetes/maintain/lightning.md).

#### Backup and restore tool BR

[BR](/how-to/maintain/backup-and-restore/br.md) is a command-line tool for distributed backup and restoration of the TiDB cluster data. Compared with Mydumper and Loader, BR is more efficient, and more suitable for scenarios of huge data volume.

The following are the basics of BR:

- [Types of backup files](/how-to/maintain/backup-and-restore/br.md#types-of-backup-files): The SST file and the `backupmeta` file.
- Applicable version of TiDB: v3.1 and v4.0.
- Kubernetes: Supported. Relevant documents are on the way.

#### Incremental import tool Syncer (Stop maintenance, not recommended)

[Syncer](/reference/tools/syncer.md) is a tool used for incremental import of real-time binlog data from MySQL/MariaDB into TiDB. It is recommended to use [TiDB Data Migration](#Incremental-import-tool-tidb-data-migration) to replace Syncer.

The following is the basics of Syncer:

- Input: Binlog data of MySQL/MariaDB.
- Output: SQL written to TiDB.
- Applicable version of TiDB: All.
- Kubernetes: Not supported.

#### Incremental import tool TiDB Data Migration

[TiDB Data Migration (DM)](/reference/tools/data-migration/overview.md) is an tool used for data migration from MySQL/MariaDB into TiDB. It supports the full data replication and the incremental data replication.

The following is the basics of DM:

- Input: Full data and binlog data of MySQL/MariaDB.
- Output: SQL written to TiDB.
- Applicable version of TiDB: All.
- Kubernetes: In development.

### Data export tools

#### Full export tool Mydumper

[Mydumper](/reference/tools/mydumper.md) is a tool used for full logical backups of MySQL/TiDB.

The following is the basics of Mydumper:

- Input: MySQL/TiDB clusters.
- Output: SQL files.
- Applicable version of TiDB: All.
- Kubernetes: Supported. [Backup and Restore](/tidb-in-kubernetes/maintain/backup-and-restore.md).

#### Full export tool TiDB Binlog

[TiDB Binlog](/reference/tidb-binlog/overview.md) is a tool used to collect binlog data from TiDB. It provides near real-time backup and replication to downstream platforms.

The following is the basics of TiDB Binlog:

- Input: TiDB clusters.
- Output: MySQL, TiDB, Kafka or incremental backup files.
- Applicable version of TiDB: v2.1 and later versions.
- Kubernetes: Supported. [TiDB Binlog Cluster Operations](/tidb-in-kubernetes/maintain/tidb-binlog.md), [TiDB Binlog Drainer Configurations in Kubernetes](/tidb-in-kubernetes/reference/configuration/tidb-drainer.md)

## Tools development roadmap

The following is a brief introduction of TiDB ecosystem tools development, so that you can easily see the relationship between tools.

### TiDB backup and restore

Mydumper and Loader -> BR:

Mydumper and Loader are inefficient since they backup and restore data on the logical level. BR is much more efficient. It takes advantage of TiDB features to backup and restore data, and can be applied in scenarios of huge data volume.

### TiDB full restore

Loader -> TiDB Lightning:

Loader is inefficient since it performs full data restoration using SQL. TiDB Lightning is much more efficient and can be used for fast full import of large amounts (more than TBs) of data into a new TiDB cluster, since it imports data into TiKV directly. It integrates the logical data import function of Loader, see [TiDB Lightning TiDB-backend Document](/reference/tools/tidb-lightning/tidb-backend.md#migrating-from-Loader-to-TiDB-Lightning-TiDB-backend). Online data import is supported.

### MySQL data migration

- Mydumper, Loader and Syncer -> DM:

    It is tedious to migrate MySQL data to TiDB using Mydumper, Loader and Syncer. DM improves ease of use and can be used to merge the sharding data, since it provides an integrated data migration scheme.

- Loader -> TiDB Lightning:

    TiDB Lightning integrates the logical data import function of Loader, see [TiDB Lightning TiDB-backend document](/reference/tools/tidb-lightning/tidb-backend.md#migrating-from-Loader-to-TiDB-Lightning-TiDB-backend). It is used to perform all data restoration.

## Data migration solutions

For v2.1, v3.0 and v3.1 of TiDB, the following introduces data migration solutions for typical business scenarios.

### Full link data migration solutions for v2.1 and v3.0

#### Migrating MySQL data to TiDB

If the volume is more than TBs of data, the recommended migration solution is:

1. Export full MySQL data using Mydumper;
2. Import full backup data into a TiDB cluster using TiDB Lightning;
3. Replicate the incremental data of MySQL into TiDB.

If the volume is less than TBs of data, it is recommended to migrate MySQL data to TiDB using DM (the migrating process includes full data import and incremental data replication).

#### Replication of TiDB cluster data

Replication of TiDB data to downstream TiDB/MySQL using TiDB Binlog.

#### Full backup and restore of TiDB cluster data

The recommended steps are:

1. Backup full data using Mydumper;
2. Restore full data into TiDB/MySQL using TiDB Lightning.

### Full link data migration solutions for v3.1

#### Migrating MySQL data to TiDB

If the volume is more than TBs of data, the recommended migration solution is:

1. Export full MySQL data using Mydumper;
2. Import full backup data into a TiDB cluster using TiDB Lightning;
3. Replicate the incremental data of MySQL into TiDB.

If the volume is less than TBs of data, it is recommended to migrate MySQL data to TiDB using DM (the migrating process includes full data import and incremental data replication).

#### Replication of TiDB cluster data

Replication of TiDB data to downstream TiDB/MySQL using TiDB Binlog.

#### Full backup and restore of TiDB cluster data

- Restore to TiDB

    - Back up full data using BR;
    - Restore full data using BR.

- Restore to MySQL

    - Back up full data using Mydumper;
    - Restore full data using TiDB Lightning.
