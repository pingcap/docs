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
- Use [SQL Editor](/develop/dev-guide-tidb-crud-sql.md#explore-sql-with-tidb) to create a table in the target database in advance. The table schema must be consistent with the local file. Alternatively, you can enter the table name in the import task and let TiDB Cloud help you automatically create the target table.

## Import local files

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/console/clusters), and choose your target project on the top of the left navigation bar.

2. Locate your target cluster, click ... in the upper-right corner of the cluster area, and select **Import Data**.

3. On the **Import** page, click the **Import Data** button in the upper-right corner, and then select **From local**.

4. Click the **Upload File** button to select and upload the local file. One task only supports uploading one CSV file within 50 MiB.

5. In the **Target Cluster** section, select the target database and the target table. If the database or the table does not exist yet, you can directly enter a database name or a table name to create one, as shown in the following screenshot. Click **Next**.

    ![Upload local files](/media/tidb-cloud/tidb-cloud-upload-local-files.png)

6. Configure the table.

    If you want to use the first row the CSV file as the column names, select **Use the first row as Column Name**. You can click **Edit CSV configuration** to edit the CSV configuration. For more information about the CSV configuration, see [CSV Configurations for Importing Data](/tidb-cloud/csv-config-for-import-data.md).

    If you want to let TiDB Cloud create the table for you, you can change the column names and data types here.

    Click **Next**.

7. Click **Start Import**. You can view the import progress on the **Import Progress** section. If there are warnings or failed tasks, you can check to view the details and solve them.
