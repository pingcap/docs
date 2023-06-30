---
title: Manage TiDB Cloud Branch
summary: Learn How to manage the TiDB Cloud branch.
---

# Manage TiDB Cloud Branch

This document describes how to manage the TiDB Cloud branch on the console. You can also manage it by [TiDB Cloud CLI](./cli-reference.md).

## List branches

To list branches for your cluster, perform the following steps:

1. Navigate to the [cluster](https://tidbcloud.com/console/clusters) page.
2. Click your cluster name, and then click **Branch** in the left navigation pane.

## Create a branch

To create a copy-on-write branch, perform the following steps:

1. Navigate to the branch list page of your cluster.
2. Click the **Create Branch** button.
3. Enter the branch name and then click **Create**.

> **Note:**
>
> Branch can only be created in the same region as the cluster now. 
> You can create up to 5 free branches in an organization. Contact us if you need more branches.

## Delete a branch

To delete a branch, perform the following steps:

1. Navigate to the branch list page of your cluster.
2. In the row of your target branch to be deleted, click ...
3. Click **Delete** in the drop-down menu.

## Get branch connection information

To get branch connection information, perform the following steps:

1. Navigate to the branch list page of your cluster.
2. In the row of your target branch to be deleted, click ...
3. Click the **Connect** in the drop-down menu.
4. Click the **Create password** or **Reset password** to create or reset the password.

> **Note:**
>
> Branch does not support private link now.

## What's next

- [Integrate branching into your CI/CD pipeline](./branch-github-integration.md)
