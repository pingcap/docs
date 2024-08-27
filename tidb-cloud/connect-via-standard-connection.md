---
title: Connect to TiDB Dedicated via Standard Connection
summary: Learn how to connect to your TiDB Cloud cluster via standard connection.
---

# Connect to TiDB Dedicated via Public Connection

This document describes how to connect to your TiDB Dedicated cluster via public connection. The public connection exposes a public endpoint with traffic filters, so you can connect to your TiDB Dedicated cluster via a SQL client from your laptop.

> **Tip:**
>
> To learn how to connect to a TiDB Serverless cluster via public connection, see [Connect to TiDB Serverless via Public Endpoint](/tidb-cloud/connect-via-standard-connection-serverless.md).

## Prerequisite: Configure IP access list

For public connection, TiDB Cloud only allows client connections from addresses in the IP access list. If you have not configured IP access list,  take the following sub-steps to configure it before first connection.

1. Navigate to the Networking page of a TiDB Dedicated cluster..

2. Click **Add IP Address**, choose one of the following options.

        - **Allow access from anywhere** : All IP addresses are allowed to access TiDB Cloud. This would expose your cluster to the internet completely, which is highly risky.
        - **Use IP addresses**: Recommand, you can add a list of IPs and CIDR addresses that are allowed to access TiDB Cloud via a SQL client.

3. Add IP addresses or CIDR range with an optional description. You can add up to 100 addresses.

4. Click **Confirm** to confirm the changes.

## Connect to the cluster:

To connect to a TiDB Dedicated cluster via public connection, take the following steps:

1. Open the overview page of the target cluster.

    1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.

        > **Tip:**
        >
        > If you have multiple projects, you can click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner and switch to another project.

    2. Click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Select `Public` in **Connection Type**. If you have not configured IP access list, you need to click **Configure IP Access List** to configure it before first connection.

4. Click **CA cert** to download CA cert for TLS connection to TiDB clusters. The CA cert supports TLS 1.2 version by default.

5. Choose your preferred connection method, and then refer to the connection string and sample code on the tab to connect to your cluster.

## What's next

After you have successfully connected to your TiDB cluster, you can [explore SQL statements with TiDB](/basic-sql-operations.md).
