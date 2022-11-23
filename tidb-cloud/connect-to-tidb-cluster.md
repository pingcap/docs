---
title: Connect to Your TiDB Cluster
summary: Connect to your TiDB cluster via a SQL client or SQL shell.
---

# Connect to Your TiDB Cluster

After your TiDB cluster is created on TiDB Cloud, you can use one of the following methods to connect to your TiDB cluster. You can access your cluster via a SQL client, or quickly via SQL Shell in the TiDB Cloud Console.

+ Connect via a SQL client

    - [Connect via standard connection](/tidb-cloud/connect-via-standard-connection.md): The standard connection exposes a public endpoint with traffic filters, so you can connect to your TiDB cluster from your laptop. You can connect to your TiDB clusters using TLS, which ensures the security of data transmission from your applications to TiDB clusters.
    - [Connect via private endpoint](/tidb-cloud/set-up-private-endpoint-connections.md) (recommended for production): Private endpoint connection provides a private endpoint to allow clients in your VPC to securely access services over AWS PrivateLink, which provides highly secure and one-way access to database services with simplified network management. Note that you cannot connect to [Serverless Tier clusters](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta) using the private endpoint.
    - [Connect via VPC peering](/tidb-cloud/set-up-vpc-peering-connections.md): If you want lower latency and more security, set up VPC peering and connect via a private endpoint using a VM instance on the corresponding cloud provider in your cloud account. Note that you cannot connect to [Serverless Tier clusters](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta) using VPC peering.

- [Connect via SQL shell](/tidb-cloud/connect-via-sql-shell.md): to try TiDB SQL and test out TiDB's compatibility with MySQL quickly, or administer user privileges

> **Tip:**
>
> For production environments, it is recommended to use the [private endpoint](#connect-via-private-endpoint-recommended) connection.

## What's next

After you have successfully connected to your TiDB cluster, you can [explore SQL statements with TiDB](/basic-sql-operations.md).
