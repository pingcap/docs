---
title: Use the My TiDB Page
summary: Learn how to use the My TiDB Page to manage your TiDB resources and projects.
---

# Use the My TiDB Page to manage your TiDB Cloud resources and projects

In the [TiDB Cloud console](https://tidbcloud.com/), [**My TiDB**](https://tidbcloud.com/tidbs) is a centralized page for all TiDB Cloud resources and projects that you can access within the current organization, helping you easily discover, access, and manage your TiDB resources.

## What are TiDB Cloud resources and projects?

### TiDB Cloud resources

A TiDB Cloud resource is a manageable TiDB Cloud deployment unit. It can be one of the following:

- A {{{ .starter }}}, {{{ .essential }}}, or {{{ .premium  }}} [instance](/tidb-cloud/tidb-cloud-glossary.md#instance)
- A {{{ .dedicated }}} [cluster](/tidb-cloud/tidb-cloud-glossary.md#cluster)

### TiDB Cloud projects

In TiDB Cloud, you can use [projects](/tidb-cloud/tidb-cloud-glossary.md#project) to group and manage your TiDB resources.

- For {{{ .starter }}}, Essential, and Premium instances, projects are optional, which means you can either group these instances in a project or keep these instances at the organization level.
- For {{{ .dedicated }}} clusters, projects are required.

## Create TiDB Cloud resources

To create a TiDB Cloud resource, go to the [**My TiDB**](https://tidbcloud.com/tidbs) page, and then click **Create Resource** in the upper-right corner.

For more information, see the following documents:

- [Create a {{{ .starter }}} or Essential Instance](/tidb-cloud/starter/create-tidb-cluster-serverless.md)
- [Create a {{{ .premium }}} Instance](/tidb-cloud/premium/create-tidb-instance-premium.md)
- [Create a {{{ .dedicated }}} Cluster](/tidb-cloud/create-tidb-cluster.md)

## View and manage TiDB Cloud resources

By default, the [**My TiDB**](https://tidbcloud.com/tidbs) page shows a list of all resources within your current organization that you have permission to access.

- To open the overview page of a TiDB Cloud resource, click the name of the target resource.
- To perform quick actions on a TiDB Cloud resource, such as deleting, renaming, and importing data, click **...** in the row of the target resource.
- If your organization has many instances or clusters, you can use the filters at the top of the page to quickly find what you need.

If you want to view your resources hierarchically by project, click the <svg width="1em" height="1em" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" stroke-width="1.5" class="tiui-icon Folder " style="width: calc(1.125rem * var(--mantine-scale)); height: calc(1.125rem * var(--mantine-scale));"><path d="M8.66671 4.66667L7.92301 3.17928C7.70898 2.7512 7.60195 2.53715 7.44229 2.38078C7.30109 2.24249 7.13092 2.13732 6.94409 2.07287C6.73282 2 6.49351 2 6.0149 2H3.46671C2.71997 2 2.3466 2 2.06139 2.14532C1.8105 2.27316 1.60653 2.47713 1.4787 2.72801C1.33337 3.01323 1.33337 3.3866 1.33337 4.13333V4.66667M1.33337 4.66667H11.4667C12.5868 4.66667 13.1469 4.66667 13.5747 4.88465C13.951 5.0764 14.257 5.38236 14.4487 5.75869C14.6667 6.18651 14.6667 6.74656 14.6667 7.86667V10.8C14.6667 11.9201 14.6667 12.4802 14.4487 12.908C14.257 13.2843 13.951 13.5903 13.5747 13.782C13.1469 14 12.5868 14 11.4667 14H4.53337C3.41327 14 2.85322 14 2.42539 13.782C2.04907 13.5903 1.74311 13.2843 1.55136 12.908C1.33337 12.4802 1.33337 11.9201 1.33337 10.8V4.66667Z" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="inherit"></path></svg> icon above the resource list to switch to the project view.

- TiDB X instances that do not belong to any project are displayed in a table named `Out of project`.
- TiDB X instances that belong to specific projects are displayed in their corresponding TiDB X project tables.
- TiDB Cloud Dedicated clusters are displayed in their corresponding Dedicated project tables. These tables have a **D** in the folder icon to identify the **Dedicated** project type.

For more information about project types, see [Project types](/tidb-cloud/tidb-cloud-glossary.md#project-types).

## Create TiDB Cloud projects

To create a new project, click **...** in the upper-right corner, and then click **Create Project**. For more information, see [Create a project](/tidb-cloud/manage-user-access.md#create-a-project).

You can also create a project when creating TiDB Cloud resources. For more information, see the following documents:

- [Create a {{{ .starter }}} or Essential Instance](/tidb-cloud/starter/create-tidb-cluster-serverless.md)
- [Create a {{{ .premium }}} Instance](/tidb-cloud/premium/create-tidb-instance-premium.md)
- [Create a TiDB Cloud Dedicated Cluster](/tidb-cloud/create-tidb-cluster.md)

## Manage TiDB Cloud projects

On the the [**My TiDB**](https://tidbcloud.com/tidbs) page, click the <svg width="1em" height="1em" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" stroke-width="1.5" class="tiui-icon Folder " style="width: calc(1.125rem * var(--mantine-scale)); height: calc(1.125rem * var(--mantine-scale));"><path d="M8.66671 4.66667L7.92301 3.17928C7.70898 2.7512 7.60195 2.53715 7.44229 2.38078C7.30109 2.24249 7.13092 2.13732 6.94409 2.07287C6.73282 2 6.49351 2 6.0149 2H3.46671C2.71997 2 2.3466 2 2.06139 2.14532C1.8105 2.27316 1.60653 2.47713 1.4787 2.72801C1.33337 3.01323 1.33337 3.3866 1.33337 4.13333V4.66667M1.33337 4.66667H11.4667C12.5868 4.66667 13.1469 4.66667 13.5747 4.88465C13.951 5.0764 14.257 5.38236 14.4487 5.75869C14.6667 6.18651 14.6667 6.74656 14.6667 7.86667V10.8C14.6667 11.9201 14.6667 12.4802 14.4487 12.908C14.257 13.2843 13.951 13.5903 13.5747 13.782C13.1469 14 12.5868 14 11.4667 14H4.53337C3.41327 14 2.85322 14 2.42539 13.782C2.04907 13.5903 1.74311 13.2843 1.55136 12.908C1.33337 12.4802 1.33337 11.9201 1.33337 10.8V4.66667Z" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="inherit"></path></svg> icon to go to the project view. Then, you can click **...** in the row of the target project name to perform quick actions on the project, such as renaming the project or inviting members to the project.

For **Dedicated** projects, you can also click the <svg width="1em" height="1em" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" stroke-width="1.5" class="tiui-icon Settings02 " style="color: var(--mantine-color-carbon-7); width: calc(1rem * var(--mantine-scale)); height: calc(1rem * var(--mantine-scale));"><path d="M6.26338 12.9141L6.65301 13.7904C6.76884 14.0513 6.95786 14.2729 7.19716 14.4284C7.43646 14.584 7.71575 14.6668 8.00116 14.6667C8.28657 14.6668 8.56586 14.584 8.80516 14.4284C9.04446 14.2729 9.23348 14.0513 9.34931 13.7904L9.73894 12.9141C9.87764 12.6032 10.1109 12.3439 10.4056 12.1734C10.7021 12.0023 11.0452 11.9295 11.3856 11.9652L12.3389 12.0667C12.6227 12.0967 12.9091 12.0438 13.1634 11.9143C13.4177 11.7848 13.6289 11.5843 13.7715 11.3371C13.9143 11.0901 13.9823 10.8069 13.9674 10.522C13.9524 10.237 13.855 9.96258 13.6871 9.73189L13.1226 8.95634C12.9217 8.67813 12.8143 8.34325 12.816 8.00004C12.8159 7.65777 12.9243 7.32427 13.1256 7.04745L13.69 6.27189C13.858 6.04121 13.9553 5.76675 13.9703 5.48182C13.9853 5.19689 13.9173 4.91373 13.7745 4.66671C13.6319 4.41953 13.4206 4.21903 13.1664 4.08953C12.9121 3.96002 12.6257 3.90706 12.3419 3.93708L11.3886 4.03856C11.0481 4.07431 10.7051 4.00145 10.4086 3.83041C10.1133 3.65888 9.87995 3.39828 9.7419 3.08597L9.34931 2.20967C9.23348 1.94882 9.04446 1.72718 8.80516 1.57164C8.56586 1.4161 8.28657 1.33333 8.00116 1.33337C7.71575 1.33333 7.43646 1.4161 7.19716 1.57164C6.95786 1.72718 6.76884 1.94882 6.65301 2.20967L6.26338 3.08597C6.12533 3.39828 5.89196 3.65888 5.59672 3.83041C5.30019 4.00145 4.95716 4.07431 4.61672 4.03856L3.66042 3.93708C3.37664 3.90706 3.09024 3.96002 2.83596 4.08953C2.58168 4.21903 2.37043 4.41953 2.22783 4.66671C2.08504 4.91373 2.01701 5.19689 2.032 5.48182C2.04699 5.76675 2.14435 6.04121 2.31227 6.27189L2.87671 7.04745C3.07801 7.32427 3.18641 7.65777 3.18634 8.00004C3.18641 8.34232 3.07801 8.67581 2.87671 8.95263L2.31227 9.72819C2.14435 9.95887 2.04699 10.2333 2.032 10.5183C2.01701 10.8032 2.08504 11.0863 2.22783 11.3334C2.37057 11.5804 2.58185 11.7808 2.83609 11.9103C3.09034 12.0398 3.37666 12.0928 3.66042 12.063L4.61375 11.9615C4.9542 11.9258 5.29723 11.9986 5.59375 12.1697C5.8901 12.3407 6.12456 12.6014 6.26338 12.9141Z" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="inherit"></path><path d="M7.99997 10C9.10454 10 9.99997 9.10461 9.99997 8.00004C9.99997 6.89547 9.10454 6.00004 7.99997 6.00004C6.8954 6.00004 5.99997 6.89547 5.99997 8.00004C5.99997 9.10461 6.8954 10 7.99997 10Z" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="inherit"></path></svg> icon in the row of the target project to access more project management operations, such as managing networks, alert subscriptions, and project members.

For more information, see [Manage project access](/tidb-cloud/manage-user-access.md).