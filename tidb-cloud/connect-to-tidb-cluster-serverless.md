---
title: Connect to Your TiDB Cloud Cluster
summary: Learn how to connect to your TiDB Cloud cluster via different methods.
---

# Connect to Your TiDB Cloud Cluster

This document describes how to connect to your TiDB Cloud cluster.

## Connection methods

After your TiDB Cloud cluster is created on TiDB Cloud, you can connect to it via one of the following methods:

- Direct connections

  Direct connections mean the MySQL native connection system over TCP. You can connect to your TiDB Cloud Starter cluster using any tool that supports MySQL connection, such as [MySQL client](https://dev.mysql.com/doc/refman/8.0/en/mysql.html).

- [Serverless Driver (beta)](/tidb-cloud/serverless-driver.md)

  TiDB Cloud provides a serverless driver for JavaScript, which allows you to connect to your TiDB Cloud Starter cluster in edge environments with the same experience as direct connections.

In the preceding connection methods, you can choose your desired one based on your needs:

| Connection method  | User interface     | Scenario                                                                                                                                                       |
|--------------------|--------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Direct connections | SQL/ORM            | Long-running environment, such as Java, Node.js, and Python.                                                                                                   |
| Serverless Driver  | SQL/ORM            | Serverless and edge environments such as [Vercel Edge Functions](https://vercel.com/docs/functions/edge-functions) and [Cloudflare Workers](https://workers.cloudflare.com/). |

## Network

There are two network connection types for TiDB Cloud:

- [Private endpoint](/tidb-cloud/set-up-private-endpoint-connections-serverless.md) (recommended)

    Private endpoint connection provides a private endpoint to allow SQL clients in your VPC to securely access services over AWS PrivateLink, which provides highly secure and one-way access to database services with simplified network management.

- [Public endpoint](/tidb-cloud/connect-via-standard-connection-serverless.md)

  The standard connection exposes a public endpoint, so you can connect to your TiDB cluster via a SQL client from your laptop.

  TiDB Cloud requires [TLS connections](/tidb-cloud/secure-connections-to-serverless-clusters.md), which ensures the security of data transmission from your applications to TiDB clusters.

The following table shows the network you can use in different connection methods:

| Connection method          | Network                      | Description                                                                                                       |
|----------------------------|------------------------------|-------------------------------------------------------------------------------------------------------------------|
| Direct connections         | Public or private endpoint   | Direct connections can be made via both public and private endpoints.                                             |
| Serverless Driver (beta)   | Public endpoint              | Serverless Driver only supports connections via public endpoint.                                                  |

## What's next

After you have successfully connected to your TiDB cluster, you can [explore SQL statements with TiDB](/basic-sql-operations.md).
