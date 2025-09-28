---
title: Create a {{{ .starter }}} or Essential Cluster
summary: Learn how to create a {{{ .starter }}} or {{{ .essential }}} cluster.
---

# Create a {{{ .starter }}} or Essential Cluster

This document describes how to create a {{{ .starter }}} or {{{ .essential }}} cluster in the [TiDB Cloud console](https://tidbcloud.com/).

> **Tip:**
>
> To learn how to create a TiDB Cloud Dedicated cluster, see [Create a TiDB Cloud Dedicated Cluster](/tidb-cloud/create-tidb-cluster.md).

## Before you begin

If you do not have a TiDB Cloud account, click [here](https://tidbcloud.com/signup) to sign up for an account.

<CustomContent language="en,zh">

- You can either sign up with email and password so that you can manage your password using TiDB Cloud, or sign up with your Google, GitHub, or Microsoft account.
- For AWS Marketplace users, you can also sign up through AWS Marketplace. To do that, search for `TiDB Cloud` in [AWS Marketplace](https://aws.amazon.com/marketplace), subscribe to TiDB Cloud, and then follow the onscreen instructions to set up your TiDB Cloud account.
- For Azure Marketplace users, you can also sign up through Azure Marketplace. To do that, search for `TiDB Cloud` in [Azure Marketplace](https://azuremarketplace.microsoft.com), subscribe to TiDB Cloud, and then follow the onscreen instructions to set up your TiDB Cloud account.
- For Google Cloud Marketplace users, you can also sign up through Google Cloud Marketplace. To do that, search for `TiDB Cloud` in [Google Cloud Marketplace](https://console.cloud.google.com/marketplace), subscribe to TiDB Cloud, and then follow the onscreen instructions to set up your TiDB Cloud account.
- For Alibaba Cloud Marketplace users, you can also sign up through Alibaba Cloud Marketplace. To do that, search for `TiDB Cloud` in [Alibaba Cloud Marketplace](https://marketplace.alibabacloud.com/), subscribe to TiDB Cloud, and then follow the onscreen instructions to set up your TiDB Cloud account.

</CustomContent>

<CustomContent language="ja">

- You can either sign up with email and password so that you can manage your password using TiDB Cloud, or sign up with your Google, GitHub, or Microsoft account.
- For AWS Marketplace users, you can also sign up through AWS Marketplace. To do that, search for `TiDB Cloud` in [AWS Marketplace](https://aws.amazon.com/marketplace), subscribe to TiDB Cloud, and then follow the onscreen instructions to set up your TiDB Cloud account.
- For Azure Marketplace users, you can also sign up through Azure Marketplace. To do that, search for `TiDB Cloud` in [Azure Marketplace](https://azuremarketplace.microsoft.com), subscribe to TiDB Cloud, and then follow the onscreen instructions to set up your TiDB Cloud account.
- For Google Cloud Marketplace users, you can also sign up through Google Cloud Marketplace. To do that, search for `TiDB Cloud` in [Google Cloud Marketplace](https://console.cloud.google.com/marketplace), subscribe to TiDB Cloud, and then follow the onscreen instructions to set up your TiDB Cloud account.

</CustomContent>

## Steps

If you are in the `Organization Owner` or the `Project Owner` role, you can create a {{{ .starter }}} or {{{ .essential }}} cluster as follows:

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/), and then navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page.

2. Click **Create Cluster**.

3. Select a cluster plan and the cloud provider.

    You can start with a **Starter** cluster and later upgrade to an **Essential** cluster as your needs grow. For more information, see [cluster plans](/tidb-cloud/select-cluster-tier.md).

4. Select a region where you want to host your cluster.

5. Update the default cluster name if necessary.

6. Update the capacity of the cluster.

    - **Starter** plan:

        - You can update the spending limit for your cluster. If the spending limit is set to 0, the cluster remains free. If the spending limit is greater than 0, you need to add a credit card before creating the cluster.

        - By default, each organization can create up to five [free Starter clusters](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless). To create additional Starter clusters, you must add a credit card and specify a spending limit.

    - **Essential** plan:

        - You must specify both a minimum and maximum number of Request Capacity Units (RCUs) for your cluster.

        - RCUs represent the compute resources provisioned for your workload. TiDB Cloud automatically scales your cluster within this range based on demand.

7. Click **Create**.

    The cluster creation process starts and your TiDB Cloud cluster will be created in approximately 30 seconds.

## What's next

After your cluster is created, follow the instructions in [Connect to TiDB Cloud via Public Endpoint](/tidb-cloud/connect-via-standard-connection-serverless.md) to create a password for your cluster.

> **Note:**
>
> If you do not set a password, you cannot connect to the cluster.
