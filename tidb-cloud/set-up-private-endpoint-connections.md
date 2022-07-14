---
title: Set Up Private Endpoint Connections
summary: Learn how to set up private endpoint connections in TiDB Cloud.
---

# Set Up Private Endpoint Connections

This document introduces what is a private endpoint, how to use it in TiDB Cloud, the billing information, and the status information.

TiDB Cloud supports using a private endpoint to privately connect your virtual private cloud (VPC) to the TiDB Cloud service hosted in an AWS VPC via the [AWS PrivateLink](https://aws.amazon.com/privatelink/?privatelink-blogs.sort-by=item.additionalFields.createdDate&privatelink-blogs.sort-order=desc), as if the service were in your own VPC. This TiDB Cloud service is an endpoint service.

Powered by AWS PrivateLink, the endpoint connection is secure and private, and does not expose your data to the public internet.

The architecture of the private endpoint is as follows:

![Private endpoint architecture](/media/tidb-cloud/aws-private-endpoint-arch.png)

The cloud vendor AWS generates a specific DNS hostname for your endpoint service. Before you grant permissions to service consumers or specific AWS principals (AWS accounts, IAM users, and IAM roles), they do not have access to your endpoint service. For more detailed definitions of the private endpoint and endpoint service, see the following AWS documents:

- [What is AWS PrivateLink?](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html)
- [AWS PrivateLink concepts](https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html)

The relationship of a TiDB cluster in TiDB Cloud, an endpoint service, and a private endpoint is as follows:

- Each TiDB cluster corresponds to one endpoint service, and each endpoint service corresponds to one TiDB cluster.
- Each endpoint service corresponds to one or multiple private endpoints.
- Each TiDB cluster corresponds to one or multiple private endpoints.

> **Note:**
>
> - Currently, TiDB Cloud supports private endpoint connection only when the endpoint service is hosted in AWS. If the service is hosted in Google Cloud Platform (GCP), the private endpoint is not applicable.
> - The private endpoint support is provided only for the TiDB Cloud Dedicated Tier, not for the Developer Tier.
> - Private endpoint connection across regions is not supported.

## Why should I use private endpoint

- Private traffic: PrivateLink-powered endpoint traffic does not traverse the public internet. Private endpoint connection uses private IP addresses and security groups within a VPC so that the services function as if they were hosted directly within a VPC.
- Enhanced security: Compared to VPC peering that allows access to all resources, private endpoint only allows access to a specific service. In addition, private endpoint only allows one-way access, and only VPC Endpoints can initiate a connection.
- Private endpoint supports CIDR overlap.
- Simplified network management: Private endpoint is easy to use and manage because it removes the need to whitelist public IPs and manage internet connectivity with internet gateways, NAT gateways, or firewall proxies. There is no longer a need to configure an internet gateway, VPC peering connection, or Transit VPC to enable connectivity.

> **Note:**
>
> In most scenarios, you are recommended to use private endpoint connection over VPC peering. However, in the following scenarios, you should use VPC peering instead of private endpoint connection:
>
> - You are using a TiCDC cluster to replicate data from a source TiDB cluster to a target TiDB cluster across regions, to get high availability. Currently, private endpoint does not support cross-region connection.
> - You are using a TiCDC cluster to replicate data to a downstream cluster (such as Amazon Aurora, MySQL, and Kafka) but you cannot maintain the endpoint service on your own.
> - You are connecting to PD or TiKV nodes directly.

## How to use private endpoint

This section describes how to create, edit, delete or terminate a private endpoint, and how to connect to a private endpoint service via private endpoint.

### Create a private endpoint

Before you create a private endpoint, make sure that you are using TiDB Cloud Dedicated Tier.

Take the following steps to create a private endpoint. If you have multiple clusters, you need to repeat these steps for each cluster that you want to connect to using AWS PrivateLink.

#### Step 1. Find the entrance

To find the entrance to creating a private endpoint, follow one of the following methods:

- From the **Project Settings** page:

    1. In the TiDB Cloud console, click the **Project Settings** tab, then click **Private Endpoint** on the left menu, and the **Private Endpoint** page is displayed. If there is any existing private endpoint, it is displayed on this page.
    2. Click **Add** on the top right corner to open the creation page.

- From the **Connect to TiDB** dialog of an active cluster:

    1. In the TiDB Cloud console, navigate to the **Active Clusters** page and click the name of your newly created cluster.
    2. Click **Connect**. The **Connect to TiDB** dialog box is displayed.
    3. Select the **Private Endpoint** tab. If no private endpoint has been created, click **Create** on the dialog to open the creation page.

On the creation page, a flow bar is displayed indicating the stages of creating a private endpoint: **Choose Cluster** > **Service Endpoint** > **Interface Endpoint** > **Accept Endpoint Connection** > **Enable Private DNS**.

#### Step 2. Choose a TiDB cluster

After you open the creation page for a private endpoint, you are at the **Choose Cluster** stage. Click the drop-down list to choose a TiDB cluster for which you want to create a private endpoint, and then click **Next**.

By default, such type of a cluster is selected:

- From the cluster page you entered the creation page
- The first cluster with no privated endpoint created for it

> **Note:**
>
> - Only the Dedicated Tier clusters are displayed in the drop-down list. Developer Tier clusters are not displayed.
> - If a cluster is being created, it is not displayed in the drop-down list. You cannot create a private endpoint for such clusters.
> - If there is no existing created cluster, you will see **Create Cluster** on the right side of the drop-down list. Click **Create Cluter** to create a TiDB cluster. For detailed instructions, see [Create a TiDB Cluster in TiDB Cloud](/tidb-cloud/create-tidb-cluster.md).

#### Step 3. Choose a region

After you have choosen a TiDB cluster, you are at the **Service Endpoint** stage. Click the drop-down list to choose the region where your cluster is located, and then click **Next**.

Note that you cannot choose other regions. Cross-region private endpoint is currently not supported.

#### Step 4. Create an endpoint service

After you have choosen a region, you are at the **Interface Endpoint** stage. When you enter this stage, TiDB Cloud begins to create an endpoint service, which takes 3 to 4 minutes.

1. During the creation process, you need to provide your VPC ID and subnet IDs that are available from your AWS Management Console.

    If you do not know how to get these IDs, click **Show Instruction** and you will see two snapshots of the AWS Management Console that illustrate how to get these IDs. To fold the snapshots, click the **Hide instruction**.

    After the endpoint service creation is complete, the endpoint service name and the **Next** button are available, and the placeholders in the command in the **Create VPC Interface Endpoint** area are automatically replaced with the real values.

2. Then you need to create the VPC interface endpoint in AWS. You can either use the AWS Management Console or the AWS CLI.

    <SimpleTab>
    <div label="AWS Console" href="aws-console">

    1. In your AWS Management Console, go to the **VPC** > **Endpoint**, and click **Create Endpoint** on the upper right corner. The **Create endpoint** page is displayed.
    2. Under **Service category**, select **Other endpoint services**.
    3. Under **Service settings**, enter the endpoint service name you have obtained from the **Interface endpoint** page of TiDB Cloud console, and click **Verify service**.
    4. After the service name is verified, under **VPC**, select your VPC in the drop-down list. Then the pre-populated **Subnets** area is displayed.
    5. In the **Subnets** area, select the availabilty zones where your TiDB cluster is located. Then click **Create endpoint**.

    > **Tip:**
    >
    > If your service is spanning more than three availability zones (AZs), you might not be able to select AZs in the area. To address the issue, contact [PingCAP Technical Support](https://docs.pingcap.com/tidbcloud/tidb-cloud-support).
    >
    > In addition to the AZs where your TiDB cluster is located, if there is an extra AZ in your selected region, this issue will occur.

    </div>
    <div label="AWS CLI" href="aws-cli">

    Copy the command in the **Create VPC Interface Endpoint** area and run it in your terminal to create the VPC interface endpoint.

    > **Tip:**
    >
    > If your service is spanning more than three availability zones (AZs), an error is returned. To address the issue, contact [PingCAP Technical Support](https://docs.pingcap.com/tidbcloud/tidb-cloud-support).
    >
    > In addition to the AZs where your TiDB cluster is located, if there is an extra AZ in your selected region, this issue will occur.

    </div>
    </SimpleTab>

    Then click **Next**.

#### Step 5. Accept the endpoint connection

After you have created an endpoint service, you are at the **Accept Endpoint Connection** stage. Fill in the box with the your VPC endpoint ID and click **Next**.

You can get your VPC endpoint ID from your AWS Management Console. If you do not know how to get it, click **Show Instruction** and you will see a snapshot of the AWS Management Console that illustrates how to get it. To fold the snapshot, click the **Hide instruction**.

#### Step 6. Enable Private DNS

After you have accepted the endpoint connection, you are at the **Enable Private DNS** stage. Click the **Copy** button to copy the command and run it in your terminal. The `<your_vpc_endpoint_id>` placeholder is automatically replaced with the value you have provided in Step 5.

Then click **Create** to finalize the creation of the private endpoint.

### Edit a private endpoint

To edit a private endpoint, take these steps:

1. Open the **Private Endpoint** page. To find this page, see [Create a private endpoint - Step 1. Find the entrance](#step-1-find-the-entrance).

    All the created private endpoints are displayed on this page.

2. Click the **Edit** button next to the private endpoint you want to edit, and you will automatically enter the last stage at which you were creating a private endpoint. For example, if you were at the **Accept Endpoint Connection** stage, you will be back to this stage once you click **Edit**.

> **Note:**
>
> - You can edit a private endpoint only when the endpoint is being created (in a status other than "Active"). Once the creation process is finished, you can no longer edit the endpoint.
> - When you are editing a private endpoint on the endpoint creation page, you cannot change the cluster or region.

### Delete or terminate a private endpoint

To delete or terminate a private endpoint, use one of the following methods:

- Drop the TiDB cluster that has been configured as a private endpoint service. In this way, all private endpoints connected to the cluster will be deleted.
- Drop a single private endpoint. To do that, open the **Private Endpoint** page, click the **Terminate** button next to the private endpoint you want to terminate, and the endpoint will be terminated.

### Connect to a private endpoint service

Take the following steps to connect to a private endpoint service using a private endpoint:

1. On the TiDB Cloud console, navigate to the **Active Clusters** page and click the name of your newly created cluster.
2. Click **Connect**. The **Connect to TiDB** dialog box is displayed.
3. Select the **Private Endpoint** tab. If you have created a private endpoint, it is displayed under **Step 1: Create Private Endpoint**.
4. Under **Step 2: Connect your application**, click the tab of your preferred connection method, and then connect to your cluster with the connection string. The placeholders `<cluster_endpoint_name>:<port>` in the connection string are automatically replaced with the real values.

## Billing information

The private endpoint is available only for Dedicated Tier clusters.

The cost of private endpoint contains the following parts:

- The cost of the private endpoint: $0.01/hour per VPC per endpoint. For details, see [AWS PrivateLink pricing - Interface Endpoint pricing](https://aws.amazon.com/privatelink/pricing/?nc1=h_ls).
- The cost of endpoint service or network load balancer. For details, see [AWS Elastic Load Balancing pricing](https://aws.amazon.com/elasticloadbalancing/pricing/).
- The cost of data transfer, which is the same as the EC2 data transfer charges. For details, see [TiDB Cloud - Data transfer cost](https://docs.pingcap.com/tidbcloud/tidb-cloud-billing#data-transfer-cost) or [AWS EC2 pricing](https://aws.amazon.com/ec2/pricing/on-demand/).

## Status information of private endpoint and private endpoint service

You can see the status of a private endpoint or private endpoint service on the [**Private Endpoint** page](#step-1-find-the-entrance).

The possible statuses of a private endpoint are explained as follows:

- **Not Configured**: You have just created an endpoint service but have not yet created a private endpoint. If you click **Edit** of that row, you are directed to the **Interface Endpoint** stage of creating a private endpoint. See [Step 4. Create an endpoint service](#step-4-create-an-endpoint-service) for details.
- **Initiating**: The private endpoint is being initiated or verified after you fill in your VPC ID at the **Interface Endpoint** stage of creating a private endpoint. If you open a new **Private Endpoint** page, you will see that the **Edit** button of the row is disabled.
- **Pending**: After your VPC ID is verified at the **Interface Endpoint** stage of creating a private endpoint, you have not yet enabled the private DNS. If you click **Edit** of that row, you are directed to the **Enable Private DNS** stage of creating a private endpoint. See [Step 6. Enable Private DNS](#step-6-enable-private-dns) for details.
- **Active**: Your private endpoint is ready to use. You cannot edit the private endpoint of this status.
- **Deleting**: The private endpoint is being deleted.
- **Failed**: The private endpoint creation fails. You can click **Edit** of that row to retry the creation.

The possible statuses of a private endpoint service are explained as follows:

- **Creating**: The endpoint service is being created, which takes 3 to 5 minutes.
- **Active**: The endpoint service is created, no matter whether the private endpoint is created or not.
- **Deleting**: The endpoint service or the cluster is being deleted, which takes 3 to 5 minutes.
