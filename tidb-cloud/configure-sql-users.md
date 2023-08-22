---
title: Manage Database Users and Roles
summary: Learn how to manage database users and roles in the TiDB Cloud console.
---

# Manage Database Users and Roles

This document describes how to manage database users and roles using the **SQL Users** page in the [TiDB Cloud console](https://tidbcloud.com/).

> **Tip**
>
> In addition to the **SQL Users** page, you can also manage database users and roles by connecting to your cluster with a SQL client and writing SQL statements. For more information, see [TiDB User Account Management](https://docs.pingcap.com/tidb/dev/user-account-management).

## SQL user roles

In TiDB Cloud, you can grant both a built-in role and multiple custom roles (if available) to a SQL user for role-based access control.

- Built-in roles

    TiDB Cloud provides the following built-in roles to help you control the database access of SQL users. You can grant one of the built-in roles to a SQL user.

    - `Database Admin`
    - `Database Read-Write`
    - `Database Read-Only`

- Custom roles

    If your cluster has custom roles that are created using the [`CREATE ROLE`](/sql-statements/sql-statement-create-role.md) statement, you can grant custom roles to a SQL user when you create or edit SQL users in the TiDB Cloud console.

After granting a SQL user a combination of a built-in role and multiple custom roles, the user's permissions are the union of all the permissions from these roles.

## Prerequisites

- To manage database users and roles using the **SQL Users** page, you must be in the `Organization Owner` role of your organization or the `Project Owner` role of your project.
- If you are in the `Project Data Access Read-Write` or `Project Data Access Read-Only` role of a project, you can only view database users on the **SQL Users** page of that project.

## Create a SQL user

To create a SQL use, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com/), go to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.

    > **Tip:**
    >
    > If you have multiple projects, you can click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner and switch to another project.

2. Click your cluster name, and then click **SQL users** in the left navigation pane.
3. Click **Create SQL User** in the upper-right corner.

    A dialog for the SQL user configuration is displayed.

4. In the dialog, provide the information of the SQL user as follows:

    1. Enter the name of the SQL user.
    2. Either enter a password for the SQL users or let TiDB Cloud automatically generate a password for the user.
    3. Grant roles to the SQL user.

        - **Built-in Role**: you need to select a built-in role for the SQL user in the **Built-in Role** drop-down list.

        - **Custom Role**: if your cluster has custom roles that are created using the [`CREATE ROLE`](/sql-statements/sql-statement-create-role.md) statement), you can grant custom roles to the SQL user by selecting the roles from the **Custom Role** drop-down list. Otherwise, the **Custom Roles** drop-down list is invisible here.

      For each SQL user, you can grant a built-in role and multiple custom roles (if any).

5. Click **Create**.

## View SQL users

To view SQL users of a cluster, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com/), go to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.

    > **Tip:**
    >
    > If you have multiple projects, you can click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner and switch to another project.

2. Click your cluster name, and then click **SQL users** in the left navigation pane.

## Edit a SQL user

To edit the password or roles of a SQL user, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com/), go to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.

    > **Tip:**
    >
    > If you have multiple projects, you can click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner and switch to another project.

2. Click your cluster name, and then click **SQL users** in the left navigation pane.
3. In the row of the SQL user to be edited, click **...** in the **Action** column, and then click **Edit**.

    A dialog for the SQL user configuration is displayed.

4. In the dialog, you can edit the user password and roles as needed.

    > **Note:**
    >
    > The roles of the default `<prefix>.root` user does not support modification.

## Delete a SQL user

To delete a SQL user, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com/), go to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.

    > **Tip:**
    >
    > If you have multiple projects, you can click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner and switch to another project.

2. Click your cluster name, and then click **SQL users** in the left navigation pane.
3. In the row of the SQL user to be edited, click **...** in the **Action** column, and then click **Delete**.

    > **Note:**
    >
    > The default `<prefix>.root` user does not support deletion.

4. Confirm the deletion.
