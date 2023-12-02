---
title: SHOW PLACEMENT LABELS
summary: The usage of SHOW PLACEMENT LABELS in TiDB.
---

# 配置ラベルを表示 {#show-placement-labels}

`SHOW PLACEMENT LABELS`は、配置ルールで使用できるラベルと値を要約するために使用されます。

> **注記：**
>
> この機能は[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)クラスターでは使用できません。

## あらすじ {#synopsis}

```ebnf+diagram
ShowStmt ::=
    "PLACEMENT" "LABELS"
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

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張機能です。

## こちらも参照 {#see-also}

-   [SQL の配置ルール](/placement-rules-in-sql.md)
-   [配置を表示](/sql-statements/sql-statement-show-placement.md)
-   [配置ポリシーの作成](/sql-statements/sql-statement-create-placement-policy.md)
