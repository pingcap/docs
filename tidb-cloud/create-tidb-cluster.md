---
title: Create a TiDB Cluster
summary: Learn how to create your TiDB cluster.
---

# Create a TiDB Cluster

This tutorial guides you through signing up and creating a TiDB cluster.

## Step 1. Create a TiDB Cloud account

1. If you do not have a TiDB Cloud account, click [here](https://tidbcloud.com/signup) to sign up for an account.

    - You can either sign up with email and password so that you can manage your password using TiDB Cloud, or sign up with your Google, GitHub, or Microsoft account.
    - For AWS Marketplace users, you can also sign up through AWS Marketplace. To do that, search for `TiDB Cloud` in [AWS Marketplace](https://aws.amazon.com/marketplace), subscribe to TiDB Cloud, and then follow the onscreen instructions to set up your TiDB Cloud account.
    - For Google Cloud Marketplace users, you can also sign up through Google Cloud Marketplace. To do that, search for `TiDB Cloud` in [Google Cloud Marketplace](https://console.cloud.google.com/marketplace), subscribe to TiDB Cloud, and then follow the onscreen instructions to set up your TiDB Cloud account.

2. [Log in](https://tidbcloud.com/) to your TiDB Cloud account.

## Step 2. Select a cluster option

TiDB Cloud provides the following two options. Before creating a TiDB cluster, consider which option suits your need better:

- TiDB Serverless (Beta)

    TiDB Serverless is a fully managed service of TiDB. It is still in the beta phase and cannot be used in production. However, you can use TiDB Serverless clusters for non-production workloads such as prototype applications, hackathons, academic courses, or to provide a temporary data service for your datasets.

- TiDB Dedicated

    TiDB Dedicated is dedicated for production use with the benefits of cross-zone high availability, horizontal scaling, and [HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing).

For more information about the two options, see [Select Your Cluster Option](/tidb-cloud/select-cluster-tier.md).

## Step 3. Use your default project or create a new project

If you are an organization owner, once you log in to TiDB Cloud, you have a default project. For more information about projects, see [Organizations and projects](/tidb-cloud/manage-user-access.md#organizations-and-projects).

- For free trial users, you can rename the default project if needed.
- For TiDB Dedicated users, you can either rename the default project or create a new project if needed.

1. Click <MDSvgIcon name="icon-top-organization" /> **Organization** in the upper-right corner of the TiDB Cloud console.

2. Click **Organization Settings**.

    The **Projects** tab is displayed by default.

3. Do one of the following:

    - To rename the default project, click **Rename** in the **Actions** column.
    - To create a project, click **Create New Project**, enter a name for your project, and then click **Confirm**.

4. To return to the cluster page, click the TiDB Cloud logo in the upper-left corner of the window.

If you are a project member, you can access only the specific projects to which your organization owner invited you, and you cannot create new projects. To check which project you belong to, take the following steps:

1. Click <MDSvgIcon name="icon-top-organization" /> **Organization** in the upper-right corner of the TiDB Cloud console.

2. Click **Organization Settings**.

    The **Projects** tab is displayed by default.

3. To return to the cluster page, click the TiDB Cloud logo in the upper-left corner of the window.

## Step 4. Create a TiDB cluster

<SimpleTab>
<div label="TiDB Serverless">

To create a TiDB Serverless cluster, take the following steps:

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page.

2. Click **Create Cluster**.

3. On the **Create Cluster** page, **Serverless** is selected by default.

4. The cloud provider of TiDB Serverless is AWS. You can select an AWS region where you want to host your cluster.

5. (Optional) Change the spend limit if you plan to use more storage and compute resources than the [free quota](/tidb-cloud/select-cluster-tier.md#usage-quota). If you have not added a payment method, you need to add a credit card after editing the limit.

    > **Note:**
    >
    > For each organization in TiDB Cloud, you can create a maximum of five TiDB Serverless clusters by default. To create more TiDB Serverless clusters, you need to add a credit card and set a [spend limit](/tidb-cloud/tidb-cloud-glossary.md#spend-limit) for the usage.

6. Update the default cluster name if necessary, and then click **Create**.

    The cluster creation process starts and your TiDB Cloud cluster will be created in approximately 30 seconds.

7. After the cluster is created, follow the instructions in [Connect via Standard Connection](/tidb-cloud/connect-via-standard-connection.md#tidb-serverless) to create a password for your cluster.

    > **Note:**
    >
    > If you do not set a password, you cannot connect to the cluster.

</div>

<div label="TiDB Dedicated">

To create a TiDB Dedicated cluster, take the following steps:

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.

    > **Tip:**
    >
    > If you have multiple projects, you can view the project list and switch to another project from the ☰ hover menu in the upper-left corner.

2. Click **Create Cluster**.

3. On the **Create Cluster** page, select **Dedicated**, and then configure the cluster information as follows:

    1. Choose a cloud provider and a region.

        > **Note:**
        >
        > - If you signed up for TiDB Cloud through [AWS Marketplace](https://aws.amazon.com/marketplace), the cloud provider is AWS, and you cannot change it in TiDB Cloud.
        > - If you signed up for TiDB Cloud through [Google Cloud Marketplace](https://console.cloud.google.com/marketplace), the cloud provider is GCP, and you cannot change it in TiDB Cloud.

    2. Configure the [cluster size](/tidb-cloud/size-your-cluster.md) for TiDB, TiKV, and TiFlash (optional) respectively.
    3. Update the default cluster name and port number if necessary.
    4. If this is the first cluster of your current project and CIDR has not been configured for this project, you need to set the project CIDR. If you do not see the **Project CIDR** field, it means that CIDR has already been configured for this project.

        > **Note:**
        >
        > When setting the project CIDR, avoid any conflicts with the CIDR of the VPC where your application is located. You cannot modify your project CIDR once it is set.

4. Confirm the cluster and billing information on the right side.

5. If you have not added a payment method, click **Add Credit Card** in the lower-right corner.

    > **Note:**
    >
    > If you signed up TiDB Cloud through [AWS Marketplace](https://aws.amazon.com/marketplace) or [Google Cloud Marketplace](https://console.cloud.google.com/marketplace), you can pay through your AWS account or Google Cloud account directly but cannot add payment methods or download invoices in the TiDB Cloud console.

6. Click **Create**.

    Your TiDB Cloud cluster will be created in approximately 20 to 30 minutes.

7. In the upper-right corner of your cluster overview page, click **...** and select **Security Settings**.

8. Set the root password and allowed IP addresses to connect to your cluster, and then click **Apply**.

</div>
</SimpleTab>
