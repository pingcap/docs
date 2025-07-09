---
title: SHOW PLACEMENT
summary: TiDB での SHOW PLACEMENT の使用法。
---

# 表示配置 {#show-placement}

`SHOW PLACEMENT` 、配置ポリシーからのすべての配置オプションを要約し、標準形式で提示します。

> **注記：**
>
> この機能は[{{{ .スターター }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)クラスターでは利用できません。

このステートメントは、配置Driver(PD) が配置のスケジュールで行った現在の進行状況を示す`Scheduling_State`フィールドを含む結果セットを返します。

-   `PENDING` : PDはまだ配置のスケジュールを開始していません。これは、配置ルールは意味的には正しいものの、クラスターが現在そのルールを満たしていないことを示している可能性があります。例えば、配置ルール`FOLLOWERS=4`あるにもかかわらず、フォロワー候補となるTiKVストアが3つしかない場合などです。
-   `INPROGRESS` : PD が現在配置をスケジュール中です。
-   `SCHEDULED` : PD は配置を正常にスケジュールしました。

## 概要 {#synopsis}

```ebnf+diagram
ShowStmt ::=
    "SHOW" "PLACEMENT" ShowLikeOrWhere?
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

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## 参照 {#see-also}

-   [SQLの配置ルール](/placement-rules-in-sql.md)
-   [表示配置](/sql-statements/sql-statement-show-placement-for.md)
-   [配置ポリシーの作成](/sql-statements/sql-statement-create-placement-policy.md)
