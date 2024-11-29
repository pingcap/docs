---
title: VARIABLES_INFO
summary: VARIABLES_INFO` information_schema テーブルについて学習します。
---

# 変数情報 {#variables-info}

`VARIABLES_INFO`テーブルには、現在の TiDB インスタンスまたは TiDB クラスターの[システム変数](/system-variables.md)のデフォルト値、現在の値、およびスコープに関する情報が提供されます。

```sql
USE information_schema;
DESC variables_info;
```

```sql
+-----------------+---------------------+------+------+---------+-------+
| Field           | Type                | Null | Key  | Default | Extra |
+-----------------+---------------------+------+------+---------+-------+
| VARIABLE_NAME   | varchar(64)         | NO   |      | NULL    |       |
| VARIABLE_SCOPE  | varchar(64)         | NO   |      | NULL    |       |
| DEFAULT_VALUE   | varchar(64)         | NO   |      | NULL    |       |
| CURRENT_VALUE   | varchar(64)         | NO   |      | NULL    |       |
| MIN_VALUE       | bigint(64)          | YES  |      | NULL    |       |
| MAX_VALUE       | bigint(64) unsigned | YES  |      | NULL    |       |
| POSSIBLE_VALUES | varchar(256)        | YES  |      | NULL    |       |
| IS_NOOP         | varchar(64)         | NO   |      | NULL    |       |
+-----------------+---------------------+------+------+---------+-------+
8 rows in set (0.00 sec)
```

```sql
SELECT * FROM variables_info ORDER BY variable_name LIMIT 3;
```

```sql
+-----------------------------------+----------------+---------------+---------------+-----------+-----------+-----------------+---------+
| VARIABLE_NAME                     | VARIABLE_SCOPE | DEFAULT_VALUE | CURRENT_VALUE | MIN_VALUE | MAX_VALUE | POSSIBLE_VALUES | IS_NOOP |
+-----------------------------------+----------------+---------------+---------------+-----------+-----------+-----------------+---------+
| allow_auto_random_explicit_insert | SESSION,GLOBAL | OFF           | OFF           |      NULL |      NULL | NULL            | NO      |
| auto_increment_increment          | SESSION,GLOBAL | 1             | 1             |         1 |     65535 | NULL            | NO      |
| auto_increment_offset             | SESSION,GLOBAL | 1             | 1             |         1 |     65535 | NULL            | NO      |
+-----------------------------------+----------------+---------------+---------------+-----------+-----------+-----------------+---------+
3 rows in set (0.01 sec)
```

`VARIABLES_INFO`のテーブル内のフィールドは次のように説明されます。

-   `VARIABLE_NAME` : システム変数の名前。
-   `VARIABLE_SCOPE` : システム変数のスコープ`SESSION` 、システム変数が現在のセッションでのみ有効であることを意味します`INSTANCE` 、システム変数が TiDB インスタンスで有効であることを意味します。6 `GLOBAL` 、システム変数が TiDB クラスターで有効であることを意味します`NONE` 、システム変数が TiDB クラスターで読み取り専用であることを意味します。
-   `DEFAULT_VALUE` : システム変数のデフォルト値。
-   `CURRENT_VALUE` : システム変数の現在の値。スコープに`SESSION`含まれる場合、現在のセッションの値は`CURRENT_VALUE`になります。
-   `MIN_VALUE` : システム変数に許可される最小値。システム変数が数値でない場合、 `MIN_VALUE` NULL になります。
-   `MAX_VALUE` : システム変数に許可される最大値。システム変数が数値でない場合、 `MAX_VALUE` NULL になります。
-   `POSSIBLE_VALUES` : システム変数の可能な値。システム変数が列挙型でない場合、 `POSSIBLE_VALUES` NULL になります。
-   `IS_NOOP` : システム変数が`noop`システム変数であるかどうか。
