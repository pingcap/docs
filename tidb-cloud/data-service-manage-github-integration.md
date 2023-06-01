---
title: Deploy Automatically with GitHub
summary: Learn how to automatically deploy metadata and endpoints of your Data App with GitHub.
---

# Deploy Automatically with GitHub

By connecting your Data App to GitHub, you can automatically deploy metadata and endpoints of the Data App to your preferred GitHub repository and branch. Whenever you push changes of the Data App configuration files to a GitHub repository, the new configurations are deployed in TiDB Cloud automatically.

## Before you begin

Before you connect a Data App to GitHub, make sure that you have the following:

- A GitHub account.
- A GitHub repository with your target branch and directory.

## Step 1. Connect your Data App to GitHub

You can connect your Data App to GitHub when you create the App. For more information, see [Create a Data App](/tidb-cloud/data-service-manage-data-app.md)

If you do not enable that during the app creation, you can still enable it as follows:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, click the name of your target Data App to view its details.
3. In the **Connect to GitHub** area, click **Connect**. A dialog box for connection settings is displayed.
4. In the dialog box, perform the following steps:

    1. Click **Install on GitHub**, and then follow the on-screen instructions to install **TiDB Cloud Data Service** as an application on your target repository.
    2. Click **Authorize** to authorize access to the application on GitHub.
    3. Specify the target repository, branch, and directory where you want to save the configuration files of your Data App.

    > **Note:**
    >
    > - The directory must start with a slash. For example, `/mydata`. If the directory you specified does not exist in the target repository and branch, it will be created automatically.
    > - The combination of repository, branch, and directory represents the path of the configuration files, which must be unique among Data Apps. If the path already contains files of existing Data Apps, you need to specify a new path instead.
    > - If the files in your specified directory are copied from another Data App's GitHub directory, the `app_id` in your `datapp_config.json` file is not the actual ID of the current Data App, so the endpoints configured in the TiDB Cloud Console will overwrite the files in your specified directory. If you want to import endpoints from an existing GitHub directory, see [Import configurations of an existing Data App](#import-configurations-of-an-existing-data-app).

5. Click **Confirm Connect**.
6. Check your selected directory on GitHub. If the configuration files of the Data App have been committed by `tidb-cloud-data-service`, it indicates that your Data App is connected to GitHub successfully.

    In your GitHub directory, you can find the following configuration files:

    | Directory  | Descriptions  |
    | ---------|---------|
    | `data_source/cluster.json`     |  This file is used to specify the linked clusters of this Data App. |
    | `http_endpoints/config.json`     | This file is used to specify the endpoints of this Data App.   |
    | `http_endpoints/sql/method-<endpoint name>.sql`     | If SQL statements have been written for your endpoints, the `http_endpoints/sql` directory contains the SQL files of the endpoints.      |
    | `datapp_config.json`  |  This file contains the `app_id`, `app_name`, `app_type` of the Data APP. |

## Step 2. Configure GitHub deployment for your App

After you connect a Data App to GitHub, you can configure whether to enable **Automatic Deployment** and **Review Changes** for the App.

> **Tip:**
>
> If you have connected your Data App to GitHub when you create the App, **Automatic Deployment** and **Review Changes** are enabled by default for the Data App.

1. On the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project, click the name of your target Data App in the left pane.
2. Click **Deployment** to view the deployment information.
3. In the upper-right corner, click **Configure**, and then enable or disable **Automatic Deployment** and **Review Changes** according to your need.

    - **Automatic Deployment**

        - When it is enabled, the changes made in your specified GitHub directory can be automatically deployed in TiDB Cloud, and you can find the corresponding deployment and commit information in the Data App deployment history.
        - When it is disabled, the changes made in your specified GitHub directory will NOT deployed in TiDB Cloud, which means that the Data App status are not affected by your changes in GitHub.

    - **Review Changes**

        - When it is enabled, you can review the Data App configuration changes you made in the TiDB Cloud console before the deployment. Based on the review, you can either deploy or discard the changes.
        - When it is disabled, the Data App configuration changes you made in the TiDB Cloud console are deployed directly.

    > **Note:**
    >
    > Every time you change the **Automatic Deployment** configuration, the **Review Changes** configuration is changed as well:
    >
    > - Enabling **Automatic Deployment** will automatically enable **Review Changes**.
    > - Disabling **Automatic Deployment** will automatically disable **Review Changes**.
    >
    > If needed, you can further change the **Review Changes** configuration after enabling or disabling **Automatic Deployment**.

## Step 3. Deploy your Data App changes to GitHub automatically

If **Automatic Deployment** is disabled, you can only [modify your Data App](/tidb-cloud/data-service-manage-data-app.md#modify-a-data-app) in the TiDB Cloud console.

If **Automatic Deployment** is enabled, you can modify your Data App either on GitHub or in the TiDB Cloud console:

> **Note:**
>
> If you have modified your Data App on GitHub and TiDB Cloud console at the same time, the deployment triggered by the changes on GitHub will succeed, while the deployment triggered by the changes in the TiDB Cloud console will fail due to the conflicts in the changes. In this case, after the successful deployment of changes on GitHub, you need to discard the changes made in the TiDB Cloud console to align with the latest GitHub commits.

- Option 1: Modify your Data App by updating files on GitHub.

    | File path  | Notes for the updates  |
    | ---------|---------|
    | `data_source/cluster.json`     |  When updating this file, make sure that the linked clusters are Serverless clusters and you have access to the clusters. You can get the ID of a cluster from the cluster URL. For example, if the cluster URL is `https://tidbcloud.com/console/clusters/1379661944646164631/overview`, the cluster ID is `1379661944646164631`.|
    | `http_endpoints/config.json`     | When modifying the endpoints, make sure that you follow the rules described in [Develop an endpoint](/tidb-cloud/data-service-manage-endpoint.md#develop-an-endpoint).       |
    | `http_endpoints/sql/method-<endpoint name>.sql`     | To add or remove the SQL files in `http_endpoints/sql` directory, you need to update the corresponding endpoint configurations as well.    |
    | `datapp_config.json`  |  **DO NOT** modify this file using GitHub. Otherwise, the deployment triggered by this modification will fail.       |

    After the changes are committed, TiDB Cloud will automatically deploy the Data App with the latest changes. You can view the deployment status in the deployment history.

- Option 2: [Modify your Data App in the TiDB Cloud console](/tidb-cloud/data-service-manage-data-app.md). For example, you can rename the Data APP, modify endpoints, and modify linked clusters.

    When **Review Changes** is enabled, after any changes are made in the TiDB Cloud console, you can review and deploy the changes as follows:

    1. Click **Review changes & Deploy** in the upper-right corner. A dialog is displayed for you to review the changes you made.
    2. If you find anything that needs to be updated in the dialog, you can close this dialog and make further changes, or you can click **Discard Changes** to revert the changes and make changes again.
    3. (Optional) Type a message for the deployment.
    4. Click **Deploy and Push to GitHub**. The deployment status will be displayed in the top banner.

## Import configurations of an existing Data App

If you have created a GitHub branch based on configuration files of an existing Data App, you can import the configuration of the existing Data App to a new Data App as follows:

1. On the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project, [create a new Data App](/tidb-cloud/data-service-manage-data-app.md#create-a-data-app) without connecting to GitHub.
2. [Connect the new Data App to GitHub](#step-1-connect-your-data-app-to-github). When you specify the target repository, branch, and directory, use the path of the new branch.
3. Click the name of your new Data App in the left pane and find its setting in the right pane. In the **General** area, copy the ID of your new Data App.
4. In the new branch, update the `app_id` in the `datapp_config.json` file to the new ID and commit the changes.

## Remove Github integration

If you no longer want to connect your Data App to GitHub, take the following steps:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, click the name of your target Data App to view its details.
3. In the **Connect to GitHub** area, click **Unlink**.