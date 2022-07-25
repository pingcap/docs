---
title: CREATE USER | TiDB SQL Statement Reference
summary: An overview of the usage of CREATE USER for the TiDB database.
---

# ユーザーを作成 {#create-user}

このステートメントは、パスワードで指定された新しいユーザーを作成します。 MySQL特権システムでは、ユーザーはユーザー名と接続元のホストの組み合わせです。したがって、IPアドレス`192.168.1.1`からのみ接続できるユーザー`'newuser2'@'192.168.1.1'`を作成することができます。 2人のユーザーが同じユーザー部分を持ち、異なるホストからログインするときに異なる権限を持つことも可能です。

## あらすじ {#synopsis}

```ebnf+diagram
CreateUserStmt ::=
    'CREATE' 'USER' IfNotExists UserSpecList RequireClauseOpt ConnectionOptions PasswordOrLockOptions

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
```

## 例 {#examples}

`newuserpassword`のパスワードでユーザーを作成します。

```sql
mysql> CREATE USER 'newuser' IDENTIFIED BY 'newuserpassword';
Query OK, 1 row affected (0.04 sec)
```

`192.168.1.1`にしかログインできないユーザーを作成します。

```sql
mysql> CREATE USER 'newuser2'@'192.168.1.1' IDENTIFIED BY 'newuserpassword';
Query OK, 1 row affected (0.02 sec)
```

TLS接続を使用してログインするように強制されるユーザーを作成します。

```sql
CREATE USER 'newuser3'@'%' REQUIRE SSL IDENTIFIED BY 'newuserpassword';
Query OK, 1 row affected (0.02 sec)
```

ログイン時にX.509証明書を使用する必要があるユーザーを作成します。

```sql
CREATE USER 'newuser4'@'%' REQUIRE ISSUER '/C=US/ST=California/L=San Francisco/O=PingCAP' IDENTIFIED BY 'newuserpassword';
Query OK, 1 row affected (0.02 sec)
```

## MySQLの互換性 {#mysql-compatibility}

次の`CREATE USER`のオプションは、TiDBでまだサポートされておらず、解析されますが無視されます。

-   TiDBは、 `WITH MAX_QUERIES_PER_HOUR` 、および`WITH MAX_UPDATES_PER_HOUR`のオプションをサポートして`WITH MAX_USER_CONNECTIONS`ません。
-   TiDBは`DEFAULT ROLE`オプションをサポートしていません。
-   `PASSWORD HISTORY` `PASSWORD EXPIRE`またはその他のオプションをサポートしていません。
-   TiDBは`ACCOUNT LOCK`と`ACCOUNT UNLOCK`のオプションをサポートしていません。

## も参照してください {#see-also}

<CustomContent platform="tidb">

-   [MySQLとのセキュリティの互換性](/security-compatibility-with-mysql.md)
-   [権限管理](/privilege-management.md)

</CustomContent>

-   [ドロップユーザー](/sql-statements/sql-statement-drop-user.md)
-   [CREATEUSERを表示する](/sql-statements/sql-statement-show-create-user.md)
-   [ALTER USER](/sql-statements/sql-statement-alter-user.md)
