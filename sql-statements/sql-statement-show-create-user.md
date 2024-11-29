---
title: SHOW CREATE USER | TiDB SQL Statement Reference
summary: TiDB データベースに対する SHOW CREATE USER の使用法の概要。
---

# 表示 ユーザーの作成 {#show-create-user}

このステートメントは、 `CREATE USER`構文を使用してユーザーを再作成する方法を示しています。

## 概要 {#synopsis}

```ebnf+diagram
ShowCreateUserStmt ::=
    "SHOW" "CREATE" "USER" (Username ("@" Hostname)? | "CURRENT_USER" ( "(" ")" )? )
```

## 例 {#examples}

```sql
mysql> SHOW CREATE USER 'root';
+--------------------------------------------------------------------------------------------------------------------------+
| CREATE USER for root@%                                                                                                   |
+--------------------------------------------------------------------------------------------------------------------------+
| CREATE USER 'root'@'%' IDENTIFIED WITH 'mysql_native_password' AS '' REQUIRE NONE PASSWORD EXPIRE DEFAULT ACCOUNT UNLOCK |
+--------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)

mysql> SHOW GRANTS FOR 'root';
+-------------------------------------------+
| Grants for root@%                         |
+-------------------------------------------+
| GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' |
+-------------------------------------------+
1 row in set (0.00 sec)
```

## MySQL 互換性 {#mysql-compatibility}

<CustomContent platform="tidb">

-   `SHOW CREATE USER`の出力は MySQL と一致するように設計されていますが、 `CREATE`のオプションのいくつかはまだ TiDB でサポートされていません。まだサポートされていないオプションは解析されますが無視されます。詳細については[Securityの互換性](/security-compatibility-with-mysql.md)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   `SHOW CREATE USER`の出力は MySQL と一致するように設計されていますが、 `CREATE`のオプションのいくつかはまだ TiDB でサポートされていません。まだサポートされていないオプションは解析されますが無視されます。詳細については[Securityの互換性](https://docs.pingcap.com/tidb/stable/security-compatibility-with-mysql/)参照してください。

</CustomContent>

## 参照 {#see-also}

-   [ユーザーを作成](/sql-statements/sql-statement-create-user.md)
-   [ショーグラント](/sql-statements/sql-statement-show-grants.md)
-   [ユーザーを削除](/sql-statements/sql-statement-drop-user.md)
