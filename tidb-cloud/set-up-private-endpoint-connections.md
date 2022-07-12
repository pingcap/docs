---
title: Set Up Private Endpoint Connections
summary: Learn how to set up private endpoint connections in TiDB Cloud.
---

# Set Up Private Endpoint Connections

This document introduces what is a private endpoint, how to use it in TiDB Cloud, and the billing information.

TiDB Cloud supports using a private endpoint to privately connect your virtual private cloud (VPC) to the TiDB Cloud service hosted in an AWS VPC via the [AWS PrivateLink](https://aws.amazon.com/privatelink/?privatelink-blogs.sort-by=item.additionalFields.createdDate&privatelink-blogs.sort-order=desc), as if the service were in your own VPC. This TiDB Cloud service is called an endpoint service.

Powered by AWS PrivateLink, the endpoint connection is secure and private, and does not expose your data to the public internet.

The architecture of the private endpoint is as follows:

![Private endpoint architecture](/media/tidb-cloud/aws-private-endpoint-arch.png)

The cloud vendor AWS generates a specific DNS hostname for your endpoint service. Before you grant permissions to service consumers or specific AWS principals (AWS accounts, IAM users, and IAM roles) by default, they do not have access to your endpoint service. For more detailed definitions of the private endpoint and private endpoint service, see the following AWS documents:

- [What is AWS PrivateLink?](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html)
- [AWS PrivateLink concepts](https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html)

The relationship of a TiDB cluster in TiDB Cloud, an endpoint service, and a private endpoint is as follows:

- Each TiDB cluster corresponds to one private endpoint service, and each private endpoint service corresponds to one TiDB cluster.
- Each endpoint service corresponds to one or multiple private endpoints.
- Each TiDB cluster corresponds to one or multiple private endpoints.

> **Note:**
>
> - Currently, TiDB Cloud supports private endpoint connection only when the endpoint service is hosted in AWS. If the service is hosted in Google Cloud Platform (GCP), the private endpoint is not applicable.
> - The private endpoint support is provided only for the TiDB Cloud Dedicated Tier, not for the Developer Tier.
> - Private endpoint connection across regions is not supported.

## Why should I use private endpoint

<!-- - Enhanced security: The private endpoint connection uses a private IP and does not expose your traffic to the public internet, which avoids the risk of data leakage.
- Ease of network management: The private endpoint is easy to create and manage. You do not need to use an internet gateway, NAT device, public IP address, Amazon Direct Connect connection, or Amazon Site-to-Site VPN connection to allow communication with the service from your private subnets. -->

- Private traffic: PrivateLink-powered endpoint traffic does not traverse the public internet.  Private endpoint connection uses private IP addresses and security groups within a VPC so that the services function as if they were hosted directly within a VPC.
- Enhanced security:  Compared to VPC peering, which allows access to all resources,  PrivateLink only allows access to a specific service. Furthermore, it only allows one-way access, only VPC Endpoints can initiate a connection.
- PrivateLink Supports CIDR overlap
- Simplify Network Management:  PrivateLink is easy to use and manage because it removes the need to whitelist public IPs and manage internet connectivity with internet gateways, NAT gateways, or firewall proxies.  There is no longer a need to configure an internet gateway, VPC peering connection, or Transit VPC to enable connectivity.

## How to use private endpoint

This section describes how to create, edit, delete or terminate a private endpoint, and how to connect to a private endpoint service via private endpoint.

### Create a private endpoint

Before you create a private endpoint, make sure that you are using Dedicated Tier.

#### Step 1. Find the entrance

To find the entrance to create a private endpoint, follow one of the following ways:

- From the **Project Settings** page:

    1. On the TiDB Cloud console, click the **Project Settings** tab, then click **Private Endpoint** on the left menu, and the **Private Endpoint** page is displayed. If there is any private endpoint already created, it is displayed on this page.
    2. Click **Add** on the top right corner to open the creation page.

- From the **Connect to TiDB** dialog of an active cluster:

    1. On the TiDB Cloud console, navigate to the **Active Clusters** page and click the name of your newly created cluster.
    2. Click **Connect**. The **Connect to TiDB** dialog box is displayed.
    3. Select the **Private Endpoint** tab. If no private endpoint has been created, click **Create** on the dialog to open the creation page.

On the creation page, a flow bar is displayed indicating the steps of creating a private endpoint: **Choose Cluster** > **Service Endpoint** > **Interface Endpoint** > **Accept Endpoint Connection** > **Enable Private DNS**.

#### Step 2. Choose a TiDB cluster

After you open the creation page for a private endpoint, you are at the **Choose Cluster** step. Click the drop-down box to choose a TiDB cluster for which you want to create a private endpoint, and then click **Next**.

By default, such type of a cluster is selected:

- From the cluster page you entered the creation page
- The first cluster with no privated endpoint created for it

> **Note:**
>
> - Only the Dedicated Tier clusters are displayed in the drop-down list. No Developer Tier cluster is displayed.
> - If a cluster is being created, it is not displayed in the drop-down list. You cannot create a private endpoint for such clusters.
> - If no cluster has been created, you will see **Create Cluster** on the right side of the drop-down box. Click **Create Cluter** to create a cluster. For details, see [Create a TiDB Cluster in TiDB Cloud](/tidb-cloud/create-tidb-cluster.md).

#### Step 3. Choose a region

After you have choosen a TiDB cluster, you are at the **Service Endpoint** step. Click the drop-down box to choose a region in which the private endpoint is selected, and then click **Next**.

Note that you can only select the regions where your cluster is located. Cross-region private endpoint is currently not supported.

#### Step 4. Create an endpoint service

After you have choosen a region, you are at the **Interface Endpoint** step. When you enter this step, TiDB Cloud begins to create an endpoint service, which takes 3 to 4 minutes.

During the creation process, you need to provide your VPC ID and subnet IDs that are available from your AWS Management Console. If you do not know how to get these IDs, click **Show Instruction** and you will see two snapshots of the AWS Management Console that illustrate how to get these IDs. To fold the snapshots, click the **Hide instruction**.

After the endpoint service creation is completed, the **Next** button is available, and the placeholders in the command in the **Create VPC Interface Endpoint** area are automatically replaced with the real values.

Copy the command and run it in your terminal to create the VPC interface endpoint. Then click **Next**.

#### Step 5. Accept the endpoint connection

After you have created the endpoint service, you are at the **Accept Endpoint Connection** step. Fill in the box with the your VPC endpoint ID and click **Next**.

You can get your VPC endpoint ID from your AWS Management Console. If you do not know how to get it, click **Show Instruction** and you will see a snapshot of the AWS Management Console that illustrate how to get it. To fold the snapshot, click the **Hide instruction**.

#### Step 6. Enable Private DNS

After you have accepted the endpoint connection, you are at the **Enable Private DNS** step. Click the **Copy** button to copy the command and run it in your terminal. The `<your_vpc_endpoint_id>` placeholder is automatically replaced with the value you have provided in Step 5.

Then click **Create** to finalize the creation of the private endpoint.

### Edit a private endpoint


### Delete or terminate a private endpoint

### Connect to a private endpoint service

## Billing information

## Status information of private endpoint and private endpoint service

