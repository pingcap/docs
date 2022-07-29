---
title: SHOW CREATE USER | TiDB SQL Statement Reference
summary: An overview of the usage of SHOW CREATE USER for the TiDB database.
---

# CREATEUSERを表示する {#show-create-user}

このステートメントは、 `CREATE USER`構文を使用してユーザーを再作成する方法を示しています。

## あらすじ {#synopsis}

**ShowCreateUserStmt：**

![ShowCreateUserStmt](/media/sqlgram/ShowCreateUserStmt.png)

**ユーザー名：**

![Username](/media/sqlgram/Username.png)

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

## MySQLの互換性 {#mysql-compatibility}

-   `SHOW CREATE USER`の出力はMySQLと一致するように設計されていますが、 `CREATE`のオプションのいくつかはまだTiDBでサポートされていません。まだサポートされていないオプションは解析されますが、無視されます。詳しくは【セキュリティ互換性】をご覧ください。

## も参照してください {#see-also}

-   [ユーザーを作成](/sql-statements/sql-statement-create-user.md)
-   [助成金を表示](/sql-statements/sql-statement-show-grants.md)
-   [ドロップユーザー](/sql-statements/sql-statement-drop-user.md)
