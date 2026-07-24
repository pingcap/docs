---
title: Connect to {{{ .starter }}} or Essential via AWS PrivateLink
summary: Learn how to connect to your {{{ .starter }}} or Essential instance via private endpoint.
---

# Connect to {{{ .starter }}} or Essential via AWS PrivateLink

This document describes how to connect to your {{{ .starter }}} or {{{ .essential }}} instance via AWS PrivateLink.

> **Tip:**
>
> - To learn how to connect to a TiDB Cloud Dedicated cluster via private endpoint with AWS, see [Connect to a TiDB Cloud Dedicated Cluster via AWS PrivateLink](/tidb-cloud/set-up-private-endpoint-connections.md).
> - To learn how to connect to a TiDB Cloud Dedicated cluster via private endpoint with Azure, see [Connect to a TiDB Cloud Dedicated Cluster via Azure Private Link](/tidb-cloud/set-up-private-endpoint-connections-on-azure.md).
> - To learn how to connect to a TiDB Cloud Dedicated cluster via private endpoint with Google Cloud, see [Connect to a TiDB Cloud Dedicated Cluster via Google Cloud Private Service Connect](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md).

TiDB Cloud supports highly secure and one-way access to the TiDB Cloud service hosted in an AWS VPC via the [AWS PrivateLink](https://aws.amazon.com/privatelink/?privatelink-blogs.sort-by=item.additionalFields.createdDate&privatelink-blogs.sort-order=desc), as if the service were in your own VPC. A private endpoint is exposed in your VPC and you can create a connection to the TiDB Cloud service via the endpoint with permission.

Powered by AWS PrivateLink, the endpoint connection is secure and private, and does not expose your data to the public internet. In addition, the endpoint connection supports CIDR overlap and is easier for network management.

The architecture of the private endpoint is as follows:

![Private endpoint architecture](/media/tidb-cloud/aws-private-endpoint-arch.png)

For more detailed definitions of the private endpoint and endpoint service, see the following AWS documents:

- [What is AWS PrivateLink?](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html)
- [AWS PrivateLink concepts](https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html)

## Restrictions

- Currently, TiDB Cloud supports AWS PrivateLink connections only when the endpoint service is hosted in AWS. If the service is hosted in other cloud providers, the AWS PrivateLink connection is not applicable.
- Cross-region private endpoint connections is not supported.

## Prerequisites

Make sure that DNS hostnames and DNS resolution are both enabled in your AWS VPC settings. They are disabled by default when you create a VPC in the [AWS Management Console](https://console.aws.amazon.com/).

## Choose an endpoint model

Depending on your TiDB Cloud plan, choose the appropriate private endpoint model:

- For {{{ .starter }}} instances or for {{{ .essential }}} instances created before July 1, 2026, use the [**endpoint shared model**](#set-up-a-private-endpoint-with-aws-endpoint-shared-model). In this model, a single private endpoint can be shared by multiple {{{ .starter }}} or {{{ .essential }}} instances in the same AWS Region and VPC.
- For {{{ .essential }}} instances created starting July 1, 2026, use the [**endpoint exclusive model**](#set-up-a-private-endpoint-with-aws-endpoint-exclusive-model). In this model, each {{{ .essential }}} instance uses its own standalone private endpoint. This model eliminates the need to include the [account prefix](/tidb-cloud/select-cluster-tier.md#user-name-prefix) when connecting, but you need to repeat the setup steps for each {{{ .essential }}} instance.

## Set up a private endpoint with AWS (endpoint shared model)

To connect to your {{{ .starter }}} or {{{ .essential }}} instance via a private endpoint using the shared model, follow these steps:

1. [Choose a {{{ .starter }}} or Essential instance](#step-1-choose-a-tidb-instance)
2. [Create an AWS interface endpoint](#step-2-create-an-aws-interface-endpoint)
3. [Authorize your private endpoint in TiDB Cloud (optional)](#step-3-authorize-your-private-endpoint-in-tidb-cloud-optional)
4. [Connect to your {{{ .starter }}} or Essential instance](#step-4-connect-to-your-tidb)

### Step 1. Choose a {{{ .starter }}} or Essential instance {#step-1-choose-a-tidb-instance}

1. On the [**My TiDB**](https://tidbcloud.com/tidbs) page, click the name of your target {{{ .starter }}} or {{{ .essential }}} instance to go to its overview page.
2. Click **Connect** in the upper-right corner. A connection dialog is displayed.
3. In the **Connection Type** drop-down list, select **Private Endpoint**.
4. Take a note of **Service Name**, **Availability Zone ID**, and **Region ID**.

    > **Note:**
    >
    > For each VPC in an AWS region, you only need to create one private endpoint. The endpoint can be used by all {{{ .starter }}} or {{{ .essential }}} instances in the same VPC of that AWS region, but cannot be shared across VPCs.

### Step 2. Create an AWS interface endpoint

<SimpleTab>
<div label="Use AWS Console">

To use the AWS Management Console to create a VPC interface endpoint, perform the following steps:

1. Sign in to the [AWS Management Console](https://aws.amazon.com/console/) and open the Amazon VPC console at [https://console.aws.amazon.com/vpc/](https://console.aws.amazon.com/vpc/).
2. Click **Endpoints** in the navigation pane, and then click **Create Endpoint** in the upper-right corner.

    The **Create endpoint** page is displayed.

    ![Verify endpoint service](/media/tidb-cloud/private-endpoint/create-endpoint-2.png)

3. Select **Endpoint services that use NLBs and GWLBs**.
4. Enter the service name that you found in [step 1](#step-1-choose-a-tidb-instance).
5. Click **Verify service**.
6. Select your VPC in the drop-down list. Expand **Additional settings** and select the **Enable DNS name** checkbox.
7. In the **Subnets** area, select the availability zone where your {{{ .starter }}} or Essential instance is located, and select the Subnet ID.
8. Select your security group properly in the **Security groups** area.

    > **Note:**
    >
    > Make sure the selected security group allows inbound access from your EC2 instances on port 4000.

9. Click **Create endpoint**.

</div>
<div label="Use AWS CLI">

To use the AWS CLI to create a VPC interface endpoint, perform the following steps:

1. To get the **VPC ID** and **Subnet ID**, navigate to your AWS Management Console, and locate them in the relevant sections. Make sure that you fill in the **Availability Zone ID** that you found in [step 1](#step-1-choose-a-tidb-instance).
2. Copy the command provided below, replace the relevant arguments with the information you obtained, and then execute it in your terminal.

```bash
aws ec2 create-vpc-endpoint --vpc-id ${your_vpc_id} --region ${region_id} --service-name ${service_name} --vpc-endpoint-type Interface --subnet-ids ${your_subnet_id}
```

> **Tip:**
>
> Before running the command, you need to have AWS CLI installed and configured. See [AWS CLI configuration basics](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html) for details.

</div>
</SimpleTab>

Then you can connect to the endpoint service with the private DNS name.

### Step 3. Authorize your private endpoint in TiDB Cloud (optional)

> **Note:**
>
> This step is optional. You only need to configure **Authorized Networks** when you want to restrict access to specific private endpoint connections. If no rules are configured, all private endpoint connections are allowed by default.

After creating the AWS interface endpoint, you can authorize it for your target {{{ .starter }}} or {{{ .essential }}} instance to restrict access.

1. On the [**My TiDB**](https://tidbcloud.com/tidbs) page, click the name of your target {{{ .starter }}} or {{{ .essential }}} instance to go to its overview page.
2. Click **Settings** > **Networking** in the left navigation pane.
3. Scroll down to the **Private Endpoint** section and then locate the **Authorized Networks** table.
4. Click **Add Rule** to add a firewall rule.

    - **Endpoint Service Name**: paste the service name you got from [Step 1](#step-1-choose-a-tidb-instance).
    - **Firewall Rule Name**: enter a name to identify this connection.
    - **Your VPC Endpoint ID**: paste your 22-character VPC Endpoint ID from the AWS Management Console (starts with `vpce-`).

    > **Tip:**
    >
    > - If you leave the **Authorized Networks** table empty, all private endpoint connections are allowed by default.
    > - To allow all private endpoint connections from your cloud region (for testing or open access), enter a single asterisk (`*`) in the **Your VPC Endpoint ID** field.

5. Click **Submit**.

### Step 4. Connect to your {{{ .starter }}} or Essential instance {#step-4-connect-to-your-tidb}

After you have created the interface endpoint, go back to the TiDB Cloud console and take the following steps:

1. On the [**My TiDB**](https://tidbcloud.com/tidbs) page, click the name of your target {{{ .starter }}} or Essential instance to go to its overview page.
2. Click **Connect** in the upper-right corner. A connection dialog is displayed.
3. In the **Connection Type** drop-down list, select **Private Endpoint**.
4. In the **Connect With** drop-down list, select your preferred connection method. The corresponding connection string is displayed at the bottom of the dialog.
5. Connect to your {{{ .starter }}} or Essential instance with the connection string.

> **Tip:**
>
> If you cannot connect to the {{{ .starter }}} or Essential instance, the reason might be that the security group of your VPC endpoint in AWS is not properly set. See [this FAQ](#troubleshooting) for solutions.
>
> When creating a VPC endpoint, if you encounter an error `private-dns-enabled cannot be set because there is already a conflicting DNS domain for gatewayXX-privatelink.XX.prod.aws.tidbcloud.com in the VPC vpc-XXXXX`, a private endpoint already exists in that VPC. You do not need to create another one for the same private DNS name.

## Set up a private endpoint with AWS (endpoint exclusive model)

> **Note:**
>
> Currently, the endpoint exclusive model is available only for {{{ .essential }}} instances created starting July 1, 2026, in certain AWS regions. If it is not available for your instance, you can use the [endpoint shared model](#set-up-a-private-endpoint-with-aws-endpoint-shared-model) instead.

In the endpoint exclusive model, each {{{ .essential }}} instance uses its own standalone private endpoint. This model eliminates the need to include the [account prefix](/tidb-cloud/select-cluster-tier.md#user-name-prefix) when connecting, but you need to repeat the setup steps for each {{{ .essential }}} instance.

To connect to a {{{ .essential }}} instance via a private endpoint using the exclusive model, take the following steps:

1. [Select a {{{ .essential }}} instance](#step-1-select-an-essential-instance)
2. [Create an AWS interface endpoint](#step-2-create-an-aws-interface-endpoint-exclusive-model)
3. [Create a private endpoint connection](#step-3-create-a-private-endpoint-connection-exclusive-model)
4. [Enable private DNS](#step-4-enable-private-dns-exclusive-model)
5. [Connect to your {{{ .essential }}} instance](#step-5-connect-to-your-essential-instance)

If you have multiple instances, you need to repeat these steps for each instance that you want to connect to using AWS PrivateLink.

### Step 1. Select a {{{ .essential }}} instance {#step-1-select-an-essential-instance}

1. On the [**My TiDB**](https://tidbcloud.com/tidbs) page of your TiDB Cloud console, click the name of your target {{{ .essential }}} instance to go to its overview page.
2. Click **Connect** in the upper-right corner. A connection dialog is displayed.
3. In the **Connection Type** drop-down list, select **Private Endpoint**, and then click **Create Private Endpoint Connection**.

> **Note:**
>
> If you have already created a private endpoint connection, the active endpoint will appear in the connection dialog. To create additional private endpoint connections, navigate to the **Networking** page by clicking **Settings** > **Networking** in the left navigation pane.

### Step 2. Create an AWS interface endpoint {#step-2-create-an-aws-interface-endpoint-exclusive-model}

> **Note:**
>
> For each {{{ .essential }}} instance, the corresponding endpoint service is automatically created 3 to 4 minutes after the instance creation.

In the connection dialog, if you see the `TiDB Private Link Service is ready` message, the corresponding endpoint service is ready. You can provide the following information to create the endpoint.

1. In the connection dialog, click **How to Generate VPC Endpoint ID**, and then fill in the **Your VPC ID** and **Your Subnet IDs** fields. You can find these IDs from your [AWS Management Console](https://console.aws.amazon.com/). For multiple subnets, enter the IDs separated by spaces.

2. Click **Generate Command** to get the following endpoint creation command.

    ```bash
    aws ec2 create-vpc-endpoint --vpc-id ${your_vpc_id} --region ${your_region} --service-name ${your_endpoint_service_name} --vpc-endpoint-type Interface --subnet-ids ${your_application_subnet_ids}
    ```

Then, you can create an AWS interface endpoint either using the AWS CLI or using the [AWS Management Console](https://aws.amazon.com/console/).

<SimpleTab>
<div label="Use AWS CLI">

To use the AWS CLI to create a VPC interface endpoint, perform the following steps:

1. Copy the generated command and run it in your terminal.
2. Record the VPC endpoint ID you just created.

> **Tip:**
>
> - Before running the command, you need to have AWS CLI installed and configured. See [AWS CLI configuration basics](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html) for details.
>
> - If your service spans across more than three availability zones (AZs), you will get an error message indicating that the VPC endpoint service does not support the AZ of the subnet. This issue occurs when there is an extra AZ in your selected region in addition to the AZs where your {{{ .essential }}} instance is located. In this case, you can contact [PingCAP Technical Support](https://docs.pingcap.com/tidbcloud/tidb-cloud-support).

</div>
<div label="Use AWS Console">

To use the AWS Management Console to create a VPC interface endpoint, perform the following steps:

1. Sign in to the [AWS Management Console](https://aws.amazon.com/console/) and open the Amazon VPC console at [https://console.aws.amazon.com/vpc/](https://console.aws.amazon.com/vpc/).
2. Click **Endpoints** in the navigation pane, and then click **Create Endpoint** in the upper-right corner.

    The **Create endpoint** page is displayed.

    ![Verify endpoint service](/media/tidb-cloud/private-endpoint/create-endpoint-2.png)

3. In the **Endpoint settings** area, fill in a name tag if needed, and then select the **Endpoint services that use NLBs and GWLBs** option.
4. In the **Service settings** area, enter the service name `${your_endpoint_service_name}` from the generated command (`--service-name ${your_endpoint_service_name}`).
5. Click **Verify service**.
6. In the **Network settings** area, select your VPC in the drop-down list.
7. In the **Subnets** area, select the availability zones where your {{{ .essential }}} instance is located.

    > **Tip:**
    >
    > If your service spans across more than three availability zones (AZs), you might not be able to select AZs in the **Subnets** area. This issue occurs when there is an extra AZ in your selected region in addition to the AZs where your {{{ .essential }}} instance is located. In this case, contact [PingCAP Technical Support](https://docs.pingcap.com/tidbcloud/tidb-cloud-support).

8. In the **Security groups** area, select your security group properly.

    > **Note:**
    >
    > Make sure the selected security group allows inbound access from your EC2 instances on port `4000` or a customer-defined port.

9. Click **Create endpoint**.

</div>
</SimpleTab>

### Step 3. Create a private endpoint connection {#step-3-create-a-private-endpoint-connection-exclusive-model}

1. Go back to the TiDB Cloud console.
2. On the **Create AWS Private Endpoint Connection** page, enter your VPC endpoint ID.
3. Click **Create Private Endpoint Connection**.

> **Tip:**
>
> You can view and manage private endpoint connections on the **Networking** page of your target {{{ .essential }}} instance. To access this page, click **Settings** > **Networking** in the left navigation pane.

### Step 4. Enable private DNS {#step-4-enable-private-dns-exclusive-model}

Enable private DNS in AWS. You can either use the AWS CLI or the AWS Management Console.

<SimpleTab>
<div label="Use AWS CLI">

To enable private DNS using your AWS CLI, copy the following `aws ec2 modify-vpc-endpoint` command from the **Create Private Endpoint Connection** page and run it in your AWS CLI.

```bash
aws ec2 modify-vpc-endpoint --vpc-endpoint-id ${your_vpc_endpoint_id} --private-dns-enabled
```

Alternatively, you can find the command on the **Networking** page of your instance. Locate the private endpoint and click **...** > **Enable DNS** in the **Action** column.

</div>
<div label="Use AWS Console">

To enable private DNS in your AWS Management Console:

1. Go to **VPC** > **Endpoints**.
2. Right-click your endpoint ID and select **Modify private DNS name**.
3. Select the **Enable for this endpoint** check box.
4. Click **Save changes**.

    ![Enable private DNS](/media/tidb-cloud/private-endpoint/enable-private-dns.png)

</div>
</SimpleTab>

### Step 5. Connect to your {{{ .essential }}} instance {#step-5-connect-to-your-essential-instance}

After you have accepted the private endpoint connection, you are redirected back to the connection dialog.

1. Wait for the private endpoint connection status to change from **System Checking** to **Active** (approximately 5 minutes).
2. In the **Connect With** drop-down list, select your preferred connection method. The corresponding connection string is displayed at the bottom of the dialog.
3. Connect to your instance using the connection string.

> **Tip:**
>
> If you cannot connect to the instance, the reason might be that the security group of your VPC endpoint in AWS is not properly set. See [this FAQ](#troubleshooting) for solutions.

## Troubleshooting

### I cannot connect to a {{{ .starter }}} or Essential instance via a private endpoint after enabling private DNS. Why?

You might need to properly set the security group for your VPC endpoint in the AWS Management Console. Go to **VPC** > **Endpoints**. Right-click your VPC endpoint and select the proper **Manage security groups**. A proper security group within your VPC that allows inbound access from your EC2 instances on Port 4000 or a customer-defined port.

![Manage security groups](/media/tidb-cloud/private-endpoint/manage-security-groups.png)
