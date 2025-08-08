---
title: SET ROLE | TiDB SQL Statement Reference
summary: TiDB データベースの SET ROLE の使用法の概要。
---

# 役割を設定する {#set-role}

`SET ROLE`文は、現在のセッションでロールを有効にするために使用されます。ロールを有効にすると、ユーザーはロールの権限を使用できるようになります。

## 概要 {#synopsis}

```ebnf+diagram
SetRoleStmt ::=
    "SET" "ROLE" ( "DEFAULT" | "ALL" ( "EXCEPT" Rolename ("," Rolename)* )? | "NONE" | Rolename ("," Rolename)* )?
```

## 例 {#examples}

ユーザー`'u1'@'%'`と3つのロール（ `'r1'@'%'` 、 `'r2'@'%'` 、 `'r3'@'%'`を作成します。これらのロールを`'u1'@'%'`に付与し、 `'r1'@'%'` `'u1'@'%'`のデフォルトロールとして設定します。

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

`'r2'`と`'r3'`有効にするには、次の`SET ROLE`ステートメントを実行します。

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

## MySQLの互換性 {#mysql-compatibility}

TiDBの`SET ROLE`文はMySQL 8.0のロール機能と完全に互換性があります。互換性に関する相違点が見つかった場合は、 [バグを報告する](https://docs.pingcap.com/tidb/stable/support)参照してください。

## 参照 {#see-also}

-   [ロールを作成](/sql-statements/sql-statement-create-role.md)
-   [役割を放棄する](/sql-statements/sql-statement-drop-role.md)
-   [`GRANT &#x3C;role>`](/sql-statements/sql-statement-grant-role.md)
-   [`REVOKE &#x3C;role>`](/sql-statements/sql-statement-revoke-role.md)
-   [デフォルトロールの設定](/sql-statements/sql-statement-set-default-role.md)

<CustomContent platform="tidb">

-   [ロールベースアクセス制御](/role-based-access-control.md)

</CustomContent>
