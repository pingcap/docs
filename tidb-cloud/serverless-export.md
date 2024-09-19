---
title: Export Data from TiDB Cloud Serverless
summary: Learn how to export data from TiDB Cloud Serverless clusters.
---

# Export Data from TiDB Cloud Serverless

TiDB Cloud Serverless Export (Beta) is a service that enables you to export data from a TiDB Cloud Serverless cluster to a local file or an external storage service. You can use the exported data for backup, migration, data analysis, or other purposes.

While you can also export data using tools such as [mysqldump](https://dev.mysql.com/doc/refman/8.0/en/mysqldump.html) and TiDB [Dumpling](https://docs.pingcap.com/tidb/dev/dumpling-overview), TiDB Cloud Serverless Export offers a more convenient and efficient way to export data from a TiDB Cloud Serverless cluster. It brings the following benefits:

- Convenience: the export service provides a simple and easy-to-use way to export data from a TiDB Cloud Serverless cluster, eliminating the need for additional tools or resources.
- Isolation: the export service uses separate computing resources, ensuring isolation from the resources used by your online services.
- Consistency: the export service ensures the consistency of the exported data without causing locks, which does not affect your online services.

## Features

This section describes the features of TiDB Serverless Export.

### Export location

You can export data to local storage or [Amazon S3](https://aws.amazon.com/s3/).

> **Note:**
>
> If the size of the data to be exported is large (more than 100 GiB), it is recommended that you export it to Amazon S3.

**Local storage**

To export data from a TiDB Cloud Serverless cluster to a local file, you need to export data [using the TiDB Cloud console](#export-data-to-a-local-file) or [using the TiDB Cloud CLI](/tidb-cloud/ticloud-serverless-export-create.md), and then download the exported data using the TiDB Cloud CLI.

- Exporting multiple databases to local storage at the same time is not supported.
- Exported data is saved in the stashing area and will expire after two days. You need to download the exported data in time.
- If the storage space of stashing area is full, you will not be able to export data to local storage.

**Amazon S3**

### Amazon S3

To export data to Amazon S3, you need to provide the following information:

- URI: `s3://<bucket-name>/<file-path>`
- One of the following access credentials:
    - [An access key](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html): make sure the access key has the `s3:PutObject` and `s3:ListBucket` permissions.
    - [A role ARN](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html): make sure the role ARN has the `s3:PutObject` and `s3:ListBucket` permissions. 

For more information, see [Configure External Storage Access for TiDB Cloud Serverless](/tidb-cloud/serverless-external-storage.md#configure-amazon-s3-access).

## Export options

### Data filtering

You can filter data by specifying the database and table you want to export. If you specify a database without specifying a table, all tables in that specified database will be exported. If you do not specify a database when you export data to Amazon S3, all databases in the cluster will be exported.

> **Note:**
>
> You must specify the database when you export data to local storage.

### Data formats

You can export data in the following formats:

- `SQL` (default): export data in SQL format.
- `CSV`: export data in CSV format.

The schema and data are exported according to the following naming conventions:

| Item            | Not compressed                           | Compressed                                          |
|-----------------|------------------------------------------|-----------------------------------------------------|
| Database schema | {database}-schema-create.sql             | {database}-schema-create.sql.{compression-type}             |
| Table schema    | {database}.{table}-schema.sql            | {database}.{table}-schema.sql.{compression-type}            |
| Data            | {database}.{table}.{0001}.{sql&#124;csv} | {database}.{table}.{0001}.{sql&#124;csv}.{compression-type} |

### Data compression

You can compress the exported data using the following algorithms:

- `gzip` (default): compress the exported data with gzip.
- `snappy`: compress the exported data with snappy.
- `zstd`: compress the exported data with zstd.
- `none`: do not compress the exported data.

### Cancel export

You can cancel an export task that is in the running state.

## Examples

Currently, you can manage export tasks using [TiDB Cloud CLI](/tidb-cloud/cli-reference.md).

### Export data to local storage

1. Create an export task that specifies the database and table you want to export:

   ```shell
   ticloud serverless export create -c <cluster-id> --database <database> --table <table>
   ```

    You will get an export ID from the output.

2. After the export is successful, download the exported data to your local storage:

   ```shell
   ticloud serverless export download -c <cluster-id> -e <export-id>
   ```

### Export data to Amazon S3

<SimpleTab>
<div label="Console">

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.

   > **Tip:**
   >
   > If you have multiple projects, you can click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner and switch to another project.

2. Click the name of your target cluster to go to its overview page, and then click **Import** in the left navigation pane.

3. On the **Import** page, click **Export Data to** in the upper-right corner, then choose **Amazon S3** from the drop-down list. Fill in the following parameters:

    - **Task Name**: enter a name for the export task. The default value is `SNAPSHOT_{snapshot_time}`.
    - **Exported Data**: choose the databases and tables you want to export.
    - **Data Format**: choose **SQL File** or **CSV**.
    - **Compression**: choose **Gzip**, **Snappy**, **Zstd**, or **None**.
    - **Folder URI**: enter the URI of the Amazon S3 with the `s3://<bucket-name>/<folder-path>/` format.
    - **Bucket Access**: choose one of the following access credentials and then fill in the credential information. If you do not have such information, see [Configure External Storage Access for TiDB Cloud Serverless](/tidb-cloud/serverless-external-storage.md#configure-amazon-s3-access).
        - **AWS Role ARN**: enter the role ARN that has the `s3:PutObject` and `s3:ListBucket` permissions to access the bucket.
        - **AWS Access Key**: enter the access key ID and access key secret that have the `s3:PutObject` and `s3:ListBucket` permissions to access the bucket.

4. Click **Export**.

</div>

<div label="CLI">

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

### Cancel an export task

```shell
ticloud serverless export cancel -c <cluster-id> -e <export-id>
```

## Pricing

The export service is free during the beta period. You only need to pay for the [Request Units (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit) generated during the export process of successful or canceled tasks. For failed export tasks, you will not be charged.