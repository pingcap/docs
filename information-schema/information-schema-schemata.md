---
title: SCHEMATA
summary: Learn the `SCHEMATA` information_schema table.
---

# スキーマ {#schemata}

`SCHEMATA`の表は、データベースに関する情報を提供します。テーブルデータは、 `SHOW DATABASES`ステートメントの結果と同等です。

{{< copyable "" >}}

```sql
USE information_schema;
desc SCHEMATA;
```

```
+----------------------------+--------------+------+------+---------+-------+
| Field                      | Type         | Null | Key  | Default | Extra |
+----------------------------+--------------+------+------+---------+-------+
| CATALOG_NAME               | varchar(512) | YES  |      | NULL    |       |
| SCHEMA_NAME                | varchar(64)  | YES  |      | NULL    |       |
| DEFAULT_CHARACTER_SET_NAME | varchar(64)  | YES  |      | NULL    |       |
| DEFAULT_COLLATION_NAME     | varchar(32)  | YES  |      | NULL    |       |
| SQL_PATH                   | varchar(512) | YES  |      | NULL    |       |
+----------------------------+--------------+------+------+---------+-------+
5 rows in set (0.00 sec)
```

{{< copyable "" >}}

```sql
SELECT * FROM SCHEMATA;
```

```
+--------------+--------------------+----------------------------+------------------------+----------+
| CATALOG_NAME | SCHEMA_NAME        | DEFAULT_CHARACTER_SET_NAME | DEFAULT_COLLATION_NAME | SQL_PATH |
+--------------+--------------------+----------------------------+------------------------+----------+
| def          | INFORMATION_SCHEMA | utf8mb4                    | utf8mb4_bin            | NULL     |
| def          | METRICS_SCHEMA     | utf8mb4                    | utf8mb4_bin            | NULL     |
| def          | mysql              | utf8mb4                    | utf8mb4_bin            | NULL     |
| def          | PERFORMANCE_SCHEMA | utf8mb4                    | utf8mb4_bin            | NULL     |
| def          | test               | utf8mb4                    | utf8mb4_bin            | NULL     |
+--------------+--------------------+----------------------------+------------------------+----------+
5 rows in set (0.00 sec)
```

`SCHEMATA`表のフィールドは次のように説明されています。

-   `CATALOG_NAME` ：データベースが属するカタログ。
-   `SCHEMA_NAME` ：データベース名。
-   `DEFAULT_CHARACTER_SET_NAME` ：データベースのデフォルトの文字セット。
-   `DEFAULT_COLLATION_NAME` ：データベースのデフォルトの照合順序。
-   `SQL_PATH` ：このアイテムの値は常に`NULL`です。
