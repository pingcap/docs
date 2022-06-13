---
title: DO | TiDB SQL Statement Reference
summary: An overview of the usage of DO for the TiDB database.
---

# 行う {#do}

`DO`は式を実行しますが、結果を返しません。ほとんどの場合、 `DO`は結果を返さない`SELECT expr, ...`と同等です。

> **ノート：**
>
> `DO`は式のみを実行します。 `SELECT`が使用できるすべての場合に使用できるわけではありません。たとえば、 `DO id FROM t1`はテーブルを参照しているため、無効です。

MySQLでは、一般的なユースケースはストアドプロシージャまたはトリガーを実行することです。 TiDBはストアドプロシージャまたはトリガーを提供しないため、この関数の使用は制限されています。

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

このSELECTステートメントは一時停止しますが、結果セットも生成します。

```sql
mysql> SELECT SLEEP(5);
+----------+
| SLEEP(5) |
+----------+
|        0 |
+----------+
1 row in set (5.00 sec)
```

一方、DOは、結果セットを生成せずに一時停止します。

```sql
mysql> DO SLEEP(5);
Query OK, 0 rows affected (5.00 sec)

mysql> DO SLEEP(1), SLEEP(1.5);
Query OK, 0 rows affected (2.50 sec)
```

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQLと完全に互換性があると理解されています。互換性の違いは、GitHubでは[問題を介して報告](https://github.com/pingcap/tidb/issues/new/choose)である必要があります。

## も参照してください {#see-also}

-   [選択する](/sql-statements/sql-statement-select.md)
