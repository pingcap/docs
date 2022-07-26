---
title: TiDB User Account Management
summary: Learn how to manage a TiDB user account.
aliases: ['/docs/dev/user-account-management/','/docs/dev/reference/security/user-account-management/']
---

# TiDB User Account Management

This document describes how to manage a TiDB user account.

## User names and passwords

TiDB stores the user accounts in the table of the `mysql.user` system database. Each account is identified by a user name and the client host. Each account may have a password.

You can connect to the TiDB server using the MySQL client, and use the specified account and password to login:

```sql
shell> mysql --port 4000 --user xxx --password
```

Or use the abbreviation of command line parameters:

```sql
shell> mysql -P 4000 -u xxx -p
```

## Add user accounts

You can create TiDB accounts in two ways:

- By using the standard account-management SQL statements intended for creating accounts and establishing their privileges, such as `CREATE USER` and `GRANT`.
- By manipulating the privilege tables directly with statements such as `INSERT`, `UPDATE`, or `DELETE`.

It is recommended to use the account-management statements, because manipulating the privilege tables directly can lead to incomplete updates. You can also create accounts by using third party GUI tools.

{{< copyable "sql" >}}

```sql
CREATE USER [IF NOT EXISTS] user [IDENTIFIED BY 'auth_string'];
```

After you assign the password, TiDB encrypts and stores the `auth_string` in the `mysql.user` table.

{{< copyable "sql" >}}

```sql
CREATE USER 'test'@'127.0.0.1' IDENTIFIED BY 'xxx';
```

The name of a TiDB account consists of a user name and a hostname. The syntax of the account name is 'user_name'@'host_name'.

- `user_name` is case sensitive.

- `host_name` is a hostname or IP address, which supports the wild card `%` or `_`. For example, the hostname `'%'` matches all hosts, and the hostname `'192.168.1.%'` matches all hosts in the subnet.

The host supports fuzzy matching:

{{< copyable "sql" >}}

```sql
CREATE USER 'test'@'192.168.10.%';
```

The `test` user is allowed to log in from any hosts on the `192.168.10` subnet.

If the host is not specified, the user is allowed to log in from any IP. If no password is specified, the default is empty password:

{{< copyable "sql" >}}

```sql
CREATE USER 'test';
```

Equivalent to:

{{< copyable "sql" >}}

```sql
CREATE USER 'test'@'%' IDENTIFIED BY '';
```

If the specified user does not exist, the behavior of automatically creating users depends on `sql_mode`. If the `sql_mode` includes `NO_AUTO_CREATE_USER`, the `GRANT` statement will not create users with an error returned.

For example, assume that the `sql_mode` does not include `NO_AUTO_CREATE_USER`, and you use the following `CREATE USER` and `GRANT` statements to create four accounts:

{{< copyable "sql" >}}

```sql
CREATE USER 'finley'@'localhost' IDENTIFIED BY 'some_pass';
```

{{< copyable "sql" >}}

```sql
GRANT ALL PRIVILEGES ON *.* TO 'finley'@'localhost' WITH GRANT OPTION;
```

{{< copyable "sql" >}}

```sql
CREATE USER 'finley'@'%' IDENTIFIED BY 'some_pass';
```

{{< copyable "sql" >}}

```sql
GRANT ALL PRIVILEGES ON *.* TO 'finley'@'%' WITH GRANT OPTION;
```

{{< copyable "sql" >}}

```sql
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin_pass';
```

{{< copyable "sql" >}}

```sql
GRANT RELOAD,PROCESS ON *.* TO 'admin'@'localhost';
```

{{< copyable "sql" >}}

```sql
CREATE USER 'dummy'@'localhost';
```

To see the privileges granted for an account, use the `SHOW GRANTS` statement:

{{< copyable "sql" >}}

```sql
SHOW GRANTS FOR 'admin'@'localhost';
```

```
+-----------------------------------------------------+
| Grants for admin@localhost                          |
+-----------------------------------------------------+
| GRANT RELOAD, PROCESS ON *.* TO 'admin'@'localhost' |
+-----------------------------------------------------+
```

## Remove user accounts

To remove a user account, use the `DROP USER` statement:

{{< copyable "sql" >}}

```sql
DROP USER 'test'@'localhost';
```

This operation clears the user's records in the `mysql.user` table and the related records in the privilege table.

## Reserved user accounts

TiDB creates the `'root'@'%'` default account during the database initialization.

## Set account resource limits

Currently, TiDB does not support setting account resource limits.

## Assign account passwords

TiDB stores passwords in the `mysql.user` system database. Operations that assign or update passwords are permitted only to users with the `CREATE USER` privilege, or, alternatively, privileges for the `mysql` database (`INSERT` privilege to create new accounts, `UPDATE` privilege to update existing accounts).

- To assign a password when you create a new account, use `CREATE USER` and include an `IDENTIFIED BY` clause:

    ```sql
    CREATE USER 'test'@'localhost' IDENTIFIED BY 'mypass';
    ```

- To assign or change a password for an existing account, use `SET PASSWORD FOR` or `ALTER USER`:

    ```sql
    SET PASSWORD FOR 'root'@'%' = 'xxx';
    ```

    Or:

    ```sql
    ALTER USER 'test'@'localhost' IDENTIFIED BY 'mypass';
    ```

## Forget the `root` password

1. Modify the configuration file by adding `skip-grant-table` in the `security` part:

    ```
    [security]
    skip-grant-table = true
    ```

2. Start TiDB with the modified configuration. Use `root` to log in and then modify the password:

    ```bash
    mysql -h 127.0.0.1 -P 4000 -u root
    ```

When the `skip-grant-table` is set, starting the TiDB process will check whether the user is an administrator of the operating system, and only the `root` user of the operating system can start the TiDB process.

## `FLUSH PRIVILEGES`

Information related to users and privileges is stored in the TiKV server, and TiDB caches this information inside the process. Generally, modification of the related information through `CREATE USER`, `GRANT`, and other statements takes effect quickly within the entire cluster. If the operation is affected by some factors such as temporarily unavailable network, the modification will take effect in about 15 minutes because TiDB will periodically reload the cache information.

If you modified the privilege tables directly, run the following command to apply changes immediately:

```sql
FLUSH PRIVILEGES;
```

For details, see [Privilege Management](/privilege-management.md).
