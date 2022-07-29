---
title: WITH | TiDB SQL Statement Reference
summary: An overview of the usage of WITH (Common Table Expression) for the TiDB database.
---

# と {#with}

共通テーブル式（CTE）は、SQLステートメント内で複数回参照して、ステートメントの可読性と実行効率を向上させることができる一時的な結果セットです。 `WITH`ステートメントを適用して、共通テーブル式を使用できます。

## あらすじ {#synopsis}

**WithClause：**

```ebnf+diagram
WithClause ::=
        "WITH" WithList
|       "WITH" recursive WithList
```

**WithList：**

```ebnf+diagram
WithList ::=
        WithList ',' CommonTableExpr
|       CommonTableExpr
```

**CommonTableExpr：**

```ebnf+diagram
CommonTableExpr ::=
        Identifier IdentListWithParenOpt "AS" SubSelect
```

**IdentListWithParenOpt：**

```ebnf+diagram
IdentListWithParenOpt ::=
( '(' IdentList ')' )?
```

## 例 {#examples}

非再帰CTE：

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

再帰CTE：

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

## MySQLの互換性 {#mysql-compatibility}

-   strictモードでは、再帰的に計算されたデータ長がシード部分のデータ長を超えると、TiDBは警告を返し、MySQLはエラーを返します。非厳密モードでは、TiDBの動作はMySQLの動作と一致しています。
-   再帰CTEのデータ型は、シード部分によって決定されます。シード部分のデータ型は、場合によってはMySQLと完全に一致していません（関数など）。
-   複数の`UNION`演算子の場合、MySQLでは`UNION ALL`の後に`UNION`を続けることはできませんが、 `UNION ALL`では許可されています。
-   CTEの定義に問題がある場合、TiDBはエラーを報告しますが、CTEが参照されていない場合はMySQLは報告しません。

## も参照してください {#see-also}

-   [選択する](/sql-statements/sql-statement-select.md)
-   [入れる](/sql-statements/sql-statement-insert.md)
-   [消去](/sql-statements/sql-statement-delete.md)
-   [アップデート](/sql-statements/sql-statement-update.md)
-   [交換](/sql-statements/sql-statement-replace.md)
