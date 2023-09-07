---
title: GRANT <role> | TiDB SQL Statement Reference
summary: An overview of the usage of GRANT <role> for the TiDB database.
---

# <code>GRANT &#x3C;role></code> {#code-grant-x3c-role-code}

以前に作成したロールを既存のユーザーに割り当てます。ユーザーは、ステートメント`SET ROLE <rolename>`を使用してロールの権限を引き受けるか、ステートメント`SET ROLE ALL`を使用して、割り当てられているすべてのロールを引き受けることができます。

## あらすじ {#synopsis}

```ebnf+diagram
GrantRoleStmt ::=
    'GRANT' RolenameList 'TO' UsernameList

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

この後、ユーザー`jennifer`はロール`analyticsteam`に関連付けられた権限を持ち、ユーザー`jennifer`ステートメント`SET ROLE`を実行する必要がなくなります。

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

## MySQLの互換性 {#mysql-compatibility}

TiDB の`GRANT <role>`ステートメントは、MySQL 8.0 のロール機能と完全な互換性があります。互換性の違いが見つかった場合は、 [バグを報告](https://docs.pingcap.com/tidb/stable/support) .

## こちらも参照 {#see-also}

-   [`GRANT &#x3C;privileges>`](/sql-statements/sql-statement-grant-privileges.md)
-   [`CREATE ROLE`](/sql-statements/sql-statement-create-role.md)
-   [`DROP ROLE`](/sql-statements/sql-statement-drop-role.md)
-   [`REVOKE &#x3C;role>`](/sql-statements/sql-statement-revoke-role.md)
-   [`SET ROLE`](/sql-statements/sql-statement-set-role.md)
-   [`SET DEFAULT ROLE`](/sql-statements/sql-statement-set-default-role.md)

<CustomContent platform="tidb">
  -   [役割ベースのアクセス制御](/role-based-access-control.md)
</CustomContent>
