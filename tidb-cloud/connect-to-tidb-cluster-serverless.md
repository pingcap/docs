---
title: Connect to Your TiDB Serverless Cluster
summary: Learn how to connect to your TiDB Serverless cluster via different methods.
---

# Connect to Your TiDB Serverless Cluster

This document describes how to connect to your TiDB Serverless cluster.

> **Tip:**
>
> To learn how to connect to a TiDB Dedicated cluster, see [Connect to Your TiDB Dedicated Cluster](/tidb-cloud/connect-to-tidb-cluster.md).

## Connection methods

After your TiDB Serverless cluster is created on TiDB Cloud, you can connect to it via one of the following methods:

- Direct connections

  TiDB Serverless is MySQL-compatible. You can connect to your TiDB Serverless cluster using any tool that supports MySQL connections, such as [MySQL client](https://dev.mysql.com/doc/refman/8.0/en/mysql.html).

- [Data Service (beta)](/tidb-cloud/data-service-overview.md)

  TiDB Serverless provides a Data Service feature that enables you to access TiDB Serverless data via an HTTPS request using a custom API endpoint.

- [Serverless Driver (beta)](/tidb-cloud/serverless-driver.md)

  TiDB Serverless provides Serverless driver, a javascript driver that allows you to connect to your TiDB Serverless cluster in edge environments over HTTP.

## Choose a connection method

- The direct connection means the MySQL native connection system over TCP. You can use it in any long-running environment, like Java, Node.js, Python, etc.
- The Data Service provides restful HTTP API for you. You can use it for all browser and application interactions.
- The serverless driver is useful in edge environments such as Vercel Edge Function and Cloudflare Workers.

## Network

There are two network connection types for TiDB Serverless:

- [Private endpoint](/tidb-cloud/set-up-private-endpoint-connections-serverless.md) (recommended)

  Private endpoint connection provides a private endpoint to allow SQL clients in your VPC to securely access services over AWS PrivateLink, which provides highly secure and one-way access to database services with simplified network management.

- [Public endpoint](/tidb-cloud/connect-via-standard-connection-serverless.md)

  The standard connection exposes a public endpoint with traffic filters, so you can connect to your TiDB cluster via a SQL client from your laptop.

  TiDB Serverless supports [TLS connections](/tidb-cloud/secure-connections-to-serverless-clusters.md), which ensures the security of data transmission from your applications to TiDB clusters.

The following table shows the network you can use in different connection methods:

| Connection method  | Network                     | Description                                                                                                             |
|--------------------|-----------------------------|-------------------------------------------------------------------------------------------------------------------------|
| Direct connections | Public or private endpoint | Direct connections can be made via both public and private endpoints.                                                   |
| Data Service (beta)       | /                           | Accessing TiDB Serverless via Data Service (beta) is through API Key so there is no need to specify the network. |
| Serverless Driver (beta)  | Public endpoint             | Serverless Driver only supports connections via public endpoint.                                                        |
| Chat2Query (beta)         | /                           | Chat2Query does not need to specify the network.                                                                        |

## What's next

After you have successfully connected to your TiDB cluster, you can [explore SQL statements with TiDB](/basic-sql-operations.md).
