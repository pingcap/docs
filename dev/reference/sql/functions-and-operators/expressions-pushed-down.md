---
title: List of Operators for Pushdown
summary: This document introduces a list of operators that can be pushed down to TiKV, the related operations of which are also provided.
category: reference
---

# List of Operators for Pushdown

When TiDB reads data from TiKV, TiDB tries to push down some expressions to TiKV to be processed thus reducing the amount of data transferred and the computational pressure on a single TiDB node. This document introduces operators that TiDB supports for pushdown and how to blacklist specific operators.

## List of operators for pushdown

| Type | Operators |
| :-------------- | :------------------------------------- |
| [Logical Functions](/dev/reference/sql/functions-and-operators/operators.md#logical-operators) | AND (&&), OR (&#124;&#124;), NOT (!) |
| [Comparison Functions](/dev/reference/sql/functions-and-operators/operators.md#comparison-functions-and-operators) | <, <=, =, != (<>), >, >=, [`<=>`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_equal-to), [`IN()`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_in), IS NULL, LIKE, IS TRUE, IS FALSE, [`COALESCE()`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_coalesce) |
| [Numeric Functions](/dev/reference/sql/functions-and-operators/numeric-functions-and-operators.md) | +, -, *, /, [`ABS()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_abs), [`CEIL()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_ceil), [`CEILING()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_ceiling), [`FLOOR()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_floor) |
| [Control Flow Functions](/dev/reference/sql/functions-and-operators/control-flow-functions.md) | [`CASE`](https://dev.mysql.com/doc/refman/5.7/en/control-flow-functions.html#operator_case), [`IF()`](https://dev.mysql.com/doc/refman/5.7/en/control-flow-functions.html#function_if), [`IFNULL()`](https://dev.mysql.com/doc/refman/5.7/en/control-flow-functions.html#function_ifnull) |
| [JSON Functions](/dev/reference/sql/functions-and-operators/json-functions.md) | [JSON_TYPE(json_val)][json_type],<br> [JSON_EXTRACT(json_doc, path[, path] ...)][json_extract],<br> [JSON_UNQUOTE(json_val)][json_unquote],<br> [JSON_OBJECT(key, val[, key, val] ...)][json_object],<br> [JSON_ARRAY([val[, val] ...])][json_array],<br> [JSON_MERGE(json_doc, json_doc[, json_doc] ...)][json_merge],<br> [JSON_SET(json_doc, path, val[, path, val] ...)][json_set],<br> [JSON_INSERT(json_doc, path, val[, path, val] ...)][json_insert],<br> [JSON_REPLACE(json_doc, path, val[, path, val] ...)][json_replace],<br> [JSON_REMOVE(json_doc, path[, path] ...)][json_remove] |
| [Date and Time Functions](/dev/reference/sql/functions-and-operators/date-and-time-functions.md) | [`DATE_FORMAT()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_date-format)  |

## Blacklist specific operators

If unexpected behavior occurs in the calculation of the function due to pushdown operators, you can quickly restore it by blacklisting specific operators. Specifically, you can prohibit operators from being pushing down by putting it on the blacklist `mysql.expr_pushdown_blacklist`.

### Add to the blacklist

To add one or more operators to the blacklist, perform the following steps:

1. Insert the corresponding operator name in `mysql.expr_pushdown_blacklist`.

2. Execute `admin reload expr_pushdown_blacklist;` command.

### Remove from the blacklist

To remove one or more operators from the blacklist, perform the following steps:

1. Delete the corresponding operator name in `mysql.expr_pushdown_blacklist`.

2. Execute `admin reload expr_pushdown_blacklist;` command.

### Example

The following example demonstrates how to add `<` and `>` to the blacklist, then remove `>` from the blacklist.

Whether the blacklist is effective can be observed from the results returned by `EXPLAIN` statement (See [how to understand `EXPLAIN` results](/dev/reference/performance/understanding-the-query-execution-plan.md)).

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
> - `admin reload expr_pushdown_blacklist` only works for TiDB server that executes this SQL statement. To enable the blacklist in every TiDB server in the cluster, you need to execute the SQL statement on each TiDB server.
> - The blacklist feature of pushdown operators is supported in v3.0.0 or later.
> - Note that in v3.0.3 or earlier, some of the operators (such as ">", "+", "is null") are not supported to add to the blacklist. This means you have to use aliases (case-insensitive) instead, as shown in the following table:
>
>     | Operator Name | Aliases |
>     | :-------- | :---------- |
>     | < | LT |
>     | > | GT |
>     | <= | LE |
>     | >= | GT |
>     | = | EQ |
>     | != | NE |
>     | <> | NE |
>     | <=> | NullEQ |
>     | &#124; | bitor |
>     | && | bitand|
>     | &#124;&#124; | or |
>     | ! | not |
>     | in | IN |
>     | + | PLUS|
>     |  - | MINUS |
>     | * | MUL |
>     |  / | DIV |
>     | DIV | INTDIV |
>     | IS NULL | ISNULL |
>     | IS TRUE | ISTRUE |
>     | IS FALSE | ISFALSE |

[json_extract]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-extract
[json_short_extract]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#operator_json-column-path
[json_short_extract_unquote]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#operator_json-inline-path
[json_unquote]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-unquote
[json_type]: https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-type
[json_set]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-set
[json_insert]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-insert
[json_replace]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-replace
[json_remove]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-remove
[json_merge]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-merge
[json_merge_preserve]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-merge-preserve
[json_object]: https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-object
[json_array]: https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-array
[json_keys]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-keys
[json_length]: https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-length
[json_valid]: https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-valid
[json_quote]: https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-quote
[json_contains]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-contains
[json_contains_path]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-contains-path
[json_arrayagg]: https://dev.mysql.com/doc/refman/5.7/en/group-by-functions.html#function_json-arrayagg
[json_depth]: https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-depth