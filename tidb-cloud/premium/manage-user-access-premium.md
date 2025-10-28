---
title: Identity Access Management for {{{ .premium }}}
summary: Learn how to manage identity access in {{{ .premium }}}.
---

# Identity Access Management for {{{ .premium }}}

This document describes how to manage access to organizations, instances, roles and user profiles in {{{ .premium }}}.

Before accessing TiDB Cloud, [create a TiDB Cloud account](https://tidbcloud.com/free-trial). You can either sign up with email and password so that you can [manage your password using TiDB Cloud](/tidb-cloud/tidb-cloud-password-authentication.md), or choose your Google, GitHub, or Microsoft account for single sign-on (SSO) to TiDB Cloud.

## Organizations and instances

{{{ .premium }}} provides a hierarchical structure based on organizations and instances to facilitate the management of TiDB Cloud users and TiDB instances. If you are an organization owner, you can create multiple TiDB instances in your organization.

For example:

```
- Your organization
    - Instance 1
    - Instance 2
    - Instance 3
    ...
```

Under this structure:

- To access an organization, a user must be a member of that organization.
- To access an instance, a user must at least have the read access to the instance in that organization.

For more information about user roles and permissions, see [User Roles](#user-roles).

### Organizations

An organization can contain multiple instances.

TiDB Cloud calculates billing at the organization level and provides the billing details for each instance.

If you are an `Organization Owner`, you have the highest permission in your organization.

For example, you can do the following:

- Create different instances for different purposes.
- Assign different users with different organization roles and instance roles.
- Configure organization settings. For example, configure the time zone for your organization.

### Instances

If you are an `Instance Admin`, you can manage instance settings.

For example, you can do the following:

- Delete the instance according to your business needs.
- Configure instance settings.

## User roles

TiDB Cloud defines different user roles to manage different permissions of TiDB Cloud users in organizations, instances, or both.

You can grant roles to a user at the organization level or at the instance level. Make sure to carefully plan the hierarchy of your organizations and instances for security considerations.

### Organization roles

At the organization level, TiDB Cloud defines four roles, in which `Organization Owner` can invite members and grant organization roles to members.

| Permission  | `Organization Owner` | `Organization Billing Manager` | `Organization Billing Viewer` | `Organization Console Audit Manager` | `Organization Viewer` |
|---|---|---|---|---|---|
| Manage organization settings, such as instances, API keys, and time zones. | ✅ | ❌ | ❌ | ❌ | ❌ |
| Invite users to or remove users from an organization, and edit organization roles of users. | ✅ | ❌ | ❌ | ❌ | ❌ |
| All the permissions of `Instance Admin` for all instances in the organization. | ✅ | ❌ | ❌ | ❌ | ❌ |
| Edit payment information for the organization. | ✅ | ✅ | ❌ | ❌ | ❌ |
| View bills and use [cost explorer](/tidb-cloud/tidb-cloud-billing.md#cost-explorer). | ✅ | ✅ | ✅ | ❌ | ❌ |
| Manage TiDB Cloud [console audit logging](/tidb-cloud/tidb-cloud-console-auditing.md) for the organization. | ✅ | ❌ | ❌ | ✅ | ❌ |
| View all users in the organization. | ✅ | ❌ | ❌ | ❌ | ❌ |
| View organization name and time zone. | ✅ | ✅ | ✅ | ✅ | ✅ |

> **Note:**
>
> - The `Organization Console Audit Manager` role (renamed from `Organization Console Audit Admin`) is used to manage audit logging in the TiDB Cloud console, instead of database audit logging.
> - The `Organization Billing Manager` role is renamed from `Organization Billing Admin`, and the `Organization Viewer` role is renamed from `Organization Member`.

### Instance roles

At the instance level, TiDB Cloud defines two roles.

> **Note:**
>
> - `Organization Owner` has all the permissions of <code>Instance Admin</code> for all instances.
> - Each instance role has all the permissions of <code>Organization Viewer</code> by default.
> - If a user in your organization does not belong to any instances, the user does not have any instance permissions.

| Permission  | `Instance Admin` | `Instance Viewer` |
|---|---|---|
| Manage instance settings | ✅ | ❌ |
| Manage [database audit logging](/tidb-cloud/tidb-cloud-auditing.md) of the instance. | ✅ | ❌ |
| Manage instance operations, such as instance creation, modification, and deletion. | ✅ | ❌ |
| Manage instance data such as data import, data backup and restore, and data migration. | ✅ | ❌ |
| Manage [changefeeds](/tidb-cloud/changefeed-overview.md). | ✅ | ❌ |
| Review and reset instance passwords. | ✅ | ❌ |
| View instance overview, backup records, metrics, events, and [changefeeds](/tidb-cloud/changefeed-overview.md) in the instance. | ✅ | ✅ |

## Manage organization access

### View and switch between organizations

To view and switch between organizations, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com), click the combo box in the upper-left corner. The list of organizations you belong to is displayed.

    > **Tip:**
    >
    > - If you are currently on the page of a specific instance, after clicking the combo box in the upper-left corner, you also need to click ← in the combo box to return to the organization list.
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
> You can also [invite a user to your instance](#invite-an-instance-member) directly according to your need, which also makes the user your organization member.

To invite a member to an organization, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com), switch to your target organization using the combo box in the upper-left corner.

2. In the left navigation pane, click **Organization Settings** > **Users**.

3. On the **Users** page, click **Invite User**.

4. Enter the email address of the user to be invited, and then select an organization role for the user.

    > **Tip:**
    >
    > - The default role at the organization level is `Organization Viewer`.
    > - If you want to invite multiple members at one time, you can enter multiple email addresses.
    > - The invited user does not belong to any instances by default. To invite a user to a instance, see [Invite an instance member](#invite-an-instance-member).

5. If you only need to assign the user an organization role and do not need to assign any project or instance roles, disable the **Add access for projects and instances** option.

6. Click **Invite**. Then the new user is successfully added into the user list. At the same time, an email is sent to the invited email address with a verification link.

7. After receiving this email, the user needs to click the link in the email to verify the identity, and a new page shows.

8. If the invited email address has not been signed up for a TiDB Cloud account, the user is directed to the sign-up page to create an account.

> **Note:**
>
> The verification link in the email expires in 24 hours. If the user you want to invite does not receive the email, click **Resend**.

### Modify organization roles

If you are in the `Organization Owner` role, you can modify organization roles of all members in your organization.

To modify the organization role of a member, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com), switch to your target organization using the combo box in the upper-left corner.

2. In the left navigation pane, click **Organization Settings** > **Users**.

3. On the **Users** page, click **...** > **Edit Role** in the row of the target member.

### Remove an organization member

If you are in the `Organization Owner` role, you can remove organization members from your organization.

To remove a member from an organization, take the following steps:

> **Note:**
>
> If a member is removed from an organization, the member is removed from the belonged instance either.

1. In the [TiDB Cloud console](https://tidbcloud.com), switch to your target organization using the combo box in the upper-left corner.

2. In the left navigation pane, click **Organization Settings** > **Users**.

3. On the **Users** page, click **...** > **Delete** in the row of the target member.

## Manage instance access

### Invite an instance member

If you are in the `Organization Owner` role, you can invite members to your instances.

> **Note:**
>
> When a user not in your organization joins your instance, the user automatically joins your organization as well.

To invite a member to a instance, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com), switch to your target organization using the combo box in the upper-left corner.

2. In the left navigation pane, click **Organization Settings** > **Users**.

3. On the **Users** page, click **Invite User**.

4. Enter the email address of the user to be invited, and then select an organization role for the user. 

5. Make sure the **Add access for projects and instances** option is enabled, click **Add access** in the **Instance access** section, and then select an instance role for the user.

6. Click **Add access**. Then the new user is successfully added into the user list. At the same time, an email is sent to the invited email address with a verification link.

7. After receiving this email, the user needs to click the link in the email to verify the identity, and a new page shows.

8. If the invited email address has not been signed up for a TiDB Cloud account, the user is directed to the sign-up page to create an account.

> **Note:**
>
> The verification link in the email will expire in 24 hours. If your user doesn't receive the email, click **Resend**.

### Modify instance roles

If you are in the `Organization Owner` role, you can modify instance roles of all organization members in your organization. 

To modify the instance role of a member, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com), switch to your target organization using the combo box in the upper-left corner.

2. In the left navigation pane, click **Organization Settings** > **Users**.

3. On the **Users** page, click **...** > **Edit Role** of the target member.

## Manage user profiles

In TiDB Cloud, you can easily manage your profile, including your first name, last name, and phone number.

1. In the [TiDB Cloud console](https://tidbcloud.com), click <MDSvgIcon name="icon-top-account-settings" /> in the lower-left corner.

2. Click **Account Settings**.

3. In the displayed dialog, update the profile information, and then click **Update**.