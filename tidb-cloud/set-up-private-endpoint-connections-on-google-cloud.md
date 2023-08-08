---
title: Connect to TiDB Dedicated via Private Service Connect on Google Cloud
summary: Learn how to connect to your TiDB Cloud cluster via Private Service Connect on Google Cloud.
---

# Connect to TiDB Dedicated via Private Service Connect on Google Cloud

This document describes how to connect to your TiDB Dedicated cluster via Private Service Connect on Google Cloud.

> **Tip:**
>
> To learn how to connect to a TiDB Serverless cluster via private endpoint, see [Connect to TiDB Serverless via Private Endpoint](/tidb-cloud/set-up-private-endpoint-connections-serverless.md).

TiDB Cloud supports highly secure and one-way access to the TiDB Cloud service hosted in an Google Cloud VPC via the [Private Service Connect](https://cloud.google.com/vpc/docs/private-service-connect), as if the service were in your own VPC. A private endpoint is exposed in your VPC and you can create a connection to the TiDB Cloud service via the endpoint with permission.

Powered by Google Cloud Private Service Connect, the endpoint connection is secure and private, and does not expose your data to the public internet. In addition, the endpoint connection supports CIDR overlap and is easier for network management.

The architecture of the private endpoint is as follows:

![Private Service Connect architecture](/media/tidb-cloud/google-cloud-psc-endpoint-overview.png)

For more detailed definitions of the private endpoint and endpoint service, see the following Google Cloud documents:

- [Private Service Connect](https://cloud.google.com/vpc/docs/private-service-connect)
- [Using Private Service Connect to publish and consume services](https://codelabs.developers.google.com/cloudnet-psc-ilb#0)

## Restrictions

- Private endpoint connection across regions is not supported.

In most scenarios, you are recommended to use private endpoint connection over VPC peering. However, in the following scenarios, you should use VPC peering instead of private endpoint connection:

- You are using a [TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview) cluster to replicate data from a source TiDB cluster to a target TiDB cluster across regions, to get high availability. Currently, private endpoint does not support cross-region connection.
- You are using a TiCDC cluster to replicate data to a downstream cluster (such as Amazon Aurora, MySQL, and Kafka) but you cannot maintain the endpoint service on your own.
- You are connecting to PD or TiKV nodes directly.

## Set up a private endpoint with Google Cloud Private Service Connect

To connect to your TiDB Dedicated cluster via a private endpoint, complete the [prerequisites](#prerequisites) and follow these steps:

1. [Choose a TiDB cluster](#step-1-choose-a-tidb-cluster)
2. [Check the service endpoint region](#step-2-check-the-service-endpoint-region)
3. [Create an AWS interface endpoint](#step-3-create-an-aws-interface-endpoint)
4. [Accept the endpoint connection](#step-4-accept-the-endpoint-connection)
5. [Enable private DNS](#step-5-enable-private-dns)
6. [Connect to your TiDB cluster](#step-6-connect-to-your-tidb-cluster)

If you have multiple clusters, you need to repeat these steps for each cluster that you want to connect to using AWS PrivateLink.

### Prerequisites

1. Log in to the [TiDB Cloud console](https://tidbcloud.com).
2. Click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner, switch to the target project if you have multiple projects, and then click **Project Settings**.
3. On the **Project Settings** page of your project, click **Network Access** in the left navigation pane, and click the **Private Endpoint** tab.
4. Click **Add** in the upper-right corner.

### Step 1. Choose a TiDB cluster

1. Click the drop-down list and choose an available TiDB Dedicated cluster.
2. Click **Next**.

### Step 2. Check the service endpoint region

Your service endpoint region is selected by default. Have a quick check and click **Next**.

> **Note:**
>
> The default region is where your cluster is located. Do not change it. Cross-region private endpoint is currently not supported.

### Step 3. Publish a service

Publish a service in your Google Cloud VPC. For more information, see [Publish a service](https://cloud.google.com/vpc/docs/configure-private-service-connect-producer#publish-service).

### Step 4. Create an endpoint

Create an endpoint following the instructions in [Create an endpoint](https://cloud.google.com/vpc/docs/configure-private-service-connect-services#create-endpoint).

Note that the endpoint needs to be on a different vpc from the vpc where the service is published. Otherwise creation will fail.

### Step 5. Accept the endpoint connection

1. Go back to the TiDB Cloud console.
2. Fill in the box with your VPC endpoint ID on the **Create Private Endpoint** page.
3. Click **Next**.

### Step 5. Enable private DNS

Enable private DNS in Google Cloud. For more information, see [View Service Directory DNS zones](https://cloud.google.com/vpc/docs/configure-private-service-connect-services#enable-private-dns).

Then you can connect to the endpoint service.

### Step 6: Connect to your TiDB cluster

After you have enabled the private DNS, go back to the TiDB Cloud console and take the following steps:

1. On the [**Clusters**](https://tidbcloud.com/console/clusters) page, click the name of your target cluster to go to its overview page.
2. Click **Connect** in the upper-right corner. A connection dialog is displayed.
3. Select the **Private Endpoint** tab. The private endpoint you just created is displayed under **Step 1: Create Private Endpoint**.
4. Under **Step 2: Connect your application**, click the tab of your preferred connection method, and then connect to your cluster with the connection string. The placeholders `<cluster_endpoint_name>:<port>` in the connection string are automatically replaced with the real values.

> **Tip:**
>
> If you cannot connect to the cluster, the reason might be that the security group of your VPC endpoint in AWS is not properly set. See [this FAQ](#troubleshooting) for solutions.

### Private endpoint status reference

When you use private endpoint connections, the statuses of private endpoints or private endpoint services are displayed on the [**Private Endpoint** page](#prerequisites).

The possible statuses of a private endpoint are explained as follows:

- **Not Configured**: The endpoint service is created but the private endpoint is not created yet.
- **Pending**: Waiting for processing.
- **Active**: Your private endpoint is ready to use. You cannot edit the private endpoint of this status.
- **Deleting**: The private endpoint is being deleted.
- **Failed**: The private endpoint creation fails. You can click **Edit** of that row to retry the creation.

The possible statuses of a private endpoint service are explained as follows:

- **Creating**: The endpoint service is being created, which takes 3 to 5 minutes.
- **Active**: The endpoint service is created, no matter whether the private endpoint is created or not.
- **Deleting**: The endpoint service or the cluster is being deleted, which takes 3 to 5 minutes.

## Troubleshooting
