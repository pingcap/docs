---
title: CREATE USER | TiDB SQL Statement Reference
summary: An overview of the usage of CREATE USER for the TiDB database.
category: reference
aliases: ['/docs/dev/reference/sql/statements/create-user/']
---

# CREATE USER

This statement creates a new user, specified with a password. In the MySQL privilege system, a user is the combination of a username and the host from which they are connecting from. Thus, it is possible to create a user `'newuser2'@'192.168.1.1'` who is only able to connect from the IP address `192.168.1.1`. It is also possible to have two users have the same user-portion, and different permissions as they login from different hosts.

## Synopsis

**CreateUserStmt:**

![CreateUserStmt](/media/sqlgram/CreateUserStmt.png)

**IfNotExists:**

![IfNotExists](/media/sqlgram/IfNotExists.png)

**UserSpecList:**

![UserSpecList](/media/sqlgram/UserSpecList.png)

**UserSpec:**

![UserSpec](/media/sqlgram/UserSpec.png)

**AuthOption:**

![AuthOption](/media/sqlgram/AuthOption.png)

**StringName:**

![StringName](/media/sqlgram/StringName.png)

## Examples

Create a user with the `newuserpassword` password.

```sql
mysql> CREATE USER 'newuser' IDENTIFIED BY 'newuserpassword';
Query OK, 1 row affected (0.04 sec)
```

Create a user which could only be login at `192.168.1.1`.

```sql
mysql> CREATE USER 'newuser2'@'192.168.1.1' IDENTIFIED BY 'newuserpassword';
Query OK, 1 row affected (0.02 sec)
```

Create a user which enforce using TLS connection.

```sql
CREATE USER 'newuser3'@'%' REQUIRE SSL IDENTIFIED BY 'newuserpassword';
Query OK, 1 row affected (0.02 sec)
``` 

Create a user which require X.509 certificate at login.

```sql
CREATE USER 'newuser4'@'%' REQUIRE ISSUER '/C=US/ST=California/L=San Francisco/O=PingCAP' IDENTIFIED BY 'newuserpassword';
Query OK, 1 row affected (0.02 sec)
```

## MySQL compatibility

* Several of the `CREATE` options are not yet supported by TiDB, and will be parsed but ignored.
* TiDB don't support `WITH MAX_QUERIES_PER_HOUR`, `WITH MAX_UPDATES_PER_HOUR`, `WITH MAX_USER_CONNECTIONS` in `CREATE USER`.
* TiDB don't support `DEFAULT ROLE` option.
* TiDB don't support `PASSWORD EXPIRE`, `PASSWORD HISTORY` or other options related to password.
* TiDB don't support  `ACCOUNT LOCK`, `ACCOUNT UNLOCK` option.

## See also

* [Security Compatibility with MySQL](/security-compatibility-with-mysql.md)
* [DROP USER](/sql-statements/sql-statement-drop-user.md)
* [SHOW CREATE USER](/sql-statements/sql-statement-show-create-user.md)
* [ALTER USER](/sql-statements/sql-statement-alter-user.md)
* [Privilege Management](/privilege-management.md)
