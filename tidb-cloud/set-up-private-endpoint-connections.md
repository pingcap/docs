---
title: Set Up Private Endpoint Connections
summary: Learn how to set up private endpoint connections in TiDB Cloud.
---

# Set Up Private Endpoint Connections

TiDB Cloud supports highy secure and one-way access to the TiDB Cloud service hosted in an AWS VPC via the [AWS PrivateLink](https://aws.amazon.com/privatelink/?privatelink-blogs.sort-by=item.additionalFields.createdDate&privatelink-blogs.sort-order=desc), as if the service were in your own VPC. A private endpoint is exposed in your VPC and you can create a connection to the TiDB Cloud service via the endpoint with permission.

Powered by AWS PrivateLink, the endpoint connection is secure and private, and does not expose your data to the public internet. In addition, the endpoint connection supports CIDR overlap and is easier for network management.

The architecture of the private endpoint is as follows:

![Private endpoint architecture](/media/tidb-cloud/aws-private-endpoint-arch.png)

For more detailed definitions of the private endpoint and endpoint service, see the following AWS documents:

- [What is AWS PrivateLink?](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html)
- [AWS PrivateLink concepts](https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html)

## Restrictions

- Currently, TiDB Cloud supports private endpoint connection only when the endpoint service is hosted in AWS. If the service is hosted in Google Cloud Platform (GCP), the private endpoint is not applicable.
- The private endpoint support is provided only for the TiDB Cloud Dedicated Tier, not for the Developer Tier.
- Private endpoint connection across regions is not supported.

In most scenarios, you are recommended to use private endpoint connection over VPC peering. However, in the following scenarios, you should use VPC peering instead of private endpoint connection:

- You are using a TiCDC cluster to replicate data from a source TiDB cluster to a target TiDB cluster across regions, to get high availability. Currently, private endpoint does not support cross-region connection.
- You are using a [TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview) cluster to replicate data to a downstream cluster (such as Amazon Aurora, MySQL, and Kafka) but you cannot maintain the endpoint service on your own.
- You are connecting to PD or TiKV nodes directly.

## Set up private endpoint with AWS

This section describes how to set up a private endpoint with AWS PrivateLink.

Take the following steps to set up a private endpoint. If you have multiple clusters, you need to repeat these steps for each cluster that you want to connect to using AWS PrivateLink.

### Prerequisites

TiDB Cloud supports private endpoints only for Dedicated Tier clusters. You are expected to create a Dedicated Tier cluster before creating a private endpoint. For detailed instructions, see [Create a TiDB Cluster in TiDB Cloud](/tidb-cloud/create-tidb-cluster.md).

#### Step 1. Find the entrance

To find the entrance to creating a private endpoint, take the following steps:

1. On the TiDB Cloud console, click the **Project Settings** tab, then click **Private Endpoint** on the left menu, and the **Private Endpoint** page is displayed.
2. Click **Add** in the upper-right corner to open the creation page.

> **Tip:**
>
> Alternatively, you can find the entrance by following these steps:
>
> 1. In the TiDB Cloud console, navigate to the **Active Clusters** page and click the name of your newly created cluster.
> 2. Click **Connect**. The **Connect to TiDB** dialog box is displayed.
> 3. Select the **Private Endpoint** tab. If no private endpoint has been created, click **Create** on the dialog to open the creation page.

On the creation page, a flow bar is displayed indicating the stages of creating a private endpoint: **Choose Cluster** > **Service Endpoint** > **Interface Endpoint** > **Accept Endpoint Connection** > **Enable Private DNS**.

#### Step 2. Choose a TiDB cluster

Click the drop-down list to choose a TiDB cluster for which you want to create a private endpoint, and then click **Next**.

> **Note:**
>
> Before a cluster is created, it is not displayed in the drop-down list.

#### Step 3. Choose Service Endpoint Region

From the **Region** List, select the region in which you want to create the private endpoint. Then, click **Next**.

> **Note:**
>
> The default region is where your cluster is located. Do not change it. Cross-region private endpoint is currently not supported.

#### Step 4. Create an AWS Interface Endpoint

At this stage, TiDB Cloud begins creating an endpoint service, which takes 3 to 4 minutes. During the creation process, perform the following operations:

1. Fill in the **VPC ID** and **Subnet IDs** fields. You can get the IDs from your AWS Management Console.

    If you do not know how to get these IDs, click **Show Instruction** and you will see two snapshots of the AWS Management Console that illustrate how to get these IDs.

2. Take a note of the endpoint service name after the endpoint service creation is complete.

    After the endpoint service is created, the endpoint service name is available in the command in the **Create VPC Interface Endpoint** area.

    ![Endpoint service name](/media/tidb-cloud/private-endpoint/private-endpoint-service-name.png)

3. Create the VPC interface endpoint in AWS. You can either use the AWS Management Console or the AWS CLI.

    <SimpleTab>
    <div label="Use AWS Console">

    To use the AWS Management Console to create the VPC interface, perform the following steps:

    1. In your AWS Management Console, go to **VPC** > **Endpoints**, and click **Create Endpoint** in the upper-right corner. The **Create endpoint** page is displayed.

        ![Create endpoint](/media/tidb-cloud/private-endpoint/create-endpoint-1.png)

    2. Under **Service category**, select **Other endpoint services**.
    3. Under **Service settings**, enter the endpoint service name you have obtained from the **Interface endpoint** page of the TiDB Cloud console, and click **Verify service**.

        ![Verify endpoint service](/media/tidb-cloud/private-endpoint/create-endpoint-2.png)

    4. After the service name is verified, under **VPC**, select your VPC in the drop-down list. Then the pre-populated **Subnets** area is displayed.
    5. In the **Subnets** area, select the availabilty zones where your TiDB cluster is located. Then click **Create endpoint** at the bottom of the page.

        ![Create endpoint service 2](/media/tidb-cloud/private-endpoint/create-endpoint-3.png)

    > **Tip:**
    >
    > If your service is spanning across more than three availability zones (AZs), you might not be able to select AZs in the **Subnets** area. This issue occurs when there is an extra AZ in your selected region in addition to the AZs where your TiDB cluster is located. To solve the issue, contact [PingCAP Technical Support](https://docs.pingcap.com/tidbcloud/tidb-cloud-support).

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

    3. Copy the command in the **Create VPC Interface Endpoint** area and run it in your terminal to create the VPC interface endpoint. Then click **Next**.

    After the endpoint service is created, the placeholders in the command are automatically replaced with the real values.

    > **Tip:**
    >
    > - If your service is spanning across more than three availability zones (AZs), you might not be able to select AZs in the **Subnets** area. This issue occurs when there is an extra AZ in your selected region in addition to the AZs where your TiDB cluster is located. The returned error message is as follows:
    >
    >    ```
    >    An error occurred (InvalidParameter) when calling the CreateVpcEndpoint operation: The VPC endpoint service com.amazonaws.vpce.<your region>.<vpce-id> does not support the availability zone of the subnet: <corresponding subnet>
    >    ```
    >
    >    To solve the issue, contact [PingCAP Technical Support](https://docs.pingcap.com/tidbcloud/tidb-cloud-support).
    >
    > - You cannot copy the command until TiDB Cloud finishes creating endpoint service in the background.

    </div>
    </SimpleTab>

#### Step 5. Accept the endpoint connection

Fill in the box with the your VPC endpoint ID and click **Next**.

#### Step 6. Enable Private DNS

Click the **Copy** button to copy the command and run it in your AWS CLI. The `<your_vpc_endpoint_id>` placeholder is automatically replaced with the value you have provided in Step 5.

Alternatively, you can enable private DNS in your AWS Management Console. If you do not know how to do it, click **Show Instruction** and you will see a snapshots of the AWS Management Console that illustrates how to enable private DNS.

Then click **Create** to finalize the creation of the private endpoint.

#### Step 7. Connect to the endpoint service

See [Connect to TiDB cluster via private endpoint](/tidb-cloud/connect-to-tidb-cluster.md#connect-via-private-endpoint) for details.
