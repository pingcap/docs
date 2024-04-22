---
title: SET DEFAULT ROLE | TiDB SQL Statement Reference
summary: このステートメントは、デフォルトでユーザーに適用される特定のロールを設定します。したがって、 `SET ROLE <rolename>`または`SET ROLE ALL`を実行しなくても、ロールに関連付けられた権限が自動的に付与されます。MySQLの互換性があります。
---

# <code>SET DEFAULT ROLE</code> {#code-set-default-role-code}

このステートメントは、デフォルトでユーザーに適用される特定のロールを設定します。したがって、 `SET ROLE <rolename>`または`SET ROLE ALL`を実行しなくても、ロールに関連付けられた権限が自動的に付与されます。

## あらすじ {#synopsis}

**SetDefaultRoleStmt:**

![SetDefaultRoleStmt](/media/sqlgram/SetDefaultRoleStmt.png)

**SetDefaultRoleOpt:**

![SetDefaultRoleOpt](/media/sqlgram/SetDefaultRoleOpt.png)

**役割名リスト:**

![RolenameList](/media/sqlgram/RolenameList.png)

**ユーザー名リスト:**

![UsernameList](/media/sqlgram/UsernameList.png)

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

`SET DEFAULT ROLE`関連付けられたロール`GRANT`ユーザーに自動的に割り当てません。 `jennifer`が付与していないロールに対して`SET DEFAULT ROLE`を実行しようとすると、次のエラーが発生します。

```sql
SET DEFAULT ROLE analyticsteam TO jennifer;
ERROR 3530 (HY000): `analyticsteam`@`%` is is not granted to jennifer@%
```

## MySQLの互換性 {#mysql-compatibility}

TiDB の`SET DEFAULT ROLE`ステートメントは、MySQL 8.0 のロール機能と完全な互換性があります。互換性の違いが見つかった場合は、 [バグを報告](https://docs.pingcap.com/tidb/stable/support) .

## こちらも参照 {#see-also}

-   [`CREATE ROLE`](/sql-statements/sql-statement-create-role.md)
-   [`DROP ROLE`](/sql-statements/sql-statement-drop-role.md)
-   [`GRANT &#x3C;role>`](/sql-statements/sql-statement-grant-role.md)
-   [`REVOKE &#x3C;role>`](/sql-statements/sql-statement-revoke-role.md)
-   [`SET ROLE`](/sql-statements/sql-statement-set-role.md)

<CustomContent platform="tidb">

-   [役割ベースのアクセス制御](/role-based-access-control.md)

</CustomContent>
