---
title: SQL Proxy Account
summary: Learn about the SQL proxy account in TiDB Cloud.
---

# SQL Proxy Account

A SQL proxy account is a SQL user account that is automatically created by TiDB Cloud for each TiDB Cloud user.

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

## SQL proxy account username

In some cases, the SQL proxy username is exact the same as the TiDB Cloud username, but in other cases it is not the exact same. The specifics are listed below.

TiDB Cloud Dedicated:

- If the length of the TiDB Cloud Dedicated user's email address is less than 32 characters long, the SQL Proxy account name is the email address.
- If the length of the TiDB Cloud Dedicated user's email address is at least 32 characters long, the SQL Proxy account is `prefix($email, 23)_prefix(base58(sha1($email)), 8)`.

TiDB Cloud Serverless:

- If the TiDB Cloud Serverless user's email address is less than 15 characters, the SQL Proxy account is serverless_unique_prefix + "." + email
- If the TiDB Cloud Serverless user's email address is at least 15 characters, the SQL Proxy account is `serverless_unique_prefix + "." + prefix($email, 6)_prefix(base58(sha1($email)), 8)`.

