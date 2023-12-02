---
title: SHOW PLACEMENT FOR
summary: The usage of SHOW PLACEMENT FOR in TiDB.
---

# のプレースメントを表示 {#show-placement-for}

`SHOW PLACEMENT FOR`すべての配置オプションを要約し、特定のテーブル、データベース スキーマ、またはパーティションの正規形式でそれらを示します。

> **注記：**
>
> この機能は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)クラスターでは使用できません。

このステートメントは、配置Driver(PD) による配置スケジュールの現在の進行状況を示す`Scheduling_State`フィールドを含む結果セットを返します。

-   `PENDING` : PD は配置のスケジュールをまだ開始していません。これは、配置ルールが意味的に正しいものの、現在クラスターが満たすことができないことを示している可能性があります。たとえば、 `FOLLOWERS=4`ある場合、フォロワーの候補となる TiKV 店舗が 3 つしかありません。
-   `INPROGRESS` : PD は現在配置をスケジュールしています。
-   `SCHEDULED` : PD は配置を正常にスケジュールしました。

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

```sql
CREATE PLACEMENT POLICY p1 PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4;
ALTER DATABASE test PLACEMENT POLICY=p1;
CREATE TABLE t1 (a INT);
SHOW PLACEMENT FOR DATABASE test;
SHOW PLACEMENT FOR TABLE t1;
SHOW CREATE TABLE t1\G;
CREATE TABLE t3 (a INT) PARTITION BY RANGE (a) (PARTITION p1 VALUES LESS THAN (10), PARTITION p2 VALUES LESS THAN (20));
SHOW PLACEMENT FOR TABLE t3 PARTITION p1\G;
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

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張機能です。

## こちらも参照 {#see-also}

-   [SQL の配置ルール](/placement-rules-in-sql.md)
-   [配置を表示](/sql-statements/sql-statement-show-placement.md)
-   [配置ポリシーの作成](/sql-statements/sql-statement-create-placement-policy.md)
