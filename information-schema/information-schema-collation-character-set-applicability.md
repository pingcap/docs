---
title: COLLATION_CHARACTER_SET_APPLICABILITY
summary: Learn the `COLLATION_CHARACTER_SET_APPLICABILITY` information_schema table.
---

# COLLATION_CHARACTER_SET_APPLICABILITY {#collation-character-set-applicability}

`COLLATION_CHARACTER_SET_APPLICABILITY`の表は、照合を該当する文字セット名にマップします。 `COLLATIONS`の表と同様に、MySQLとの互換性のためにのみ含まれています。

{{< copyable "" >}}

```sql
USE information_schema;
DESC collation_character_set_applicability;
```

```sql
+--------------------+-------------+------+------+---------+-------+
| Field              | Type        | Null | Key  | Default | Extra |
+--------------------+-------------+------+------+---------+-------+
| COLLATION_NAME     | varchar(32) | NO   |      | NULL    |       |
| CHARACTER_SET_NAME | varchar(32) | NO   |      | NULL    |       |
+--------------------+-------------+------+------+---------+-------+
2 rows in set (0.00 sec)
```

{{< copyable "" >}}

```sql
SELECT * FROM collation_character_set_applicability WHERE character_set_name='utf8mb4';
```

```sql
+----------------+--------------------+
| COLLATION_NAME | CHARACTER_SET_NAME |
+----------------+--------------------+
| utf8mb4_bin    | utf8mb4            |
+----------------+--------------------+
1 row in set (0.00 sec)
```

`COLLATION_CHARACTER_SET_APPLICABILITY`テーブルの列の説明は次のとおりです。

-   `COLLATION_NAME` ：照合順序の名前。
-   `CHARACTER_SET_NAME` ：照合順序が属する文字セットの名前。
