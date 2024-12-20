---
title: TRUNCATE | TiDB SQL Statement Reference
summary: TiDB データベースでの TRUNCATE の使用法の概要。
---

# 切り捨て {#truncate}

`TRUNCATE`ステートメントは、非トランザクション方式でテーブルからすべてのデータを削除します。3 `TRUNCATE`前の定義の`DROP TABLE` + `CREATE TABLE`と意味的に同じであると考えることができます。

`TRUNCATE TABLE tableName`と`TRUNCATE tableName`どちらも有効な構文です。

## 概要 {#synopsis}

```ebnf+diagram
TruncateTableStmt ::=
    "TRUNCATE" ( "TABLE" )? TableName

TableName ::=
    (Identifier ".")? Identifier
```

## 例 {#examples}

```sql
mysql> CREATE TABLE t1 (a INT NOT NULL PRIMARY KEY);
Query OK, 0 rows affected (0.11 sec)

mysql> INSERT INTO t1 VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.01 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> SELECT * FROM t1;
+---+
| a |
+---+
| 1 |
| 2 |
| 3 |
| 4 |
| 5 |
+---+
5 rows in set (0.00 sec)

mysql> TRUNCATE t1;
Query OK, 0 rows affected (0.11 sec)

mysql> SELECT * FROM t1;
Empty set (0.00 sec)

mysql> INSERT INTO t1 VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.01 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> TRUNCATE TABLE t1;
Query OK, 0 rows affected (0.11 sec)
```

## MySQL 互換性 {#mysql-compatibility}

TiDB の`TRUNCATE`ステートメントは MySQL と完全に互換性があります。互換性の違いが見つかった場合は、 [バグを報告する](https://docs.pingcap.com/tidb/stable/support) 。

## 参照 {#see-also}

-   [テーブルを削除](/sql-statements/sql-statement-drop-table.md)
-   [消去](/sql-statements/sql-statement-delete.md)
-   [テーブルの作成](/sql-statements/sql-statement-create-table.md)
-   [表示テーブルの作成](/sql-statements/sql-statement-show-create-table.md)
