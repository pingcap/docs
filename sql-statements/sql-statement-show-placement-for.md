---
title: SHOW PLACEMENT FOR
summary: TiDB における SHOW PLACEMENT FOR の使用方法。
---

# ショーの掲載場所 {#show-placement-for}

`SHOW PLACEMENT FOR` 、すべての配置オプションを要約し、特定のテーブル、データベーススキーマ、またはパーティションに対して正規の形式で表示します。

> **注記：**
>
> この機能は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)インスタンスではご利用いただけません。

このステートメントは`Scheduling_State`フィールドが配置Driver(PD) が配置スケジュールに関して現在行っている進捗状況を示す結果セットを返します。

-   `PENDING` : PD はまだ配置のスケジュールを開始していません。これは、配置ルールが意味的には正しいものの、現在のところクラスタで満たすことができないことを示している可能性があります。たとえば、 `FOLLOWERS=4`ですが、フォロワー候補となる TiKV ストアが 3 つしかない場合などです。
-   `INPROGRESS` : PD は現在配置のスケジュールを調整中です。
-   `SCHEDULED` : PD は配置を正常にスケジュールしました。

## あらすじ {#synopsis}

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
      `a` int DEFAULT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin /*T![placement] PLACEMENT POLICY=`p1` */
    1 row in set (0.00 sec)

    ***************************[ 1. row ]***************************
    Target           | TABLE test.t3 PARTITION p1
    Placement        | PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4
    Scheduling_State | PENDING
    1 row in set (0.00 sec)

## MySQLとの互換性 {#mysql-compatibility}

このステートメントは、MySQL構文に対するTiDBの拡張機能です。

## 関連項目 {#see-also}

-   [SQLにおける配置ルール](/placement-rules-in-sql.md)
-   [番組掲載](/sql-statements/sql-statement-show-placement.md)
-   [配置ポリシーを作成する](/sql-statements/sql-statement-create-placement-policy.md)
