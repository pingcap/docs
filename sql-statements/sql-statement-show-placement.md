---
title: SHOW PLACEMENT
summary: The usage of SHOW PLACEMENT in TiDB.
---

# 配置を表示 {#show-placement}

`SHOW PLACEMENT`配置ポリシーからのすべての配置オプションを要約し、正規形式で表示します。

> **注記：**
>
> この機能は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)クラスターでは使用できません。

このステートメントは、配置Driver(PD) による配置スケジュールの現在の進行状況を示す`Scheduling_State`フィールドを含む結果セットを返します。

-   `PENDING` : PD は配置のスケジュールをまだ開始していません。これは、配置ルールが意味的に正しいものの、現在クラスターが満たすことができないことを示している可能性があります。たとえば、 `FOLLOWERS=4`である場合、フォロワーの候補となる TiKV ストアは 3 つしかありません。
-   `INPROGRESS` : PD は現在配置をスケジュールしています。
-   `SCHEDULED` : PD は配置を正常にスケジュールしました。

## あらすじ {#synopsis}

```ebnf+diagram
ShowStmt ::=
    "PLACEMENT"
```

## 例 {#examples}

```sql
CREATE PLACEMENT POLICY p1 PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4;
CREATE TABLE t1 (a INT) PLACEMENT POLICY=p1;
SHOW PLACEMENT;
```

    Query OK, 0 rows affected (0.01 sec)

    Query OK, 0 rows affected (0.00 sec)

    +---------------+----------------------------------------------------------------------+------------------+
    | Target        | Placement                                                            | Scheduling_State |
    +---------------+----------------------------------------------------------------------+------------------+
    | POLICY p1     | PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4 | NULL             |
    | DATABASE test | PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4 | INPROGRESS       |
    | TABLE test.t1 | PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4 | INPROGRESS       |
    +---------------+----------------------------------------------------------------------+------------------+
    4 rows in set (0.00 sec)

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張機能です。

## こちらも参照 {#see-also}

-   [SQL の配置ルール](/placement-rules-in-sql.md)
-   [のプレースメントを表示](/sql-statements/sql-statement-show-placement-for.md)
-   [配置ポリシーの作成](/sql-statements/sql-statement-create-placement-policy.md)
