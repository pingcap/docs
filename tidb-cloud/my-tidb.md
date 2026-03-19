---
title: Use the My TiDB Page
summary: Learn how to use the My TiDB Page to manage your TiDB resources and projects.
---

# Use the My TiDB Page to manage your TiDB resources and projects

In the [TiDB Cloud console](https://tidbcloud.com/), [**My TiDB**](https://tidbcloud.com/tidbs) is a centralized page for all TiDB resources and projects that you can access within the current organization, helping you easily discover, access, and manage your TiDB resources.

## What are TiDB resources and projects?

### TiDB resources

In TiDB Cloud, a TiDB resource is a manageable TiDB deployment unit. It can be one of the following:

- A {{{ .starter }}}, {{{ .essential }}}, or {{{ .premium  }}} [instance](/tidb-cloud/tidb-cloud-glossary.md#instance)
- A {{{ .dedicated }}} [cluster](/tidb-cloud/tidb-cloud-glossary.md#cluster)

### TiDB projects

In TiDB Cloud, you can use [projects](/tidb-cloud/tidb-cloud-glossary.md#project) to group and manage your TiDB resources.

- For {{{ .starter }}}, Essential, and Premium instances, projects are optional, which means you can either group these instances in a project or keep these instances at the organization level.
- For {{{ .dedicated }}} clusters, projects are required.

## Create TiDB resources

To create a TiDB resource, go to the [**My TiDB**](https://tidbcloud.com/tidbs) page, and then click **Create Resource** in the upper-right corner.

For more information, see the following documents:

- [Create a {{{ .starter }}} or Essential Instance](/tidb-cloud/starter/create-tidb-cluster-serverless.md)
- [Create a {{{ .premium }}} Instance](/tidb-cloud/premium/create-tidb-instance-premium.md)
- [Create a TiDB Cloud Dedicated Cluster](/tidb-cloud/create-tidb-cluster.md)

## View and manage TiDB resources

By default, the [**My TiDB**](https://tidbcloud.com/tidbs) page shows a list of all resources within your current organization that you have permission to access.

- To open the overview page of a TiDB resource, click the name of the target resource.
- To perform quick actions on a TiDB resource, such as deleting, renaming, and importing data, click **...** in the row of the target resource.
- If your organization has many instances or clusters, you can use the filters at the top of the page to quickly find what you need.

If you want to view your resources hierarchically by project, click the folder icon above the resource list to switch to the **Project view**.

- TiDB instances that do not belong to any project are displayed in a default folder named `Global instances - in [Your Org Name]`.
- TiDB instances that belong to specific projects are displayed in their corresponding project folders.
- TiDB Cloud Dedicated clusters are displayed in their corresponding project folders. These folders have a **D** in the folder icon to identify the **Dedicated** project type.

For more information about project types, see [Project types](/tidb-cloud/tidb-cloud-glossary.md#project-types).

## Create TiDB projects

To create a new project, click **...** in the upper-right corner, and then click **Create Project**. For more information, see [Create a project](/tidb-cloud/manage-user-access.md#create-a-project).

You can also create a project when creating TiDB resources. For more information, see the following documents:

- [Create a {{{ .starter }}} or Essential Instance](/tidb-cloud/starter/create-tidb-cluster-serverless.md)
- [Create a {{{ .premium }}} Instance](/tidb-cloud/premium/create-tidb-instance-premium.md)
- [Create a TiDB Cloud Dedicated Cluster](/tidb-cloud/create-tidb-cluster.md)

## Manage TiDB projects

In the **Project view**, you can click **...** in the row of the target project to perform quick actions on the project, such as renaming the project or inviting members to the project.

For **Dedicated** projects, you can also click the gear icon in the row of the target project to access more project management operations, such as managing networks, alert subscriptions, and project members.

For more information, see [Manage project access](/tidb-cloud/manage-user-access.md)