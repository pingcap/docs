---
title: WITH | TiDB SQL Statement Reference
summary: An overview of the usage of WITH (Common Table Expression) for the TiDB database.
---

# と {#with}

共通テーブル式 (CTE) は、ステートメントの読みやすさと実行効率を向上させるために、SQL ステートメント内で複数回参照できる一時的な結果セットです。 `WITH`ステートメントを適用して、共通テーブル式を使用できます。

## あらすじ {#synopsis}

**With句:**

```ebnf+diagram
WithClause ::=
        "WITH" WithList
|       "WITH" recursive WithList
```

**リストあり:**

```ebnf+diagram
WithList ::=
        WithList ',' CommonTableExpr
|       CommonTableExpr
```

**CommonTableExpr:**

```ebnf+diagram
CommonTableExpr ::=
        Identifier IdentListWithParenOpt "AS" SubSelect
```

**IdentListWithParenOpt:**

```ebnf+diagram
IdentListWithParenOpt ::=
( '(' IdentList ')' )?
```

## 例 {#examples}

非再帰 CTE:

{{< copyable "" >}}

```sql
WITH CTE AS (SELECT 1, 2) SELECT * FROM cte t1, cte t2;
```

```
+---+---+---+---+
| 1 | 2 | 1 | 2 |
+---+---+---+---+
| 1 | 2 | 1 | 2 |
+---+---+---+---+
1 row in set (0.00 sec)
```

再帰的 CTE:

{{< copyable "" >}}

```sql
WITH RECURSIVE cte(a) AS (SELECT 1 UNION SELECT a+1 FROM cte WHERE a < 5) SELECT * FROM cte;
```

```
+---+
| a |
+---+
| 1 |
| 2 |
| 3 |
| 4 |
| 5 |
+---+
5 rows in set (0.00 sec)
```

## MySQL の互換性 {#mysql-compatibility}

-   厳密モードでは、再帰的に計算されたデータ長がシード部分のデータ長を超えると、TiDB は警告を返しますが、MySQL はエラーを返します。非厳密モードでは、TiDB の動作は MySQL の動作と一致します。
-   再帰 CTE のデータ型は、シード部分によって決まります。シード部分のデータ型は、MySQL と完全に一致しない場合があります (関数など)。
-   複数の`UNION` / `UNION ALL`演算子の場合、MySQL は`UNION`後に`UNION ALL`が続くことを許可しませんが、TiDB は許可します。
-   CTE の定義に問題がある場合、TiDB はエラーを報告しますが、CTE が参照されていない場合、MySQL はエラーを報告しません。

## こちらもご覧ください {#see-also}

-   [選択する](/sql-statements/sql-statement-select.md)
-   [入れる](/sql-statements/sql-statement-insert.md)
-   [消去](/sql-statements/sql-statement-delete.md)
-   [アップデート](/sql-statements/sql-statement-update.md)
-   [交換](/sql-statements/sql-statement-replace.md)
