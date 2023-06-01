---
title: SHOW PLACEMENT LABELS
summary: The usage of SHOW PLACEMENT LABELS in TiDB.
---

# 配置ラベルを表示 {#show-placement-labels}

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

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張機能です。

## こちらも参照 {#see-also}

-   [<a href="/placement-rules-in-sql.md">SQL の配置ルール</a>](/placement-rules-in-sql.md)
-   [<a href="/sql-statements/sql-statement-show-placement.md">配置を表示</a>](/sql-statements/sql-statement-show-placement.md)
-   [<a href="/sql-statements/sql-statement-create-placement-policy.md">配置ポリシーの作成</a>](/sql-statements/sql-statement-create-placement-policy.md)
