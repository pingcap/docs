---
title: TiDB Serverless Export (Beta)
summary: Learn how to export data from TiDB Serverless clusters.
---

# TiDB Serverless Export (Beta)

TiDB Serverless Export (Beta) is a service that enables you to export data from a TiDB Serverless cluster to local storage or an external storage service. You can use the exported data for backup, migration, data analysis, or other purposes.

While you can also export data using tools such as [mysqldump](https://dev.mysql.com/doc/refman/8.0/en/mysqldump.html) and TiDB [Dumpling](https://docs.pingcap.com/tidb/dev/dumpling-overview), TiDB Serverless Export offers a more convenient and efficient way to export data from a TiDB Serverless cluster. It brings the following benefits:

- Convenience: the export service provides a simple and easy-to-use way to export data from a TiDB Serverless cluster, eliminating the need for additional tools or resources.
- Isolation: the export service uses separate computing resources, ensuring isolation from the resources used by your online services.
- Consistency: the export service ensures the consistency of the exported data without causing locks, which does not affect your online services.

## Features

This section describes the features of TiDB Serverless Export.

### Export location

You can export data to local storage or [Amazon S3](https://aws.amazon.com/s3/).

> **Note:**
>
> If the size of the data to be exported is large(more than 100 GiB), it is recommended that you export it to Amazon S3.

**Local storage**

Exporting data to local storage has the following limitations:

- Exporting multiple databases to local storage at the same time is not supported.
- Exported data is saved in the stashing area and will expire after two days. You need to download the exported data in time.
- TiDB Cloud offers 250 GiB of storage space in the stashing area for each organization per region. If the storage space is full, you will not be able to export data to local storage.

**Amazon S3**

To export data to Amazon S3, you need to provide an [access key](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html) for your S3 bucket. Please make sure the access key has the read and write access for your S3 bucket, including at least these permissions: `s3:PutObject`, and `s3:ListBucket`.


### Data filtering

You can filter data by specifying the database and table you want to export. If you specify a database without specifying a table, all tables in that specified database will be exported. If you do not specify a database when you export data to Amazon S3, all databases in the cluster will be exported.

> **Note:**
>
> You must specify the database when you export data to local storage.

### Data formats

You can export data in the following formats:

- `SQL` (default): export data in SQL format.
- `CSV`: export data in CSV format.

### Data compression

You can compress the exported data using the following algorithms:

- `gzip` (default): compress the exported data with gzip.
- `snappy`: compress the exported data with snappy.
- `zstd`: compress the exported data with zstd.
- `none`: do not compress the exported data.

### Cancel export

You can cancel an export job that is in the running state.

## Examples

Currently, you can manage export jobs using [TiDB Cloud CLI](/tidb-cloud/cli-reference.md).

### Export data to local storage

1. Create an export job that specifies the database and table you want to export:

   ```shell
   ticloud serverless export create -c <cluster-id> --database <database> --table <table>
   ```

    You will get an export ID from the output.

2. After the export is successful, download the exported data to your local storage:

   ```shell
   ticloud serverless export download -c <cluster-id> -e <export-id>
   ```

### Export data to Amazon S3

   ```shell
   ticloud serverless export create -c <cluster-id> --bucket-uri <bucket-uri> --access-key-id <access-key-id> --secret-access-key <secret-access-key>
   ```

### Export with the CSV format

   ```shell
   ticloud serverless export create -c <cluster-id> --file-type CSV
   ```

### Export the whole database

   ```shell
   ticloud serverless export create -c <cluster-id> --database <database>
   ```

### Export with snappy compression

   ```shell
   ticloud serverless export create -c <cluster-id> --compress snappy
   ```

### Cancel an export job

   ```shell
   ticloud serverless export cancel -c <cluster-id> -e <export-id>
   ```

## Pricing

The export service is free during the beta period. You only need to pay for the [Request Units (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit) generated during the export process of successful or canceled jobs. For failed export jobs, you will not be charged.