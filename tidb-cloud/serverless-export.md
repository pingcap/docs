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

> **Note:**
>
> The maximum export size is currently 1 TiB. To export more data or request a higher export speed, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

## Export locations

You can export data to the following locations:

- A local file
- An external storage, including:

    - [Amazon S3](https://aws.amazon.com/s3/)
    - [Google Cloud Storage](https://cloud.google.com/storage)
    - [Azure Blob Storage](https://azure.microsoft.com/en-us/services/storage/blobs/)
    - [Alibaba Cloud Object Storage Service (OSS)](https://www.alibabacloud.com/product/oss)

> **Note:**
>
> If the size of the data to be exported is large (more than 100 GiB), it is recommended that you export it to an external storage.

### A local file

To export data from a TiDB Cloud Serverless cluster to a local file, you need to export data [using the TiDB Cloud console](#export-data-to-a-local-file) or [using the TiDB Cloud CLI](/tidb-cloud/ticloud-serverless-export-create.md), and then download the exported data using the TiDB Cloud CLI.

Exporting data to a local file has the following limitations:

- Downloading exported data using the TiDB Cloud console is not supported.
- Exported data is saved in the stashing area of TiDB Cloud and will expire after two days. You need to download the exported data in time.
- If the storage space of stashing area is full, you will not be able to export data to the local file.

### Amazon S3

To export data to Amazon S3, you need to provide the following information:

- URI: `s3://<bucket-name>/<folder-path>/`
- One of the following access credentials:
    - [An access key](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html): make sure the access key has the `s3:PutObject` and `s3:ListBucket` permissions.
    - [A role ARN](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html): make sure the role ARN (Amazon Resource Name) has the `s3:PutObject` and `s3:ListBucket` permissions. Note that only clusters hosted on AWS support the role ARN.

For more information, see [Configure Amazon S3 access](/tidb-cloud/serverless-external-storage.md#configure-amazon-s3-access).

### Google Cloud Storage

To export data to Google Cloud Storage, you need to provide the following information:

- URI: `gs://<bucket-name>/<folder-path>/`
- Access credential: a **base64 encoded** [service account key](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) for your bucket. Make sure the service account key has the `storage.objects.create` permission.

For more information, see [Configure GCS access](/tidb-cloud/serverless-external-storage.md#configure-gcs-access).

### Azure Blob Storage

To export data to Azure Blob Storage, you need to provide the following information:

- URI: `azure://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/` or `https://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/`
- Access credential: a [shared access signature (SAS) token](https://docs.microsoft.com/en-us/azure/storage/common/storage-sas-overview) for your Azure Blob Storage container. Make sure the SAS token has the `Read` and `Write` permissions on the `Container` and `Object` resources.

For more information, see [Configure Azure Blob Storage access](/tidb-cloud/serverless-external-storage.md#configure-azure-blob-storage-access).

### Alibaba Cloud OSS

To export data to Alibaba Cloud OSS, you need to provide the following information:

- URI: `oss://<bucket-name>/<folder-path>/`
- Access credential: An [AccessKey pair](https://www.alibabacloud.com/help/en/ram/user-guide/create-an-accesskey-pair) for your Alibaba Cloud account. Make sure the AccessKey pair has the `oss:PutObject`, `oss:ListBuckets` and `oss:GetBucketInfo` permissions to allow data export to the OSS bucket.

For more information, see [Configure Alibaba Cloud Object Storage Service (OSS) access](/tidb-cloud/serverless-external-storage.md#configure-alibaba-cloud-object-storage-service-oss-access).

## Export options

### Data filtering

- TiDB Cloud console supports exporting data with the selected databases and tables.
- TiDB Cloud CLI supports exporting data with SQL statements and [table filters](/table-filter.md).

### Data formats

You can export data in the following formats:

- `SQL`: export data in SQL format.
- `CSV`: export data in CSV format. You can specify the following options:
    - `delimiter`: specify the delimiter used in the exported data. The default delimiter is `"`.
    - `separator`: specify the character used to separate fields in the exported data. The default separator is `,`.
    - `header`: specify whether to include a header row in the exported data. The default value is `true`.
    - `null-value`: specify the string that represents a NULL value in the exported data. The default value is `\N`.
- `Parquet`: export data in Parquet format.

The schema and data are exported according to the following naming conventions:

| Item            | Not compressed                                        | Compressed                                                                                                          |
|-----------------|-------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|
| Database schema | {database}-schema-create.sql                          | {database}-schema-create.sql.{compression-type}                                                                     |
| Table schema    | {database}.{table}-schema.sql                         | {database}.{table}-schema.sql.{compression-type}                                                                    |
| Data            | {database}.{table}.{0001}.{csv&#124;parquet&#124;sql} | {database}.{table}.{0001}.{csv&#124;sql}.{compression-type}<br/>{database}.{table}.{0001}.{compression-type}.parquet |

### Data compression

You can compress the exported CSV and SQL data using the following algorithms:

- `gzip` (default): compress the exported data with `gzip`.
- `snappy`: compress the exported data with `snappy`.
- `zstd`: compress the exported data with `zstd`.
- `none`: do not compress the exported `data`.

You can compress the exported Parquet data using the following algorithms:

- `zstd` (default): compress the Parquet file with `zstd`.
- `gzip`: compress the Parquet file with `gzip`.
- `snappy`: compress the Parquet file with `snappy`.
- `none`: do not compress the Parquet file.

### Data conversion

When exporting data to the Parquet format, the data conversion between TiDB Cloud Serverless and Parquet is as follows:

| TiDB Cloud Serverless Type | Parquest primitive type | Parquet logical type                         |
|----------------------------|-------------------------|----------------------------------------------|
| VARCHAR                    | BYTE_ARRAY              | String(UTF8)                                 |
| TIME                       | BYTE_ARRAY              | String(UTF8)                                 |
| TINYTEXT                   | BYTE_ARRAY              | String(UTF8)                                 |
| MEDIUMTEXT                 | BYTE_ARRAY              | String(UTF8)                                 |
| TEXT                       | BYTE_ARRAY              | String(UTF8)                                 |
| LONGTEXT                   | BYTE_ARRAY              | String(UTF8)                                 |
| SET                        | BYTE_ARRAY              | String(UTF8)                                 |
| JSON                       | BYTE_ARRAY              | String(UTF8)                                 |
| DATE                       | BYTE_ARRAY              | String(UTF8)                                 |
| CHAR                       | BYTE_ARRAY              | String(UTF8)                                 |
| VECTOR                     | BYTE_ARRAY              | String(UTF8)                                 |
| DECIMAL(1<=p<=9)           | INT32                   | DECIMAL(p,s)                                 |
| DECIMAL(10<=p<=18)         | INT64                   | DECIMAL(p,s)                                 |
| DECIMAL(p>=19)             | BYTE_ARRAY              | String(UTF8)                                 |
| ENUM                       | BYTE_ARRAY              | String(UTF8)                                 |
| TIMESTAMP                  | INT64                   | TIMESTAMP(unit=MICROS,isAdjustedToUTC=false) |
| DATETIME                   | INT64                   | TIMESTAMP(unit=MICROS,isAdjustedToUTC=false) |
| YEAR                       | INT32                   | /                                            |
| TINYINT                    | INT32                   | /                                            |
| UNSIGNED TINYINT           | INT32                   | /                                            |
| SMALLINT                   | INT32                   | /                                            |
| UNSIGNED SMALLINT          | INT32                   | /                                            |
| MEDIUMINT                  | INT32                   | /                                            |
| UNSIGNED MEDIUMINT         | INT32                   | /                                            |
| INT                        | INT32                   | /                                            |
| UNSIGNED INT               | FIXED_LEN_BYTE_ARRAY(9) | DECIMAL(20,0)                                |
| BIGINT                     | FIXED_LEN_BYTE_ARRAY(9) | DECIMAL(20,0)                                |
| UNSIGNED BIGINT            | BYTE_ARRAY              | String(UTF8)                                 |
| FLOAT                      | FLOAT                   | /                                            |
| DOUBLE                     | DOUBLE                  | /                                            |
| BLOB                       | BYTE_ARRAY              | /                                            |
| TINYBLOB                   | BYTE_ARRAY              | /                                            |
| MEDIUMBLOB                 | BYTE_ARRAY              | /                                            |
| LONGBLOB                   | BYTE_ARRAY              | /                                            |
| BINARY                     | BYTE_ARRAY              | /                                            |
| VARBINARY                  | BYTE_ARRAY              | /                                            |
| BIT                        | BYTE_ARRAY              | /                                            |

## Examples

### Export data to a local file

<SimpleTab>
<div label="Console">

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

   > **Tip:**
   >
   > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. Click the name of your target cluster to go to its overview page, and then click **Data** > **Import** in the left navigation pane.

3. On the **Import** page, click **Export Data to** in the upper-right corner, then choose **Local File** from the drop-down list. Fill in the following parameters:

    - **Task Name**: enter a name for the export task. The default value is `SNAPSHOT_{snapshot_time}`.
    - **Exported Data**: choose the databases and tables you want to export.
    - **Data Format**: choose **SQL**, **CSV**, or **Parquet**.
    - **Compression**: choose **Gzip**, **Snappy**, **Zstd**, or **None**.

   > **Tip:**
   >
   > If your cluster has neither imported nor exported any data before, you need to click **Click here to export data to...** at the bottom of the page to export data.

4. Click **Export**.

5. After the export task is successful, you can copy the download command displayed in the export task detail, and then download the exported data by running the command in the [TiDB Cloud CLI](/tidb-cloud/cli-reference.md).

</div>

<div label="CLI">

1. Create an export task:

    ```shell
    ticloud serverless export create -c <cluster-id>
    ```

    You will get an export ID from the output.

2. After the export task is successful, download the exported data to your local file:

    ```shell
    ticloud serverless export download -c <cluster-id> -e <export-id>
    ```

    For more information about the download command, see [ticloud serverless export download](/tidb-cloud/ticloud-serverless-export-download.md).
 
</div>
</SimpleTab>

### Export data to Amazon S3

<SimpleTab>
<div label="Console">

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

   > **Tip:**
   >
   > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. Click the name of your target cluster to go to its overview page, and then click **Data** > **Import** in the left navigation pane.

3. On the **Import** page, click **Export Data to** in the upper-right corner, then choose **Amazon S3** from the drop-down list. Fill in the following parameters:

    - **Task Name**: enter a name for the export task. The default value is `SNAPSHOT_{snapshot_time}`.
    - **Exported Data**: choose the databases and tables you want to export.
    - **Data Format**: choose **SQL**, **CSV**, or **Parquet**.
    - **Compression**: choose **Gzip**, **Snappy**, **Zstd**, or **None**.
    - **Folder URI**: enter the URI of the Amazon S3 with the `s3://<bucket-name>/<folder-path>/` format.
    - **Bucket Access**: choose one of the following access credentials and then fill in the credential information:
        - **AWS Role ARN**: enter the role ARN that has the permission to access the bucket. It is recommended to create the role ARN with AWS CloudFormation. For more information, see [Configure External Storage Access for TiDB Cloud Serverless](/tidb-cloud/serverless-external-storage.md#configure-amazon-s3-access).
        - **AWS Access Key**: enter the access key ID and access key secret that have the permission to access the bucket.

4. Click **Export**.

</div>

<div label="CLI">

```shell
ticloud serverless export create -c <cluster-id> --target-type S3 --s3.uri <uri> --s3.access-key-id <access-key-id> --s3.secret-access-key <secret-access-key> --filter "database.table"

ticloud serverless export create -c <cluster-id> --target-type S3 --s3.uri <uri> --s3.role-arn <role-arn> --filter "database.table"
```

- `s3.uri`: the Amazon S3 URI with the `s3://<bucket-name>/<folder-path>/` format.
- `s3.access-key-id`: the access key ID of the user who has the permission to access the bucket.
- `s3.secret-access-key`: the access key secret of the user who has the permission to access the bucket.
- `s3.role-arn`: the role ARN that has the permission to access the bucket.

</div>
</SimpleTab>

### Export data to Google Cloud Storage

<SimpleTab>
<div label="Console">

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

   > **Tip:**
   >
   > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. Click the name of your target cluster to go to its overview page, and then click **Data** > **Import** in the left navigation pane.

3. On the **Import** page, click **Export Data to** in the upper-right corner, and then choose **Google Cloud Storage** from the drop-down list. Fill in the following parameters:

    - **Task Name**: enter a name for the export task. The default value is `SNAPSHOT_{snapshot_time}`.
    - **Exported Data**: choose the databases and tables you want to export.
    - **Data Format**: choose **SQL**, **CSV**, or **Parquet**.
    - **Compression**: choose **Gzip**, **Snappy**, **Zstd**, or **None**.
    - **Folder URI**: enter the URI of the Google Cloud Storage with the `gs://<bucket-name>/<folder-path>/` format.
    - **Bucket Access**: upload the Google Cloud credentials file that has permission to access the bucket.

4. Click **Export**.

</div>

<div label="CLI">

```shell
ticloud serverless export create -c <cluster-id> --target-type GCS --gcs.uri <uri> --gcs.service-account-key <service-account-key> --filter "database.table"
```

- `gcs.uri`: the URI of the Google Cloud Storage bucket in the `gs://<bucket-name>/<folder-path>/` format.
- `gcs.service-account-key`: the base64 encoded service account key.

</div>
</SimpleTab>

### Export data to Azure Blob Storage

<SimpleTab>
<div label="Console">

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

   > **Tip:**
   >
   > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. Click the name of your target cluster to go to its overview page, and then click **Data** > **Import** in the left navigation pane.

3. On the **Import** page, click **Export Data to** in the upper-right corner, and then choose **Azure Blob Storage** from the drop-down list. Fill in the following parameters:

    - **Task Name**: enter a name for the export task. The default value is `SNAPSHOT_{snapshot_time}`.
    - **Exported Data**: choose the databases and tables you want to export.
    - **Data Format**: choose **SQL**, **CSV**, or **Parquet**.
    - **Compression**: choose **Gzip**, **Snappy**, **Zstd**, or **None**.
    - **Folder URI**: enter the URI of Azure Blob Storage with the `azure://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/` format.
    - **SAS Token**: enter the SAS token that has the permission to access the container. It is recommended to create a SAS token with the [Azure ARM template](https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/). For more information, see [Configure External Storage Access for TiDB Cloud Serverless](/tidb-cloud/serverless-external-storage.md#configure-azure-blob-storage-access).

4. Click **Export**.

</div>

<div label="CLI">

```shell
ticloud serverless export create -c <cluster-id> --target-type AZURE_BLOB --azblob.uri <uri> --azblob.sas-token <sas-token> --filter "database.table"
```

- `azblob.uri`: the URI of the Azure Blob Storage in the `(azure|https)://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/` format.
- `azblob.sas-token`: the account SAS token of the Azure Blob Storage.

</div>
</SimpleTab>

### Export data to Alibaba Cloud OSS

<SimpleTab>
<div label="Console">

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

   > **Tip:**
   >
   > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. Click the name of your target cluster to go to its overview page, and then click **Data** > **Import** in the left navigation pane.

3. On the **Import** page, click **Export Data to** in the upper-right corner, and then choose **Alibaba Cloud OSS** from the drop-down list. 

4. Fill in the following parameters:

    - **Task Name**: enter a name for the export task. The default value is `SNAPSHOT_{snapshot_time}`.
    - **Exported Data**: choose the databases and tables you want to export.
    - **Data Format**: choose **SQL**, **CSV**, or **Parquet**.
    - **Compression**: choose **Gzip**, **Snappy**, **Zstd**, or **None**.
    - **Folder URI**: enter the Alibaba Cloud OSS URI where you want to export the data, in the `oss://<bucket-name>/<folder-path>/` format.
    - **AccessKey ID** and **AccessKey Secret**: enter the AccessKey ID and AccessKey Secret that have the permission to access the bucket.

5. Click **Export**.

</div>

<div label="CLI">

```shell
ticloud serverless export create -c <cluster-id> --target-type OSS --oss.uri <uri> --oss.access-key-id <access-key-id> --oss.access-key-secret <access-key-secret> --filter "database.table"
```

- `oss.uri`: the Alibaba Cloud OSS URI where you want to export the data, in the `oss://<bucket-name>/<folder-path>/` format.
- `oss.access-key-id`: the AccessKey ID of the user who has the permission to access the bucket.
- `oss.access-key-secret`: the AccessKey secret of the user who has the permission to access the bucket.

</div>
</SimpleTab>

### Cancel an export task

To cancel an ongoing export task, take the following steps:

<SimpleTab>
<div label="Console">

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

   > **Tip:**
   >
   > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. Click the name of your target cluster to go to its overview page, and then click **Data** > **Import** in the left navigation pane.

3. On the **Import** page, click **Export** to view the export task list.

4. Choose the export task you want to cancel, and then click **Action**.

5. Choose **Cancel** in the drop-down list. Note that you can only cancel the export task that is in the **Running** status.

</div>

<div label="CLI">

```shell
ticloud serverless export cancel -c <cluster-id> -e <export-id>
```

</div>
</SimpleTab>

## Export speed

The export speed depends on your [cluster plan](/tidb-cloud/select-cluster-tier.md#cluster-plans). For details, see the following table:

| Plan               | Export speed       |
|:-------------------|:-------------------|
| Free cluster plan      | Up to 25 MiB/s      |
| Scalable cluster plan  | Up to 100 MiB/s     |

## Pricing

The export service is free during the beta period. You only need to pay for the [Request Units (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit) generated during the export process of successful or canceled tasks. For failed export tasks, you will not be charged.
