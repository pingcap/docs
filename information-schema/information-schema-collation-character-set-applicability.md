---
title: COLLATION_CHARACTER_SET_APPLICABILITY
summary: COLLATION_CHARACTER_SET_APPLICABILITY` INFORMATION_SCHEMA テーブルについて学習します。
---

# 照合文字セットの適用性 {#collation-character-set-applicability}

`COLLATION_CHARACTER_SET_APPLICABILITY`テーブルは、照合順序を該当する文字セット名にマッピングします。3 `COLLATIONS`と同様に、これは MySQL との互換性のためだけに含まれています。

```sql
USE INFORMATION_SCHEMA;
DESC COLLATION_CHARACTER_SET_APPLICABILITY;
```

出力は次のようになります。

```sql
+--------------------+-------------+------+------+---------+-------+
| Field              | Type        | Null | Key  | Default | Extra |
+--------------------+-------------+------+------+---------+-------+
| COLLATION_NAME     | varchar(32) | NO   |      | NULL    |       |
| CHARACTER_SET_NAME | varchar(32) | NO   |      | NULL    |       |
+--------------------+-------------+------+------+---------+-------+
2 rows in set (0.00 sec)
```

`COLLATION_CHARACTER_SET_APPLICABILITY`の表の`utf8mb4`の文字セットの照合順序マッピングをビュー。

```sql
SELECT * FROM COLLATION_CHARACTER_SET_APPLICABILITY WHERE character_set_name='utf8mb4';
```

出力は次のようになります。

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

`COLLATION_CHARACTER_SET_APPLICABILITY`表の列の説明は次のとおりです。

-   `COLLATION_NAME` :照合順序の名前。
-   `CHARACTER_SET_NAME` :照合順序が属する文字セットの名前。

## 参照 {#see-also}

-   [`SHOW CHARACTER SET`](/sql-statements/sql-statement-show-character-set.md)
-   [`SHOW COLLATION`](/sql-statements/sql-statement-show-collation.md)
-   [`INFORMATION_SCHEMA.CHARACTER_SETS`](/information-schema/information-schema-character-sets.md)
-   [`INFORMATION_SCHEMA.COLLATIONS`](/information-schema/information-schema-collations.md)
