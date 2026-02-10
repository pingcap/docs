---
title: Import CSV Files from Cloud Storage into TiDB Cloud Dedicated
summary: Learn how to import CSV files from Amazon S3, GCS, or Azure Blob Storage into TiDB Cloud Dedicated.
aliases: ['/tidbcloud/migrate-from-amazon-s3-or-gcs','/tidbcloud/migrate-from-aurora-bulk-import']
---

# Import CSV Files from Cloud Storage into TiDB Cloud Dedicated

This document describes how to import CSV files from Amazon Simple Storage Service (Amazon S3), Google Cloud Storage (GCS), or Azure Blob Storage into TiDB Cloud Dedicated.

## Limitations

- To ensure data consistency, TiDB Cloud allows importing CSV files into empty tables only. To import data into an existing table that already contains data, you can use TiDB Cloud to import the data into a temporary empty table by following this document, and then use the `INSERT SELECT` statement to copy the data to the target existing table.

- If a TiDB Cloud Dedicated cluster has a [changefeed](/tidb-cloud/changefeed-overview.md) or has [Point-in-time Restore](/tidb-cloud/backup-and-restore.md#turn-on-point-in-time-restore) enabled, you cannot import data to the cluster (the **Import Data** button will be disabled) because the current data import feature uses the [physical import mode](https://docs.pingcap.com/tidb/stable/tidb-lightning-physical-import-mode). In this mode, the imported data does not generate change logs, so the changefeed and Point-in-time Restore cannot detect the imported data.

## Step 1. Prepare the CSV files

1. If a CSV file is larger than 256 MiB, consider splitting it into smaller files, each with a size of around 256 MiB.

    TiDB Cloud supports importing very large CSV files but performs best with multiple input files around 256 MiB in size. This is because TiDB Cloud can process multiple files in parallel, which can greatly improve the import speed.

2. Name the CSV files as follows:

    - If a CSV file contains all data of an entire table, name the file in the `${db_name}.${table_name}.csv` format, which maps to the `${db_name}.${table_name}` table when you import the data.
    - If the data of one table is separated into multiple CSV files, append a numeric suffix to these CSV files. For example, `${db_name}.${table_name}.000001.csv` and `${db_name}.${table_name}.000002.csv`. The numeric suffixes can be inconsecutive but must be in ascending order. You also need to add extra zeros before the number to ensure all the suffixes are of the same length.
    - TiDB Cloud supports importing compressed files in the following formats: `.gzip`, `.gz`, `.zstd`, `.zst`, and `.snappy`. If you want to import compressed CSV files, name the files in the `${db_name}.${table_name}.${suffix}.csv.${compress}` format, in which `${suffix}` is optional and can be any integer such as '000001'. For example, if you want to import the `trips.000001.csv.gz` file to the `bikeshare.trips` table, you need to rename the file as `bikeshare.trips.000001.csv.gz`.

    > **Note:**
    >
    > - You only need to compress the data files, not the database or table schema files.
    > - To achieve better performance, it is recommended to limit the size of each compressed file to 100 MiB.
    > - The Snappy compressed file must be in the [official Snappy format](https://github.com/google/snappy). Other variants of Snappy compression are not supported.
    > - For uncompressed files, if you cannot update the CSV filenames according to the preceding rules in some cases (for example, the CSV file links are also used by your other programs), you can keep the filenames unchanged and use the **Mapping Settings** in [Step 4](#step-4-import-csv-files-to-tidb-cloud) to import your source data to a single target table.

## Step 2. Create the target table schemas

Because CSV files do not contain schema information, before importing data from CSV files into TiDB Cloud, you need to create the table schemas using either of the following methods:

- Method 1: In TiDB Cloud, create the target databases and tables for your source data.

- Method 2: In the Amazon S3, GCS, or Azure Blob Storage directory where the CSV files are located, create the target table schema files for your source data as follows:

    1. Create database schema files for your source data.

        If your CSV files follow the naming rules in [Step 1](#step-1-prepare-the-csv-files), the database schema files are optional for the data import. Otherwise, the database schema files are mandatory.

        Each database schema file must be in the `${db_name}-schema-create.sql` format and contain a `CREATE DATABASE` DDL statement. With this file, TiDB Cloud will create the `${db_name}` database to store your data when you import the data.

        For example, if you create a `mydb-scehma-create.sql` file that contains the following statement, TiDB Cloud will create the `mydb` database when you import the data.

        {{< copyable "sql" >}}

        ```sql
        CREATE DATABASE mydb;
        ```

    2. Create table schema files for your source data.

        If you do not include the table schema files in the Amazon S3, GCS, or Azure Blob Storage directory where the CSV files are located, TiDB Cloud will not create the corresponding tables for you when you import the data.

        Each table schema file must be in the `${db_name}.${table_name}-schema.sql` format and contain a `CREATE TABLE` DDL statement. With this file, TiDB Cloud will create the `${db_table}` table in the `${db_name}` database when you import the data.

        For example, if you create a `mydb.mytable-schema.sql` file that contains the following statement, TiDB Cloud will create the `mytable` table in the `mydb` database when you import the data.

        {{< copyable "sql" >}}

        ```sql
        CREATE TABLE mytable (
        ID INT,
        REGION VARCHAR(20),
        COUNT INT );
        ```

        > **Note:**
        >
        > Each `${db_name}.${table_name}-schema.sql` file should only contain a single DDL statement. If the file contains multiple DDL statements, only the first one takes effect.

## Step 3. Configure cross-account access

To allow TiDB Cloud to access the CSV files in the Amazon S3 bucket, GCS bucket, or Azure Blob Storage container, do one of the following:

- If your CSV files are located in Amazon S3, [configure Amazon S3 access](/tidb-cloud/dedicated-external-storage.md#configure-amazon-s3-access).

    You can use either an AWS access key or a Role ARN to access your bucket. Once finished, make a note of the access key (including the access key ID and secret access key) or the Role ARN value as you will need it in [Step 4](#step-4-import-csv-files-to-tidb-cloud).

- If your CSV files are located in GCS, [configure GCS access](/tidb-cloud/dedicated-external-storage.md#configure-gcs-access).

- If your CSV files are located in Azure Blob Storage, [configure Azure Blob Storage access](/tidb-cloud/dedicated-external-storage.md#configure-azure-blob-storage-access).

## Step 4. Import CSV files to TiDB Cloud

To import the CSV files to TiDB Cloud, take the following steps:

<SimpleTab>
<div label="Amazon S3">

1. Open the **Import** page for your target cluster.

    1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

        > **Tip:**
        >
        > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

    2. Click the name of your target cluster to go to its overview page, and then click **Data** > **Import** in the left navigation pane.

2. Select **Import data from Cloud Storage**.

3. On the **Import Data from Amazon S3** page, provide the following information:

    - **Included Schema Files**: if the source folder contains the target table schema files (such as `${db_name}-schema-create.sql`), select **Yes**. Otherwise, select **No**.
    - **Data Format**: select **CSV**.
    - **Edit CSV Configuration**: if necessary, configure the options according to your CSV files. You can set the separator and delimiter characters, specify whether to use backslashes for escaped characters, and specify whether your files contain a header row.
    - **Folder URI**: enter the source folder URI in the `s3://[bucket_name]/[data_source_folder]/` format. The path must end with a `/`. For example, `s3://mybucket/myfolder/`.
    - **Bucket Access**: you can use either an AWS IAM role ARN or an AWS access key to access your bucket.
        - **AWS Role ARN** (recommended): enter the AWS IAM role ARN value. If you don't have an IAM role for the bucket yet, you can create it using the provided AWS CloudFormation template by clicking **Click here to create new one with AWS CloudFormation** and following the instructions on the screen. Alternatively, you can manually create an IAM role ARN for the bucket.
        - **AWS Access Key**: enter the AWS access key ID and AWS secret access key.
        - For detailed instructions on both methods, see [Configure Amazon S3 access](/tidb-cloud/dedicated-external-storage.md#configure-amazon-s3-access).

4. Click **Connect**.

5. In the **Destination** section, select the target database and table.

    When importing multiple files, you can use **Advanced Settings** > **Mapping Settings** to customize the mapping of individual target tables to their corresponding CSV files. For each target database and table:

    - **Target Database**: select the corresponding database name from the list.
    - **Target Table**: select the corresponding table name from the list.
    - **Source File URIs and Names**: enter the full URI of the source file, including the folder and file name, making sure it is in the `s3://[bucket_name]/[data_source_folder]/[file_name].csv` format. You can also use wildcards (`?` and `*`) to match multiple files. For example:
        - `s3://mybucket/myfolder/my-data1.csv`: a single CSV file named `my-data1.csv` in `myfolder` will be imported into the target table.
        - `s3://mybucket/myfolder/my-data?.csv`: all CSV files starting with `my-data` followed by one character (such as `my-data1.csv` and `my-data2.csv`) in `myfolder` will be imported into the same target table.
        - `s3://mybucket/myfolder/my-data*.csv`: all CSV files starting with `my-data` (such as `my-data10.csv` and `my-data100.csv`) in `myfolder` will be imported into the same target table.

6. Click **Start Import**.

7. When the import progress shows **Completed**, check the imported tables.

</div>

<div label="Google Cloud">

1. Open the **Import** page for your target cluster.

    1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

        > **Tip:**
        >
        > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

    2. Click the name of your target cluster to go to its overview page, and then click **Data** > **Import** in the left navigation pane.

2. Select **Import data from Cloud Storage**.

3. On the **Import Data from Cloud Storage** page, provide the following information for the source CSV files:

    - **Included Schema Files**: if the source folder contains the target table schema files (such as `${db_name}-schema-create.sql`), select **Yes**. Otherwise, select **No**.
    - **Data Format**: select **CSV**.
    - **Edit CSV Configuration**: if necessary, configure the options according to your CSV files. You can set the separator and delimiter characters, specify whether to use backslashes for escaped characters, and specify whether your files contain a header row.
    - **Folder URI**: enter the source folder URI in the `gs://[bucket_name]/[data_source_folder]/` format. The path must end with a `/`. For example, `gs://sampledata/ingest/`.
    - **Google Cloud Service Account ID**: TiDB Cloud provides a unique Service Account ID on this page (such as `example-service-account@your-project.iam.gserviceaccount.com`). You must grant this Service Account ID the necessary IAM permissions (such as "Storage Object Viewer") on your GCS bucket within your Google Cloud project. For more information, see [Configure GCS access](/tidb-cloud/dedicated-external-storage.md#configure-gcs-access).

4. Click **Connect**.

5. In the **Destination** section, select the target database and table.

    When importing multiple files, you can use **Advanced Settings** > **Mapping Settings** to customize the mapping of individual target tables to their corresponding CSV files. For each target database and table:

    - **Target Database**: select the corresponding database name from the list.
    - **Target Table**: select the corresponding table name from the list.
    - **Source File URIs and Names**: enter the full URI of the source file, including the folder and file name, making sure it is in the `gs://[bucket_name]/[data_source_folder]/[file_name].csv` format. You can also use wildcards (`?` and `*`) to match multiple files. For example:
        - `gs://mybucket/myfolder/my-data1.csv`: a single CSV file named `my-data1.csv` in `myfolder` will be imported into the target table.
        - `gs://mybucket/myfolder/my-data?.csv`: all CSV files starting with `my-data` followed by one character (such as `my-data1.csv` and `my-data2.csv`) in `myfolder` will be imported into the same target table.
        - `gs://mybucket/myfolder/my-data*.csv`: all CSV files starting with `my-data` (such as `my-data10.csv` and `my-data100.csv`) in `myfolder` will be imported into the same target table.

6. Click **Start Import**.

7. When the import progress shows **Completed**, check the imported tables.

</div>

<div label="Azure Blob Storage">

1. Open the **Import** page for your target cluster.

    1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

        > **Tip:**
        >
        > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

    2. Click the name of your target cluster to go to its overview page, and then click **Data** > **Import** in the left navigation pane.

2. Select **Import data from Cloud Storage**.

3. On the **Import Data from Azure Blob Storage** page, provide the following information:

    - **Included Schema Files**: if the source folder contains the target table schema files (such as `${db_name}-schema-create.sql`), select **Yes**. Otherwise, select **No**.
    - **Data Format**: select **CSV**.
    - **Connectivity Method**: select how TiDB Cloud connects to your Azure Blob Storage:

        - **Public** (default): connects over the public internet. Use this option when the storage account allows public network access.
        - **Private Link**: connects through an Azure private endpoint for network-isolated access. Use this option when the storage account blocks public access or when your security policy requires private connectivity. If you select **Private Link**, you need to provide the following additional field **Azure Blob Storage Resource ID**.  To find the resource ID:
            
            1. Go to the [Azure portal](https://portal.azure.com/).
            2. Navigate to your storage account, click **Overview** > **JSON View**.
            3. Copy the value of the `id` property. The resource ID is in the format `/subscriptions/<subscription_id>/resourceGroups/<resource_group>/providers/Microsoft.Storage/storageAccounts/<account_name>`.

    - **Edit CSV Configuration**: if necessary, configure the options according to your CSV files. You can set the separator and delimiter characters, specify whether to use backslashes for escaped characters, and specify whether your files contain a header row.
    - **Folder URI**: enter the Azure Blob Storage URI where your source files are located using the format `https://[account_name].blob.core.windows.net/[container_name]/[data_source_folder]/`. The path must end with a `/`. For example, `https://myaccount.blob.core.windows.net/mycontainer/myfolder/`.
    - **SAS Token**: enter an account SAS token to allow TiDB Cloud to access the source files in your Azure Blob Storage container. If you don't have one yet, you can create it using the provided Azure ARM template by clicking **Click here to create a new one with Azure ARM template** and following the instructions on the screen. Alternatively, you can manually create an account SAS token. For more information, see [Configure Azure Blob Storage access](/tidb-cloud/dedicated-external-storage.md#configure-azure-blob-storage-access).

4. Click **Connect**.

    If you selected **Private Link** as the connectivity method, TiDB Cloud creates a private endpoint for your storage account. You need to approve this endpoint request in the Azure portal before the connection can proceed:

    1. Go to the [Azure portal](https://portal.azure.com/) and navigate to your storage account.
    2. Click **Networking** > **Private endpoint connections**.
    3. Find the pending connection request from TiDB Cloud and click **Approve**.
    4. Return to the [TiDB Cloud console](https://tidbcloud.com/). The import wizard proceeds automatically once the endpoint is approved.

    > **Note:**
    >
    > If the endpoint is not yet approved, TiDB Cloud displays the following message: "Connection pending. Please approve the Private Endpoint request in your Azure Portal settings and try again." Approve the request in the [Azure portal](https://portal.azure.com/) and retry the connection.

5. In the **Destination** section, select the target database and table.

    When importing multiple files, you can use **Advanced Settings** > **Mapping Settings** to customize the mapping of individual target tables to their corresponding CSV files. For each target database and table:

    - **Target Database**: select the corresponding database name from the list.
    - **Target Table**: select the corresponding table name from the list.
    - **Source File URIs and Names**: enter the full URI of the source file, including the folder and file name, making sure it is in the `https://[account_name].blob.core.windows.net/[container_name]/[data_source_folder]/[file_name].csv` format. You can also use wildcards (`?` and `*`) to match multiple files. For example:
        - `https://myaccount.blob.core.windows.net/mycontainer/myfolder/my-data1.csv`: a single CSV file named `my-data1.csv` in `myfolder` will be imported into the target table.
        - `https://myaccount.blob.core.windows.net/mycontainer/myfolder/my-data?.csv`: all CSV files starting with `my-data` followed by one character (such as `my-data1.csv` and `my-data2.csv`) in `myfolder` will be imported into the same target table.
        - `https://myaccount.blob.core.windows.net/mycontainer/myfolder/my-data*.csv`: all CSV files starting with `my-data` (such as `my-data10.csv` and `my-data100.csv`) in `myfolder` will be imported into the same target table.

6. Click **Start Import**.

7. When the import progress shows **Completed**, check the imported tables.

</div>

</SimpleTab>

When you run an import task, if any unsupported or invalid conversions are detected, TiDB Cloud terminates the import job automatically and reports an importing error. You can view details in the **Status** field.

If you get an importing error, do the following:

1. Drop the partially imported table.
2. Check the table schema file. If there are any errors, correct the table schema file.
3. Check the data types in the CSV files.
4. Try the import task again.

## Troubleshooting

### Resolve warnings during data import

After clicking **Start Import**, if you see a warning message such as `can't find the corresponding source files`, resolve this by providing the correct source file, renaming the existing one according to [Naming Conventions for Data Import](/tidb-cloud/naming-conventions-for-data-import.md), or using **Advanced Settings** to make changes.

After resolving these issues, you need to import the data again.

### Zero rows in the imported tables

After the import progress shows **Completed**, check the imported tables. If the number of rows is zero, it means no data files matched the Bucket URI that you entered. In this case, resolve this issue by providing the correct source file, renaming the existing one according to [Naming Conventions for Data Import](/tidb-cloud/naming-conventions-for-data-import.md), or using **Advanced Settings** to make changes. After that, import those tables again.
