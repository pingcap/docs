---
title: SHOW [FULL] COLUMNS FROM | TiDB SQL Statement Reference
summary: TiDB データベースの SHOW [FULL] COLUMNS FROM の使用法の概要。
---

# [全列表示] から {#show-full-columns-from}

ステートメント`SHOW [FULL] COLUMNS FROM <table_name>` 、テーブルまたはビューの列を便利な表形式で記述します。オプションのキーワード`FULL` 、現在のユーザーがその列に対して持っている権限と、テーブル定義の`comment`表示します。

ステートメント`SHOW [FULL] FIELDS FROM <table_name>` 、 `DESC <table_name>` 、 `DESCRIBE <table_name>` 、および`EXPLAIN <table_name>`はこのステートメントのエイリアスです。

> **注記：**
>
> `DESC TABLE <table_name>` 、 `DESCRIBE TABLE <table_name>` 、 `EXPLAIN TABLE <table_name>`上記の文と同等ではありません。これらは[`DESC SELECT * FROM &#x3C;table_name>`](/sql-statements/sql-statement-explain.md)の別名です。

## 概要 {#synopsis}

```ebnf+diagram
ShowColumnsFromStmt ::=
    "SHOW" "FULL"? ("COLUMNS" | "FIELDS") ("FROM" | "IN") TableName ( ("FROM" | "IN") SchemaName)? ShowLikeOrWhere?

TableName ::=
    (Identifier ".")? Identifier

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## 例 {#examples}

```sql
mysql> CREATE VIEW v1 AS SELECT 1;
Query OK, 0 rows affected (0.11 sec)

mysql> SHOW COLUMNS FROM v1;
+-------+--------+------+------+---------+-------+
| Field | Type   | Null | Key  | Default | Extra |
+-------+--------+------+------+---------+-------+
| 1     | bigint | YES  |      | NULL    |       |
+-------+--------+------+------+---------+-------+
1 row in set (0.00 sec)

mysql> DESC v1;
+-------+--------+------+------+---------+-------+
| Field | Type   | Null | Key  | Default | Extra |
+-------+--------+------+------+---------+-------+
| 1     | bigint | YES  |      | NULL    |       |
+-------+--------+------+------+---------+-------+
1 row in set (0.00 sec)

mysql> DESCRIBE v1;
+-------+--------+------+------+---------+-------+
| Field | Type   | Null | Key  | Default | Extra |
+-------+--------+------+------+---------+-------+
| 1     | bigint | YES  |      | NULL    |       |
+-------+-----------+------+------+---------+-------+
1 row in set (0.00 sec)

mysql> EXPLAIN v1;
+-------+--------+------+------+---------+-------+
| Field | Type   | Null | Key  | Default | Extra |
+-------+--------+------+------+---------+-------+
| 1     | bigint | YES  |      | NULL    |       |
+-------+--------+------+------+---------+-------+
1 row in set (0.00 sec)

mysql> SHOW FIELDS FROM v1;
+-------+--------+------+------+---------+-------+
| Field | Type   | Null | Key  | Default | Extra |
+-------+--------+------+------+---------+-------+
| 1     | bigint | YES  |      | NULL    |       |
+-------+--------+------+------+---------+-------+
1 row in set (0.00 sec)

mysql> SHOW FULL COLUMNS FROM v1;
+-------+--------+-----------+------+------+---------+-------+---------------------------------+---------+
| Field | Type   | Collation | Null | Key  | Default | Extra | Privileges                      | Comment |
+-------+--------+-----------+------+------+---------+-------+---------------------------------+---------+
| 1     | bigint | NULL      | YES  |      | NULL    |       | select,insert,update,references |         |
+-------+--------+-----------+------+------+---------+-------+---------------------------------+---------+
1 row in set (0.00 sec)

mysql> SHOW FULL COLUMNS FROM mysql.user;
+------------------------+---------------+-------------+------+------+---------+-------+---------------------------------+---------+
| Field                  | Type          | Collation   | Null | Key  | Default | Extra | Privileges                      | Comment |
+------------------------+---------------+-------------+------+------+---------+-------+---------------------------------+---------+
| Host                   | char(255)     | utf8mb4_bin | NO   | PRI  | NULL    |       | select,insert,update,references |         |
| User                   | char(32)      | utf8mb4_bin | NO   | PRI  | NULL    |       | select,insert,update,references |         |
| authentication_string  | text          | utf8mb4_bin | YES  |      | NULL    |       | select,insert,update,references |         |
| plugin                 | char(64)      | utf8mb4_bin | YES  |      | NULL    |       | select,insert,update,references |         |
| Select_priv            | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Insert_priv            | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Update_priv            | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Delete_priv            | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Create_priv            | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Drop_priv              | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Process_priv           | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Grant_priv             | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| References_priv        | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Alter_priv             | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Show_db_priv           | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Super_priv             | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Create_tmp_table_priv  | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Lock_tables_priv       | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Execute_priv           | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Create_view_priv       | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Show_view_priv         | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Create_routine_priv    | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Alter_routine_priv     | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Index_priv             | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Create_user_priv       | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Event_priv             | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Repl_slave_priv        | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Repl_client_priv       | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Trigger_priv           | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Create_role_priv       | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Drop_role_priv         | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Account_locked         | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Shutdown_priv          | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Reload_priv            | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| FILE_priv              | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Config_priv            | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Create_Tablespace_Priv | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| User_attributes        | json          | NULL        | YES  |      | NULL    |       | select,insert,update,references |         |
+------------------------+---------------+-------------+------+------+---------+-------+---------------------------------+---------+
38 rows in set (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

TiDBの`SHOW [FULL] COLUMNS FROM`文はMySQLと完全に互換性があります。互換性に違いがある場合は、 [バグを報告する](https://docs.pingcap.com/tidb/stable/support)参照してください。

## 参照 {#see-also}

-   [表示テーブルの作成](/sql-statements/sql-statement-show-create-table.md)
