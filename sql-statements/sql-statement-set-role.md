---
title: SET ROLE | TiDB SQL Statement Reference
summary: An overview of the usage of SET ROLE for the TiDB database.
---

# 役割を設定する {#set-role}

`SET ROLE`ステートメントは、現在のセッションでロールを有効にするために使用されます。ロールを有効にした後、ユーザーはロールの権限を使用できます。

## あらすじ {#synopsis}

**SetRoleStmt：**

![SetRoleStmt](/media/sqlgram/SetRoleStmt.png)

**SetRoleOpt：**

![SetRoleOpt](/media/sqlgram/SetRoleOpt.png)

**SetDefaultRoleOpt：**

![SetDefaultRoleOpt](/media/sqlgram/SetDefaultRoleOpt.png)

## 例 {#examples}

ユーザー`'u1'@'%'`と3 `'r3'@'%'`の役割を作成し`'r2'@'%'` ： `'r1'@'%'` 。これらの役割を`'u1'@'%'`に付与し、 `'r1'@'%'`をデフォルトの役割`'u1'@'%'`として設定します。

{{< copyable "" >}}

```sql
CREATE USER 'u1'@'%';
CREATE ROLE 'r1', 'r2', 'r3';
GRANT 'r1', 'r2', 'r3' TO 'u1'@'%';
SET DEFAULT ROLE 'r1' TO 'u1'@'%';
```

`'u1'@'%'`としてログインし、次の`SET ROLE`のステートメントを実行して、すべての役割を有効にします。

{{< copyable "" >}}

```sql
SET ROLE ALL;
SELECT CURRENT_ROLE();
```

```
+----------------------------+
| CURRENT_ROLE()             |
+----------------------------+
| `r1`@`%`,`r2`@`%`,`r3`@`%` |
+----------------------------+
1 row in set (0.000 sec)
```

次の`SET ROLE`のステートメントを実行して、 `'r2'`と`'r3'`を有効にします。

{{< copyable "" >}}

```sql
SET ROLE 'r2', 'r3';
SELECT CURRENT_ROLE();
```

```
+-------------------+
| CURRENT_ROLE()    |
+-------------------+
| `r2`@`%`,`r3`@`%` |
+-------------------+
1 row in set (0.000 sec)
```

次の`SET ROLE`のステートメントを実行して、デフォルトの役割を有効にします。

{{< copyable "" >}}

```sql
SET ROLE DEFAULT;
SELECT CURRENT_ROLE();
```

```
+----------------+
| CURRENT_ROLE() |
+----------------+
| `r1`@`%`       |
+----------------+
1 row in set (0.000 sec)
```

次の`SET ROLE`のステートメントを実行して、有効なすべてのロールをキャンセルします。

{{< copyable "" >}}

```sql
SET ROLE NONE;
SELECT CURRENT_ROLE();
```

```
+----------------+
| CURRENT_ROLE() |
+----------------+
|                |
+----------------+
1 row in set (0.000 sec)
```

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL8.0の機能であるロールと完全に互換性があると理解されています。互換性の違いは、GitHubでは[問題を介して報告](https://github.com/pingcap/tidb/issues/new/choose)である必要があります。

## も参照してください {#see-also}

-   [役割の作成](/sql-statements/sql-statement-create-role.md)
-   [ドロップロール](/sql-statements/sql-statement-drop-role.md)
-   [`GRANT &#x3C;role>`](/sql-statements/sql-statement-grant-role.md)
-   [`REVOKE &#x3C;role>`](/sql-statements/sql-statement-revoke-role.md)
-   [デフォルトの役割を設定](/sql-statements/sql-statement-set-default-role.md)
-   [ロールベースのアクセス制御](/role-based-access-control.md)
