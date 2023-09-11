---
title: Connect to Your TiDB Serverless Cluster
summary: Learn how to connect to your TiDB Serverless cluster via different methods.
---

# Connect to Your TiDB Serverless Cluster

## Connection Methods

This document introduces the methods to connect to your TiDB Serverless cluster.

> **Tip:**
>
> To learn how to connect to a TiDB Dedicated cluster, see [Connect to Your TiDB Dedicated Cluster](/tidb-cloud/connect-to-tidb-cluster.md).

After your TiDB Serverless cluster is created on TiDB Cloud, you can connect to it via one of the following methods:

- Direct Connections

  TiDB Serverless provides MySQL-compatible database for you. You can connect to your TiDB Serverless using any tool which supports MySQL, such as [MySQL client](https://dev.mysql.com/downloads/shell/).

- [Data Service (beta)](/tidb-cloud/data-service-overview.md)

  TiDB Serverless provides a Data Service feature that enables you to access TiDB Serverless data via an HTTPS request using a custom API endpoint.

- [Serverless Driver (beta)](/tidb-cloud/serverless-driver.md)

  TiDB Serverless provides Serverless Driver, a javascript driver that allows you to connect to your TiDB Serverless in the edge environment over HTTP.

- [Chat2Query (beta)](/tidb-cloud/explore-data-with-chat2query.md)

  TiDB Cloud is powered by artificial intelligence (AI). You can use Chat2Query (beta), an AI-powered SQL editor in the [TiDB Cloud console](https://tidbcloud.com/), to maximize your data value.

  In Chat2Query, you can either simply type `--` followed by your instructions to let AI generate SQL queries automatically or write SQL queries manually, and then run SQL queries against databases without a terminal. You can find the query results in tables intuitively and check the query logs easily.

## Network

There are two types of network of TiDB Serverless:

- [Private endpoint](/tidb-cloud/set-up-private-endpoint-connections-serverless.md) (recommended)

  Private endpoint connection provides a private endpoint to allow SQL clients in your VPC to securely access services over AWS PrivateLink, which provides highly secure and one-way access to database services with simplified network management.

- [Public endpoint](/tidb-cloud/connect-via-standard-connection-serverless.md)

  The standard connection exposes a public endpoint with traffic filters, so you can connect to your TiDB cluster via a SQL client from your laptop.

  TiDB Serverless supports [TLS connections](/tidb-cloud/secure-connections-to-serverless-clusters.md), which ensures the security of data transmission from your applications to TiDB clusters.

The following table shows the network you can use in different connection methods:

| Connection method  | Network                     | Description                                                                   |
|--------------------|-----------------------------|-------------------------------------------------------------------------------|
| Direct Connections | Public and Private endpoint | Both public endpoint and private endpoint are supported in direct connections |
| Data Service       | /                           | Data Service needn't specify network                                          |
| Serverless Driver  | Public endpoint             | Serverless driver only support public endpoint                                |
| Chat2Query         | /                           | Chat2Query needn't specify network                                            |

## What's next

After you have successfully connected to your TiDB cluster, you can [explore SQL statements with TiDB](/basic-sql-operations.md).
