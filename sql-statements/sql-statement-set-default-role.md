---
title: SET DEFAULT ROLE | TiDB SQL Statement Reference
summary: TiDB データベースの SET DEFAULT ROLE の使用法の概要。
---

# <code>SET DEFAULT ROLE</code> {#code-set-default-role-code}

このステートメントは、特定のロールをユーザーにデフォルトで適用するように設定します。これにより、 `SET ROLE <rolename>`または`SET ROLE ALL`実行しなくても、ロールに関連付けられた権限が自動的に付与されます。

## 概要 {#synopsis}

```ebnf+diagram
SetDefaultRoleStmt ::=
    "SET" "DEFAULT" "ROLE" ( "NONE" | "ALL" | Rolename ("," Rolename)* ) "TO" Username ("," Username)*
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
| GRANT Select ON test.* TO 'jennifer'@'%'    |
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

ステートメント`SET DEFAULT ROLE` 、ロール`analyticsteam`を`jennifer`に関連付けるために使用できます。

```sql
SET DEFAULT ROLE analyticsteam TO jennifer;
Query OK, 0 rows affected (0.02 sec)
```

`jennifer`ユーザーとして TiDB に接続します。

```shell
mysql -h 127.0.0.1 -P 4000 -u jennifer
```

この後、ユーザー`jennifer`ロール`analyticsteam`に関連付け`jennifer`た権限を持ち、ステートメント`SET ROLE`実行する必要がなくなります。

```sql
SHOW GRANTS;
+---------------------------------------------+
| Grants for User                             |
+---------------------------------------------+
| GRANT USAGE ON *.* TO 'jennifer'@'%'        |
| GRANT Select ON test.* TO 'jennifer'@'%'    |
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

`SET DEFAULT ROLE` 、ユーザーに関連付けられたロールを自動的に`GRANT`付与しません。 `jennifer`れていないロールに対して`SET DEFAULT ROLE`を付与しようとすると、次のエラーが発生します。

```sql
SET DEFAULT ROLE analyticsteam TO jennifer;
ERROR 3530 (HY000): `analyticsteam`@`%` is is not granted to jennifer@%
```

## MySQLの互換性 {#mysql-compatibility}

TiDBの`SET DEFAULT ROLE`文はMySQL 8.0のロール機能と完全に互換性があります。互換性に関する相違点が見つかった場合は、 [バグを報告する](https://docs.pingcap.com/tidb/stable/support)参照してください。

## 参照 {#see-also}

-   [`CREATE ROLE`](/sql-statements/sql-statement-create-role.md)
-   [`DROP ROLE`](/sql-statements/sql-statement-drop-role.md)
-   [`GRANT &#x3C;role>`](/sql-statements/sql-statement-grant-role.md)
-   [`REVOKE &#x3C;role>`](/sql-statements/sql-statement-revoke-role.md)
-   [`SET ROLE`](/sql-statements/sql-statement-set-role.md)

<CustomContent platform="tidb">

-   [ロールベースアクセス制御](/role-based-access-control.md)

</CustomContent>
