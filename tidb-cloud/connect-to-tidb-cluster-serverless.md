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

This section describes the connection methods you can use to connect to a TiDB Serverless cluster.

- Direct connections

  Direct connections mean the MySQL native connection system over TCP, You can connect to your TiDB Serverless cluster using any tool that supports MySQL connection, such as [MySQL client](https://dev.mysql.com/doc/refman/8.0/en/mysql.html).

- [Data Service (beta)](/tidb-cloud/data-service-overview.md)

  TiDB Serverless provides a Data Service feature that enables you to connect to your TiDB Serverless cluster via an HTTPS request using a custom API endpoint. Different from direct connections, Data Service access TiDB Serverless data via restful api rather than the raw SQL.

- [Serverless Driver (beta)](/tidb-cloud/serverless-driver.md)

  TiDB Serverless provides serverless driver, a javascript driver that allows you to connect to your TiDB Serverless cluster in edge environment with the same experience as direct connection.

In the preceding connection methods, you can choose your desired one based on your needs:

| Connection method  | Protocol | Scenario                                                               |
|--------------------|----------|------------------------------------------------------------------------|
| Direct connections | TCP      | Long-running environment, like Java, Node.js, Python, etc.             |
| Data Service       | HTTP     | All browser and application interactions.                              |
| Serverless driver  | HTTP     | Edge environments such as Vercel Edge Function and Cloudflare Workers. |

## Network

There are two network connection types for TiDB Serverless:

- [Private endpoint](/tidb-cloud/set-up-private-endpoint-connections-serverless.md) (recommended)

  Private endpoint connection provides a private endpoint to allow SQL clients in your VPC to securely access services over AWS PrivateLink, which provides highly secure and one-way access to database services with simplified network management.

- [Public endpoint](/tidb-cloud/connect-via-standard-connection-serverless.md)

  The standard connection exposes a public endpoint, so you can connect to your TiDB cluster via a SQL client from your laptop.

  TiDB Serverless supports [TLS connections](/tidb-cloud/secure-connections-to-serverless-clusters.md), which ensures the security of data transmission from your applications to TiDB clusters.

The following table shows the network you can use in different connection methods:

| Connection method          | Network                      | Description                                                                                                          |
|----------------------------|------------------------------|----------------------------------------------------------------------------------------------------------------------|
| Direct connections         | Public or private endpoint   | Direct connections can be made via both public and private endpoints.                                                |
| Data Service (beta)        | /                            | Accessing TiDB Serverless via Data Service (beta) is through API Key so there is no need to specify the network.     |
| Serverless Driver (beta)   | Public endpoint              | Serverless Driver only supports connections via public endpoint.                                                     ||

## What's next

After you have successfully connected to your TiDB cluster, you can [explore SQL statements with TiDB](/basic-sql-operations.md).
