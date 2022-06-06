---
title: SHOW PLACEMENT
summary: The usage of SHOW PLACEMENT in TiDB.
---

# 配置を表示 {#show-placement}

> **警告：**
>
> SQLの配置ルールは実験的機能です。 GAの前に構文が変更される可能性があり、バグもある可能性があります。
>
> リスクを理解している場合は、 `SET GLOBAL tidb_enable_alter_placement = 1;`を実行することでこの実験機能を有効にできます。

`SHOW PLACEMENT`は、直接配置および配置ポリシーからのすべての配置オプションを要約し、それらを標準形式で表示します。

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
CREATE TABLE t2 (a INT) PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4;
SHOW PLACEMENT;
```

```
Query OK, 0 rows affected (0.01 sec)

Query OK, 0 rows affected (0.00 sec)

Query OK, 0 rows affected (0.00 sec)

+---------------+----------------------------------------------------------------------+------------------+
| Target        | Placement                                                            | Scheduling_State |
+---------------+----------------------------------------------------------------------+------------------+
| POLICY p1     | PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4 | NULL             |
| DATABASE test | PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4 | INPROGRESS       |
| TABLE test.t1 | PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4 | INPROGRESS       |
| TABLE test.t2 | PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1" FOLLOWERS=4 | INPROGRESS       |
+---------------+----------------------------------------------------------------------+------------------+
4 rows in set (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL構文のTiDB拡張です。

## も参照してください {#see-also}

-   [SQLの配置ルール](/placement-rules-in-sql.md)
-   [の配置を表示](/sql-statements/sql-statement-show-placement-for.md)
-   [プレースメントポリシーを作成する](/sql-statements/sql-statement-create-placement-policy.md)
