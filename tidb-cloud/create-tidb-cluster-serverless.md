---
title: Create a {{{ .starter }}} or Essential Instance
summary: Learn how to create a {{{ .starter }}} or {{{ .essential }}} instance.
---

# Create a {{{ .starter }}} or Essential Instance

This document describes how to create a {{{ .starter }}} or {{{ .essential }}} instance in the [TiDB Cloud console](https://tidbcloud.com/).

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

If you are in the `Organization Owner` or the `Project Owner` role, you can create a {{{ .starter }}} or {{{ .essential }}} instance as follows:

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/), and then navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page.

2. Click **Create Resource**.

3. Select a plan.

    You can start with a **Starter** instance and later upgrade to an **Essential** instance as your needs grow. For more information, see [Select a Plan](/tidb-cloud/select-cluster-tier.md).

4. Choose a cloud provider and a region where you want to host your instance.

5. Update the default instance name if necessary.

6. Update the capacity of the instance.

    - **Starter** plan:

        - You can update the spending limit for your {{{ .starter }}} instance. If the spending limit is set to 0, the instance remains free. If the spending limit is greater than 0, you need to add a credit card before creating the {{{ .starter }}} instance.

        - By default, each organization can create up to five [free {{{ .starter }}} instances](/tidb-cloud/select-cluster-tier.md#starter). To create additional {{{ .starter }}} instances, you must add a credit card and specify a spending limit.

    - **Essential** plan:

        - You must specify both a minimum and maximum number of Request Capacity Units (RCUs) for your {{{ .essential }}} instance.

        - RCUs represent the compute resources provisioned for your workload. TiDB Cloud automatically scales your {{{ .essential }}} instance within this range based on demand.

7. Click **Create**.

    The instance creation process starts and your instance will be created in approximately 30 seconds.

## What's next

After your {{{ .starter }}} or Essential instance is created, follow the instructions in [Connect to TiDB Cloud via Public Endpoint](/tidb-cloud/connect-via-standard-connection-serverless.md) to create a password for your instance.

> **Note:**
>
> If you do not set a password, you cannot connect to the {{{ .starter }}} or Essential instance.
