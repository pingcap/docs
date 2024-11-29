---
title: DO | TiDB SQL Statement Reference
summary: TiDB データベースにおける DO の使用法の概要。
---

# する {#do}

`DO`式を実行しますが、結果は返しません。ほとんどの場合、 `DO`結果を返さない`SELECT expr, ...`と同等です。

> **注記：**
>
> `DO`式のみを実行します。2 `SELECT`使用できるすべてのケースで使用できるわけではありません。たとえば、 `DO id FROM t1`テーブルを参照するため無効です。

MySQL では、ストアド プロシージャまたはトリガーを実行するのが一般的な使用例です。TiDB はストアド プロシージャまたはトリガーを提供しないため、この機能の使用は制限されます。

## 概要 {#synopsis}

```ebnf+diagram
DoStmt   ::= 'DO' ExpressionList

ExpressionList ::=
    Expression ( ',' Expression )*

Expression ::=
    ( singleAtIdentifier assignmentEq | 'NOT' | Expression ( logOr | 'XOR' | logAnd ) ) Expression
|   'MATCH' '(' ColumnNameList ')' 'AGAINST' '(' BitExpr FulltextSearchModifierOpt ')'
|   PredicateExpr ( IsOrNotOp 'NULL' | CompareOp ( ( singleAtIdentifier assignmentEq )? PredicateExpr | AnyOrAll SubSelect ) )* ( IsOrNotOp ( trueKwd | falseKwd | 'UNKNOWN' ) )?
```

## 例 {#examples}

この SELECT ステートメントは一時停止しますが、結果セットも生成します。

```sql
mysql> SELECT SLEEP(5);
+----------+
| SLEEP(5) |
+----------+
|        0 |
+----------+
1 row in set (5.00 sec)
```

一方、DO は結果セットを生成せずに一時停止します。

```sql
mysql> DO SLEEP(5);
Query OK, 0 rows affected (5.00 sec)

mysql> DO SLEEP(1), SLEEP(1.5);
Query OK, 0 rows affected (2.50 sec)
```

## MySQL 互換性 {#mysql-compatibility}

TiDB の`DO`ステートメントは MySQL と完全に互換性があります。互換性の違いが見つかった場合は、 [バグを報告する](https://docs.pingcap.com/tidb/stable/support) 。

## 参照 {#see-also}

-   [選択](/sql-statements/sql-statement-select.md)
