---
title: CHECK_CONSTRAINTS
summary: CHECK_CONSTRAINTS表には、CHECK制約の表に関する情報が記載されています。CONSTRAINT_CATALOGは常にdefで、CONSTRAINT_SCHEMAは制約のスキーマを示し、CONSTRAINT_NAMEは制約の名前を示します。CHECK_CLAUSEはチェック制約の句を示します。CREATE TABLEステートメントを使用してCHECK制約を追加することができます。
---

# CHECK_CONSTRAINTS {#check-constraints}

`CHECK_CONSTRAINTS`表には、 [`CHECK`制約](/constraints.md#check)の表に関する情報が記載されています。

```sql
USE INFORMATION_SCHEMA;
DESC CHECK_CONSTRAINTS;
```

出力は次のとおりです。

```sql
+--------------------+-------------+------+-----+---------+-------+
| Field              | Type        | Null | Key | Default | Extra |
+--------------------+-------------+------+-----+---------+-------+
| CONSTRAINT_CATALOG | varchar(64) | NO   |     | NULL    |       |
| CONSTRAINT_SCHEMA  | varchar(64) | NO   |     | NULL    |       |
| CONSTRAINT_NAME    | varchar(64) | NO   |     | NULL    |       |
| CHECK_CLAUSE       | longtext    | NO   |     | NULL    |       |
+--------------------+-------------+------+-----+---------+-------+
4 rows in set (0.00 sec)
```

次の例では、 `CREATE TABLE`ステートメントを使用して`CHECK`制約を追加します。

```sql
CREATE TABLE test.t1 (id INT PRIMARY KEY, CHECK (id%2 = 0));
SELECT * FROM CHECK_CONSTRAINTS\G
```

出力は次のとおりです。

```sql
*************************** 1. row ***************************
CONSTRAINT_CATALOG: def
 CONSTRAINT_SCHEMA: test
   CONSTRAINT_NAME: t1_chk_1
      CHECK_CLAUSE: (`id` % 2 = 0)
1 row in set (0.00 sec)
```

`CHECK_CONSTRAINTS`テーブルのフィールドは次のように説明されています。

-   `CONSTRAINT_CATALOG` : 制約のカタログ。常に`def`です。
-   `CONSTRAINT_SCHEMA` : 制約のスキーマ。
-   `CONSTRAINT_NAME` : 制約の名前。
-   `CHECK_CLAUSE` : チェック制約の句。
