---
title: Expression Syntax
summary: Learn about the expression syntax in TiDB.
aliases: ['/docs/v3.1/expression-syntax/','/docs/v3.1/reference/sql/language-structure/expression-syntax/']
---

# Expression Syntax

<<<<<<< HEAD
The following rules define the expression syntax in TiDB. You can find the definition in `parser/parser.y`. The syntax parsing in TiDB is based on Yacc.

```
Expression:
      singleAtIdentifier assignmentEq Expression
    | Expression logOr Expression
    | Expression "XOR" Expression
    | Expression logAnd Expression
    | "NOT" Expression
    | Factor IsOrNotOp trueKwd
    | Factor IsOrNotOp falseKwd
    | Factor IsOrNotOp "UNKNOWN"
    | Factor

Factor:
      Factor IsOrNotOp "NULL"
    | Factor CompareOp PredicateExpr
    | Factor CompareOp singleAtIdentifier assignmentEq PredicateExpr
    | Factor CompareOp AnyOrAll SubSelect
    | PredicateExpr

PredicateExpr:
      PrimaryFactor InOrNotOp '(' ExpressionList ')'
    | PrimaryFactor InOrNotOp SubSelect
    | PrimaryFactor BetweenOrNotOp PrimaryFactor "AND" PredicateExpr
    | PrimaryFactor LikeOrNotOp PrimaryExpression LikeEscapeOpt
    | PrimaryFactor RegexpOrNotOp PrimaryExpression
    | PrimaryFactor

PrimaryFactor:
      PrimaryFactor '|' PrimaryFactor
    | PrimaryFactor '&' PrimaryFactor
    | PrimaryFactor "<<" PrimaryFactor
    | PrimaryFactor ">>" PrimaryFactor
    | PrimaryFactor '+' PrimaryFactor
    | PrimaryFactor '-' PrimaryFactor
    | PrimaryFactor '*' PrimaryFactor
    | PrimaryFactor '/' PrimaryFactor
    | PrimaryFactor '%' PrimaryFactor
    | PrimaryFactor "DIV" PrimaryFactor
    | PrimaryFactor "MOD" PrimaryFactor
    | PrimaryFactor '^' PrimaryFactor
    | PrimaryExpression

PrimaryExpression:
      Operand
    | FunctionCallKeyword
    | FunctionCallNonKeyword
    | FunctionCallAgg
    | FunctionCallGeneric
    | Identifier jss stringLit
    | Identifier juss stringLit
    | SubSelect
    | '!' PrimaryExpression
    | '~'  PrimaryExpression
    | '-' PrimaryExpression
    | '+' PrimaryExpression
    | "BINARY" PrimaryExpression
    | PrimaryExpression "COLLATE" StringName
=======
An expression is a combination of one or more values, operators, or functions. In TiDB, expressions are mainly used in various clauses of the `SELECT` statement, including Group by clause, Where clause, Having clause, Join condition and window function. In addition, some DDL statements also use expressions, such as the setting of the default values, columns, and partition rules when creating tables.

The expressions can be divided into the following types:

- Identifier. For reference, see [Schema object names](/schema-object-names.md).

- Predicates, numeric values, strings, date expressions. The [Literal values](/literal-values.md) of these types are also expressions.

- Function calls and window functions. For reference, see [Functions and operators overview](/functions-and-operators/functions-and-operators-overview.md) and [Window functions](/functions-and-operators/window-functions.md)

- ParamMarker (`?`), system variables, user variables and CASE expressions.

The following rules are the expression syntax, which is based on the [parser.y](https://github.com/pingcap/parser/blob/master/parser.y) rules of TiDB parser. For the navigable version of the following syntax diagram, refer to [TiDB SQL Syntax Diagram](https://pingcap.github.io/sqlgram/#Expression).

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
>>>>>>> 4c603f53... sql-statements: use EBNF to render syntax diagrams for ADD, ALTER and ANALYZE statements (#4722)
```
