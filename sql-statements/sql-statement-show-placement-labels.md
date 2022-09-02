---
title: SHOW PLACEMENT LABELS
summary: The usage of SHOW PLACEMENT LABELS in TiDB.
---

# プレースメント ラベルを表示 {#show-placement-labels}

`SHOW PLACEMENT LABELS`は、配置ルールで使用できるラベルと値を要約するために使用されます。

## あらすじ {#synopsis}

```ebnf+diagram
ShowStmt ::=
    "PLACEMENT" "LABELS"
```

## 例 {#examples}

{{< copyable "" >}}

```sql
SHOW PLACEMENT LABELS;
```

```
+--------+----------------+
| Key    | Values         |
+--------+----------------+
| region | ["us-east-1"]  |
| zone   | ["us-east-1a"] |
+--------+----------------+
2 rows in set (0.00 sec)
```

## MySQL の互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## こちらもご覧ください {#see-also}

-   [SQL の配置規則](/placement-rules-in-sql.md)
-   [配置を表示](/sql-statements/sql-statement-show-placement.md)
-   [配置ポリシーを作成する](/sql-statements/sql-statement-create-placement-policy.md)
