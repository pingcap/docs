---
title: Manage TiDB Serverless Branch
summary: Learn How to manage the TiDB Serverless branch.
---

# Manage TiDB Serverless Branches

This document describes how to manage the TiDB Serverless branches using the [TiDB Cloud console](https://tidbcloud.com). You can also manage it using the [TiDB Cloud CLI](/tidb-cloud/cli-reference.md).

## View branches

To view branches for your cluster, perform the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.
2. Click your cluster name. The cluster overview page is displayed.
3. Click **Branches** in the left navigation pane.

## Create a branch

To create a branch, perform the following steps:

1. Navigate to the **Branches** page of your cluster.
2. Click **Create Branch** in the upper-right corner.
3. Enter the branch name, and then click **Create**.

Depending on the data size in your cluster, the branch creation will be completed in a few minutes.

## Delete a branch

To delete a branch, perform the following steps:

1. Navigate to the *Branches** page of your cluster.
2. In the row of your target branch to be deleted, click **...** in the **Action** column.
3. Click **Delete** in the drop-down list.
4. Confirm the deletion.

## Get branch connection information

To get the connection information of a branch, perform the following steps:

1. Navigate to the *Branches** page of your cluster.
2. In the row of your target branch to be deleted, click **...** in the **Action** column.
3. Click **Connect** in the drop-down list. The dialog for the connection information is displayed.
4. Click the **Create password** or **Reset password** to create or reset the root password.

> **Note:**
>
> Currently, branches do not support [private endpoints](/tidb-cloud/set-up-private-endpoint-connections-serverless.md).

## What's next

- [Integrate branches into your CI/CD pipeline](/tidb-cloud/branch-github-integration.md)
