---
title: SHOW TABLE STATUS | TiDB SQL Statement Reference
summary: An overview of the usage of SHOW TABLE STATUS for the TiDB database.
---

# テーブルステータスを表示 {#show-table-status}

このステートメントは、TiDBのテーブルに関するさまざまな統計を示しています。統計が古くなっているように見える場合は、 [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)を実行することをお勧めします。

## あらすじ {#synopsis}

**ShowTableStatusStmt：**

![ShowTableStatusStmt](/media/sqlgram/ShowTableStatusStmt.png)

**FromOrIn：**

![FromOrIn](/media/sqlgram/FromOrIn.png)

**StatusTableName：**

![StatusTableName](/media/sqlgram/StatusTableName.png)

## 例 {#examples}

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
Query OK, 0 rows affected (0.11 sec)

mysql> INSERT INTO t1 (c1) VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.02 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> SHOW TABLE STATUS LIKE 't1'\G
*************************** 1. row ***************************
           Name: t1
         Engine: InnoDB
        Version: 10
     Row_format: Compact
           Rows: 0
 Avg_row_length: 0
    Data_length: 0
Max_data_length: 0
   Index_length: 0
      Data_free: 0
 Auto_increment: 30001
    Create_time: 2019-04-19 08:32:06
    Update_time: NULL
     Check_time: NULL
      Collation: utf8mb4_bin
       Checksum:
 Create_options:
        Comment:
1 row in set (0.00 sec)

mysql> analyze table t1;
Query OK, 0 rows affected (0.12 sec)

mysql> SHOW TABLE STATUS LIKE 't1'\G
*************************** 1. row ***************************
           Name: t1
         Engine: InnoDB
        Version: 10
     Row_format: Compact
           Rows: 5
 Avg_row_length: 16
    Data_length: 80
Max_data_length: 0
   Index_length: 0
      Data_free: 0
 Auto_increment: 30001
    Create_time: 2019-04-19 08:32:06
    Update_time: NULL
     Check_time: NULL
      Collation: utf8mb4_bin
       Checksum:
 Create_options:
        Comment:
1 row in set (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQLと完全に互換性があると理解されています。互換性の違いは、GitHubでは[問題を介して報告された](https://github.com/pingcap/tidb/issues/new/choose)である必要があります。

## も参照してください {#see-also}

-   [テーブルを表示](/sql-statements/sql-statement-show-tables.md)
-   [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
-   [ドロップテーブル](/sql-statements/sql-statement-drop-table.md)
-   [CREATETABLEを表示する](/sql-statements/sql-statement-show-create-table.md)
