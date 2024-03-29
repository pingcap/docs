---
title: Select Your Cluster Tier
summary: Learn how to select your cluster tier on TiDB Cloud.
aliases: ['/tidbcloud/developer-tier-cluster']
---

# Select Your Cluster Tier

The cluster tier determines the throughput and performance of your cluster.

TiDB Cloud provides the following two options of cluster tiers. Before creating a cluster, you need to consider which option suits your need better.

- [TiDB Serverless](#tidb-serverless)
- [TiDB Dedicated](#tidb-dedicated)

## TiDB Serverless

<!--To be confirmed-->
TiDB Serverless is a fully managed, multi-tenant TiDB offering. It delivers an instant, autoscaling MySQL-compatible database and offers a generous free tier and consumption based billing once free limits are exceeded.

### Cluster Plan

At TiDB Serverless, we offer two distinct service plans designed to cater to the diverse needs of our users. Whether you're just getting started or scaling to meet the demands of growing applications, our service plans provide the flexibility and power you need.

#### Free Cluster
The Free Cluster Plan is ideal for those who are getting started with TiDB Serverless. It's designed to provide developers and small teams with the essential features as following:

- **No Cost**: Absolutely free with no credit card required to start.
- **Storage**: Comes with 5GiB of initial storage capacity.
- **Request Units**: Includes 50 million request units for your database operations.
- **Easy Upgrade**: Seamlessly transition to the Scalable Cluster Plan as your needs grow.

#### Scalable Cluster

For applications with increasing workloads that require on-the-fly scalability, the Scalable Cluster Plan offers the agility and performance to keep pace with your business growth with the following features:

- **Enhanced Capabilities**: Includes all the capabilities of the Free Cluster Plan, plus the ability to handle larger, more demanding workloads, with more advanced security features.
- **Automatic Scaling**: Automatically adjusts storage and compute resources to efficiently handle varying workload demands.
- **Predictable Pricing**: While this plan requires a credit card, you pay only for the resources you consume, ensuring cost efficiency as you scale.

### Usage quota

For each organization in TiDB Cloud, you can create a maximum of five Free Clusters by default. To create more TiDB Serverless clusters, you need to add a credit card and create Scalable Clusters for the usage.

For the first five TiDB Serverless clusters in your organization, no matter Free Cluster or Scalable Cluster, TiDB Cloud provides a free usage quota for each of them as follows:

- Row-based storage: 5 GiB
- [Request Units (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit): 50 million RUs per month

A Request Unit (RU) is a unit of measure used to represent the amount of resources consumed by a single request to the database. The amount of RUs consumed by a request depends on various factors, such as the operation type or the amount of data being retrieved or modified.

Once the free quota of a cluster is reached, the read and write operations on this cluster will be throttled until you [increase the quota](/tidb-cloud/manage-serverless-spend-limit.md#update-spending-limit) or the usage is reset upon the start of a new month. For example, when the storage of a cluster exceeds 5 GiB, the maximum size limit of a single transaction is reduced from 10 MiB to 1 MiB.

To learn more about the RU consumption of different resources (including read, write, SQL CPU, and network egress), the pricing details, and the throttled information, see [TiDB Serverless Pricing Details](https://www.pingcap.com/tidb-cloud-serverless-pricing-details).

### User name prefix

<!--Important: Do not update the section name "User name prefix" because this section is referenced by TiDB backend error messages.-->

For each TiDB Serverless cluster, TiDB Cloud generates a unique prefix to distinguish it from other clusters.

Whenever you use or set a database user name, you must include the prefix in the user name. For example, assume that the prefix of your cluster is `3pTAoNNegb47Uc8`.

- To connect to your cluster:

    ```shell
    mysql -u '3pTAoNNegb47Uc8.root' -h <host> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=<CA_root_path> -p
    ```

    > **Note:**
    >
    > TiDB Serverless requires TLS connection. To find the CA root path on your system, see [Root certificate default path](/tidb-cloud/secure-connections-to-serverless-clusters.md#root-certificate-default-path).

- To create a database user:

    ```sql
    CREATE USER '3pTAoNNegb47Uc8.jeffrey';
    ```

To get the prefix for your cluster, take the following steps:

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page.
2. Click the name of your target cluster to go to its overview page, and then click **Connect** in the upper-right corner. A connection dialog is displayed.
3. In the dialog, get the prefix from the connection string.

### TiDB Serverless special terms and conditions

Some of TiDB Cloud features are partially supported or not supported on TiDB Serverless. See [TiDB Serverless Limitations](/tidb-cloud/serverless-limitations.md) for details.

## TiDB Dedicated

TiDB Dedicated is for production use with the benefits of cross-zone high availability, horizontal scaling, and [HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing).

For TiDB Dedicated clusters, you can customize the cluster size of TiDB, TiKV, and TiFlash easily according to your business need. For each TiKV node and TiFlash node, the data on the node is replicated and distributed in different availability zones for [high availability](/tidb-cloud/high-availability-with-multi-az.md).

To create a TiDB Dedicated cluster, you need to [add a payment method](/tidb-cloud/tidb-cloud-billing.md#payment-method) or [apply for a Proof of Concept (PoC) trial](/tidb-cloud/tidb-cloud-poc.md).

> **Note:**
>
> You cannot decrease the node storage after your cluster is created.
