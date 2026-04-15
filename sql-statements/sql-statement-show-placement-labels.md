---
title: SHOW PLACEMENT LABELS
summary: TiDBにおけるSHOW PLACEMENT LABELSの使用方法。
---

# 配置ラベルを表示する {#show-placement-labels}

`SHOW PLACEMENT LABELS`配置ルールで使用可能なラベルと値を要約するために使用されます。

> **注記：**
>
> この機能は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)インスタンスではご利用いただけません。

## あらすじ {#synopsis}

```ebnf+diagram
ShowStmt ::=
    "SHOW" "PLACEMENT" "LABELS" ShowLikeOrWhere?
```

## 例 {#examples}

```sql
SHOW PLACEMENT LABELS;
```

    +--------+----------------+
    | Key    | Values         |
    +--------+----------------+
    | region | ["us-east-1"]  |
    | zone   | ["us-east-1a"] |
    +--------+----------------+
    2 rows in set (0.00 sec)

## MySQLとの互換性 {#mysql-compatibility}

このステートメントは、MySQL構文に対するTiDBの拡張機能です。

## 関連項目 {#see-also}

-   [SQLにおける配置ルール](/placement-rules-in-sql.md)
-   [番組掲載](/sql-statements/sql-statement-show-placement.md)
-   [配置ポリシーを作成する](/sql-statements/sql-statement-create-placement-policy.md)
