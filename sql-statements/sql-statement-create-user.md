---
title: CREATE USER | TiDB SQL Statement Reference
summary: TiDB データベースの CREATE USER の使用法の概要。
---

# ユーザーの作成 {#create-user}

この文は、パスワードを指定して新しいユーザーを作成します。MySQLの権限システムでは、ユーザーはユーザー名と接続元のホストの組み合わせです。したがって、IPアドレス`192.168.1.1`からのみ接続できるユーザー`'newuser2'@'192.168.1.1'`作成することが可能です。また、2人のユーザーが同じユーザー領域を持ち、異なるホストからログインするため、異なる権限を持つことも可能になります。

## 概要 {#synopsis}

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

## 例 {#examples}

`newuserpassword`パスワードでユーザーを作成します。

```sql
mysql> CREATE USER 'newuser' IDENTIFIED BY 'newuserpassword';
Query OK, 1 row affected (0.04 sec)
```

`192.168.1.1`のみにログインできるユーザーを作成します。

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

    Query OK, 1 row affected (0.02 sec)

コメント付きのユーザーを作成します。

```sql
CREATE USER 'newuser6'@'%' COMMENT 'This user is created only for test';
SELECT * FROM information_schema.user_attributes;
```

    +-----------+------+---------------------------------------------------+
    | USER      | HOST | ATTRIBUTE                                         |
    +-----------+------+---------------------------------------------------+
    | newuser6  | %    | {"comment": "This user is created only for test"} |
    +-----------+------+---------------------------------------------------+
    1 rows in set (0.00 sec)

属性が`email`ユーザーを作成します。

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

    Query OK, 1 row affected (0.02 sec)

パスワードを手動で期限切れにするユーザーを作成します。

```sql
CREATE USER 'newuser9'@'%' PASSWORD EXPIRE;
```

    Query OK, 1 row affected (0.02 sec)

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

-   `PASSWORD REQUIRE CURRENT DEFAULT`
-   `WITH MAX_QUERIES_PER_HOUR`
-   `WITH MAX_UPDATES_PER_HOUR`
-   `WITH MAX_USER_CONNECTIONS`

次の`CREATE USER`オプションも TiDB ではサポートされておらず、パーサーでは受け入れられ*ません*。

-   `DEFAULT ROLE`
-   `PASSWORD REQUIRE CURRENT OPTIONAL`

## 参照 {#see-also}

<CustomContent platform="tidb">

-   [MySQLとのSecurity互換性](/security-compatibility-with-mysql.md)
-   [権限管理](/privilege-management.md)

</CustomContent>

-   [ユーザーを削除](/sql-statements/sql-statement-drop-user.md)
-   [表示 ユーザーの作成](/sql-statements/sql-statement-show-create-user.md)
-   [ユーザーの変更](/sql-statements/sql-statement-alter-user.md)
