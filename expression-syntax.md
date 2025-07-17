---
title: 表达式语法
summary: 了解 TiDB 中的表达式语法。
---

# 表达式语法

表达式是由一个或多个值、运算符或函数组成的组合。在 TiDB 中，表达式主要用于 `SELECT` 语句的各种子句中，包括 Group by 子句、Where 子句、Having 子句、Join 条件和窗口函数。此外，一些 DDL 语句也会使用表达式，例如在创建表时设置默认值、列和分区规则。

表达式可以分为以下几类：

- 标识符。有关参考内容，请参见 [Schema object names](/schema-object-names.md)。

- 谓词、数值、字符串、日期表达式。这些类型的 [Literal values](/literal-values.md) 也是表达式。

- 函数调用和窗口函数。有关参考内容，请参见 [Functions and operators overview](/functions-and-operators/functions-and-operators-overview.md) 和 [Window functions](/functions-and-operators/window-functions.md)

- ParamMarker (`?`)、系统变量、用户变量和 CASE 表达式。

以下是基于 TiDB 解析器的 [`parser.y`](https://github.com/pingcap/tidb/blob/release-8.5/pkg/parser/parser.y) 规则的表达式语法规则。

```ebnf+diagram
Expression ::=
    ( singleAtIdentifier assignmentEq | 'NOT' | Expression ( logOr | 'XOR' | logAnd ) ) Expression
|   'MATCH' '(' ColumnNameList ')' 'AGAINST' '(' BitExpr FulltextSearchModifierOpt ')'
|   PredicateExpr ( IsOrNotOp 'NULL' | CompareOp ( ( singleAtIdentifier assignmentEq )? PredicateExpr | AnyOrAll SubSelect ) )* ( IsOrNotOp ( trueKwd | falseKwd | 'UNKNOWN' ) )?

PredicateExpr ::=
    BitExpr ( BetweenOrNotOp BitExpr 'AND' BitExpr )* ( InOrNotOp ( '(' ExpressionList ')' | SubSelect ) | LikeOrNotOp SimpleExpr LikeEscapeOpt | RegexpOrNotOp SimpleExpr )?

BitExpr ::=
    BitExpr ( ( '|' | '&' | '<<' | '>>' | '*' | '/' | '%' | 'DIV' | 'MOD' | '^' ) BitExpr | ( '+' | '-' ) ( BitExpr | "INTERVAL" Expression TimeUnit ) )
|   SimpleExpr

SimpleExpr ::=
    SimpleIdent ( ( '->' | '->>' ) stringLit )?
|   FunctionCallKeyword
|   FunctionCallNonKeyword
|   FunctionCallGeneric
|   SimpleExpr ( 'COLLATE' CollationName | pipes SimpleExpr )
|   WindowFuncCall
|   Literal
|   paramMarker
|   Variable
|   SumExpr
|   ( '!' | '~' | '-' | '+' | 'NOT' | 'BINARY' ) SimpleExpr
|   'EXISTS'? SubSelect
|   ( ( '(' ( ExpressionList ',' )? | 'ROW' '(' ExpressionList ',' ) Expression | builtinCast '(' Expression 'AS' CastType | ( 'DEFAULT' | 'VALUES' ) '(' SimpleIdent | 'CONVERT' '(' Expression ( ',' CastType | 'USING' CharsetName ) ) '
|   'CASE' ExpressionOpt WhenClause+ ElseOpt 'END'
```