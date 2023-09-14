---
title: GROUP BY Modifiers
summary: Learn about the group by modifiers in TiDB.
aliases: ['/docs/dev/functions-and-operators/group-by-modifiers/','/docs/dev/reference/sql/functions-and-operators/group-by-modifiers/']
---
# GROUP BY Modifiers

## Normal Usage Guide

The GROUP BY clause permits a WITH ROLLUP modifier that causes summary output to include extra rows that represent higher-level (that is, super-aggregate) summary operations. ROLLUP thus enables you to answer questions at multiple levels of analysis with a single query. For example, ROLLUP can be used to provide support for OLAP (Online Analytical Processing) operations.

TiDB does support `GROUP BY` modifiers such as `WITH ROLLUP` only under MPP mode, which means tiflash nodes are necessary. HTAP capability can supply a more flexible redistribution and regroup action for implementation of `Rollup` syntax, leading a more efficient execution flow of multidimensional aggregation.

Suppose that a sales table has year, country, product, and profit columns for recording sales profitability:

```sql
CREATE TABLE sales
(
    year    INT,
    country VARCHAR(20),
    product VARCHAR(32),
    profit  INT
);

alter table sales set tiflash replica 1;

insert into sales values(2000,"China","apple",1),(2001,"Japan","banana",2),(2000,"China","lemon",3)
```

To summarize table contents per year, use a simple GROUP BY like this:

```sql
TiDB [test]> SELECT year, SUM(profit) AS profit
                  ->        FROM sales
                  ->        GROUP BY year;
+------+--------+
| year | profit |
+------+--------+
| 2001 |      2 |
| 2000 |      4 |
+------+--------+
2 rows in set (0.057 sec)
```

The output shows the total (aggregate) profit for each year. To also determine the total profit summed over all years, you must add up the individual values yourself or run an additional query. Or you can use ROLLUP, which provides both levels of analysis with a single query. Adding a WITH ROLLUP modifier to the GROUP BY clause causes the query to produce another (super-aggregate) row that shows the grand total over all year values:

```sql
TiDB [test]> SELECT year, SUM(profit) AS profit
    ->        FROM sales
    ->        GROUP BY year WITH ROLLUP;
+------+--------+
| year | profit |
+------+--------+
| 2000 |      4 |
| 2001 |      2 |
| NULL |      6 |
+------+--------+
3 rows in set (0.029 sec)
```

The `NULL` value in the year column identifies the grand total super-aggregate line.

ROLLUP has a more complex effect when there are multiple GROUP BY columns. In this case, each time there is a change in value in any but the last grouping column, the query produces an extra super-aggregate summary row.

For example, without ROLLUP, a summary of the sales table based on year, country, and product might look like this, where the output indicates summary values only at the year/country/product level of analysis:

```sql
TiDB [test]> SELECT year, country, product, SUM(profit) AS profit
    ->        FROM sales
    ->        GROUP BY year, country, product;
+------+---------+---------+--------+
| year | country | product | profit |
+------+---------+---------+--------+
| 2000 | China   | lemon   |      3 |
| 2000 | China   | apple   |      1 |
| 2001 | Japan   | banana  |      2 |
+------+---------+---------+--------+
3 rows in set (0.002 sec)
```

With ROLLUP added, the query produces several extra rows:

```sql
TiDB [test]> SELECT year, country, product, SUM(profit) AS profit
    ->        FROM sales
    ->        GROUP BY year, country, product WITH ROLLUP;
+------+---------+---------+--------+
| year | country | product | profit |
+------+---------+---------+--------+
| 2000 | NULL    | NULL    |      4 |
| 2001 | Japan   | NULL    |      2 |
| 2001 | Japan   | banana  |      2 |
| 2001 | NULL    | NULL    |      2 |
| 2000 | China   | apple   |      1 |
| 2000 | China   | lemon   |      3 |
| 2000 | China   | NULL    |      4 |
| NULL | NULL    | NULL    |      6 |
+------+---------+---------+--------+
8 rows in set (0.029 sec)
```

Now the output includes summary information at four levels of analysis, not just one:
- Following each set of product rows for a given year and country, an extra super-aggregate summary row appears showing the total for all products. These rows have the product column set to `NULL`.


- Following each set of rows for a given year, an extra super-aggregate summary row appears showing the total for all countries and products. These rows have the country and products columns set to `NULL`.


- Finally, following all other rows, an extra super-aggregate summary row appears showing the grand total for all years, countries, and products. This row has the year, country, and products columns set to `NULL`.

The `NULL` indicators in each super-aggregate row are produced when the row is sent to the client. The server looks at the columns named in the GROUP BY clause following the leftmost one that has changed value. For any column in the result set with a name that matches any of those names, its value is set to `NULL`. (If you specify grouping columns by column position, the server identifies which columns to set to `NULL` by position.)

Because the `NULL` values in the super-aggregate rows are placed into the result set at such a late stage in query processing, you can test them as `NULL` values only in the select list or HAVING clause. You cannot test them as `NULL` values in join conditions or the WHERE clause to determine which rows to select. For example, you cannot add WHERE product IS `NULL` to the query to eliminate from the output all but the super-aggregate rows.

The `NULL` values do appear as `NULL` on the client side and can be tested as such using any MySQL client programming interface. However, at this point, you **cannot** distinguish whether a `NULL` represents a regular grouped value or a super-aggregate value. To distinguish the distinction, use the GROUPING() function, described later.

For `GROUP BY ... WITH ROLLUP` queries, to test whether `NULL` values in the result represent super-aggregate values, the `GROUPING()` function is available for use in the select list, `HAVING` clause, and ORDER BY clause. For example, `GROUPING(year)` returns 1 when `NULL` in the year column occurs in a super-aggregate row, and 0 otherwise. Similarly, `GROUPING(country)` and `GROUPING(product)` return 1 for super-aggregate `NULL` values in the country and product columns, respectively:

```sql
TiDB [test]> SELECT
    ->          year, country, product, SUM(profit) AS profit,
    ->          GROUPING(year) AS grp_year,
    ->          GROUPING(country) AS grp_country,
    ->          GROUPING(product) AS grp_product
    ->        FROM sales
    ->        GROUP BY year, country, product WITH ROLLUP;
+------+---------+---------+--------+----------+-------------+-------------+
| year | country | product | profit | grp_year | grp_country | grp_product |
+------+---------+---------+--------+----------+-------------+-------------+
| 2000 | China   | apple   |      1 |        0 |           0 |           0 |
| 2000 | China   | lemon   |      3 |        0 |           0 |           0 |
| 2000 | NULL    | NULL    |      4 |        0 |           1 |           1 |
| 2001 | Japan   | NULL    |      2 |        0 |           0 |           1 |
| 2001 | Japan   | banana  |      2 |        0 |           0 |           0 |
| 2000 | China   | NULL    |      4 |        0 |           0 |           1 |
| NULL | NULL    | NULL    |      6 |        1 |           1 |           1 |
| 2001 | NULL    | NULL    |      2 |        0 |           1 |           1 |
+------+---------+---------+--------+----------+-------------+-------------+
8 rows in set (0.040 sec)
```

Instead of displaying the `GROUPING()` results directly, you can use `GROUPING()` to substitute labels for super-aggregate `NULL` values, which will make the result more semantically understandable:

```sql
TiDB [test]> SELECT
    ->          IF(GROUPING(year), 'All years', year) AS year,
    ->          IF(GROUPING(country), 'All countries', country) AS country,
    ->          IF(GROUPING(product), 'All products', product) AS product,
    ->          SUM(profit) AS profit
    ->        FROM sales
    ->        GROUP BY year, country, product WITH ROLLUP;
+-----------+---------------+--------------+--------+
| year      | country       | product      | profit |
+-----------+---------------+--------------+--------+
| 2001      | Japan         | banana       |      2 |
| 2000      | China         | All products |      4 |
| 2001      | All countries | All products |      2 |
| All years | All countries | All products |      6 |
| 2000      | China         | apple        |      1 |
| 2000      | China         | lemon        |      3 |
| 2000      | All countries | All products |      4 |
| 2001      | Japan         | All products |      2 |
+-----------+---------------+--------------+--------+
8 rows in set (0.022 sec)
```

With multiple expression arguments (64 at the maximum), `GROUPING()` returns a result representing a bitmask the combines the results for each expression, with the lowest-order bit corresponding to the result for the rightmost expression. For example, `GROUPING(year, country, product)` is evaluated like this:

```sql
  result for GROUPING(product)
+ result for GROUPING(country) << 1
+ result for GROUPING(year) << 2
```

And bitmap combination indicates the column-type-info of `GROUPING()` is about `UNSIGNED LONGLONG` rather than `LONGLONG` as MySQL does.

The result of such a `GROUPING()` is nonzero if any of the expressions represents a super-aggregate `NULL`, so you can return only the super-aggregate rows and filter out the regular grouped rows like this:

```sql
TiDB [test]> SELECT year, country, product, SUM(profit) AS profit
    ->        FROM sales
    ->        GROUP BY year, country, product WITH ROLLUP
    ->        HAVING GROUPING(year, country, product) <> 0;
+------+---------+---------+--------+
| year | country | product | profit |
+------+---------+---------+--------+
| NULL | NULL    | NULL    |      6 |
| 2000 | NULL    | NULL    |      4 |
| 2001 | Japan   | NULL    |      2 |
| 2000 | China   | NULL    |      4 |
| 2001 | NULL    | NULL    |      2 |
+------+---------+---------+--------+
5 rows in set (0.027 sec)
```

The sales table contains no `NULL` values, so all `NULL` values in a ROLLUP result represent super-aggregate values. When the data set contains `NULL` values, ROLLUP summaries may contain `NULL` values not only in super-aggregate rows, but also in regular grouped rows. `GROUPING()` enables these to be distinguished. Suppose that table t1 contains a simple data set with two grouping factors for a set of quantity values, where `NULL` indicates something like “other” or “unknown”:

```sql
TiDB [test]> select * from t1;
+------+-------+----------+
| name | size  | quantity |
+------+-------+----------+
| ball | small |       10 |
| ball | large |       20 |
| ball | NULL  |        5 |
| hoop | small |       15 |
| hoop | large |        5 |
| hoop | NULL  |        3 |
+------+-------+----------+
6 rows in set (0.003 sec)
```

A simple ROLLUP operation produces these results, in which it is not so easy to distinguish `NULL` values in super-aggregate rows from `NULL` values in regular grouped rows:

```sql
TiDB [test]> SELECT name, size, SUM(quantity) AS quantity
    ->        FROM t1
    ->        GROUP BY name, size WITH ROLLUP;
+------+-------+----------+
| name | size  | quantity |
+------+-------+----------+
| hoop | NULL  |        3 |
| ball | NULL  |       35 |
| ball | large |       20 |
| ball | NULL  |        5 |
| ball | small |       10 |
| NULL | NULL  |       58 |
| hoop | small |       15 |
| hoop | large |        5 |
| hoop | NULL  |       23 |
+------+-------+----------+
9 rows in set (0.111 sec)
```
Using `GROUPING()` to substitute labels for the super-aggregate `NULL` values makes the result easier to interpret:

```sql
TiDB [test]> SELECT
    ->          IF(GROUPING(name) = 1, 'All items', name) AS name,
    ->          IF(GROUPING(size) = 1, 'All sizes', size) AS size,
    ->          SUM(quantity) AS quantity
    ->        FROM t1
    ->        GROUP BY name, size WITH ROLLUP;
+-----------+-----------+----------+
| name      | size      | quantity |
+-----------+-----------+----------+
| ball      | large     |       20 |
| ball      | NULL      |        5 |
| ball      | small     |       10 |
| All items | All sizes |       58 |
| hoop      | NULL      |        3 |
| ball      | All sizes |       35 |
| hoop      | small     |       15 |
| hoop      | large     |        5 |
| hoop      | All sizes |       23 |
+-----------+-----------+----------+
9 rows in set (0.029 sec)
```

## How to read the plan detail from ROLLUP?

Multidimensional aggregation currently depends on `Expand` operator to replicate underlying datasource, each replica of them corresponds to a specified grouping-set/grouping-layout, and redistribute them among mpp nodes utilizing the computation resource on each of them. 

`Expand` operator is quite similar to `Projection` operator which is inspired by the same name operator from SparkSQL, while the difference is that `Expand` operator receives a series of projection expressions which is generated by TiDB optimizer after analysis of grouping sets converted from ROLLUP syntax description. 

```go
// LogicalExpand represents a logical Expand OP serves for data replication requirement.
type LogicalExpand struct {
	// The level projections is generated from grouping sets，make execution more clearly.
	LevelExprs [][]expression.Expression
	// ...
}

// LogicalExpand represents a logical Expand OP serves for data replication requirement.
type LogicalProjection struct {
	// Exprs describe how to generate the projected columns
	Exprs []expression.Expression 
    // ...
}
```

This means for every one single row, `Projection` operator will produce corresponding single projected row out, while `Expand` operator will produce N (let's say len(`LevelExprs`) = N) rows with each row of them strictly projected from corresponding same position from first dimension of `LevelExprs`. Let's take the second sql above as an example.

```sql
TiDB [test]> explain SELECT year, GROUPING(year), SUM(profit) AS profit
    ->        FROM sales
    ->        GROUP BY year WITH ROLLUP;
+------------------------------------------+---------+--------------+---------------+------------------------------------------------------------------------------------------------------------------------------------------------------+
| id                                       | estRows | task         | access object | operator info                                                                                                                                        |
+------------------------------------------+---------+--------------+---------------+------------------------------------------------------------------------------------------------------------------------------------------------------+
| TableReader_44                           | 2.40    | root         |               | MppVersion: 2, data:ExchangeSender_43                                                                                                                |
| └─ExchangeSender_43                      | 2.40    | mpp[tiflash] |               | ExchangeType: PassThrough                                                                                                                            |
|   └─Projection_8                         | 2.40    | mpp[tiflash] |               | Column#6->Column#10, grouping(gid)->Column#11, Column#8->Column#12                                                                                   |
|     └─Projection_38                      | 2.40    | mpp[tiflash] |               | Column#8, Column#6, gid                                                                                                                              |
|       └─HashAgg_36                       | 2.40    | mpp[tiflash] |               | group by:Column#26, Column#27, funcs:sum(Column#23)->Column#8, funcs:firstrow(Column#24)->Column#6, funcs:firstrow(Column#25)->gid, stream_count: 10 |
|         └─Projection_45                  | 3.00    | mpp[tiflash] |               | cast(test.sales.profit, decimal(10,0) BINARY)->Column#23, Column#6->Column#24, gid->Column#25, Column#6->Column#26, gid->Column#27, stream_count: 10 |
|           └─ExchangeReceiver_22          | 3.00    | mpp[tiflash] |               | stream_count: 10                                                                                                                                     |
|             └─ExchangeSender_21          | 3.00    | mpp[tiflash] |               | ExchangeType: HashPartition, Compression: FAST, Hash Cols: [name: Column#6, collate: binary], [name: gid, collate: binary], stream_count: 10         |
|               └─Expand_20                | 3.00    | mpp[tiflash] |               | level-projection:[test.sales.profit, <nil>->Column#6, 0->gid],[test.sales.profit, Column#6, 1->gid]; schema: [test.sales.profit,Column#6,gid]        |
|                 └─Projection_16          | 3.00    | mpp[tiflash] |               | test.sales.profit, test.sales.year->Column#6                                                                                                         |
|                   └─TableFullScan_17     | 3.00    | mpp[tiflash] | table:sales   | keep order:false, stats:pseudo                                                                                                                       |
+------------------------------------------+---------+--------------+---------------+------------------------------------------------------------------------------------------------------------------------------------------------------+
11 rows in set (0.034 sec)

```

`Expand_20` operator info shows the generated level-projection expression: `[test.sales.profit, <nil>->Column#6, 0->gid],[test.sales.profit, Column#6, 1->gid]` composed as two-level expression slice, with suffix with `Expand` schema out as `[test.sales.profit,Column#6,gid]`.

As you see, additional column `gid` will be added in the schema, whose value will also be generated in its projection logic inside. `gid` generation rule has several mode:

```go
type GroupingMode int32

const (
	GroupingMode_ModeBitAnd     GroupingMode = 1
	GroupingMode_ModeNumericCmp GroupingMode = 2
	GroupingMode_ModeNumericSet GroupingMode = 3
)
```

The most common usage is the first grouping mode `GroupingMode_ModeBitAnd`, which indicates that `gid` is generated from current grouping set formation. Take this case for explanation, all the group-by column will be seen as a series of bits according their orders in group-by clause, one column [year] here. 

From rollup semantic, two grouping set will be converted as {year},{}. For the grouping set {year}, column year is needed in current grouping set, so we should keep its value rather than projecting it as `NULL` value. So the projection expression generation for grouping set {year} is obvious, it should be [test.sales.profit, Column#6, 1->gid].

Let's break it down, for grouping set {year}, the first projection expression `test.sales.profit` is normal column asked from upper operators, so we keep it; the second projection expression `column#6` is exactly the grouping set column year, which should be kept as its real as we said above; the third projection expression is `gid` column, a functional supplementary column added by Expand operator, indicating which grouping set current row is replicated for.

And how does `gid` equal to 1 is derived? As we said above, under grouping mode `GroupingMode_ModeBitAnd`, for current grouping set {year} and a bitmap [_] inferred from all grouping set column series [year], once a grouping set column is needed in current grouping set, fill it as a bit `1` in the same position of the bitmap. So we derive a bitmap [1] for grouping set {year} and a bitmap [0] for grouping set {}, and the length of both bitmap is exactly the same as the length of all grouping set column series [year], both equal to 1 here; And finally we convert the bitmap to a `UNSIGNED LONGLONG` value, which is exactly 1 and 0 as shown in the plan detail above.

Once there is `GROUPING(year)` function in the select list of the case above, TiDB will rewrite this grouping function by computing the relationship between its arg, a grouping set column `year` and generated column `gid`, because the latter one reflected the targeted grouping set information with a format of bitmap value in `gid`. Finally `GROUPING(year)` will be rewritten as `GROUPING(gid) with metadata`, in which the metadata illustrate how derive the final result from a `gid` value.