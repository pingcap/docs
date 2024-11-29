---
title: Expression Syntax
summary: TiDB の式構文について学習します。
---

# 式の構文 {#expression-syntax}

式は、1 つ以上の値、演算子、または関数の組み合わせです。TiDB では、式は主に、Group by 句、Where 句、Having 句、結合条件、ウィンドウ関数など、 `SELECT`ステートメントのさまざまな句で使用されます。また、テーブルを作成するときにデフォルト値、列、パーティション ルールを設定するなど、一部の DDL ステートメントでも式が使用されます。

表現は以下の種類に分けられます。

-   識別子。参考については[スキーマオブジェクト名](/schema-object-names.md)参照してください。

-   述語、数値、文字列、日付式。これらのタイプのうち[リテラル値](/literal-values.md)つも式です。

-   関数呼び出しとウィンドウ関数。参考までに[関数と演算子の概要](/functions-and-operators/functions-and-operators-overview.md)と[ウィンドウ関数](/functions-and-operators/window-functions.md)参照

-   ParamMarker（ `?` ）、システム変数、ユーザー変数、CASE式。

以下のルールは、TiDB パーサーの[`parser.y`](https://github.com/pingcap/tidb/blob/release-8.1/pkg/parser/parser.y)ルールに基づいた式構文です。

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
