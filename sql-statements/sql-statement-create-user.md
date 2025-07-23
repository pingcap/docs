---
title: CREATE USER | TiDB SQL 语句参考
summary: 关于在 TiDB 数据库中使用 CREATE USER 的概述。
---

# CREATE USER

此语句用于创建一个新用户，并指定密码。在 MySQL 权限系统中，用户是用户名和连接来源主机的组合。因此，可以创建一个 `'newuser2'@'192.168.1.1'` 用户，该用户只能从 IP 地址 `192.168.1.1` 连接。也可以让两个用户具有相同的用户名部分，但登录来源不同，从而拥有不同的权限。

## 概要

```ebnf+diagram
CreateUserStmt ::=
    'CREATE' 'USER' IfNotExists UserSpecList RequireClauseOpt ConnectionOptions PasswordOption LockOption AttributeOption ResourceGroupNameOption

IfNotExists ::=
    ('IF' 'NOT' 'EXISTS')?

UserSpecList ::=
    UserSpec ( ',' UserSpec )*

RequireClauseOpt ::=
    ( 'REQUIRE' 'NONE' | 'REQUIRE' 'SSL' | 'REQUIRE' 'X509' | 'REQUIRE' RequireList )?

RequireList ::=
    ( "ISSUER" stringLit | "SUBJECT" stringLit | "CIPHER" stringLit | "SAN" stringLit | "TOKEN_ISSUER" stringLit )*

UserSpec ::=
    Username AuthOption

AuthOption ::=
    ( 'IDENTIFIED' ( 'BY' ( AuthString | 'PASSWORD' HashString ) | 'WITH' StringName ( 'BY' AuthString | 'AS' HashString )? ) )?

StringName ::=
    stringLit
|   Identifier

PasswordOption ::= ( 'PASSWORD' 'EXPIRE' ( 'DEFAULT' | 'NEVER' | 'INTERVAL' N 'DAY' )?
| 'PASSWORD' 'HISTORY' ( 'DEFAULT' | N )
| 'PASSWORD' 'REUSE' 'INTERVAL' ( 'DEFAULT' | N 'DAY' )
| 'PASSWORD' 'REQUIRE' 'CURRENT' 'DEFAULT'
| 'FAILED_LOGIN_ATTEMPTS' N
| 'PASSWORD_LOCK_TIME' ( N | 'UNBOUNDED' ) )*

LockOption ::= ( 'ACCOUNT' 'LOCK' | 'ACCOUNT' 'UNLOCK' )?

AttributeOption ::= ( 'COMMENT' CommentString | 'ATTRIBUTE' AttributeString )?

ResourceGroupNameOption::= ( 'RESOURCE' 'GROUP' Identifier)?

RequireClauseOpt ::= ('REQUIRE' ('NONE' | 'SSL' | 'X509' | RequireListElement ('AND'? RequireListElement)*))?

RequireListElement ::= 'ISSUER' Issuer | 'SUBJECT' Subject | 'CIPHER' Cipher | 'SAN' SAN | 'TOKEN_ISSUER' TokenIssuer
```

## 示例

创建一个密码为 `newuserpassword` 的用户。

```sql
mysql> CREATE USER 'newuser' IDENTIFIED BY 'newuserpassword';
Query OK, 1 row affected (0.04 sec)
```

创建一个只能登录到 `192.168.1.1` 的用户。

```sql
mysql> CREATE USER 'newuser2'@'192.168.1.1' IDENTIFIED BY 'newuserpassword';
Query OK, 1 row affected (0.02 sec)
```

创建一个强制使用 TLS 连接登录的用户。

```sql
CREATE USER 'newuser3'@'%' IDENTIFIED BY 'newuserpassword' REQUIRE SSL;
Query OK, 1 row affected (0.02 sec)
```

创建一个在登录时必须使用 X.509 证书的用户。

```sql
CREATE USER 'newuser4'@'%' IDENTIFIED BY 'newuserpassword' REQUIRE ISSUER '/C=US/ST=California/L=San Francisco/O=PingCAP';
Query OK, 1 row affected (0.02 sec)
```

创建一个在创建时被锁定的用户。

```sql
CREATE USER 'newuser5'@'%' ACCOUNT LOCK;
```

```
Query OK, 1 row affected (0.02 sec)
```

创建带有备注的用户。

```sql
CREATE USER 'newuser6'@'%' COMMENT 'This user is created only for test';
SELECT * FROM information_schema.user_attributes;
```

```
+-----------+------+---------------------------------------------------+
| USER      | HOST | ATTRIBUTE                                         |
+-----------+------+---------------------------------------------------+
| newuser6  | %    | {"comment": "This user is created only for test"} |
+-----------+------+---------------------------------------------------+
1 rows in set (0.00 sec)
```

创建带有 `email` 属性的用户。

```sql
CREATE USER 'newuser7'@'%' ATTRIBUTE '{"email": "user@pingcap.com"}';
SELECT * FROM information_schema.user_attributes;
```

```sql
+-----------+------+---------------------------------------------------+
| USER      | HOST | ATTRIBUTE                                         |
+-----------+------+---------------------------------------------------+
| newuser7  | %    | {"email": "user@pingcap.com"} |
+-----------+------+---------------------------------------------------+
1 rows in set (0.00 sec)
```

创建一个不允许重用最后 5 个密码的用户：

```sql
CREATE USER 'newuser8'@'%' PASSWORD HISTORY 5;
```

```
Query OK, 1 row affected (0.02 sec)
```

创建一个密码被手动过期的用户：

```sql
CREATE USER 'newuser9'@'%' PASSWORD EXPIRE;
```

```
Query OK, 1 row affected (0.02 sec)
```

创建使用资源组 `rg1` 的用户。

```sql
CREATE USER 'newuser7'@'%' RESOURCE GROUP rg1;
SELECT USER, HOST, USER_ATTRIBUTES FROM MYSQL.USER WHERE USER='newuser7';
```

```sql
+----------+------+---------------------------+
| USER     | HOST | USER_ATTRIBUTES           |
+----------+------+---------------------------+
| newuser7 | %    | {"resource_group": "rg1"} |
+----------+------+---------------------------+
1 rows in set (0.00 sec)
```

## MySQL 兼容性

以下 `CREATE USER` 选项尚未被 TiDB 支持，虽然会被解析但会被忽略：

* `PASSWORD REQUIRE CURRENT DEFAULT`
* `WITH MAX_QUERIES_PER_HOUR`
* `WITH MAX_UPDATES_PER_HOUR`
* `WITH MAX_USER_CONNECTIONS`

以下 `CREATE USER` 选项 TiDB 也不支持，且不会被解析器接受：

* `DEFAULT ROLE`
* `PASSWORD REQUIRE CURRENT OPTIONAL`

## 相关链接

<CustomContent platform="tidb">

* [Security Compatibility with MySQL](/security-compatibility-with-mysql.md)
* [Privilege Management](/privilege-management.md)

</CustomContent>

* [DROP USER](/sql-statements/sql-statement-drop-user.md)
* [SHOW CREATE USER](/sql-statements/sql-statement-show-create-user.md)
* [ALTER USER](/sql-statements/sql-statement-alter-user.md)
