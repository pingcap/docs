---
title: Deploy Automatically with GitHub
summary: Learn how to automatically deploy metadata and endpoints of your Data App with GitHub.
---

# Deploy Automatically with GitHub

By connecting your Data App to GitHub, you can automatically deploy metadata and endpoints of the Data App to your preferred GitHub repository and branch. Whenever you push changes of the Data App configuration files to a GitHub
repository, the new configurations are deployed in TiDB Cloud automatically.

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

    1. Click **Install on GitHub**, and then follow the on-screen instructions to install TiDB Cloud data services as an application on your target repository.
    2. Click **Authorize**, and then follow the on-screen instructions to authorize access to the application on GitHub.
    3. Select the target repository, branch, and directory where you want to save the the configuration files of your Data App.

    > **Note:**
    >
    > The directory you selected must be empty. If the directory already contains files of the existing Data Apps, you need to select a new directory instead or clear it.

5. Click **Confirm Connect**.
6. Check your selected directory on GitHub. If the configuration files of the Data App are committed, it indicates that your Data App is connected to GitHub successfully.

## Step 2. Configure GitHub deployment

After you connect your Data App to GitHub, the automatic deployment of changes for this Data App is enabled by default. 

- **Automatic Deployment**

    - When it is enabled, configuration changes in either GitHub or the TiDB Cloud console will be synchronized to each other.
    - When it is disabled, only configuration changes in the TiDB Cloud console is synchronized to GitHub, but configuration changes in github is not synchronized to TiDB Cloud console.

    You can stop automatic deployment at any time. Disabling automatic deployment may be useful for testing or manually deploying small changes.

- **Review Changes**

    - When it is enabled, you can review changes between this submission and the last release version, and you can either deploy or discard the changes.
    - When it is disabled, any configuration changes made in the TiDB Cloud console will be deployed directly.

## Step 3. Deploy your changes to the App configurations in GitHub automatically

After connecting to GitHub, you can make changes to your application configurations in either of the following ways:

- Option 1: Update configuration files of your Data App in GitHub.

    In your specified GitHub directory, you can find the following files:

    |File path  | Descriptions  |
    |---------|---------|
    |`data_source/cluster.json`     |  In this file, you can modify the linked clusters of this Data App. When updating this file, make sure that the linked clusters are Serverless clusters and you have access to the clusters. |
    |`http_endpoints/config.json`     | In this file, you can modify the endpoints of this Data App.        |
    |`http_endpoints/sql/sql_xx.sql`     | In the SQL file, you can modify the SQL statements of your Data App.        |
    |`datapp_config.json`  |  The configurations in this file are unchangeable. Do not modify this file using GitHub. Otherwise, the deployment triggered by this modification will fail.       |

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

## Remove Github integration

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, click the name of your target Data App to view its details.
3. In the **Connect to GitHub** area, click **Unlink**. 