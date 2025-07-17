---
title: GRANT <privileges> | TiDB SQL 语句参考
summary: 关于在 TiDB 数据库中使用 GRANT <privileges> 的概述。
---

# `GRANT <privileges>`

此语句用于为 TiDB 中已存在的用户分配权限。TiDB 的权限系统遵循 MySQL 的设计，其中凭据是基于数据库/表的模式进行分配。执行此语句需要拥有 `GRANT OPTION` 权限以及你所分配的所有权限。

## 概述

```ebnf+diagram
GrantStmt ::=
    'GRANT' PrivElemList 'ON' ObjectType PrivLevel 'TO' UserSpecList RequireClauseOpt WithGrantOptionOpt

PrivElemList ::=
    PrivElem ( ',' PrivElem )*

PrivElem ::=
    PrivType ( '(' ColumnNameList ')' )?

PrivType ::=
    'ALL' 'PRIVILEGES'?
|    'ALTER' 'ROUTINE'?
|   'CREATE' ( 'USER' | 'TEMPORARY' 'TABLES' | 'VIEW' | 'ROLE' | 'ROUTINE' )?
|   'TRIGGER'
|   'DELETE'
|   'DROP' 'ROLE'?
|    'PROCESS'
|   'EXECUTE'
|   'INDEX'
|   'INSERT'
|   'SELECT'
|   'SUPER'
|   'SHOW' ( 'DATABASES' | 'VIEW' )
|   'UPDATE'
|    'GRANT' 'OPTION'
|    'REFERENCES'
|    'REPLICATION' ( 'SLAVE' | 'CLIENT' )
|    'USAGE'
|   'RELOAD'
|   'FILE'
|   'CONFIG'
|   'LOCK' 'TABLES'
|   'EVENT'
|   'SHUTDOWN'

ObjectType ::=
    'TABLE'?

PrivLevel ::=
    '*' ( '.' '*' )?
|    Identifier ( '.' ( '*' | Identifier ) )?

UserSpecList ::=
    UserSpec ( ',' UserSpec )*

RequireClauseOpt ::= ('REQUIRE' ('NONE' | 'SSL' | 'X509' | RequireListElement ('AND'? RequireListElement)*))?

RequireListElement ::= 'ISSUER' Issuer | 'SUBJECT' Subject | 'CIPHER' Cipher | 'SAN' SAN | 'TOKEN_ISSUER' TokenIssuer
```

## 示例

```sql
mysql> CREATE USER 'newuser' IDENTIFIED BY 'mypassword';
Query OK, 1 row affected (0.02 sec)

mysql> GRANT ALL ON test.* TO 'newuser';
Query OK, 0 rows affected (0.03 sec)

mysql> SHOW GRANTS FOR 'newuser';
+-------------------------------------------------+
| Grants for newuser@%                            |
+-------------------------------------------------+
| GRANT USAGE ON *.* TO 'newuser'@'%'             |
| GRANT ALL PRIVILEGES ON test.* TO 'newuser'@'%' |
+-------------------------------------------------+
2 rows in set (0.00 sec)
```

## MySQL 兼容性

* 类似于 MySQL，`USAGE` 权限表示登录 TiDB 服务器的能力。
* 目前不支持列级权限。
* 类似于 MySQL，当 sql mode 中没有 `NO_AUTO_CREATE_USER` 时，如果用户不存在，`GRANT` 语句会自动创建一个空密码的新用户。移除此 sql mode（它默认启用）存在安全风险。
* 在 TiDB 中，成功执行 `GRANT <privileges>` 语句后，执行结果会立即在当前连接生效。而 [在 MySQL 中，对于某些权限，执行结果只在后续连接中生效](https://dev.mysql.com/doc/refman/8.0/en/privilege-changes.html)。详情请参见 [TiDB #39356](https://github.com/pingcap/tidb/issues/39356)。

## 相关链接

* [`GRANT <role>`](/sql-statements/sql-statement-grant-role.md)
* [`REVOKE <privileges>`](/sql-statements/sql-statement-revoke-privileges.md)
* [SHOW GRANTS](/sql-statements/sql-statement-show-grants.md)

<CustomContent platform="tidb">

* [Privilege Management](/privilege-management.md)

</CustomContent>