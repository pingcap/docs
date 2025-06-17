---
title: Select Your Cluster Plan
summary: Learn how to select your cluster plan on TiDB Cloud.
---

# Select Your Cluster Plan

The cluster plan determines the throughput and performance of your cluster.

TiDB Cloud provides the following two options of cluster plan. Before creating a cluster, you need to consider which option suits your need better.

- [TiDB Cloud Starter](#tidb-cloud-starter)
- [TiDB Cloud Essential](#tidb-cloud-essential)
<!--TBD, ToDo-->

## TiDB Cloud Starter

<!--To be confirmed-->
TiDB Cloud Starter is a fully managed, multi-tenant TiDB offering. It delivers an instant, autoscaling MySQL-compatible database and offers a generous free plan and consumption based billing once free limits are exceeded.

### Cluster plans

TiDB Cloud Starter offers two service plans to meet different user requirements. Whether you are just getting started or scaling to meet the increasing application demands, these service plans provide the flexibility and capability you need.

#### Free cluster plan

The free cluster plan is ideal for those who are getting started with TiDB Cloud Starter. It provides developers and small teams with the following essential features:

- **No cost**: This plan is completely free, with no credit card required to get started.
- **Storage**: Provides an initial 5 GiB of row-based storage and 5 GiB of columnar storage.
- **Request Units**: Includes 50 million [Request Units (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit) for database operations.

### Usage quota

For each organization in TiDB Cloud, you can create a maximum of five [free clusters](#free-cluster-plan) by default. To create more TiDB Cloud Starter clusters, you need to add a credit card and specify a spending limit.

For the first five TiDB Cloud Starter clusters in your organization, whether they are free or scalable, TiDB Cloud provides a free usage quota for each of them as follows:

- Row-based storage: 5 GiB
- Columnar storage: 5 GiB
- Request Units (RUs): 50 million RUs per month

A Request Unit (RU) is a unit of measure used to represent the amount of resources consumed by a single request to the database. The amount of RUs consumed by a request depends on various factors, such as the operation type or the amount of data being retrieved or modified.

Once a cluster reaches its usage quota, it immediately denies any new connection attempts until you [increase the quota](/tidb-cloud/manage-serverless-spend-limit.md#update-spending-limit) or the usage is reset upon the start of a new month. Existing connections established before reaching the quota will remain active but will experience throttling. For example, when the row-based storage of a cluster exceeds 5 GiB for a free cluster, the cluster automatically restricts any new connection attempts.

To learn more about the RU consumption of different resources (including read, write, SQL CPU, and network egress), the pricing details, and the throttled information, see [TiDB Cloud Starter Pricing Details](https://www.pingcap.com/tidb-cloud-serverless-pricing-details). <!--TBD, ToDo: Not sure the Pricing URL for TiDB Cloud Starter-->

### User name prefix

<!--Important: Do not update the section name "User name prefix" because this section is referenced by TiDB backend error messages.-->

For each TiDB Cloud Starter cluster, TiDB Cloud generates a unique prefix to distinguish it from other clusters.

Whenever you use or set a database user name, you must include the prefix in the user name. For example, assume that the prefix of your cluster is `3pTAoNNegb47Uc8`.

- To connect to your cluster:

    ```shell
    mysql -u '3pTAoNNegb47Uc8.root' -h <host> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=<CA_root_path> -p
    ```

    > **Note:**
    >
    > TiDB Cloud Starter requires TLS connection. To find the CA root path on your system, see [Root certificate default path](/tidb-cloud/secure-connections-to-serverless-clusters.md#root-certificate-default-path).

- To create a database user:

    ```sql
    CREATE USER '3pTAoNNegb47Uc8.jeffrey';
    ```

To get the prefix for your cluster, take the following steps:

1. Navigate to the [**Clusters**](https://console.tidb.io/project/clusters) page.
2. Click the name of your target cluster to go to its overview page, and then click **Connect** in the upper-right corner. A connection dialog is displayed.
3. In the dialog, get the prefix from the connection string.

## TiDB Cloud Essential

For applications experiencing growing workloads and needing scalability in real time, the Essential cluster plan provides the flexibility and performance to keep pace with your business growth with the following features:

- **Enhanced capabilities**: includes all capabilities of the Starter plan, along with the capacity to handle larger and more complex workloads, as well as advanced security features.
- **Automatic scaling**: automatically adjusts storage and computing resources to efficiently meet changing workload demands.
- **High availability**: built-in fault tolerance and redundancy ensure your applications remain available and resilient, even during infrastructure failures.
- **Predictable pricing**: billed based on storage and Request Capacity Units (RCUs) of the compute resources, offering transparent, usage-based pricing that scales with your needs, so you only pay for what you use without surprises.
