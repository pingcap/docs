---
title: COLLATION_CHARACTER_SET_APPLICABILITY
summary: Learn the `COLLATION_CHARACTER_SET_APPLICABILITY` INFORMATION_SCHEMA table.
---

# COLLATION_CHARACTER_SET_APPLICABILITY {#collation-character-set-applicability}

`COLLATION_CHARACTER_SET_APPLICABILITY`表は、照合順序を該当する文字セット名にマップします。 `COLLATIONS`テーブルと同様に、これは MySQL との互換性のためだけに含まれています。

```sql
USE INFORMATION_SCHEMA;
DESC COLLATION_CHARACTER_SET_APPLICABILITY;
```

出力は次のとおりです。

```sql
+--------------------+-------------+------+------+---------+-------+
| Field              | Type        | Null | Key  | Default | Extra |
+--------------------+-------------+------+------+---------+-------+
| COLLATION_NAME     | varchar(32) | NO   |      | NULL    |       |
| CHARACTER_SET_NAME | varchar(32) | NO   |      | NULL    |       |
+--------------------+-------------+------+------+---------+-------+
2 rows in set (0.00 sec)
```

`COLLATION_CHARACTER_SET_APPLICABILITY`表の`utf8mb4`文字セットの照合順序マッピングをビュー。

```sql
SELECT * FROM COLLATION_CHARACTER_SET_APPLICABILITY WHERE character_set_name='utf8mb4';
```

出力は次のとおりです。

```sql
+--------------------+--------------------+
| COLLATION_NAME     | CHARACTER_SET_NAME |
+--------------------+--------------------+
| utf8mb4_bin        | utf8mb4            |
| utf8mb4_general_ci | utf8mb4            |
| utf8mb4_unicode_ci | utf8mb4            |
+--------------------+--------------------+
3 rows in set (0.00 sec)
```

`COLLATION_CHARACTER_SET_APPLICABILITY`のテーブルの列の説明は次のとおりです。

-   `COLLATION_NAME` :照合順序の名前。
-   `CHARACTER_SET_NAME` :照合順序が属する文字セットの名前。
