---
title: Connect to Your TiDB Cloud Dedicated Cluster
summary: Learn how to connect to your TiDB Cloud Dedicated cluster via different methods.
---

# Connect to Your TiDB Cloud Dedicated Cluster

This document introduces the methods to connect to your TiDB Cloud Dedicated cluster.

> **Tip:**
>
> To learn how to connect to a TiDB Cloud Serverless cluster, see [Connect to Your TiDB Cloud Serverless Cluster](/tidb-cloud/connect-to-tidb-cluster-serverless.md).

After your TiDB Cloud Dedicated cluster is created on TiDB Cloud, you can connect to it via one of the following methods:

- Direct connections

    Direct connections use the MySQL native connection system over TCP. You can connect to your TiDB Cloud Dedicated cluster using any tool that supports MySQL connections, such as the [MySQL Command-Line Client](https://dev.mysql.com/doc/refman/8.0/en/mysql.html). TiDB Cloud also provides [SQL Shell](/tidb-cloud/connect-via-sql-shell.md), which enables you to try TiDB SQL, test out TiDB's compatibility with MySQL quickly, and manage user privileges.

    TiDB Cloud Dedicated provides three network connection types:

    - [Public connection](/tidb-cloud/connect-via-standard-connection.md)

        The public connection exposes a public endpoint with traffic filters, so you can connect to your TiDB cluster via a SQL client from your laptop. You can connect to your TiDB clusters using TLS, which ensures the security of data transmission from your applications to TiDB clusters. For more information, see [Connect to TiDB Cloud Dedicated via Public Connection](/tidb-cloud/connect-via-standard-connection.md).

    - Private endpoint (recommended)

        Private endpoint connection provides a private endpoint to allow SQL clients in your VPC to securely access TiDB Cloud Dedicated clusters. This uses the private link service provided by different cloud providers, which provides highly secure and one-way access to database services with simplified network management.

        - For TiDB Cloud Dedicated clusters hosted on AWS, the private endpoint connection uses AWS PrivateLink. For more information, see [Connect to a TiDB Cloud Dedicated Cluster via AWS PrivateLink](/tidb-cloud/set-up-private-endpoint-connections.md).
        - For TiDB Cloud Dedicated clusters hosted on Azure, the private endpoint connection uses Azure Private Link. For more information, see [Connect to a TiDB Cloud Dedicated Cluster via Azure Private Link](/tidb-cloud/set-up-private-endpoint-connections-on-azure.md).
        - For TiDB Cloud Dedicated clusters hosted on Google Cloud, the private endpoint connection uses Google Cloud Private Service Connect. For more information, see [Connect to a TiDB Cloud Dedicated Cluster via Google Cloud Private Service Connect](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md).

    - [VPC peering](/tidb-cloud/set-up-vpc-peering-connections.md)

        If you want lower latency and more security, set up VPC peering and connect via a private endpoint using a VM instance on the corresponding cloud provider in your cloud account. For more information, see [Connect to TiDB Cloud Dedicated via VPC Peering](/tidb-cloud/set-up-vpc-peering-connections.md).

- [Built-in SQL Editor](/tidb-cloud/explore-data-with-chat2query.md)

    > **Note:**
    >
    > To use SQL Editor on [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters, contact [TiDB Cloud support](/tidb-cloud/tidb-cloud-support.md).

    If your cluster is hosted on AWS and the TiDB version of the cluster is v6.5.0 or later, you can use the AI-assisted SQL Editor in the [TiDB Cloud console](https://tidbcloud.com/) to maximize your data value.

    In SQL Editor, you can either write SQL queries manually or simply press <kbd>⌘</kbd> + <kbd>I</kbd> on macOS (or <kbd>Control</kbd> + <kbd>I</kbd> on Windows or Linux) to instruct [Chat2Query (beta)](/tidb-cloud/tidb-cloud-glossary.md#chat2query) to generate SQL queries automatically. This enables you to run SQL queries against databases without a local SQL client. You can intuitively view the query results in tables or charts and easily check the query logs.

## What's next

After you have successfully connected to your TiDB cluster, you can [explore SQL statements with TiDB](/basic-sql-operations.md).
