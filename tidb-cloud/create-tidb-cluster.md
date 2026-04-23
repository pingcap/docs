---
title: Create a TiDB Cloud Dedicated Cluster
summary: Learn how to create your TiDB Cloud Dedicated cluster.
---

# Create a TiDB Cloud Dedicated Cluster

This tutorial guides you through signing up and creating a TiDB Cloud Dedicated cluster.

> **Tip:**
>
> To learn how to create a {{{ .starter }}} or {{{ .essential }}} instance, see [Create a {{{ .starter }}} or Essential Instance](/tidb-cloud/create-tidb-cluster-serverless.md).

## Before you begin

If you do not have a TiDB Cloud account, click [here](https://tidbcloud.com/signup) to sign up for an account.

- You can either sign up with email and password so that you can manage your password using TiDB Cloud, or sign up with your Google, GitHub, or Microsoft account.
- For AWS Marketplace users, you can also sign up through AWS Marketplace. To do that, search for `TiDB Cloud` in [AWS Marketplace](https://aws.amazon.com/marketplace), subscribe to TiDB Cloud, and then follow the onscreen instructions to set up your TiDB Cloud account.
- For Azure Marketplace users, you can also sign up through Azure Marketplace. To do that, search for `TiDB Cloud` in [Azure Marketplace](https://azuremarketplace.microsoft.com), subscribe to TiDB Cloud, and then follow the onscreen instructions to set up your TiDB Cloud account.
- For Google Cloud Marketplace users, you can also sign up through Google Cloud Marketplace. To do that, search for `TiDB Cloud` in [Google Cloud Marketplace](https://console.cloud.google.com/marketplace), subscribe to TiDB Cloud, and then follow the onscreen instructions to set up your TiDB Cloud account.

## Step 1. Create a TiDB Cloud Dedicated cluster

If you are in the `Organization Owner` or the `Project Owner` role, you can create a TiDB Cloud Dedicated cluster as follows:

1. Navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page.

    > **Tip:**
    >
    > If you are in multiple organizations, use the combo box in the upper-left corner to switch to your target organization first.

2. Click **Create Resource**.

3. On the **Create Resource** page, select **Dedicated**, and then configure the cluster information as follows:

    1. Select a project for your TiDB Cloud Dedicated cluster. If there is no project in your organization, you can create one by clicking **Create a Project**.
    2. Enter a name for your TiDB Cloud Dedicated cluster.
    3. Choose a cloud provider and a region where you want to host your cluster.

        > **Note:**
        >
        > - If you signed up for TiDB Cloud through [AWS Marketplace](https://aws.amazon.com/marketplace), the cloud provider is AWS, and you cannot change it in TiDB Cloud.
        > - If you signed up for TiDB Cloud through [Azure Marketplace](https://azuremarketplace.microsoft.com), the cloud provider is Azure Cloud, and you cannot change it in TiDB Cloud.
        > - If you signed up for TiDB Cloud through [Google Cloud Marketplace](https://console.cloud.google.com/marketplace), the cloud provider is Google Cloud, and you cannot change it in TiDB Cloud.

    4. Configure the [cluster size](/tidb-cloud/size-your-cluster.md) for TiDB, TiKV, and TiFlash (optional) respectively.
    5. Update the default port number if necessary.
    6. If CIDR has not been configured for this region, you need to set the CIDR. If you do not see the **Project CIDR** field, it means that CIDR has already been configured for this region.

        > **Note:**
        >
        > - TiDB Cloud will create a VPC with this CIDR when the first cluster in this region is created. All the subsequent clusters of the same project in this region will use this VPC.
        > - When setting the CIDR, avoid any conflicts with the CIDR of the VPC where your application is located. You cannot modify your CIDR once the VPC is created.

4. Confirm the cluster and billing information on the right side.

5. If you have not added a payment method, click **Add Credit Card** in the lower-right corner.

    > **Note:**
    >
    > If you signed up TiDB Cloud through [AWS Marketplace](https://aws.amazon.com/marketplace), [Azure Marketplace](https://azuremarketplace.microsoft.com), or [Google Cloud Marketplace](https://console.cloud.google.com/marketplace), you can pay through your AWS account, Azure account, or Google Cloud account directly but cannot add payment methods or download invoices in the TiDB Cloud console.

6. Click **Create**.

    Your TiDB Cloud cluster will be created in approximately 20 to 30 minutes. You will receive a notification from the TiDB Cloud console when the creation is complete.

    > **Note:**
    >
    > The cluster creation time can vary by region and might take longer than 30 minutes. If the process takes significantly longer than expected, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

## Step 2. Set the root password

After your TiDB Cloud Dedicated cluster is created, take the following steps to set the root password:

1. In the upper-right corner of your cluster overview page, click **...** and select **Password Settings**.

2. Set the root password to connect to your cluster, and then click **Save**.

    You can click **Auto-generate Password** to generate a random password. The generated password will not show again, so save your password in a secure location.

## What's next

After your TiDB Cloud Dedicated cluster is created on TiDB Cloud, you can connect to it via the methods provided in [Connect to Your TiDB Cloud Dedicated Cluster](/tidb-cloud/connect-to-tidb-cluster.md).
