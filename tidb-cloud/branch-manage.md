---
title: Manage TiDB Cloud Serverless Branches
summary: Learn How to manage TiDB Cloud Serverless branches.
---

# Manage TiDB Cloud Serverless Branches

This document describes how to manage TiDB Cloud Serverless branches using the [TiDB Cloud console](https://tidbcloud.com). To manage it using the TiDB Cloud CLI, see [`ticloud branch`](/tidb-cloud/ticloud-branch-create.md).

## Required access

- To [create a branch](#create-a-branch) or [connect to a branch](#connect-to-a-branch), you must be in the `Organization Owner` role of your organization or the `Project Owner` role of the target project.
- To [view branches](#create-a-branch) for clusters in a project, you must belong to that project.

For more information about permissions, see [User roles](/tidb-cloud/manage-user-access.md#user-roles).

## Create a branch

> **Note:**
>
> You can only create branches for TiDB Cloud Serverless clusters that are created after July 5, 2023. See [Limitations and quotas](/tidb-cloud/branch-overview.md#limitations-and-quotas) for more limitations.

To create a branch, perform the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project, and then click the name of your target TiDB Cloud Serverless cluster to go to its overview page.
2. Click **Branches** in the left navigation pane.
3. In the upper-right corner of the **Branches** page, click **Create Branch**. A dialog is displayed.

    Alternatively, to create a branch from an existing parent branch, locate the row of your target parent branch, and then click **...** > **Create Branch** in the **Action** column.

4. In the **Create Branch** dialog, configure the following options:

    - **Name**: enter a name for the branch.
    - **Parent branch**: select the original cluster or an existing branch. `main` represents the current cluster.
    - **Include data up to**: choose one of the following:
        - **Current point in time**: create a branch from the current state.
        - **Specific date and time**: create a branch from a specified time.

5. Click **Create**.

Depending on the data size in your cluster, the branch creation will be completed in a few minutes.

## View branches

To view branches for your cluster, perform the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project, and then click the name of your target TiDB Cloud Serverless cluster to go to its overview page.
2. Click **Branches** in the left navigation pane.

    The branch list of the cluster is displayed in the right pane.

## Connect to a branch

To connect to a branch, perform the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project, and then click the name of your target TiDB Cloud Serverless cluster to go to its overview page.
2. Click **Branches** in the left navigation pane.
3. In the row of your target branch to be connected, click **...** in the **Action** column.
4. Click **Connect** in the drop-down list. The dialog for the connection information is displayed.
5. Click **Generate Password** or **Reset Password** to create or reset the root password.
6. Connect to the branch using the connection information.

Alternatively, you can get the connection string from the cluster overview page:

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project, and then click the name of your target TiDB Cloud Serverless cluster to go to its overview page.
2. Click **Connect** in the upper-right corner.
3. Select the branch you want to connect to in the `Branch` drop-down list.
4. Click **Generate Password** or **Reset Password** to create or reset the root password.
5. Connect to the branch using the connection information.

## Delete a branch

To delete a branch, perform the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project, and then click the name of your target TiDB Cloud Serverless cluster to go to its overview page.
2. Click **Branches** in the left navigation pane.
3. In the row of your target branch to be deleted, click **...** in the **Action** column.
4. Click **Delete** in the drop-down list.
5. Confirm the deletion.

## Reset a branch

Resetting a branch synchronizes it with the latest data from its parent.

> **Note:**
> 
> This operation is irreversible. Before resetting a branch, make sure that you have backed up any important data.

To reset a branch, perform the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project, and then click the name of your target TiDB Cloud Serverless cluster to go to its overview page.
2. Click **Branches** in the left navigation pane.
3. In the row of your target branch to be reset, click **...** in the **Action** column.
4. Click **Reset** in the drop-down list.
5. Confirm the reset.

## What's next

- [Integrate TiDB Cloud Serverless branching into your GitHub CI/CD pipeline](/tidb-cloud/branch-github-integration.md)
