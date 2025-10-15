---
title: Create a Premium instance
summary: Learn how to create a Premium instance. 
---

# Create a Premium instance

This document describes how to create a Premium instance in the [TiDB Cloud console](https://tidbcloud.com/).

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

> **Note:**
>
> Currently, TiDB Cloud Premium is only available upon request. To request this feature, click **?** in the lower-right corner of the [TiDB Cloud console](https://tidbcloud.com) and click **Request Support**. Then, fill in "Apply for TiDB Cloud Premium" in the **Description** field and click **Submit**.


## Steps

If you are in the `Organization Owner` or the `Instance Creator` role, you can create a Premium instance as follows:

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/).At the bottom of the left navigation bar, locate the "Switch to Private Preview" entry and click it to enter the Premium Preview interface. If you cannot see this entry, it might be because your organization has not been invited to the Premium Private Preview yet. In this case, please contact Tech Support.

2. Navigate to the [**TiDB Instances**] page.

3. Click **Create Instance**.

4. Input instance name .

5. Choose a cloud provider and a region where you want to host your instance.

6. Update the capacity of the instance.

    - You must specify both a minimum and maximum number of Request Capacity Units (RCUs) for your instance.

    - RCUs represent the compute resources provisioned for your workload. TiDB Cloud automatically scales your instance within this range based on demand.

7. Click **Create**.

    The instance creation process begins. If this is your first instance in the selected region, provisioning typically takes about 30 minutes. If you already have an existing instance in the region, the process is faster and usually completes within about 1 minute.

## What's next

After your instance is created, follow the instructions in [Connect to TiDB Cloud via Public Endpoint](/tidb-cloud/connect-via-standard-connection-premium.md) to create a password for your instance.

> **Note:**
>
> If you do not set a password, you cannot connect to the instance.
