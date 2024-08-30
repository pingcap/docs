---
title: Connect to TiDB Serverless via Public Endpoint
summary: Learn how to connect to your TiDB Serverless cluster via public endpoint.
---

# Connect to TiDB Serverless via Public Endpoint

This document describes how to connect to your TiDB Serverless cluster via a public endpoint, using a SQL client from your computer, as well as how to disable a public endpoint.

## Connect via a public endpoint

> **Tip:**
>
> To learn how to connect to a TiDB Dedicated cluster via public endpoint, see [Connect to TiDB Dedicated via Public Connection](/tidb-cloud/connect-via-standard-connection.md).

To connect to a TiDB Serverless cluster via public endpoint, take the following steps:

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. In the dialog, keep the default setting of the endpoint type as `Public`, and select your preferred connection method and operating system to get the corresponding connection string.

    > **Note:**
    >
    > - Keeping the endpoint type as `Public` means the connection is via standard TLS connection. For more information, see [TLS Connection to TiDB Serverless](/tidb-cloud/secure-connections-to-serverless-clusters.md).
    > - If you choose **Private** in the **Endpoint Type** drop-down list, it means that the connection is via private endpoint. For more information, see [Connect to TiDB Serverless via Private Endpoint](/tidb-cloud/set-up-private-endpoint-connections-serverless.md).

4. TiDB Serverless lets you create [branches](/tidb-cloud/branch-overview.md) for your cluster. After a branch is created, you can choose to connect to the branch via the **Branch** drop-down list. `main` represents the cluster itself.

5. If you have not set a password yet, click **Generate Password** to generate a random password. The generated password will not show again, so save your password in a secure location.

6. Connect to your cluster with the connection string.

    > **Note:**
    >
    > When you connect to a TiDB Serverless cluster, you must include the prefix for your cluster in the user name and wrap the name with quotation marks. For more information, see [User name prefix](/tidb-cloud/select-cluster-tier.md#user-name-prefix).

## Disable a public endpoint

If you do not need to use a public endpoint of a TiDB Serverless cluster, you can disable it to prevent connections from the internet:

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Networking** in the left navigation pane and click **Disable** in the right pane. A confirmation dialog is displayed.

3. Click **Disable** in the confirmation dialog.

After disabling the public endpoint, the `Public` entry in the **Endpoint Type** drop-down list of the connect dialog is disabled. If users are still trying to access the cluster from the public endpoint, they will get an error.

> **Note:**
>
> Disabling the public endpoint does not affect existing connections. It only prevents new connections from the internet.

You can re-enable the public endpoint after disabling it:

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Networking** in the left navigation pane and click **Enable** in the right pane.

## What's next

After you have successfully connected to your TiDB cluster, you can [explore SQL statements with TiDB](/basic-sql-operations.md).
