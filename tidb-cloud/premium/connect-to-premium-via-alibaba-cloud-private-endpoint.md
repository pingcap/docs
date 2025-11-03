---
title: Connect to {{{ .premium }}} via Alibaba Cloud Private Endpoint
summary: Learn how to connect to your {{{ .premium }}} instance via Alibaba Cloud private endpoint.
---

# Connect to {{{ .premium }}} via Alibaba Cloud Private Endpoint

This document describes how to connect to your {{{ .premium }}} instance via a private endpoint on Alibaba Cloud. Connecting through a private endpoint enables secure and private communication between your services and your TiDB instance without using the public internet.

> **Tip:**
>
> To learn how to connect to a {{{ .premium }}} instance via AWS PrivateLink, see [Connect to {{{ .premium }}} via AWS PrivateLink](/tidb-cloud/premium/connect-to-premium-via-aws-private-endpoint.md).

## Restrictions

- Currently, TiDB Premium supports private endpoint connections when the endpoint service is hosted on AWS or Alibaba Cloud. If the service is hosted on another cloud provider, the private endpoint is not applicable.
- Private endpoint connection across regions is not supported.

## Set up a private endpoint with Alibaba Cloud

To connect to your Premium instance via a private endpoint, follow these steps:

1. [Choose a TiDB instance](#step-1-choose-a-tidb-instance)
2. [Create a private endpoint on Alibaba Cloud](#step-2-create-a-private-endpoint-on-alibaba-cloud)
3. [Connect to your TiDB instance using the private endpoint](#step-3-connect-to-your-tidb-instance-using-the-private-endpoint)
4. [Accept the endpoint and create the endpoint connection](#step-4-accept-the-endpoint-and-create-the-endpoint-connection)

### Step 1. Choose a TiDB instance

1. On the [**TiDB Instances**](https://{{{.console-url}}}/instances) page, click the name of your target TiDB instance to go to its overview page.
2. Click **Connect** in the upper-right corner. A connection dialog is displayed.
3. In the **Connection Type** drop-down list, select **Private Endpoint**.
4. Take a note of **Service Name**, **Availability Zone ID**, and **Region ID**.

### Step 2. Create a private endpoint on Alibaba Cloud

To use the Alibaba Cloud Management Console to create a VPC interface endpoint, perform the following steps:

1. Sign in to the [Alibaba Cloud Management Console](https://account.alibabacloud.com/login/login.htm).
2. Navigate to **VPC** > **Endpoints**.
3. Click the **Interface Endpoints** tab, and then click **Create Endpoint**.
4. Fill in the endpoint details:
    - **Region**: select the same region as your TiDB Cloud instance.
    - **Endpoint Name**: enter a name for the endpoint.
    - **Endpoint Type**: choose **Interface Endpoint**.
    - **Endpoint Service**: select **Other Endpoint Services**.
5. Paste the **Endpoint Service Name** you copied from TiDB Cloud.
6. Click **Verify**. A green check mark indicates that the service is valid.
7. Choose the **VPC**, **Security Group**, and **Zone** to associated with the endpoint.
8. Click **OK** to create the endpoint.
9. Wait until the endpoint status is **Active** and the connection status is **Connected**.

After creating the interface endpoint, navigate to the **EndPoints** page and select the newly created endpoint.

- In the **Basic Information** section, copy the **Endpoint ID**. You will use this value later as the *Endpoint Resource ID*.

- In the **Domain name of Endpoint Service** section, copy the **Default Domain Name**. You will use this value later as the *Domain Name*.

    ![AliCloud private endpoint Information](/media/tidb-cloud/private-endpoint/alicloud-private-endpoint-info.png)

### Step 3. Accept the endpoint and create the endpoint connection

1. Return to the **Create Alibaba Cloud Private Endpoint Connection** dialog in the TiDB Cloud console.

2. Paste the *Endpoint Resource ID* and *Domain Name* that you copied earlier into the corresponding fields.

3. Click **Create Private Endpoint Connection** to accept the connection from your private endpoint.

### Step 4. Connect to your TiDB instance

After you have accepted the endpoint connection, you are redirected back to the connection dialog.

1. Wait for the private endpoint connection status to become **Active** (approximately 5 minutes). To check the status, navigate to the **Networking** page by clicking **Settings** > **Networking** in the left navigation pane.

2. In the **Connect With** drop-down list, select your preferred connection method. The corresponding connection string is displayed at the bottom of the dialog.

3. Connect to your instance with the connection string.

## Private endpoint status reference

To view the statuses of private endpoints or private endpoint services, navigate to the **Networking** page by clicking **Settings** > **Networking** in the left navigation pane.

The possible statuses of a private endpoint are explained as follows:

- **Pending**: waiting for processing.
- **Active**: the private endpoint is ready for use.
- **Deleting**: the private endpoint is being deleted.
- **Failed**: the private endpoint creation fails. You can delete the Endpoint connection and create a new one.

The possible statuses of a private endpoint service are explained as follows:

- **Creating**: the endpoint service is being created, which takes 3 to 5 minutes.
- **Active**: the endpoint service is created, no matter whether the private endpoint is created or not.