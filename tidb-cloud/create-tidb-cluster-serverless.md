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

> **Note:**
>
> PostgreSQL-compatible TiDB Cloud Starter is currently available in public preview. You can select the PostgreSQL compatibility mode when creating a Starter instance.

## Steps

If you have the `Organization Owner` or `Project Owner` role, you can create a TiDB Cloud Starter or TiDB Cloud Essential instance as follows:

1. Log in to the [TiDB Cloud console](https://tidbcloud.com/), and then navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page.

2. Click **Create Resource**.

3. Select a plan.

    You can select **Starter** or **Essential**.

    For MySQL-compatible workloads, you can start with a Starter instance and later upgrade to an Essential instance as your needs grow. For more information, see [Select a Plan](/tidb-cloud/select-cluster-tier.md).

4. If you select **Starter**, choose one of the following options in the **Compatibility Mode** section:

    - **MySQL Compatible**: the default compatibility mode for TiDB Cloud Starter.
    - **PostgreSQL Compatible**: provides PostgreSQL compatibility and is currently in public preview. This compatibility mode is available only for TiDB Cloud Starter.

5. Enter a name for your instance, and then choose a cloud provider and a region where you want to host your instance.

6. (Optional) To group this instance in a project for management, click **Group Your Instance in a Project**, and then select the target project for the instance. If there is no project in your organization, you can create one by clicking **Create a Project**.

7. Configure or review the capacity and usage quota based on the selected plan and compatibility mode. For the free usage quotas of each Starter compatibility mode, see [Select a Plan](/tidb-cloud/select-cluster-tier.md#starter).

    - **MySQL-compatible Starter**:

        - You can update the spending limit for your TiDB Cloud Starter instance. If the spending limit is set to 0, the instance remains free. If the spending limit is greater than 0, you need to add a credit card before creating the instance.
        - By default, each organization can create up to five free MySQL-compatible Starter instances. To create additional instances, you must add a credit card and specify a spending limit.

    - **PostgreSQL-compatible Starter**:

        During public preview, each organization can create up to 10 free PostgreSQL-compatible Starter instances.

        When an instance reaches its free quota, excessive resource consumption might be subject to usage restrictions or service suspension. If you anticipate exceeding the free usage quota, please contact <a href="mailto:support@pingcap.com">support@pingcap.com</a> to discuss your requirements.

    - **Essential**:

        - For {{{ .essential }}} instances running on CLOUD.202603.x or later, **Elastic Mode** is selected by default. In Elastic Mode, you do not set a maximum number of RCUs. Instead, your instance uses a fixed **Baseline RCU** of 2,000 RCUs, which is the minimum number of Request Capacity Units (RCUs) you are billed for and the initial capacity for autoscaling.

        - To limit the capacity, select **Limited Mode**, and then specify the maximum number of RCUs that your instance can scale up to. {{{ .essential }}} instances on earlier versions do not support Elastic Mode; for these instances, specify both the minimum and maximum number of RCUs.

        - RCUs represent the compute resources provisioned for your workload. TiDB Cloud automatically scales your {{{ .essential }}} instance based on demand. If your workload consistently requires more than 100,000 RCUs, consider upgrading to {{{ .premium }}} to avoid potential bottlenecks.

8. Click **Create**.

The instance creation process starts, and your instance will be created in approximately 30 seconds.

## What's next

- After your {{{ .starter }}} or Essential instance is created, follow the instructions in [Connect to TiDB Cloud via Public Endpoint](/tidb-cloud/connect-via-standard-connection-serverless.md) to create a password for your instance.

    > **Note:**
    >
    > If you do not set a password, you cannot connect to the {{{ .starter }}} or Essential instance.

- To manage your instance using the TiDB Cloud CLI, see [TiDB Cloud CLI Reference (PREVIEW)](/tidb-cloud/cli-reference.md).