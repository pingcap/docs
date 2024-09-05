---
title: SQL Proxy Account
summary: Learn about the SQL proxy account in TiDB Cloud.
---

# SQL Proxy Account

A SQL proxy account is a SQL user account that is automatically created by TiDB Cloud to access the database by SQL Editor and Data Service on behalf of a TiDB Cloud user. For example, `testuser@pingcap.com` is a TiDB Cloud user account, while `3jhEcSimm7keKP8.testuser._41mqK6H4` is its corresponding SQL proxy account.

SQL proxy accounts are needed for the SQL Editor or Data Service to access the database on behalf of a TiDB Cloud user.

## Identify the SQL proxy account

If you want to identify whether a specific SQL account is a SQL proxy account, take the following steps:

1. Examine the `mysql.user` table:

    ```sql
    USE mysql;
    SELECT user FROM user WHERE plugin = 'tidb_auth_token';
    ```

2. Check grants for the SQL account. If roles like `role_admin`, `role_readonly`, or `role_readwrite` are listed, then it is a SQL proxy account.

    ```sql
    SHOW GRANTS for 'username';
    ```

## SQL proxy account creation

The SQL proxy account is created during TiDB Cloud cluster initialization for the TiDB Cloud user who is granted a role with permissions in the cluster.

## SQL proxy account deletion

When a user is removed from [an organization](/tidb-cloud/manage-user-access.md#remove-an-organization-member) or [a project](/tidb-cloud/manage-user-access.md#remove-a-project-member), or their role changes to one that does not have access to the cluster, the SQL proxy account is automatically deleted.

Note that if a SQL proxy account is manually deleted, it will be automatically recreated when the user log in to the TiDB Cloud console next time.

## SQL proxy account username

In some cases, the SQL proxy account username is exactly the same as the TiDB Cloud username, but in other cases it is not exactly the same. The SQL proxy account username is determined by the length of the TiDB Cloud user's email address. The rules are as follows:

- TiDB Cloud Dedicated:

    - If the length of the TiDB Cloud Dedicated user's email address is less than 32 characters, the SQL proxy account name is the email address. <!--to be confirmed; give an example-->
    - If the length of the TiDB Cloud Dedicated user's email address is equal to or more than 32 characters, the SQL proxy account is `prefix($email, 23)_prefix(base58(sha1($email)), 8)`.

- TiDB Cloud Serverless:

    - If the TiDB Cloud Serverless user's email address is less than 15 characters, the SQL proxy account is `serverless_unique_prefix + "." + email`. <!--to be confirmed; give an example-->
    - If the TiDB Cloud Serverless user's email address is equal to or more than 15 characters, the SQL proxy account is `serverless_unique_prefix + "." + prefix($email, 6)_prefix(base58(sha1($email)), 8)`.

## SQL proxy account password

Since SQL proxy accounts are JWT token-based, it is not necessary to manage passwords for these accounts. The security token is automatically managed by the system.

## SQL proxy account roles

The SQL proxy account's role depends on the TiDB Cloud user's IAM role:

- Organization Level:
  - Organization Owner: role_admin
  - Organization Billing Admin: No Proxy account
  - Organization Member: No Proxy account
  - Organization Console Audit admin: No Proxy account

- Project Level:
  - Project Owner: role_admin
  - Project Data Access Read-Write: role_readwrite
  - Project Data Access Read-Only: role_readonly

## SQL proxy account access control

SQL proxy accounts are JWT token-based and only accessible to the Data Service and SQL Editor. It is impossible to access the TiDB Cloud cluster using a SQL proxy account with a username and password.
