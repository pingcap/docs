---
title: SESSION_VARIABLES
summary: Learn the `SESSION_VARIABLES` information_schema table.
---

# SESSION_VARIABLES {#session-variables}

`SESSION_VARIABLES`の表は、セッション変数に関する情報を提供します。テーブルデータは、 `SHOW SESSION VARIABLES`ステートメントの結果と同様です。

{{< copyable "" >}}

```sql
USE information_schema;
DESC session_variables;
```

```sql
+----------------+---------------+------+------+---------+-------+
| Field          | Type          | Null | Key  | Default | Extra |
+----------------+---------------+------+------+---------+-------+
| VARIABLE_NAME  | varchar(64)   | YES  |      | NULL    |       |
| VARIABLE_VALUE | varchar(1024) | YES  |      | NULL    |       |
+----------------+---------------+------+------+---------+-------+
2 rows in set (0.00 sec)
```

{{< copyable "" >}}

```sql
SELECT * FROM session_variables ORDER BY variable_name LIMIT 10;
```

```sql
+-----------------------------------+------------------+
| VARIABLE_NAME                     | VARIABLE_VALUE   |
+-----------------------------------+------------------+
| allow_auto_random_explicit_insert | off              |
| auto_increment_increment          | 1                |
| auto_increment_offset             | 1                |
| autocommit                        | 1                |
| automatic_sp_privileges           | 1                |
| avoid_temporal_upgrade            | 0                |
| back_log                          | 80               |
| basedir                           | /usr/local/mysql |
| big_tables                        | 0                |
| bind_address                      | *                |
+-----------------------------------+------------------+
10 rows in set (0.00 sec)
```

`SESSION_VARIABLES`テーブルの列の説明は次のとおりです。

-   `VARIABLE_NAME` ：データベース内のセッションレベル変数の名前。
-   `VARIABLE_VALUE` ：データベース内のセッションレベル変数の値。
