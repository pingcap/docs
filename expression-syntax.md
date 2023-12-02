---
title: Expression Syntax
summary: Learn about the expression syntax in TiDB.
---

# 式の構文 {#expression-syntax}

式は、1 つ以上の値、演算子、または関数の組み合わせです。 TiDB では、式は主に、Group by 句、Where 句、Having 句、Join 条件、ウィンドウ関数など、 `SELECT`ステートメントのさまざまな句で使用されます。さらに、一部の DDL ステートメントでは、テーブル作成時のデフォルト値、列、パーティション ルールの設定などの式も使用します。

式は次のタイプに分類できます。

-   識別子。参考までに[スキーマオブジェクト名](/schema-object-names.md)を参照してください。

-   述語、数値、文字列、日付式。これらのタイプの[リテラル値](/literal-values.md)も式です。

-   関数呼び出しとウィンドウ関数。参考までに、 [関数と演算子の概要](/functions-and-operators/functions-and-operators-overview.md)と[ウィンドウ関数](/functions-and-operators/window-functions.md)を参照してください。

-   ParamMarker ( `?` )、システム変数、ユーザー変数、および CASE 式。

次のルールは、TiDB パーサーの[parser.y](https://github.com/pingcap/parser/blob/master/parser.y)ルールに基づいた式の構文です。次の構文図のナビゲート可能なバージョンについては、 [TiDB SQL構文図](https://pingcap.github.io/sqlgram/#Expression)を参照してください。

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
|   ( ( '(' ( ExpressionList ',' )? | 'ROW' '(' ExpressionList ',' ) Expression | builtinCast '(' Expression 'AS' CastType | ( 'DEFAULT' | 'VALUES' ) '(' SimpleIdent | 'CONVERT' '(' Expression ( ',' CastType | 'USING' CharsetName ) ) ')'
|   'CASE' ExpressionOpt WhenClause+ ElseOpt 'END'
```
