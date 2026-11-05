---
title: COLLATIONS
summary: Learn the `COLLATIONS` information_schema table.
---

# COLLATIONS

The `COLLATIONS` table provides a list of collations that correspond to character sets in the `CHARACTER_SETS` table. Currently, this table is included only for compatibility with MySQL.

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
| ID                 | bigint      | YES  |      | NULL    |       |
| IS_DEFAULT         | varchar(3)  | YES  |      | NULL    |       |
| IS_COMPILED        | varchar(3)  | YES  |      | NULL    |       |
| SORTLEN            | bigint      | YES  |      | NULL    |       |
| PAD_ATTRIBUTE      | varchar(9)  | YES  |      | NULL    |       |
+--------------------+-------------+------+------+---------+-------+
7 rows in set (0.001 sec)
```

```sql
SELECT * FROM collations WHERE character_set_name='utf8mb4';
```

```sql
+--------------------+--------------------+------+------------+-------------+---------+---------------+
| COLLATION_NAME     | CHARACTER_SET_NAME | ID   | IS_DEFAULT | IS_COMPILED | SORTLEN | PAD_ATTRIBUTE |
+--------------------+--------------------+------+------------+-------------+---------+---------------+
| utf8mb4_0900_ai_ci | utf8mb4            |  255 |            | Yes         |       0 | NO PAD        |
| utf8mb4_0900_bin   | utf8mb4            |  309 |            | Yes         |       1 | NO PAD        |
| utf8mb4_bin        | utf8mb4            |   46 | Yes        | Yes         |       1 | PAD SPACE     |
| utf8mb4_general_ci | utf8mb4            |   45 |            | Yes         |       1 | PAD SPACE     |
| utf8mb4_unicode_ci | utf8mb4            |  224 |            | Yes         |       8 | PAD SPACE     |
+--------------------+--------------------+------+------------+-------------+---------+---------------+
5 rows in set (0.001 sec)
```

The description of columns in the `COLLATIONS` table is as follows:

* `COLLATION_NAME`: The name of the collation.
* `CHARACTER_SET_NAME`: The name of the character set which the collation belongs to.
* `ID`: The ID of the collation.
* `IS_DEFAULT`: Whether this collation is the default collation of the character set it belongs to.
* `IS_COMPILED`: Whether the character set is compiled into the server.
* `SORTLEN`: The minimum length of memory allocated when the collation sorts characters.
* `PAD_ATTRIBUTE`: Whether trailing spaces are ignored during string comparison. `PAD SPACE` means that trailing spaces are ignored (for example, `'abc'` equals `'abc   '`), while `NO PAD` means that trailing spaces are significant (for example, `'abc'` does not equal `'abc   '`).

## See also

- [`SHOW CHARACTER SET`](/sql-statements/sql-statement-show-character-set.md)
- [`SHOW COLLATION`](/sql-statements/sql-statement-show-collation.md)
- [`INFORMATION_SCHEMA.CHARACTER_SETS`](/information-schema/information-schema-character-sets.md)
- [`INFORMATION_SCHEMA.COLLATION_CHARACTER_SET_APPLICABILITY`](/information-schema/information-schema-collation-character-set-applicability.md)