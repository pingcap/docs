---
title: Upload Local Files to TiDB Cloud
summary: Learn how to upload local files to TiDB Cloud.
---

# Upload Local Files to TiDB Cloud

You can upload local files to TiDB Cloud directly. You only need to select the local file, select the the target cluster, and directly import the data after the validation is passed.

This feature now supports the following:

- Uploading one CSV file within 50 MiB for one task
- Serverless Tier clusters

## Upload local files

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/console/clusters), and choose your target project on the top of the left navigation bar.

2. Locate your target cluster, click ... in the upper-right corner of the cluster area, and select **Import Data**.

3. Click **Import Data** in the upper-right corner of the page, and then select **From local**.

4. Click the **Upload File** button to select and upload the local file. One task only supports uploading one file within 50 MiB.

5. In the **Target Cluster** section, select the target database and the target table. Click **Next**.

6. Configure the table schema. If you want to use the first row as the column names, select **Use the first row as Column Name**. You can click **Edit CSV configuration** to edit the CSV configuration. For more information about the CSV configuration, see [CSV Configurations for Importing Data](/tidb-cloud/naming-conventions-for-data-import.md).

7. Click **Start Import**. You can view the import progress on the **Import Progress** section. If there are warnings or failed tasks, you can check to view the details and solve them.
