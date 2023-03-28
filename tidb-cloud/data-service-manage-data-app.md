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

## Modify a Data App

You can rename a Data App, and manage its API keys, linked clusters, and endpoints.

### Rename a Data App

To rename a Data App, navigate to the [**Data Service**](https://tidbcloud.com/console/dataservice) page, and do one of the following:

- In the left pane, locate your target Data App, click **...** > **Rename**, and enter a new name.

- In the left pane, click the name of your target Data App to view its details. In the **Basic Settings** area, modify the **Name** field and click **Save**.

### Manage linked clusters

<!--TODO: add a new area: **Linked Cluster**-->

You can add or remove linked clusters for a Data App. After you remove a linked cluster from, the endpoints in the Data App can still access other linked clusters.

<!--TODO: add a new button: **Add Cluster**-->

To add a linked cluster to a Data App, perform the following steps:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/dataservice) page of your project.
2. In the left pane, locate your target Data App and click the name of your target Data App to view its details.
3. In the **Linked Cluster** area, click **Add Cluster**.
4. In the displayed dialog box, select a cluster from the list and click **Add**.

<!--TODO: add a new button: Linked Cluster > Action > Delete-->

To remove a linked cluster from a Data App, perform the following steps:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/dataservice) page of your project.
2. In the left pane, locate your target Data App and click the name of your target Data App to view its details.
3. In the **Linked Cluster** area, locate the target linked cluster you want to remove from the Data App, and click **Delete** in the **Action** column.
4. In the displayed dialog box, click **I understand, remove** to confirm the removal.

    After you remove a linked cluster, the cluster is not deleted, but the existing endpoints in the Data App cannot access it.

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
2. In the left pane, locate your target Data App, and click **...** > **Delete**. The **Confirm deletion of DataApp** dialog box is displayed.
3. Click **Delete** to confirm the deletion.

    Once a Data App is deleted, the existing endpoints and API keys in the Data App are also deleted.
