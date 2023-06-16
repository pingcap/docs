---
title: Manage Spend Limit for TiDB Serverless clusters
summary: Learn how to manage spend limit for your TiDB Serverless clusters.
---

# Manage Spend Limit for TiDB Serverless Clusters

> **Note:**
>
> The spend limit is only applicable to TiDB Serverless clusters.

Spend limit refers to the maximum amount of money that you are willing to spend on a particular workload in a month. It is a cost-control mechanism that allows you to set a budget for your TiDB Serverless clusters.

For each organization in TiDB Cloud, you can create a maximum of five TiDB Serverless clusters by default. To create more TiDB Serverless clusters, you need to add a credit card and set a spend limit for the usage. But if you delete some of your previous clusters before creating more, the new cluster can still be created without a credit card.

## Usage quota

For the first five TiDB Serverless clusters in your organization, TiDB Cloud provides a free usage quota for each of them as follows:

- Row storage: 5 GiB
- [Request Units (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit): 50 million RUs per month

Once the free quota of a cluster is reached, the read and write operations on this cluster will be throttled until you [increase the quota](#update-spend-limit) or the usage is reset upon the start of a new month. For example, when the storage of a cluster exceeds 5 GiB, the maximum size limit of a single transaction is reduced from 10 MiB to 1 MiB.

To learn more about the RU consumption of different resources (including read, write, SQL CPU, and network egress), the pricing details, and the throttled information, see [TiDB Serverless Pricing Details](https://www.pingcap.com/tidb-cloud-serverless-pricing-details).

If you want to create a TiDB Serverless cluster with an additional quota, you can edit the spend limit on the cluster creation page. For more information, see [Create a TiDB Serverless cluster](/tidb-cloud/create-tidb-cluster-serverless.md).

## Update spend limit

For an existing TiDB Serverless cluster, you can increase the usage quota by updating the spend limit as follows:

1. In the TiDB Cloud console, click the ☰ hover menu in the upper-left corner, and then click the name of your target cluster to go to its overview page.

    > **Tip:**
    >
    > If you have multiple projects, you can view the project list and switch to another project in the ☰ hover menu.

2. In the **Usage This Month** area, click **Get more usage quota**.
3. Edit the monthly spend limit as needed. If you have not added a payment method, you will need to add a credit card after editing the limit.
4. Click **Update spend limit**.
