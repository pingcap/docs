---
title: SHOW PLACEMENT FOR
summary: The usage of SHOW PLACEMENT FOR in TiDB.
---

# の配置を表示 {#show-placement-for}

> **警告：**
>
> SQLの配置ルールは実験的機能です。 GAの前に構文が変更される可能性があり、バグもある可能性があります。
>
> リスクを理解している場合は、 `SET GLOBAL tidb_enable_alter_placement = 1;`を実行することでこの実験機能を有効にできます。

`SHOW PLACEMENT FOR`は、直接配置および配置ポリシーからのすべての配置オプションを要約し、特定のテーブル、データベーススキーマ、またはパーティションの標準形式でそれらを表示します。

## あらすじ {#synopsis}

```ebnf+diagram
ShowStmt ::=
    "PLACEMENT" "FOR" ShowPlacementTarget

ShowPlacementTarget ::=
    DatabaseSym DBName
|   "TABLE" TableName
|   "TABLE" TableName "PARTITION" Identifier
```

## 例 {#examples}

{{< copyable "" >}}

```sql
CREATE PLACEMENT POLICY p1 PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4;
use test;
ALTER DATABASE test PLACEMENT POLICY=p1;
CREATE TABLE t1 (a INT);
CREATE TABLE t2 (a INT) PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4;
SHOW PLACEMENT FOR DATABASE test;
SHOW PLACEMENT FOR TABLE t1;
SHOW CREATE TABLE t1\G
SHOW PLACEMENT FOR TABLE t2;
CREATE TABLE t3 (a INT) PARTITION BY RANGE (a) (PARTITION p1 VALUES LESS THAN (10), PARTITION p2 VALUES LESS THAN (20) FOLLOWERS=4);
SHOW PLACEMENT FOR TABLE t3 PARTITION p1;
SHOW PLACEMENT FOR TABLE t3 PARTITION p2;
```

```
Query OK, 0 rows affected (0.02 sec)

Query OK, 0 rows affected (0.00 sec)

Query OK, 0 rows affected (0.00 sec)

Query OK, 0 rows affected (0.01 sec)

+---------------+----------------------------------------------------------------------+------------------+
| Target        | Placement                                                            | Scheduling_State |
+---------------+----------------------------------------------------------------------+------------------+
| DATABASE test | PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4 | INPROGRESS       |
+---------------+----------------------------------------------------------------------+------------------+
1 row in set (0.00 sec)

+---------------+-------------+------------------+
| Target        | Placement   | Scheduling_State |
+---------------+-------------+------------------+
| TABLE test.t1 | FOLLOWERS=4 | INPROGRESS       |
+---------------+-------------+------------------+
1 row in set (0.00 sec)

*************************** 1. row ***************************
       Table: t1
Create Table: CREATE TABLE `t1` (
  `a` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin /*T![placement] PLACEMENT POLICY=`p1` */
1 row in set (0.00 sec)

+---------------+----------------------------------------------------------------------+------------------+
| Target        | Placement                                                            | Scheduling_State |
+---------------+----------------------------------------------------------------------+------------------+
| TABLE test.t2 | PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4 | INPROGRESS       |
+---------------+----------------------------------------------------------------------+------------------+
1 row in set (0.00 sec)

Query OK, 0 rows affected (0.14 sec)

+----------------------------+-----------------------------------------------------------------------+------------------+
| Target                     | Placement                                                             | Scheduling_State |
+----------------------------+-----------------------------------------------------------------------+------------------+
| TABLE test.t3 PARTITION p1 | PRIMARY_REGION="us-east-1" REGIONS="us-east-1,,us-west-1" FOLLOWERS=4 | INPROGRESS       |
+----------------------------+-----------------------------------------------------------------------+------------------+
1 row in set (0.00 sec)

+----------------------------+-------------+------------------+
| Target                     | Placement   | Scheduling_State |
+----------------------------+-------------+------------------+
| TABLE test.t3 PARTITION p2 | FOLLOWERS=4 | INPROGRESS       |
+----------------------------+-------------+------------------+
1 row in set (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL構文のTiDB拡張です。

## も参照してください {#see-also}

-   [SQLの配置ルール](/placement-rules-in-sql.md)
-   [配置を表示](/sql-statements/sql-statement-show-placement.md)
-   [プレースメントポリシーを作成する](/sql-statements/sql-statement-create-placement-policy.md)
