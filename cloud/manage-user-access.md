---
title: Manage User Access
summary: Learn how to manage the user access in your TiDB Cloud cluster.
---

# Manage User Access

This document describes how to manage the user access in your TiDB Cloud cluster.

## Sign in

1. Navigate to the TiDB Cloud login page: <https://tidbcloud.com>.

2. Enter your Email and Password, and click **Sign In**.

> **Note:**
>
> If you have already created a TiDB Cloud account using your Google account, click **Sign in with Google**.

## Sign out

After you have signed into TiDB Cloud, if you need to sign out, perform the following steps:

1. Click the account name on the upper right of the window.

2. Click **Logout**.

## View the organization and project

TiDB Cloud provides a hierarchical structure based on organizations and projects to facilitate the management of your TiDB cluster. In the hierarchy of organizations and projects, an organization can contain multiple projects and organization members, and a project can contain multiple clusters and project members.

Under this structure:

- Billing occurs at the organization level, while retaining visibility of usage in each project and cluster.

- You can view all members in your organization.

- You can also view all members in your project.

To access a cluster in a project under an organization, a user must be both a member of the organization and a member of the project. Organization owners can invite users to join the project to create and manage clusters in the project.

To check which project you belong to, perform these steps:

1. Click the account name in the upper-right corner of the window.
2. Click **Preferences**. The **Project** tab is displayed by default.

## Invite an organization member

If you are the owner of an organization, you can invite organization members. Otherwise, skip this section.

To invite a member to an organization, perform the following steps:

1. Click the account name in the upper-right corner of the window.

2. Click **Preferences**. The organization preferences page is displayed.

3. Click **User Access**, and then select the **By all users** tab.

4. Click the **+ Invite** icon.

5. Enter the email address of the user that you want to invite in the dialog box. 

    > **Tip:**
    > 
    > - If you know which project the user belongs to, you can also choose the project to invite the user as a project member.
    > - If you want to invite multiple members at one time, you can enter multiple email addresses.

6. Click **Confirm**. Then the new user is successfully added into the user list. At the same time, an email is sent to the invited email address with a verification link.

7. After receiving this email, the user needs to click the link in the email to verify the identity, and a new page shows.

8. On the new page, the user needs to view and agree with our license, and then click **Submit** to create the account in TiDB Cloud. After that, the user is redirected to the login page.

> **Note:**
>
> The verification link in the email will expire in 24 hours. If your user doesn't receive the email, click **Resend**.

## Invite a project member

If you are the owner of an organization, you can invite project members. Otherwise, skip this section.

To invite a member to a project, perform the following steps:

1. Click the account name in the upper-right corner of the window.

2. Click **Preferences**. The organization preferences page is displayed.

3. Click **User Access**, and then select the **By Project** tab.

4. Click the **+ Invite** icon.

5. Enter the email address of the user that you want to invite in the dialog box, and then choose the project that you want to invite.

    > **Tip:**
    > 
    > If you want to invite multiple members at one time, you can enter multiple email addresses.

6. Click **Confirm**. Then the new user is successfully added into the user list. At the same time, an email is sent to the invited email address with a verification link.

7. After receiving this email, the user needs to click the link in the email to verify the identity, and a new page shows.

8. On the new page, the user needs to view and agree with our license, and then click **Submit** to create the account in TiDB Cloud. After that, the user is redirected to the login page.

> **Note:**
>
> The verification link in the email will expire in 24 hours. If your user doesn't receive the email, click **Resend**.

## Configure member roles

If you are the owner of an organization, you can perform the following steps to configure roles for your organization members:

1. Click the account name in the upper-right corner of the window.
2. Click **Preferences**. The project preference page is displayed.
3. Click **User Access**, and then select the **By all users** tab.
4. Click the role of the target member, and then modify the role.

There are three roles in an organization. The permissions of each role are as follows:

- Owner: 
    - Invite members to join the organization and remove members from the the organization
    - Configure the roles of organization members
    - Create and rename projects
    - Invite members to join a project and remove members from a project
    - Edit time zone
    - View bills and edit payment information
- Billing Admin: 
    - View bills and edit payment information
    - Can be invited to join a project and obtain project instance management rights
- Member:
    - Can be invited to join a project and obtain project instance management rights

## Remove an organization member

If you are the owner of an organization, you can remove organization members. Otherwise, skip this section.

To remove a member from an organization, perform the following steps:

> **Note:**
>
> If a member is removed from an organization, the member is removed from the belonged projects either.

1. Click the account name in the upper-right corner of the window.

2. Click **Preferences**. The organization preferences page is displayed.

3. Click **User Access by all users**.

4. Click **Delete** in the user row that you want to delete.

## Remove a project member

If you are the owner of an organization, you can remove project members. Otherwise, skip this section.

To remove a member from a project, perform the following steps:

1. Click the account name in the upper-right corner of the window.

2. Click **Preferences**. The organization preferences page is displayed.

3. Click **User Access by project**.

4. Click **Delete** in the user row that you want to delete.

## Set the local time zone

If you are the organization owner, you can modify the system display time according to your time zone. 

To change the local timezone setting, perform the following steps:

1. Click the account name in the upper-right corner of the window.

2. Click **Preferences**. The organization preferences page is displayed.

3. Click **Time Zone**.

4. Click the drop-down list and select your time zone.

5. Click **Confirm**.
