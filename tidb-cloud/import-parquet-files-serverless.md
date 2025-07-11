---
title: Import Apache Parquet Files from Amazon S3, GCS, Azure Blob Storage, or Alibaba Cloud OSS into TiDB Cloud Serverless
summary: Learn how to import Apache Parquet files from Amazon S3, GCS, Azure Blob Storage, or Alibaba Cloud Object Storage Service (OSS) into TiDB Cloud Serverless.
---

# Import Apache Parquet Files from Amazon S3, GCS, Azure Blob Storage, or Alibaba Cloud OSS into TiDB Cloud Serverless

You can import both uncompressed and Snappy compressed [Apache Parquet](https://parquet.apache.org/) format data files to TiDB Cloud Serverless. This document describes how to import Parquet files from Amazon Simple Storage Service (Amazon S3), Google Cloud Storage (GCS), Azure Blob Storage, or Alibaba Cloud Object Storage Service (OSS) into TiDB Cloud Serverless.

> **Note:**
>
> - TiDB Cloud Serverless only supports importing Parquet files into empty tables. To import data into an existing table that already contains data, you can use TiDB Cloud Serverless to import the data into a temporary empty table by following this document, and then use the `INSERT SELECT` statement to copy the data to the target existing table.
> - The Snappy compressed file must be in the [official Snappy format](https://github.com/google/snappy). Other variants of Snappy compression are not supported.

## Step 1. Prepare the Parquet files

> **Note:**
>
> Currently, TiDB Cloud Serverless does not support importing Parquet files that contain any of the following data types. If Parquet files to be imported contain such data types, you need to first regenerate the Parquet files using the [supported data types](#supported-data-types) (for example, `STRING`). Alternatively, you could use a service such as AWS Glue to transform data types easily.
>
> - `LIST`
> - `NEST STRUCT`
> - `BOOL`
> - `ARRAY`
> - `MAP`

1. If a Parquet file is larger than 256 MB, consider splitting it into smaller files, each with a size around 256 MB.

    TiDB Cloud Serverless supports importing very large Parquet files but performs best with multiple input files around 256 MB in size. This is because TiDB Cloud Serverless can process multiple files in parallel, which can greatly improve the import speed.

2. Name the Parquet files as follows:

    - If a Parquet file contains all data of an entire table, name the file in the `${db_name}.${table_name}.parquet` format, which maps to the `${db_name}.${table_name}` table when you import the data.
    - If the data of one table is separated into multiple Parquet files, append a numeric suffix to these Parquet files. For example, `${db_name}.${table_name}.000001.parquet` and `${db_name}.${table_name}.000002.parquet`. The numeric suffixes can be inconsecutive but must be in ascending order. You also need to add extra zeros before the number to ensure all the suffixes are in the same length.

    > **Note:**
    >
    > If you cannot update the Parquet filenames according to the preceding rules in some cases (for example, the Parquet file links are also used by your other programs), you can keep the filenames unchanged and use the **Mapping Settings** in [Step 4](#step-4-import-parquet-files-to-tidb-cloud-serverless) to import your source data to a single target table.

## Step 2. Create the target table schemas

Because Parquet files do not contain schema information, before importing data from Parquet files into TiDB Cloud Serverless, you need to create the table schemas using either of the following methods:

- Method 1: In TiDB Cloud Serverless, create the target databases and tables for your source data.

- Method 2: In the Amazon S3, GCS, Azure Blob Storage, or Alibaba Cloud Object Storage Service directory where the Parquet files are located, create the target table schema files for your source data as follows:

    1. Create database schema files for your source data.

        If your Parquet files follow the naming rules in [Step 1](#step-1-prepare-the-parquet-files), the database schema files are optional for the data import. Otherwise, the database schema files are mandatory.

        Each database schema file must be in the `${db_name}-schema-create.sql` format and contain a `CREATE DATABASE` DDL statement. With this file, TiDB Cloud Serverless will create the `${db_name}` database to store your data when you import the data.

        For example, if you create a `mydb-scehma-create.sql` file that contains the following statement, TiDB Cloud Serverless will create the `mydb` database when you import the data.

        ```sql
        CREATE DATABASE mydb;
        ```

    2. Create table schema files for your source data.

        If you do not include the table schema files in the Amazon S3, GCS, Azure Blob Storage, or Alibaba Cloud Object Storage Service directory where the Parquet files are located, TiDB Cloud Serverless will not create the corresponding tables for you when you import the data.

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

To allow TiDB Cloud Serverless to access the Parquet files in the Amazon S3, GCS, Azure Blob Storage, or Alibaba Cloud Object Storage Service bucket, do one of the following:

- If your Parquet files are located in Amazon S3, [configure external storage access for TiDB Cloud Serverless](/tidb-cloud/serverless-external-storage.md#configure-amazon-s3-access).

    You can use either an AWS access key or a Role ARN to access your bucket. Once finished, make a note of the access key (including the access key ID and secret access key) or the Role ARN value as you will need it in [Step 4](#step-4-import-parquet-files-to-tidb-cloud-serverless).

- If your Parquet files are located in GCS, [configure external storage access for TiDB Cloud Serverless](/tidb-cloud/serverless-external-storage.md#configure-gcs-access).

- If your Parquet files are located in Azure Blob Storage, [configure external storage access for TiDB Cloud Serverless](/tidb-cloud/serverless-external-storage.md#configure-azure-blob-storage-access).

- If your Parquet files are located in Alibaba Cloud Object Storage Service (OSS), [configure external storage access for TiDB Cloud Serverless](/tidb-cloud/serverless-external-storage.md#configure-alibaba-cloud-object-storage-service-oss-access).

## Step 4. Import Parquet files to TiDB Cloud Serverless

To import the Parquet files to TiDB Cloud Serverless, take the following steps:

<SimpleTab>
<div label="Amazon S3">

1. Open the **Import** page for your target cluster.

    1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

        > **Tip:**
        >
        > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

    2. Click the name of your target cluster to go to its overview page, and then click **Data** > **Import** in the left navigation pane.

2. Click **Import data from Cloud Storage**.

3. On the **Import Data from Cloud Storage** page, provide the following information:

    - **Storage Provider**: select **Amazon S3**.
    - **Source Files URI**:
        - When importing one file, enter the source file URI and name in the following format `s3://[bucket_name]/[data_source_folder]/[file_name].parquet`. For example, `s3://sampledata/ingest/TableName.01.parquet`.
        - When importing multiple files, enter the source file URI and name in the following format `s3://[bucket_name]/[data_source_folder]/`. For example, `s3://sampledata/ingest/`.
    - **Credential**: you can use either an AWS Role ARN or an AWS access key to access your bucket. For more information, see [Configure Amazon S3 access](/tidb-cloud/serverless-external-storage.md#configure-amazon-s3-access).
        - **AWS Role ARN**: enter the AWS Role ARN value.
        - **AWS Access Key**: enter the AWS access key ID and AWS secret access key.

4. Click **Next**.

5. In the **Destination Mapping** section, specify how source files are mapped to target tables.

    When a directory is specified in **Source Files URI**, the **Use [TiDB Dumpling file naming conventions](/tidb-cloud/naming-conventions-for-data-import.md) for automatic mapping** option is selected by default.

    > **Note:**
    >
    > When a single file is specified in **Source Files URI**, the **Use [TiDB Dumpling file naming conventions](/tidb-cloud/naming-conventions-for-data-import.md) for automatic mapping** option is not displayed, and TiDB Cloud automatically populates the **Source** field with the file name. In this case, you only need to select the target database and table for data import.

    - To let TiDB Cloud automatically map all source files that follow the [TiDB Dumpling file naming conventions](/tidb-cloud/naming-conventions-for-data-import.md) to their corresponding tables, keep this option selected and select **Parquet** as the data format.

    - To manually configure the mapping rules to associate your source Parquet files with the target database and table, unselect this option, and then fill in the following fields:

        - **Source**: enter the file name pattern in the `[file_name].parquet` format. For example: `TableName.01.parquet`. You can also use wildcards to match multiple files. Only `*` and `?` wildcards are supported.

            - `my-data?.parquet`: matches all Parquet files that start with `my-data` followed by a single character, such as `my-data1.parquet` and `my-data2.parquet`.
            - `my-data*.parquet`: matches all Parquet files that start with `my-data`, such as `my-data-2023.parquet` and `my-data-final.parquet`.

        - **Target Database** and **Target Table**: select the target database and table to import the data to.

6. Click **Next**. TiDB Cloud scans the source files accordingly.

7. Review the scan results, check the data files found and corresponding target tables, and then click **Start Import**.

8. When the import progress shows **Completed**, check the imported tables.

</div>

<div label="Google Cloud">

1. Open the **Import** page for your target cluster.

    1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

        > **Tip:**
        >
        > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

    2. Click the name of your target cluster to go to its overview page, and then click **Data** > **Import** in the left navigation pane.

2. Click **Import data from Cloud Storage**.

3. On the **Import Data from Google Cloud Storage** page, provide the following information:

    - **Storage Provider**: select **Google Cloud Storage**.
    - **Source Files URI**:
        - When importing one file, enter the source file URI and name in the following format `[gcs|gs]://[bucket_name]/[data_source_folder]/[file_name].parquet`. For example, `[gcs|gs]://sampledata/ingest/TableName.01.parquet`.
        - When importing multiple files, enter the source file URI and name in the following format `[gcs|gs]://[bucket_name]/[data_source_folder]/`. For example, `[gcs|gs]://sampledata/ingest/`.
    - **Credential**: you can use a GCS IAM Role Service Account key to access your bucket. For more information, see [Configure GCS access](/tidb-cloud/serverless-external-storage.md#configure-gcs-access).

4. Click **Next**.

5. In the **Destination Mapping** section, specify how source files are mapped to target tables.

    When a directory is specified in **Source Files URI**, the **Use [TiDB Dumpling file naming conventions](/tidb-cloud/naming-conventions-for-data-import.md) for automatic mapping** option is selected by default.

    > **Note:**
    >
    > When a single file is specified in **Source Files URI**, the **Use [TiDB Dumpling file naming conventions](/tidb-cloud/naming-conventions-for-data-import.md) for automatic mapping** option is not displayed, and TiDB Cloud automatically populates the **Source** field with the file name. In this case, you only need to select the target database and table for data import.

    - To let TiDB Cloud automatically map all source files that follow the [TiDB Dumpling file naming conventions](/tidb-cloud/naming-conventions-for-data-import.md) to their corresponding tables, keep this option selected and select **Parquet** as the data format.

    - To manually configure the mapping rules to associate your source Parquet files with the target database and table, unselect this option, and then fill in the following fields:

        - **Source**: enter the file name pattern in the `[file_name].parquet` format. For example: `TableName.01.parquet`. You can also use wildcards to match multiple files. Only `*` and `?` wildcards are supported.

            - `my-data?.parquet`: matches all Parquet files that start with `my-data` followed by a single character, such as `my-data1.parquet` and `my-data2.parquet`.
            - `my-data*.parquet`: matches all Parquet files that start with `my-data`, such as `my-data-2023.parquet` and `my-data-final.parquet`.

        - **Target Database** and **Target Table**: select the target database and table to import the data to.

6. Click **Next**. TiDB Cloud scans the source files accordingly.

7. Review the scan results, check the data files found and corresponding target tables, and then click **Start Import**.

8. When the import progress shows **Completed**, check the imported tables.

</div>

<div label="Azure Blob Storage">

1. Open the **Import** page for your target cluster.

    1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

        > **Tip:**
        >
        > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

    2. Click the name of your target cluster to go to its overview page, and then click **Data** > **Import** in the left navigation pane.

2. Click **Import data from Cloud Storage**.

3. On the **Import Data from Cloud Storage** page, provide the following information:

    - **Storage Provider**: select **Azure Blob Storage**.
    - **Source Files URI**:
        - When importing one file, enter the source file URI and name in the following format `[azure|https]://[bucket_name]/[data_source_folder]/[file_name].parquet`. For example, `[azure|https]://sampledata/ingest/TableName.01.parquet`.
        - When importing multiple files, enter the source file URI and name in the following format `[azure|https]://[bucket_name]/[data_source_folder]/`. For example, `[azure|https]://sampledata/ingest/`.
    - **Credential**: you can use a shared access signature (SAS) token to access your bucket. For more information, see [Configure Azure Blob Storage access](/tidb-cloud/serverless-external-storage.md#configure-azure-blob-storage-access)

4. Click **Next**.

5. In the **Destination Mapping** section, specify how source files are mapped to target tables.

    When a directory is specified in **Source Files URI**, the **Use [TiDB Dumpling file naming conventions](/tidb-cloud/naming-conventions-for-data-import.md) for automatic mapping** option is selected by default.

    > **Note:**
    >
    > When a single file is specified in **Source Files URI**, the **Use [TiDB Dumpling file naming conventions](/tidb-cloud/naming-conventions-for-data-import.md) for automatic mapping** option is not displayed, and TiDB Cloud automatically populates the **Source** field with the file name. In this case, you only need to select the target database and table for data import.

    - To let TiDB Cloud automatically map all source files that follow the [TiDB Dumpling file naming conventions](/tidb-cloud/naming-conventions-for-data-import.md) to their corresponding tables, keep this option selected and select **Parquet** as the data format.

    - To manually configure the mapping rules to associate your source Parquet files with the target database and table, unselect this option, and then fill in the following fields:

        - **Source**: enter the file name pattern in the `[file_name].parquet` format. For example: `TableName.01.parquet`. You can also use wildcards to match multiple files. Only `*` and `?` wildcards are supported.

            - `my-data?.parquet`: matches all Parquet files that start with `my-data` followed by a single character, such as `my-data1.parquet` and `my-data2.parquet`.
            - `my-data*.parquet`: matches all Parquet files that start with `my-data`, such as `my-data-2023.parquet` and `my-data-final.parquet`.

        - **Target Database** and **Target Table**: select the target database and table to import the data to.

6. Click **Next**. TiDB Cloud scans the source files accordingly.

7. Review the scan results, check the data files found and corresponding target tables, and then click **Start Import**.

8. When the import progress shows **Completed**, check the imported tables.

</div>

<div label="Alibaba Cloud Object Storage Service (OSS)">

1. Open the **Import** page for your target cluster.

    1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

        > **Tip:**
        >
        > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

    2. Click the name of your target cluster to go to its overview page, and then click **Data** > **Import** in the left navigation pane.

2. Click **Import data from Cloud Storage**.

3. On the **Import Data from Cloud Storage** page, provide the following information:

    - **Storage Provider**: select **Alibaba Cloud OSS**.
    - **Source Files URI**:
        - When importing one file, enter the source file URI and name in the following format `oss://[bucket_name]/[data_source_folder]/[file_name].parquet`. For example, `oss://sampledata/ingest/TableName.01.parquet`.
        - When importing multiple files, enter the source file URI and name in the following format `oss://[bucket_name]/[data_source_folder]/`. For example, `oss://sampledata/ingest/`.
    - **Credential**: you can use an AccessKey pair to access your bucket. For more information, see [Configure Alibaba Cloud Object Storage Service (OSS) access](/tidb-cloud/serverless-external-storage.md#configure-alibaba-cloud-object-storage-service-oss-access).

4. Click **Next**.

5. In the **Destination Mapping** section, specify how source files are mapped to target tables.

    When a directory is specified in **Source Files URI**, the **Use [TiDB Dumpling file naming conventions](/tidb-cloud/naming-conventions-for-data-import.md) for automatic mapping** option is selected by default.

    > **Note:**
    >
    > When a single file is specified in **Source Files URI**, the **Use [TiDB Dumpling file naming conventions](/tidb-cloud/naming-conventions-for-data-import.md) for automatic mapping** option is not displayed, and TiDB Cloud automatically populates the **Source** field with the file name. In this case, you only need to select the target database and table for data import.

    - To let TiDB Cloud automatically map all source files that follow the [TiDB Dumpling file naming conventions](/tidb-cloud/naming-conventions-for-data-import.md) to their corresponding tables, keep this option selected and select **Parquet** as the data format.

    - To manually configure the mapping rules to associate your source Parquet files with the target database and table, unselect this option, and then fill in the following fields:

        - **Source**: enter the file name pattern in the `[file_name].parquet` format. For example: `TableName.01.parquet`. You can also use wildcards to match multiple files. Only `*` and `?` wildcards are supported.

            - `my-data?.parquet`: matches all Parquet files that start with `my-data` followed by a single character, such as `my-data1.parquet` and `my-data2.parquet`.
            - `my-data*.parquet`: matches all Parquet files that start with `my-data`, such as `my-data-2023.parquet` and `my-data-final.parquet`.

        - **Target Database** and **Target Table**: select the target database and table to import the data to.

6. Click **Next**. TiDB Cloud scans the source files accordingly.

7. Review the scan results, check the data files found and corresponding target tables, and then click **Start Import**.

8. When the import progress shows **Completed**, check the imported tables.

</div>

</SimpleTab>

When you run an import task, if any unsupported or invalid conversions are detected, TiDB Cloud Serverless terminates the import job automatically and reports an importing error.

If you get an importing error, do the following:

1. Drop the partially imported table.
2. Check the table schema file. If there are any errors, correct the table schema file.
3. Check the data types in the Parquet files.

    If the Parquet files contain any unsupported data types (for example, `NEST STRUCT`, `ARRAY`, or `MAP`), you need to regenerate the Parquet files using [supported data types](#supported-data-types) (for example, `STRING`).

4. Try the import task again.

## Supported data types

The following table lists the supported Parquet data types that can be imported to TiDB Cloud Serverless.

| Parquet Primitive Type | Parquet Logical Type | Types in TiDB or MySQL |
|---|---|---|
| DOUBLE | DOUBLE | DOUBLE<br />FLOAT |
| FIXED_LEN_BYTE_ARRAY(9) | DECIMAL(20,0) | BIGINT UNSIGNED |
| FIXED_LEN_BYTE_ARRAY(N) | DECIMAL(p,s) | DECIMAL<br />NUMERIC |
| INT32 | DECIMAL(p,s) | DECIMAL<br />NUMERIC |
| INT32 | N/A | INT<br />MEDIUMINT<br />YEAR |
| INT64 | DECIMAL(p,s) | DECIMAL<br />NUMERIC |
| INT64 | N/A | BIGINT<br />INT UNSIGNED<br />MEDIUMINT UNSIGNED |
| INT64 | TIMESTAMP_MICROS | DATETIME<br />TIMESTAMP |
| BYTE_ARRAY | N/A | BINARY<br />BIT<br />BLOB<br />CHAR<br />LINESTRING<br />LONGBLOB<br />MEDIUMBLOB<br />MULTILINESTRING<br />TINYBLOB<br />VARBINARY |
| BYTE_ARRAY | STRING | ENUM<br />DATE<br />DECIMAL<br />GEOMETRY<br />GEOMETRYCOLLECTION<br />JSON<br />LONGTEXT<br />MEDIUMTEXT<br />MULTIPOINT<br />MULTIPOLYGON<br />NUMERIC<br />POINT<br />POLYGON<br />SET<br />TEXT<br />TIME<br />TINYTEXT<br />VARCHAR |
| SMALLINT | N/A | INT32 |
| SMALLINT UNSIGNED | N/A | INT32 |
| TINYINT | N/A | INT32 |
| TINYINT UNSIGNED | N/A | INT32 |

## Troubleshooting

### Resolve warnings during data import

After clicking **Start Import**, if you see a warning message such as `can't find the corresponding source files`, resolve this by providing the correct source file, renaming the existing one according to [Naming Conventions for Data Import](/tidb-cloud/naming-conventions-for-data-import.md), or using **Advanced Settings** to make changes.

After resolving these issues, you need to import the data again.

### Zero rows in the imported tables

After the import progress shows **Completed**, check the imported tables. If the number of rows is zero, it means no data files matched the Bucket URI that you entered. In this case, resolve this issue by providing the correct source file, renaming the existing one according to [Naming Conventions for Data Import](/tidb-cloud/naming-conventions-for-data-import.md), or using **Advanced Settings** to make changes. After that, import those tables again.
