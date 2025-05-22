---
title: Import Apache Parquet Files from Amazon S3 or GCS into TiDB Cloud
summary: Learn how to import Apache Parquet files from Amazon S3 or GCS into TiDB Cloud.
---

# Import Apache Parquet Files from Amazon S3 or GCS into TiDB Cloud

You can import both uncompressed and Snappy compressed [Apache Parquet](https://parquet.apache.org/) format data files to TiDB Cloud. This document describes how to import Parquet files from Amazon Simple Storage Service (Amazon S3) or Google Cloud Storage (GCS) into TiDB Cloud.

> **Note:**
>
> - TiDB Cloud only supports importing Parquet files into empty tables. To import data into an existing table that already contains data, you can use TiDB Cloud to import the data into a temporary empty table by following this document, and then use the `INSERT SELECT` statement to copy the data to the target existing table.
> - If there is a changefeed in a TiDB Cloud Dedicated cluster, you cannot import data to the cluster (the **Import Data** button will be disabled), because the current import data feature uses the [physical import mode](https://docs.pingcap.com/tidb/stable/tidb-lightning-physical-import-mode). In this mode, the imported data does not generate change logs, so the changefeed cannot detect the imported data.
> - Only TiDB Cloud Dedicated clusters support importing Parquet files from GCS.
> - The Snappy compressed file must be in the [official Snappy format](https://github.com/google/snappy). Other variants of Snappy compression are not supported.

## Step 1. Prepare the Parquet files

> **Note:**
>
> Currently, TiDB Cloud does not support importing Parquet files that contain any of the following data types. If Parquet files to be imported contain such data types, you need to first regenerate the Parquet files using the [supported data types](#supported-data-types) (for example, `STRING`). Alternatively, you could use a service such as AWS Glue to transform data types easily.
>
> - `LIST`
> - `NEST STRUCT`
> - `BOOL`
> - `ARRAY`
> - `MAP`

1. If a Parquet file is larger than 256 MB, consider splitting it into smaller files, each with a size around 256 MB.

    TiDB Cloud supports importing very large Parquet files but performs best with multiple input files around 256 MB in size. This is because TiDB Cloud can process multiple files in parallel, which can greatly improve the import speed.

2. Name the Parquet files as follows:

    - If a Parquet file contains all data of an entire table, name the file in the `${db_name}.${table_name}.parquet` format, which maps to the `${db_name}.${table_name}` table when you import the data.
    - If the data of one table is separated into multiple Parquet files, append a numeric suffix to these Parquet files. For example, `${db_name}.${table_name}.000001.parquet` and `${db_name}.${table_name}.000002.parquet`. The numeric suffixes can be inconsecutive but must be in ascending order. You also need to add extra zeros before the number to ensure all the suffixes are in the same length.

    > **Note:**
    >
    > If you cannot update the Parquet filenames according to the preceding rules in some cases (for example, the Parquet file links are also used by your other programs), you can keep the filenames unchanged and use the **Mapping Settings** in [Step 4](#step-4-import-parquet-files-to-tidb-cloud) to import your source data to a single target table.

## Step 2. Create the target table schemas

Because Parquet files do not contain schema information, before importing data from Parquet files into TiDB Cloud, you need to create the table schemas using either of the following methods:

- Method 1: In TiDB Cloud, create the target databases and tables for your source data.

- Method 2: In the Amazon S3 or GCS directory where the Parquet files are located, create the target table schema files for your source data as follows:

    1. Create database schema files for your source data.

        If your Parquet files follow the naming rules in [Step 1](#step-1-prepare-the-parquet-files), the database schema files are optional for the data import. Otherwise, the database schema files are mandatory.

        Each database schema file must be in the `${db_name}-schema-create.sql` format and contain a `CREATE DATABASE` DDL statement. With this file, TiDB Cloud will create the `${db_name}` database to store your data when you import the data.

        For example, if you create a `mydb-scehma-create.sql` file that contains the following statement, TiDB Cloud will create the `mydb` database when you import the data.

        {{< copyable "sql" >}}

        ```sql
        CREATE DATABASE mydb;
        ```

    2. Create table schema files for your source data.

        If you do not include the table schema files in the Amazon S3 or GCS directory where the Parquet files are located, TiDB Cloud will not create the corresponding tables for you when you import the data.

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

To allow TiDB Cloud to access the Parquet files in the Amazon S3 or GCS bucket, do one of the following:

- If your Parquet files are located in Amazon S3, [configure Amazon S3 access](/tidb-cloud/config-s3-and-gcs-access.md#configure-amazon-s3-access).

    You can use either an AWS access key or a Role ARN to access your bucket. Once finished, make a note of the access key (including the access key ID and secret access key) or the Role ARN value as you will need it in [Step 4](#step-4-import-parquet-files-to-tidb-cloud).

- If your Parquet files are located in GCS, [configure GCS access](/tidb-cloud/config-s3-and-gcs-access.md#configure-gcs-access).

## Step 4. Import Parquet files to TiDB Cloud

To import the Parquet files to TiDB Cloud, take the following steps:

<SimpleTab>
<div label="Amazon S3">

1. Open the **Import** page for your target cluster.

    1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.

        > **Tip:**
        >
        > If you have multiple projects, you can click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner and switch to another project.

    2. Click the name of your target cluster to go to its overview page, and then click **Import** in the left navigation pane.

2. Select **Import data from S3**.

    If this is your first time importing data into this cluster, select **Import From Amazon S3**.

3. On the **Import Data from Amazon S3** page, provide the following information for the source Parquet files:

    - **Import File Count**: select **One file** or **Multiple files** as needed.
    - **Included Schema Files**: this field is only visible when importing multiple files. If the source folder contains the target table schemas, select **Yes**. Otherwise, select **No**.
    - **Data Format**: select **Parquet**.
    - **File URI** or **Folder URI**:
        - When importing one file, enter the source file URI and name in the following format `s3://[bucket_name]/[data_source_folder]/[file_name].parquet`. For example, `s3://sampledata/ingest/TableName.01.parquet`.
        - When importing multiple files, enter the source file URI and name in the following format `s3://[bucket_name]/[data_source_folder]/`. For example, `s3://sampledata/ingest/`.
    - **Bucket Access**: you can use either an AWS Role ARN or an AWS access key to access your bucket. For more information, see [Configure Amazon S3 access](/tidb-cloud/config-s3-and-gcs-access.md#configure-amazon-s3-access).
        - **AWS Role ARN**: enter the AWS Role ARN value.
        - **AWS Access Key**: enter the AWS access key ID and AWS secret access key.

4. Click **Connect**.

5. In the **Destination** section, select the target database and table.

    When importing multiple files, you can use **Advanced Settings** > **Mapping Settings** to define a custom mapping rule for each target table and its corresponding Parquet file. After that, the data source files will be re-scanned using the provided custom mapping rule.

    When you enter the source file URI and name in **Source File URIs and Names**, make sure it is in the following format `s3://[bucket_name]/[data_source_folder]/[file_name].parquet`. For example, `s3://sampledata/ingest/TableName.01.parquet`.

    You can also use wildcards to match the source files. For example:

    - `s3://[bucket_name]/[data_source_folder]/my-data?.parquet`: all Parquet files starting with `my-data` followed by one character (such as `my-data1.parquet` and `my-data2.parquet`) in that folder will be imported into the same target table.

    - `s3://[bucket_name]/[data_source_folder]/my-data*.parquet`: all Parquet files in the folder starting with `my-data` will be imported into the same target table.

    Note that only `?` and `*` are supported.

    > **Note:**
    >
    > The URI must contain the data source folder.

6. Click **Start Import**.

7. When the import progress shows **Completed**, check the imported tables.

</div>

<div label="Google Cloud">

1. Open the **Import** page for your target cluster.

    1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.

        > **Tip:**
        >
        > If you have multiple projects, you can click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner and switch to another project.

    2. Click the name of your target cluster to go to its overview page, and then click **Import** in the left navigation pane.

2. Click **Import Data** in the upper-right corner.

    If this is your first time importing data into this cluster, select **Import From GCS**.

3. On the **Import Data from GCS** page, provide the following information for the source Parquet files:

    - **Import File Count**: select **One file** or **Multiple files** as needed.
    - **Included Schema Files**: this field is only visible when importing multiple files. If the source folder contains the target table schemas, select **Yes**. Otherwise, select **No**.
    - **Data Format**: select **Parquet**.
    - **File URI** or **Folder URI**:
        - When importing one file, enter the source file URI and name in the following format `gs://[bucket_name]/[data_source_folder]/[file_name].parquet`. For example, `gs://sampledata/ingest/TableName.01.parquet`.
        - When importing multiple files, enter the source file URI and name in the following format `gs://[bucket_name]/[data_source_folder]/`. For example, `gs://sampledata/ingest/`.
    - **Bucket Access**: you can use a GCS IAM Role to access your bucket. For more information, see [Configure GCS access](/tidb-cloud/config-s3-and-gcs-access.md#configure-gcs-access).

4. Click **Connect**.

5. In the **Destination** section, select the target database and table.

    When importing multiple files, you can use **Advanced Settings** > **Mapping Settings** to define a custom mapping rule for each target table and its corresponding Parquet file. After that, the data source files will be re-scanned using the provided custom mapping rule.

    When you enter the source file URI and name in **Source File URIs and Names**, make sure it is in the following format `gs://[bucket_name]/[data_source_folder]/[file_name].parquet`. For example, `gs://sampledata/ingest/TableName.01.parquet`.

    You can also use wildcards to match the source files. For example:

    - `gs://[bucket_name]/[data_source_folder]/my-data?.parquet`: all Parquet files starting with `my-data` followed by one character (such as `my-data1.parquet` and `my-data2.parquet`) in that folder will be imported into the same target table.

    - `gs://[bucket_name]/[data_source_folder]/my-data*.parquet`: all Parquet files in the folder starting with `my-data` will be imported into the same target table.

    Note that only `?` and `*` are supported.

    > **Note:**
    >
    > The URI must contain the data source folder.

6. Click **Start Import**.

7. When the import progress shows **Completed**, check the imported tables.

</div>

</SimpleTab>

When you run an import task, if any unsupported or invalid conversions are detected, TiDB Cloud terminates the import job automatically and reports an importing error.

If you get an importing error, do the following:

1. Drop the partially imported table.
2. Check the table schema file. If there are any errors, correct the table schema file.
3. Check the data types in the Parquet files.

    If the Parquet files contain any unsupported data types (for example, `NEST STRUCT`, `ARRAY`, or `MAP`), you need to regenerate the Parquet files using [supported data types](#supported-data-types) (for example, `STRING`).

4. Try the import task again.

## Supported data types

The following table lists the supported Parquet data types that can be imported to TiDB Cloud.

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
