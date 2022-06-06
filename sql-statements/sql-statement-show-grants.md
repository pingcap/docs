---
title: SHOW GRANTS | TiDB SQL Statement Reference
summary: An overview of the usage of SHOW GRANTS for the TiDB database.
---

# 助成金を表示 {#show-grants}

このステートメントは、ユーザーに関連付けられている特権のリストを示しています。 MySQLと同様に、 `USAGE`特権はTiDBにログインする機能を示します。

## あらすじ {#synopsis}

**ShowGrantsStmt：**

![ShowGrantsStmt](/media/sqlgram/ShowGrantsStmt.png)

**ユーザー名：**

![Username](/media/sqlgram/Username.png)

**UsingRoles：**

![UsingRoles](/media/sqlgram/UsingRoles.png)

**RolenameList：**

![RolenameList](/media/sqlgram/RolenameList.png)

**役割名：**

![Rolename](/media/sqlgram/Rolename.png)

## 例 {#examples}

```sql
mysql> SHOW GRANTS;
+-------------------------------------------+
| Grants for User                           |
+-------------------------------------------+
| GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' |
+-------------------------------------------+
1 row in set (0.00 sec)

mysql> SHOW GRANTS FOR 'u1';
ERROR 1141 (42000): There is no such grant defined for user 'u1' on host '%'
mysql> CREATE USER u1;
Query OK, 1 row affected (0.04 sec)

mysql> GRANT SELECT ON test.* TO u1;
Query OK, 0 rows affected (0.04 sec)

mysql> SHOW GRANTS FOR u1;
+------------------------------------+
| Grants for u1@%                    |
+------------------------------------+
| GRANT USAGE ON *.* TO 'u1'@'%'     |
| GRANT Select ON test.* TO 'u1'@'%' |
+------------------------------------+
2 rows in set (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQLと完全に互換性があると理解されています。互換性の違いは、GitHubでは[問題を介して報告](https://github.com/pingcap/tidb/issues/new/choose)である必要があります。

## も参照してください {#see-also}

-   [CREATEUSERを表示する](/sql-statements/sql-statement-show-create-user.md)
-   [許す](/sql-statements/sql-statement-grant-privileges.md)
