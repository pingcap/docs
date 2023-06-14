---
title: Connect to Your TiDB Dedicated Cluster
summary: Learn how to connect to your TiDB Dedicated cluster via different methods.
---

# Connect to Your TiDB Dedicated Cluster

This document introduces the methods to connect to your TiDB Dedicated cluster.

> **Tip:**
>
> To learn how to connect to a TiDB Serverless cluster, see [Connect to Your TiDB Serverless Cluster](/tidb-cloud/connect-to-tidb-cluster-serverless.md).

After your TiDB Dedicated cluster is created on TiDB Cloud, you can connect to it via one of the following methods:

- [Connect via standard connection](/tidb-cloud/connect-via-standard-connection.md)

    The standard connection exposes a public endpoint with traffic filters, so you can connect to your TiDB cluster via a SQL client from your laptop. You can connect to your TiDB clusters using TLS, which ensures the security of data transmission from your applications to TiDB clusters.

- [Connect via private endpoint](/tidb-cloud/set-up-private-endpoint-connections.md) (recommended)

    Private endpoint connection provides a private endpoint to allow SQL clients in your VPC to securely access services over AWS PrivateLink, which provides highly secure and one-way access to database services with simplified network management.

- [Connect via VPC peering](/tidb-cloud/set-up-vpc-peering-connections.md)

    If you want lower latency and more security, set up VPC peering and connect via a private endpoint using a VM instance on the corresponding cloud provider in your cloud account.

- [Connect via SQL Shell](/tidb-cloud/connect-via-sql-shell.md): to try TiDB SQL and test out TiDB's compatibility with MySQL quickly, or administer user privileges.

## What's next

After you have successfully connected to your TiDB cluster, you can [explore SQL statements with TiDB](/basic-sql-operations.md).
