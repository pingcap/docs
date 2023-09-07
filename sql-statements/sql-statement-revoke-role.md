---
title: REVOKE <role> | TiDB SQL Statement Reference
summary: An overview of the usage of REVOKE <role> for the TiDB database.
---

# <code>REVOKE &#x3C;role></code> {#code-revoke-x3c-role-code}

このステートメントは、指定されたユーザー (またはユーザーのリスト) から以前に割り当てられたロールを削除します。

## あらすじ {#synopsis}

```ebnf+diagram
RevokeRoleStmt ::=
    'REVOKE' RolenameList 'FROM' UsernameList

RolenameList ::=
    Rolename ( ',' Rolename )*

UsernameList ::=
    Username ( ',' Username )*
```

## 例 {#examples}

`root`ユーザーとして TiDB に接続します。

```shell
mysql -h 127.0.0.1 -P 4000 -u root
```

新しいロール`analyticsteam`と新しいユーザー`jennifer`を作成します。

```sql
CREATE ROLE analyticsteam;
Query OK, 0 rows affected (0.02 sec)

GRANT SELECT ON test.* TO analyticsteam;
Query OK, 0 rows affected (0.02 sec)

CREATE USER jennifer;
Query OK, 0 rows affected (0.01 sec)

GRANT analyticsteam TO jennifer;
Query OK, 0 rows affected (0.01 sec)
```

`jennifer`ユーザーとして TiDB に接続します。

```shell
mysql -h 127.0.0.1 -P 4000 -u jennifer
```

デフォルトでは、 `analyticsteam`ロールに関連付けられた権限を使用できるようにするには、 `jennifer` `SET ROLE analyticsteam`実行する必要があることに注意してください。

```sql
SHOW GRANTS;
+---------------------------------------------+
| Grants for User                             |
+---------------------------------------------+
| GRANT USAGE ON *.* TO 'jennifer'@'%'        |
| GRANT 'analyticsteam'@'%' TO 'jennifer'@'%' |
+---------------------------------------------+
2 rows in set (0.00 sec)

SHOW TABLES in test;
ERROR 1044 (42000): Access denied for user 'jennifer'@'%' to database 'test'
SET ROLE analyticsteam;
Query OK, 0 rows affected (0.00 sec)

SHOW GRANTS;
+---------------------------------------------+
| Grants for User                             |
+---------------------------------------------+
| GRANT USAGE ON *.* TO 'jennifer'@'%'        |
| GRANT SELECT ON test.* TO 'jennifer'@'%'    |
| GRANT 'analyticsteam'@'%' TO 'jennifer'@'%' |
+---------------------------------------------+
3 rows in set (0.00 sec)

SHOW TABLES IN test;
+----------------+
| Tables_in_test |
+----------------+
| t1             |
+----------------+
1 row in set (0.00 sec)
```

`root`ユーザーとして TiDB に接続します。

```shell
mysql -h 127.0.0.1 -P 4000 -u root
```

ステートメント`SET DEFAULT ROLE`使用して、ロール`analyticsteam`を`jennifer`に関連付けることができます。

```sql
SET DEFAULT ROLE analyticsteam TO jennifer;
Query OK, 0 rows affected (0.02 sec)
```

`jennifer`ユーザーとして TiDB に接続します。

```shell
mysql -h 127.0.0.1 -P 4000 -u jennifer
```

この後、ユーザー`jennifer`はロール`analyticsteam`に関連付けられた権限を持ち、ユーザー`jennifer`はステートメント`SET ROLE`を実行する必要がなくなります。

```sql
SHOW GRANTS;
+---------------------------------------------+
| Grants for User                             |
+---------------------------------------------+
| GRANT USAGE ON *.* TO 'jennifer'@'%'        |
| GRANT SELECT ON test.* TO 'jennifer'@'%'    |
| GRANT 'analyticsteam'@'%' TO 'jennifer'@'%' |
+---------------------------------------------+
3 rows in set (0.00 sec)

SHOW TABLES IN test;
+----------------+
| Tables_in_test |
+----------------+
| t1             |
+----------------+
1 row in set (0.00 sec)
```

`root`ユーザーとして TiDB に接続します。

```shell
mysql -h 127.0.0.1 -P 4000 -u root
```

Analyticsteam の役割を`jennifer`から取り消します。

```sql
REVOKE analyticsteam FROM jennifer;
Query OK, 0 rows affected (0.01 sec)
```

`jennifer`ユーザーとして TiDB に接続します。

```shell
mysql -h 127.0.0.1 -P 4000 -u jennifer
```

`jennifer`の権限を表示します。

```sql
SHOW GRANTS;
+--------------------------------------+
| Grants for User                      |
+--------------------------------------+
| GRANT USAGE ON *.* TO 'jennifer'@'%' |
+--------------------------------------+
1 row in set (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

TiDB の`REVOKE <role>`ステートメントは、MySQL 8.0 のロール機能と完全な互換性があります。互換性の違いが見つかった場合は、 [バグを報告](https://docs.pingcap.com/tidb/stable/support) .

## こちらも参照 {#see-also}

-   [`CREATE ROLE`](/sql-statements/sql-statement-create-role.md)
-   [`DROP ROLE`](/sql-statements/sql-statement-drop-role.md)
-   [`GRANT &#x3C;role>`](/sql-statements/sql-statement-grant-role.md)
-   [`SET ROLE`](/sql-statements/sql-statement-set-role.md)
-   [`SET DEFAULT ROLE`](/sql-statements/sql-statement-set-default-role.md)

<CustomContent platform="tidb">
  -   [役割ベースのアクセス制御](/role-based-access-control.md)
</CustomContent>
