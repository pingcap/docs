---
title: SET ROLE | TiDB SQL Statement Reference
summary: TiDB データベースの SET ROLE の使用法の概要。
---

# 役割を設定 {#set-role}

`SET ROLE`ステートメントは、現在のセッションでロールを有効にするために使用されます。ロールを有効にすると、ユーザーはロールの権限を使用できるようになります。

## 概要 {#synopsis}

```ebnf+diagram
SetRoleStmt ::=
    "SET" "ROLE" ( "DEFAULT" | "ALL" ( "EXCEPT" Rolename ("," Rolename)* )? | "NONE" | Rolename ("," Rolename)* )?
```

## 例 {#examples}

ユーザー`'u1'@'%'`と`'r1'@'%'` 、 `'r2'@'%'` 、 `'r3'@'%'` 3 つのロールを作成します。これらのロールを`'u1'@'%'`に付与し、 `'r1'@'%'` `'u1'@'%'`のデフォルト ロールとして設定します。

```sql
CREATE USER 'u1'@'%';
CREATE ROLE 'r1', 'r2', 'r3';
GRANT 'r1', 'r2', 'r3' TO 'u1'@'%';
SET DEFAULT ROLE 'r1' TO 'u1'@'%';
```

`'u1'@'%'`としてログインし、次の`SET ROLE`のステートメントを実行してすべてのロールを有効にします。

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

`'r2'`と`'r3'`を有効にするには、次の`SET ROLE`ステートメントを実行します。

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

デフォルトのロールを有効にするには、次の`SET ROLE`ステートメントを実行します。

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

有効なロールをすべてキャンセルするには、次の`SET ROLE`ステートメントを実行します。

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

## MySQL 互換性 {#mysql-compatibility}

TiDB の`SET ROLE`ステートメントは、MySQL 8.0 のロール機能と完全に互換性があります。互換性の違いが見つかった場合は、 [バグを報告](https://docs.pingcap.com/tidb/stable/support) 。

## 参照 {#see-also}

-   [ロールの作成](/sql-statements/sql-statement-create-role.md)
-   [役割をドロップ](/sql-statements/sql-statement-drop-role.md)
-   [`GRANT &#x3C;role>`](/sql-statements/sql-statement-grant-role.md)
-   [`REVOKE &#x3C;role>`](/sql-statements/sql-statement-revoke-role.md)
-   [デフォルトロールの設定](/sql-statements/sql-statement-set-default-role.md)

<CustomContent platform="tidb">

-   [ロールベースのアクセス制御](/role-based-access-control.md)

</CustomContent>
