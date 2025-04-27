---
title: Connect to a TiDB Cloud Dedicated Cluster via Private Endpoint with Azure
summary: Learn how to connect to your TiDB Cloud cluster via Azure Private Endpoint.
---

# Connect to a TiDB Dedicated Cluster via Azure Private Endpoint

This document describes how to connect to your TiDB Dedicated cluster via Azure Private Endpoint.

> **Tip:**
>
> - To learn how to connect to a TiDB Dedicated cluster via private endpoint with AWS, see [Connect to TiDB Dedicated via Private Endpoint with AWS](/tidb-cloud/set-up-private-endpoint-connections.md).
> - To learn how to connect to a TiDB Dedicated cluster via private endpoint with Google Cloud, see [Connect to TiDB Dedicated via Private Service Connect with Google Cloud](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md)
> - To learn how to connect to a TiDB Serverless cluster via private endpoint, see [Connect to TiDB Serverless via Private Endpoint](/tidb-cloud/set-up-private-endpoint-connections-serverless.md).

TiDB Cloud supports highly secure and one-way access to the TiDB Cloud service hosted in an Azure VPC via the [Azure Private Link](https://learn.microsoft.com/en-us/azure/private-link/private-link-overview), as if the service were in your own VPC. A private endpoint is exposed in your VPC and you can create a connection to the TiDB Cloud service via the endpoint with permission. 

Powered by Azure Private Link, the endpoint connection is secure and private, and does not expose your data to the public internet. In addition, the endpoint connection supports CIDR overlap and is easier for network management.

The architecture of Azure private endpoint is as follows:

![Private Service Connect architecture](/media/tidb-cloud/google-cloud-psc-endpoint-overview.png)

For more detailed definitions of the private endpoint and endpoint service, see the following Azure documents:

- [What is Azure Private Link?](https://learn.microsoft.com/en-us/azure/private-link/private-link-overview)
- [What is a private endpoint?](https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-overview)
- [Create a private endpoint](https://learn.microsoft.com/en-us/azure/private-link/create-private-endpoint-portal?tabs=dynamic-ip)

## Restrictions

- Only the `Organization Owner` and `Project Owner` roles can create Google Cloud Private Service Connect endpoints.
- The private endpoint and the TiDB cluster to be connected must be located in the same region.

## Set up a private endpoint with Azure Private Link

To connect to your TiDB Cloud Dedicated cluster via a private endpoint, complete the follow these steps:

1. [Choose a TiDB cluster](#step-1-choose-a-tidb-cluster)
2. [Create Azure private endpoint](#step-2-provide-the-information-for-creating-an-endpoint)
3. [Accept endpoint](#step-3-accept-endpoint-access)
4. [Connect to your TiDB cluster](#step-4-connect-to-your-tidb-cluster)

If you have multiple clusters, you need to repeat these steps for each cluster that you want to connect to using Azure Private Link.

### Step 1. Choose a TiDB cluster

1. On the [Clusters](https://tidbcloud.com/console/clusters) page, click the name of your target TiDB cluster to go to its overview page.
2. Click Connect in the upper-right corner. A connection dialog is displayed.
3. In the Connection Type drop-down list, select Private Endpoint, and then click Create Private Endpoint Connection.


### Step 2. Provide the information for creating an endpoint

1. Provide the following information to generate the command for private endpoint creation:
    - **Google Cloud Project ID**: the Project ID associated with your Google Cloud account. You can find the ID on the [Google Cloud **Dashboard** page](https://console.cloud.google.com/home/dashboard).
    - **Google Cloud VPC Name**: the name of the VPC in your specified project. You can find it on the [Google Cloud **VPC networks** page](https://console.cloud.google.com/networking/networks/list).
    - **Google Cloud Subnet Name**: the name of the subnet in the specified VPC. You can find it on the **VPC network details** page.
    - **Private Service Connect Endpoint Name**: enter a unique name for the private endpoint that will be created.
2. After entering the information, click **Generate Command**.
3. Copy the command.
4. Go to [Google Cloud Shell](https://console.cloud.google.com/home/dashboard) to execute the command.

### Step 3. Accept endpoint access

After executing the command in Google Cloud Shell successfully, go back to the TiDB Cloud console and then click **Accept Endpoint Access**.

If you see an error `not received connection request from endpoint`, make sure that you have copied the command correctly and successfully executed it in your Google Cloud Shell.

### Step 4. Connect to your TiDB cluster

After you have accepted the endpoint connection, take the following steps to connect to your TiDB cluster:

1. On the [**Clusters**](https://tidbcloud.com/console/clusters) page, click **...** in the **Action** column.
2. Click **Connect**. A connection dialog is displayed.
3. Select the **Private Endpoint** tab. The private endpoint you just created is displayed. Copy the command to connect to the TiDB cluster.

### Private endpoint status reference

When you use private endpoint connections, the statuses of private endpoints or private endpoint services are displayed on the [**Private Endpoint** page](#prerequisites).

The possible statuses of a private endpoint are explained as follows:

- **Pending**: waiting for processing.
- **Active**: your private endpoint is ready to use. You cannot edit the private endpoint of this status.
- **Deleting**: the private endpoint is being deleted.
- **Failed**: the private endpoint creation fails. You can click **Edit** of that row to retry the creation.

The possible statuses of a private endpoint service are explained as follows:

- **Creating**: the endpoint service is being created, which takes 3 to 5 minutes.
- **Active**: the endpoint service is created, no matter whether the private endpoint is created or not.

## Troubleshooting

### TiDB Cloud fails to create an endpoint service. What should I do?

The endpoint service is created automatically after you open the **Create Google Cloud Private Endpoint** page and choose the TiDB cluster. If it shows as failed or remains in the **Creating** state for a long time, submit a [support ticket](/tidb-cloud/tidb-cloud-support.md) for assistance.

### Fail to create an endpoint in Google Cloud. What should I do?

To troubleshoot the issue, you need to review the error message returned by Google Cloud Shell after you execute the private endpoint creation command. If it is a permission-related error, you must grant the necessary permissions before retrying.

### I cancelled some actions. What should I do to handle cancellation before accepting endpoint access?

Unsaved drafts of cancelled actions will not be retained or displayed. You need to repeat each step when creating a new private endpoint in the TiDB Cloud console next time.

If you have already executed the command to create a private endpoint in Google Cloud Shell, you need to manually [delete the corresponding endpoint](https://cloud.google.com/vpc/docs/configure-private-service-connect-services#delete-endpoint) in the Google Cloud console.

### Why can't I see the endpoints generated by directly copying the service attachment in the TiDB Cloud console?

In the TiDB Cloud console, you can only view endpoints that are created through the command generated on the **Create Google Cloud Private Endpoint** page.

However, endpoints generated by directly copying the service attachment (that is, not created through the command generated in the TiDB Cloud console) are not displayed in the TiDB Cloud console.
