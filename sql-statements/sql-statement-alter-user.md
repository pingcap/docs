---
title: ALTER USER | TiDB SQL Statement Reference
summary: An overview of the usage of ALTER USER for the TiDB database.
---

# ユーザーの変更 {#alter-user}

このステートメントは、TiDB 特権システム内の既存のユーザーを変更します。 MySQL 特権システムでは、ユーザーはユーザー名と接続元のホストの組み合わせです。これにより、ＩＰアドレス`192.168.1.1`からしか接続できないユーザ`'newuser2'@'192.168.1.1'`を作成することができる。 2 人のユーザーが同じユーザー部分を持ち、異なるホストからログインするときに異なる権限を持つことも可能です。

## あらすじ {#synopsis}

```ebnf+diagram
AlterUserStmt ::=
    'ALTER' 'USER' IfExists (UserSpecList RequireClauseOpt ConnectionOptions LockOption | 'USER' '(' ')' 'IDENTIFIED' 'BY' AuthString)

UserSpecList ::=
    UserSpec ( ',' UserSpec )*

UserSpec ::=
    Username AuthOption

Username ::=
    StringName ('@' StringName | singleAtIdentifier)? | 'CURRENT_USER' OptionalBraces

AuthOption ::=
    ( 'IDENTIFIED' ( 'BY' ( AuthString | 'PASSWORD' HashString ) | 'WITH' StringName ( 'BY' AuthString | 'AS' HashString )? ) )?

LockOption ::= ( 'ACCOUNT' 'LOCK' | 'ACCOUNT' 'UNLOCK' )?
```

## 例 {#examples}

```sql
mysql> CREATE USER 'newuser' IDENTIFIED BY 'newuserpassword';
Query OK, 1 row affected (0.01 sec)

mysql> SHOW CREATE USER 'newuser';
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| CREATE USER for newuser@%                                                                                                                                            |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| CREATE USER 'newuser'@'%' IDENTIFIED WITH 'mysql_native_password' AS '*5806E04BBEE79E1899964C6A04D68BCA69B1A879' REQUIRE NONE PASSWORD EXPIRE DEFAULT ACCOUNT UNLOCK |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)

mysql> ALTER USER 'newuser' IDENTIFIED BY 'newnewpassword';
Query OK, 0 rows affected (0.02 sec)

mysql> SHOW CREATE USER 'newuser';
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| CREATE USER for newuser@%                                                                                                                                            |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| CREATE USER 'newuser'@'%' IDENTIFIED WITH 'mysql_native_password' AS '*FB8A1EA1353E8775CA836233E367FBDFCB37BE73' REQUIRE NONE PASSWORD EXPIRE DEFAULT ACCOUNT UNLOCK |
+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

```sql
ALTER USER 'newuser' ACCOUNT LOCK;
```

```
Query OK, 0 rows affected (0.02 sec)
```

> **ノート：**
>
> `ACCOUNT UNLOCK`を使用して[役割](/sql-statements/sql-statement-create-role.md)のロックを解除しないでください。それ以外の場合、ロック解除された役割を使用して、パスワードなしで TiDB にログインできます。

## MySQL の互換性 {#mysql-compatibility}

-   MySQL では、このステートメントは、パスワードの期限切れなどの属性を変更するために使用されます。この機能は、TiDB ではまだサポートされていません。

## こちらもご覧ください {#see-also}

<CustomContent platform="tidb">

-   [MySQL とのセキュリティの互換性](/security-compatibility-with-mysql.md)

</CustomContent>

-   [ユーザーを作成](/sql-statements/sql-statement-create-user.md)
-   [ユーザーをドロップ](/sql-statements/sql-statement-drop-user.md)
-   [ユーザーの作成を表示](/sql-statements/sql-statement-show-create-user.md)
