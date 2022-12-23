---
title: Identity Access Management
summary: Learn how to manage identity access of TiDB Cloud.
---

# Identity Access Management

This document describes how to manage access to organizations, projects, roles, and user profiles in TiDB Cloud.

To access your TiDB cloud, you must [create a TiDB cloud account](https://tidbcloud.com/free-trial). You can either sign up with email and password to [manage your password using the TiDB Cloud](/tidb-cloud/tidb-cloud-security-password-authentication.md), or choose your Google Workspace or GitHub account for single sign-on (SSO) to TiDB Cloud.

## Organizations and projects

TiDB Cloud provides a hierarchical structure based on organizations and projects to facilitate the management of your TiDB cluster. In the hierarchy of organizations and projects, an organization can contain multiple projects and organization members, and a project can contain multiple clusters and project members.

To access a cluster in a project under an organization, a user must be both a member of the organization and a member of the project. Organization owners can invite users to join the project to create and manage clusters in the project.

Under this structure:

- Billing occurs at the organization level, while retaining visibility of usage in each project and cluster.

- You can view all members in your organization.

- You can also view all members in your project.

## Manage organization access

### View organizations

To check which project you belong to, perform these steps:

1. Click the account name in the upper-right corner of the TiDB Cloud console.

2. Click **Organization Settings**. You can view your organization.

### Switch between organizations

If you are a member of multiple organizations, you can switch your account between organizations.

To switch between organizations, perform these steps:

1. Click <MDSvgIcon name="icon-top-organization" /> **Organization** in the upper-right corner of the TiDB Cloud console.

2. Select **Switch Organization** in the drop-down menu, and click the organization you want to switch to.

### Set the time zone for your organization

If you are the organization owner, you can modify the system display time according to your time zone.

To change the local timezone setting, perform the following steps:

1. Click the account name in the upper-right corner of the TiDB Cloud console.

2. Click **Organization Settings**. The organization settings page is displayed.

3. Click **Time Zone**.

4. Click the drop-down list and select your time zone.

5. Click **Confirm**.

### Invite an organization member

If you are the owner of an organization, you can invite organization members. Otherwise, skip this section.

To invite a member to an organization, perform the following steps:

1. Click <MDSvgIcon name="icon-top-organization" /> **Organization** in the upper-right corner of the TiDB Cloud console.

2. Click **Organization Settings**. The organization settings page is displayed.

3. Click **User Management**, and then select the **By All Users** tab.

4. Click **Invite**.

5. Enter the email address of the user to be invited, select a role for the user, and then choose a project for the user.

    > **Tip:**
    >
    > If you want to invite multiple members at one time, you can enter multiple email addresses.

6. Click **Confirm**. Then the new user is successfully added into the user list. At the same time, an email is sent to the invited email address with a verification link.

7. After receiving this email, the user needs to click the link in the email to verify the identity, and a new page shows.

8. If the invited email address has not been signed up for a TiDB Cloud account, the user is directed to the sign-up page to create an account. If the email address has been signed up for a TiDB Cloud account, the user is directed to the sign-in page, and after sign-in, the account joins the organization automatically.

> **Note:**
>
> The verification link in the email will expire in 24 hours. If your user doesn't receive the email, click **Resend**.

### Remove an organization member

If you are the owner of an organization, you can remove organization members. Otherwise, skip this section.

To remove a member from an organization, perform the following steps:

> **Note:**
>
> If a member is removed from an organization, the member is removed from the belonged projects either.

1. Click the account name in the upper-right corner of the TiDB Cloud console.

2. Click **Organization Settings**. The organization settings page is displayed.

3. Click **User Management**, and then select the **By All Users** tab.

4. Click **Delete** in the user row that you want to delete.

## Manage project access

### Create a project

To create a new project, perform the following steps:

1. Click <MDSvgIcon name="icon-top-organization" /> **Organization** in the upper-right corner of the TiDB Cloud console.

2. Click **Organization Settings**. The **Projects** tab is displayed by default.

3. Click **Create New Project**.

4. Enter your project name.

5. Click **Confirm**.

### View projects

To check which project you belong to, perform the following steps:

1. Click <MDSvgIcon name="icon-top-organization" /> **Organization** in the upper-right corner of the TiDB Cloud console.

2. Click **Organization Settings**. The **Projects** tab is displayed by default.

### Rename a project

To rename a project, perform the following steps:

1. Click <MDSvgIcon name="icon-top-organization" /> **Organization** in the upper-right corner of the TiDB Cloud console.

2. Click **Organization Settings**. The **Projects** tab is displayed by default.

3. In the row of your project to be renamed, click **Rename**.

4. Enter a new project name.

5. Click **Confirm**.

### Invite a project member

If you are the owner of an organization, you can invite project members. Otherwise, skip this section.

To invite a member to a project, perform the following steps:

1. Click the account name in the upper-right corner of the TiDB Cloud console.

2. Click **Organization Settings**. The organization settings page is displayed.

3. Click **User Management**, and then select the **By Project** tab.

4. Click **Invite**.

5. Enter the email address of the user to be invited, select a role for the user, and then choose a project for the user.

    > **Tip:**
    >
    > If you want to invite multiple members at one time, you can enter multiple email addresses.

6. Click **Confirm**. Then the new user is successfully added into the user list. At the same time, an email is sent to the invited email address with a verification link.

7. After receiving this email, the user needs to click the link in the email to verify the identity, and a new page shows.

8. On the new page, the user needs to view and agree with our license, and then click **Submit** to create the account in TiDB Cloud. After that, the user is redirected to the login page.

> **Note:**
>
> The verification link in the email will expire in 24 hours. If your user doesn't receive the email, click **Resend**.

## Remove a project member

If you are the owner of an organization, you can remove project members. Otherwise, skip this section.

To remove a member from a project, perform the following steps:

1. Click the account name in the upper-right corner of the TiDB Cloud console.

2. Click **Organization Settings**. The organization settings page is displayed.

3. Click the **User Management** tab, and then select the **By Project**.

4. Click **Delete** in the user row that you want to delete.

## Manage roles access

If you are the owner of an organization, you can perform the following steps to configure roles for your organization members:

1. Click the account name in the upper-right corner of the TiDB Cloud console.

2. Click **Organization Settings**. The organization settings page is displayed.

3. Click the **User Management** tab, and then select **By All Users**.

4. Click the role of the target member, and then modify the role.

There are four roles in an organization. The permissions of each role are as follows:

|  Permission                                                                           | Owner | Member | Billing Admin | Audit Admin |
|---------------------------------------------------------------------------------------|-------|--------|---------------|-------------|
| Invite members to join the organization, and remove members from the organization     | ✅     | ❌      | ❌             | ❌           |
| Set roles for an organization member                                                  | ✅     | ❌      | ❌             | ❌           |
| Create and rename projects                                                            | ✅     | ❌      | ❌             | ❌           |
| Invite members to join a project, and remove members from a project                   | ✅     | ❌      | ❌             | ❌           |
| Edit time zone                                                                        | ✅     | ❌      | ❌             | ❌           |
| View bills and edit payment information                                               | ✅     | ❌      | ✅             | ❌           |
| View and configure audit logging                                                      | ❌     | ❌      | ❌             | ✅           |
| Obtain project instance management rights                                             | ✅     | ✅      | ✅             | ✅           |
| Manage an API key                                                                     | ✅     | ❌      | ❌             | ❌           |

## Manage user profiles

In TiDB Cloud, you can easily manage your profile, including your first name, last name, and phone number.

1. Click <MDSvgIcon name="icon-top-account-settings" /> **Account** in the upper-right corner of the TiDB Cloud console.

2. Click **Account Settings**. The **Profile** tab is displayed by default.

3. Update the profile information, and then click **Save**.