---
title: mysql_user
summary: Learn about the `user` table in the `mysql` schema.
---

# `mysql.user`

`mysql.user` is a frequently used system table. You can display the columns of `mysql.user` by:

```sql
DESC mysql.user;
```

```
+------------------------+----------------------+------+------+-------------------+-------+
| Field                  | Type                 | Null | Key  | Default           | Extra |
+------------------------+----------------------+------+------+-------------------+-------+
| Host                   | char(255)            | NO   | PRI  | NULL              |       |
| User                   | char(32)             | NO   | PRI  | NULL              |       |
| authentication_string  | text                 | YES  |      | NULL              |       |
| plugin                 | char(64)             | YES  |      | NULL              |       |
| Select_priv            | enum('N','Y')        | NO   |      | N                 |       |
| Insert_priv            | enum('N','Y')        | NO   |      | N                 |       |
| Update_priv            | enum('N','Y')        | NO   |      | N                 |       |
| Delete_priv            | enum('N','Y')        | NO   |      | N                 |       |
| Create_priv            | enum('N','Y')        | NO   |      | N                 |       |
| Drop_priv              | enum('N','Y')        | NO   |      | N                 |       |
| Process_priv           | enum('N','Y')        | NO   |      | N                 |       |
| Grant_priv             | enum('N','Y')        | NO   |      | N                 |       |
| References_priv        | enum('N','Y')        | NO   |      | N                 |       |
| Alter_priv             | enum('N','Y')        | NO   |      | N                 |       |
| Show_db_priv           | enum('N','Y')        | NO   |      | N                 |       |
| Super_priv             | enum('N','Y')        | NO   |      | N                 |       |
| Create_tmp_table_priv  | enum('N','Y')        | NO   |      | N                 |       |
| Lock_tables_priv       | enum('N','Y')        | NO   |      | N                 |       |
| Execute_priv           | enum('N','Y')        | NO   |      | N                 |       |
| Create_view_priv       | enum('N','Y')        | NO   |      | N                 |       |
| Show_view_priv         | enum('N','Y')        | NO   |      | N                 |       |
| Create_routine_priv    | enum('N','Y')        | NO   |      | N                 |       |
| Alter_routine_priv     | enum('N','Y')        | NO   |      | N                 |       |
| Index_priv             | enum('N','Y')        | NO   |      | N                 |       |
| Create_user_priv       | enum('N','Y')        | NO   |      | N                 |       |
| Event_priv             | enum('N','Y')        | NO   |      | N                 |       |
| Repl_slave_priv        | enum('N','Y')        | NO   |      | N                 |       |
| Repl_client_priv       | enum('N','Y')        | NO   |      | N                 |       |
| Trigger_priv           | enum('N','Y')        | NO   |      | N                 |       |
| Create_role_priv       | enum('N','Y')        | NO   |      | N                 |       |
| Drop_role_priv         | enum('N','Y')        | NO   |      | N                 |       |
| Account_locked         | enum('N','Y')        | NO   |      | N                 |       |
| Shutdown_priv          | enum('N','Y')        | NO   |      | N                 |       |
| Reload_priv            | enum('N','Y')        | NO   |      | N                 |       |
| FILE_priv              | enum('N','Y')        | NO   |      | N                 |       |
| Config_priv            | enum('N','Y')        | NO   |      | N                 |       |
| Create_Tablespace_Priv | enum('N','Y')        | NO   |      | N                 |       |
| Password_reuse_history | smallint(5) unsigned | YES  |      | NULL              |       |
| Password_reuse_time    | smallint(5) unsigned | YES  |      | NULL              |       |
| User_attributes        | json                 | YES  |      | NULL              |       |
| Token_issuer           | varchar(255)         | YES  |      | NULL              |       |
| Password_expired       | enum('N','Y')        | NO   |      | N                 |       |
| Password_last_changed  | timestamp            | YES  |      | CURRENT_TIMESTAMP |       |
| Password_lifetime      | smallint(5) unsigned | YES  |      | NULL              |       |
+------------------------+----------------------+------+------+-------------------+-------+
44 rows in set (0.00 sec)
```

There are several types of columns in `mysql.user`:

* Scope:
    * `Host` and `User` are used to specify a TiDB account
* Privilege:
    * From `Select_priv` to `Drop_role_priv`, and from `Shutdown_priv` to `Create_Tablespace_Priv`: see [privileges required for TiDB operations](/privilege-management.md#privileges-required-for-tidb-operations)
* Security
    * `authentication_string` and `plugin`: `authentication_string` records credentials for the accounts. Credentials are interpreted using the authentication plugin named in the `plugin` column.
    * `Account_locked` records the account locking state.
    * `Password_reuse_history` and `Password_reuse_time` are used for [password reuse policy](/password-management.md#password-reuse-policy)
    * `User_attributes` provides information about user comments and user attributes
    * `Token_issuer` is used for [`tidb_auth_token`](/security-compatibility-with-mysql.md#tidb_auth_token)
    * `Password_expired`, `Password_last_changed` and `Password_lifetime` are used for [password expiration policy](/password-management.md#password-expiration-policy)

Most of the columns above exist in MySQL's `mysql.user`, except `Token_issuer`.