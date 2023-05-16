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
- A GitHub repository with an empty branch.

## Enable automatic deployment with GitHub

You can enable automatic deployment with GitHub when you create a Data App. For more information, see [Create a Data App](/tidb-cloud/data-service-manage-data-app.md)

If you do not enable that during the app creation, you can still enable it as follows:

1. Navigate to the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. In the left pane, click the name of your target Data App to view its details.
3. In the **Connect to GitHub** area, click **Connect**. A dialog box for connection settings are displayed.
4. In the dialog box, perform the following steps:

    1. Click **Install on GitHub**, and then follow the on-screen instructions to install TiDB Cloud data services as an application on your target repository.
    2. Click **Authorize**, and then follow the on-screen instructions to authorize access to the application on GitHub.
    3. Select 

