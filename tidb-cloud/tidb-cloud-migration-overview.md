---
title: Migration and Import Overview
summary: 了解 TiDB Cloud 的数据迁移和导入场景概览。
aliases: ['/tidbcloud/export-data-from-tidb-cloud']
---

# 迁移与导入概览

你可以将数据从多种数据源迁移到 TiDB Cloud。本文档将对数据迁移场景进行概述。

## 从 MySQL 兼容数据库迁移数据

当你从 MySQL 兼容数据库迁移数据时，可以执行全量数据迁移和增量数据迁移。具体的迁移场景和方法如下：

- 使用 Data Migration 迁移 MySQL 兼容数据库

    TiDB 对 MySQL 具有高度兼容性。你可以在 TiDB Cloud 控制台中使用 Data Migration，将任何 MySQL 兼容数据库的数据平滑迁移到 TiDB Cloud。更多信息，参见 [Migrate MySQL-Compatible Databases to TiDB Cloud Using Data Migration](/tidb-cloud/migrate-from-mysql-using-data-migration.md)。

- 使用 AWS DMS 进行迁移

    如果你需要将异构数据库（如 PostgreSQL、Oracle 和 SQL Server）迁移到 TiDB Cloud，推荐使用 AWS Database Migration Service（AWS DMS）。

    - [Migrate from MySQL-Compatible Databases to TiDB Cloud Using AWS DMS](/tidb-cloud/migrate-from-mysql-using-aws-dms.md)
    - [Migrate from Amazon RDS for Oracle Using AWS DMS](/tidb-cloud/migrate-from-oracle-using-aws-dms.md)

- 迁移并合并 MySQL 分片

    如果你的应用使用 MySQL 分片进行数据存储，可以将这些分片合并迁移到 TiDB Cloud 的一张表中。更多信息，参见 [Migrate and Merge MySQL Shards of Large Datasets to TiDB Cloud](/tidb-cloud/migrate-sql-shards.md)。

- 从 TiDB 自建集群迁移

    你可以通过 Dumpling 和 TiCDC，将自建 TiDB 集群的数据迁移到 TiDB Cloud（AWS）。更多信息，参见 [Migrate from TiDB Self-Managed to TiDB Cloud](/tidb-cloud/migrate-from-op-tidb.md)。

## 从文件导入数据到 TiDB Cloud

如果你有 SQL、CSV、Parquet 或 Aurora Snapshot 格式的数据文件，可以一次性将这些文件导入到 TiDB Cloud。具体的导入场景和方法如下：

- 导入本地 CSV 文件到 TiDB Cloud

    你可以将本地 CSV 文件导入到 TiDB Cloud。更多信息，参见 [Import Local Files to TiDB Cloud](/tidb-cloud/tidb-cloud-import-local-files.md)。

- 导入示例数据（SQL 文件）到 TiDB Cloud

    你可以将示例数据（SQL 文件）导入到 TiDB Cloud，以便快速熟悉 TiDB Cloud 的界面和导入流程。更多信息，参见 [Import Sample Data to TiDB Cloud Serverless](/tidb-cloud/import-sample-data-serverless.md) 和 [Import Sample Data to TiDB Cloud Dedicated](/tidb-cloud/import-sample-data.md)。

- 从 Amazon S3、Google Cloud Storage（GCS）或 Azure Blob Storage 导入 CSV 文件到 TiDB Cloud

    你可以从 Amazon S3、Google Cloud Storage（GCS）或 Azure Blob Storage 导入 CSV 文件到 TiDB Cloud。更多信息，参见 [Import CSV Files from Cloud Storage into TiDB Cloud Serverless](/tidb-cloud/import-csv-files-serverless.md) 和 [Import CSV Files from Cloud Storage into TiDB Cloud Dedicated](/tidb-cloud/import-csv-files.md)。

- 从 Amazon S3、Google Cloud Storage（GCS）或 Azure Blob Storage 导入 Apache Parquet 文件到 TiDB Cloud

    你可以从 Amazon S3、Google Cloud Storage（GCS）或 Azure Blob Storage 导入 Parquet 文件到 TiDB Cloud。更多信息，参见 [Import Apache Parquet Files from Cloud Storage into TiDB Cloud Serverless](/tidb-cloud/import-parquet-files-serverless.md) 和 [Import Apache Parquet Files from Cloud Storage into TiDB Cloud Dedicated](/tidb-cloud/import-parquet-files.md)。

## 参考

### 配置云存储访问

如果你的源数据存储在 Amazon S3、Google Cloud Storage（GCS）桶或 Azure Blob Storage 容器中，在将数据导入或迁移到 TiDB Cloud 之前，需要先配置存储访问。更多信息，参见 [Configure External Storage Access for TiDB Cloud Serverless](/tidb-cloud/serverless-external-storage.md) 和 [Configure External Storage Access for TiDB Cloud Dedicated](/tidb-cloud/dedicated-external-storage.md)。

### 数据导入命名规范

为确保数据能够成功导入，你需要准备符合命名规范的 schema 文件和数据文件。更多信息，参见 [Naming Conventions for Data Import](/tidb-cloud/naming-conventions-for-data-import.md)。

### 排查从 Amazon S3 导入数据时的访问被拒绝错误

你可以排查在从 Amazon S3 导入数据到 TiDB Cloud 时可能出现的访问被拒绝错误。更多信息，参见 [Troubleshoot Access Denied Errors during Data Import from Amazon S3](/tidb-cloud/troubleshoot-import-access-denied-error.md)。