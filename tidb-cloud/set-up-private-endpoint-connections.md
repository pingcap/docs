---
title: Set Up Private Endpoint Connections
summary: Learn how to set up private endpoint connections in TiDB Cloud.
---

# Set Up Private Endpoint Connections

TiDB Cloud supports highy secure and one-way access to the TiDB Cloud service hosted in an AWS VPC via the [AWS PrivateLink](https://aws.amazon.com/privatelink/?privatelink-blogs.sort-by=item.additionalFields.createdDate&privatelink-blogs.sort-order=desc), as if the service were in your own VPC. A private endpoint is exposed in your VPC and you can create a connection to the TiDB Cloud service via the endpoint with permission.

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

## Use private endpoint with AWS

This section describes how to create, edit, delete or terminate a private endpoint, and how to connect to a private endpoint service via private endpoint.

### Prerequisites

TiDB Cloud supports private endpoints only Dedicated Tier clusters. You are expected to create a Dedicated Tier cluster before creating a private endpoint. For detailed instructions, see [Create a TiDB Cluster in TiDB Cloud](/tidb-cloud/create-tidb-cluster.md).

### Create a private endpoint

Take the following steps to create a private endpoint. If you have multiple clusters, you need to repeat these steps for each cluster that you want to connect to using AWS PrivateLink.

#### Step 1. Find the entrance

To find the entrance to creating a private endpoint, take one of the following methods:

- From the **Project Settings** page:

    1. On the TiDB Cloud console, click the **Project Settings** tab, then click **Private Endpoint** on the left menu, and the **Private Endpoint** page is displayed. If there is any existing private endpoint, it is displayed on this page.
    2. Click **Add** in the upper-right corner to open the creation page.

- From the **Connect to TiDB** dialog of an active cluster:

    1. In the TiDB Cloud console, navigate to the **Active Clusters** page and click the name of your newly created cluster.
    2. Click **Connect**. The **Connect to TiDB** dialog box is displayed.
    3. Select the **Private Endpoint** tab. If no private endpoint has been created, click **Create** on the dialog to open the creation page.

On the creation page, a flow bar is displayed indicating the stages of creating a private endpoint: **Choose Cluster** > **Service Endpoint** > **Interface Endpoint** > **Accept Endpoint Connection** > **Enable Private DNS**.

#### Step 2. Choose a TiDB cluster

After you open the creation page for a private endpoint, you are at the **Choose Cluster** stage. Click the drop-down list to choose a TiDB cluster for which you want to create a private endpoint, and then click **Next**.

> **Note:**
>
> Before a cluster is created, it is not displayed in the drop-down list. You cannot create a private endpoint for a cluster that is not created.

#### Step 3. Choose Service Endpoint Region

After you have choosen a TiDB cluster, you are at the **Service Endpoint** stage. From the **Region** List, select the region in which you want to create the private endpoint. Then, click **Next**.

> **Note:**
>
> The default region is where your cluster is located. Do not change it. Cross-region private endpoint is currently not supported.

#### Step 4. Create an AWS Interface Endpoint

After you have choosen a region, you are at the **Interface Endpoint** stage. When you enter this stage, TiDB Cloud begins to create an endpoint service, which takes 3 to 4 minutes.

1. During the creation process, you need to provide your VPC ID and subnet IDs that are available from your AWS Management Console.

    If you do not know how to get these IDs, click **Show Instruction** and you will see two snapshots of the AWS Management Console that illustrate how to get these IDs. To fold the snapshots, click the **Hide instruction**.

    After the endpoint service creation is complete, the endpoint service name and the **Next** button are available, and the placeholders in the command in the **Create VPC Interface Endpoint** area are automatically replaced with the real values.

2. Then you need to create the VPC interface endpoint in AWS. You can either use the AWS Management Console or the AWS CLI.

    <SimpleTab>
    <div label="Use AWS Console">

    To use the AWS Management Console to create the VPC interface, perform the following steps:

    1. In your AWS Management Console, go to **VPC** > **Endpoint**, and click **Create Endpoint** in the upper-right corner. The **Create endpoint** page is displayed.
    2. Under **Service category**, select **Other endpoint services**.
    3. Under **Service settings**, enter the endpoint service name you have obtained from the **Interface endpoint** page of the TiDB Cloud console, and click **Verify service**.
    4. After the service name is verified, under **VPC**, select your VPC in the drop-down list. Then the pre-populated **Subnets** area is displayed.
    5. In the **Subnets** area, select the availabilty zones where your TiDB cluster is located. Then click **Create endpoint**.

    > **Tip:**
    >
    > If your service is spanning across more than three availability zones (AZs), you might not be able to select AZs in the **Subnets** area. To solve the issue, contact [PingCAP Technical Support](https://docs.pingcap.com/tidbcloud/tidb-cloud-support).
    >
    > In addition to the AZs where your TiDB cluster is located, if there is an extra AZ in your selected region, this issue will occur.

    </div>
    <div label="AWS CLI">

    To use the AWS CLI to create an AWS Interface Endpoint, perform the following steps:

    1. Install AWS Command Line Interface (AWS CLI).

        ```bash
        curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
        unzip awscliv2.zip
        sudo ./aws/install
        ```

    2. Configure AWS CLI according to your account information. To get the information required by AWS CLI, see [AWS CLI configuration basics](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html).

        ```bash
        aws configure
        ```

    3. Copy the command in the **Create VPC Interface Endpoint** area and run it in your terminal to create the VPC interface endpoint.

    > **Tip:**
    >
    > - If your service is spanning across more than three availability zones (AZs), an error is returned. To resolve the issue, contact [PingCAP Technical Support](https://docs.pingcap.com/tidbcloud/tidb-cloud-support).
    >
    >     In addition to the AZs where your TiDB cluster is located, if there is an extra AZ in your selected region, this issue will occur.
    >
    > - You cannot copy the command until TiDB Cloud finishes creating endpoint service in the background.

    </div>
    </SimpleTab>

    Then click **Next**.

#### Step 5. Accept the endpoint connection

After you have created an endpoint service, you are at the **Accept Endpoint Connection** stage. Fill in the box with the your VPC endpoint ID and click **Next**.

You can get your VPC endpoint ID from your AWS Management Console. If you do not know how to get it, click **Show Instruction** and you will see a snapshot of the AWS Management Console that illustrates how to get it. To fold the snapshot, click the **Hide instruction**.

#### Step 6. Enable Private DNS

After you have accepted the endpoint connection, you are at the **Enable Private DNS** stage. Click the **Copy** button to copy the command and run it in your AWS CLI. The `<your_vpc_endpoint_id>` placeholder is automatically replaced with the value you have provided in Step 5.

Then click **Create** to finalize the creation of the private endpoint.

### Connect to a private endpoint service

Take the following steps to connect to a private endpoint service using a private endpoint:

1. In the TiDB Cloud console, navigate to the **Active Clusters** page and click the name of your newly created cluster.
2. Click **Connect**. The **Connect to TiDB** dialog box is displayed.
3. Select the **Private Endpoint** tab. If you have created a private endpoint, it is displayed under **Step 1: Create Private Endpoint**.
4. Under **Step 2: Connect your application**, click the tab of your preferred connection method, and then connect to your cluster with the connection string. The placeholders `<cluster_endpoint_name>:<port>` in the connection string are automatically replaced with the real values.

## Billing information

The private endpoint is available only for Dedicated Tier clusters.

The cost of private endpoint contains the following parts:

- The cost of the private endpoint: $0.01/hour per VPC per endpoint. For details, see [AWS PrivateLink pricing - Interface Endpoint pricing](https://aws.amazon.com/privatelink/pricing/?nc1=h_ls).
- The cost of endpoint service or network load balancer. For details, see [AWS Elastic Load Balancing pricing](https://aws.amazon.com/elasticloadbalancing/pricing/).
- The cost of data transfer, which is the same as the EC2 data transfer charges. For details, see [TiDB Cloud - Data transfer cost](https://docs.pingcap.com/tidbcloud/tidb-cloud-billing#data-transfer-cost) or [AWS EC2 pricing](https://aws.amazon.com/ec2/pricing/on-demand/).
