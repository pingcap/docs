---
title: WITH | TiDB SQL Statement Reference
summary: TiDB データベースの WITH (共通テーブル式) の使用法の概要。
---

# と {#with}

共通テーブル式（CTE）は、SQL文内で複数回参照できる一時的な結果セットであり、文の可読性と実行効率を向上させます。共通テーブル式を使用するには、 `WITH`文を適用します。

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

**共通テーブル式:**

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

## MySQLの互換性 {#mysql-compatibility}

-   厳密モードでは、再帰的に計算されたデータ長がシード部分のデータ長を超えると、TiDBは警告を返し、MySQLはエラーを返します。非厳密モードでは、TiDBの動作はMySQLの動作と一致します。
-   再帰CTEのデータ型はシード部によって決定されます。シード部のデータ型は、場合によってはMySQLと完全に一致しないことがあります（関数など）。
-   複数の`UNION` / `UNION ALL`演算子の場合、MySQL では`UNION`後に`UNION ALL`続くことは許可されませんが、TiDB では許可されます。
-   CTE の定義に問題がある場合、TiDB はエラーを報告しますが、MySQL は CTE が参照されていない場合はエラーを報告しません。

## 参照 {#see-also}

-   [開発者ガイド: 共通テーブル式](/develop/dev-guide-use-common-table-expression.md)
-   [選択](/sql-statements/sql-statement-select.md)
-   [入れる](/sql-statements/sql-statement-insert.md)
-   [消去](/sql-statements/sql-statement-delete.md)
-   [アップデート](/sql-statements/sql-statement-update.md)
-   [交換する](/sql-statements/sql-statement-replace.md)
