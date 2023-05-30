---
title: Deploy Automatically with GitHub
summary: Learn how to automatically deploy metadata and endpoints of your Data App with GitHub.
---

# Deploy Automatically with GitHub

By connecting your Data App to GitHub, you can automatically deploy metadata and endpoints of the Data App to your preferred GitHub repository and branch. Whenever you push changes of the Data App configuration files to a GitHub repository, the new configurations are deployed in TiDB Cloud automatically.

This document describes how to manage the GitHub integration of a Data App in the TiDB Cloud console.

## Before you begin

Before you connect a Data App to GitHub, make sure that you have the following:

- A GitHub account.
- A GitHub repository with your target branch and directory.

## Step 1. Connect your Data App to GitHub

You can connect your Data App to GitHub when you create the App. For more information, see [Create a Data App](/tidb-cloud/data-service-manage-data-app.md)

If you do not enable that during the app creation, you can still enable it as follows:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, click the name of your target Data App to view its details.
3. In the **Connect to GitHub** area, click **Connect**. A dialog box for connection settings are displayed.
4. In the dialog box, perform the following steps:

    1. Click **Install on GitHub**, and then follow the on-screen instructions to install TiDB Cloud Data Services as an application on your target repository.
    2. Click **Authorize**, and then follow the on-screen instructions to authorize access to the application on GitHub.
    3. Select the target repository, branch, and directory where you want to store the configuration files of your Data App.

    > **Note:**
    >
    > The combination of repository, branch, and directory represents the path of the configuration files, which must be unique among Data Apps. If the path already contains files of existing Data Apps, you need to select a new path instead. If you have created a GitHub branch based on configuration files of an existing Data App and want to import the configuration of the existing Data App to a new Data App, see [Import configurations of an existing Data App](#import-configurations-of-an-existing-data-app).

5. Click **Confirm Connect**.
6. Check your selected directory on GitHub. If the configuration files of the Data App have been committed by `tidb-cloud-data-services`, it indicates that your Data App is connected to GitHub successfully.

    In your GitHub directory, you can find the following configuration files:

    |File path  | Descriptions  |
    |---------|---------|
    |`data_source/cluster.json`     |  This file specifies the linked clusters of this Data App. |
    |`http_endpoints/config.json`     | This file specifies the endpoints of this Data App.   |
    |`http_endpoints/sql/sql_xx.sql`     | If SQL statements have been written for your endpoints, the `http_endpoints/sql` directory contains the SQL files.      |
    |`datapp_config.json`  |  This file contains the ID, name, and type information of the Data APP. |

## Step 2. Configure GitHub deployment

After you connect a Data App to GitHub, you can configure whether to enable **Automatic Deployment** and **Review Changes**.

> **Tip:**
>
> If you have connected your Data App to GitHub during cluster creation, the following configurations are enabled by default for the Data App.

- **Automatic Deployment**

    - When it is enabled, configuration changes in either GitHub or the TiDB Cloud console will be synchronized to each other.
    - When it is disabled, only configuration changes in the TiDB Cloud console is synchronized to GitHub, but configuration changes in github is not synchronized to TiDB Cloud console.

    You can stop automatic deployment at any time. Disabling automatic deployment may be useful for testing or manually deploying small changes.

- **Review Changes**

    - When it is enabled, you can review changes between this submission and the last release version, and you can either deploy or discard the changes.
    - When it is disabled, any configuration changes made in the TiDB Cloud console will be deployed directly.

## Step 3. Deploy your changes to the App configurations to GitHub automatically

If **Automatic Deployment** is disabled, you can only update [the Data App settings](/tidb-cloud/data-service-manage-data-app.md) in the TiDB Cloud console.

If **Automatic Deployment** is enabled, you can make changes to your application configurations in either GitHub or the TiDB Cloud console:

- Option 1: Update configuration files of your Data App in GitHub.

    |File path  | Notes for the updates  |
    |---------|---------|
    |`data_source/cluster.json`     |  When updating this file, make sure that the linked clusters are Serverless clusters and you have access to the clusters. You can get the ID of a cluster from the cluster URL. For example, if the cluster URL is `https://tidbcloud.com/console/clusters/1379661944646164631/overview`, the cluster ID is `1379661944646164631`.|
    |`http_endpoints/config.json`     | When modifying the endpoints, make sure that you follow the rules described in [Develop an endpoint](/tidb-cloud/data-service-manage-endpoint.md#develop-an-endpoint).       |
    |`http_endpoints/sql/sql_xx.sql`     | To add or remove the SQL files in `http_endpoints/sql` directory, you need to update the corresponding endpoint configurations as well.    |
    |`datapp_config.json`  |  **DO NOT** modify this file using GitHub. Otherwise, the deployment triggered by this modification will fail.       |

    After the changes are committed, TiDB Cloud will automatically deploy the Data App with the latest changes. You can view the deployment status in the deployment history.

- Option 2: Update [the Data App settings](/tidb-cloud/data-service-manage-data-app.md) in the TiDB Cloud console. For example, you can rename the Data APP, modify endpoints, and modify linked clusters.

    After the changes are made in the TiDB Cloud console, perform the following steps:

    1. Click **Deploy** in the upper-right corner.
    2. If **Review Changes** is enabled, a dialog is displayed for you to review the changes you made. Otherwise, skip this step.

        If you find anything needs to be updated in the dialog, you can close this dialog and make further changes, or you can click **Discard Changes** to revert the changes and make changes again.

    3. (Optional) Type a message for the deployment.
    4. click **Deploy and Push to GitHub**. The deployment status will be displayed in the top banner.

> **Note:**
>
> If you have modify configurations in GitHub and TiDB Cloud console at the same time, the deployment triggered by the changes in GitHub will success, while the deployment triggered by the changes in the TiDB Cloud console will fail due to the conflicts in the changes. In this case, after the successful deployment of changes in GitHub, you need to discard the changes made in the TiDB Cloud console, and then make the further changes if necessary.

## View deployment history

While not recommended, you might stop or re-start deployment at any time. View the full deployment history.

## Import configurations of an existing Data App

If you have created a GitHub branch based on configuration files of an existing Data App, you can import the configuration of the existing Data App to a new Data App as follows:

1. Create a new Data App without connecting to GitHub.
2. Get the ID of the new Data App.
3. In the new branch, update the Data App ID in the `datapp_config.json` file to the new ID, and then modify the linked cluster and endpoints information if necessary.
4. Follow the steps in [Connect your Data App to GitHub](#step-1-connect-your-data-app-to-github) to specify directory of the new branch for the new Data App.

## Remove Github integration

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, click the name of your target Data App to view its details.
3. In the **Connect to GitHub** area, click **Unlink**.