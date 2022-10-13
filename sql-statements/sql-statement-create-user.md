---
title: CREATE USER | TiDB SQL Statement Reference
summary: An overview of the usage of CREATE USER for the TiDB database.
---

# ユーザーを作成 {#create-user}

このステートメントは、パスワードで指定された新しいユーザーを作成します。 MySQL 特権システムでは、ユーザーはユーザー名と接続元のホストの組み合わせです。これにより、ＩＰアドレス`192.168.1.1`からしか接続できないユーザ`'newuser2'@'192.168.1.1'`を作成することができる。 2 人のユーザーが同じユーザー部分を持ち、異なるホストからログインするときに異なる権限を持つことも可能です。

## あらすじ {#synopsis}

```ebnf+diagram
CreateUserStmt ::=
    'CREATE' 'USER' IfNotExists UserSpecList RequireClauseOpt ConnectionOptions LockOption

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

LockOption ::= ( 'ACCOUNT' 'LOCK' | 'ACCOUNT' 'UNLOCK' )?
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
CREATE USER 'newuser3'@'%' REQUIRE SSL IDENTIFIED BY 'newuserpassword';
Query OK, 1 row affected (0.02 sec)
```

ログイン時に X.509 証明書を使用する必要があるユーザーを作成します。

```sql
CREATE USER 'newuser4'@'%' REQUIRE ISSUER '/C=US/ST=California/L=San Francisco/O=PingCAP' IDENTIFIED BY 'newuserpassword';
Query OK, 1 row affected (0.02 sec)
```

作成時にロックされるユーザーを作成します。

```sql
CREATE USER 'newuser5'@'%' ACCOUNT LOCK;
```

```
Query OK, 1 row affected (0.02 sec)
```

## MySQL の互換性 {#mysql-compatibility}

次の`CREATE USER`のオプションは TiDB ではまだサポートされておらず、解析されますが無視されます。

-   TiDB は、 `WITH MAX_QUERIES_PER_HOUR` 、 `WITH MAX_UPDATES_PER_HOUR` 、および`WITH MAX_USER_CONNECTIONS`のオプションをサポートしていません。
-   TiDB は`DEFAULT ROLE`オプションをサポートしていません。
-   TiDB は、パスワードに関連する`PASSWORD EXPIRE` 、 `PASSWORD HISTORY`またはその他のオプションをサポートしていません。

## こちらもご覧ください {#see-also}

<CustomContent platform="tidb">

-   [MySQL とのセキュリティの互換性](/security-compatibility-with-mysql.md)
-   [権限管理](/privilege-management.md)

</CustomContent>

-   [ユーザーをドロップ](/sql-statements/sql-statement-drop-user.md)
-   [ユーザーの作成を表示](/sql-statements/sql-statement-show-create-user.md)
-   [ユーザーの変更](/sql-statements/sql-statement-alter-user.md)
