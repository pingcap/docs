---
title: Upload Local Files to TiDB Cloud
summary: Learn how to upload local files to TiDB Cloud.
---

# Upload Local Files to TiDB Cloud

You can upload local files to TiDB Cloud directly. You only need to select the local file, select the the target cluster, and directly import the data after the validation is passed.

This feature now supports the following:

- Uploading one CSV file within 50 MiB for one task
- Both Serverless Tier and Dedicated Tier clusters

## Upload local files

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/console/clusters), and choose your target project on the top of the left navigation bar.

2. Locate your target cluster, click ... in the upper-right corner of the cluster area, and select **Data Replication**.

3. Click the **Import** tab, and then click **Create Import Task** in the upper-right corner of the page. The **Create Import Task** page is displayed.

4. In the **Task Name**, create a task name.

5. In the **Source** section, click **Local**. Select **CSV** as the data format.

6. Click **Click to upload** button to select the local file. One task only supports uploading one file within 50 MiB.

7. In the **Target** section, select the target database and the target table. Click **Next**.

8. On the **Define Table** page, you can define the table schema.