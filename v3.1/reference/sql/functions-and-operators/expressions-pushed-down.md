---
title: List of Expressions for Pushdown
summary: Learn a list of expressions that can be pushed down to TiKV and the related operations.
category: reference
---

# List of Expressions for Pushdown

When TiDB reads data from TiKV, TiDB tries to push down some expressions (including calculations of functions or operators) to be processed to TiKV. This reduces the amount of transferred data and offloads processing from a single TiDB node. This document introduces the expressions that TiDB already supports pushing down and how to prohibit specific expressions from being pushed down using blacklist.

## Supported expressions for pushdown

| Expression Type | Operations |
| :-------------- | :------------------------------------- |
| [Logical operators](/v3.1/reference/sql/functions-and-operators/operators.md#logical-operators) | AND (&&), OR (&#124;&#124;), NOT (!) |
| [Comparison functions and operators](/v3.1/reference/sql/functions-and-operators/operators.md#comparison-functions-and-operators) | <, <=, =, != (<>), >, >=, [`<=>`](https://v3.1.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_equal-to), [`IN()`](https://v3.1.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_in), IS NULL, LIKE, IS TRUE, IS FALSE, [`COALESCE()`](https://v3.1.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_coalesce) |
| [Numeric functions and operators](/v3.1/reference/sql/functions-and-operators/numeric-functions-and-operators.md) | +, -, *, /, [`ABS()`](https://v3.1.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_abs), [`CEIL()`](https://v3.1.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_ceil), [`CEILING()`](https://v3.1.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_ceiling), [`FLOOR()`](https://v3.1.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_floor) |
| [Control flow functions](/v3.1/reference/sql/functions-and-operators/control-flow-functions.md) | [`CASE`](https://v3.1.mysql.com/doc/refman/5.7/en/control-flow-functions.html#operator_case), [`IF()`](https://v3.1.mysql.com/doc/refman/5.7/en/control-flow-functions.html#function_if), [`IFNULL()`](https://v3.1.mysql.com/doc/refman/5.7/en/control-flow-functions.html#function_ifnull) |
| [JSON functions](/v3.1/reference/sql/functions-and-operators/json-functions.md) | [JSON_TYPE(json_val)][json_type],<br> [JSON_EXTRACT(json_doc, path[, path] ...)][json_extract],<br> [JSON_UNQUOTE(json_val)][json_unquote],<br> [JSON_OBJECT(key, val[, key, val] ...)][json_object],<br> [JSON_ARRAY([val[, val] ...])][json_array],<br> [JSON_MERGE(json_doc, json_doc[, json_doc] ...)][json_merge],<br> [JSON_SET(json_doc, path, val[, path, val] ...)][json_set],<br> [JSON_INSERT(json_doc, path, val[, path, val] ...)][json_insert],<br> [JSON_REPLACE(json_doc, path, val[, path, val] ...)][json_replace],<br> [JSON_REMOVE(json_doc, path[, path] ...)][json_remove] |
| [Date and time functions](/v3.1/reference/sql/functions-and-operators/date-and-time-functions.md) | [`DATE_FORMAT()`](https://v3.1.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_date-format)  |

## Blacklist specific expressions

If unexpected behavior occurs during the calculation of a function caused by its pushdown, you can quickly restore the application by blacklisting that function. Specifically, you can prohibit an expression from being pushed down by adding the corresponding functions or operator to the blacklist `mysql.expr_pushdown_blacklist`.

### Add to the blacklist

To add one or more functions or operators to the blacklist, perform the following steps:

1. Insert the function or operator name to `mysql.expr_pushdown_blacklist`.

2. Execute the `admin reload expr_pushdown_blacklist;` command.

### Remove from the blacklist

To remove one or more functions or operators from the blacklist, perform the following steps:

1. Delete the function or operator name in `mysql.expr_pushdown_blacklist`.

2. Execute the `admin reload expr_pushdown_blacklist;` command.

### Blacklist usage examples

The following example demonstrates how to add the `<` and `>` operators to the blacklist, then remove `>` from the blacklist.

You can see whether the blacklist takes effect by checking the results returned by `EXPLAIN` statement (See [Understanding `EXPLAIN` results](/v3.1/reference/performance/understanding-the-query-execution-plan.md)).

```sql
tidb> create table t(a int);
Query OK, 0 rows affected (0.01 sec)

tidb> explain select * from t where a < 2 and a > 2;
+---------------------+----------+------+------------------------------------------------------------+
| id                  | count    | task | operator info                                              |
+---------------------+----------+------+------------------------------------------------------------+
| TableReader_7       | 0.00     | root | data:Selection_6                                           |
| └─Selection_6       | 0.00     | cop  | gt(test.t.a, 2), lt(test.t.a, 2)                           |
|   └─TableScan_5     | 10000.00 | cop  | table:t, range:[-inf,+inf], keep order:false, stats:pseudo |
+---------------------+----------+------+------------------------------------------------------------+
3 rows in set (0.00 sec)

tidb> insert into mysql.expr_pushdown_blacklist values('<'), ('>');
Query OK, 2 rows affected (0.00 sec)
Records: 2  Duplicates: 0  Warnings: 0

tidb> admin reload expr_pushdown_blacklist;
Query OK, 0 rows affected (0.00 sec)

tidb> explain select * from t where a < 2 and a > 2;
+---------------------+----------+------+------------------------------------------------------------+
| id                  | count    | task | operator info                                              |
+---------------------+----------+------+------------------------------------------------------------+
| Selection_5         | 8000.00  | root | gt(test.t.a, 2), lt(test.t.a, 2)                           |
| └─TableReader_7     | 10000.00 | root | data:TableScan_6                                           |
|   └─TableScan_6     | 10000.00 | cop  | table:t, range:[-inf,+inf], keep order:false, stats:pseudo |
+---------------------+----------+------+------------------------------------------------------------+
3 rows in set (0.00 sec)

tidb> delete from mysql.expr_pushdown_blacklist where name = '>';
Query OK, 1 row affected (0.00 sec)

tidb> admin reload expr_pushdown_blacklist;
Query OK, 0 rows affected (0.00 sec)

tidb> explain select * from t where a < 2 and a > 2;
+-----------------------+----------+------+------------------------------------------------------------+
| id                    | count    | task | operator info                                              |
+-----------------------+----------+------+------------------------------------------------------------+
| Selection_5           | 2666.67  | root | lt(test.t.a, 2)                                            |
| └─TableReader_8       | 3333.33  | root | data:Selection_7                                           |
|   └─Selection_7       | 3333.33  | cop  | gt(test.t.a, 2)                                            |
|     └─TableScan_6     | 10000.00 | cop  | table:t, range:[-inf,+inf], keep order:false, stats:pseudo |
+-----------------------+----------+------+------------------------------------------------------------+
4 rows in set (0.00 sec)
```

> **Note:**
>
> - `admin reload expr_pushdown_blacklist` only takes effect on the TiDB server that executes this SQL statement. To make it apply to all TiDB servers, execute the SQL statement on each TiDB server.
> - The feature of blacklisting specific expressions is supported in TiDB 3.0.0 or later versions.
> - TiDB 3.0.3 or earlier versions does not support adding some of the operators (such as ">", "+", "is null") to the blacklist by using their original names. You need to use their aliases (case-insensitive) instead, as shown in the following table:

| Operator Name | Aliases |
| :-------- | :---------- |
| < | LT |
| > | GT |
| <= | LE |
| >= | GT |
| = | EQ |
| != | NE |
| <> | NE |
| <=> | NullEQ |
| &#124; | bitor |
| && | bitand|
| &#124;&#124; | or |
| ! | not |
| in | IN |
| + | PLUS|
|  - | MINUS |
| * | MUL |
|  / | DIV |
| DIV | INTDIV |
| IS NULL | ISNULL |
| IS TRUE | ISTRUE |
| IS FALSE | ISFALSE |

[json_extract]: https://v3.1.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-extract
[json_short_extract]: https://v3.1.mysql.com/doc/refman/5.7/en/json-search-functions.html#operator_json-column-path
[json_short_extract_unquote]: https://v3.1.mysql.com/doc/refman/5.7/en/json-search-functions.html#operator_json-inline-path
[json_unquote]: https://v3.1.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-unquote
[json_type]: https://v3.1.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-type
[json_set]: https://v3.1.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-set
[json_insert]: https://v3.1.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-insert
[json_replace]: https://v3.1.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-replace
[json_remove]: https://v3.1.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-remove
[json_merge]: https://v3.1.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-merge
[json_merge_preserve]: https://v3.1.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-merge-preserve
[json_object]: https://v3.1.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-object
[json_array]: https://v3.1.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-array
[json_keys]: https://v3.1.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-keys
[json_length]: https://v3.1.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-length
[json_valid]: https://v3.1.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-valid
[json_quote]: https://v3.1.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-quote
[json_contains]: https://v3.1.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-contains
[json_contains_path]: https://v3.1.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-contains-path
[json_arrayagg]: https://v3.1.mysql.com/doc/refman/5.7/en/group-by-functions.html#function_json-arrayagg
[json_depth]: https://v3.1.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-depth