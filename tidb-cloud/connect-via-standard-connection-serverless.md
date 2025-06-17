---
title: Connect to TiDB Cloud Serverless via Public Endpoint
summary: Learn how to connect to your TiDB Cloud Serverless cluster via public endpoint.
---

# Connect to TiDB Cloud Serverless via Public Endpoint

This document describes how to connect to your TiDB Cloud Serverless cluster via a public endpoint, using a SQL client from your computer, as well as how to disable a public endpoint.

## Connect via a public endpoint

> **Tip:**
>
> To learn how to connect to a TiDB Cloud Dedicated cluster via public endpoint, see [Connect to TiDB Cloud Dedicated via Public Connection](/tidb-cloud/connect-via-standard-connection.md).

To connect to a TiDB Cloud Serverless cluster via public endpoint, take the following steps:

1. Navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. In the dialog, keep the default setting of the connection type as `Public`, and select your preferred connection method and operating system to get the corresponding connection string.

    > **Note:**
    >
    > - Keeping the connection type as `Public` means the connection is via standard TLS connection. For more information, see [TLS Connection to TiDB Cloud Serverless](/tidb-cloud/secure-connections-to-serverless-clusters.md).
    > - If you choose **Private Endpoint** in the **Connection Type** drop-down list, it means that the connection is via private endpoint. For more information, see [Connect to TiDB Cloud Serverless via Private Endpoint](/tidb-cloud/set-up-private-endpoint-connections-serverless.md).

4. TiDB Cloud Serverless lets you create [branches](/tidb-cloud/branch-overview.md) for your cluster. After a branch is created, you can choose to connect to the branch via the **Branch** drop-down list. `main` represents the cluster itself.

5. If you have not set a password yet, click **Generate Password** to generate a random password. The generated password will not show again, so save your password in a secure location.

6. Connect to your cluster with the connection string.

    > **Note:**
    >
    > When you connect to a TiDB Cloud Serverless cluster, you must include the prefix for your cluster in the user name and wrap the name with quotation marks. For more information, see [User name prefix](/tidb-cloud/select-cluster-tier.md#user-name-prefix).
    > Your client IP must be in the allowed IP rules of the public endpoint of your cluster. For more information, see [Configure TiDB Cloud Serverless Firewall Rules for Public Endpoints](/tidb-cloud/configure-serverless-firewall-rules-for-public-endpoints.md).

## Disable a public endpoint

If you do not need to use a public endpoint of a TiDB Cloud Serverless cluster, you can disable it to prevent connections from the internet:

1. Navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page, and then click the name of your target cluster to go to its overview page.

2. In the left navigation pane, click **Settings** > **Networking**.

3. On the **Networking** page, click **Disable**. A confirmation dialog is displayed.

4. Click **Disable** in the confirmation dialog.

After disabling the public endpoint, the `Public` entry in the **Connection Type** drop-down list of the connect dialog is disabled. If users are still trying to access the cluster from the public endpoint, they will get an error.

> **Note:**
>
> Disabling the public endpoint does not affect existing connections. It only prevents new connections from the internet.

You can re-enable the public endpoint after disabling it:

1. Navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page, and then click the name of your target cluster to go to its overview page.

2. In the left navigation pane, click **Settings** > **Networking**.

3. On the **Networking** page, click **Enable**.

## What's next

After you have successfully connected to your TiDB cluster, you can [explore SQL statements with TiDB](/basic-sql-operations.md).
