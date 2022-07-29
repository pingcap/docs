---
title: SHOW PLACEMENT
summary: The usage of SHOW PLACEMENT in TiDB.
---

# 配置を表示 {#show-placement}

`SHOW PLACEMENT`は、配置ポリシーのすべての配置オプションを要約し、それらを標準形式で表示します。

このステートメントは、配置Driver（PD）が配置のスケジューリングで行った現在の進行状況を`Scheduling_State`フィールドが示す結果セットを返します。

-   `PENDING` ：PDはまだ配置のスケジュールを開始していません。これは、配置ルールが意味的に正しいが、現在クラスタが満たすことができないことを示している可能性があります。たとえば、フォロワーの候補となるTiKVストアが`FOLLOWERS=4`あるが、3つしかない場合です。
-   `INPROGRESS` ：PDは現在配置をスケジュールしています。
-   `SCHEDULED` ：PDは配置を正常にスケジュールしました。

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

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL構文のTiDB拡張です。

## も参照してください {#see-also}

-   [SQLでの配置ルール](/placement-rules-in-sql.md)
-   [の配置を表示](/sql-statements/sql-statement-show-placement-for.md)
-   [プレースメントポリシーを作成する](/sql-statements/sql-statement-create-placement-policy.md)
