---
title: DELETE | TiDB SQL Statement Reference
summary: DELETEステートメントは、指定されたテーブルから行を削除します。MySQLの互換性があります。
---

# 消去 {#delete}

`DELETE`ステートメントは、指定されたテーブルから行を削除します。

## あらすじ {#synopsis}

```ebnf+diagram
DeleteFromStmt ::=
    'DELETE' TableOptimizerHints PriorityOpt QuickOptional IgnoreOptional ( 'FROM' ( TableName TableAsNameOpt IndexHintListOpt WhereClauseOptional OrderByOptional LimitClause | TableAliasRefList 'USING' TableRefs WhereClauseOptional ) | TableAliasRefList 'FROM' TableRefs WhereClauseOptional )
```

## 例 {#examples}

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
Query OK, 0 rows affected (0.11 sec)

mysql> INSERT INTO t1 (c1) VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.03 sec)
Records: 5  Duplicates: 0  Warnings: 0

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

mysql> DELETE FROM t1 WHERE id = 4;
Query OK, 1 row affected (0.02 sec)

mysql> SELECT * FROM t1;
+----+----+
| id | c1 |
+----+----+
|  1 |  1 |
|  2 |  2 |
|  3 |  3 |
|  5 |  5 |
+----+----+
4 rows in set (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

TiDB の`DELETE`ステートメントは MySQL と完全な互換性があります。互換性の違いが見つかった場合は、 [バグを報告](https://docs.pingcap.com/tidb/stable/support) .

## こちらも参照 {#see-also}

-   [入れる](/sql-statements/sql-statement-insert.md)
-   [選択する](/sql-statements/sql-statement-select.md)
-   [アップデート](/sql-statements/sql-statement-update.md)
-   [交換する](/sql-statements/sql-statement-replace.md)
