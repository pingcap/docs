---
title: COLLATIONS
summary: COLLATIONS` information_schema テーブルについて学習します。
---

# 照合 {#collations}

`COLLATIONS`テーブルには、 `CHARACTER_SETS`テーブル内の文字セットに対応する照合順序のリストが提供されます。現在、このテーブルは MySQL との互換性のためだけに含まれています。

```sql
USE information_schema;
DESC collations;
```

```sql
+--------------------+-------------+------+------+---------+-------+
| Field              | Type        | Null | Key  | Default | Extra |
+--------------------+-------------+------+------+---------+-------+
| COLLATION_NAME     | varchar(32) | YES  |      | NULL    |       |
| CHARACTER_SET_NAME | varchar(32) | YES  |      | NULL    |       |
| ID                 | bigint(11)  | YES  |      | NULL    |       |
| IS_DEFAULT         | varchar(3)  | YES  |      | NULL    |       |
| IS_COMPILED        | varchar(3)  | YES  |      | NULL    |       |
| SORTLEN            | bigint(3)   | YES  |      | NULL    |       |
+--------------------+-------------+------+------+---------+-------+
6 rows in set (0.00 sec)
```

```sql
SELECT * FROM collations WHERE character_set_name='utf8mb4';
```

```sql
+--------------------+--------------------+------+------------+-------------+---------+
| COLLATION_NAME     | CHARACTER_SET_NAME | ID   | IS_DEFAULT | IS_COMPILED | SORTLEN |
+--------------------+--------------------+------+------------+-------------+---------+
| utf8mb4_bin        | utf8mb4            |   46 | Yes        | Yes         |       1 |
| utf8mb4_general_ci | utf8mb4            |   45 |            | Yes         |       1 |
| utf8mb4_unicode_ci | utf8mb4            |  224 |            | Yes         |       1 |
+--------------------+--------------------+------+------------+-------------+---------+
3 rows in set (0.001 sec)
```

`COLLATIONS`表の列の説明は次のとおりです。

-   `COLLATION_NAME` :照合順序の名前。
-   `CHARACTER_SET_NAME` :照合順序が属する文字セットの名前。
-   `ID` :照合順序のID。
-   `IS_DEFAULT` : この照合順序が、それが属する文字セットのデフォルトの照合順序であるかどうか。
-   `IS_COMPILED` : 文字セットがサーバーにコンパイルされているかどうか。
-   `SORTLEN` :照合順序が文字をソートするときに割り当てられるメモリの最小長。

## 参照 {#see-also}

-   [`SHOW CHARACTER SET`](/sql-statements/sql-statement-show-character-set.md)
-   [`SHOW COLLATION`](/sql-statements/sql-statement-show-collation.md)
-   [`INFORMATION_SCHEMA.CHARACTER_SETS`](/information-schema/information-schema-character-sets.md)
-   [`INFORMATION_SCHEMA.COLLATION_CHARACTER_SET_APPLICABILITY`](/information-schema/information-schema-collation-character-set-applicability.md)
