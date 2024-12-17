---
title: UPDATE | TiDB SQL Statement Reference
summary: TiDB データベースの UPDATE の使用法の概要。
---

# アップデート {#update}

`UPDATE`ステートメントは、指定されたテーブル内のデータを変更するために使用されます。

## 概要 {#synopsis}

```ebnf+diagram
UpdateStmt ::=
    "UPDATE" UpdateOption
(   TableRef "SET" Assignment ("," Assignment)* WhereClause? OrderBy? Limit?
|   TableRefs "SET" Assignment ("," Assignment)* WhereClause?
)

UpdateOption ::=
    OptimizerHints? ("LOW_PRIORITY" | "HIGH_PRIORITY" | "DELAYED")? "IGNORE"?

TableRef ::=
    ( TableFactor | JoinTable )

TableRefs ::=
    EscapedTableRef ("," EscapedTableRef)*
```

> **注記：**
>
> v6.6.0 以降、TiDB は[リソース管理](/tidb-resource-control.md)サポートします。この機能を使用すると、異なるリソース グループで異なる優先度の SQL 文を実行できます。これらのリソース グループに適切なクォータと優先度を構成することで、異なる優先度の SQL 文のスケジュールをより適切に制御できます。リソース制御を有効にすると、文の優先度 ( `LOW_PRIORITY`と`HIGH_PRIORITY` ) は無効になります。異なる SQL 文のリソース使用を管理するには、 [リソース管理](/tidb-resource-control.md)使用することをお勧めします。

## 例 {#examples}

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
Query OK, 0 rows affected (0.11 sec)

mysql> INSERT INTO t1 (c1) VALUES (1), (2), (3);
Query OK, 3 rows affected (0.02 sec)
Records: 3  Duplicates: 0  Warnings: 0

mysql> SELECT * FROM t1;
+----+----+
| id | c1 |
+----+----+
|  1 |  1 |
|  2 |  2 |
|  3 |  3 |
+----+----+
3 rows in set (0.00 sec)

mysql> UPDATE t1 SET c1=5 WHERE c1=3;
Query OK, 1 row affected (0.01 sec)
Rows matched: 1  Changed: 1  Warnings: 0

mysql> SELECT * FROM t1;
+----+----+
| id | c1 |
+----+----+
|  1 |  1 |
|  2 |  2 |
|  3 |  5 |
+----+----+
3 rows in set (0.00 sec)
```

## MySQL 互換性 {#mysql-compatibility}

TiDB は、式を評価するときに常に列の元の値を使用します。例:

```sql
CREATE TABLE t (a int, b int);
INSERT INTO t VALUES (1,2);
UPDATE t SET a = a+1,b=a;
```

MySQL では、列`b`値`a`に設定されているため 2 に更新され、同じステートメントで値`a` (1) は値`a+1` (2) に更新されます。

TiDB はより標準的な SQL 動作に従い、 `b`対 1 で更新します。

## 参照 {#see-also}

-   [入れる](/sql-statements/sql-statement-insert.md)
-   [選択](/sql-statements/sql-statement-select.md)
-   [消去](/sql-statements/sql-statement-delete.md)
-   [交換する](/sql-statements/sql-statement-replace.md)
