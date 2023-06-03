---
title: Deploy Automatically with GitHub
summary: Learn how to automatically deploy metadata and endpoints of your Data App with GitHub.
---

# Deploy Automatically with GitHub

By connecting your Data App to GitHub, you can automatically deploy endpoints of the Data App to your preferred GitHub repository and branch. Whenever you push changes of the Data App configuration files to a GitHub repository, the new configurations are deployed in TiDB Cloud automatically.

## Before you begin

Before you connect a Data App to GitHub, make sure that you have the following:

- A GitHub account.
- A GitHub repository with your target branch.

> **Note:**
>
> The GitHub repository is used to store [Data App configuration files](/tidb-cloud/data-service-app-config-files.md) after your connect a Data App to it. If the information (such as cluster ID and endpoint URL) in the configuration files is sensitive, make sure to use a private repository instead of a public one.

## Step 1. Connect your Data App to GitHub

You can connect your Data App to GitHub when you create the App. For more information, see [Create a Data App](/tidb-cloud/data-service-manage-data-app.md)

If you did not enable the GitHub connection during the app creation, you can still enable it as follows:

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
        > - The combination of repository, branch, and directory identifies the path of the configuration files, which must be unique among Data Apps. If your specified path is already used by another Data App, you need to specify a new path instead. Otherwise, the endpoints configured in the TiDB Cloud console for the current Data App will overwrite the files in your specified path.
        > - If your specified path contains configuration files copied from another Data App and you want to import these files to the current Data App, see [Import configurations of an existing Data App](#import-configurations-of-an-existing-data-app).

    4. For **Configure Automatic Deployment**, enable or disable this option according to your need.

        - When it is enabled, the changes made in your specified GitHub directory can be automatically deployed in TiDB Cloud, and you can find the corresponding deployment and commit information in the Data App deployment history.
        - When it is disabled, the changes made in your specified GitHub directory will NOT deployed in TiDB Cloud, which means that the Data App are not affected by your changes in GitHub.

5. Click **Connect**.

## Step 2. Verify the GitHub connection

Check whether your Data App configuration files have been committed to your specified GitHub directory by `tidb-cloud-data-service`. If yes, it indicates that your Data App is connected to GitHub successfully.

| File directory  | Descriptions  |
| ---------|---------|
| `data_source/cluster.json`     |  This file is used to specify the linked clusters of this Data App. |
| `http_endpoints/config.json`     | This file is used to specify the endpoints of this Data App.   |
| `http_endpoints/sql/method-<endpoint name>.sql`     | If SQL statements have been written for your endpoints, the `http_endpoints/sql` directory contains the SQL files of the endpoints.      |
| `datapp_config.json`  |  This file contains the `app_id`, `app_name`, `app_type` of the Data APP. |

## Step 3. Deploy your Data App changes with GitHub automatically

If automatic deployment is disabled, you can [modify your Data App](/tidb-cloud/data-service-manage-data-app.md#modify-a-data-app) only in the TiDB Cloud console. The changes made in the console will be pushed to your specified GitHub directory immediately.

If automatic deployment is enabled, you can modify your Data App either on GitHub or in the TiDB Cloud console.

> **Note:**
>
> If you have modified your Data App on GitHub and TiDB Cloud console at the same time, to resolve conflicts, you can choose either discard the changes made in the console or let the console changes to overwrite the GitHub changes.

- Option 1: Modify your Data App by updating files on GitHub.

    | File path  | Notes for the updates  |
    | ---------|---------|
    | `data_source/cluster.json`     |  When updating this file, make sure that the linked clusters are Serverless clusters and you have access to the clusters. You can get the ID of a cluster from the cluster URL. For example, if the cluster URL is `https://tidbcloud.com/console/clusters/1379661944646164631/overview`, the cluster ID is `1379661944646164631`.|
    | `http_endpoints/config.json`     | When modifying the endpoints, make sure that you follow the rules described in [HTTP endpoint configuration](/tidb-cloud/data-service-app-config-files.md#http-endpoint-configuration). |
    | `http_endpoints/sql/method-<endpoint name>.sql`     | To add or remove the SQL files in `http_endpoints/sql` directory, you need to update the corresponding endpoint configurations as well.    |
    | `datapp_config.json`  |  **DO NOT** modify this file using GitHub. Otherwise, the deployment triggered by this modification will fail.       |

    For more information about the field configuration in these files, see [Data App configuration files](/tidb-cloud/data-service-app-config-files.md).

    After the file changes are committed, TiDB Cloud will automatically deploy the Data App with the latest changes. You can view the deployment status and commit information in the deployment history.

- Option 2: [Modify your Data App in the TiDB Cloud console](/tidb-cloud/data-service-manage-data-app.md). For example, you can rename the Data APP, modify endpoints, and modify linked clusters.

    After modifying your Data App in the TiDB Cloud console, you can review and deploy the changes as follows:

    1. Click **Review draft** in the upper-right corner. A dialog is displayed for you to review the changes you made.
    2. If you find anything that needs to be updated in the dialog, you can close this dialog and make further changes, or you can click **Discard Draft** to revert the current changes and make new changes.
    3. (Optional) Type a message for the deployment.
    4. Click **Deploy and Push to GitHub**. The deployment status will be displayed in the top banner.

    If you prefer to skip the review process and push the Data App changes in the TiDB Cloud console to GitHub directly, you can disable **Review draft** as instructed in [Configure Data App deployment](/tidb-cloud/data-service-manage-data-app.md#manage-deployments).

## Import configurations of an existing Data App

To import configurations of an existing Data App to a new Data App, take the following steps:

1. Copy configuration files of the existing Data App to a new branch or directory on GitHub.
2. On the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project, [create a new Data App](/tidb-cloud/data-service-manage-data-app.md#create-a-data-app) without connecting to GitHub.
3. [Connect your new Data App to GitHub](#step-1-connect-your-data-app-to-github) with automatic deployment enabled. When you specify the target repository, branch, and directory for your new Data App, use your new path with the copied configuration files.
4. Get the ID of your new Data App. You can click the name of your new Data App in the left pane and get the App ID in the **Data App Properties** area of the right pane.
5. In your new path on GitHub, update the `app_id` in the `datapp_config.json` file to the ID you get, and then commit the changes.

After the file changes are committed, TiDB Cloud will automatically deploy your new Data App with the latest changes. You can view the deployment status and commit information in the deployment history.

## Edit GitHub connection

If you want to edit the GitHub connection for your Data App (such as switching the repository, branch, and directory), perform the following steps.

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, click the name of your target Data App to view its details.
3. In the **Connect to GitHub** area, click the Edit icon. A dialog box for connection settings is displayed.
4. In the dialog box, modify the repository, branch, and directory of your Data App.

    > **Note:**
    >
    > - The directory must start with a slash. For example, `/mydata`. If the directory you specified does not exist in the target repository and branch, it will be created automatically.
    > - The combination of repository, branch, and directory identifies the path of the configuration files, which must be unique among Data Apps. If your specified path is already used by another Data App, you need to specify a new path instead. Otherwise, the endpoints configured in the TiDB Cloud console for the current Data App will overwrite the files in your specified path.
    > - If your specified path contains configuration files copied from another Data App and you want to import these files to the current Data App, see [Import configurations of an existing Data App](#import-configurations-of-an-existing-data-app).

5. For **Configure Automatic Deployment**, enable or disable this option according to your need.

    - When it is enabled, the changes made in your specified GitHub directory can be automatically deployed in TiDB Cloud, and you can find the corresponding deployment and commit information in the Data App deployment history.
    - When it is disabled, the changes made in your specified GitHub directory will NOT deployed in TiDB Cloud, which means that the Data App are not affected by your changes in GitHub.

6. Click **Confirm**.

## Remove Github connection

If you no longer want to connect your Data App to GitHub, take the following steps:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, click the name of your target Data App to view its details.
3. In the **Connect to GitHub** area, click **Unlink**.