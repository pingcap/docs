---
title: WITH | TiDB SQL Statement Reference
summary: An overview of the usage of WITH (Common Table Expression) for the TiDB database.
---

# と {#with}

共通テーブル式 (CTE) は、SQL ステートメント内で複数回参照できる一時的な結果セットで、ステートメントの可読性と実行効率を向上させます。 `WITH`ステートメントを適用して共通テーブル式を使用できます。

## あらすじ {#synopsis}

**句あり:**

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

非再帰的 CTE:

```sql
WITH CTE AS (SELECT 1, 2) SELECT * FROM cte t1, cte t2;
```

    +---+---+---+---+
    | 1 | 2 | 1 | 2 |
    +---+---+---+---+
    | 1 | 2 | 1 | 2 |
    +---+---+---+---+
    1 row in set (0.00 sec)

再帰的 CTE:

```sql
WITH RECURSIVE cte(a) AS (SELECT 1 UNION SELECT a+1 FROM cte WHERE a < 5) SELECT * FROM cte;
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

## MySQLの互換性 {#mysql-compatibility}

-   strict モードでは、再帰的に計算されたデータ長がシード部分のデータ長を超えると、TiDB は警告を返しますが、MySQL はエラーを返します。非厳密モードでは、TiDB の動作は MySQL の動作と一致します。
-   再帰的 CTE のデータ型はシード部分によって決定されます。シード部分のデータ型は、MySQL と完全に一致していない場合があります (関数など)。
-   複数の`UNION` / `UNION ALL`演算子の場合、MySQL では`UNION`後に`UNION ALL`を続けることは許可されませんが、TiDB では許可されます。
-   CTE の定義に問題がある場合、TiDB はエラーを報告しますが、MySQL は CTE が参照されていない場合はエラーを報告しません。

## こちらも参照 {#see-also}

-   [選択する](/sql-statements/sql-statement-select.md)
-   [入れる](/sql-statements/sql-statement-insert.md)
-   [消去](/sql-statements/sql-statement-delete.md)
-   [アップデート](/sql-statements/sql-statement-update.md)
-   [交換する](/sql-statements/sql-statement-replace.md)
