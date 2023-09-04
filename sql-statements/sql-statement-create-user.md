---
title: CREATE USER | TiDB SQL Statement Reference
summary: An overview of the usage of CREATE USER for the TiDB database.
---

# ユーザーを作成 {#create-user}

このステートメントは、パスワードを指定して新しいユーザーを作成します。 MySQL 権限システムでは、ユーザーはユーザー名と接続元のホストの組み合わせです。これにより、ＩＰアドレス`192.168.1.1`からのみ接続可能なユーザ`'newuser2'@'192.168.1.1'`を作成することができる。 2 人のユーザーに同じユーザー部分を持たせ、異なるホストからログインするときに異なる権限を持たせることもできます。

## あらすじ {#synopsis}

```ebnf+diagram
CreateUserStmt ::=
    'CREATE' 'USER' IfNotExists UserSpecList RequireClauseOpt ConnectionOptions PasswordOption LockOption AttributeOption ResourceGroupNameOption

IfNotExists ::=
    ('IF' 'NOT' 'EXISTS')?

UserSpecList ::=
    UserSpec ( ',' UserSpec )*

UserSpec ::=
    Username AuthOption

AuthOption ::=
    ( 'IDENTIFIED' ( 'BY' ( AuthString | 'PASSWORD' HashString ) | 'WITH' StringName ( 'BY' AuthString | 'AS' HashString )? ) )?

StringName ::=
    stringLit
|   Identifier

PasswordOption ::= ( 'PASSWORD' 'EXPIRE' ( 'DEFAULT' | 'NEVER' | 'INTERVAL' N 'DAY' )? | 'PASSWORD' 'HISTORY' ( 'DEFAULT' | N ) | 'PASSWORD' 'REUSE' 'INTERVAL' ( 'DEFAULT' | N 'DAY' ) | 'FAILED_LOGIN_ATTEMPTS' N | 'PASSWORD_LOCK_TIME' ( N | 'UNBOUNDED' ) )*

LockOption ::= ( 'ACCOUNT' 'LOCK' | 'ACCOUNT' 'UNLOCK' )?

AttributeOption ::= ( 'COMMENT' CommentString | 'ATTRIBUTE' AttributeString )?

ResourceGroupNameOption::= ( 'RESOURCE' 'GROUP' Identifier)?
```

## 例 {#examples}

`newuserpassword`パスワードを使用してユーザーを作成します。

```sql
mysql> CREATE USER 'newuser' IDENTIFIED BY 'newuserpassword';
Query OK, 1 row affected (0.04 sec)
```

`192.168.1.1`にのみログインできるユーザーを作成します。

```sql
mysql> CREATE USER 'newuser2'@'192.168.1.1' IDENTIFIED BY 'newuserpassword';
Query OK, 1 row affected (0.02 sec)
```

TLS 接続を使用してログインすることが強制されるユーザーを作成します。

```sql
CREATE USER 'newuser3'@'%' IDENTIFIED BY 'newuserpassword' REQUIRE SSL;
Query OK, 1 row affected (0.02 sec)
```

ログイン時に X.509 証明書を使用する必要があるユーザーを作成します。

```sql
CREATE USER 'newuser4'@'%' IDENTIFIED BY 'newuserpassword' REQUIRE ISSUER '/C=US/ST=California/L=San Francisco/O=PingCAP';
Query OK, 1 row affected (0.02 sec)
```

作成時にロックされるユーザーを作成します。

```sql
CREATE USER 'newuser5'@'%' ACCOUNT LOCK;
```

```
Query OK, 1 row affected (0.02 sec)
```

コメントを含むユーザーを作成します。

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

`email`属性のユーザーを作成します。

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

最新の 5 つのパスワードの再利用を許可しないユーザーを作成します。

```sql
CREATE USER 'newuser8'@'%' PASSWORD HISTORY 5;
```

```
Query OK, 1 row affected (0.02 sec)
```

パスワードが手動で期限切れになったユーザーを作成します。

```sql
CREATE USER 'newuser9'@'%' PASSWORD EXPIRE;
```

```
Query OK, 1 row affected (0.02 sec)
```

リソース グループ`rg1`を使用するユーザーを作成します。

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

## MySQLの互換性 {#mysql-compatibility}

次の`CREATE USER`オプションは TiDB ではまだサポートされていないため、解析されますが無視されます。

-   TiDB は、 `WITH MAX_QUERIES_PER_HOUR` 、 `WITH MAX_UPDATES_PER_HOUR` 、および`WITH MAX_USER_CONNECTIONS`オプションをサポートしません。
-   TiDB は`DEFAULT ROLE`オプションをサポートしていません。

## こちらも参照 {#see-also}

<CustomContent platform="tidb">
  -   [MySQL とのSecurity互換性](/security-compatibility-with-mysql.md)
  -   [権限管理](/privilege-management.md)
</CustomContent>

-   [ユーザーを削除する](/sql-statements/sql-statement-drop-user.md)
-   [ユーザーの作成を表示](/sql-statements/sql-statement-show-create-user.md)
-   [ユーザーの変更](/sql-statements/sql-statement-alter-user.md)
