---
title: SHOW PLACEMENT LABELS
summary: The usage of SHOW PLACEMENT LABELS in TiDB.
---

# 配置ラベルを表示する {#show-placement-labels}

> **警告：**
>
> SQLの配置ルールは実験的機能です。 GAの前に構文が変更される可能性があり、バグもある可能性があります。
>
> リスクを理解している場合は、 `SET GLOBAL tidb_enable_alter_placement = 1;`を実行することでこの実験機能を有効にできます。

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

このステートメントは、MySQL構文のTiDB拡張です。

## も参照してください {#see-also}

-   [SQLの配置ルール](/placement-rules-in-sql.md)
-   [配置を表示](/sql-statements/sql-statement-show-placement.md)
-   [プレースメントポリシーを作成する](/sql-statements/sql-statement-create-placement-policy.md)
