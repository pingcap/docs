---
title: SHOW PLACEMENT
summary: The usage of SHOW PLACEMENT in TiDB.
---

# 配置を表示 {#show-placement}

`SHOW PLACEMENT`配置ポリシーからのすべての配置オプションを要約し、標準形式で表示します。

このステートメントは、配置Driver(PD) が配置のスケジューリングで行った現在の進行状況を`Scheduling_State`フィールドが示す結果セットを返します。

-   `PENDING` : PD はまだプレースメントのスケジューリングを開始していません。これは、配置ルールが意味的に正しいことを示している可能性がありますが、現在クラスターが満たすことはできません。例えば、 `FOLLOWERS=4`つでもフォロワー候補のTiKV店舗が3つしかない場合。
-   `INPROGRESS` : PD は現在配置をスケジュールしています。
-   `SCHEDULED` : PD は配置を正常にスケジュールしました。

## あらすじ {#synopsis}

```ebnf+diagram
ShowStmt ::=
    "PLACEMENT"
```

## 例 {#examples}

{{< copyable "" >}}

```sql
CREATE PLACEMENT POLICY p1 PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4;
CREATE TABLE t1 (a INT) PLACEMENT POLICY=p1;
SHOW PLACEMENT;
```

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
```

## MySQL の互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## こちらもご覧ください {#see-also}

-   [SQL の配置規則](/placement-rules-in-sql.md)
-   [のプレースメントを表示](/sql-statements/sql-statement-show-placement-for.md)
-   [配置ポリシーを作成する](/sql-statements/sql-statement-create-placement-policy.md)
