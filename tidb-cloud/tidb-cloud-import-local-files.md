---
title: Import Local Files to TiDB Cloud
summary: Learn how to import local files to TiDB Cloud.
---

# Import Local Files to TiDB Cloud

You can import local files to TiDB Cloud directly. It only takes a few seconds to complete the task configuration, and then the data will be imported to TiDB immediately. You no longer need to configure the cloud storage bucket path, ARN Role authorization or other complicated operations. Importing data to TiDB Cloud is quick and smooth.

This feature now supports the following:

- Importing one CSV file within 50 MiB for one task into an existing table or a new table
- Only Serverless Tier clusters

## Prerequisites

- Prepare the local file to be imported. The file must be in CSV format within 50 MiB.
- If you import a CSV file into an existing table in TiDB Cloud, make sure that the order of the columns in the CSV file is the same as that in the target table.

## Import local files

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/console/clusters), and choose your target project on the top of the left navigation bar.

2. Locate your target cluster, click **...** in the upper-right corner of the cluster area, and select **Import Data**.

3. On the **Import** page, click **Import Data** in the upper-right corner, and then select **From local**.

4. Click **Upload File** to select and upload the local file. Note that the file name must have a ".csv" suffix and must be no more than 50 MiB.

5. In the **Target Cluster** section, select the target database and the target table, or create a new database or new table. Then click **Next**.

    To create a new database or a new table, click **+ Create a new database** or **+ Create a new table**, directly enter a database name or a table name to create one, as shown in the following screenshot. TiDB Cloud will automatically create the database and the table according to the CSV data and the configured column name. The name must start with letters (a-z and A-Z), and can contain numbers (0-9), letters (a-z and A-Z), the underscore (_), and the hyphen (-) characters.

    ![Upload local files](/media/tidb-cloud/tidb-cloud-upload-local-files.png)

6. Configure the table.

    Here you can see a list of configurable table columns. Each line shows the table column name (if it can be inferred by TiDB Cloud), the table column type inferred, and the previewed data from the CSV file.

    - If you import data into an existing table, the column list is extracted from the table definition, and the previewed data is mapped to the corresponding columns by column names.

    - If you want to create a new table, the column list is extracted from the CSV file, and the column type is inferred by TiDB Cloud. For example, if the previewed data is all integers, the inferred column type will be **int** (integer).

    - If your first row in the CSV file is column names, make sure that **Use the first row as Column Name** is selected, which is selected by default.

    - If the CSV file has no columns, do not select **Use the first row as Column Name**. In this case:
        * If the table is not created, input the names for each column. The name must start with letters (a-z and A-Z), and can contain numbers (0-9), letters (a-z and A-Z), the underscore (_), and the hyphen (-) characters.
        * If the table already exists, make sure the order of the columns is the same as the column list of the target table.

    To edit the CSV configuration for more fine-grained control, you can also click **Edit CSV configuration**. For more information about the CSV configuration, see [CSV Configurations for Importing Data](/tidb-cloud/csv-config-for-import-data.md).

    For a new table, you can change the column names and data types.

    Click **Next**.

7. Click **Start Import**.

    You can view the import progress in the **Import Progress** section. If there are warnings or failed tasks, you can check to view the details and solve them.
