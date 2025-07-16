---
title: Connect via SQL Shell
summary: Learn how to connect to your TiDB cluster via SQL Shell.
---

# Connect via SQL Shell

In TiDB Cloud SQL Shell, you can try TiDB SQL, test out TiDB's compatibility with MySQL quickly, and administer database user privileges.

> **Note:**
>
> You cannot connect to [TiDB Cloud Serverless clusters](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) using SQL Shell. To connect to your TiDB Cloud Serverless cluster, see [Connect to TiDB Cloud Serverless clusters](/tidb-cloud/connect-to-tidb-cluster-serverless.md).

To connect to your TiDB cluster using SQL shell, perform the following steps:

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations, projects, and clusters.

2. Click the name of your target cluster to go to its cluster overview page, and then click **Settings** > **Networking** in the left navigation pane.
3. On the **Networking** page, click **Web SQL Shell** in the upper-right corner.
4. On the prompted **Enter password** line, enter the root password of the current cluster. Then your application is connected to the TiDB cluster.