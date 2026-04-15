---
title: SHOW PLACEMENT
summary: TiDBにおけるSHOW PLACEMENTの使用方法。
---

# 番組掲載 {#show-placement}

`SHOW PLACEMENT`配置ポリシーからのすべての配置オプションを要約し、正規の形式で表示します。

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

## MySQLとの互換性 {#mysql-compatibility}

このステートメントは、MySQL構文に対するTiDBの拡張機能です。

## 関連項目 {#see-also}

-   [SQLにおける配置ルール](/placement-rules-in-sql.md)
-   [ショーの掲載場所](/sql-statements/sql-statement-show-placement-for.md)
-   [配置ポリシーを作成する](/sql-statements/sql-statement-create-placement-policy.md)
