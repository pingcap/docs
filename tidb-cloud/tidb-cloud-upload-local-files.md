---
title: Upload Local Files to TiDB Cloud
summary: Learn how to upload local files to TiDB Cloud.
---

# Upload Local Files to TiDB Cloud

You can upload local files to TiDB Cloud directly. You only need to select the local file, select the the target cluster, and directly import the data after the validation is passed.

This feature now supports the following:

- Uploading one CSV file within 50 MiB for one task
- Only Serverless Tier clusters

## Prerequisites

- Prepare the local file to be uploaded. The file must be in CSV format within 50 MiB.
- Use [SQL Editor](/develop/dev-guide-tidb-crud-sql.md#explore-sql-with-tidb) to create a table in the target database. The table schema must be consistent with the local file. Alternatively, you can create a table when filling in the import task.

## Upload local files

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/console/clusters), and choose your target project on the top of the left navigation bar.

2. Locate your target cluster, click ... in the upper-right corner of the cluster area, and select **Import Data**.

3. On the **Import** page, click the **Import Data** button in the upper-right corner, and then select **From local**.

4. Click the **Upload File** button to select and upload the local file. One task only supports uploading one file within 50 MiB.

5. In the **Target Cluster** section, select the target database and the target table. If the table does not exist yet, you can directly enter a table to create one, as shown in the following screenshot. Click **Next**.

    ![Upload local files](/media/tidb-cloud/tidb-cloud-upload-local-files.png)

6. Configure the table schema.

    If you want to use the first row as the column names, select **Use the first row as Column Name**. You can click **Edit CSV configuration** to edit the CSV configuration. For more information about the CSV configuration, see [CSV Configurations for Importing Data](/tidb-cloud/naming-conventions-for-data-import.md).

    If your table is newly created on the previous step, you can change the column names and data types here.

    Click **Next**.

7. Click **Start Import**. You can view the import progress on the **Import Progress** section. If there are warnings or failed tasks, you can check to view the details and solve them.

If you encouter any problems, you can solve them according to the error messages.
