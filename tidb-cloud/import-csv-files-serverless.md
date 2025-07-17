---
title: Import CSV Files from Amazon S3, GCS, Azure Blob Storage, or Alibaba Cloud OSS into TiDB Cloud Serverless
summary: Learn how to import CSV files from Amazon S3, GCS, Azure Blob Storage, or Alibaba Cloud Object Storage Service (OSS) into TiDB Cloud Serverless.
---

# Import CSV Files from Amazon S3, GCS, Azure Blob Storage, or Alibaba Cloud OSS into TiDB Cloud Serverless

This document describes how to import CSV files from Amazon Simple Storage Service (Amazon S3), Google Cloud Storage (GCS), Azure Blob Storage, or Alibaba Cloud Object Storage Service (OSS) into TiDB Cloud Serverless.

## Limitations

- To ensure data consistency, TiDB Cloud Serverless allows to import CSV files into empty tables only. To import data into an existing table that already contains data, you can use TiDB Cloud Serverless to import the data into a temporary empty table by following this document, and then use the `INSERT SELECT` statement to copy the data to the target existing table.

## Step 1. Prepare the CSV files

1. If a CSV file is larger than 256 MB, consider splitting it into smaller files, each with a size around 256 MB.

    TiDB Cloud Serverless supports importing very large CSV files but performs best with multiple input files around 256 MB in size. This is because TiDB Cloud Serverless can process multiple files in parallel, which can greatly improve the import speed.

2. Name the CSV files as follows:

    - If a CSV file contains all data of an entire table, name the file in the `${db_name}.${table_name}.csv` format, which maps to the `${db_name}.${table_name}` table when you import the data.
    - If the data of one table is separated into multiple CSV files, append a numeric suffix to these CSV files. For example, `${db_name}.${table_name}.000001.csv` and `${db_name}.${table_name}.000002.csv`. The numeric suffixes can be inconsecutive but must be in ascending order. You also need to add extra zeros before the number to ensure all the suffixes are in the same length.
    - TiDB Cloud Serverless supports importing compressed files in the following formats: `.gzip`, `.gz`, `.zstd`, `.zst` and `.snappy`. If you want to import compressed CSV files, name the files in the `${db_name}.${table_name}.${suffix}.csv.${compress}` format, in which `${suffix}` is optional and can be any integer such as '000001'. For example, if you want to import the `trips.000001.csv.gz` file to the `bikeshare.trips` table, you need to rename the file as `bikeshare.trips.000001.csv.gz`.

    > **Note:**
    >
    > - To achieve better performance, it is recommended to limit the size of each compressed file to 100 MiB.
    > - The Snappy compressed file must be in the [official Snappy format](https://github.com/google/snappy). Other variants of Snappy compression are not supported.
    > - For uncompressed files, if you cannot update the CSV filenames according to the preceding rules in some cases (for example, the CSV file links are also used by your other programs), you can keep the filenames unchanged and use the **Mapping Settings** in [Step 4](#step-4-import-csv-files-to-tidb-cloud-serverless) to import your source data to a single target table.

## Step 2. Create the target table schemas

Because CSV files do not contain schema information, before importing data from CSV files into TiDB Cloud Serverless, you need to create the table schemas using either of the following methods:

- Method 1: In TiDB Cloud Serverless, create the target databases and tables for your source data.

- Method 2: In the Amazon S3, GCS, Azure Blob Storage, or Alibaba Cloud Object Storage Service directory where the CSV files are located, create the target table schema files for your source data as follows:

    1. Create database schema files for your source data.

        If your CSV files follow the naming rules in [Step 1](#step-1-prepare-the-csv-files), the database schema files are optional for the data import. Otherwise, the database schema files are mandatory.

        Each database schema file must be in the `${db_name}-schema-create.sql` format and contain a `CREATE DATABASE` DDL statement. With this file, TiDB Cloud Serverless will create the `${db_name}` database to store your data when you import the data.

        For example, if you create a `mydb-scehma-create.sql` file that contains the following statement, TiDB Cloud Serverless will create the `mydb` database when you import the data.

        ```sql
        CREATE DATABASE mydb;
        ```

    2. Create table schema files for your source data.

        If you do not include the table schema files in the Amazon S3, GCS, Azure Blob Storage, or Alibaba Cloud Object Storage Service directory where the CSV files are located, TiDB Cloud Serverless will not create the corresponding tables for you when you import the data.

        Each table schema file must be in the `${db_name}.${table_name}-schema.sql` format and contain a `CREATE TABLE` DDL statement. With this file, TiDB Cloud Serverless will create the `${db_table}` table in the `${db_name}` database when you import the data.

        For example, if you create a `mydb.mytable-schema.sql` file that contains the following statement, TiDB Cloud Serverless will create the `mytable` table in the `mydb` database when you import the data.

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

To allow TiDB Cloud Serverless to access the CSV files in the Amazon S3, GCS, Azure Blob Storage, or Alibaba Cloud Object Storage Service bucket, do one of the following:

- If your CSV files are located in Amazon S3, [configure external storage access for TiDB Cloud Serverless](/tidb-cloud/serverless-external-storage.md#configure-amazon-s3-access).

    You can use either an AWS access key or a Role ARN to access your bucket. Once finished, make a note of the access key (including the access key ID and secret access key) or the Role ARN value as you will need it in [Step 4](#step-4-import-csv-files-to-tidb-cloud-serverless).

- If your CSV files are located in GCS, [configure external storage access for TiDB Cloud Serverless](/tidb-cloud/serverless-external-storage.md#configure-gcs-access).

- If your CSV files are located in Azure Blob Storage, [configure external storage access for TiDB Cloud Serverless](/tidb-cloud/serverless-external-storage.md#configure-azure-blob-storage-access).

- If your CSV files are located in Alibaba Cloud Object Storage Service (OSS), [configure external storage access for TiDB Cloud Serverless](/tidb-cloud/serverless-external-storage.md#configure-alibaba-cloud-object-storage-service-oss-access).

## Step 4. Import CSV files to TiDB Cloud Serverless

To import the CSV files to TiDB Cloud Serverless, take the following steps:

<SimpleTab>
<div label="Amazon S3">

1. Open the **Import** page for your target cluster.

    1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

        > **Tip:**
        >
        > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

    2. Click the name of your target cluster to go to its overview page, and then click **Data** > **Import** in the left navigation pane.

2. Select **Import data from Cloud Storage**, and then click **Amazon S3**.

3. On the **Import Data from Amazon S3** page, provide the following information for the source CSV files:

    - **Import File Count**: select **One file** or **Multiple files** as needed.
    - **Included Schema Files**: this field is only visible when importing multiple files. If the source folder contains the target table schemas, select **Yes**. Otherwise, select **No**.
    - **Data Format**: select **CSV**.
    - **File URI** or **Folder URI**:
        - When importing one file, enter the source file URI and name in the following format `s3://[bucket_name]/[data_source_folder]/[file_name].csv`. For example, `s3://sampledata/ingest/TableName.01.csv`.
        - When importing multiple files, enter the source file URI and name in the following format `s3://[bucket_name]/[data_source_folder]/`. For example, `s3://sampledata/ingest/`.
    - **Bucket Access**: you can use either an AWS Role ARN or an AWS access key to access your bucket. For more information, see [Configure Amazon S3 access](/tidb-cloud/serverless-external-storage.md#configure-amazon-s3-access).
        - **AWS Role ARN**: enter the AWS Role ARN value.
        - **AWS Access Key**: enter the AWS access key ID and AWS secret access key.

4. Click **Connect**.

5. In the **Destination** section, select the target database and table.

    When importing multiple files, you can use **Advanced Settings** > **Mapping Settings** to define a custom mapping rule for each target table and its corresponding CSV file. After that, the data source files will be re-scanned using the provided custom mapping rule.

    When you enter the source file URI and name in **Source File URIs and Names**, make sure it is in the following format `s3://[bucket_name]/[data_source_folder]/[file_name].csv`. For example, `s3://sampledata/ingest/TableName.01.csv`.

    You can also use wildcards to match the source files. For example:

    - `s3://[bucket_name]/[data_source_folder]/my-data?.csv`: all CSV files starting with `my-data` followed by one character (such as `my-data1.csv` and `my-data2.csv`) in that folder will be imported into the same target table.

    - `s3://[bucket_name]/[data_source_folder]/my-data*.csv`: all CSV files in the folder starting with `my-data` will be imported into the same target table.

    Note that only `?` and `*` are supported.

    > **Note:**
    >
    > The URI must contain the data source folder.

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

2. Select **Import data from Cloud Storage**, and then click **Google Cloud Storage**.

3. On the **Import Data from Google Cloud Storage** page, provide the following information for the source CSV files:

    - **Import File Count**: select **One file** or **Multiple files** as needed.
    - **Included Schema Files**: this field is only visible when importing multiple files. If the source folder contains the target table schemas, select **Yes**. Otherwise, select **No**.
    - **Data Format**: select **CSV**.
    - **File URI** or **Folder URI**:
        - When importing one file, enter the source file URI and name in the following format `[gcs|gs]://[bucket_name]/[data_source_folder]/[file_name].csv`. For example, `[gcs|gs]://sampledata/ingest/TableName.01.csv`.
        - When importing multiple files, enter the source file URI and name in the following format `[gcs|gs]://[bucket_name]/[data_source_folder]/`. For example, `[gcs|gs]://sampledata/ingest/`.
    - **Bucket Access**: you can use a service account key to access your bucket. For more information, see [Configure GCS access](/tidb-cloud/serverless-external-storage.md#configure-gcs-access).

4. Click **Connect**.

5. In the **Destination** section, select the target database and table.

    When importing multiple files, you can use **Advanced Settings** > **Mapping Settings** to define a custom mapping rule for each target table and its corresponding CSV file. After that, the data source files will be re-scanned using the provided custom mapping rule.

    When you enter the source file URI and name in **Source File URIs and Names**, make sure it is in the following format `[gcs|gs]://[bucket_name]/[data_source_folder]/[file_name].csv`. For example, `[gcs|gs]://sampledata/ingest/TableName.01.csv`.

    You can also use wildcards to match the source files. For example:

    - `[gcs|gs]://[bucket_name]/[data_source_folder]/my-data?.csv`: all CSV files starting with `my-data` followed by one character (such as `my-data1.csv` and `my-data2.csv`) in that folder will be imported into the same target table.

    - `[gcs|gs]://[bucket_name]/[data_source_folder]/my-data*.csv`: all CSV files in the folder starting with `my-data` will be imported into the same target table.

    Note that only `?` and `*` are supported.

    > **Note:**
    >
    > The URI must contain the data source folder.

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

2. Select **Import data from Cloud Storage**, and then click **Azure Blob Storage**.

3. On the **Import Data from Azure Blob Storage** page, provide the following information for the source CSV files:

    - **Import File Count**: select **One file** or **Multiple files** as needed.
    - **Included Schema Files**: this field is only visible when importing multiple files. If the source folder contains the target table schemas, select **Yes**. Otherwise, select **No**.
    - **Data Format**: select **CSV**.
    - **File URI** or **Folder URI**:
        - When importing one file, enter the source file URI and name in the following format `[azure|https]://[bucket_name]/[data_source_folder]/[file_name].csv`. For example, `[azure|https]://sampledata/ingest/TableName.01.csv`.
        - When importing multiple files, enter the source file URI and name in the following format `[azure|https]://[bucket_name]/[data_source_folder]/`. For example, `[azure|https]://sampledata/ingest/`.
    - **Bucket Access**: you can use a shared access signature (SAS) token to access your bucket. For more information, see [Configure Azure Blob Storage access](/tidb-cloud/serverless-external-storage.md#configure-azure-blob-storage-access).

4. Click **Connect**.

5. In the **Destination** section, select the target database and table.

    When importing multiple files, you can use **Advanced Settings** > **Mapping Settings** to define a custom mapping rule for each target table and its corresponding CSV file. After that, the data source files will be re-scanned using the provided custom mapping rule.

    When you enter the source file URI and name in **Source File URIs and Names**, make sure it is in the following format `[azure|https]://[bucket_name]/[data_source_folder]/[file_name].csv`. For example, `[azure|https]://sampledata/ingest/TableName.01.csv`.

    You can also use wildcards to match the source files. For example:

    - `[azure|https]://[bucket_name]/[data_source_folder]/my-data?.csv`: all CSV files starting with `my-data` followed by one character (such as `my-data1.csv` and `my-data2.csv`) in that folder will be imported into the same target table.

    - `[azure|https]://[bucket_name]/[data_source_folder]/my-data*.csv`: all CSV files in the folder starting with `my-data` will be imported into the same target table.

    Note that only `?` and `*` are supported.

    > **Note:**
    >
    > The URI must contain the data source folder.

6. Click **Start Import**.

7. When the import progress shows **Completed**, check the imported tables.

</div>

<div label="Alibaba Cloud Object Storage Service (OSS)">

1. Open the **Import** page for your target cluster.

    1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

        > **Tip:**
        >
        > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

    2. Click the name of your target cluster to go to its overview page, and then click **Data** > **Import** in the left navigation pane.

2. Select **Import data from Cloud Storage**, and then click **Alibaba Cloud OSS**.

3. On the **Import Data from Alibaba Cloud OSS** page, provide the following information for the source CSV files:

    - **Import File Count**: select **One file** or **Multiple files** as needed.
    - **Included Schema Files**: this field is only visible when importing multiple files. If the source folder contains the target table schemas, select **Yes**. Otherwise, select **No**.
    - **Data Format**: select **CSV**.
    - **File URI** or **Folder URI**:
        - When importing one file, enter the source file URI and name in the following format `oss://[bucket_name]/[data_source_folder]/[file_name].csv`. For example, `oss://sampledata/ingest/TableName.01.csv`.
        - When importing multiple files, enter the source file URI and name in the following format `oss://[bucket_name]/[data_source_folder]/`. For example, `oss://sampledata/ingest/`.
    - **Bucket Access**: you can use an AccessKey pair to access your bucket. For more information, see [Configure Alibaba Cloud Object Storage Service (OSS) access](/tidb-cloud/serverless-external-storage.md#configure-alibaba-cloud-object-storage-service-oss-access).

4. Click **Connect**.

5. In the **Destination** section, select the target database and table.

    When importing multiple files, you can use **Advanced Settings** > **Mapping Settings** to define a custom mapping rule for each target table and its corresponding CSV file. After that, the data source files will be re-scanned using the provided custom mapping rule.

    When you enter the source file URI and name in **Source File URIs and Names**, make sure it is in the following format `oss://[bucket_name]/[data_source_folder]/[file_name].csv`. For example, `oss://sampledata/ingest/TableName.01.csv`.

    You can also use wildcards to match the source files. For example:

    - `oss://[bucket_name]/[data_source_folder]/my-data?.csv`: all CSV files starting with `my-data` followed by one character (such as `my-data1.csv` and `my-data2.csv`) in that folder will be imported into the same target table.

    - `oss://[bucket_name]/[data_source_folder]/my-data*.csv`: all CSV files in the folder starting with `my-data` will be imported into the same target table.

    Note that only `?` and `*` are supported.

    > **Note:**
    >
    > The URI must contain the data source folder.

6. Click **Start Import**.

7. When the import progress shows **Completed**, check the imported tables.

</div>

</SimpleTab>

When you run an import task, if any unsupported or invalid conversions are detected, TiDB Cloud Serverless terminates the import job automatically and reports an importing error.

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
