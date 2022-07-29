---
title: Expression Syntax
summary: Learn about the expression syntax in TiDB.
---

# 式の構文 {#expression-syntax}

式は、1つ以上の値、演算子、または関数の組み合わせです。 TiDBでは、式は主に`SELECT`ステートメントのさまざまな句で使用されます。これには、Group by句、Where句、Having句、Join条件、ウィンドウ関数が含まれます。さらに、一部のDDLステートメントでは、テーブルの作成時にデフォルト値、列、パーティションルールの設定などの式も使用されます。

式は次のタイプに分けることができます。

-   識別子。参考までに、 [スキーマオブジェクト名](/schema-object-names.md)を参照してください。

-   述語、数値、文字列、日付式。これらのタイプの[リテラル値](/literal-values.md)つも式です。

-   関数呼び出しとウィンドウ関数。参考までに、 [関数と演算子の概要](/functions-and-operators/functions-and-operators-overview.md)と[ウィンドウ関数](/functions-and-operators/window-functions.md)を参照してください

-   ParamMarker（ `?` ）、システム変数、ユーザー変数、およびCASE式。

次のルールは、TiDBパーサーの[parser.y](https://github.com/pingcap/parser/blob/master/parser.y)のルールに基づく式の構文です。次のシンタックスダイアグラムのナビゲート可能なバージョンについては、 [TiDB SQL構文図](https://pingcap.github.io/sqlgram/#Expression)を参照してください。

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
