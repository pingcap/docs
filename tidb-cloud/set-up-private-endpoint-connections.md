---
title: Connect to a TiDB Dedicated Cluster via Private Endpoint with AWS
summary: Learn how to connect to your TiDB Cloud cluster via private endpoint with AWS.
---

# Connect to a TiDB Dedicated Cluster via Private Endpoint with AWS

This document describes how to connect to your TiDB Dedicated cluster via private endpoint with AWS.

> **Tip:**
>
> To learn how to connect to a TiDB Serverless cluster via private endpoint, see [Connect to TiDB Serverless via Private Endpoint](/tidb-cloud/set-up-private-endpoint-connections-serverless.md).
> To learn how to connect to a TiDB Dedicated cluster via private endpoint with Google Cloud, see [Connect to TiDB Dedicated via Private Service Connect with Google Cloud](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md).

TiDB Cloud supports highly secure and one-way access to the TiDB Cloud service hosted in an AWS VPC via the [AWS PrivateLink](https://aws.amazon.com/privatelink/?privatelink-blogs.sort-by=item.additionalFields.createdDate&privatelink-blogs.sort-order=desc), as if the service were in your own VPC. A private endpoint is exposed in your VPC and you can create a connection to the TiDB Cloud service via the endpoint with permission.

Powered by AWS PrivateLink, the endpoint connection is secure and private, and does not expose your data to the public internet. In addition, the endpoint connection supports CIDR overlap and is easier for network management.

The architecture of the private endpoint is as follows:

![Private endpoint architecture](/media/tidb-cloud/aws-private-endpoint-arch.png)

For more detailed definitions of the private endpoint and endpoint service, see the following AWS documents:

- [What is AWS PrivateLink?](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html)
- [AWS PrivateLink concepts](https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html)

## Restrictions

- Only the `Organization Owner` and the `Project Owner` roles can create private endpoints.
- The private endpoint and the TiDB cluster to be connected must be located in the same region.

In most scenarios, you are recommended to use private endpoint connection over VPC peering. However, in the following scenarios, you should use VPC peering instead of private endpoint connection:

- You are using a [TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview) cluster to replicate data from a source TiDB cluster to a target TiDB cluster across regions, to get high availability. Currently, private endpoint does not support cross-region connection.
- You are using a TiCDC cluster to replicate data to a downstream cluster (such as Amazon Aurora, MySQL, and Kafka) but you cannot maintain the endpoint service on your own.
- You are connecting to PD or TiKV nodes directly.

## Set up a private endpoint with AWS

To connect to your TiDB Dedicated cluster via a private endpoint, complete the [prerequisites](#prerequisites) and follow these steps:

1. [Select a TiDB cluster](#step-1-select-a-tidb-cluster)
2. [Create an AWS interface endpoint](#step-2-create-an-aws-interface-endpoint)
3. [Fill in your endpoint ID](#step-3-fill-in-your-endpoint-id)
4. [Enable private DNS and create connection](#step-4-enable-private-dns-and-create-connection)
5. [Connect to your TiDB cluster](#step-5-connect-to-your-tidb-cluster)

If you have multiple clusters, you need to repeat these steps for each cluster that you want to connect to using AWS PrivateLink.

### Prerequisites

1. Log in to the [TiDB Cloud console](https://tidbcloud.com).
2. Click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner, switch to the target project if you have multiple projects, and then click **Project Settings**.
3. On the **Project Settings** page of your project, click **Network Access** in the left navigation pane, and click the **Private Endpoint** > **AWS** tab to view the AWS private endpoints.
4. In the upper-right corner, click **Create Private Endpoint Connection**.

### Step 1. Select a TiDB cluster

In the **Cluster** list, select the TiDB Dedicated cluster that you want to establish a private endpoint connection.

### Step 2. Create an AWS interface endpoint

> **Note:**
>
> For each TiDB Dedicated cluster created after March 28, 2023, the corresponding endpoint service is automatically created 3 to 4 minutes after the cluster creation.

If you see the `TiDB Private Link Service is ready` message, the corresponding endpoint service is ready. You can provide the following information to create the endpoint.

1. On the **Create AWS Private Endpoint Connection** page, fill in the **Your VPC ID** and **Your Subnet IDs** fields. You can get the IDs from your [AWS Management Console](https://console.aws.amazon.com/).
2. Click **Generate Command** to get the following endpoint creation command.

    ```bash
    aws ec2 create-vpc-endpoint --vpc-id ${your_vpc_id} --region ${your_region} --service-name ${your_endpoint_service_name} --vpc-endpoint-type Interface --subnet-ids ${your_application_subnet_ids}
    ```

Then, you can create an AWS interface endpoint either using the [AWS Management Console](https://aws.amazon.com/console/) or using the AWS CLI.

<SimpleTab>
<div label="Use AWS Console">

To use the AWS Management Console to create a VPC interface endpoint, perform the following steps:

1. Sign in to the [AWS Management Console](https://aws.amazon.com/console/) and open the Amazon VPC console at [https://console.aws.amazon.com/vpc/](https://console.aws.amazon.com/vpc/).
2. Click **Endpoints** in the navigation pane, and then click **Create Endpoint** in the upper-right corner.

    The **Create endpoint** page is displayed.

    ![Verify endpoint service](/media/tidb-cloud/private-endpoint/create-endpoint-2.png)

3. Select **Other endpoint services**.
4. Enter the service name `${your_endpoint_service_name}` from the generated command (`--service-name ${your_endpoint_service_name}`).
5. Click **Verify service**.
6. Select your VPC in the drop-down list.
7. Select the availability zones where your TiDB cluster is located in the **Subnets** area.

    > **Tip:**
    >
    > If your service is spanning across more than three availability zones (AZs), you might not be able to select AZs in the **Subnets** area. This issue occurs when there is an extra AZ in your selected region in addition to the AZs where your TiDB cluster is located. In this case, contact [PingCAP Technical Support](https://docs.pingcap.com/tidbcloud/tidb-cloud-support).

8. Select your security group properly in the **Security groups** area.

    > **Note:**
    >
    > Make sure the selected security group allows inbound access from your EC2 instances on Port 4000 or a customer-defined port.

9. Click **Create endpoint**.

</div>
<div label="Use AWS CLI">

To use the AWS CLI to create a VPC interface endpoint, perform the following steps:

1. Copy the generated command and run it in your terminal.
2. Record the VPC endpoint ID you just created.

> **Tip:**
>
> - Before running the command, you need to have AWS CLI installed and configured. See [AWS CLI configuration basics](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html) for details.
>
> - If your service is spanning across more than three availability zones (AZs), you will get an error message indicating that the VPC endpoint service does not support the AZ of the subnet. This issue occurs when there is an extra AZ in your selected region in addition to the AZs where your TiDB cluster is located. In this case, you can contact [PingCAP Technical Support](https://docs.pingcap.com/tidbcloud/tidb-cloud-support).

</div>
</SimpleTab>

### Step 3. Fill in your endpoint ID

1. Go back to the TiDB Cloud console.
2. On the **Create AWS Private Endpoint Connection** page, enter your VPC endpoint ID.

### Step 4. Enable private DNS and create connection

Enable private DNS in AWS. You can either use the AWS Management Console or the AWS CLI.

<SimpleTab>
<div label="Use AWS Console">

To enable private DNS in your AWS Management Console:

1. Go to **VPC** > **Endpoints**.
2. Right-click your endpoint ID and select **Modify private DNS name**.
3. Select the **Enable for this endpoint** check box.
4. Click **Save changes**.

    ![Enable private DNS](/media/tidb-cloud/private-endpoint/enable-private-dns.png)

</div>
<div label="Use AWS CLI">

To enable private DNS using your AWS CLI, copy the command and run it in your AWS CLI.

```bash
aws ec2 modify-vpc-endpoint --vpc-endpoint-id ${your_vpc_endpoint_id} --private-dns-enabled
```

</div>
</SimpleTab>

Click **Create Private Endpoint Connection** in the TiDB Cloud console to finalize the creation of the private endpoint.

Then you can connect to your TiDB cluster.

### Step 5. Connect to your TiDB cluster

After you have enabled the private DNS, go back to the TiDB Cloud console and take the following steps:

1. On the [**Clusters**](https://tidbcloud.com/console/clusters) page, click **...** in the **Action** column.
2. Click **Connect**. A connection dialog is displayed.
3. Select the **Private Endpoint** tab. The private endpoint you just created is displayed under **Step 1: Create Private Endpoint**.
4. Under **Step 2: Connect your connection**, click **Connect**, click the tab of your preferred connection method, and then connect to your cluster with the connection string. The placeholders `<cluster_endpoint_name>:<port>` in the connection string are automatically replaced with the real values.

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

### I cannot connect to a TiDB cluster via a private endpoint after enabling private DNS. Why?

You might need to properly set the security group for your VPC endpoint in the AWS Management Console. Go to **VPC** > **Endpoints**. Right-click your VPC endpoint and select the proper **Manage security groups**. A proper security group within your VPC that allows inbound access from your EC2 instances on Port 4000 or a customer-defined port.

![Manage security groups](/media/tidb-cloud/private-endpoint/manage-security-groups.png)

### I cannot enable private DNS. An error is reported indicating that the `enableDnsSupport` and `enableDnsHostnames` VPC attributes are not enabled

Make sure that DNS hostname and DNS resolution are both enabled in your VPC setting. They are disabled by default when you create a VPC in the AWS Management Console.
