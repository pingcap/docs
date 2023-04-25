---
title: Manage Spend Limit for Serverless Tier clusters
summary: Learn how to manage spend limit for your Serverless Tier clusters.
---

# Manage Spend Limit for Serverless Tier Clusters

> **Note:**
>
> The spend limit is only applicable to Serverless Tier clusters.

Spend limit refers to the maximum amount of money that you are willing to spend on a particular workload in a month. It is a cost-control mechanism that allows you to set a budget for your Serverless Tier clusters.

For each organization in TiDB Cloud, you can create a maximum of five Serverless Tier clusters by default. To create more Serverless Tier clusters, you need to add a credit card and set a spend limit for the usage. But if you delete some of your previous clusters before creating more, the new cluster can still be created without a credit card.

## Usage quota

For each Serverless Tier cluster, TiDB Cloud provides a free usage quota as follows:

- Row storage: 5 GiB
- Column storage: 5 GiB
- [Request Units](/tidb-cloud/tidb-cloud-glossary.md#request-unit) (RUs): 50 million RUs per month

Once the free quota of a cluster is reached, the read and write operations on this cluster will be throttled until you get more usage quota or the current usage is reset after the next month.

To learn more about the RU consumption of different resources (including read, write, SQL CPU, and network egress), the pricing details, and the throttled information, see [TiDB Cloud Serverless Tier Pricing Details](https://www.pingcap.com/tidb-cloud-serverless-pricing-details).

If you want to create a Serverless Tier cluster with an additional quota, you can edit the spend limit on the cluster creation page. For more information, see [Create a TiDB cluster](/tidb-cloud/create-tidb-cluster.md#step-4-create-a-tidb-cluster).

## Update spend limit

After creating a Serverless Tier, you can still check and edit the spend limit on your cluster overview page as follows:

1. In the TiDB Cloud console, click the ☰ hover menu in the upper-left corner, and then click the name of your target cluster to go to its overview page.

    > **Tip:**
    >
    > If you have multiple projects, you can view the project list and switch to another project in the ☰ hover menu.

2. In the **Usage This Month** area, click **Get more usage quota**.
3. Edit the monthly spend limit as needed. If you have not added a payment method, you will need to add a credit card after editing the limit.
4. Click **Update spend limit**.
