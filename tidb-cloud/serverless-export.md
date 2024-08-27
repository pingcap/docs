---
title: Export Data from TiDB Serverless
summary: Learn how to export data from TiDB Serverless clusters.
---

# Export Data from TiDB Serverless

TiDB Serverless Export (Beta) is a service that enables you to export data from a TiDB Serverless cluster to local file or an external storage service. You can use the exported data for backup, migration, data analysis, or other purposes.

While you can also export data using tools such as [mysqldump](https://dev.mysql.com/doc/refman/8.0/en/mysqldump.html) and TiDB [Dumpling](https://docs.pingcap.com/tidb/dev/dumpling-overview), TiDB Serverless Export offers a more convenient and efficient way to export data from a TiDB Serverless cluster. It brings the following benefits:

- Convenience: the export service provides a simple and easy-to-use way to export data from a TiDB Serverless cluster, eliminating the need for additional tools or resources.
- Isolation: the export service uses separate computing resources, ensuring isolation from the resources used by your online services.
- Consistency: the export service ensures the consistency of the exported data without causing locks, which does not affect your online services.

## Export location

You can export data to:

- Local file 
- External storage
    - [Amazon S3](https://aws.amazon.com/s3/)
    - [Google Cloud Storage](https://cloud.google.com/storage)
    - [Azure Blob Storage](https://azure.microsoft.com/en-us/services/storage/blobs/)

> **Note:**
>
> If the size of the data to be exported is large (more than 100 GiB), it is recommended that you export it to external storage.

### Local file

Exporting data to a local file has the following limitations:

- You can only download the exported data with the [TiDB Cloud CLI](/tidb-cloud/cli-reference.md). Downloading on the TiDB Cloud console is not supported.
- Exported data is saved in the stashing area and will expire after two days. You need to download the exported data in time.
- If the storage space of stashing area is full, you will not be able to export data to the local file.

### Amazon S3

To export data to Amazon S3, you need to provide the following information:

- uri: `s3://<bucket-name>/<file-path>`
- one of the following access methods:
    - [An access key](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html): make sure the access key has the `s3:PutObject` and `s3:ListBucket` permissions.
    - [A role ARN](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html): make sure the role ARN has the `s3:PutObject` and `s3:ListBucket` permissions. 

See [Configure External Storage Access for TiDB Serverless](/tidb-cloud/serverless-external-storage.md#configure-amazon-s3-access) to learn how to configure the Amazon S3 access.

### Google Cloud Storage

To export data to Google Cloud Storage, you need to provide the following information:

- uri: `gs://<bucket-name>/<file-path>`
- access method: a **base64 encoded** [service account key](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) for your bucket. Make sure the service account key has the `storage.objects.create` permission.

See [Configure External Storage Access for TiDB Serverless](/tidb-cloud/serverless-external-storage.md#configure-gcs-access) to learn how to configure the Google Cloud Storage access.

> **Note:**
>
> You can only export to Google Cloud Storage with TiDB Cloud CLI now.

### Azure Blob Storage

To export data to Azure Blob Storage, you need to provide the following information:

- uri: `azure://<account-name>.blob.core.windows.net/<container-name>/<file-path>`
- access method: a [shared access signature (SAS) token](https://docs.microsoft.com/en-us/azure/storage/common/storage-sas-overview) for your Azure Blob Storage container. Make sure the SAS token has the `Read` and `Write` permissions on the `Container` and `Object` resources.

See [Configure External Storage Access for TiDB Serverless](/tidb-cloud/serverless-external-storage.md#configure-azure-blob-access) to learn how to configure the Azure Blob Storage access.       

> **Note:**
>
> You can only export to Azure Blob Storage with TiDB Cloud CLI now.

## Export options

### Data filtering

- TiDB Cloud console supports exporting data with the selected databases and tables.
- TiDB Cloud CLI supports exporting data with sql statements and [table filter](https://docs.pingcap.com/tidb/stable/table-filter).

### Data formats

You can export data in the following formats:

- `SQL`: export data in SQL format.
- `CSV`: export data in CSV format, you can specify the following options:
    - `delimiter`: specify the delimiter used in the exported data. The default delimiter is `"`.
    - `separator`: specify the character used to separate fields in the exported data. The default separator is `,`.
    - `header`: specify whether to include a header row in the exported data. The default value is `true`.
    - `null-value`: specify the string that represents a NULL value in the exported data. The default value is `\N`.
- `Parquet`: export data in Parquet format. It is only supported in TiDB Cloud CLI now.

The schema and data are exported according to the following naming conventions:

| Item            | Not compressed                                        | Compressed                                                                                                           |
|-----------------|-------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------|
| Database schema | {database}-schema-create.sql                          | {database}-schema-create.sql.{compression-type}                                                                      |
| Table schema    | {database}.{table}-schema.sql                         | {database}.{table}-schema.sql.{compression-type}                                                                     |
| Data            | {database}.{table}.{0001}.{csv&#124;parquet&#124;sql} | {database}.{table}.{0001}.{csv&#124;sql}.{compression-type}<br/>{database}.{table}.{0001}.{compression-type}.parquet |

### Data compression

You can compress the exported CSV and SQL data using the following algorithms:

- `gzip` (default): compress the exported data with gzip.
- `snappy`: compress the exported data with snappy.
- `zstd`: compress the exported data with zstd.
- `none`: do not compress the exported data.

You can compress the exported Parquet data using the following algorithms:

- `zstd `(default): compress the Parquet file with zstd.
- `gzip`: compress the Parquet file with gzip.
- `snappy`: compress the Parquet file with snappy.
- `none`: do not compress the Parquet file.

## Examples

### Export data to a local file

<SimpleTab>
<div label="Console">

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project. 

   > **Tip:**
   >
   > If you have multiple projects, you can click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner and switch to another project.

2. Click the name of your target cluster to go to its overview page, and then click **Import & Export** in the left navigation pane.

3. On the **Import & Export** page, click **Export Data to** in the upper-right corner, then choose **Local File** from the drop-down list. Fill in the following parameters:

    - **Task Name**: enter a name for the export task. The default is `SNAPSHOT_{snapshot_time}`.
    - **Exported data**: choose the databases and tables you want to export.
    - **Data format**: choose **SQL File** or **CSV**.
    - **Compression**: choose **Gzip**, **Snappy**, **Zstd**, or **None**.

4. Click **Export**.

5. After the export task is successful, you can download the exported data to your local file with TiDB Cloud CLI.

</div>

<div label="CLI">

1. Create an export task. TiDB Cloud CLI will export the data to local file by default:

    ```shell
    ticloud serverless export create -c <cluster-id> --filter "database.table"
    ```

    You will get an export ID from the output.

2. After the export task is successful, download the exported data to your local file:

    ```shell
    ticloud serverless export download -c <cluster-id> -e <export-id>
    ```

</div>
</SimpleTab>

### Export data to Amazon S3

<SimpleTab>
<div label="Console">

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.

       > **Tip:**
       >
       > If you have multiple projects, you can click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner and switch to another project.

2. Click the name of your target cluster to go to its overview page, and then click **Import & Export** in the left navigation pane.

3. Configure the export information. On the **Import & Export** page, click **Export Data to** in the upper-right corner, then choose **Amazon S3** from the drop-down list. Fill in the following parameters:

    - **Task Name**: enter a name for the export task. The default value is `SNAPSHOT_{snapshot_time}`.
    - **Exported data**: choose the databases and tables you want to export.
    - **Data format**: choose **SQL File** or **CSV**.
    - **Compression**: choose **Gzip**, **Snappy**, **Zstd**, or **None**.
    - **File URI**: enter the URI of the Amazon S3 with the `s3://<bucket-name>/<file-path>` format.
    - **Bucket Access**
        - **AWS Role ARN**: enter the role ARN that has the permission to access the bucket.
        - **AWS Access Key ID**: enter the access key ID and access key secret that have the permission to access the bucket.

4. Click **Export**.

5. After the export task is successful, you can download the exported data to your local file with TiDB Cloud CLI.

</div>

<div label="CLI">

```shell
ticloud serverless export create -c <cluster-id> --s3.uri <uri> --s3.access-key-id <access-key-id> --s3.secret-access-key <secret-access-key> --filter "database.table"
```

- s3.uri: the Amazon S3 URI with the `s3://<bucket-name>/<file-path>` format.
- s3.access-key-id: the access key ID of the user who has the permission to access the bucket.
- s3.secret-access-key: the access key secret of the user who has the permission to access the bucket.

```shell
ticloud serverless export create -c <cluster-id> --s3.uri <uri> --s3.role-arn <role-arn> --filter "database.table"
```

- s3.uri: the URI of the Amazon S3 bucket with the `s3://<bucket-name>/<file-path>` format.
- s3.role-arn: the ARN of the role that has the permission to access the bucket.

</div>
</SimpleTab>

### Export data to Google Cloud Storage

You can only export data to Google Cloud Storage using the TiDB Cloud CLI now.

```shell
ticloud serverless export create -c <cluster-id> --gcs.uri <uri> --gcs.service-account-key <service-account-key> --filter "database.table"
```

- gcs.uri: the URI of the Google Cloud Storage bucket with the `gs://<bucket-name>/<file-path>` format.
- gcs.service-account-key: the base64 encoded service account key.

### Export data to Azure Blob Storage

You can only export data to Azure Blob Storage using the TiDB Cloud CLI now.

```shell
ticloud serverless export create -c <cluster-id> --azblob.uri <uri> --azblob.sas-token <sas-token> --filter "database.table"
```

- azblob.uri: the URI of the Azure Blob Storage with the `azure://<account-name>.blob.core.windows.net/<container-name>/<file-path>` format.
- azblob.sas-token: the account SAS token of the Azure Blob Storage.

### Cancel an export task

<SimpleTab>
<div label="Console">

1. Open the **Import & Export** page for your target cluster, log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.

   > **Tip:**
   >
   > If you have multiple projects, you can click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner and switch to another project.

2. Click the name of your target cluster to go to its overview page, and then click **Import & Export** in the left navigation pane.

3. On the **Import & Export** page, click **Export** to view the export task list.

4. Choose the export task you want to cancel, and then click **Action** button.

5. Choose **Cancel** in the drop-down list. Note that you can only cancel the export task that is in the **Running** status.

</div>

<div label="CLI">

```shell
ticloud serverless export cancel -c <cluster-id> -e <export-id>
```

</div>
</SimpleTab>

## Pricing

The export service is free during the beta period. You only need to pay for the [Request Units (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit) generated during the export process of successful or canceled tasks. For failed export tasks, you will not be charged.
