---
title: ALTER USER | TiDB SQL Statement Reference
summary: TiDB データベースの ALTER USER の使用法の概要。
---

# ユーザーの変更 {#alter-user}

このステートメントは、TiDB 権限システム内の既存のユーザーを変更します。MySQL 権限システムでは、ユーザーはユーザー名と接続元のホストの組み合わせです。したがって、IP アドレス`192.168.1.1`からのみ接続できるユーザー`'newuser2'@'192.168.1.1'`を作成できます。また、2 人のユーザーに同じユーザー部分を持たせ、異なるホストからログインするときに異なる権限を持たせることもできます。

## 概要 {#synopsis}

```ebnf+diagram
AlterUserStmt ::=
    'ALTER' 'USER' IfExists (UserSpecList RequireClauseOpt ConnectionOptions PasswordOption LockOption AttributeOption | 'USER' '(' ')' 'IDENTIFIED' 'BY' AuthString) ResourceGroupNameOption

UserSpecList ::=
    UserSpec ( ',' UserSpec )*

UserSpec ::=
    Username AuthOption

RequireClauseOpt ::=
    ( 'REQUIRE' 'NONE' | 'REQUIRE' 'SSL' | 'REQUIRE' 'X509' | 'REQUIRE' RequireList )?  
    
RequireList ::=
    ( "ISSUER" stringLit | "SUBJECT" stringLit | "CIPHER" stringLit | "SAN" stringLit | "TOKEN_ISSUER" stringLit )*

Username ::=
    StringName ('@' StringName | singleAtIdentifier)? | 'CURRENT_USER' OptionalBraces

AuthOption ::=
    ( 'IDENTIFIED' ( 'BY' ( AuthString | 'PASSWORD' HashString ) | 'WITH' StringName ( 'BY' AuthString | 'AS' HashString )? ) )?

PasswordOption ::= ( 'PASSWORD' 'EXPIRE' ( 'DEFAULT' | 'NEVER' | 'INTERVAL' N 'DAY' )? | 'PASSWORD' 'HISTORY' ( 'DEFAULT' | N ) | 'PASSWORD' 'REUSE' 'INTERVAL' ( 'DEFAULT' | N 'DAY' ) | 'FAILED_LOGIN_ATTEMPTS' N | 'PASSWORD_LOCK_TIME' ( N | 'UNBOUNDED' ) )*

LockOption ::= ( 'ACCOUNT' 'LOCK' | 'ACCOUNT' 'UNLOCK' )?

AttributeOption ::= ( 'COMMENT' CommentString | 'ATTRIBUTE' AttributeString )?

ResourceGroupNameOption::= ( 'RESOURCE' 'GROUP' Identifier)?

RequireClauseOpt ::= ('REQUIRE' ('NONE' | 'SSL' | 'X509' | RequireListElement ('AND'? RequireListElement)*))?

RequireListElement ::= 'ISSUER' Issuer | 'SUBJECT' Subject | 'CIPHER' Cipher | 'SAN' SAN | 'TOKEN_ISSUER' TokenIssuer
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
```

### 基本的なユーザー情報を変更する {#modify-basic-user-information}

ユーザー`newuser`のパスワードを変更します:

    mysql> ALTER USER 'newuser' IDENTIFIED BY 'newnewpassword';
    Query OK, 0 rows affected (0.02 sec)

    mysql> SHOW CREATE USER 'newuser';
    +----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | CREATE USER for newuser@%                                                                                                                                            |
    +----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | CREATE USER 'newuser'@'%' IDENTIFIED WITH 'mysql_native_password' AS '*FB8A1EA1353E8775CA836233E367FBDFCB37BE73' REQUIRE NONE PASSWORD EXPIRE DEFAULT ACCOUNT UNLOCK |
    +----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    1 row in set (0.00 sec)

ユーザー`newuser`ロックする:

```sql
ALTER USER 'newuser' ACCOUNT LOCK;
```

    Query OK, 0 rows affected (0.02 sec)

`newuser`の属性を変更します:

```sql
ALTER USER 'newuser' ATTRIBUTE '{"newAttr": "value", "deprecatedAttr": null}';
SELECT * FROM information_schema.user_attributes;
```

```sql
+-----------+------+--------------------------+
| USER      | HOST | ATTRIBUTE                |
+-----------+------+--------------------------+
| newuser   | %    | {"newAttr": "value"}     |
+-----------+------+--------------------------+
1 rows in set (0.00 sec)
```

`ALTER USER ... COMMENT`を使用して`newuser`のコメントを変更します。

```sql
ALTER USER 'newuser' COMMENT 'Here is the comment';
SELECT * FROM information_schema.user_attributes;
```

```sql
+-----------+------+--------------------------------------------------------+
| USER      | HOST | ATTRIBUTE                                              |
+-----------+------+--------------------------------------------------------+
| newuser   | %    | {"comment": "Here is the comment", "newAttr": "value"} |
+-----------+------+--------------------------------------------------------+
1 rows in set (0.00 sec)
```

`ALTER USER ... ATTRIBUTE`を使用して`newuser`のコメントを削除します。

```sql
ALTER USER 'newuser' ATTRIBUTE '{"comment": null}';
SELECT * FROM information_schema.user_attributes;
```

```sql
+-----------+------+---------------------------+
| USER      | HOST | ATTRIBUTE                 |
+-----------+------+---------------------------+
| newuser   | %    | {"newAttr": "value"}      |
+-----------+------+---------------------------+
1 rows in set (0.00 sec)
```

`ALTER USER ... PASSWORD EXPIRE NEVER`を実行して、 `newuser`の自動パスワード有効期限ポリシーを無期限に変更します。

```sql
ALTER USER 'newuser' PASSWORD EXPIRE NEVER;
```

    Query OK, 0 rows affected (0.02 sec)

`ALTER USER ... PASSWORD REUSE INTERVAL ... DAY`を使用して、 `newuser`のパスワード再利用ポリシーを変更し、過去 90 日以内に使用されたパスワードの再利用を禁止します。

```sql
ALTER USER 'newuser' PASSWORD REUSE INTERVAL 90 DAY;
```

    Query OK, 0 rows affected (0.02 sec)

### ユーザーにバインドされているリソース グループを変更する {#modify-the-resource-group-bound-to-the-user}

`ALTER USER ... RESOURCE GROUP`使用して、ユーザー`newuser` ～ `rg1`のリソース グループを変更します。

```sql
ALTER USER 'newuser' RESOURCE GROUP rg1;
```

    Query OK, 0 rows affected (0.02 sec)

現在のユーザーにバインドされているリソース グループをビュー。

```sql
SELECT USER, JSON_EXTRACT(User_attributes, "$.resource_group") FROM mysql.user WHERE user = "newuser";
```

    +---------+---------------------------------------------------+
    | USER    | JSON_EXTRACT(User_attributes, "$.resource_group") |
    +---------+---------------------------------------------------+
    | newuser | "rg1"                                             |
    +---------+---------------------------------------------------+
    1 row in set (0.02 sec)

ユーザーをリソース グループからバインド解除します。つまり、ユーザーを`default`リソース グループにバインドします。

```sql
ALTER USER 'newuser' RESOURCE GROUP `default`;
SELECT USER, JSON_EXTRACT(User_attributes, "$.resource_group") FROM mysql.user WHERE user = "newuser";
```

    +---------+---------------------------------------------------+
    | USER    | JSON_EXTRACT(User_attributes, "$.resource_group") |
    +---------+---------------------------------------------------+
    | newuser | "default"                                         |
    +---------+---------------------------------------------------+
    1 row in set (0.02 sec)

## 参照 {#see-also}

<CustomContent platform="tidb">

-   [MySQL とのSecurity互換性](/security-compatibility-with-mysql.md)

</CustomContent>

-   [ユーザーを作成](/sql-statements/sql-statement-create-user.md)
-   [ユーザーを削除](/sql-statements/sql-statement-drop-user.md)
-   [ユーザーの作成を表示](/sql-statements/sql-statement-show-create-user.md)
