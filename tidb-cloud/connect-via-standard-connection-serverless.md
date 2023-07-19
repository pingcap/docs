---
title: Connect to TiDB Serverless via Public Endpoint
summary: Learn how to connect to your TiDB Serverless cluster via public endpoint.
---

# Connect to TiDB Serverless via Public Endpoint

This document describes how to connect to your TiDB Serverless cluster via public endpoint. With the public endpoint, you can connect to your TiDB Serverless cluster via a SQL client from your laptop.

> **Tip:**
>
> To learn how to connect to a TiDB Dedicated cluster via public endpoint, see [Connect to TiDB Dedicated via Standard Connection](/tidb-cloud/connect-via-standard-connection.md).

To connect to a TiDB Serverless cluster via public endpoint, take the following steps:

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. In the dialog, keep the default setting of the endpoint type as `Public`, and select your preferred connection method and operating system to get the corresponding connection string.

    > **Note:**
    >
    > - Keeping the endpoint type as `Public` means the connection is via standard TLS connection. For more information, see [TLS Connection to TiDB Serverless](/tidb-cloud/secure-connections-to-serverless-clusters.md).
    > - If you choose **Private** in the **Endpoint Type** drop-down list, it means that the connection is via private endpoint. For more information, see [Connect to TiDB Serverless via Private Endpoint](/tidb-cloud/set-up-private-endpoint-connections-serverless.md).

4. If you have not set a password yet, click **Create password** to generate a random password. The generated password will not show again, so save your password in a secure location.

5. Connect to your cluster with the connection string.

    > **Note:**
    >
    > When you connect to a TiDB Serverless cluster, you must include the prefix for your cluster in the user name and wrap the name with quotation marks. For more information, see [User name prefix](/tidb-cloud/select-cluster-tier.md#user-name-prefix).

## Obtain TiDB Serverless Connection Parameters

In the connection dialog, you can obtaining the connection parameters follow these instractions. If you don't know how to enter the connection dialog, please go back to the [top of this document](#connect-to-tidb-serverless-via-public-endpoint) to get more information.

1. Select the **General** tab in the **Connect With** item.

2. Select the operating system you want in the **Operating System** selector. This selection will affect the value of `ssl_ca`.

3. You can get `host`, `port`, `user`, `password`, and `ssl_ca` here.

## What's next

After you have successfully connected to your TiDB cluster, you can [explore SQL statements with TiDB](/basic-sql-operations.md).
