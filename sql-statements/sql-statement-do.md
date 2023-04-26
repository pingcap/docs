---
title: DO | TiDB SQL Statement Reference
summary: An overview of the usage of DO for the TiDB database.
---

# する {#do}

`DO`式を実行しますが、結果を返しません。ほとんどの場合、 `DO`結果を返さない`SELECT expr, ...`に相当します。

> **ノート：**
>
> `DO`は式のみを実行します。 `SELECT`使用できるすべての場合に使用できるわけではありません。たとえば、 `DO id FROM t1`はテーブルを参照しているため無効です。

MySQL での一般的な使用例は、ストアド プロシージャまたはトリガーを実行することです。 TiDB はストアド プロシージャまたはトリガーを提供しないため、この関数の用途は限られています。

## あらすじ {#synopsis}

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

## MySQL の互換性 {#mysql-compatibility}

このステートメントは、MySQL と完全に互換性があると理解されています。互換性の違いは、GitHub で[問題を介して報告された](https://github.com/pingcap/tidb/issues/new/choose)にする必要があります。

## こちらもご覧ください {#see-also}

-   [選択する](/sql-statements/sql-statement-select.md)
