---
title: ALTER INDEX
summary: TiDB データベースの ALTER INDEX の使用法の概要。
---

# インデックスの変更 {#alter-index}

`ALTER INDEX`ステートメントは、インデックスの可視性を`Visible`または`Invisible`に変更するために使用されます。非表示のインデックスは DML ステートメントによって維持されますが、クエリ オプティマイザーでは使用されません。これは、インデックスを永続的に削除する前に再確認したいシナリオで役立ちます。TiDB v8.0.0 以降では、システム変数[`tidb_opt_use_invisible_indexes`](/system-variables.md#tidb_opt_use_invisible_indexes-new-in-v800)変更することで、オプティマイザーが非表示のインデックスを選択するようにすることができます。

## 概要 {#synopsis}

```ebnf+diagram
AlterTableStmt
         ::= 'ALTER' 'IGNORE'? 'TABLE' TableName AlterIndexSpec ( ',' AlterIndexSpec )*

AlterIndexSpec
         ::= 'ALTER' 'INDEX' Identifier ( 'VISIBLE' | 'INVISIBLE' )
```

## 例 {#examples}

`ALTER TABLE ... ALTER INDEX ...`ステートメントを使用してインデックスの可視性を変更できます。

```sql
CREATE TABLE t1 (c1 INT, UNIQUE(c1));
ALTER TABLE t1 ALTER INDEX c1 INVISIBLE;
```

```sql
Query OK, 0 rows affected (0.02 sec)
```

```sql
SHOW CREATE TABLE t1;
```

```sql
+-------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table | Create Table
                                    |
+-------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| t1    | CREATE TABLE `t1` (
  `c1` int DEFAULT NULL,
  UNIQUE KEY `c1` (`c1`) /*!80000 INVISIBLE */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin |
+-------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

オプティマイザーは**非表示のインデックス**`c1`を使用できません。

```sql
EXPLAIN SELECT c1 FROM t1 ORDER BY c1;
```

```sql
+-------------------------+----------+-----------+---------------+--------------------------------+
| id                      | estRows  | task      | access object | operator info                  |
+-------------------------+----------+-----------+---------------+--------------------------------+
| Sort_4                  | 10000.00 | root      |               | test.t1.c1:asc                 |
| └─TableReader_8         | 10000.00 | root      |               | data:TableFullScan_7           |
|   └─TableFullScan_7     | 10000.00 | cop[tikv] | table:t1      | keep order:false, stats:pseudo |
+-------------------------+----------+-----------+---------------+--------------------------------+
3 rows in set (0.00 sec)
```

比較すると、 `c2`**可視インデックス**であり、オプティマイザーで使用できます。

```sql
EXPLAIN SELECT c2 FROM t1 ORDER BY c2;
```

```sql
+------------------------+----------+-----------+------------------------+-------------------------------+
| id                     | estRows  | task      | access object          | operator info                 |
+------------------------+----------+-----------+------------------------+-------------------------------+
| IndexReader_13         | 10000.00 | root      |                        | index:IndexFullScan_12        |
| └─IndexFullScan_12     | 10000.00 | cop[tikv] | table:t1, index:c2(c2) | keep order:true, stats:pseudo |
+------------------------+----------+-----------+------------------------+-------------------------------+
2 rows in set (0.00 sec)
```

`USE INDEX` SQL ヒントを使用して強制的にインデックスを使用した場合でも、オプティマイザーは非表示のインデックスを使用できません。そうでない場合は、エラーが返されます。

```sql
SELECT * FROM t1 USE INDEX(c1);
```

```sql
ERROR 1176 (42000): Key 'c1' doesn't exist in table 't1'
```

> **注記：**
>
> ここでの「非表示」とは、オプティマイザに対してのみ非表示であることを意味します。非表示のインデックスを変更または削除することは可能です。

```sql
ALTER TABLE t1 DROP INDEX c1;
```

```sql
Query OK, 0 rows affected (0.02 sec)
```

## MySQL 互換性 {#mysql-compatibility}

-   TiDB の非表示インデックスは、MySQL 8.0 の同等の機能に基づいてモデル化されています。
-   MySQL と同様に、TiDB では`PRIMARY KEY`インデックスを非表示にすることはできません。

## 参照 {#see-also}

-   [テーブルの作成](/sql-statements/sql-statement-create-table.md)
-   [インデックスの作成](/sql-statements/sql-statement-create-index.md)
-   [インデックスを追加](/sql-statements/sql-statement-add-index.md)
-   [インデックスを削除](/sql-statements/sql-statement-drop-index.md)
-   [インデックス名の変更](/sql-statements/sql-statement-rename-index.md)
