---
title: Manage a Data App
summary: Learn how to create, view, modify, and delete a Data App in the TiDB Cloud console.
---

# Manage a Data App

A Data App in Data Service (beta) is a group of endpoints that you can use to access data for a specific application. You can configure authorization settings using API keys to restrict access to endpoints in a Data App.

This document describes how to manage your Data Apps in the TiDB Cloud console. On the [**Data Service**](https://tidbcloud.com/console/dataservice) page, you can manage all Data Apps, endpoints, and API keys.

## Create a Data App

To create a Data App for your project, perform the following steps:

<!--TODO: Add the icon to website-docs/MDSvgIcon.tsx-->

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/dataservice) page of your project.
2. In the left pane, click <svg width="16" height="16" viewBox="0 -2 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M20.6397 7.27783L12.4797 12.0001M12.4797 12.0001L12.4798 21.5001M12.4797 12.0001L9.83976 10.4723L8.51977 9.7084M21.1198 12.0001V7.94153C21.1198 7.59889 21.1198 7.42757 21.0713 7.27477C21.0284 7.13959 20.9583 7.01551 20.8657 6.91082C20.761 6.79248 20.6173 6.70928 20.3297 6.54288L13.2257 2.43177C12.9535 2.27421 12.8173 2.19543 12.6732 2.16454C12.5456 2.13721 12.414 2.13721 12.2864 2.16454C12.1422 2.19543 12.0061 2.27421 11.7338 2.43177L9.92124 3.33908M15.0017 20.5406L13.2257 21.5684C12.9535 21.726 12.8173 21.8047 12.6732 21.8356C12.5456 21.863 12.414 21.863 12.2864 21.8356C12.1422 21.8047 12.0061 21.726 11.7338 21.5684L5.75977 17.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path><path d="M19.1998 21V15M16.3198 18H22.0798" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path><path d="M3.07206 3.8C3.07206 3.51997 3.07206 3.37996 3.12438 3.273C3.1704 3.17892 3.24383 3.10243 3.33415 3.0545C3.43682 3 3.57124 3 3.84006 3H6.14406C6.41289 3 6.5473 3 6.64998 3.0545C6.74029 3.10243 6.81372 3.17892 6.85974 3.273C6.91206 3.37996 6.91206 3.51997 6.91206 3.8V6.2C6.91206 6.48003 6.91206 6.62004 6.85974 6.727C6.81372 6.82108 6.74029 6.89757 6.64998 6.9455C6.5473 7 6.41289 7 6.14406 7H3.84006C3.57124 7 3.43682 7 3.33415 6.9455C3.24383 6.89757 3.1704 6.82108 3.12438 6.727C3.07206 6.62004 3.07206 6.48003 3.07206 6.2V3.8Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path><path d="M2 11.6134C2 11.3334 2 11.1934 2.05232 11.0865C2.09834 10.9924 2.17177 10.9159 2.26208 10.8679C2.36476 10.8134 2.49917 10.8134 2.768 10.8134H5.072C5.34082 10.8134 5.47524 10.8134 5.57792 10.8679C5.66823 10.9159 5.74166 10.9924 5.78768 11.0865C5.84 11.1934 5.84 11.3334 5.84 11.6134V14.0134C5.84 14.2935 5.84 14.4335 5.78768 14.5404C5.74166 14.6345 5.66823 14.711 5.57792 14.759C5.47524 14.8134 5.34082 14.8134 5.072 14.8134H2.768C2.49917 14.8134 2.36476 14.8134 2.26208 14.759C2.17177 14.711 2.09834 14.6345 2.05232 14.5404C2 14.4335 2 14.2935 2 14.0134V11.6134Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg> **Create DataApp** and update the default name if necessary.
3. The newly created Data App is added to the top of the list. A default endpoint called **New Endpoint** is created for the new Data App.

## View a Data App

In the left pane of the [**Data Service**](https://tidbcloud.com/console/dataservice) page, click the name of your target Data App to view its details. The following areas are displayed:

- **Basic Settings**:

    - **Name**: the name of the Data App.
    - **ID**: the ID of the Data App (read-only).

- **API Key**:

    In this area, you can manage API keys for the Data App. A table lists all API keys with the following fields:

    - **Public Key**: the public key of the API key.
    - **Private Key**: the private key of the API key.
    - **Description**: the description of the API key.
    - **Action**: you can edit the description of the key or delete the key.

## Modify a Data App

You can rename a Data App, and manage its endpoints and API keys.

### Rename a Data App

To rename a Data App, navigate to the [**Data Service**](https://tidbcloud.com/console/dataservice) page, and do one of the following:

- In the left pane, locate your target Data App, click **...** > **Rename**, and enter a new name.

- In the left pane, click the name of your target Data App to view its details. In the **Basic Settings** area, modify the **Name** field and click **Save**.

### Manage an API key

For more information, see [Manage an API key](/tidb-cloud/data-service-api-key.md).

### Manage an endpoint

For more information, see [Manage an endpoint](/tidb-cloud/data-service-manage-endpoint.md).

## Delete a Data App

> **Note:**
>
> Before you delete a Data App, make sure that all endpoints are not online. Otherwise, you cannot delete the Data App. To undeploy an endpoint, refer to [Undeploy an endpoint](/tidb-cloud/data-service-manage-endpoint.md#undeploy-an-endpoint).

To delete a Data App, perform the following steps:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/dataservice) page of your project.
2. In the left pane, locate your target Data App, and click **...** > **Delete**. The **Confirm deletion of service** dialog box is displayed.
3. Click **Delete** to confirm the deletion.

    Once a Data App is deleted, the existing endpoints and API keys in the Data App are also deleted.
