---
title: Create a TiDB Cloud Cluster
summary: Learn how to create your TiDB Cloud cluster.
---

# Create a TiDB Cloud Cluster

This document describes how to create a TiDB Cloud cluster in the [TiDB Cloud console](https://console.tidb.io/signup?provider_source=alicloud).

## Before you begin

If you do not have a TiDB Cloud account, click [here](https://console.tidb.io/free-trial?provider_source=alicloud) to sign up for an account.

- You can either sign up with email and password so that you can manage your password using TiDB Cloud, or sign up with your Google, GitHub, or Microsoft account.

## Steps

If you are in the `Organization Owner` or the `Project Owner` role, you can create a TiDB Cloud cluster as follows:

1. Log in to the [TiDB Cloud console](https://console.tidb.io/signup?provider_source=alicloud), and then navigate to the [**Clusters**](https://console.tidb.io/project/clusters) page.

2. Click **Create Cluster**.

3. Select a cluster plan. TiDB Cloud provides two [cluster plans](/tidb-cloud/select-cluster-tier.md#cluster-plans): **Starter** and **Essential**. You can start with a Starter cluster and later upgrade to an Essential cluster as your needs grow.

4. The cloud provider is Alibaba Cloud. You can select an Alibaba Cloud region where you want to host your cluster.

5. Update the default cluster name if necessary.

6. Update the capacity of the cluster.

    - Starter plan:

        - You can update the spending limit for your cluster. If the spending limit is set to 0, the cluster remains in the free tier. If the spending limit is greater than 0, you need to add a credit card before creating the cluster.

        - By default, each organization can create up to five [free Starter clusters](/tidb-cloud/select-cluster-tier.md#free-cluster-plan) by default. To create additional Starter clusters, you must add a credit card and specify a spending limit.

    - Essential plan:

        - You must specify both a minimum and maximum number of Request Capacity Units (RCUs) for your cluster.

        - RCUs represent the compute resources provisioned for your workload. TiDB Cloud automatically scales your cluster within this range based on demand.

7. Click **Create**.

    The cluster creation process starts and your TiDB Cloud cluster will be created in approximately 30 seconds.

## What's next

After your cluster is created, follow the instructions in [Connect to TiDB Cloud via Public Endpoint](/tidb-cloud/connect-via-standard-connection-serverless.md) to create a password for your cluster.

> **Note:**
>
> If you do not set a password, you cannot connect to the cluster.
