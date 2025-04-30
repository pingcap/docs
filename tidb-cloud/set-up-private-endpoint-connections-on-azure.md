---
title: Connect to a TiDB Cloud Dedicated Cluster via Azure Private Endpoint
summary: Learn how to connect to your TiDB Cloud cluster via Azure Private Endpoint.
---

# Connect to a TiDB Cloud Dedicated Cluster via Azure Private Endpoint

This document describes how to connect to your TiDB Cloud Dedicated cluster via Azure Private Endpoint.

> **Tip:**
>
> - To learn how to connect to a TiDB Dedicated cluster via private endpoint with AWS, see [Connect to TiDB Dedicated via Private Endpoint with AWS](/tidb-cloud/set-up-private-endpoint-connections.md).
> - To learn how to connect to a TiDB Dedicated cluster via private endpoint with Google Cloud, see [Connect to TiDB Dedicated via Private Service Connect with Google Cloud](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md)
> - To learn how to connect to a TiDB Serverless cluster via private endpoint, see [Connect to TiDB Serverless via Private Endpoint](/tidb-cloud/set-up-private-endpoint-connections-serverless.md).

TiDB Cloud supports highly secure and one-way access to the TiDB Cloud service hosted in an Azure virtual network via [Azure Private Link](https://learn.microsoft.com/en-us/azure/private-link/private-link-overview), as if the service were in your own virtual network. You can create a private endpoint in your virtual network, and then connect to the TiDB Cloud service via the endpoint with permission. 

Powered by Azure Private Link, the endpoint connection is secure and private, and does not expose your data to the public internet. In addition, the endpoint connection supports CIDR overlap and is easier for network management.

The architecture of Azure private endpoint is as follows:

![Azure Private Endpoint architecture](/media/tidb-cloud/azure-private-endpoint-arch.png)

For more detailed definitions of the private endpoint and endpoint service, see the following Azure documents:

- [What is Azure Private Link?](https://learn.microsoft.com/en-us/azure/private-link/private-link-overview)
- [What is a private endpoint?](https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-overview)
- [Create a private endpoint](https://learn.microsoft.com/en-us/azure/private-link/create-private-endpoint-portal?tabs=dynamic-ip)

## Restrictions

- Only the `Organization Owner` and `Project Owner` roles can create Private Endpoints.
- The private endpoint and the TiDB cluster to be connected must be located in the same region.

## Set up a private endpoint with Azure Private Link

To connect to your TiDB Cloud Dedicated cluster via a private endpoint, complete the follow these steps:

1. [Select a TiDB cluster](#step-1-select-a-tidb-cluster)
2. [Create Azure private endpoint](#step-2-create-Azure-private-endpoint)
3. [Accept endpoint](#step-3-accept-endpoint)
4. [Connect to your TiDB cluster](#step-4-connect-to-your-tidb-cluster)

If you have multiple clusters, you need to repeat these steps for each cluster that you want to connect to using Azure Private Link.

### Step 1. Select a TiDB cluster

1. On the [**Clusters**](https://tidbcloud.com/console/clusters) page, click the name of your target TiDB cluster to go to its overview page.
2. Click **Connect** in the upper-right corner. A connection dialog is displayed.
3. In the **Connection Type** drop-down list, select **Private Endpoint**, and then click **Create Private Endpoint Connection** to open the **Create Azure Private Endpoint Connection** dialog.

> **Note:**
>
> If you have already created a private endpoint connection, the active endpoint will appear in the connection dialog. To create additional private endpoint connections, navigate to the **Networking** page in the left navigation pane.

### Step 2. Create Azure private endpoint

1. In the **Create Azure Private Endpoint Connection** dialog, copy the TiDB Cloud resource ID of the private link service and leave the dialog open for later use.

> **Note:**
>
> For each TiDB Cloud Dedicated cluster, the corresponding endpoint service is automatically created 3 to 4 minutes after the cluster creation.

2. Log in to the [Azure portal](https://portal.azure.com/), and then create a private endpoint for your cluster using the copied TiDB Cloud resource ID as follows:
    1. In the Azure portal, search for **Private endpoint**, and then select **Private endpoint** in the reresult. 
    2. On the **Private endpoint** page, click **+ Create**.
    3. In the **Basics** tab, fill in the project and instance information, and then click **Next: Resource**. 
    4. In the **Resource** tab, choose **Connect to an Azure resource by resource ID or alias** as the **connection method**, paste the TiDB Cloud resource ID to the **Resource ID or alias** field, and then click **Next: Virtual Network**.
    5. Complete the rest of the configurations of this private endpoint, and then click **Create**. For more information, see [Create a private endpoint](https://learn.microsoft.com/en-us/azure/private-link/create-private-endpoint-portal?tabs=dynamic-ip#create-a-private-endpoint) in Azure documentation.

3. After the private endpoint is created, click **Go to resource**, and then do the following:

     - Click **Properties** in the left navigation pane, and copy its **Resource ID** for later use.

     ![Azure private endpoint resource id](/media/tidb-cloud/azure-private-endpoint-resource-id.png)

     - Click **DNS configuration** in the left navigation pane, and then copy its **IP address** for later use.

     ![Azure private endpoint dns ip](/media/tidb-cloud/azure-private-endpoint-dns-ip.png)

       
  

### Step 3. Accept endpoint

1. Return to the **Create Azure Private Endpoint Connection** dialog in the TiDB Cloud console, and then paste the copied **Resource ID** and **IP address** into the corresponding fields.
2. Click **Verify Endpoint** to validate the private endpoint access. If you encounter any error, follow the error message for troubleshooting, and then try again.
3. Once verification is successful, click **Accept Endpoint** to approve the connection from your private endpoint.

### Step 4. Connect to your TiDB cluster

After you have accepted the endpoint connection, you are redirected back to the connection dialog.

1. Wait for the private endpoint connection status to become Active (approximately 5 minutes). You can go to **Networking** page to check its status.
2. In the **Connect With** drop-down list, select your preferred connection method. The corresponding connection string is displayed at the bottom of the dialog.
3. Connect to your cluster with the connection string.

### Private endpoint status reference

You can view the statuses of private endpoints or private endpoint services on the **Networking** page of your cluster.

The possible statuses of a private endpoint are explained as follows:

- **Discovered**: TiDB Cloud can automatically detect your private endpoint associated with the endpoint service before accepting the request to prevent the need for creating another one.
- **Pending**: waiting for processing.
- **Active**: your private endpoint is ready to use. You cannot edit the private endpoint of this status.
- **Deleting**: the private endpoint is being deleted.
- **Failed**: the private endpoint creation fails. You can click **Edit** of that row to retry the creation.

The possible statuses of a private endpoint service are explained as follows:

- **Creating**: the endpoint service is being created, which takes 3 to 5 minutes.
- **Active**: the endpoint service is created, no matter whether the private endpoint is created or not.

## Troubleshooting

### TiDB Cloud fails to create an endpoint service. What should I do?

The endpoint service is created automatically after you open the **Create Azure Private Endpoint** page and choose the TiDB cluster. If it shows as failed or remains in the **Creating** state for a long time, submit a [support ticket](/tidb-cloud/tidb-cloud-support.md) for assistance.


### If I cancel the action during setup, what should I do before accepting the private endpoint?

The Azure private endpoint connection feature can automatically detect your private endpoints. This means if you cancel your action during the setup of a private endpoint connection, you can still view your created endpoint on the networking page. If the cancellation is unintentional, you can continue to edit it to complete the setup. If the cancellation is deliberate, you can delete the endpoint directly in the TiDB Cloud console.
