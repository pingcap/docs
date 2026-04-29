---
title: Manage TiDB Cloud Resources and Projects
summary: Learn how to manage your TiDB Cloud resources and projects on the My TiDB page.
---

# Manage TiDB Cloud Resources and Projects

In the [TiDB Cloud console](https://tidbcloud.com/), you can discover, access, and manage all TiDB Cloud resources and projects within your organization on the [**My TiDB**](https://tidbcloud.com/tidbs) page.

## What are TiDB Cloud resources and projects?

### TiDB Cloud resources

A TiDB Cloud resource is a deployable unit that you can manage. It can be one of the following:

- A TiDB X instance, which is a service-oriented TiDB Cloud offering built on the [TiDB X architecture](/tidb-cloud/tidb-x-architecture.md), such as a {{{ .starter }}}, Essential, or Premium instance
- A {{{ .dedicated }}} cluster

### TiDB Cloud projects

In TiDB Cloud, you can use [projects](/tidb-cloud/tidb-cloud-glossary.md#project) to organize and manage your TiDB Cloud resources.

- For TiDB X instances, projects are optional, which means you can either group these instances in a project or keep them at the organization level.
- For {{{ .dedicated }}} clusters, projects are required.

## Manage TiDB Cloud resources

This section describes how to view, create, and manage TiDB Cloud resources using the [**My TiDB**](https://tidbcloud.com/tidbs) page.

### View TiDB Cloud resources

By default, the [**My TiDB**](https://tidbcloud.com/tidbs) page shows the resource view, which displays all resources within your current organization that you have permission to access.

If your organization has many instances or clusters, you can use the filters at the top of the page to quickly find what you need.

To view detailed information about a TiDB Cloud resource, click the name of the target resource to go to its overview page.

### Create TiDB Cloud resources

To create a TiDB Cloud resource, navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page of your organization, and then click **Create Resource**.

For more information, see the following documents:

- [Create a {{{ .starter }}} or Essential Instance](/tidb-cloud/create-tidb-cluster-serverless.md)

- [Create a {{{ .premium }}} Instance](/tidb-cloud/premium/create-tidb-instance-premium.md)

- [Create a {{{ .dedicated }}} Cluster](/tidb-cloud/create-tidb-cluster.md)

### Manage TiDB Cloud resources

On the **My TiDB** page, you can click **...** in the row of the target resource to perform quick actions on a TiDB Cloud resource, such as deleting, renaming, and importing data.

To perform more operations and manage settings of a specific TiDB Cloud resource, click the name of the target resource to go to its overview page.

## Manage TiDB Cloud projects

This section describes how to view, create, and manage TiDB Cloud projects using the [**My TiDB**](https://tidbcloud.com/tidbs) page.

### View projects

To view your TiDB Cloud resources grouped by projects, click the **Project view** tab on the [**My TiDB**](https://tidbcloud.com/tidbs) page.

> **Tip:**
>
> If you are in multiple organizations, use the combo box in the upper-left corner to switch to your target organization first.

In the project view, you can see the projects you belong to in the organization:

- TiDB X instances that do not belong to any project are displayed in a table named `Out of project`.
- TiDB X instances that belong to specific projects are displayed in their corresponding TiDB X project tables.
- TiDB Cloud Dedicated clusters are displayed in their corresponding Dedicated project tables. These tables have a **D** in the folder icon to identify the **Dedicated** project type.

### Create a project

> **Note:**
>
> - Free trial users cannot create new projects.
> - For TiDB X instances, creating a project is optional. For TiDB Cloud Dedicated clusters, you must use the default project or create new projects to manage them.

If you are in the `Organization Owner` role, you can create projects in your organization.

To create a new project, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com), navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page of your organization, and then click **Create Project**.

    > **Tip:**
    >
    > If you are in multiple organizations, use the combo box in the upper-left corner to switch to your target organization first.

2. In the displayed dialog, enter a project name.

3. Depending on which type of TiDB Cloud resources you are creating the project for, do one of the following:

    - If the project is created for TiDB X instances, click **Confirm**.

        > **Note:**
        >
        > For {{{ .premium }}} instances, encryption is configured per instance rather than per project. After you create the instance, you can enable [Dual-Layer Data Encryption](/tidb-cloud/premium/dual-layer-data-encryption-premium.md) to add a database-layer encryption on top of the default storage-layer encryption.

    - If the project is created for {{{ .dedicated }}} clusters, select the **Create for Dedicated Cluster** option, configure [Customer-Managed Encryption Keys (CMEK)](/tidb-cloud/tidb-cloud-encrypt-cmek-aws.md) and [maintenance window](/tidb-cloud/configure-maintenance-window.md) for the project, and then click **Confirm**.

### Manage a project

If you are in the `Organization Owner` or `Project Owner` role, you can manage your project.

To manage a project, take the following steps:

1. In the TiDB Cloud console, navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page of your organization, and then click the **Project view** tab.

    > **Tip:**
    >
    > If you are in multiple organizations, use the combo box in the upper-left corner to switch to your target organization first.

2. In the project view, locate your target project, and then manage it as follows:

    - For both TiDB X and TiDB Dedicated projects, you can click **...** in the row of the target project to perform quick actions on a project, such as renaming the project or inviting members to the project. For more information, see [Manage project access](/tidb-cloud/manage-user-access.md).
    - For TiDB Dedicated projects, you can also click the <MDSvgIcon name="icon-project-settings" /> icon in the row of the target project to manage settings, such as networking, maintenance, alert subscriptions, and encryption access, for {{{ .dedicated }}} clusters by project.

### Move a TiDB X instance between projects

If you are in the `Organization Owner` or `Project Owner` role, you can move a TiDB X instance to a project or out of any project.

> **Note:**
>
> Only TiDB X instances support moving between TiDB X projects and out of any TiDB X project. TiDB Cloud Dedicated clusters do not support moving between projects.

To move a TiDB X instance, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com), navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page of your organization, and then click the **Project view** tab.

2. In the project view, expand the project folder that contains the TiDB X instance to be moved, click **...** for the target TiDB X instance, and then click **Move**.

    > **Tip:**
    >
    > If the TiDB X instance is not in any project, it is displayed in the **Out of project** folder.

3. In the displayed dialog, do one of the following:

    - To move the TiDB X instance to a project, select **To a project**, and then select the target project from the drop-down list.
    - To move the TiDB X instance out of any project, select **Outside any project**.

4. Click **Move**.
