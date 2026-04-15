---
title: Identity Access Management
summary: Learn how to manage identity access in TiDB Cloud.
---

# Identity Access Management

This document describes how to manage access to organizations, projects, resources, roles, and user profiles in TiDB Cloud.

Before accessing TiDB Cloud, [create a TiDB Cloud account](https://tidbcloud.com/free-trial). You can either sign up with email and password so that you can [manage your password using TiDB Cloud](/tidb-cloud/tidb-cloud-password-authentication.md), or choose your Google, GitHub, or Microsoft account for single sign-on (SSO) to TiDB Cloud.

## Organizations, projects, and resources

TiDB Cloud uses a hierarchical structure based on organizations, projects, and resources to help you manage users and TiDB deployments.

- An organization is a top-level entity (such as a company or a customer) that you use to manage your TiDB Cloud accounts (including a management account with any number of member accounts), [projects](#projects), and [resources](/tidb-cloud/tidb-cloud-glossary.md#tidb-cloud-resource).
- A project is a container for TiDB Cloud resources.

    - For {{{ .starter }}} and Essential instances, a project is an optional logical container, which means you can either group these instances in a project or keep these instances at the organization level.
    - For {{{ .dedicated }}} clusters, a project is infrastructure-bound and required, which means {{{ .dedicated }}} clusters must be grouped in projects for management purposes.
- A resource in TiDB Cloud can be either a TiDB X instance (for example, {{{ .starter }}} or {{{ .essential }}}) or a {{{ .dedicated }}} cluster.

If you are an organization owner, you can create multiple projects in your organization.

- For TiDB X instances, you can either group them into projects or keep them directly at the organization level.
- For TiDB Cloud Dedicated clusters, you must group them into projects.

The following is an example of the hierarchical structure:

```
- Your organization
    - TiDB X instances out of any project
        - {{{ .starter }}} instance 1
        - {{{ .essential }}} instance 1
    - TiDB X project 1
        - {{{ .starter }}} instance 2
        - {{{ .starter }}} instance 3
        - {{{ .essential }}} instance 2
    - TiDB Dedicated project 1
        - {{{ .dedicated }}} cluster 1
        - {{{ .dedicated }}} cluster 2
```

Under this structure:

- To access an organization, a user must be a member of that organization.
- To access a project in an organization, a user must at least have the read access to the project in that organization.
- To access a specific TiDB X instance, a user can be granted access through either a project role or an instance role.
- To access a TiDB Cloud Dedicated cluster, a user must have the read access to the project in which the cluster is located.

For more information about user roles and permissions, see [User Roles](#user-roles).

### Organizations

An organization can contain multiple projects and TiDB X instances that are not grouped in any project.

TiDB Cloud calculates billing at the organization level and provides billing details for each project and resource.

If you are an organization owner, you have the highest permission in your organization.

For example, you can do the following:

- Create different projects (such as development, staging, and production) for different purposes.
- Assign different users with different organization roles, project roles, and instance roles.
- Configure organization settings. For example, configure the time zone for your organization.

### Projects

A project groups and manages TiDB Cloud resources.

In TiDB Cloud, there are three types of projects:

- **TiDB Dedicated project**: This project type is used only for {{{ .dedicated }}} clusters. It helps you manage settings for {{{ .dedicated }}} clusters separately by project, such as RBAC, networks, maintenance, alert subscriptions, and encryption access.
- **TiDB X project**: This project type is used only for TiDB X instances ({{{ .starter }}} and {{{ .essential }}}). It helps you manage RBAC for TiDB X instances by project. A TiDB X project is the default project type when you create a project on the [**My TiDB**](https://tidbcloud.com/tidbs) page.
- **TiDB X virtual project**: This project is virtual and does not provide any management capabilities. It acts as a virtual container for TiDB X instances ({{{ .starter }}} and {{{ .essential }}}) that do not belong to any project, so these instances can be accessed through the TiDB Cloud API by using a project ID. Each organization has a unique virtual project ID. You can get this ID from the [List all accessible projects](https://docs.pingcap.com/tidbcloud/api/v1beta/#tag/Project/operation/ListProjects) endpoint of TiDB Cloud API.

The following table lists the differences between these project types:

| Feature | TiDB Dedicated Project | TiDB X Project | TiDB X Virtual Project |
|---|---|---|---|
| Project icon in the project view of the [**My TiDB**](https://tidbcloud.com/tidbs) page | <svg width="1.1em" height="1.1em" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" stroke-width="0.7" class="tiui-icon DProject " style="width: calc(1rem * var(--mantine-scale)); height: calc(1rem * var(--mantine-scale));"><path d="M11.8845 4.76892L11.2136 5.10433L11.2136 5.10433L11.8845 4.76892ZM10.4161 3.10931L10.6606 2.4003L10.6606 2.4003L10.4161 3.10931ZM11.1634 3.57116L11.6882 3.03535V3.03535L11.1634 3.57116ZM3.09202 3.21799L2.75153 2.54973L2.75153 2.54973L3.09202 3.21799ZM2.21799 4.09202L1.54973 3.75153L1.54973 3.75153L2.21799 4.09202ZM3.63803 20.673L3.29754 21.3413L3.63803 20.673ZM2.32698 19.362L1.65873 19.7025L2.32698 19.362ZM21.673 19.362L22.3413 19.7025L21.673 19.362ZM20.362 20.673L20.7025 21.3413L20.362 20.673ZM20.362 7.32698L20.7025 6.65873L20.362 7.32698ZM21.673 8.63803L22.3413 8.29754L21.673 8.63803ZM8.92285 10.5134V9.76343C8.50864 9.76343 8.17285 10.0992 8.17285 10.5134H8.92285ZM8.92285 17.5796H8.17285C8.17285 17.9938 8.50864 18.3296 8.92285 18.3296V17.5796ZM5.2 3V3.75H9.02229V3V2.25H5.2V3ZM11.8845 4.76892L11.2136 5.10433L12.3292 7.33541L13 7L13.6708 6.66459L12.5553 4.43351L11.8845 4.76892ZM2 7H2.75V6.2H2H1.25V7H2ZM9.02229 3V3.75C9.79458 3.75 10.0018 3.75979 10.1715 3.81832L10.4161 3.10931L10.6606 2.4003C10.1965 2.24021 9.68584 2.25 9.02229 2.25V3ZM11.8845 4.76892L12.5553 4.43351C12.2585 3.84002 12.0389 3.37888 11.6882 3.03535L11.1634 3.57116L10.6386 4.10698C10.7668 4.23258 10.8683 4.41358 11.2136 5.10433L11.8845 4.76892ZM10.4161 3.10931L10.1715 3.81832C10.3467 3.87873 10.5062 3.97733 10.6386 4.10698L11.1634 3.57116L11.6882 3.03535C11.3969 2.75013 11.046 2.53321 10.6606 2.4003L10.4161 3.10931ZM5.2 3V2.25C4.65232 2.25 4.19646 2.24942 3.82533 2.27974C3.44545 2.31078 3.08879 2.37789 2.75153 2.54973L3.09202 3.21799L3.43251 3.88624C3.52307 3.8401 3.66035 3.79822 3.94748 3.77476C4.24336 3.75058 4.62757 3.75 5.2 3.75V3ZM2 6.2H2.75C2.75 5.62757 2.75058 5.24336 2.77476 4.94748C2.79822 4.66035 2.8401 4.52307 2.88624 4.43251L2.21799 4.09202L1.54973 3.75153C1.37789 4.08879 1.31078 4.44545 1.27974 4.82533C1.24942 5.19646 1.25 5.65232 1.25 6.2H2ZM3.09202 3.21799L2.75153 2.54973C2.23408 2.81338 1.81338 3.23408 1.54973 3.75153L2.21799 4.09202L2.88624 4.43251C3.00608 4.19731 3.19731 4.00608 3.43251 3.88624L3.09202 3.21799ZM2 7V7.75H17.2V7V6.25H2V7ZM22 11.8H21.25V16.2H22H22.75V11.8H22ZM17.2 21V20.25H6.8V21V21.75H17.2V21ZM2 16.2H2.75V7H2H1.25V16.2H2ZM6.8 21V20.25C5.94755 20.25 5.35331 20.2494 4.89068 20.2116C4.4368 20.1745 4.17604 20.1054 3.97852 20.0048L3.63803 20.673L3.29754 21.3413C3.74175 21.5676 4.22189 21.662 4.76853 21.7066C5.30641 21.7506 5.9723 21.75 6.8 21.75V21ZM2 16.2H1.25C1.25 17.0277 1.24942 17.6936 1.29336 18.2315C1.33803 18.7781 1.43238 19.2582 1.65873 19.7025L2.32698 19.362L2.99524 19.0215C2.8946 18.824 2.82546 18.5632 2.78838 18.1093C2.75058 17.6467 2.75 17.0525 2.75 16.2H2ZM3.63803 20.673L3.97852 20.0048C3.55516 19.789 3.21095 19.4448 2.99524 19.0215L2.32698 19.362L1.65873 19.7025C2.01825 20.4081 2.59193 20.9817 3.29754 21.3413L3.63803 20.673ZM22 16.2H21.25C21.25 17.0525 21.2494 17.6467 21.2116 18.1093C21.1745 18.5632 21.1054 18.824 21.0048 19.0215L21.673 19.362L22.3413 19.7025C22.5676 19.2582 22.662 18.7781 22.7066 18.2315C22.7506 17.6936 22.75 17.0277 22.75 16.2H22ZM17.2 21V21.75C18.0277 21.75 18.6936 21.7506 19.2315 21.7066C19.7781 21.662 20.2582 21.5676 20.7025 21.3413L20.362 20.673L20.0215 20.0048C19.824 20.1054 19.5632 20.1745 19.1093 20.2116C18.6467 20.2494 18.0525 20.25 17.2 20.25V21ZM21.673 19.362L21.0048 19.0215C20.789 19.4448 20.4448 19.789 20.0215 20.0048L20.362 20.673L20.7025 21.3413C21.4081 20.9817 21.9817 20.4081 22.3413 19.7025L21.673 19.362ZM17.2 7V7.75C18.0525 7.75 18.6467 7.75058 19.1093 7.78838C19.5632 7.82546 19.824 7.8946 20.0215 7.99524L20.362 7.32698L20.7025 6.65873C20.2582 6.43238 19.7781 6.33803 19.2315 6.29336C18.6936 6.24942 18.0277 6.25 17.2 6.25V7ZM22 11.8H22.75C22.75 10.9723 22.7506 10.3064 22.7066 9.76853C22.662 9.2219 22.5676 8.74175 22.3413 8.29754L21.673 8.63803L21.0048 8.97852C21.1054 9.17604 21.1745 9.4368 21.2116 9.89068C21.2494 10.3533 21.25 10.9475 21.25 11.8H22ZM20.362 7.32698L20.0215 7.99524C20.4448 8.21095 20.789 8.55516 21.0048 8.97852L21.673 8.63803L22.3413 8.29754C21.9817 7.59193 21.4081 7.01825 20.7025 6.65873L20.362 7.32698ZM8.92285 10.5134H8.17285V17.5796H8.92285H9.67285V10.5134H8.92285ZM8.92285 10.5134V11.2634C10.7257 11.2634 12.1155 11.585 13.0271 12.1187C13.9047 12.6326 14.3271 13.3261 14.3271 14.1978H15.0771H15.8271C15.8271 12.7118 15.0471 11.5632 13.785 10.8243C12.5568 10.1052 10.8695 9.76343 8.92285 9.76343V10.5134ZM15.0771 14.1978H14.3271C14.3271 14.7061 14.2418 15.086 14.0918 15.3783C13.946 15.6622 13.7158 15.9097 13.3447 16.1211C12.5598 16.5683 11.1931 16.8296 8.92285 16.8296V17.5796V18.3296C11.2286 18.3296 12.939 18.0787 14.0873 17.4244C14.6827 17.0851 15.1331 16.6344 15.4263 16.0633C15.7152 15.5004 15.8271 14.8682 15.8271 14.1978H15.0771Z" fill="#383E40" stroke-width="inherit" stroke="currentColor"></path></svg> <br/> (Folder icon with D inside it) | <svg width="1em" height="1em" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" stroke-width="1.5" class="tiui-icon Folder " style="width: calc(1.125rem * var(--mantine-scale)); height: calc(1.125rem * var(--mantine-scale));"><path d="M8.66671 4.66667L7.92301 3.17928C7.70898 2.7512 7.60195 2.53715 7.44229 2.38078C7.30109 2.24249 7.13092 2.13732 6.94409 2.07287C6.73282 2 6.49351 2 6.0149 2H3.46671C2.71997 2 2.3466 2 2.06139 2.14532C1.8105 2.27316 1.60653 2.47713 1.4787 2.72801C1.33337 3.01323 1.33337 3.3866 1.33337 4.13333V4.66667M1.33337 4.66667H11.4667C12.5868 4.66667 13.1469 4.66667 13.5747 4.88465C13.951 5.0764 14.257 5.38236 14.4487 5.75869C14.6667 6.18651 14.6667 6.74656 14.6667 7.86667V10.8C14.6667 11.9201 14.6667 12.4802 14.4487 12.908C14.257 13.2843 13.951 13.5903 13.5747 13.782C13.1469 14 12.5868 14 11.4667 14H4.53337C3.41327 14 2.85322 14 2.42539 13.782C2.04907 13.5903 1.74311 13.2843 1.55136 12.908C1.33337 12.4802 1.33337 11.9201 1.33337 10.8V4.66667Z" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="inherit"></path></svg> <br/> (Regular folder icon) | The project view displays TiDB X instances that do not assign to any project in the **Out of project** list. |
| Resource type in the project | {{{ .dedicated}}} clusters only | TiDB X instances only | TiDB X instances only |
| Project is optional | ❌ <br/>(Each {{{ .dedicated }}} cluster must belong to a Dedicated project) | ✅ <br/> (You can either group a TiDB X instance in a TiDB X project or keep it at the organization level) | TiDB X instances that you do not assign to any project are automatically grouped in the TiDB X virtual project. |
| Project settings | ✅ | ❌ | ❌ |
| Infrastructure binding | ✅ <br/>(Strong binding) | ❌ | ❌ |
| RBAC model | Organization -> Project | Organization -> Project -> Instance | Organization -> Project -> Instance |
| Project-level RBAC | ✅ | ✅ | ❌ |
| Project-level Billing | ✅ | ✅ | ❌ |
| Instance movement between TiDB X projects or the global scope | ❌ | ✅ | ✅ <br/>(Global only) |

## User roles

TiDB Cloud defines different user roles to manage permissions at the organization, project, and instance levels.

You can grant roles to a user at the organization level, the project level, or the instance level. Make sure to carefully plan the hierarchy of your organizations, projects, and resources for security considerations.

### Organization roles

At the organization level, TiDB Cloud defines five roles, in which `Organization Owner` can invite members and grant organization roles to members.

| Permission  | `Organization Owner` | `Organization Billing Manager` | `Organization Billing Viewer` | `Organization Console Audit Manager` | `Organization Viewer` |
|---|---|---|---|---|---|
| Manage organization settings, such as projects, API keys, and time zones. | ✅ | ❌ | ❌ | ❌ | ❌ |
| Invite users to or remove users from an organization, and edit organization roles of users. | ✅ | ❌ | ❌ | ❌ | ❌ |
| All the permissions of `Project Owner` for all projects in the organization, and all the permissions of TiDB X instance roles for all TiDB X instances in the organization. | ✅ | ❌ | ❌ | ❌ | ❌ |
| Create projects with Customer-Managed Encryption Key (CMEK) enabled. | ✅ | ❌ | ❌ | ❌ | ❌ |
| Edit payment information for the organization. | ✅ | ✅ | ❌ | ❌ | ❌ |
| View bills and use [cost explorer](/tidb-cloud/tidb-cloud-billing.md#cost-explorer). | ✅ | ✅ | ✅ | ❌ | ❌ |
| Manage TiDB Cloud [console audit logging](/tidb-cloud/tidb-cloud-console-auditing.md) for the organization. | ✅ | ❌ | ❌ | ✅ | ❌ |
| View users in the organization and projects in which the member belong to. | ✅ | ✅ | ✅ | ✅ | ✅ |

> **Note:**
>
> - The `Organization Console Audit Manager` role (renamed from `Organization Console Audit Admin`) is used to manage audit logging in the TiDB Cloud console, instead of database audit logging. To manage database auditing, use the `Project Owner` role at the project level.
> - The `Organization Billing Manager` role is renamed from `Organization Billing Admin`, and the `Organization Viewer` role is renamed from `Organization Member`.

### Project roles

At the project level, TiDB Cloud defines four roles, in which `Project Owner` can invite members and grant project roles to members.

> **Note:**
>
> - `Organization Owner` has all the permissions of `Project Owner` for all projects so `Organization Owner` can invite project members and grant project roles to members too.
> - Each project role has all the permissions of `Organization Viewer` by default.
> - If a user in your organization does not belong to any projects, the user does not have any project permissions.
> - For both TiDB X projects and TiDB Dedicated projects, project roles control access to resources in the project. For TiDB Dedicated projects, project roles also control Dedicated-specific project settings.
> - Project roles do not apply to the TiDB X virtual project because TiDB X virtual project does not provide any management capabilities. To manage RBAC for a specific TiDB X instance that are not grouped in any TiDB X project, use [instance roles](#instance-roles).

| Permission  | `Project Owner` | `Project Data Access Read-Write` | `Project Data Access Read-Only` | `Project Viewer` |
|---|---|---|---|---|
| Manage project settings | ✅ | ❌ | ❌ | ❌ |
| Invite users to or remove users from a project, and edit project roles of users. | ✅ | ❌ | ❌ | ❌ |
| Manage [database audit logging](/tidb-cloud/tidb-cloud-auditing.md) of the project. | ✅ | ❌ | ❌ | ❌ |
| Manage [spending limit](/tidb-cloud/manage-serverless-spend-limit.md) for all {{{ .starter }}} instances in the project. | ✅ | ❌ | ❌ | ❌ |
| Manage resource operations in the project, such as creating, modifying, moving, and deleting instances or clusters supported by the project type. | ✅ | ❌ | ❌ | ❌ |
| Manage branches for {{{ .starter }}} and {{{ .essential }}} instances in the project, such as branch creation, connection, and deletion. | ✅ | ❌ | ❌ | ❌ |
| Manage resource data such as data import, data backup and restore, and data migration. | ✅ | ✅ | ❌ | ❌ |
| Manage [Data Service](/tidb-cloud/data-service-overview.md) for data read-only operations such as using or creating endpoints to read data. | ✅ | ✅ | ✅ | ❌ |
| Manage [Data Service](/tidb-cloud/data-service-overview.md) for data read and write operations. | ✅ | ✅ | ❌ | ❌ |
| View resource data using [SQL Editor](/tidb-cloud/explore-data-with-chat2query.md), if supported by the resource type. | ✅ | ✅ | ✅ | ❌ |
| Modify and delete resource data using [SQL Editor](/tidb-cloud/explore-data-with-chat2query.md), if supported by the resource type. | ✅ | ✅ | ❌ | ❌ |
| Manage [changefeeds](/tidb-cloud/changefeed-overview.md). | ✅ | ✅ | ✅ | ❌ |
| Review and reset resource passwords, if supported by the resource type. | ✅ | ❌ | ❌ | ❌ |
| View resource overview, backup records, metrics, events, and [changefeeds](/tidb-cloud/changefeed-overview.md) in the project. | ✅ | ✅ | ✅ | ✅ |

### Instance roles

TiDB X instances support instance-level roles so that you can grant access to a single TiDB X instance without granting the same access to all resources in a project.

> **Note:**
>
> - Instance roles apply only to {{{ .starter }}} and {{{ .essential }}}. TiDB Cloud Dedicated clusters do not support instance roles.
> - `Organization Owner` automatically has all permissions for all TiDB X instances in the organization.
> - Each instance role inherits all the permissions of the `Organization Viewer` role by default.
> - Project roles and instance roles are additive. A user can inherit access from a project role and also have a more specific role on an individual instance.

| Permission  | `Instance Manager` | `TiDB X Instance Data Access Read-Write` | `TiDB X Instance Data Access Read-Only` | `TiDB X Instance Viewer` |
|---|---|---|---|---|
| Manage instance operations, such as instance creation, modification, and deletion. | ✅ | ❌ | ❌ | ❌ |
| View and modify instance data using [SQL Editor](/tidb-cloud/explore-data-with-chat2query.md). | ✅ | ✅ | ❌ | ❌ |
| View instance data using [SQL Editor](/tidb-cloud/explore-data-with-chat2query.md). | ✅ | ✅ | ✅ | ❌ |
| Manage instance-scoped roles. | ✅ | ❌ | ❌ | ❌ |
| View backup records of the TiDB X instance. | ✅ | ❌ | ❌ | ✅ |
| Restore the TiDB X instance from backups. | ✅ | ❌ | ❌ | ❌ |
| View instance overview. | ✅ | ❌ | ❌ | ✅ |
| View network settings. | ✅ | ❌ | ❌ | ✅ |
| View monitor and metrics. | ✅ | ❌ | ❌ | ✅ |
| View alerts. | ✅ | ❌ | ❌ | ✅ |

Use project roles when you want to manage all resources in a project, and use instance roles when you want to grant access only to a specific TiDB X instance.

## Manage organization access

### View and switch between organizations

To view and switch between organizations, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com), click the combo box in the upper-left corner. The list of organizations you belong to is displayed.

    > **Tip:**
    >
    > - If you are currently on the page of a specific TiDB Cloud resource, after clicking the combo box in the upper-left corner, you also need to click **Back to My TiDB** in the combo box to return to the organization list.
    > - If you are a member of multiple organizations, you can click the target organization name in the combo box to switch your account between organizations.

2. To view the detailed information of your organization such as the organization ID and time zone, click the organization name, and then click **Organization Settings** > **General** in the left navigation pane.

### Set the time zone for your organization

If you are in the `Organization Owner` role, you can modify the system display time according to your time zone.

To change the local timezone setting, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com), switch to your target organization using the combo box in the upper-left corner.

2. In the left navigation pane, click **Organization Settings** > **General**.

3. In the **Time Zone** section, select your time zone from the drop-down list.

4. Click **Update**.

### Invite a user to your organization

If you are in the `Organization Owner` role, you can invite users to your organization.

> **Note:**
>
> You can also [invite a user to your project](#invite-a-project-member) or [grant a user access to a TiDB X instance](#grant-access-to-a-tidb-x-instance) directly according to your need, which also makes the user your organization member.

To invite a user to your organization, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com), switch to your target organization using the combo box in the upper-left corner.

2. In the left navigation pane, click **Organization Settings** > **Users**.

3. On the **Users** page, click **Invite User** in the upper-right corner.

4. Enter the email address of the user to be invited.

    > **Tip:**
    >
    > If you want to invite multiple members at one time, you can enter multiple email addresses.

5. (Optional) The invited user does not have any project or instance permissions by default. To grant project or instance roles to the user, do the following:

    - To grant project-level access to the user, click **Add Roles and Select Project**, and then grant roles and select the target projects for the user.
    - To grant access to a specific TiDB X instance to the user, click **Add Roles and Select Instance**, and then grant roles and select the target TiDB X instance for the user.

6. Click **Invite**. Then the new user is successfully added into the user list. At the same time, an email is sent to the invited email address with a verification link.

7. After receiving this email, the user needs to click the link in the email to verify the identity, and a new page shows.

8. If the invited email address has not been signed up for a TiDB Cloud account, the user is directed to the sign-up page to create an account. If the email address has been signed up for a TiDB Cloud account, the user is directed to the sign-in page, and after sign-in, the account joins the organization automatically.

> **Note:**
>
> The verification link in the email expires in 24 hours. If the user you want to invite does not receive the email, click **Resend**.

### Remove an organization member

If you are in the `Organization Owner` role, you can remove organization members from your organization.

To remove a member from an organization, take the following steps:

> **Note:**
>
> If a member is removed from an organization, the member is also removed from all projects and loses all instance access in the organization.

1. In the [TiDB Cloud console](https://tidbcloud.com), switch to your target organization using the combo box in the upper-left corner.

2. In the left navigation pane, click **Organization Settings** > **Users**.

3. On the **Users** page, locate the row of the target member, click **...** in the row, and then click **Delete**.

4. In the confirmation dialog, click **Delete**.

## Manage project access

This section describes how to rename a project and how to invite and remove project members. To learn how to create or manage a project, see [Manage projects](/tidb-cloud/manage-projects-and-resources.md#manage-tidb-cloud-projects).

### Rename a project

If you are in the `Organization Owner` role, you can rename any projects in your organization. If you are in the `Project Owner` role, you can rename your project.

To rename a project, take the following steps:

1. In the TiDB Cloud console, navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page of your organization, and then click the **Project view** tab.

    > **Tip:**
    >
    > If you are in multiple organizations, use the combo box in the upper-left corner to switch to your target organization first.

2. In the project view, locate the table of your target project, click **...** in the upper-right corner of the table, and then click **Rename**.

3. Enter a new project name.

4. Click **Confirm**.

### Invite a project member

If you are in the `Organization Owner` or `Project Owner` role, you can invite members to your projects.

> **Note:**
>
> When a user not in your organization joins your project, the user automatically joins your organization as well.

To invite a member to a project, take the following steps:

1. In the TiDB Cloud console, navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page of your organization, and then click the <svg width="1em" height="1em" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" stroke-width="1.5" class="tiui-icon Folder " style="width: calc(1.125rem * var(--mantine-scale)); height: calc(1.125rem * var(--mantine-scale));"><path d="M8.66671 4.66667L7.92301 3.17928C7.70898 2.7512 7.60195 2.53715 7.44229 2.38078C7.30109 2.24249 7.13092 2.13732 6.94409 2.07287C6.73282 2 6.49351 2 6.0149 2H3.46671C2.71997 2 2.3466 2 2.06139 2.14532C1.8105 2.27316 1.60653 2.47713 1.4787 2.72801C1.33337 3.01323 1.33337 3.3866 1.33337 4.13333V4.66667M1.33337 4.66667H11.4667C12.5868 4.66667 13.1469 4.66667 13.5747 4.88465C13.951 5.0764 14.257 5.38236 14.4487 5.75869C14.6667 6.18651 14.6667 6.74656 14.6667 7.86667V10.8C14.6667 11.9201 14.6667 12.4802 14.4487 12.908C14.257 13.2843 13.951 13.5903 13.5747 13.782C13.1469 14 12.5868 14 11.4667 14H4.53337C3.41327 14 2.85322 14 2.42539 13.782C2.04907 13.5903 1.74311 13.2843 1.55136 12.908C1.33337 12.4802 1.33337 11.9201 1.33337 10.8V4.66667Z" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="inherit"></path></svg> icon to go to the project view.

    > **Tip:**
    >
    > If you are in multiple organizations, use the combo box in the upper-left corner to switch to your target organization first.

2. In the project view, locate the table of your target project, click **...** in the upper-right corner of the table, and then click **Invite**.

3. In the displayed dialog, enter the email address of the user to be invited, and then select a project role for the user.

    > **Tip:**
    >
    > If you want to invite multiple members at one time, you can enter multiple email addresses.

4. Click **Confirm**. Then the new user is successfully added into the user list. At the same time, an email is sent to the invited email address with a verification link.

5. After receiving this email, the user needs to click the link in the email to verify the identity, and a new page shows.

6. If the invited email address has not been signed up for a TiDB Cloud account, the user is directed to the sign-up page to create an account. If the email address has been signed up for a TiDB Cloud account, the user is directed to the sign-in page. After sign-in, the account joins the project automatically.

> **Note:**
>
> The verification link in the email will expire in 24 hours. If the invited user doesn't receive the email, click **Resend**.

### Remove project access for a user

If you are in the `Organization Owner` or `Project Owner` role, you can remove project members.

To remove a member from a project, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com), switch to your target organization using the combo box in the upper-left corner.

2. In the left navigation pane, click **Organization Settings** > **Users**.

3. On the **Users** page, locate the row of the target member, click **...** in the row, and then click **Edit Role**.

4. On the  **Edit Role** dialog, locate the target project, and then click the <svg width="1em" height="1em" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" stroke-width="1.5" class="tiui-icon Trash01 " style="width: calc(1rem * var(--mantine-scale)); height: calc(1rem * var(--mantine-scale));"><path d="M10.6667 4.00004V3.46671C10.6667 2.71997 10.6667 2.3466 10.5213 2.06139C10.3935 1.8105 10.1895 1.60653 9.93865 1.4787C9.65344 1.33337 9.28007 1.33337 8.53333 1.33337H7.46667C6.71993 1.33337 6.34656 1.33337 6.06135 1.4787C5.81046 1.60653 5.60649 1.8105 5.47866 2.06139C5.33333 2.3466 5.33333 2.71997 5.33333 3.46671V4.00004M6.66667 7.66671V11M9.33333 7.66671V11M2 4.00004H14M12.6667 4.00004V11.4667C12.6667 12.5868 12.6667 13.1469 12.4487 13.5747C12.2569 13.951 11.951 14.257 11.5746 14.4487C11.1468 14.6667 10.5868 14.6667 9.46667 14.6667H6.53333C5.41323 14.6667 4.85318 14.6667 4.42535 14.4487C4.04903 14.257 3.74307 13.951 3.55132 13.5747C3.33333 13.1469 3.33333 12.5868 3.33333 11.4667V4.00004" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="inherit"></path></svg> icon.

5. Click **Save**.

## Manage instance access

### Grant access to a TiDB X instance {#grant-access-to-a-tidb-x-instance}

If you are in the `Organization Owner` or `Project Owner` role, you can grant an instance role for a specific TiDB X instance to a user.

> **Note:**
>
> Instance access applies only to TiDB X instances.

To grant access to a TiDB X instance, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com), switch to your target organization using the combo box in the upper-left corner.

2. In the left navigation pane, click **Organization Settings** > **Users**.

3. On the **Users** page, locate the row of the target member, click **...** in the row, and then click **Edit Role**.

    > **Tip:**
    >
    > If the user is not in your organization yet, click **Invite User** in the upper-right corner, and follow the steps in [Invite a user to your organization](#invite-a-user-to-your-organization) to grant the instance role to the user.

4. On the **Edit Role** page, click **Add Role and Select Instance** in the **Instance access** section, and then grant roles and select the target TiDB X instance for the user.

5. Click **Save**.

### Remove instance access for a user

If you are in the `Organization Owner` or `Project Owner` role, you can remove instance access for a user.

To remove instance access for a user, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com), switch to your target organization using the combo box in the upper-left corner.

2. In the left navigation pane, click **Organization Settings** > **Users**.

3. On the **Users** page, locate the row of the target member, click **...** in the row, and then click **Edit Role**.

4. On the  **Edit Role** dialog, locate the target instance, and then click the <svg width="1em" height="1em" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" stroke-width="1.5" class="tiui-icon Trash01 " style="width: calc(1rem * var(--mantine-scale)); height: calc(1rem * var(--mantine-scale));"><path d="M10.6667 4.00004V3.46671C10.6667 2.71997 10.6667 2.3466 10.5213 2.06139C10.3935 1.8105 10.1895 1.60653 9.93865 1.4787C9.65344 1.33337 9.28007 1.33337 8.53333 1.33337H7.46667C6.71993 1.33337 6.34656 1.33337 6.06135 1.4787C5.81046 1.60653 5.60649 1.8105 5.47866 2.06139C5.33333 2.3466 5.33333 2.71997 5.33333 3.46671V4.00004M6.66667 7.66671V11M9.33333 7.66671V11M2 4.00004H14M12.6667 4.00004V11.4667C12.6667 12.5868 12.6667 13.1469 12.4487 13.5747C12.2569 13.951 11.951 14.257 11.5746 14.4487C11.1468 14.6667 10.5868 14.6667 9.46667 14.6667H6.53333C5.41323 14.6667 4.85318 14.6667 4.42535 14.4487C4.04903 14.257 3.74307 13.951 3.55132 13.5747C3.33333 13.1469 3.33333 12.5868 3.33333 11.4667V4.00004" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="inherit"></path></svg> icon.

5. Click **Save**.

## Modify roles of a user

To modify a role of a user in TiDB Cloud, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com), switch to your target organization using the combo box in the upper-left corner.

2. In the left navigation pane, click **Organization Settings** > **Users**.

3. On the **Users** page, locate the row of the target user, click **...** in the row, and then click **Edit Role**.

    - If you are in the `Organization Owner` role, you can modify organization roles, project roles, and instance roles of the target user.
    - If you are in the `Project Owner` role, you can modify project roles and instance roles of the target user.

4. Click **Save**.

## Manage user profiles

In TiDB Cloud, you can easily manage your profile, including your first name, last name, and phone number.

1. In the [TiDB Cloud console](https://tidbcloud.com), click <MDSvgIcon name="icon-top-account-settings" /> in the lower-left corner.

2. Click **Account Settings**.

3. In the displayed dialog, update the profile information, and then click **Update**.
