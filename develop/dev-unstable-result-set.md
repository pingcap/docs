---
title: Unstable Result Set
summary: The treatment of result set unstable error.
---

# Unstable Result Set

This chapter will describe the treatment of result set unstable errors.

## GROUP BY

For convenience reasons, MySQL "extends" the `GROUP BY` syntax to allow the `SELECT` clause to refer to non-aggregated fields not declared in the `GROUP BY` clause, i.e., the `NON-FULL GROUP BY` syntax. In other databases, this is considered a syntax **_ERROR_** because it causes the result set to be unstable.

In the following 3 SQL statements, the first SQL uses the `FULL GROUP BY` syntax and all the fields referenced in the `SELECT` clause are declared in the `GROUP BY` clause, so its result set is stable, and you can see that there are three combinations of `class` and `stuname`;

The second and third SQL is the same SQL, but it gets different results when executed twice. The `GROUP BY` clause of this SQL declares only one `class` field, so the result set will only be aggregated for `class`, and there are two unique values for `class`, which means the result set will only contain two rows of data, and there are three combinations of `class` and `stuname`, and there are two students in class `2018_CS_03`, so there is no semantic restriction on which one is returned in each execution. There is no semantic restriction on which classmate is returned in each execution, and the results are semantically consistent.

{{< copyable "sql" >}}

```sql
mysql> SELECT a.class, a.stuname, max(b.courscore) from stu_info a join stu_score b on a.stuno=b.stuno group by a.class, a.stuname order by a.class, a.stuname;
+------------+--------------+------------------+
| class      | stuname      | max(b.courscore) |
+------------+--------------+------------------+
| 2018_CS_01 | MonkeyDLuffy |             95.5 |
| 2018_CS_03 | PatrickStar  |             99.0 |
| 2018_CS_03 | SpongeBob    |             95.0 |
+------------+--------------+------------------+
3 rows in set (0.00 sec)

mysql> select a.class, a.stuname, max(b.courscore) from stu_info a join stu_score b on a.stuno=b.stuno group by a.class order by a.class, a.stuname;
+------------+--------------+------------------+
| class      | stuname      | max(b.courscore) |
+------------+--------------+------------------+
| 2018_CS_01 | MonkeyDLuffy |             95.5 |
| 2018_CS_03 | SpongeBob    |             99.0 |
+------------+--------------+------------------+
2 rows in set (0.01 sec)

mysql> select a.class, a.stuname, max(b.courscore) from stu_info a join stu_score b on a.stuno=b.stuno group by a.class order by a.class, a.stuname;
+------------+--------------+------------------+
| class      | stuname      | max(b.courscore) |
+------------+--------------+------------------+
| 2018_CS_01 | MonkeyDLuffy |             95.5 |
| 2018_CS_03 | PatrickStar  |             99.0 |
+------------+--------------+------------------+
2 rows in set (0.01 sec)

```

Therefore, if you want to guarantee the stability of `GROUP BY` statement result set, please use `FULL GROUP BY` syntax.

MySQL provides a `sql_mode` switch `ONLY_FULL_GROUP_BY` to control whether to check the `FULL GROUP BY` syntax or not, TiDB is also compatible with this `sql_mode` switch.

{{< copyable "sql" >}}

```sql
mysql> select a.class, a.stuname, max(b.courscore) from stu_info a join stu_score b on a.stuno=b.stuno group by a.class order by a.class, a.stuname;
+------------+--------------+------------------+
| class      | stuname      | max(b.courscore) |
+------------+--------------+------------------+
| 2018_CS_01 | MonkeyDLuffy |             95.5 |
| 2018_CS_03 | PatrickStar  |             99.0 |
+------------+--------------+------------------+
2 rows in set (0.01 sec)

mysql> set @@sql_mode='STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION,ONLY_FULL_GROUP_BY';
Query OK, 0 rows affected (0.01 sec)

mysql> select a.class, a.stuname, max(b.courscore) from stu_info a join stu_score b on a.stuno=b.stuno group by a.class order by a.class, a.stuname;
ERROR 1055 (42000): Expression #2 of ORDER BY is not in GROUP BY clause and contains nonaggregated column '' which is not functionally dependent on columns in GROUP BY clause; this is incompatible with sql_mode=only_full_group_by
```

**Brief description of run results**: The above example sets the effect of `ONLY_FULL_GROUP_BY` for `sql_mode`.

## ORDER BY

In SQL semantics, the order output of the result set is guaranteed only if the `ORDER BY` syntax is used. Since the data in a single-instance database is stored on one server, the results of multiple executions are often stable without data reorganization. Some databases (especially the MySQL InnoDB storage engine) also output the result set in the order of the primary key or index. TiDB is a distributed database, and data is stored on multiple servers. In addition, the TiDB layer does not cache data pages, so the result set display order of SQL statements without `ORDER BY` is easily perceived as unstable. To output a sequential result set, you need to explicitly add the column to be sorted into the `ORDER BY` clause, which conforms to SQL semantics.

In the following case, the user added only one field to the `ORDER BY` clause, and TiDB will only sort by that one field.

{{< copyable "sql" >}}

```sql
mysql> select a.class, a.stuname, b.course, b.courscore from stu_info a join stu_score b on a.stuno=b.stuno order by a.class;
+------------+--------------+-------------------------+-----------+
| class      | stuname      | course                  | courscore |
+------------+--------------+-------------------------+-----------+
| 2018_CS_01 | MonkeyDLuffy | PrinciplesofDatabase    |      60.5 |
| 2018_CS_01 | MonkeyDLuffy | English                 |      43.0 |
| 2018_CS_01 | MonkeyDLuffy | OpSwimming              |      67.0 |
| 2018_CS_01 | MonkeyDLuffy | OpFencing               |      76.0 |
| 2018_CS_01 | MonkeyDLuffy | FundamentalsofCompiling |      88.0 |
| 2018_CS_01 | MonkeyDLuffy | OperatingSystem         |      90.5 |
| 2018_CS_01 | MonkeyDLuffy | PrincipleofStatistics   |      69.0 |
| 2018_CS_01 | MonkeyDLuffy | ProbabilityTheory       |      76.0 |
| 2018_CS_01 | MonkeyDLuffy | Physics                 |      63.5 |
| 2018_CS_01 | MonkeyDLuffy | AdvancedMathematics     |      95.5 |
| 2018_CS_01 | MonkeyDLuffy | LinearAlgebra           |      92.5 |
| 2018_CS_01 | MonkeyDLuffy | DiscreteMathematics     |      89.0 |
| 2018_CS_03 | SpongeBob    | PrinciplesofDatabase    |      88.0 |
| 2018_CS_03 | SpongeBob    | English                 |      79.0 |
| 2018_CS_03 | SpongeBob    | OpBasketball            |      92.0 |
| 2018_CS_03 | SpongeBob    | OpTennis                |      94.0 |
| 2018_CS_03 | PatrickStar  | LinearAlgebra           |       6.5 |
| 2018_CS_03 | PatrickStar  | AdvancedMathematics     |       5.0 |
| 2018_CS_03 | SpongeBob    | DiscreteMathematics     |      72.0 |
| 2018_CS_03 | PatrickStar  | ProbabilityTheory       |      12.0 |
| 2018_CS_03 | PatrickStar  | PrincipleofStatistics   |      20.0 |
| 2018_CS_03 | PatrickStar  | OperatingSystem         |      36.0 |
| 2018_CS_03 | PatrickStar  | FundamentalsofCompiling |       2.0 |
| 2018_CS_03 | PatrickStar  | DiscreteMathematics     |      14.0 |
| 2018_CS_03 | PatrickStar  | PrinciplesofDatabase    |       9.0 |
| 2018_CS_03 | PatrickStar  | English                 |      60.0 |
| 2018_CS_03 | PatrickStar  | OpTableTennis           |      12.0 |
| 2018_CS_03 | PatrickStar  | OpPiano                 |      99.0 |
| 2018_CS_03 | SpongeBob    | FundamentalsofCompiling |      43.0 |
| 2018_CS_03 | SpongeBob    | OperatingSystem         |      95.0 |
| 2018_CS_03 | SpongeBob    | PrincipleofStatistics   |      90.0 |
| 2018_CS_03 | SpongeBob    | ProbabilityTheory       |      87.0 |
| 2018_CS_03 | SpongeBob    | Physics                 |      65.0 |
| 2018_CS_03 | SpongeBob    | AdvancedMathematics     |      55.0 |
| 2018_CS_03 | SpongeBob    | LinearAlgebra           |      60.5 |
| 2018_CS_03 | PatrickStar  | Physics                 |       6.0 |
+------------+--------------+-------------------------+-----------+
36 rows in set (0.01 sec)

```

Sorting results are unstable when the same `ORDER BY` value is encountered. To reduce randomness, `ORDER BY` values should be kept as unique. If you can't guarantee the uniqueness, you need to keep adding `ORDER BY` fields to ensure that the combination of fields in `ORDER BY` is unique, then the result will be stable.

## The result set is unstable because order by is not used in `GROUP_CONCAT()`

The result set is unstable because TiDB reads data from the storage layer in parallel, so the order in which `GROUP_CONCAT()` presents the result set without `ORDER BY` is easily perceived as unstable.

To get the result set output in order, `GROUP_CONCAT()` needs to add the fields used for sorting to the `ORDER BY` clause, which is consistent with the semantics of SQL. In the following case, using `GROUP_CONCAT()` to splice `customer_id` without `ORDER BY` causes the result set to be unstable.

1. Excluded `ORDER BY`

   First query:

   {{< copyable "sql" >}}

   ```sql
   mysql>  select GROUP_CONCAT( customer_id SEPARATOR ',' ) FROM customer where customer_id like '200002%';
   +-------------------------------------------------------------------------+
   | GROUP_CONCAT(customer_id  SEPARATOR ',')                                |
   +-------------------------------------------------------------------------+
   | 20000200992,20000200993,20000200994,20000200995,20000200996,20000200... |
   +-------------------------------------------------------------------------+
   ```

   Second query:

   {{< copyable "sql" >}}

   ```sql
   mysql>  select GROUP_CONCAT( customer_id SEPARATOR ',' ) FROM customer where customer_id like '200002%';
   +-------------------------------------------------------------------------+
   | GROUP_CONCAT(customer_id  SEPARATOR ',')                                |
   +-------------------------------------------------------------------------+
   | 20000203040,20000203041,20000203042,20000203043,20000203044,20000203... |
   +-------------------------------------------------------------------------+
   ```

2. Include `ORDER BY`

   First query:

   {{< copyable "sql" >}}

   ```sql
   mysql>  select GROUP_CONCAT( customer_id order by customer_id SEPARATOR ',' ) FROM customer where customer_id like '200002%';
   +-------------------------------------------------------------------------+
   | GROUP_CONCAT(customer_id  SEPARATOR ',')                                |
   +-------------------------------------------------------------------------+
   | 20000200000,20000200001,20000200002,20000200003,20000200004,20000200... |
   +-------------------------------------------------------------------------+
   ```

   Second query:

   {{< copyable "sql" >}}

   ```sql
   mysql>  select GROUP_CONCAT( customer_id order by customer_id SEPARATOR ',' ) FROM customer where customer_id like '200002%';
   +-------------------------------------------------------------------------+
   | GROUP_CONCAT(customer_id  SEPARATOR ',')                                |
   +-------------------------------------------------------------------------+
   | 20000200000,20000200001,20000200002,20000200003,20000200004,20000200... |
   +-------------------------------------------------------------------------+
   ```

## SELECT \* FROM T LIMIT N has unstable results

The return result is related to the distribution of data on the storage node (TiKV). If multiple queries are performed, different storage units (Regions) of the storage nodes (TiKV) return results at different speeds, which can cause unstable results.
