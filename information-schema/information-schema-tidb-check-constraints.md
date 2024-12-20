---
title: TIDB_CHECK_CONSTRAINTS
summary: TIDB_CHECK_CONSTRAINTS` INFORMATION_SCHEMA テーブルについて学習します。
---

# TIDB_CHECK_CONSTRAINTS {#tidb-check-constraints}

`TIDB_CHECK_CONSTRAINTS`テーブルは、 [`CHECK`制約](/constraints.md#check)テーブルに関する情報を提供します。 [`CHECK_CONSTRAINTS`](/information-schema/information-schema-check-constraints.md)の列に加えて、 `TIDB_CHECK_CONSTRAINTS` `CHECK`制約を定義するテーブルの名前と ID を提供します。

```sql
USE INFORMATION_SCHEMA;
DESC TIDB_CHECK_CONSTRAINTS;
```

出力は次のようになります。

```sql
+--------------------+-------------+------+------+---------+-------+
| Field              | Type        | Null | Key  | Default | Extra |
+--------------------+-------------+------+------+---------+-------+
| CONSTRAINT_CATALOG | varchar(64) | NO   |      | NULL    |       |
| CONSTRAINT_SCHEMA  | varchar(64) | NO   |      | NULL    |       |
| CONSTRAINT_NAME    | varchar(64) | NO   |      | NULL    |       |
| CHECK_CLAUSE       | longtext    | NO   |      | NULL    |       |
| TABLE_NAME         | varchar(64) | YES  |      | NULL    |       |
| TABLE_ID           | bigint(21)  | YES  |      | NULL    |       |
+--------------------+-------------+------+------+---------+-------+
6 rows in set (0.00 sec)
```

次の例では、 `CREATE TABLE`ステートメントを使用して`CHECK`制約を追加します。

```sql
SET GLOBAL tidb_enable_check_constraint = ON;
CREATE TABLE test.t1 (id INT PRIMARY KEY, CHECK (id%2 = 0));
SELECT * FROM TIDB_CHECK_CONSTRAINTS\G
```

出力は次のようになります。

```sql
*************************** 1. row ***************************
CONSTRAINT_CATALOG: def
 CONSTRAINT_SCHEMA: test
   CONSTRAINT_NAME: t1_chk_1
      CHECK_CLAUSE: (`id` % 2 = 0)
        TABLE_NAME: t1
          TABLE_ID: 107
1 row in set (0.02 sec)
```

`TIDB_CHECK_CONSTRAINTS`テーブル内のフィールドは次のように説明されます。

-   `CONSTRAINT_CATALOG` : 制約のカタログ。常に`def`です。
-   `CONSTRAINT_SCHEMA` : 制約のスキーマ。
-   `CONSTRAINT_NAME` : 制約の名前。
-   `CHECK_CLAUSE` : チェック制約の句。
-   `TABLE_NAME` : 制約が配置されているテーブルの名前。
-   `TABLE_ID` : 制約が配置されているテーブルの ID。
