---
title: TiDB Serverless Export (Beta)
summary: Learn how to export data from TiDB Serverless clusters.
---

# TiDB Serverless Export (Beta)

TiDB Serverless Export (Beta) is a service that enables you to export data from a TiDB Serverless cluster to local storage or an external storage service. You can use the exported data for backup, migration, data analysis, or other purposes.

While you can also export data using `mysqldump`, TiDB Dumpling, or other tools, TiDB Serverless Export offers a more convenient and efficient way to export data from a TiDB Serverless cluster. It brings the following benefits:

- Convenience: the export service provides a simple and easy-to-use way to export data from a TiDB Serverless cluster, eliminating the need for additional tools or resources.
- Isolation: the export service uses separate computing resources, ensuring isolation from the resources used by your online services.
- Consistency: the export service ensures the consistency of the exported data without causing locks, which does not affect your online services.

## Features

### Location of files

You can export data to the local storage or an external storage service.

**Local storage**

There are some limitations when you export data to local storage:

1. You are not allowed to export multiple databases at the same time.
2. The exported data will be expired after two days, please download the data in time.
3. The exported data will be saved in the stashing area, which offers 250 GB storage space for each organization per region. If the storage space is full, you will not be able to export data to local.

**[Amazon S3](https://aws.amazon.com/s3/)**

You need to provide the credentials of the S3 bucket. Supported credentials include:

- [Access Key](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html): The long-term credentials for an IAM user or the AWS account root user. Please make sure the access key has the necessary permissions to your S3 bucket, we recommend you create a new bucket with full s3 access.
  
> **Note:**
>
> We recommend you export to the external storage service such as S3 when you want to export a large amount of data.

### Data Filtering

You can filter data by specifying the database and table you want to export. If you do not specify the table, we will export all tables in the specified database. If you do not specify the database, we will export all databases in the cluster.

> **Note:**
>
> You must specify the database when you export data to local storage.

### Data Formats

You can export data in the following formats:

- SQL(default): export data in SQL format.
- CSV: export data in CSV format.

### Data Compression

You can compress the exported data in the following algorithms:

- gzip(default): compress the exported data with gzip 
- snappy: compress the exported data with snappy.
- zstd: compress the exported data with zstd.
- none: do not compress the exported data.

### Cancel Export

You can cancel an export job that is in running state.

## Examples

Now, you can manage exports with [TiDB Cloud CLI](/tidb-cloud/cli-reference.md).

### Export to local

First, create an export job which specifies the database and table you want to export. It will output the export ID.

   ```sh
   ticloud serverless export create -c <cluster-id> --database <database> --table <table>
   ```

Then, download the exported data after the export is succeeded.

   ```sh
   ticloud serverless export download -c <cluster-id> -e <export-id>
   ```

### Export to S3

   ```sh
   ticloud serverless export create -c <cluster-id> --bucket-uri <bucket-uri> --access-key-id <access-key-id> --secret-access-key <secret-access-key>
   ```

### Export with CSV format

   ```sh
   ticloud serverless export create -c <cluster-id> --file-type CSV
   ```

### Export the whole database

   ```sh
   ticloud serverless export create -c <cluster-id> --database <database>
   ```

### Export with snappy compression.

   ```sh
   ticloud serverless export create -c <cluster-id> --compress snappy
   ```

### Cancel an export job

   ```sh
   ticloud serverless export cancel -c <cluster-id> -e <export-id>
   ```

## Pricing

You will only be charged for a successful or canceled export.

The export service is free during the beta period. You only need to pay for the [Request Units (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit) generated during the export process.