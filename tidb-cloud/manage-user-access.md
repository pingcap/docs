---
title: Identity Access Management
summary: Learn how to manage identity access in TiDB Cloud.
---

# Identity Access Management

This document describes how to manage access to organizations, projects, roles, and user profiles in TiDB Cloud.

Before accessing TiDB Cloud, [create a TiDB Cloud account](https://tidbcloud.com/free-trial). You can either sign up with email and password so that you can [manage your password using TiDB Cloud](/tidb-cloud/tidb-cloud-password-authentication.md), or choose your Google, GitHub, or Microsoft account for single sign-on (SSO) to TiDB Cloud.

## Organizations and projects

TiDB Cloud provides a hierarchical structure based on organizations and projects to facilitate the management of TiDB Cloud users and clusters. If you are an organization owner, you can create multiple projects in your organization.

For example:

```
- Your organization
    - Project 1
        - Cluster 1
        - Cluster 2
    - Project 2
        - Cluster 3
        - Cluster 4
    - Project 3
        - Cluster 5
        - Cluster 6
```

Under this structure:

- To access an organization, a user must be a member of that organization.
- To access a project in an organization, a user must at least have the read access to the project in that organization.
- To manage clusters in a project, a user must be in the `Project Owner` role.

For more information about user roles and permissions, see [User Roles](#user-roles).

### Organizations

An organization can contain multiple projects.

TiDB Cloud calculates billing at the organization level and provides the billing details for each project.

If you are an organization owner, you have the highest permission in your organization.

For example, you can do the following:

- Create different projects (such as development, staging, and production) for different purposes.
- Assign different users with different organization roles and project roles.
- Configure organization settings. For example, configure the time zone for your organization.

### Projects

A project can contain multiple clusters.

If you are a project owner, you can manage clusters and project settings for your project.

For example, you can do the following:

- Create multiple clusters according to your business need.
- Assign different users with different project roles.
- Configure project settings. For example, configure different alert settings for different projects.

## User roles

TiDB Cloud defines different user roles to manage different permissions of TiDB Cloud users in organizations, projects, or both.

You can grant roles to a user at the organization level or at the project level. Make sure to carefully plan the hierarchy of your organizations and projects for security considerations.

### Organization roles

At the organization level, TiDB Cloud defines four roles, in which `Organization Owner` can invite members and grant organization roles to members.

| Permission  | `Organization Owner` | `Organization Billing Manager` | `Organization Billing Viewer` | `Organization Console Audit Manager` | `Organization Viewer` |
|---|---|---|---|---|---|
| Manage organization settings, such as projects, API keys, and time zones. | ✅ | ❌ | ❌ | ❌ | ❌ |
| Invite users to or remove users from an organization, and edit organization roles of users. | ✅ | ❌ | ❌ | ❌ | ❌ |
| All the permissions of `Project Owner` for all projects in the organization. | ✅ | ❌ | ❌ | ❌ | ❌ |
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

At the project level, TiDB Cloud defines three roles, in which `Project Owner` can invite members and grant project roles to members.

> **Note:**
>
> - `Organization Owner` has all the permissions of <code>Project Owner</code> for all projects so `Organization Owner` can invite project members and grant project roles to members too.
> - Each project role has all the permissions of <code>Organization Viewer</code> by default.
> - If a user in your organization does not belong to any projects, the user does not have any project permissions.

| Permission  | `Project Owner` | `Project Data Access Read-Write` | `Project Data Access Read-Only` | `Project Viewer` |
|---|---|---|---|---|
| Manage project settings | ✅ | ❌ | ❌ | ❌ |
| Invite users to or remove users from a project, and edit project roles of users. | ✅ | ❌ | ❌ | ❌ |
| Manage [database audit logging](/tidb-cloud/tidb-cloud-auditing.md) of the project. | ✅ | ❌ | ❌ | ❌ |
| Manage [spending limit](/tidb-cloud/manage-serverless-spend-limit.md) for all TiDB Cloud Serverless clusters in the project. | ✅ | ❌ | ❌ | ❌ |
| Manage cluster operations in the project, such as cluster creation, modification, and deletion. | ✅ | ❌ | ❌ | ❌ |
| Manage branches for TiDB Cloud Serverless clusters in the project, such as branch creation, connection, and deletion. | ✅ | ❌ | ❌ | ❌ |
| Manage [recovery groups](/tidb-cloud/recovery-group-overview.md) for TiDB Cloud Dedicated clusters in the project, such as recovery group creation and deletion. | ✅ | ❌ | ❌ | ❌ |
| Manage cluster data such as data import, data backup and restore, and data migration. | ✅ | ✅ | ❌ | ❌ |
| Manage [Data Service](/tidb-cloud/data-service-overview.md) for data read-only operations such as using or creating endpoints to read data. | ✅ | ✅ | ✅ | ❌ |
| Manage [Data Service](/tidb-cloud/data-service-overview.md) for data read and write operations. | ✅ | ✅ | ❌ | ❌ |
| View cluster data using [SQL Editor](/tidb-cloud/explore-data-with-chat2query.md). | ✅ | ✅ | ✅ | ❌ |
| Modify and delete cluster data using [SQL Editor](/tidb-cloud/explore-data-with-chat2query.md). | ✅ | ✅ | ❌ | ❌ |
| Manage [changefeeds](/tidb-cloud/changefeed-overview.md). | ✅ | ✅ | ✅ | ❌ |
| Review and reset cluster passwords. | ✅ | ❌ | ❌ | ❌ |
| View cluster overview, backup records, metrics, events, and [changefeeds](/tidb-cloud/changefeed-overview.md) in the project. | ✅ | ✅ | ✅ | ✅ |

## Manage organization access

### View and switch between organizations

To view and switch between organizations, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com), click the combo box in the upper-left corner. The list of organizations and projects you belong to is displayed.

    > **Tip:**
    >
    > - If you are currently on the page of a specific cluster, after clicking the combo box in the upper-left corner, you also need to click ← in the combo box to return to the organization and project list.
    > - If you are a member of multiple organizations, you can click the target organization name in the combo box to switch your account between organizations.

2. To view the detailed information of your organization such as the organization ID and time zone, click the organization name, and then click **Organization Settings** > **General** in the left navigation pane.

### Set the time zone for your organization

If you are in the `Organization Owner` role, you can modify the system display time according to your time zone.

To change the local timezone setting, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com), switch to your target organization using the combo box in the upper-left corner.

2. In the left navigation pane, click **Organization Settings** > **General**.

3. In the **Time Zone** section, select your time zone from the drop-down list.

4. Click **Update**.

### Invite an organization member

If you are in the `Organization Owner` role, you can invite users to your organization.

> **Note:**
>
> You can also [invite a user to your project](#invite-a-project-member) directly according to your need, which also makes the user your organization member.

To invite a member to an organization, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com), switch to your target organization using the combo box in the upper-left corner.

2. In the left navigation pane, click **Organization Settings** > **Users**.

3. On the **Users** page, click the **By Organization** tab.

4. Click **Invite**.

5. Enter the email address of the user to be invited, and then select an organization role for the user.

    > **Tip:**
    >
    > - If you want to invite multiple members at one time, you can enter multiple email addresses.
    > - The invited user does not belong to any projects by default. To invite a user to a project, see [Invite a project member](#invite-a-project-member).

6. Click **Confirm**. Then the new user is successfully added into the user list. At the same time, an email is sent to the invited email address with a verification link.

7. After receiving this email, the user needs to click the link in the email to verify the identity, and a new page shows.

8. If the invited email address has not been signed up for a TiDB Cloud account, the user is directed to the sign-up page to create an account. If the email address has been signed up for a TiDB Cloud account, the user is directed to the sign-in page, and after sign-in, the account joins the organization automatically.

> **Note:**
>
> The verification link in the email expires in 24 hours. If the user you want to invite does not receive the email, click **Resend**.

### Modify organization roles

If you are in the `Organization Owner` role, you can modify organization roles of all members in your organization.

To modify the organization role of a member, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com), switch to your target organization using the combo box in the upper-left corner.

2. In the left navigation pane, click **Organization Settings** > **Users**.

3. On the **Users** page, click the **By Organization** tab.

4. Click the role of the target member, and then modify the role.

### Remove an organization member

If you are in the `Organization Owner` role, you can remove organization members from your organization.

To remove a member from an organization, take the following steps:

> **Note:**
>
> If a member is removed from an organization, the member is removed from the belonged projects either.

1. In the [TiDB Cloud console](https://tidbcloud.com), switch to your target organization using the combo box in the upper-left corner.

2. In the left navigation pane, click **Organization Settings** > **Users**.

3. On the **Users** page, click the **By Organization** tab.

4. In the row of the target member, click **...** > **Delete**.

## Manage project access

### View and switch between projects

To view and switch between projects, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com), click the combo box in the upper-left corner. The list of organizations and projects you belong to is displayed.

    > **Tip:**
    >
    > - If you are currently on the page of a specific cluster, after clicking the combo box in the upper-left corner, you also need to click ← in the combo box to return to the organization and project list.
    > - If you are a member of multiple projects, you can click the target project name in the combo box to switch between projects.

2. To view the detailed information of your project, click the project name, and then click **Project Settings** in the left navigation pane.

### Create a project

> **Note:**
>
> For free trial users, you cannot create a new project.

If you are in the `Organization Owner` role, you can create projects in your organization.

To create a new project, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com), switch to your target organization using the combo box in the upper-left corner.

2. In the left navigation pane, click **Projects**.

3. On the **Projects** page, click **Create New Project**.

4. Enter your project name.

5. Click **Confirm**.

### Rename a project

If you are in the `Organization Owner` role, you can rename any projects in your organization. If you are in the `Project Owner` role, you can rename your project.

To rename a project, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com), switch to your target organization using the combo box in the upper-left corner.

2. In the left navigation pane, click **Projects**.

3. In the row of your project to be renamed, click **...** > **Rename**.

4. Enter a new project name.

5. Click **Confirm**.

### Invite a project member

If you are in the `Organization Owner` or `Project Owner` role, you can invite members to your projects.

> **Note:**
>
> When a user not in your organization joins your project, the user automatically joins your organization as well.

To invite a member to a project, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com), switch to your target organization using the combo box in the upper-left corner.

2. In the left navigation pane, click **Organization Settings** > **Users**.

3. On the **Users** page, click the **By Project** tab, and then choose your project in the drop-down list.

4. Click **Invite**.

5. Enter the email address of the user to be invited, and then select a project role for the user.

    > **Tip:**
    >
    > If you want to invite multiple members at one time, you can enter multiple email addresses.

6. Click **Confirm**. Then the new user is successfully added into the user list. At the same time, an email is sent to the invited email address with a verification link.

7. After receiving this email, the user needs to click the link in the email to verify the identity, and a new page shows.

8. If the invited email address has not been signed up for a TiDB Cloud account, the user is directed to the sign-up page to create an account. If the email address has been signed up for a TiDB Cloud account, the user is directed to the sign-in page. After sign-in, the account joins the project automatically.

> **Note:**
>
> The verification link in the email will expire in 24 hours. If your user doesn't receive the email, click **Resend**.

### Modify project roles

If you are in the `Organization Owner` role, you can modify project roles of all project members in your organization. If you are in the `Project Owner` role, you can modify project roles of all members in your project.

To modify the project role of a member, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com), switch to your target organization using the combo box in the upper-left corner.

2. In the left navigation pane, click **Organization Settings** > **Users**.

3. On the **Users** page, click the **By Project** tab, and then choose your project in the drop-down list.

4. In the row of the target member, click the role in the **Role** column, and then choose a new role from the drop-down list.

### Remove a project member

If you are in the `Organization Owner` or `Project Owner` role, you can remove project members.

To remove a member from a project, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com), switch to your target organization using the combo box in the upper-left corner.

2. In the left navigation pane, click **Organization Settings** > **Users**.

3. On the **Users** page, click the **By Project** tab, and then choose your project in the drop-down list.

4. In the row of the target member, click **...** > **Delete**.

## Manage user profiles

In TiDB Cloud, you can easily manage your profile, including your first name, last name, and phone number.

1. In the [TiDB Cloud console](https://tidbcloud.com), click <MDSvgIcon name="icon-top-account-settings" /> in the lower-left corner.

2. Click **Account Settings**.

3. In the displayed dialog, update the profile information, and then click **Update**.
