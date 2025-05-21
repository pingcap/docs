---
title: Create a TiDB Cloud Serverless Cluster
summary: Learn how to create your TiDB Cloud Serverless cluster.
---

# Create a TiDB Cloud Serverless Cluster

This document describes how to create a TiDB Cloud Serverless cluster in the [TiDB Cloud console](https://tidbcloud.com/).

> **Tip:**
>
> To learn how to create a TiDB Cloud Dedicated cluster, see [Create a TiDB Cloud Dedicated Cluster](/tidb-cloud/create-tidb-cluster.md).

## Before you begin

If you do not have a TiDB Cloud account, click [here](https://tidbcloud.com/signup) to sign up for an account.

- You can either sign up with email and password so that you can manage your password using TiDB Cloud, or sign up with your Google, GitHub, or Microsoft account.
- For AWS Marketplace users, you can also sign up through AWS Marketplace. To do that, search for `TiDB Cloud` in [AWS Marketplace](https://aws.amazon.com/marketplace), subscribe to TiDB Cloud, and then follow the onscreen instructions to set up your TiDB Cloud account.
- For Azure Marketplace users, you can also sign up through Azure Marketplace. To do that, search for `TiDB Cloud` in [Azure Marketplace](https://azuremarketplace.microsoft.com), subscribe to TiDB Cloud, and then follow the onscreen instructions to set up your TiDB Cloud account.
- For Google Cloud Marketplace users, you can also sign up through Google Cloud Marketplace. To do that, search for `TiDB Cloud` in [Google Cloud Marketplace](https://console.cloud.google.com/marketplace), subscribe to TiDB Cloud, and then follow the onscreen instructions to set up your TiDB Cloud account.

## Steps

If you are in the `Organization Owner` or the `Project Owner` role, you can create a TiDB Cloud Serverless cluster as follows:

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/), and then navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page.

2. Click **Create Cluster**.

3. On the **Create Cluster** page, **Serverless** is selected by default.

4. The cloud provider of TiDB Cloud Serverless is AWS. You can select an AWS region where you want to host your cluster.

5. Update the default cluster name if necessary.

6. Select a cluster plan. TiDB Cloud Serverless provides two [cluster plans](/tidb-cloud/select-cluster-tier.md#cluster-plans): **Free Cluster** and **Scalable Cluster**. You can start with a free cluster and later upgrade to a scalable cluster as your needs grow. To create a scalable cluster, you need to specify a **Monthly Spending Limit** and add a credit card.

    > **Note:**
    >
    > For each organization in TiDB Cloud, you can create a maximum of five [free clusters](/tidb-cloud/select-cluster-tier.md#free-cluster-plan) by default. To create more TiDB Cloud Serverless clusters, you need to add a credit card and create [scalable clusters](/tidb-cloud/select-cluster-tier.md#scalable-cluster-plan) for the usage.

7. Click **Create**.

    The cluster creation process starts and your TiDB Cloud cluster will be created in approximately 30 seconds.

## What's next

After your cluster is created, follow the instructions in [Connect to TiDB Cloud Serverless via Public Endpoint](/tidb-cloud/connect-via-standard-connection-serverless.md) to create a password for your cluster.

> **Note:**
>
> If you do not set a password, you cannot connect to the cluster.
