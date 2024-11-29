---
title: WITH | TiDB SQL Statement Reference
summary: TiDB データベースの WITH (共通テーブル式) の使用法の概要。
---

# と {#with}

共通テーブル式 (CTE) は、SQL ステートメント内で複数回参照できる一時的な結果セットであり、ステートメントの可読性と実行効率を向上させます。共通テーブル式を使用するには、 `WITH`ステートメントを適用できます。

## 概要 {#synopsis}

**句:**

```ebnf+diagram
WithClause ::=
        "WITH" WithList
|       "WITH" "RECURSIVE" WithList
```

**リスト付き:**

```ebnf+diagram
WithList ::=
        WithList ',' CommonTableExpr
|       CommonTableExpr
```

**共通テーブル表現:**

```ebnf+diagram
CommonTableExpr ::=
        Identifier IdentListWithParenOpt "AS" SubSelect
```

**親オプション付き識別子リスト:**

```ebnf+diagram
IdentListWithParenOpt ::=
( '(' IdentList ')' )?
```

## 例 {#examples}

非再帰CTE:

```sql
WITH cte AS (SELECT 1, 2) SELECT * FROM cte t1, cte t2;
```

    +---+---+---+---+
    | 1 | 2 | 1 | 2 |
    +---+---+---+---+
    | 1 | 2 | 1 | 2 |
    +---+---+---+---+
    1 row in set (0.00 sec)

再帰CTE:

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

## MySQL 互換性 {#mysql-compatibility}

-   厳密モードでは、再帰的に計算されたデータ長がシード部分のデータ長を超えると、TiDB は警告を返し、MySQL はエラーを返します。非厳密モードでは、TiDB の動作は MySQL の動作と一致します。
-   再帰 CTE のデータ型はシード部分によって決まります。シード部分のデータ型は、場合によっては MySQL と完全に一致しません (関数など)。
-   `UNION` / `UNION ALL`演算子が複数ある場合、MySQL では`UNION`の後に`UNION ALL`を続けることはできませんが、TiDB では可能です。
-   CTE の定義に問題がある場合、TiDB はエラーを報告しますが、CTE が参照されていない場合、MySQL はエラーを報告しません。

## 参照 {#see-also}

-   [開発者ガイド: 共通テーブル式](/develop/dev-guide-use-common-table-expression.md)
-   [選択](/sql-statements/sql-statement-select.md)
-   [入れる](/sql-statements/sql-statement-insert.md)
-   [消去](/sql-statements/sql-statement-delete.md)
-   [アップデート](/sql-statements/sql-statement-update.md)
-   [交換する](/sql-statements/sql-statement-replace.md)
