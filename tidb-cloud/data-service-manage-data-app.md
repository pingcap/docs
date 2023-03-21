---
title: Manage a Data App
summary: Learn how to create, view, modify, and delete a Data App in the TiDB Cloud console.
---

# Manage a Data App

A Data App in Data Service (beta) is a group of endpoints that you can use to access data for a specific application. You can configure authorization settings using API keys to restrict access to endpoints in a Data App.

This document describes how to manage your Data Apps in the TiDB Cloud console. On the [**Data Service**](https://tidbcloud.com/console/dataservice) page, you can manage all Data Apps, endpoints, and API keys.

## Create a Data App

To create a Data App for your project, perform the following steps:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/dataservice) page of your project.
2. In the left pane, click <MDSvgIcon name="icon-create-data-app" /> **Create DataApp** and update the default name if necessary.
3. The newly created Data App is added to the top of the list. A default `untitled endpoint` is created for the new Data App.

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
