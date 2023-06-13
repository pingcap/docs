---
title: Import CSV Files from Amazon S3 or GCS into TiDB Cloud
summary: Learn how to import CSV files from Amazon S3 or GCS into TiDB Cloud.
---

# Import CSV Files from Amazon S3 or GCS into TiDB Cloud

This document describes how to import CSV files from Amazon Simple Storage Service (Amazon S3) or Google Cloud Storage (GCS) into TiDB Cloud.

> **Note:**
>
> - To ensure data consistency, TiDB Cloud allows to import CSV files into empty tables only. To import data into an existing table that already contains data, you can use TiDB Cloud to import the data into a temporary empty table by following this document, and then use the `INSERT SELECT` statement to copy the data to the target existing table.
> - If there is a changefeed in a TiDB Dedicated cluster, you cannot import data to the cluster (the **Import Data** button will be disabled), because the current import data feature uses the [physical import mode](https://docs.pingcap.com/tidb/stable/tidb-lightning-physical-import-mode). In this mode, the imported data does not generate change logs, so the changefeed cannot detect the imported data.

## Step 1. Prepare the CSV files

1. If a CSV file is larger than 256 MB, consider splitting it into smaller files, each with a size around 256 MB.

    TiDB Cloud supports importing very large CSV files but performs best with multiple input files around 256 MB in size. This is because TiDB Cloud can process multiple files in parallel, which can greatly improve the import speed.

2. Name the CSV files as follows:

    - If a CSV file contains all data of an entire table, name the file in the `${db_name}.${table_name}.csv` format, which maps to the `${db_name}.${table_name}` table when you import the data.
    - If the data of one table is separated into multiple CSV files, append a numeric suffix to these CSV files. For example, `${db_name}.${table_name}.000001.csv` and `${db_name}.${table_name}.000002.csv`. The numeric suffixes can be inconsecutive but must be in ascending order. You also need to add extra zeros before the number to ensure all the suffixes are in the same length.
    - TiDB Cloud supports importing compressed files in the following formats: `.gzip`, `.gz`, `.zstd`, `.zst` and `.snappy`. If you want to import compressed CSV files, name the files in the `${db_name}.${table_name}.${suffix}.csv.${compress}` format, in which `${suffix}` is optional and can be any integer such as '000001'. For example, if you want to import the `trips.000001.csv.gz` file to the `bikeshare.trips` table, you need to rename the file as `bikeshare.trips.000001.csv.gz`.

    > **Note:**
    >
    > - You only need to compress the data files, not the database or table schema files.
    > - To achieve better performance, it is recommended to limit the size of each compressed file to 100 MiB.
    > - For uncompressed files, if you cannot update the CSV filenames according to the preceding rules in some cases (for example, the CSV file links are also used by your other programs), you can keep the filenames unchanged and use the **File Pattern** in [Step 4](#step-4-import-csv-files-to-tidb-cloud) to import your source data to a single target table.

## Step 2. Create the target table schemas

Because CSV files do not contain schema information, before importing data from CSV files into TiDB Cloud, you need to create the table schemas using either of the following methods:

- Method 1: In TiDB Cloud, create the target databases and tables for your source data.

- Method 2: In the Amazon S3 or GCS directory where the CSV files are located, create the target table schema files for your source data as follows:

    1. Create database schema files for your source data.

        If your CSV files follow the naming rules in [Step 1](#step-1-prepare-the-csv-files), the database schema files are optional for the data import. Otherwise, the database schema files are mandatory.

        Each database schema file must be in the `${db_name}-schema-create.sql` format and contain a `CREATE DATABASE` DDL statement. With this file, TiDB Cloud will create the `${db_name}` database to store your data when you import the data.

        For example, if you create a `mydb-scehma-create.sql` file that contains the following statement, TiDB Cloud will create the `mydb` database when you import the data.

        {{< copyable "sql" >}}

        ```sql
        CREATE DATABASE mydb;
        ```

    2. Create table schema files for your source data.

        If you do not include the table schema files in the Amazon S3 or GCS directory where the CSV files are located, TiDB Cloud will not create the corresponding tables for you when you import the data.

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

To allow TiDB Cloud to access the CSV files in the Amazon S3 or GCS bucket, do one of the following:

- If your CSV files are located in Amazon S3, [configure Amazon S3 access](/tidb-cloud/config-s3-and-gcs-access.md#configure-amazon-s3-access).

    You can use either an AWS access key or a Role ARN to access your bucket. Once finished, make a note of the access key (including the access key ID and secret access key) or the Role ARN value as you will need it in [Step 4](#step-4-import-csv-files-to-tidb-cloud).

- If your CSV files are located in GCS, [configure GCS access](/tidb-cloud/config-s3-and-gcs-access.md#configure-gcs-access).

## Step 4. Import CSV files to TiDB Cloud

To import the CSV files to TiDB Cloud, take the following steps:

1. Open the **Import** page for your target cluster.

    1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.

        > **Tip:**
        >
        > If you have multiple projects, you can view the project list and switch to another project from the ☰ hover menu in the upper-left corner.

    2. Click the name of your target cluster to go to its overview page, and then click **Import** in the left navigation pane.

2. On the **Import** page:
   - For a TiDB Dedicated cluster, click **Import Data** in the upper-right corner.
   - For a TiDB Serverless cluster, click the **import data from S3** link above the upload area.

3. Provide the following information for the source CSV files:

    - **Data Format**: select **CSV**.
    - **Bucket URI**: select the bucket URI where your CSV files are located.
    - **Bucket Access** (This field is visible only for AWS S3): you can use either an AWS access key or an AWS Role ARN to access your bucket. For more information, see [Configure Amazon S3 access](/tidb-cloud/config-s3-and-gcs-access.md#configure-amazon-s3-access).
        - **AWS Access Keys**: enter the AWS access key ID and AWS secret access key.
        - **AWS Role ARN**: enter the AWS Role ARN value.

4. If you want to modify the file patterns, click **Advanced Settings** and then click **Mapping Settings**.

    > **Note:**
    >
    > When you use this feature, one import task can only import data to a single table at a time. If you want to use this feature to import data into different tables, you need to import several times, each time specifying a different target table.

    To modify the file pattern, specify a custom mapping rule between CSV files and a single target table in the following fields, and then click **Submit**. After that, the data source files will be re-scanned using the provided custom mapping rule.

    - **Target Database**: enter the name of the target database in TiDB Cloud.

    - **Target Tables**: enter the name of the target table in TiDB Cloud. Note that this field only accepts one specific table name, so wildcards are not supported.

    - **Source file URIs and names**: enter the source file URI and name, for example, `s3://sampledate/ingest/TableName.01.csv`.

5. Click **Next**. If you see a warning message, resolve this by providing the correct source file, renaming the existing one according to [Naming Conventions for Data Import](/tidb-cloud/naming-conventions-for-data-import.md), or using **Advanced settings** to make changes. After that, click **Ignore warning and preview**.

6. On the **Preview** page, you can have a preview of the data. If the previewed data is not what you expect, click the **Click here to edit csv configuration** link to update the CSV-specific configurations, including separator, delimiter, header, `backslash escape`, and `trim last separator`. For more information, see [CSV Configurations for Importing Data](/tidb-cloud/csv-config-for-import-data.md).

    > **Note:**
    >
    > For the configurations of separator and delimiter, you can use both alphanumeric characters and certain special characters. The supported special characters include `\t`, `\b`, `\n`, `\r`, `\f`, and `\u0001`.

7. Click **Start Import**.

8. When the import progress shows **Finished**, check the imported tables.

    If the number is zero, it means no data files matched the value you entered in the **Source file name** field. In this case, ensure that there are no typos in the **Source file name** field and try again.

9. After the import task is completed, you can click **Chat2Qury** in the left navigation pane to query your imported data. For more information about how to use Chat2Qury, see [Explore Your Data with AI-Powered Chat2Query](/tidb-cloud/explore-data-with-chat2query.md).

When you run an import task, if any unsupported or invalid conversions are detected, TiDB Cloud terminates the import job automatically and reports an importing error.

If you get an importing error, do the following:

1. Drop the partially imported table.
2. Check the table schema file. If there are any errors, correct the table schema file.
3. Check the data types in the CSV files.
4. Try the import task again.
