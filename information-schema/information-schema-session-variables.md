---
title: SESSION_VARIABLES
summary: SESSION_VARIABLES` INFORMATION_SCHEMA テーブルについて学習します。
---

# セッション変数 {#session-variables}

`SESSION_VARIABLES`番目の表はセッション変数に関する情報を提供します。表のデータは[`SHOW SESSION VARIABLES`](/sql-statements/sql-statement-show-variables.md)のステートメントの結果と似ています。

```sql
USE INFORMATION_SCHEMA;
DESC SESSION_VARIABLES;
```

出力は次のようになります。

```sql
+----------------+---------------+------+------+---------+-------+
| Field          | Type          | Null | Key  | Default | Extra |
+----------------+---------------+------+------+---------+-------+
| VARIABLE_NAME  | varchar(64)   | YES  |      | NULL    |       |
| VARIABLE_VALUE | varchar(1024) | YES  |      | NULL    |       |
+----------------+---------------+------+------+---------+-------+
2 rows in set (0.00 sec)
```

`SESSION_VARIABLES`テーブルの最初の 10 行をクエリします。

```sql
SELECT * FROM SESSION_VARIABLES ORDER BY variable_name LIMIT 10;
```

出力は次のようになります。

```sql
+-----------------------------------+------------------+
| VARIABLE_NAME                     | VARIABLE_VALUE   |
+-----------------------------------+------------------+
| allow_auto_random_explicit_insert | OFF              |
| auto_increment_increment          | 1                |
| auto_increment_offset             | 1                |
| autocommit                        | ON               |
| automatic_sp_privileges           | 1                |
| avoid_temporal_upgrade            | OFF              |
| back_log                          | 80               |
| basedir                           | /usr/local/mysql |
| big_tables                        | OFF              |
| bind_address                      | *                |
+-----------------------------------+------------------+
10 rows in set (0.00 sec)
```

`SESSION_VARIABLES`表の列の説明は次のとおりです。

-   `VARIABLE_NAME` : データベース内のセッション レベル変数の名前。
-   `VARIABLE_VALUE` : データベース内のセッション レベルの変数の値。
