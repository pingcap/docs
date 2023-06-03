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
3. (Optional) To automatically deploy endpoints of the Data App to your preferred GitHub repository and branch, enable **Connect your Data App to GitHub**, and then do the following:

    1. Click **Install on GitHub**, and then follow the on-screen instructions to install **TiDB Cloud Data Service** as an application on your target repository.
    2. Click **Authorize** to authorize access to the application on GitHub.
    3. Specify the target repository, branch, and directory where you want to save the configuration files of your Data App.

        > **Note:**
        >
        > - The directory must start with a slash. For example, `/mydata`. If the directory you specified does not exist in the target repository and branch, it will be created automatically.
        > - The combination of repository, branch, and directory identifies the path of the configuration files, which must be unique among Data Apps. If your specified path is already used by another Data App, you need to specify a new path instead. Otherwise, the endpoints configured in the TiDB Cloud console for the current Data App will overwrite the files in your specified path.
        > - If your specified path contains configuration files copied from another Data App and you want to import these files to the current Data App, see [Import configurations of an existing Data App](#import-configurations-of-an-existing-data-app).

4. Click **Create Data App**.

    The newly created Data App is added to the top of the list. A default `untitled endpoint` is created for the new Data App.

5. If you have configured to connect your Data App to GitHub, check whether your Data App configuration files](/tidb-cloud/data-service-app-config-files.md) have been committed to your specified GitHub directory by `tidb-cloud-data-service`. If yes, it indicates that your Data App is connected to GitHub successfully.

    For your new Data App, **Review draft** and **Automatic deployment** are enabled by default so you can easily synchronize changes between TiDB Cloud console and GitHub and review changes before the deployment. For more information about the GitHub integration , see [Deploy your Data App changes with GitHub automatically](/tidb-cloud/data-service-manage-github-integration.md).

## Modify a Data App

You can rename a Data App, and manage its API keys, linked clusters, and endpoints.

### Rename a Data App

To rename a Data App, perform the following steps:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, click the name of your target Data App to view its details.
3. In the **Data App Properties** area, click the Edit icon, modify the **App Name** field, and then click **Save**.

### Manage GitHub connection

For more information, see [Deploy Automatically with GitHub](/tidb-cloud/data-service-manage-github-integration.md).

### Manage linked data sources

You can add or remove linked clusters for a Data App.

To link a cluster to a Data App, perform the following steps:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, locate your target Data App and click the name of your target Data App to view its details.
3. In the **Linked Data Sources** area, click **Add Cluster**.
4. In the displayed dialog box, select a cluster from the list and click **Add**.

To remove a linked cluster from a Data App, perform the following steps:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, locate your target Data App and click the name of your target Data App to view its details.
3. In the **Linked Data Sources** area, locate the target linked cluster you want to remove from the Data App, and click **Delete** in the **Action** column.
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
3. Click the **Deployment** tab to view the deployment information.
4. In the upper-right corner, click **Configure**, and then choose your desired setting of **Review draft** and **Automatic deployment**.

    - **Review draft**

        - When it is enabled, you can review the Data App changes you made in the TiDB Cloud console before the deployment. Based on the review, you can either deploy or discard the changes.
        - When it is disabled, the Data App changes you made in the TiDB Cloud console are deployed directly.

    - **Automatic deployment**

        - This option can be enabled only when your Data App is connected to GitHub. For more information, see [Deploy Automatically with GitHub](/tidb-cloud/data-service-manage-github-integration.md#deploy-automatically-with-github).
        - When it is enabled, the changes made in your specified GitHub directory can be automatically deployed in TiDB Cloud, and you can find the corresponding deployment and commit information in the Data App deployment history.
        - When it is disabled, the changes made in your specified GitHub directory will NOT deployed in TiDB Cloud, which means that the Data App are not affected by your changes in GitHub.

5. In the **Action** column, you can edit or re-deploy your changes according to your needs.

## Delete a Data App

> **Note:**
>
> Before you delete a Data App, make sure that all endpoints are not online. Otherwise, you cannot delete the Data App. To undeploy an endpoint, refer to [Undeploy an endpoint](/tidb-cloud/data-service-manage-endpoint.md#undeploy-an-endpoint).

To delete a Data App, perform the following steps:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, locate your target Data App and click the name of your target Data App to view its details.
3. In the **Danger Zone** area, click **Delete Data App**. A dialog box for confirmation is displayed.
4. Type the name of target Data App, and then click **I understand, delete**.

    Once a Data App is deleted, the existing endpoints and API keys in the Data App are also deleted. If this Data App is connected to GitHub, deleting the App does not delete the files in the corresponding GitHub repository.
