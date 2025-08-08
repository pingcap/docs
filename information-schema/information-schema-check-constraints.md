---
title: CHECK_CONSTRAINTS
summary: CHECK_CONSTRAINTS` INFORMATION_SCHEMA テーブルについて学習します。
---

# CHECK_CONSTRAINTS {#check-constraints}

`CHECK_CONSTRAINTS`表には、 [`CHECK`制約](/constraints.md#check)表に関する情報が示されています。

```sql
USE INFORMATION_SCHEMA;
DESC CHECK_CONSTRAINTS;
```

出力は次のようになります。

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
SET GLOBAL tidb_enable_check_constraint = ON;
CREATE TABLE test.t1 (id INT PRIMARY KEY, CHECK (id%2 = 0));
SELECT * FROM CHECK_CONSTRAINTS\G
```

出力は次のようになります。

```sql
*************************** 1. row ***************************
CONSTRAINT_CATALOG: def
 CONSTRAINT_SCHEMA: test
   CONSTRAINT_NAME: t1_chk_1
      CHECK_CLAUSE: (`id` % 2 = 0)
1 row in set (0.00 sec)
```

`CHECK_CONSTRAINTS`テーブル内のフィールドは次のように説明されます。

-   `CONSTRAINT_CATALOG` : 制約のカタログ。常に`def`です。
-   `CONSTRAINT_SCHEMA` : 制約のスキーマ。
-   `CONSTRAINT_NAME` : 制約の名前。
-   `CHECK_CLAUSE` : チェック制約の句。
