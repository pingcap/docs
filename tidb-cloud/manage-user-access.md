---
title: Identity Access Management
summary: Learn how to manage identity access in TiDB Cloud.
---

# Identity Access Management

This document describes how to manage access to organizations, projects, roles, and user profiles in TiDB Cloud.

Before accessing TiDB cloud, [create a TiDB cloud account](https://tidbcloud.com/free-trial). You can either sign up with email and password so that you can [manage your password using TiDB Cloud](/tidb-cloud/tidb-cloud-password-authentication.md), or choose your Google, GitHub, or Microsoft account for single sign-on (SSO) to TiDB Cloud.

## Organizations and projects

TiDB Cloud provides a hierarchical structure based on organizations and projects to facilitate the management of TiDB Cloud clusters. If you are an organization owner for TiDB Dedicated, you can create multiple projects in your organization.

```
- Your organization
    - Project 1
        - cluster 1
        - cluster 2
    - Project 2
        - cluster 3
        - cluster 4
    - Project 3
        - cluster 5
        - cluster 6
```

Under this structure:

- To access an organization, a user must be a member of that organization.
- To access a project in an organization, a user must at least have the read access to the project in that organization.
- To manage clusters in a project, a user must be in the project owner role.

For more information about user roles and permissions, see [TiDB Cloud User Roles]().

### Organizations

An organization can contain multiple projects.

TiDB Cloud calculates billing at the organization level and provides the billing details for each project respectively.

If you are an organization owner, you can the highest permission in your organization.

For example, you can do the following:

- Create different projects (such as development, staging, and production) for different purposes
- Assign different users with different roles.
- Configure organization settings. For example, configure the time zone for your organization.

### Projects

An project can contain multiple clusters.

If you are an project owner, you can manage clusters and project settings for your project.

For example, you can do the following:

- Create multiple clusters according to your business need.
- Assign different users with different project roles.
- Configure project settings. For example, configure different alert settings for different projects.

## User Roles

TiDB Cloud user roles define the actions TiDB Cloud users can perform in organizations, projects, or both. Organization owner and project owner can manage TiDB Cloud users and their roles within their respective organizations and projects.

You can apply these permissions only at the organization level or the project level. Please carefully plan the hierarchy of your organizations and projects. To learn more, see Organization and Projects.

### Organization roles

<table border="0" cellspacing="0" cellpadding="0" width="500">
  <thead>
    <tr>
      <td>
        <p><strong>Organization Roles</strong></p>
      </td>
      <td>
        <p><strong>Description</strong></p>
      </td>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <p>Organization Owner</p>
      </td>
      <td>
        <p>Grants root access to the organization, including:</p>
        <ul type="disc">
          <li>Project Owner access to all projects in the organization</li>
          <li>Privileges to administer organization settings.</li>
          <li>Privileges to invite/remove/edit TiDB Cloud users within the organization.</li>
          <li>All the privileges granted by the other organization roles combined.</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>
        <p>Organization Billing Admin</p>
      </td>
      <td>
        <p>Grants the following access:</p>
        <ul type="disc">
          <li>Privileges to administer billing information for the organization.</li>
          <li>All the privileges granted by organization member role.</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>
        <p>Organization Console Audit Admin</p>
      </td>
      <td>
        <p>Grants the following access:</p>
        <ul type="disc">
          <li>Privileges to administer TiDB Cloud console audit logging for the organization.</li>
          <li>All the privileges granted by organization member role.</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>
        <p>Organization Member</p>
      </td>
      <td>
        <p>Provides read-only access to the settings, users in the organization and the projects they belong to.</p>
      </td>
    </tr>
  </tbody>
</table>

### Project roles

<table>
  <colgroup>
    <col width="277"/>
    <col width="503"/>  
  </colgroup>
  <thead>
    <tr>
      <th colspan="1" rowspan="1">
        <div>
          Project Roles
        </div>
      </th>
      <th colspan="1" rowspan="1">
        <div>  
          Description
        </div>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td colspan="1" rowspan="1">
        <div>
          Project Owner
        </div>
        <div><br/></div>
      </td>
      <td colspan="1" rowspan="1">
        <div>
          Grants the privileges to perform the following actions:
        </div>
        <ul start="1">
          <li>Create and delete cluster</li>
          <li>Manage project settings for network access, 3rd party integration, alert subscription, maintenance and recycle bin</li>
          <li>Invite/remove/edit TiDB Cloud users in the project</li>
          <li>Manage cluster database audit logs</li>
          <li>Manage backup and restore for all clusters in the project</li>
          <li>Manage tasks for import, data migration and changefeed</li>
          <li>Manage spend limits for all serverless clusters in the project</li>
          <li>Access to Chat2Query and Data Service</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td colspan="1" rowspan="1">
        <div>
          Project Data Access Read-Write  
        </div>
        <div><br/></div>
      </td>
      <td colspan="1" rowspan="1">
        <div>
          Grants the privileges to perform the following actions:
        </div>
        <ul start="1">
          <li>View clusters in the project</li>
          <li>View cluster backup records</li>
          <li>Manage tasks for import, data migration and changefeed</li>
          <li>View, modify and delete database from Chat2Query</li>
          <li>Manage Data Service</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td colspan="1" rowspan="1">
        <div>
          Project Data Access Read-Only
        </div>
      </td>
      <td colspan="1" rowspan="1">
        <div>
          Grants the privileges to perform the following actions:
        </div>
        <ul start="1">
          <li>View clusters in the project</li>
          <li>view cluster backup records</li>
          <li>View database from Chat2Query</li>
          <li>Manage Data Service with read-only</li>
        </ul>
      </td>
    </tr>
  </tbody>
</table>


## Manage organization access

### View organizations

To check which organizations you belong to, take the following steps:

1. Click <MDSvgIcon name="icon-top-organization" /> in the lower-left corner of the TiDB Cloud console.
2. Click **Organization Settings**. You can view your organization on the page that is displayed.

### Switch between organizations

If you are a member of multiple organizations, you can switch your account between organizations.

To switch between organizations, take the following steps:

1. Click <MDSvgIcon name="icon-top-organization" /> in the lower-left corner of the TiDB Cloud console.
2. Select **Switch Organization** in the drop-down menu, and click the organization you want to switch to.

### Set the time zone for your organization

If you are the organization owner, you can modify the system display time according to your time zone.

To change the local timezone setting, take the following steps:

1. Click <MDSvgIcon name="icon-top-organization" /> in the lower-left corner of the TiDB Cloud console.

2. Click **Organization Settings**. The organization settings page is displayed.

3. Click the **Time Zone** tab.

4. Click the drop-down list and select your time zone.

5. Click **Confirm**.

### Invite an organization member

If you are the owner of an organization, you can invite organization members.

To invite a member to an organization, take the following steps:

1. Click <MDSvgIcon name="icon-top-organization" /> in the lower-left corner of the TiDB Cloud console.

2. Click **Organization Settings**. The organization settings page is displayed.

3. Click the  **User Management** tab, and then select **By All Users**.

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
> The verification link in the email expires in 24 hours. If the user you want to invite does not receive the email, click **Resend**.

### Remove an organization member

If you are the owner of an organization, you can remove organization members.

To remove a member from an organization, take the following steps:

> **Note:**
>
> If a member is removed from an organization, the member is removed from the belonged projects either.

1. Click <MDSvgIcon name="icon-top-organization" /> in the lower-left corner of the TiDB Cloud console.

2. Click **Organization Settings**. The organization settings page is displayed.

3. Click the **User Management** tab, and then select **By All Users**.

4. Click **Delete** in the user row that you want to delete.

## Manage project access

### View projects

To check which project you belong to, take the following steps:

1. Click <MDSvgIcon name="icon-top-organization" /> in the lower-left corner of the TiDB Cloud console.

2. Click **Organization Settings**. The **Projects** tab is displayed by default.

> **Tip:**
>
> If you have multiple projects, you can click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner and switch to another project.

### Create a project

> **Note:**
>
> For free trial users, you cannot create a new project.

To create a new project, take the following steps:

1. Click <MDSvgIcon name="icon-top-organization" /> in the lower-left corner of the TiDB Cloud console.

2. Click **Organization Settings**. The **Projects** tab is displayed by default.

3. Click **Create New Project**.

4. Enter your project name.

5. Click **Confirm**.

### Rename a project

To rename a project, take the following steps:

1. Click <MDSvgIcon name="icon-top-organization" /> in the lower-left corner of the TiDB Cloud console.

2. Click **Organization Settings**. The **Projects** tab is displayed by default.

3. In the row of your project to be renamed, click **Rename**.

4. Enter a new project name.

5. Click **Confirm**.

### Invite a project member

If you are the owner of an organization, you can invite project members.

To invite a member to a project, take the following steps:

1. Click <MDSvgIcon name="icon-top-organization" /> in the lower-left corner of the TiDB Cloud console.

2. Click **Organization Settings**. The organization settings page is displayed.

3. Click the **User Management** tab, and then select **By Project**.

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

### Remove a project member

If you are the owner of an organization, you can remove project members.

To remove a member from a project, take the following steps:

1. Click <MDSvgIcon name="icon-top-organization" /> in the lower-left corner of the TiDB Cloud console.

2. Click **Organization Settings**. The organization settings page is displayed.

3. Click the **User Management** tab, and then select the **By Project**.

4. Click **Delete** in the user row that you want to delete.

## Manage role access

If you are the owner of an organization, you can take the following steps to configure roles for your organization members:

1. Click <MDSvgIcon name="icon-top-organization" /> in the lower-left corner of the TiDB Cloud console.

2. Click **Organization Settings**. The organization settings page is displayed.

3. Click the **User Management** tab, and then select **By All Users**.

4. Click the role of the target member, and then modify the role.

There are four roles in an organization. The permissions of each role are as follows:

|  Permission                                                                           | Owner | Member | Billing Admin | Audit Admin |
|---------------------------------------------------------------------------------------|-------|--------|---------------|-------------|
| Invite members to or remove members from an organization     | ✅     | ❌      | ❌             | ❌           |
| Set roles for an organization member                                                  | ✅     | ❌      | ❌             | ❌           |
| Create and rename projects                                                            | ✅     | ❌      | ❌             | ❌           |
| Invite members to or remove members from a project          | ✅     | ❌      | ❌             | ❌           |
| Edit time zone                                                                        | ✅     | ❌      | ❌             | ❌           |
| View bills and edit payment information                                               | ✅     | ❌      | ✅             | ❌           |
| Enable, view, or disable [console audit logging](/tidb-cloud/tidb-cloud-console-auditing.md)                                                      | ✅     | ❌      | ❌             | ✅           |
| View and configure [database audit logging](/tidb-cloud/tidb-cloud-auditing.md)                                                      | ❌     | ❌      | ❌             | ✅           |
| Obtain project instance management permissions                                             | ✅     | ✅      | ✅             | ✅           |
| Manage an API key                                                                     | ✅     | ❌      | ❌             | ❌           |

> **Note:**
>
> Currently, the Audit Admin role is only visible upon request.
>
> - For [console audit logging](/tidb-cloud/tidb-cloud-console-auditing.md), it is recommended that you use the Owner role directly. If you need to use the Audit Admin role, click **?** in the lower-right corner of the [TiDB Cloud console](https://tidbcloud.com) and click **Chat with Us**. Then, fill in "Apply for the Audit Admin role" in the **Description** field and click **Send**.
> - For [database audit logging](/tidb-cloud/tidb-cloud-auditing.md), to get the Audit Admin role, click **?** in the lower-right corner of the [TiDB Cloud console](https://tidbcloud.com) and click **Chat with Us**. Then, fill in "Apply for database audit logging" in the **Description** field and click **Send**.

## Manage user profiles

In TiDB Cloud, you can easily manage your profile, including your first name, last name, and phone number.

1. Click <MDSvgIcon name="icon-top-account-settings" /> in the lower-left corner of the TiDB Cloud console.

2. Click **Account Settings**. The **Profile** tab is displayed by default.

3. Update the profile information, and then click **Save**.
