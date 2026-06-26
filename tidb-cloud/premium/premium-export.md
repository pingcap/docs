---
title: Export Data from {{{ .premium }}}
summary: Learn how to export data from {{{ .premium }}} instances.
---

# Export Data from {{{ .premium }}}

TiDB Cloud enables you to export data from a {{{ .premium }}} instance to an external storage service. You can use the exported data for backup, migration, data analysis, or other purposes.

While you can also export data using tools such as [mysqldump](https://dev.mysql.com/doc/refman/8.0/en/mysqldump.html) and TiDB [Dumpling](https://docs.pingcap.com/tidb/dev/dumpling-overview), the export feature provided by TiDB Cloud offers a more convenient and efficient way to export data from a {{{ .premium }}} instance. It brings the following benefits:

- Convenience: the export service provides a simple and easy-to-use way to export data from a {{{ .premium }}} instance, eliminating the need for additional tools or resources.
- Isolation: the export service uses separate computing resources, ensuring isolation from the resources used by your online services.
- Consistency: the export service ensures the consistency of the exported data without causing locks, which does not affect your online services.

> **Note:**
>
> - Currently, this feature is only available upon request. To request this feature, click **?** in the lower-right corner of the [TiDB Cloud console](https://tidbcloud.com), and then click **Support Tickets** to go to the [Help Center](https://tidb.support.pingcap.com/servicedesk/customer/portals). Create a ticket, fill in "Apply for data export for {{{ .premium }}} instance" in the **Description** field, and then click **Submit**.
> - The maximum export size is 1 TiB. Exports larger than this limit might fail. To export more data or request a higher export speed, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

## Export locations

You can export data to the following external storage locations:

- [Amazon S3](https://aws.amazon.com/s3/)
- [Azure Blob Storage](https://azure.microsoft.com/en-us/services/storage/blobs/)
- [Alibaba Cloud Object Storage Service (OSS)](https://www.alibabacloud.com/product/oss)

### Amazon S3

To export data to Amazon S3, you need to provide the following information:

- URI: `s3://<bucket-name>/<folder-path>/`
- One of the following access credentials:
    - [An access key](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html): make sure the access key has the `s3:PutObject` permission.
    - [A role ARN](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html): make sure the role ARN (Amazon Resource Name) has the `s3:PutObject` permission. Note that only {{{ .premium }}} instances hosted on AWS support the role ARN.

For more information, see [Configure External Storage Access](/tidb-cloud/configure-external-storage-access.md#configure-amazon-s3-access).

### Azure Blob Storage

To export data to Azure Blob Storage, you need to provide the following information:

- URI: `azure://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/` or `https://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/`
- Access credential: a [shared access signature (SAS) token](https://docs.microsoft.com/en-us/azure/storage/common/storage-sas-overview) for your Azure Blob Storage container. Make sure the SAS token has the `Read` and `Write` permissions on the `Container` and `Object` resources.

For more information, see [Configure External Storage Access](/tidb-cloud/configure-external-storage-access.md#configure-azure-blob-storage-access).

### Alibaba Cloud OSS

To export data to Alibaba Cloud OSS, you need to provide the following information:

- URI: `oss://<bucket-name>/<folder-path>/`
- Access credential: an [AccessKey pair](https://www.alibabacloud.com/help/en/ram/user-guide/create-an-accesskey-pair) for your Alibaba Cloud account. Make sure the AccessKey pair has the `oss:PutObject` and `oss:GetBucketInfo` permissions.

For more information, see [Configure External Storage Access](/tidb-cloud/configure-external-storage-access.md#configure-alibaba-cloud-object-storage-service-oss-access).

## Export options

### Data filtering

TiDB Cloud console supports exporting data with the selected databases and tables.

### Data formats

You can export data in the following formats:

- `SQL`: export data in SQL format.
- `CSV`: export data in CSV format. You can specify the following options:
    - `delimiter`: specify the delimiter used in the exported data. The default delimiter is `"`.
    - `separator`: specify the character used to separate fields in the exported data. The default separator is `,`.
    - `header`: specify whether to include a header row in the exported data. The default value is `true`.
    - `null-value`: specify the string that represents a NULL value in the exported data. The default value is `\N`.

The schema and data are exported according to the following naming conventions:

| Item            | Not compressed                | Compressed                                                   |
|-----------------|-------------------------------|--------------------------------------------------------------|
| Database schema | {database}-schema-create.sql  | {database}-schema-create.sql.{compression-type}              |
| Table schema    | {database}.{table}-schema.sql | {database}.{table}-schema.sql.{compression-type}             |
| Data            | {database}.{table}.{0001}.csv | {database}.{table}.{0001}.csv.{compression-type}             |
| Data            | {database}.{table}.{0001}.sql | {database}.{table}.{0001}.sql.{compression-type}             |

### Data compression

You can compress the exported CSV and SQL data using the following algorithms:

- `gzip` (default): compress the exported data with `gzip`.
- `snappy`: compress the exported data with `snappy`.
- `zstd`: compress the exported data with `zstd`.
- `none`: do not compress the exported data.

## Examples

### Export data to Amazon S3

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**TiDB Instances**](https://tidbcloud.com/tidbs) page.

   > **Tip:**
   >
   > If you are in multiple organizations, use the combo box in the upper-left corner to switch to your target organization first.

2. Click the name of your target {{{ .premium }}} instance to go to its overview page, and then click **Data** > **Export** in the left navigation pane.

3. On the **Export** page, click **Export Data** in the upper-right corner. Then configure the following settings:

    - **Task Name**: enter a name for the export task. The default value is `SNAPSHOT_{snapshot_time}`.
    - **Source Connection**: enter **Username** and **Password** of your {{{ .premium }}} instance, and then click **Test Connection** to verify the credentials.
    - **Target Connection**:
        - **Storage Provider**: choose Amazon S3.
        - **Folder URI**: enter the URI of the Amazon S3 with the `s3://<bucket-name>/<folder-path>/` format.
        - **Bucket Access**: choose one of the following access credentials and then fill in the credential information:
            - **AWS Role ARN**: enter the role ARN that has the permission to access the bucket. It is recommended to create the role ARN with AWS CloudFormation. For more information, see [Configure External Storage Access](/tidb-cloud/configure-external-storage-access.md#configure-amazon-s3-access).
            - **AWS Access Key**: enter the access key ID and access key secret that have the permission to access the bucket.
    - **Exported Data**: choose the databases or tables you want to export.
    - **Data Format**: choose **SQL** or **CSV**.
    - **Compression**: choose **Gzip**, **Snappy**, **Zstd**, or **None**.

4. Click **Export**.

### Export data to Azure Blob Storage

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**TiDB Instances**](https://tidbcloud.com/tidbs) page.

   > **Tip:**
   >
   > If you are in multiple organizations, use the combo box in the upper-left corner to switch to your target organization first.

2. Click the name of your target {{{ .premium }}} instance to go to its overview page, and then click **Data** > **Export** in the left navigation pane.

3. On the **Export** page, click **Export Data** in the upper-right corner. Then configure the following settings:

    - **Task Name**: enter a name for the export task. The default value is `SNAPSHOT_{snapshot_time}`.
    - **Source Connection**: enter **Username** and **Password** of your {{{ .premium }}} instance, and then click **Test Connection** to verify the credentials.
    - **Target Connection**:
        - **Storage Provider**: choose Azure Blob Storage.
        - **Folder URI**: enter the URI of Azure Blob Storage with the `azure://<account-name>.blob.core.windows.net/<container-name>/<folder-path>/` format.
        - **SAS Token**: enter the SAS token that has the permission to access the container. It is recommended to create a SAS token with the [Azure ARM template](https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/). For more information, see [Configure External Storage Access](/tidb-cloud/configure-external-storage-access.md#configure-azure-blob-storage-access).
    - **Exported Data**: choose the databases or tables you want to export.
    - **Data Format**: choose **SQL** or **CSV**.
    - **Compression**: choose **Gzip**, **Snappy**, **Zstd**, or **None**.

4. Click **Export**.

### Export data to Alibaba Cloud OSS

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**TiDB Instances**](https://tidbcloud.com/tidbs) page.

   > **Tip:**
   >
   > If you are in multiple organizations, use the combo box in the upper-left corner to switch to your target organization first.

2. Click the name of your target {{{ .premium }}} instance to go to its overview page, and then click **Data** > **Export** in the left navigation pane.

3. On the **Export** page, click **Export Data** in the upper-right corner:

    - **Task Name**: enter a name for the export task. The default value is `SNAPSHOT_{snapshot_time}`.
    - **Source Connection**: enter **Username** and **Password** of your {{{ .premium }}} instance, and then click **Test Connection** to verify the credentials.
    - **Target Connection**:
        - **Storage Provider**: choose Alibaba Cloud OSS.
        - **Folder URI**: enter the Alibaba Cloud OSS URI where you want to export the data, in the `oss://<bucket-name>/<folder-path>/` format.
        - **AccessKey ID** and **AccessKey Secret**: enter the AccessKey ID and AccessKey Secret that have the permission to access the bucket.
    - **Exported Data**: choose the databases or tables you want to export.
    - **Data Format**: choose **SQL** or **CSV**.
    - **Compression**: choose **Gzip**, **Snappy**, **Zstd**, or **None**.

4. Click **Export**.

### Cancel an export task

To cancel an ongoing export task, take the following steps:

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**TiDB Instances**](https://tidbcloud.com/tidbs) page.

   > **Tip:**
   >
   > If you are in multiple organizations, use the combo box in the upper-left corner to switch to your target organization first.

2. Click the name of your target {{{ .premium }}} instance to go to its overview page, and then click **Data** > **Export** in the left navigation pane.

3. On the **Export** page, view the export task list.

4. Choose the export task you want to cancel, and then click **Action**.

5. Choose **Cancel** in the drop-down list. Note that you can only cancel the export task that is in the **Running** status.
