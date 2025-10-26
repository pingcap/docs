---
title: Connect to TiDB Cloud Premium via Public Connection
summary: Learn how to connect to your TiDB Cloud cluster via public connection.
---

# Connect to TiDB Cloud Premium via Public Connection

This document describes how to connect to your TiDB Cloud Premium cluster via public connection. The public connection exposes a public endpoint with traffic filters, so you can connect to your TiDB Cloud Premium cluster via a SQL client from your laptop.

> **Tip:**
>
> - To learn how to connect to a {{{ .starter }}} or {{{ .essential }}} cluster via public connection, see [Connect to {{{ .starter }}} or Essential via Public Endpoint](/tidb-cloud/connect-via-standard-connection-serverless.md).
> - To learn how to connect to a TiDB Cloud Dedicated cluster via public endpoint, see [Connect to TiDB Cloud Dedicated via Public Connection](/tidb-cloud/connect-via-standard-connection.md).

## Prerequisite: Configure IP access list

For public connections, TiDB Cloud Premium only allows client connections from addresses in the IP access list. If you have not configured the IP access list, follow the steps in [Configure an IP Access List](/tidb-cloud/configure-ip-access-list-premium.md) to configure it before your first connection.

## Connect to the instance

To connect to a TiDB Cloud Premium instance via public connection, take the following steps:

1. Open the overview page of the target instance.

    1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**TiDBs**](https://tidbcloud.com/tidbs) page of your project.

        > **Tip:**
        >
        > You can use the combo box in the upper-left corner to switch between organizations.

    2. Click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. In the connection dialog, select **Public** from the **Connection Type** drop-down list.

    If you have not configured the IP access list, click **Configure IP Access List** or follow the steps in [Configure an IP Access List](/tidb-cloud/configure-ip-access-list-premium.md) to configure it before your first connection.

4. Click **CA cert** to download CA cert for TLS connection to TiDB clusters. The CA cert supports TLS 1.2 version by default.

5. Choose your preferred connection method, and then refer to the connection string and sample code on the tab to connect to your cluster.

## What's next

After you have successfully connected to your TiDB instance, you can [explore SQL statements with TiDB](/basic-sql-operations.md).
