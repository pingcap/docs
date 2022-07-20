---
title: SHOW INDEXES [FROM|IN] | TiDB SQL Statement Reference
summary: An overview of the usage of SHOW INDEXES [FROM|IN] for the TiDB database.
---

# インデックスを表示[FROM|IN] {#show-indexes-from-in}

ステートメント`SHOW INDEXES [FROM|IN]`は、指定されたテーブルのインデックスをリストします。ステートメント`SHOW INDEX [FROM|IN]`はこのステートメントのエイリアスであり、MySQLとの互換性のために含まれて`SHOW KEYS [FROM|IN]`ます。

## あらすじ {#synopsis}

**ShowIndexStmt：**

![ShowIndexStmt](/media/sqlgram/ShowIndexStmt.png)

**ShowIndexKwd：**

![ShowIndexKwd](/media/sqlgram/ShowIndexKwd.png)

**FromOrIn：**

![FromOrIn](/media/sqlgram/FromOrIn.png)

**TableName：**

![TableName](/media/sqlgram/TableName.png)

**ShowLikeOrWhereOpt：**

![ShowLikeOrWhereOpt](/media/sqlgram/ShowLikeOrWhereOpt.png)

## 例 {#examples}

```sql
mysql> CREATE TABLE t1 (id int not null primary key AUTO_INCREMENT, col1 INT, INDEX(col1));
Query OK, 0 rows affected (0.12 sec)

mysql> SHOW INDEXES FROM t1;
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+
| Table | Non_unique | Key_name | Seq_in_index | Column_name | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment | Visible | Expression |
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+
| t1    |          0 | PRIMARY  |            1 | id          | A         |           0 |     NULL | NULL   |      | BTREE      |         |               | YES
    | NULL       |
| t1    |          1 | col1     |            1 | col1        | A         |           0 |     NULL | NULL   | YES  | BTREE      |         |               | YES
    | NULL       |
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+
2 rows in set (0.00 sec)

mysql> SHOW INDEX FROM t1;
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+
| Table | Non_unique | Key_name | Seq_in_index | Column_name | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment | Visible | Expression |
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+
| t1    |          0 | PRIMARY  |            1 | id          | A         |           0 |     NULL | NULL   |      | BTREE      |         |               | YES
    | NULL       |
| t1    |          1 | col1     |            1 | col1        | A         |           0 |     NULL | NULL   | YES  | BTREE      |         |               | YES
    | NULL       |
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+
2 rows in set (0.00 sec)

mysql> SHOW KEYS FROM t1;
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+
| Table | Non_unique | Key_name | Seq_in_index | Column_name | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment | Visible | Expression |
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+
| t1    |          0 | PRIMARY  |            1 | id          | A         |           0 |     NULL | NULL   |      | BTREE      |         |               | YES
    | NULL       |
| t1    |          1 | col1     |            1 | col1        | A         |           0 |     NULL | NULL   | YES  | BTREE      |         |               | YES
    | NULL       |
+-------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+
2 rows in set (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

MySQLの`Cardinality`列は、インデックスのさまざまな値の数を示しています。 TiDBでは、 `Cardinality`列には常に`0`が表示されます。

## も参照してください {#see-also}

-   [作成テーブルを表示](/sql-statements/sql-statement-show-create-table.md)
-   [ドロップインデックス](/sql-statements/sql-statement-drop-index.md)
-   [インデックスの作成](/sql-statements/sql-statement-create-index.md)
