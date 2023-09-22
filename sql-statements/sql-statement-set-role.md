---
title: SET ROLE | TiDB SQL Statement Reference
summary: An overview of the usage of SET ROLE for the TiDB database.
---

# 役割を設定する {#set-role}

`SET ROLE`ステートメントは、現在のセッションでロールを有効にするために使用されます。ロールを有効にすると、ユーザーはロールの権限を使用できるようになります。

## あらすじ {#synopsis}

**SetRoleStmt:**

![SetRoleStmt](/media/sqlgram/SetRoleStmt.png)

**SetRoleOpt:**

![SetRoleOpt](/media/sqlgram/SetRoleOpt.png)

**SetDefaultRoleOpt:**

![SetDefaultRoleOpt](/media/sqlgram/SetDefaultRoleOpt.png)

## 例 {#examples}

ユーザー`'u1'@'%'`と 3 つのロール ( `'r1'@'%'` 、 `'r2'@'%'` 、および`'r3'@'%'`を作成します。これらのロールを`'u1'@'%'`に付与し、 `'r1'@'%'`デフォルトのロール`'u1'@'%'`として設定します。

```sql
CREATE USER 'u1'@'%';
CREATE ROLE 'r1', 'r2', 'r3';
GRANT 'r1', 'r2', 'r3' TO 'u1'@'%';
SET DEFAULT ROLE 'r1' TO 'u1'@'%';
```

`'u1'@'%'`としてログインし、次の`SET ROLE`ステートメントを実行してすべてのロールを有効にします。

```sql
SET ROLE ALL;
SELECT CURRENT_ROLE();
```

    +----------------------------+
    | CURRENT_ROLE()             |
    +----------------------------+
    | `r1`@`%`,`r2`@`%`,`r3`@`%` |
    +----------------------------+
    1 row in set (0.000 sec)

次の`SET ROLE`ステートメントを実行して、 `'r2'`と`'r3'`を有効にします。

```sql
SET ROLE 'r2', 'r3';
SELECT CURRENT_ROLE();
```

    +-------------------+
    | CURRENT_ROLE()    |
    +-------------------+
    | `r2`@`%`,`r3`@`%` |
    +-------------------+
    1 row in set (0.000 sec)

次の`SET ROLE`ステートメントを実行して、デフォルトのロールを有効にします。

```sql
SET ROLE DEFAULT;
SELECT CURRENT_ROLE();
```

    +----------------+
    | CURRENT_ROLE() |
    +----------------+
    | `r1`@`%`       |
    +----------------+
    1 row in set (0.000 sec)

次の`SET ROLE`ステートメントを実行して、有効なロールをすべてキャンセルします。

```sql
SET ROLE NONE;
SELECT CURRENT_ROLE();
```

    +----------------+
    | CURRENT_ROLE() |
    +----------------+
    |                |
    +----------------+
    1 row in set (0.000 sec)

## MySQLの互換性 {#mysql-compatibility}

TiDB の`SET ROLE`ステートメントは、MySQL 8.0 のロール機能と完全な互換性があります。互換性の違いが見つかった場合は、 [バグを報告](https://docs.pingcap.com/tidb/stable/support) .

## こちらも参照 {#see-also}

-   [ロールの作成](/sql-statements/sql-statement-create-role.md)
-   [役割を削除する](/sql-statements/sql-statement-drop-role.md)
-   [`GRANT &#x3C;role>`](/sql-statements/sql-statement-grant-role.md)
-   [`REVOKE &#x3C;role>`](/sql-statements/sql-statement-revoke-role.md)
-   [デフォルトの役割を設定](/sql-statements/sql-statement-set-default-role.md)

<CustomContent platform="tidb">

-   [役割ベースのアクセス制御](/role-based-access-control.md)

</CustomContent>
