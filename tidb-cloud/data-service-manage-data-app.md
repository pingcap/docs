---
title: Manage a Data App
summary: Learn how to create, view, modify, and delete a Data App in the TiDB Cloud console.
---

# Manage a Data App

A Data App in Data Service (beta) is a group of endpoints that you can use to access data for a specific application. You can configure authorization settings using API keys to restrict access to endpoints in a Data App.

This document describes how to manage your Data Apps in the TiDB Cloud console. On the [**Data Service**](https://tidbcloud.com/console/data-service) page, you can manage all Data Apps, endpoints, and API keys.

## Create a Data App

To create a Data App for your project, perform the following steps:

1. On the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project, click <MDSvgIcon name="icon-create-data-app" /> **Create DataApp** in the left pane.
2. Enter a name for the Data App, and select clusters that you want the Data App to access.
3. (Optional) To automatically deploy metadata and endpoints of the Data App to your preferred GitHub repository and branch, expand **Connect your Data App to GitHub**, and then do the following:

    1. Click **Install on GitHub**, and then follow the on-screen instructions to install **TiDB Cloud Data Services** as an application on your target repository.
    2. Click **Authorize** to authorize access to the application on GitHub.
    3. Specify the target repository, branch, and directory where you want to save the configuration files of your Data App.

    > **Note:**
    >
    > - The directory must start with a slash. For example, `/mydata`. If the directory you specified does not exist in the target repository and branch, it will be created automatically.
    > - The combination of repository, branch, and directory represents the path of the configuration files, which must be unique among Data Apps. If the path already contains files of existing Data Apps, you need to select a new path instead.
    > - If you have created a GitHub branch based on configuration files of an existing Data App and want to import the configuration of the existing Data App to a new Data App, see [Import configurations of an existing Data App](#import-configurations-of-an-existing-data-app).

4.Click **Create Data App**.

The newly created Data App is added to the top of the list. A default `untitled endpoint` is created for the new Data App.

If you have connected your Data App to GitHub, Check your selected directory on GitHub. If the configuration files of the Data App have been committed by `tidb-cloud-data-services`, it indicates that your Data App is connected to GitHub successfully. For more information, see [Deploy Automatically with GitHub](/tidb-cloud/data-service-manage-github-integration.md).

## Modify a Data App

You can rename a Data App, and manage its API keys, linked clusters, and endpoints.

### Rename a Data App

To rename a Data App, perform the following steps:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, click the name of your target Data App to view its details.
3. In the **General** area, modify the **Name** field and click **Save**.

### Manage GitHub integration

For more information, see [Manage GitHub integration](/tidb-cloud/data-service-manage-github-integration.md).

### Manage linked clusters

You can add or remove linked clusters for a Data App. After you remove a linked cluster, the endpoints in the Data App can still access other linked clusters.

To link a cluster to a Data App, perform the following steps:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, locate your target Data App and click the name of your target Data App to view its details.
3. In the **Linked Cluster** area, click **Add Cluster**.
4. In the displayed dialog box, select a cluster from the list and click **Add**.

To remove a linked cluster from a Data App, perform the following steps:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, locate your target Data App and click the name of your target Data App to view its details.
3. In the **Linked Cluster** area, locate the target linked cluster you want to remove from the Data App, and click **Delete** in the **Action** column.
4. In the displayed dialog box, confirm the removal.

    After you remove a linked cluster, the cluster is not deleted, but the existing endpoints in the Data App cannot access it.

### Manage an API key

For more information, see [Manage an API key](/tidb-cloud/data-service-api-key.md).

### Manage an endpoint

For more information, see [Manage an endpoint](/tidb-cloud/data-service-manage-endpoint.md).

### Manage deployments

To manage deployments, perform the following steps:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, locate your target Data App and click the name of your target Data App to view its details.
3. Click **Deployment** to view the deployment information.
4. In the upper-right corner, you can click **Configure** to enable or disable **Automatic Deployment** and **Review Changes** for your Data App.

    - **Automatic Deployment**

        - This option can be enabled only when you Data App is connected to GitHub. For more information, see [Deploy Automatically with GitHub](/tidb-cloud/data-service-manage-github-integration.md#deploy-automatically-with-github).
        - When it is enabled, configuration changes in either GitHub or the TiDB Cloud console will be synchronized to each other. Whenever you push changes of the Data App configuration files to a GitHub repository, the new configurations are deployed in TiDB Cloud automatically.
        - When it is disabled, only configuration changes in the TiDB Cloud console are synchronized to GitHub, but configuration changes on GitHub is not synchronized to the TiDB Cloud console.

    - **Review Changes**

        - When it is enabled, you can review the Data App configuration changes you made in the TiDB Cloud console before the deployment. Based on the review, you can either deploy or discard the changes.
        - When it is disabled, the Data App configuration changes you made in the TiDB Cloud console are deployed directly.

5. In the **Action** column, you can edit or re-deploy your changes according to your needs.

## Delete a Data App

> **Note:**
>
> Before you delete a Data App, make sure that all endpoints are not online. Otherwise, you cannot delete the Data App. To undeploy an endpoint, refer to [Undeploy an endpoint](/tidb-cloud/data-service-manage-endpoint.md#undeploy-an-endpoint).

To delete a Data App, perform the following steps:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, locate your target Data App and click the name of your target Data App to view its details.
3. In the **Delete Data App** area, click **Delete Data App**. A dialog box for confirmation is displayed.
4. Type the name of target Data App, and then click **I understand, delete**.

    Once a Data App is deleted, the existing endpoints and API keys in the Data App are also deleted. If this Data App is connected to GitHub, deleting the App does not delete the files in the corresponding GitHub repository.
