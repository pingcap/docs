---
title: Import Local Files to TiDB Cloud
summary: Learn how to import local files to TiDB Cloud.
---

# Import Local Files to TiDB Cloud

You can import local files to TiDB Cloud directly. You only need to select a local file, select the target cluster and table, make changes if needed, and then directly import the data into TiDB Cloud.

This feature now supports the following:

- Importing one CSV file within 50 MiB for one task
- Only Serverless Tier clusters

## Prerequisites

- Prepare the local file to be imported. The file must be in CSV format within 50 MiB.
- You can import the CSV file into an existing table or into a new table. If you import the CSV file into an existing table, make sure that the order of the columns in the CSV file is the same as that in the target table.

## Import local files

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/console/clusters), and choose your target project on the top of the left navigation bar.

2. Locate your target cluster, click ... in the upper-right corner of the cluster area, and select **Import Data**.

3. On the **Import** page, click the **Import Data** button in the upper-right corner, and then select **From local**.

4. Click the **Upload File** button to select and upload the local file. Note that the file name must have a “.csv” suffix and must be less than 50 MiB.

5. In the **Target Cluster** section, select the target database and the target table. If you want to import the data into an existing table, choose the database name and table name in the drop-down list. If you want to create a new database or a new table, you can directly enter a database name or a table name to create one, as shown in the following screenshot. TiDB Cloud will automatically create the database and the table according to the CSV data and the configured column name. Click **Next**.

    ![Upload local files](/media/tidb-cloud/tidb-cloud-upload-local-files.png)

6. Configure the table.
Here you can see a list of possible columns and configure it. Each row shows the column name (if it can be inferred by TiDB Cloud), the column type inferred, and the previewed data from the CSV file.  

If you import the data into an existing table, the column list is extracted from the table definition, and the previewed data is mapped to the corresponding columns by column names. If a new table will be created, the column list is extracted from the CSV file, and the column type is inferred by TiDB Cloud. For example, if the previewed data is all integers, the inferred column type will be **int** (integer).
    If your first row in the CSV file is column names, select **Use the first row as Column Name**, which is selected by default. If the CSV file has no columns, do not select **Use the first row as Column Name**. In this case: 
    * If the table needs to be created, you need to input the names for each column.
    * If the table already exists, you need to make sure the order of the columns is the same as the column list of the target table.
    You can also click **Edit CSV configuration** to edit the CSV configuration for more fine-grained control. For more information about the CSV configuration, see [CSV Configurations for Importing Data](/tidb-cloud/csv-config-for-import-data.md).

    If you want to let TiDB Cloud create the table for you, you can change the column names and data types here.

    Click **Next**.

7. Click **Start Import**. You can view the import progress on the **Import Progress** section. If there are warnings or failed tasks, you can check to view the details and solve them.
