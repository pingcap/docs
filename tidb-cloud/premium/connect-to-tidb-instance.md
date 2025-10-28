---
title: Connect to Your TiDB Cloud Instance
summary: Learn how to connect to your TiDB Cloud instance via different methods.
---

# Connect to Your TiDB Cloud Instance

This document describes how to connect to your {{{ .premium }}} instance.

> **Tip:**
>
> To learn how to connect to a TiDB Cloud Dedicated cluster, see [Connect to Your TiDB Cloud Dedicated Cluster](/tidb-cloud/connect-to-tidb-cluster.md).

## Connection methods

After your {{{ .premium }}} instance is created on TiDB Cloud, you can connect to it via direct connections.

Direct connections mean the MySQL native connection system over TCP. You can connect to your instance using any tool that supports MySQL connection, such as [MySQL client](https://dev.mysql.com/doc/refman/8.0/en/mysql.html).

| Connection method  | User interface     | Scenario                                                                                                                                                       |
|--------------------|--------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Direct connections | SQL/ORM            | Long-running environment, such as Java, Node.js, and Python.                                                                                                   |

## Network

There are two network connection types for {{{ .premium }}}:

- [Private endpoint](/tidb-cloud/premium/connect-to-premium-via-aws-private-endpoint.md) (recommended)

    Private endpoint connection provides a private endpoint to allow SQL clients in your VPC to securely access services over AWS PrivateLink, which provides highly secure and one-way access to database services with simplified network management.

- [Public endpoint](/tidb-cloud/premium/connect-to-premium-via-standard-connection.md)

  The standard connection exposes a public endpoint, so you can connect to your TiDB cluster via a SQL client from your laptop.

To ensure the security of data transmission, you need to [establish a TLS connection](/tidb-cloud/tidb-cloud-tls-connect-to-premium.md) from your client to your cluster.

The following table shows the network you can use:

| Connection method          | Network                      | Description                                                                                                       |
|----------------------------|------------------------------|-------------------------------------------------------------------------------------------------------------------|
| Direct connections         | Public or private endpoint   | Direct connections can be made via both public and private endpoints.                                             |

## What's next

After you have successfully connected to your TiDB cluster, you can [explore SQL statements with TiDB](/basic-sql-operations.md).
