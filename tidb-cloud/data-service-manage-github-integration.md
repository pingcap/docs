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

You can connect your Data App to GitHub when you create the App. For more information, see [Create a Data App](/tidb-cloud/data-service-manage-data-app.md).

If you did not enable the GitHub connection during the app creation, you can still enable it as follows:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, click the name of your target Data App to view its details.
3. On the **Settings** tab, click **Connect** in the **Connect to GitHub** area. A dialog box for connection settings is displayed.
4. In the dialog box, perform the following steps:

    1. Click **Install on GitHub**, and then follow the on-screen instructions to install **TiDB Cloud Data Service** as an application on your target repository.
    2. Click **Authorize** to authorize access to the application on GitHub.
    3. Specify the target repository, branch, and directory where you want to store the configuration files of your Data App.

        > **Note:**
        >
        > - The directory must start with a slash. For example, `/mydata`. If the directory you specified does not exist in the target repository and branch, it will be created automatically.
        > - The combination of repository, branch, and directory identifies the path of the configuration files, which must be unique among Data Apps. If your specified path is already used by another Data App, you need to specify a new path instead. Otherwise, the endpoints configured in the TiDB Cloud console for the current Data App will overwrite the files in your specified path.
        > - If your specified path contains configuration files copied from another Data App and you want to import these files to the current Data App, see [Import configurations of an existing Data App](#import-configurations-of-an-existing-data-app).

    4. For **Configure Automatic Deployment**, enable or disable this option according to your need.

        - When it is enabled, the changes made in your specified GitHub directory can be automatically deployed in TiDB Cloud, and you can find the corresponding deployment and commit information in the Data App deployment history.
        - When it is disabled, the changes made in your specified GitHub directory will NOT deployed in TiDB Cloud, which means that the Data App are not affected by your changes in GitHub.

5. Click **Confirm Connect**.

## Step 2. Synchronize Data App configurations to GitHub

If GitHub connection is enabled when you [create a Data App](/tidb-cloud/data-service-manage-data-app.md), TiDB Cloud pushes the configuration files of this Data App to GitHub immediately after the App creation.

If GitHub connection for your Data App is enabled after the App creation, you need to perform a deployment operation to synchronize the Data App configurations to GitHub. For example, you can click **Deployment** tab, and then re-deploy a deployment for this Data App.

After the deployment operation, check your specified GitHub directory. You will find that the Data App configuration files have been committed to the directory by `tidb-cloud-data-service`, which means that your Data App is connected to GitHub successfully.

| File directory  | Descriptions  |
| ---------|---------|
| `data_source/cluster.json`     |  This file is used to specify the linked clusters of this Data App. |
| `http_endpoints/config.json`     | This file is used to specify the endpoints of this Data App.   |
| `http_endpoints/sql/method-<endpoint name>.sql`     | If SQL statements have been written for your endpoints, the `http_endpoints/sql` directory contains the SQL files of the endpoints.      |
| `datapp_config.json`  |  This file contains the `app_id`, `app_name`, `app_type` of the Data APP. |

## Step 3. Modify your Data App

If automatic deployment is disabled, you can modify your Data App only in the TiDB Cloud console.

If automatic deployment is enabled, you can modify your Data App either on GitHub or in the TiDB Cloud console.

> **Note:**
>
> If you have modified your Data App on GitHub and TiDB Cloud console at the same time, to resolve conflicts, you can choose either discard the changes made in the console or let the console changes to overwrite the GitHub changes.

### Option 1: Modify your Data App by updating files on GitHub

| File path  | Notes for the updates  |
| ---------|---------|
| `data_source/cluster.json`     |  When updating this file, make sure that the linked clusters are Serverless clusters and you have access to the clusters. You can get the ID of a cluster from the cluster URL. For example, if the cluster URL is `https://tidbcloud.com/console/clusters/1379661944646164631/overview`, the cluster ID is `1379661944646164631`.|
| `http_endpoints/config.json`     | When modifying the endpoints, make sure that you follow the rules described in [HTTP endpoint configuration](/tidb-cloud/data-service-app-config-files.md#http-endpoint-configuration). |
| `http_endpoints/sql/method-<endpoint name>.sql`     | To add or remove the SQL files in `http_endpoints/sql` directory, you need to update the corresponding endpoint configurations as well.    |
| `datapp_config.json`  |  **DO NOT** modify this file using GitHub. Otherwise, the deployment triggered by this modification will fail.       |

For more information about the field configuration in these files, see [Data App configuration files](/tidb-cloud/data-service-app-config-files.md).

After the file changes are committed, TiDB Cloud will automatically deploy the Data App with the latest changes. You can view the deployment status and commit information in the deployment history.

### Option 2: [Modify your Data App in the TiDB Cloud console](/tidb-cloud/data-service-manage-data-app.md)

After modifying your Data App in the TiDB Cloud console (such as modifying endpoints), you can review and deploy the changes to GitHub as follows:

1. Click **Review Draft & Deploy** in the upper-right corner. A dialog is displayed for you to review the changes you made.
2. Depending on your review, do one of the following:

    - If you still want to make further changes based on the current draft, close this dialog and make the changes.
    - If you want to revert the current changes to the last deployment, click **Discard Changes**. Then, click **Discard Changes** in the displayed dialog for confirmation.
    - If the current changes look fine, write a change description (optional), and then click **Deploy and Push to GitHub**. The deployment status will be displayed in the top banner.

> **Note:**
>
> If automatic deployment is disabled and you prefer to skip the review process, you can disable **Review draft** as instructed in [Configure Data App deployment](/tidb-cloud/data-service-manage-data-app.md#manage-deployments). After **Review draft** is disabled, the Data App changes made in the TiDB Cloud console are pushed to GitHub immediately.

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
3. In the **Connect to GitHub** area, click <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" color="gray.1"><path d="M11 3.99998H6.8C5.11984 3.99998 4.27976 3.99998 3.63803 4.32696C3.07354 4.61458 2.6146 5.07353 2.32698 5.63801C2 6.27975 2 7.11983 2 8.79998V17.2C2 18.8801 2 19.7202 2.32698 20.362C2.6146 20.9264 3.07354 21.3854 3.63803 21.673C4.27976 22 5.11984 22 6.8 22H15.2C16.8802 22 17.7202 22 18.362 21.673C18.9265 21.3854 19.3854 20.9264 19.673 20.362C20 19.7202 20 18.8801 20 17.2V13M7.99997 16H9.67452C10.1637 16 10.4083 16 10.6385 15.9447C10.8425 15.8957 11.0376 15.8149 11.2166 15.7053C11.4184 15.5816 11.5914 15.4086 11.9373 15.0627L21.5 5.49998C22.3284 4.67156 22.3284 3.32841 21.5 2.49998C20.6716 1.67156 19.3284 1.67155 18.5 2.49998L8.93723 12.0627C8.59133 12.4086 8.41838 12.5816 8.29469 12.7834C8.18504 12.9624 8.10423 13.1574 8.05523 13.3615C7.99997 13.5917 7.99997 13.8363 7.99997 14.3255V16Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>. A dialog box for connection settings is displayed.
4. In the dialog box, modify the repository, branch, and directory of your Data App.

    > **Note:**
    >
    > - The directory must start with a slash. For example, `/mydata`. If the directory you specified does not exist in the target repository and branch, it will be created automatically.
    > - The combination of repository, branch, and directory identifies the path of the configuration files, which must be unique among Data Apps. If your specified path is already used by another Data App, you need to specify a new path instead. Otherwise, the endpoints configured in the TiDB Cloud console for the current Data App will overwrite the files in your specified path.
    > - If your specified path contains configuration files copied from another Data App and you want to import these files to the current Data App, see [Import configurations of an existing Data App](#import-configurations-of-an-existing-data-app).

5. For **Configure Automatic Deployment**, enable or disable this option according to your need.

    - When it is enabled, the changes made in your specified GitHub directory can be automatically deployed in TiDB Cloud, and you can find the corresponding deployment and commit information in the Data App deployment history.
    - When it is disabled, the changes made in your specified GitHub directory will NOT deployed in TiDB Cloud, which means that the Data App are not affected by your changes in GitHub.

6. Click **Confirm Connect**.

## Remove Github connection

If you no longer want to connect your Data App to GitHub, take the following steps:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, click the name of your target Data App to view its details.
3. On the **Settings** tab, click **Disconnect** in the **Connect to GitHub** area.
4. Click **Unlink** to confirm the unlinking.

After the unlinking operation, your Data App configuration files will remain in your GitHub directory but will not be synchronized by `tidb-cloud-data-service` anymore.