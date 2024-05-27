---
title: SHOW PLACEMENT LABELS
summary: TiDB での SHOW PLACEMENT LABELS の使用法。
---

# 配置ラベルを表示 {#show-placement-labels}

`SHOW PLACEMENT LABELS` 、配置ルールで使用できるラベルと値を要約するために使用されます。

> **注記：**
>
> この機能は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)クラスターでは使用できません。

## 概要 {#synopsis}

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

## MySQL 互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## 参照 {#see-also}

-   [SQL の配置ルール](/placement-rules-in-sql.md)
-   [表示配置](/sql-statements/sql-statement-show-placement.md)
-   [配置ポリシーの作成](/sql-statements/sql-statement-create-placement-policy.md)
