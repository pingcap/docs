---
title: Deploy Automatically with GitHub
summary: Learn how to create, develop, test, deploy, and delete an endpoint in a Data App in the TiDB Cloud console.
---

# Deploy Automatically with GitHub

By connecting your Data App to GitHub, you can automatically deploy metadata and endpoints of the Data App to your preferred GitHub repository and branch. Whenever you push changes of the Data App configuration files to a GitHub
repository.

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

## Step 2. Deploy your changes to the App configurations in GitHub automatically

After connecting to GitHub, you can make changes to your application configurations in either of the following ways:

- Update configuration files of your Data App in GitHub.

    After the changes are committed, TiDB Cloud will automatically deploy the Data App with the latest changes.

- Update [the Data App settings](/tidb-cloud/data-service-manage-data-app.md) in the TiDB Cloud console. For example, you can rename the Data APP, modify endpoints, and modify linked clusters.

    After the changes are made in the TiDB Cloud console, perform the following steps:

    1. Click **Review changes** in the upper-right corner.
    2. In the displayed dialog, review the changes you made. If anything needs to be updated, you can close this dialog and make further changes, or you can click **Discard Changes** to revert the changes and make changes again.
    3. If the changes look fine, type a message for the deployment (optional) and click **Deploy and Push to GitHub**. The deployment status will be displayed.

## View deployment history

While not recommended, you might stop or re-start deployment at any time. View the full deployment history.

## Configure GitHub deployment

- **Automatic Deployment**

    - Disabling automatic deployment may be useful for testing or manually deploying small changes. By pausing automatic deployment, your application and the version in GitHub might not be in sync.

    - If you choose to start automatic deployment with GitHub, any changes made through the TiDB Cloud console can be reviewed before deployment. You may stop automatic deployment at any time.

- **Review Changes**

    You are able to review changes and either deploy them or discard them. When it is disabled, any changes made via the UI will be applied immediately.

    If you choose to disable review changes, any changes made to your application via the UI will be applied immediately.