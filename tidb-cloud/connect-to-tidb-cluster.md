---
title: Connect to Your TiDB Cluster
summary: Learn how to connect to your TiDB cluster via different methods.
---

# Connect to Your TiDB Cluster

After your TiDB cluster is created on TiDB Cloud, you can connect to your TiDB cluster. Depending on whether you are using a Serverless Tier cluster or a Dedicated Tier cluster, you can find the available connection methods as follows:

## Serverless Tier

For Serverless Tier clusters, you can connect to your cluster via standard connection or via Chat2Query (Beta) in the TiDB Cloud console.

- [Connect via standard connection](/tidb-cloud/connect-via-standard-connection.md#serverless-tier)

    The standard connection exposes a public endpoint with traffic filters, so you can connect to your TiDB cluster via a SQL client from your laptop.

    Serverless Tier only [supports TLS connections](/tidb-cloud/secure-connections-to-serverless-tier-clusters.md), which ensures the security of data transmission from your applications to TiDB clusters.

- Chat2Query (Beta)

    Chat2Query is a web-based SQL editor in the [TiDB Cloud console](https://tidbcloud.com/), which allows you to directly edit and run SQL queries against databases of Serverless Tier. In Chat2Query, you can use AI to generate SQL queries automatically. To access Chat2Query, go to the [**Clusters**](https://tidbcloud.com/console/clusters) page, click your cluster name, and select **Chat2Query** on the left navigation bar.

## Dedicated Tier

For Dedicated Tier clusters, you can connect to your cluster via one of the following methods:

- [Connect via standard connection](/tidb-cloud/connect-via-standard-connection.md#dedicated-tier)

    The standard connection exposes a public endpoint with traffic filters, so you can connect to your TiDB cluster via a SQL client from your laptop. You can connect to your TiDB clusters using TLS, which ensures the security of data transmission from your applications to TiDB clusters.

- [Connect via private endpoint](/tidb-cloud/set-up-private-endpoint-connections.md) (recommended)

    Private endpoint connection provides a private endpoint to allow SQL clients in your VPC to securely access services over AWS PrivateLink, which provides highly secure and one-way access to database services with simplified network management.

- [Connect via VPC peering](/tidb-cloud/set-up-vpc-peering-connections.md)

    If you want lower latency and more security, set up VPC peering and connect via a private endpoint using a VM instance on the corresponding cloud provider in your cloud account.

- [Connect via SQL Shell](/tidb-cloud/connect-via-sql-shell.md): to try TiDB SQL and test out TiDB's compatibility with MySQL quickly, or administer user privileges.

## What's next

After you have successfully connected to your TiDB cluster, you can [explore SQL statements with TiDB](/basic-sql-operations.md).
