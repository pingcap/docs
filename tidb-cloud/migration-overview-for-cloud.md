---
title: Migration Overview
summary: Learn the overview of data migration scenarios and the solutions for TiDB Cloud.
---

# Migration Overview

You can migrate data from a wide variety of data sources to TiDB Cloud. This document gives an overview of the data migration scenarios.

## Migrate data from MySQL-compatible databases

TiDB is highly compatible with MySQL. You can migrate data from any MySQL-compatible databases to TiDB smoothly, whether the data is from a self-hosted MySQL instance or RDS service provided by the public cloud. For more information, see [Migrate Data from MySQL-Compatible Databases](/tidb-cloud/migrate-data-into-tidb.md).

After full data migration, you can also perform incremental data migration from MySQL-compatible databases to TiDB Cloud. For more information, see [Migrate Incremental Data from MySQL-Compatible Databases](/tidb-cloud/migrate-incremental-data-from-mysql.md).

If your application uses MySQL shards for data storage, you can migrate these shards into TiDB Cloud as one table. For more information, see [Migrate and Merge MySQL Shards of Large Datasets to TiDB Cloud](/tidb-cloud/migrate-sql-shards.md)

## Migrate from Amazon Aurora MySQL to TiDB Cloud in bulk

You can migrate data from Amazon Aurora MySQL to TiDB Cloud in bulk using the import tools on TiDB Cloud console.

For more information, see [Migrate from Amazon Aurora MySQL to TiDB Cloud in Bulk](/tidb-cloud/migrate-from-aurora-bulk-import.md)

## Import or migrate from Amazon S3 or GCS to TiDB Cloud

You can use Amazon Simple Storage Service (Amazon S3) or Google Cloud Storage (GCS) as a staging area for importing or migrating data into TiDB Cloud.

For more information, see [Import or Migrate from Amazon S3 or GCS to TiDB Cloud](/tidb-cloud/migrate-from-amazon-s3-or-gcs.md)

## Migrate data from files to TiDB Cloud

- [Import CSV Files from Amazon S3 or GCS into TiDB Cloud](/tidb-cloud/import-csv-files.md)
- [Import Apache Parquet Files from Amazon S3 or GCS into TiDB Cloud](/tidb-cloud/import-parquet-files.md)
