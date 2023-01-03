---
title: Connect via SQL Shell
summary: Learn how to connect to your TiDB cluster via SQL Shell.
---

# Connect via SQL Shell

In TiDB Cloud SQL Shell, you can try TiDB SQL, test out TiDB's compatibility with MySQL quickly, and administer database user privileges.

> **Note:**
>
> You cannot connect to [Serverless Tier clusters](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta) using SQL Shell. To connect to your Serverless Tier cluster, see [Connect to Serverless Tier clusters](/tidb-cloud/connect-to-tidb-cluster.md#serverless-tier).

To connect to your TiDB cluster using SQL shell, perform the following steps:

1. Open the overview page of the target cluster.

    1. Log in to the [TiDB Cloud console](https://tidbcloud.com/).
    2. If you have multiple projects, choose a target project in the left navigation pane. Otherwise, skip this step.
    3. In the row of your target cluster, click the cluster name.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. In the dialog, select the **Web SQL Shell** tab, and then click **Open SQL Shell**.

4. On the prompted **Enter password** line, enter the root password of the current cluster. Then your application is connected to the TiDB cluster.