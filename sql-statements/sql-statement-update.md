---
title: UPDATE | TiDB SQL Statement Reference
summary: An overview of the usage of UPDATE for the TiDB database.
---

# アップデート {#update}

`UPDATE`ステートメントは、指定されたテーブルのデータを変更するために使用されます。

## あらすじ {#synopsis}

**UpdateStmt：**

![UpdateStmt](/media/sqlgram/UpdateStmt.png)

**PriorityOpt：**

![PriorityOpt](/media/sqlgram/PriorityOpt.png)

**TableRef：**

![TableRef](/media/sqlgram/TableRef.png)

**TableRefs：**

![TableRefs](/media/sqlgram/TableRefs.png)

**AssignmentList：**

![AssignmentList](/media/sqlgram/AssignmentList.png)

**WhereClauseOptional：**

![WhereClauseOptional](/media/sqlgram/WhereClauseOptional.png)

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

## MySQLの互換性 {#mysql-compatibility}

TiDBは、式を評価するときに常に列の元の値を使用します。例えば：

```sql
CREATE TABLE t (a int, b int);
INSERT INTO t VALUES (1,2);
UPDATE t SET a = a+1,b=a;
```

MySQLでは、同じステートメントで列1が値`a`に設定されているため、列`b`が2に更新され、値`a` （1）が`a+1` （2）に更新されます。

TiDBは、より標準的なSQLの動作に従い、 `b`から1に更新します。

## も参照してください {#see-also}

-   [入れる](/sql-statements/sql-statement-insert.md)
-   [選択する](/sql-statements/sql-statement-select.md)
-   [消去](/sql-statements/sql-statement-delete.md)
-   [交換](/sql-statements/sql-statement-replace.md)
