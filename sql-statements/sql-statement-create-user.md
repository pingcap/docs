---
title: CREATE USER | TiDB SQL Statement Reference
summary: An overview of the usage of CREATE USER for the TiDB database.
---

# ユーザーを作成 {#create-user}

このステートメントは、パスワードで指定された新しいユーザーを作成します。 MySQL 特権システムでは、ユーザーはユーザー名と接続元のホストの組み合わせです。これにより、ＩＰアドレス`192.168.1.1`からしか接続できないユーザ`'newuser2'@'192.168.1.1'`を作成することができる。 2 人のユーザーが同じユーザー部分を持ち、異なるホストからログインするときに異なる権限を持つことも可能です。

## あらすじ {#synopsis}

```ebnf+diagram
CreateUserStmt ::=
    'CREATE' 'USER' IfNotExists UserSpecList RequireClauseOpt ConnectionOptions PasswordOption LockOption AttributeOption

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
```

## 例 {#examples}

`newuserpassword`パスワードでユーザーを作成します。

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

コメント付きのユーザーを作成します。

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

属性が`email`のユーザーを作成します。

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

過去 5 回のパスワードの再利用を許可しないユーザーを作成します。

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

## MySQL の互換性 {#mysql-compatibility}

次の`CREATE USER`オプションは TiDB ではまだサポートされておらず、解析されますが無視されます。

-   TiDB は、 `WITH MAX_QUERIES_PER_HOUR` 、 `WITH MAX_UPDATES_PER_HOUR` 、および`WITH MAX_USER_CONNECTIONS`オプションをサポートしていません。
-   TiDB は`DEFAULT ROLE`オプションをサポートしていません。
-   TiDB は、パスワードに関連する`PASSWORD EXPIRE` 、 `PASSWORD HISTORY`またはその他のオプションをサポートしていません。

## こちらもご覧ください {#see-also}

<CustomContent platform="tidb">

-   [MySQL とのSecurityの互換性](/security-compatibility-with-mysql.md)
-   [権限管理](/privilege-management.md)

</CustomContent>

-   [ユーザーをドロップ](/sql-statements/sql-statement-drop-user.md)
-   [ユーザーの作成を表示](/sql-statements/sql-statement-show-create-user.md)
-   [ユーザーの変更](/sql-statements/sql-statement-alter-user.md)
