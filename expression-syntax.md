---
title: Expression Syntax
summary: TiDB の式構文について学習します。
---

# 式の構文 {#expression-syntax}

式とは、1つ以上の値、演算子、または関数の組み合わせです。TiDBでは、式は主に`SELECT`文の様々な句、例えばGroup by句、Where句、Having句、結合条件、ウィンドウ関数などで使用されます。また、テーブル作成時のデフォルト値、列、パーティションルールの設定など、一部のDDL文でも式が使用されます。

表現は次の種類に分けられます。

-   識別子。参考として[スキーマオブジェクト名](/schema-object-names.md)参照してください。

-   述語、数値、文字列、日付式。これらのうち[リテラル値](/literal-values.md)式です。

-   関数呼び出しとウィンドウ関数。参考までに[関数と演算子の概要](/functions-and-operators/functions-and-operators-overview.md)と[ウィンドウ関数](/functions-and-operators/window-functions.md)参照。

-   ParamMarker( `?` )、システム変数、ユーザー変数、CASE式。

以下の規則は、TiDB パーサーの[`parser.y`](https://github.com/pingcap/tidb/blob/release-8.5/pkg/parser/parser.y)規則に基づいた式構文です。

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
