---
title: SHOW PLACEMENT FOR
summary: TiDB での SHOW PLACEMENT FOR の使用法。
---

# 表示配置 {#show-placement-for}

`SHOW PLACEMENT FOR` 、すべての配置オプションを要約し、特定のテーブル、データベース スキーマ、またはパーティションの標準形式で提示します。

> **注記：**
>
> この機能は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)クラスターでは使用できません。

このステートメントは、配置Driver(PD) が配置のスケジュールで行った現在の進行状況を示す`Scheduling_State`フィールドを含む結果セットを返します。

-   `PENDING` : PD はまだ配置のスケジュールを開始していません。これは、配置ルールが意味的には正しいが、現在クラスターによって満たされないことを示している可能性があります。たとえば、 `FOLLOWERS=4`場合、フォロワーの候補となる TiKV ストアは 3 つしかありません。
-   `INPROGRESS` : PD が現在配置をスケジュール中です。
-   `SCHEDULED` : PD は配置を正常にスケジュールしました。

## 概要 {#synopsis}

```ebnf+diagram
ShowStmt ::=
    "SHOW" "PLACEMENT" "FOR" ShowPlacementTarget

ShowPlacementTarget ::=
    DatabaseSym DBName
|   "TABLE" TableName
|   "TABLE" TableName "PARTITION" Identifier
```

## 例 {#examples}

```sql
CREATE PLACEMENT POLICY p1 PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4;
ALTER DATABASE test PLACEMENT POLICY=p1;
CREATE TABLE t1 (a INT);
SHOW PLACEMENT FOR DATABASE test;
SHOW PLACEMENT FOR TABLE t1;
SHOW CREATE TABLE t1\G
CREATE TABLE t3 (a INT) PARTITION BY RANGE (a) (PARTITION p1 VALUES LESS THAN (10), PARTITION p2 VALUES LESS THAN (20));
SHOW PLACEMENT FOR TABLE t3 PARTITION p1\G
```

    Query OK, 0 rows affected (0.02 sec)

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

    ***************************[ 1. row ]***************************
    Table        | t1
    Create Table | CREATE TABLE `t1` (
      `a` int(11) DEFAULT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin /*T![placement] PLACEMENT POLICY=`p1` */
    1 row in set (0.00 sec)

    ***************************[ 1. row ]***************************
    Target           | TABLE test.t3 PARTITION p1
    Placement        | PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4
    Scheduling_State | PENDING
    1 row in set (0.00 sec)

## MySQL 互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## 参照 {#see-also}

-   [SQL の配置ルール](/placement-rules-in-sql.md)
-   [表示配置](/sql-statements/sql-statement-show-placement.md)
-   [配置ポリシーの作成](/sql-statements/sql-statement-create-placement-policy.md)
