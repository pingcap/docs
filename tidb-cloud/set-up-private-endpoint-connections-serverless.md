---
title: Connect to TiDB Cloud via Private Endpoint
summary: Learn how to connect to your TiDB Cloud cluster via private endpoint.
---

# Connect to TiDB Cloud via Private Endpoint

This tutorial walks you through the steps to connect to your TiDB Cloud cluster via a private endpoint on Alibaba Cloud. Connecting through a private endpoint allows secure and private communication between your services and your TiDB Cloud cluster without using the public internet.

## Restrictions

- Currently, TiDB Cloud Starter and TiDB Cloud Essential support private endpoint connections when the endpoint service is hosted on Alibaba Cloud. If the service is hosted on AWS, Google Cloud, or another cloud provider, the private endpoint is not applicable.
- Private endpoint connection across regions is not supported.

## Set up a private endpoint with Alibaba Cloud

To connect to your TiDB Cloud Starter cluster via a private endpoint, follow these steps:

1. [Choose a TiDB cluster](#step-1-choose-a-tidb-cluster)
2. [Create a VOC endpoint on Alibaba Cloud](#step-2-create-a-voc-endpoint-on-alibaba-cloud)
3. [Connect to your TiDB cluster using the private endpoint](#step-3-connect-to-your-tidb-cluster-using-the-private-endpoint)

### Step 1. Choose a TiDB cluster

1. On the [**Clusters**](https://console.tidb.io/clusters) page, click the name of your target TiDB Cloud cluster to go to its overview page.
2. Click **Connect** in the upper-right corner. A connection dialog is displayed.
3. In the **Connection Type** drop-down list, select **Private Endpoint**.
4. Take a note of **Service Name**, **Availability Zone ID**, and **Region ID**.

### Step 2. Create a VOC endpoint on Alibaba Cloud

To use the Alibaba Cloud Management Console to create a VPC interface endpoint, perform the following steps:

1. Sign in to the [Alibaba Cloud Management Console](https://account.alibabacloud.com/login/login.htm).
2. Navigate to **VPC** > **Endpoints**.
3. Under the **Interface Endpoints** tab, click **Create Endpoint**.
4. Fill out the endpoint information:
    - **Region**: select the same region as your TiDB Cloud cluster.
    - **Endpoint Name**: choose a name for the endpoint.
    - **Endpoint Type**: select **Interface Endpoint**.
    - **Endpoint Service**: select **Other Endpoint Services**.

5. Paste the **Endpoint Service Name** you copied from TiDB Cloud.
6. Click **Verify**. A green check will appear if the service is valid.
7. Choose the **VPC**, **Security Group**, and **Zone** to use for the endpoint.
8. Click **OK** to create the endpoint.
9. Wait for the endpoint status to become **Active** and the connection status to become **Connected**.

### Step 3: Connect to your TiDB cluster using the private endpoint

After you have created the interface endpoint, go back to the TiDB Cloud console and take the following steps:

1. On the [**Clusters**](https://console.tidb.io/clusters) page, click the name of your target cluster to go to its overview page.
2. Click **Connect** in the upper-right corner. A connection dialog is displayed.
3. In the **Connection Type** drop-down list, select **Private Endpoint**.
4. In the **Connect With** drop-down list, select your preferred connection method. The corresponding connection string is displayed at the bottom of the dialog.

    For the host, go to the **Endpoint Details** page in Alibaba Cloud, and copy the **Domain Name of Endpoint Service** as your host.

5. Connect to your cluster with the connection string.
