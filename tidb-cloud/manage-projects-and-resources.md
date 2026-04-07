---
title: Manage TiDB Cloud Resources and Projects
summary: Learn how to manage your TiDB Cloud resources and projects on the My TiDB page.
---

# Manage TiDB Cloud Resources and Projects

In the [TiDB Cloud console](https://tidbcloud.com/), you can discover, access, and manage all TiDB Cloud resources and projects within your organization on the [**My TiDB**](https://tidbcloud.com/tidbs) page.

## What are TiDB Cloud resources and projects?

### TiDB Cloud resources

A TiDB Cloud resource is a deployable unit that you can manage. It can be one of the following:

- A TiDB X instance, which is a service-oriented TiDB Cloud offering built on the [TiDB X architecture](/tidb-cloud/tidb-x-architecture.md), such as a {{{ .starter }}}, {{{ .essential }}}, or {{{ .premium }}} instance
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
    - For TiDB Dedicated projects, you can also click the <svg width="1em" height="1em" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" stroke-width="1.5" class="tiui-icon Settings02 " style="color: var(--mantine-color-carbon-7); width: calc(1rem * var(--mantine-scale)); height: calc(1rem * var(--mantine-scale));"><path d="M6.26338 12.9141L6.65301 13.7904C6.76884 14.0513 6.95786 14.2729 7.19716 14.4284C7.43646 14.584 7.71575 14.6668 8.00116 14.6667C8.28657 14.6668 8.56586 14.584 8.80516 14.4284C9.04446 14.2729 9.23348 14.0513 9.34931 13.7904L9.73894 12.9141C9.87764 12.6032 10.1109 12.3439 10.4056 12.1734C10.7021 12.0023 11.0452 11.9295 11.3856 11.9652L12.3389 12.0667C12.6227 12.0967 12.9091 12.0438 13.1634 11.9143C13.4177 11.7848 13.6289 11.5843 13.7715 11.3371C13.9143 11.0901 13.9823 10.8069 13.9674 10.522C13.9524 10.237 13.855 9.96258 13.6871 9.73189L13.1226 8.95634C12.9217 8.67813 12.8143 8.34325 12.816 8.00004C12.8159 7.65777 12.9243 7.32427 13.1256 7.04745L13.69 6.27189C13.858 6.04121 13.9553 5.76675 13.9703 5.48182C13.9853 5.19689 13.9173 4.91373 13.7745 4.66671C13.6319 4.41953 13.4206 4.21903 13.1664 4.08953C12.9121 3.96002 12.6257 3.90706 12.3419 3.93708L11.3886 4.03856C11.0481 4.07431 10.7051 4.00145 10.4086 3.83041C10.1133 3.65888 9.87995 3.39828 9.7419 3.08597L9.34931 2.20967C9.23348 1.94882 9.04446 1.72718 8.80516 1.57164C8.56586 1.4161 8.28657 1.33333 8.00116 1.33337C7.71575 1.33333 7.43646 1.4161 7.19716 1.57164C6.95786 1.72718 6.76884 1.94882 6.65301 2.20967L6.26338 3.08597C6.12533 3.39828 5.89196 3.65888 5.59672 3.83041C5.30019 4.00145 4.95716 4.07431 4.61672 4.03856L3.66042 3.93708C3.37664 3.90706 3.09024 3.96002 2.83596 4.08953C2.58168 4.21903 2.37043 4.41953 2.22783 4.66671C2.08504 4.91373 2.01701 5.19689 2.032 5.48182C2.04699 5.76675 2.14435 6.04121 2.31227 6.27189L2.87671 7.04745C3.07801 7.32427 3.18641 7.65777 3.18634 8.00004C3.18641 8.34232 3.07801 8.67581 2.87671 8.95263L2.31227 9.72819C2.14435 9.95887 2.04699 10.2333 2.032 10.5183C2.01701 10.8032 2.08504 11.0863 2.22783 11.3334C2.37057 11.5804 2.58185 11.7808 2.83609 11.9103C3.09034 12.0398 3.37666 12.0928 3.66042 12.063L4.61375 11.9615C4.9542 11.9258 5.29723 11.9986 5.59375 12.1697C5.8901 12.3407 6.12456 12.6014 6.26338 12.9141Z" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="inherit"></path><path d="M7.99997 10C9.10454 10 9.99997 9.10461 9.99997 8.00004C9.99997 6.89547 9.10454 6.00004 7.99997 6.00004C6.8954 6.00004 5.99997 6.89547 5.99997 8.00004C5.99997 9.10461 6.8954 10 7.99997 10Z" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="inherit"></path></svg> icon in the row of the target project to manage settings, such as networking, maintenance, alert subscriptions, and encryption access, for {{{ .dedicated }}} clusters by project.

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