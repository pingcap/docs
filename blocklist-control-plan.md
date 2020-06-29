---
title: The Blocklist of Optimization Rules and Expression Pushdown
summary: Learn about the blocklist to control the optimization rules and the behavior of expression pushdown.
category: performance
---

# The Blocklist of Optimization Rules and Expression Pushdown

This document introduces how we use the blocklist of optimization rules and the blocklist of expression pushdown to control the behavior of TiDB.

## The Blocklist of Optimization Rules

### Important Optimization Rules

|**Optimization Rule**|**Rule Name**|**Description**|
| :--- | :--- | :--- |
| Column Pruning | column_prune | One executor will prune the column if it's not needed by the upper executor |
| Decorrelate Subquery | decorrelate | Try to rewrite the correlated subquery to non-correlated join or aggregation |
| Aggregation Elimination | aggregation_eliminate | Try to remove some unnecessary aggregations |
| Projection Elimination | projection_eliminate | Remove unnecessary projects |
| Max/Min Elimination | max_min_eliminate | Rewrite some max/min function in aggregation to the form `order by` + `limit 1` |
| Predicate Pushdown | predicate_push_down | Try to push predicates to the executor that is closer to the data source |
| Outer Join Elimination | outer_join_eliminate | Try to convert the left/right join to inner join |
| Partition Pruning | partition_processor | Pruning partitions which are rejected by the predicates and rewrite to the form `UnionAll + Partition Datasource` |
| Aggregation Pushdown | aggregation_push_down| Try to push aggregations down to their children |
| TopN Pushdown | topn_push_down | Try to push the topn to where is closer to the data source |
| Join Reorder | join_reorder | Decide the order of multi-table joins |

### Disable Optimization Rules

We can use the **Blocklist of Optimization Rules** to disable some of them if some rules lead to a sub-optimal execution plan for some special queries.

#### Usage

> **Note:**
>
> All the following operations need the `super privilege` privilege of the database. Each optimization rule has a name. e.g. the name of column pruning is `column_prune`. The names of all optimization rules can be found in the second column of the table [Important Optimization Rules](#Important_Optimization_Rules).

- If you want to disable some rules, you can write its name to the table `mysql.opt_rule_blacklist`. e.g.

    {{< copyable "sql" >}}

    ```sql
    insert into mysql.opt_rule_blacklist values("join_reorder"), ("topn_push_down");
    ```

    Executing the following SQL statement can make the above operation take effect immediately. Including old connections of the corresponding TiDB Server:

    {{< copyable "sql" >}}

    ```sql
    admin reload opt_rule_blacklist;
    ```

    > **Note:**
    >
    > `admin reload opt_rule_blacklist` only takes effect on the TiDB Server which runs this statement. If you need all TiDB Server of the cluster to disable some rules, you need to run this command on each of the TiDB Server.

- If you want to re-enable some rules, delete the corresponding data in the table, and then run `admin reload` statement:

    {{< copyable "sql" >}}

    ```sql
    delete from mysql.opt_rule_blacklist where name in ("join_reoder", "topn_push_down");
    admin reload opt_rule_blacklist;
    ```

## The Blocklist of Expression Pushdown

**The Blocklist of Expression Pushdown** is one way to tuning the expression pushdown, mainly used to disable some expression of some specific data types.

### Expressions which are supported to be pushed down

| Expression Classification | Concrete Operations |
| :-------------- | :------------------------------------- |
| [Logical Operations](/functions-and-operators/operators.md#logical-operators) | AND (&&), OR (&#124;&#124;), NOT (!) |
| [Comparison functions and operators](#comparison-functions-and-operators) | <, <=, =, != (`<>`), >, >=, [`<=>`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_equal-to), [`IN()`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_in), IS NULL, LIKE, IS TRUE, IS FALSE, [`COALESCE()`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_coalesce) |
| [Numberic functions and operators](/functions-and-operators/numeric-functions-and-operators.md) | +, -, *, /, [`ABS()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_abs), [`CEIL()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_ceil), [`CEILING()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_ceiling), [`FLOOR()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_floor) |
| [Control flow functions](/functions-and-operators/control-flow-functions.md) | [`CASE`](https://dev.mysql.com/doc/refman/5.7/en/control-flow-functions.html#operator_case), [`IF()`](https://dev.mysql.com/doc/refman/5.7/en/control-flow-functions.html#function_if), [`IFNULL()`](https://dev.mysql.com/doc/refman/5.7/en/control-flow-functions.html#function_ifnull) |
| [JSON functions](/functions-and-operators/json-functions.md) | [JSON_TYPE(json_val)][json_type],<br/> [JSON_EXTRACT(json_doc, path[, path] ...)][json_extract],<br/> [JSON_UNQUOTE(json_val)][json_unquote],<br/> [JSON_OBJECT(key, val[, key, val] ...)][json_object],<br/> [JSON_ARRAY([val[, val] ...])][json_array],<br/> [JSON_MERGE(json_doc, json_doc[, json_doc] ...)][json_merge],<br/> [JSON_SET(json_doc, path, val[, path, val] ...)][json_set],<br/> [JSON_INSERT(json_doc, path, val[, path, val] ...)][json_insert],<br/> [JSON_REPLACE(json_doc, path, val[, path, val] ...)][json_replace],<br/> [JSON_REMOVE(json_doc, path[, path] ...)][json_remove] |
| [Date and time functions](/functions-and-operators/date-and-time-functions.md) | [`DATE_FORMAT()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_date-format)  |

### Disable the pushdown of specific expression

When we got wrong results due to the expression pushdown, use the blocklist can make a quick recovery for the business. More clearly, you can add some of the supported functions or operators to the table `mysql.expr_pushdown_blacklist` to disable the pushdown of some specific expressions.

The schema of `mysql.expr_pushdown_blacklist` is shown as below:

{{< copyable "sql" >}}

```sql
desc mysql.expr_pushdown_blacklist;
```

```sql
+------------+--------------+------+------+-------------------+-------+
| Field      | Type         | Null | Key  | Default           | Extra |
+------------+--------------+------+------+-------------------+-------+
| name       | char(100)    | NO   |      | NULL              |       |
| store_type | char(100)    | NO   |      | tikv,tiflash,tidb |       |
| reason     | varchar(200) | YES  |      | NULL              |       |
+------------+--------------+------+------+-------------------+-------+
3 rows in set (0.00 sec)
```

Here is the description of each field:

+ `name`: The name of expression that is disabled to be pushed down.
+ `store_type`: To specify the component you don't want the expression to be pushed down. Three components `tidb`, `tikv`, and `tiflash` are available. The `store_type` is case-insensitive. Use the comma to divide each component if more than one component is specified.
    - The `store_type` `tidb` decides whether the expression can be executed in other TiDB Server when reading the TiDB memory table.
    - The `store_type` `tikv` decides whether the expression can be executed in TiKV Server's Coprocessor component.
    - The `store_type` `tiflash` decides whether the expression can be executed in TiFlash Server's Coprocessor component.
+ `reason`: To record the reason why this expression is added to the blocklist.

### Usage

#### Add to the blocklist

Using the following procedures if you want to add one or more expressions to the blocklist:

1. Insert the corresponding function name or operator name and the set of components you want to disable the pushdown to the table `mysql.expr_pushdown_blacklist`.

2. Execute `admin reload expr_pushdown_blacklist`.

### Remove from the blocklist

Using the following procedures if you want to remove one or more expressions from the blocklist:

1. Delete the corresponding function name or operator name and the set of components you want to disable the pushdown from the table `mysql.expr_pushdown_blacklist`.

2. Execute `admin reload expr_pushdown_blacklist`.

> **Note:**
>
> `admin reload expr_pushdown_blacklist` only takes effect on the TiDB Server which runs this statement. If you need all TiDB Server of the cluster to disable some rules, you need to run this command on each of the TiDB Server.

## Example of the Expression Blocklist

The following example first adds the operator `<` and `>` to the blocklist then removes the operator `>` from the blocklist.

Whether the blocklist takes effect can be observed in the `EXPLAIN` result(See [SQL Tuning with `EXPLAIN`](/query-execution-plan.md)).

1. The predicates `a < 2` and `a > 2` in the `WHERE` clause of the following SQL statement can be pushed down to TiKV.

    {{< copyable "sql" >}}

    ```sql
    explain select * from t where a < 2 and a > 2;
    ```

    ```sql
    +-------------------------+----------+-----------+---------------+------------------------------------+
    | id                      | estRows  | task      | access object | operator info                      |
    +-------------------------+----------+-----------+---------------+------------------------------------+
    | TableReader_7           | 0.00     | root      |               | data:Selection_6                   |
    | └─Selection_6           | 0.00     | cop[tikv] |               | gt(ssb_1.t.a, 2), lt(ssb_1.t.a, 2) |
    |   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo     |
    +-------------------------+----------+-----------+---------------+------------------------------------+
    3 rows in set (0.00 sec)
    ```

2. Insert the expression to the table `mysql.expr_pushdown_blacklist` and execute `admin reload expr_pushdown_blacklist`.

    {{< copyable "sql" >}}

    ```sql
    insert into mysql.expr_pushdown_blacklist values('<','tikv',''), ('>','tikv','');
    ```

    ```sql
    Query OK, 2 rows affected (0.01 sec)
    Records: 2  Duplicates: 0  Warnings: 0
    ```

    {{< copyable "sql" >}}

    ```sql
    admin reload expr_pushdown_blacklist;
    ```

    ```sql
    Query OK, 0 rows affected (0.00 sec)
    ```

3. Observe the execution plan again and you will find that both the operator `<` and `>` are not pushed down to TiKV Coprocessor.

    {{< copyable "sql" >}}

    ```sql
    explain select * from t where a < 2 and a > 2;
    ```

    ```sql
    +-------------------------+----------+-----------+---------------+------------------------------------+
    | id                      | estRows  | task      | access object | operator info                      |
    +-------------------------+----------+-----------+---------------+------------------------------------+
    | Selection_7             | 10000.00 | root      |               | gt(ssb_1.t.a, 2), lt(ssb_1.t.a, 2) |
    | └─TableReader_6         | 10000.00 | root      |               | data:TableFullScan_5               |
    |   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo     |
    +-------------------------+----------+-----------+---------------+------------------------------------+
    3 rows in set (0.00 sec)
    ```

4. Remove one expression(here is `>`) from the blacklist and execute `admin reload expr_pushdown_blacklist`.

    {{< copyable "sql" >}}

    ```sql
    delete from mysql.expr_pushdown_blacklist where name = '>';
    ```

    ```sql
    Query OK, 1 row affected (0.01 sec)
    ```

    {{< copyable "sql" >}}

    ```sql
    admin reload expr_pushdown_blacklist;
    ```

    ```sql
    Query OK, 0 rows affected (0.00 sec)

5. Observe the execution plan again and you will find that `<` is not pushed down while `>` is not pushed down to TiKV Coprocessor.

    {{< copyable "sql" >}}

    ```sql
    explain select * from t where a < 2 and a > 2;
    ```

    ```sql
    +---------------------------+----------+-----------+---------------+--------------------------------+
    | id                        | estRows  | task      | access object | operator info                  |
    +---------------------------+----------+-----------+---------------+--------------------------------+
    | Selection_8               | 0.00     | root      |               | lt(ssb_1.t.a, 2)               |
    | └─TableReader_7           | 0.00     | root      |               | data:Selection_6               |
    |   └─Selection_6           | 0.00     | cop[tikv] |               | gt(ssb_1.t.a, 2)               |
    |     └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo |
    +---------------------------+----------+-----------+---------------+--------------------------------+
    4 rows in set (0.00 sec)
    ```