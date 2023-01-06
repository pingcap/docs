---
title: Import Local Files to TiDB Cloud
summary: Learn how to import local files to TiDB Cloud.
---

# Import Local Files to TiDB Cloud

You can import local files to TiDB Cloud directly. It only takes a few clicks to complete the task configuration, and then your local CSV data will be quickly imported to your TiDB cluster. Using this method, you do not need to provide the cloud storage bucket path and Role ARN. The whole importing process is quick and smooth.

Currently, this method supports importing one CSV file for one task into either an existing table or a new table.

## Limitations

- Currently, TiDB Cloud only supports importing a local file in CSV format within 50 MiB for one task.
- Importing local files is supported only for Serverless Tier clusters, not for Dedicated Tier clusters.
- You cannot run more than one import task at the same time.
- If you import a CSV file into an existing table in TiDB Cloud, make sure that the first line of the CSV file contains the column names, and the order of the columns in the CSV file must be the same as that in the target table.

## Import local files

1. Open the **Import** page for your target cluster.

    1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.

        > **Tip:**
        >
        > If you have multiple projects, you can switch to the target project in the left navigation pane of the **Clusters** page.

    2. Click the name of your target cluster to go to its overview page, and then click **Import** in the left navigation pane.

2. On the **Import** page, click **Import Data** in the upper-right corner, and then select **From local file**.

3. Click **Upload File** to select and upload the target local file. Note that the file name must have a ".csv" extension and must be no more than 50 MiB.

4. In the **Target** section, select the target database and the target table, or create a new database or new table. Then click **Next**.

    To create a new database or a new table, click **+ Create a new database** or **+ Create a new table**, directly enter a database name or a table name to create one, as shown in the following screenshot. TiDB Cloud will automatically create the database and the table according to the CSV data and the configured column name. The name must start with letters (a-z and A-Z) or numbers (0-9), and can contain letters (a-z and A-Z), numbers (0-9), and the underscore (_) characters.

    ![Upload local files](/media/tidb-cloud/tidb-cloud-upload-local-files-new.png)

5. Check the table.

    Here you can see a list of configurable table columns. Each line shows the table column name inferred by TiDB Cloud, the table column type inferred, and the previewed data from the CSV file.

    - If you import data into an existing table in TiDB Cloud, the column list is extracted from the table definition, and the previewed data is mapped to the corresponding columns by column names.

    - If you want to create a new table, the column list is extracted from the CSV file, and the column type is inferred by TiDB Cloud. For example, if the previewed data is all integers, the inferred column type will be **int** (integer).

6. Configure the column names and data types.

    If the first row in the CSV file records the column names, make sure that **Use the first row as Column Name** is selected, which is selected by default.

    If the CSV file does not have a row for the column names, do not select **Use the first row as Column Name**. In this case:

    - If the CSV table already exists, make sure the order of the columns is the same as the column list of the target table.

    - If the CSV table is not created yet, input the names for each column. The column name must start with letters (a-z and A-Z) or numbers (0-9), and can contain letters (a-z and A-Z), numbers (0-9), and the underscore (_) characters. You can also change the data type if needed.

7. Edit the CSV configuration if needed.

   To edit the CSV configuration for more fine-grained control, you can also click **Edit CSV configuration**. For more information about the CSV configuration, see [CSV Configurations for Importing Data](/tidb-cloud/csv-config-for-import-data.md).

8. Click **Start Import**.

    You can view the import progress in the **Import Progress** section. If there are warnings or failed tasks, you can check to view the details and solve them.

9. After the data import task is complete, on the **Import Task Details** page, you can click **Query Data** in the upper-right corner, and then use [**Chat2Query**](/tidb-cloud/tidb-cloud-quickstart.md#step-2-try-chat2query-beta) to write SQL statements to query the imported data. 
