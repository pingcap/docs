---
title: CREATE VIEW | TiDB SQL Statement Reference
summary: An overview of the usage of CREATE VIEW for the TiDB database.
---

# ビューの作成 {#create-view}

`CREATE VIEW`ステートメントは、テーブルと同様に、 `SELECT`ステートメントをクエリ可能なオブジェクトとして保存します。 TiDBのビューは実体化されていません。これは、ビューがクエリされると、TiDBが内部的にクエリを書き換えて、ビュー定義をSQLクエリと結合することを意味します。

## あらすじ {#synopsis}

```ebnf+diagram
CreateViewStmt ::=
    'CREATE' OrReplace ViewAlgorithm ViewDefiner ViewSQLSecurity 'VIEW' ViewName ViewFieldList 'AS' CreateViewSelectOpt ViewCheckOption

OrReplace ::=
    ( 'OR' 'REPLACE' )?

ViewAlgorithm ::=
    ( 'ALGORITHM' '=' ( 'UNDEFINED' | 'MERGE' | 'TEMPTABLE' ) )?

ViewDefiner ::=
    ( 'DEFINER' '=' Username )?

ViewSQLSecurity ::=
    ( 'SQL' 'SECURITY' ( 'DEFINER' | 'INVOKER' ) )?

ViewName ::= TableName

ViewFieldList ::=
    ( '(' Identifier ( ',' Identifier )* ')' )?

ViewCheckOption ::=
    ( 'WITH' ( 'CASCADED' | 'LOCAL' ) 'CHECK' 'OPTION' )?
```

## 例 {#examples}

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
Query OK, 0 rows affected (0.11 sec)

mysql> INSERT INTO t1 (c1) VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.03 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> CREATE VIEW v1 AS SELECT * FROM t1 WHERE c1 > 2;
Query OK, 0 rows affected (0.11 sec)

mysql> SELECT * FROM t1;
+----+----+
| id | c1 |
+----+----+
|  1 |  1 |
|  2 |  2 |
|  3 |  3 |
|  4 |  4 |
|  5 |  5 |
+----+----+
5 rows in set (0.00 sec)

mysql> SELECT * FROM v1;
+----+----+
| id | c1 |
+----+----+
|  3 |  3 |
|  4 |  4 |
|  5 |  5 |
+----+----+
3 rows in set (0.00 sec)

mysql> INSERT INTO t1 (c1) VALUES (6);
Query OK, 1 row affected (0.01 sec)

mysql> SELECT * FROM v1;
+----+----+
| id | c1 |
+----+----+
|  3 |  3 |
|  4 |  4 |
|  5 |  5 |
|  6 |  6 |
+----+----+
4 rows in set (0.00 sec)

mysql> INSERT INTO v1 (c1) VALUES (7);
ERROR 1105 (HY000): insert into view v1 is not supported now.
```

## MySQLの互換性 {#mysql-compatibility}

-   現在、TiDBのビューは挿入または更新できません（つまり、 `INSERT VIEW`と`UPDATE VIEW`はサポートされていません）。 `WITH CHECK OPTION`は構文的に互換性があるだけですが、有効にはなりません。
-   現在、TiDBのビューは`ALTER VIEW`をサポートしていませんが、代わりに`CREATE OR REPLACE`を使用できます。
-   現在、 `ALGORITHM`フィールドはTiDBで構文的にのみ互換性がありますが、有効にはなりません。 TiDBは現在、MERGEアルゴリズムのみをサポートしています。

## も参照してください {#see-also}

-   [ドロップビュー](/sql-statements/sql-statement-drop-view.md)
-   [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
-   [CREATETABLEを表示する](/sql-statements/sql-statement-show-create-table.md)
-   [ドロップテーブル](/sql-statements/sql-statement-drop-table.md)
