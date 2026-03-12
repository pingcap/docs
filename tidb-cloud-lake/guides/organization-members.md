---
title: Organization & Members
---

This topic explains the concept of an organization and its members in Databend Cloud.

## Understanding Organization

Organization is an essential concept in Databend Cloud. All the users, databases, warehouses, and other objects in Databend Cloud are associated with an organization. An organization is a group for managing users and their resources.

In an organization of Databend Cloud, data and resources are shared among all users of the organization. Users can collaborate with each other to manage and analyze the organization's data effectively by taking advantage of the cloud-native features.

Please note that data is not shared across organizations, and organizations cannot be combined either if your company owns multiple organizations in Databend Cloud.

### Creating an Organization

When you provide an organization name during the signup process, you create an organization in Databend Cloud with your account as an Admin account. You will also need to select a pricing plan, a cloud provider, and a region for the new organization. For more information, see [Getting Started](../01-getting-started.md).

![](@site/static/img/documents/getting-started/01.jpg)

:::tip
If you're invited by a user who already belongs to an organization in Databend Cloud, the textbox will show that organization's name. In this case, you cannot create another organization.
:::

### Switching to Another Organization

If you're a Databend Cloud user who has accepted invitations from multiple organizations, you can switch between these organizations by clicking on the organization name in the top left corner of the page and selecting the organization you want to switch to.

![Alt text](@site/static/img/documents/overview/switch-org.gif)

## Managing Members

To view all the members in your organization, go to **Admin** > **Users & Roles**. This page provides a list of all members, including their email addresses, roles, join times, and last active times. If you're an `account_admin`, you can also change a member's role or remove a member from your organization.

- The roles listed show the roles assigned to users when they were invited. While these roles can be changed on the page, they cannot be revoked using SQL. However, you can grant additional roles, or grant privileges to roles and assign them to users based on their email addresses. These user accounts, identified by their email addresses, can also function as SQL users in Databend Cloud. Example:

```sql
GRANT SELECT ON *.* TO ROLE writer;
GRANT ROLE writer to 'eric@databend.com';
```

- The page does not display users created using SQL. To view the SQL users that have been created([**CREATE USER**](/sql/sql-commands/ddl/user/user-create-user)、[**CREATE ROLE**](/sql/sql-commands/ddl/user/user-create-role)), use the [SHOW USERS](/sql/sql-commands/ddl/user/user-show-users) command.

### Inviting New Members

To invite a new member to your organization, navigate to the **Admin** > **Users & Roles** page and click on **Invite New Member**. In the dialog box that appears, enter the user's email address and select a role from the list. This list includes built-in roles and any created roles created for your organization. For more information about the roles, see [Roles](/guides/security/access-control/roles).

An invitation email will be sent to the invited user. Inside the email, there will be a link that the user can click on to initiate the signup process.

![Alt text](@site/static/img/documents/overview/invite.png)

![Alt text](@site/static/img/documents/overview/invite2.png)

:::note

- Inviting new members to the organization is a privilege restricted to account_admin roles only.

- If your organization is under the Trial Plan, it permits a maximum of one user. In such a case, you won't have the capability to extend invitations to additional members.
  :::
