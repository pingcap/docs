---
title: Connect via SQL Shell
summary: Learn how to connect to your TiDB cluster via SQL Shell.
---

# Connect via SQL Shell

In TiDB Cloud SQL Shell, you can try TiDB SQL, test out TiDB's compatibility with MySQL quickly, and administer database user privileges.

> **Note:**
>
> You cannot connect to [{{{ .starter }}}](/tidb-cloud/select-cluster-tier.md#starter) or [{{{ .essential }}}](/tidb-cloud/select-cluster-tier.md#essential) using SQL Shell. To connect to your {{{ .starter }}} or {{{ .essential }}} instance, see [Connect to {{{ .starter }}} or Essential Instance](/tidb-cloud/connect-to-tidb-cluster-serverless.md).

To Connect to TiDB using SQL shell, perform the following steps:

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page.

    > **Tip:**
    >
    > If you are in multiple organizations, use the combo box in the upper-left corner to switch to your target organization first.

2. Click the name of your target TiDB Cloud Dedicated cluster to go to its overview page, and then click **Settings** > **Networking** in the left navigation pane.
3. On the **Networking** page, click **Web SQL Shell** in the upper-right corner.
4. On the prompted **Enter password** line, enter the root password of the current cluster. Then your application is connected to the TiDB cluster.