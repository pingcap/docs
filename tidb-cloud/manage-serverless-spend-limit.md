---
title: Manage Spend Limit for Serverless Tier clusters
summary: Learn how to manage spend limit for your Serverless Tier clusters.
---

# Manage Spend Limit for Serverless Tier Clusters

> **Note:**
>
> The spend limit is only applicable to Serverless Tier clusters. For Dedicated Tier clusters, TiDB Cloud charges according to the resources that you consume.

For each Serverless Tier cluster, TiDB Cloud provides a free usage quota as follows:

- Row storage: 5 GiB
- Column storage: 5 GiB
- Request Units (RU): 50 MB per month

Once the free quota limit of a cluster is reached, the cluster will be throttled to 100 RU/s until you get more usage quota or the current usage is reset after the next month.

If you want to create a Serverless Tier cluster with an additional quota, you can edit the spend limit on the cluster creation page. For more information, see [Create a TiDB cluster](/tidb-cloud/create-tidb-cluster.md#step-4-create-a-tidb-cluster).

After creating a Serverless Tier, you can still check and edit the spend limit on your cluster overview page as follows:

1. In the TiDB Cloud console, click the ☰ hover menu in the upper-left corner, and then click the name of your target cluster to go to its overview page.

    > **Tip:**
    >
    > If you have multiple projects, you can view the project list and switch to another project in the ☰ hover menu.

2. In the **Usage This Month** area, click **Get more usage quota**.
3. Edit the monthly spend limit as needed. If you have not added a payment method, you will need to add a credit card after editing the limit.
4. Click **Update spend limit**.
