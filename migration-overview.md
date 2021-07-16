---
title: Migration Overview
summary: This document describes how to migrate data from databases or data formats (CSV/SQL).
aliases: ['/docs/dev/migration-overview/']
---

# Migration Overview

这篇文章描述如何迁移数据到 TiDB。TiDB 提供了下面几种数据迁移功能

- 全量数据迁移：使用 TiDB Lightning 将 CSV/Aurora Snapshot/mydumper sql file 数据导入到 TiDB 集群；为了更好的配合从 MySQL/MariaDB 数据库进行全量迁移，TiDB 也提供了数据导出工具 dumpling，支持将全量数据导出成 CSV/mydumper sql 文件。

  - 快速初始化 TiDB 集群：TiDB Lightning 还提供的快速导入功能，可以实现快速初始化 TiDB 集群的指定表的效果，使用该功能前需要了解，快速导入期间对 TiDB 集群影响极大， 集群不适合对外提供访问；

- 增量数据迁移：使用 TiDB DM 从 MySQL/MariaDB/Aurora 同步 Binlog 到 TiDB，该功能可以极大降低业务迁移过程中停机窗口时间；此外 DM 提供了适合小规模数据量数据库（< 1T）的全量数据迁移功能；

- TiDB 集群复制： TiDB 支持备份恢复功能，该功能可以实现将 TiDB 的某个快照初始化到另一个全新的 TiDB 集群。

根据迁移数据所在数据库类型、部署位置、业务数据规模大小、业务需求等因素，会有不同数据迁移选择。下面展示一些常用的数据迁移场景，方便用户依据这些线索选择到最适合自己的数据迁移方案。

## Migrate from Aurora/AWS RDS to TiDB

从 Aurora/AWS RDS 迁移数据到部署在 AWS 的 TiDB 集群， 数据迁移可以氛围全量迁移和增量迁移两个步骤进行，根据你的业务需求选择相应的步骤。考虑到 Aurora/AWS RDS 和 TiDB 部署在不同 region 的情况，方案也包含介绍从不同 region 之前进行数据迁移的最佳实践。

- Aurora 全量数据迁移到 TiDB 教程
- AWS RDS 全量数据迁移到 TiDB 教程
- Aurora/AWS RDS 增量数据（Binlog）同步到 TiDB 教程

## Migrate from MySQL to TiDB

没有 Cloud storage（S3）服务，网络联通和延迟情况良好， 从 MySQL 迁移数据到 TiDB 可以考虑参照下面的方案

- 一键迁移 MySQL 数据到 TiDB 教程

如果你对数据迁移速度有要求，或者数据规模特别大（例如 > 2T），并且允许 TiDB 集群在迁移期间禁止其他业务写入，那么你可以先使用 Lightning 进行快速导入，然后根据业务需要选择是否使用 DM 进行增量数据（Binlog）同步

- 快速导入数据到 TiDB 教程

## Merge Shard Tables (on multiple MySQL) instance to TiDB

如果你的业务使用了基于 MySQL 分库的方案来存储数据，业务数据从 MySQL 迁移到 TiDB 后合并这些分表数据到一张合并，你可以使用 DM 进行分表合并迁移

- 分表合并迁移到 TiDB 教程

如果分表数据总规模特别大（例如大于 > 2T），并且允许 TiDB 集群在迁移期间禁止其他业务写入，那么你可以使用 Lightning 对分表数据进行快速合并导入，然后根据业务需要选择是否使用 DM 进行增量数据（Binlog）的分表同步

- 快速合并导入分表数据到 TiDB 教程

## Migrate to TiDB Cloud

如果你想使用 TiDB Cloud，将现在的业务迁移到 TiDB Cloud，那么可以参考下面的教程

- 业务跨云迁移到 TiDB Cloud
- IDC 业务迁移上云

## Restore a new TiDB Cluster

如果你需要构建灾备集群，或者想要将现有 TiDB 的数据快照复制到一套的新的 TiDB 集群进行测试，那么你可以使用 BR 对现有集群进行备份，然后恢复备份数据到一个新的集群

- 构建灾备集群教程
- 备份数据恢复到新的 TiDB 集群教程