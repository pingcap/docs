---
title: CREATE USER | TiDB SQL Statement Reference
summary: An overview of the usage of CREATE USER for the TiDB database.
---

# CREATE USER

This statement creates a new user, specified with a password. In the MySQL privilege system, a user is the combination of a username and the host from which they are connecting from. Thus, it is possible to create a user `'newuser2'@'192.168.1.1'` who is only able to connect from the IP address `192.168.1.1`. It is also possible to have two users have the same user-portion, and different permissions as they login from different hosts.

## Synopsis

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

## Examples

Create a user with the `newuserpassword` password.

```sql
mysql> CREATE USER 'newuser' IDENTIFIED BY 'newuserpassword';
Query OK, 1 row affected (0.04 sec)
```

Create a user who can only log in to `192.168.1.1`.

```sql
mysql> CREATE USER 'newuser2'@'192.168.1.1' IDENTIFIED BY 'newuserpassword';
Query OK, 1 row affected (0.02 sec)
```

Create a user who is enforced to log in using TLS connection.

```sql
CREATE USER 'newuser3'@'%' IDENTIFIED BY 'newuserpassword' REQUIRE SSL;
Query OK, 1 row affected (0.02 sec)
```

Create a user who is required to use X.509 certificate at login.

```sql
CREATE USER 'newuser4'@'%' IDENTIFIED BY 'newuserpassword' REQUIRE ISSUER '/C=US/ST=California/L=San Francisco/O=PingCAP';
Query OK, 1 row affected (0.02 sec)
```

Create a user who is locked upon creation.

```sql
CREATE USER 'newuser5'@'%' ACCOUNT LOCK;
```

```
Query OK, 1 row affected (0.02 sec)
```

Create a user with a comment.

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

Create a user with an `email` attribute.

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

Create a user who is not allowed to reuse the last 5 passwords:

```sql
CREATE USER 'newuser8'@'%' PASSWORD HISTORY 5;
```

```
Query OK, 1 row affected (0.02 sec)
```

Create a user whose password is manually expired:

```sql
CREATE USER 'newuser9'@'%' PASSWORD EXPIRE;
```

```
Query OK, 1 row affected (0.02 sec)
```

Create a user that uses the resource group `rg1`.

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

## MySQL compatibility

The following `CREATE USER` options are not yet supported by TiDB, and will be parsed but ignored:

* `PASSWORD REQUIRE CURRENT DEFAULT`
* `WITH MAX_QUERIES_PER_HOUR`
* `WITH MAX_UPDATES_PER_HOUR`
* `WITH MAX_USER_CONNECTIONS`

The following `CREATE USER` options are not supported by TiDB either, and are *not* accepted by the parser:

* `DEFAULT ROLE`
* `PASSWORD REQUIRE CURRENT OPTIONAL`

## See also

<CustomContent platform="tidb">

* [Security Compatibility with MySQL](/security-compatibility-with-mysql.md)
* [Privilege Management](/privilege-management.md)

</CustomContent>

* [DROP USER](/sql-statements/sql-statement-drop-user.md)
* [SHOW CREATE USER](/sql-statements/sql-statement-show-create-user.md)
* [ALTER USER](/sql-statements/sql-statement-alter-user.md)
