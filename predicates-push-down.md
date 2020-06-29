---
title: Predicates Push Down
category: reference
aliases: ['/docs/dev/predicates-push-down.md/','/docs/dev/reference/performance/predicates-push-down/']
---

# Predicates Push Down(PPD)

This document introduces one of the TiDB's logic optimization rules—Predicate Push Down(PPD). It aims to help readers understand the predicate push down and know its suitable and unsuitable scenarios.

PPD pushes down selection operators as close to data source as possible to complete data filtering as early as possible. Thereby significantly reducing the cost of data transmission or computation. 

## Examples

The following cases describes the optimization of PPD. Examples 1, 2, and 3 are cases where PPD is applicable, and examples 4, 5, and 6 are cases where PPD is not applicable.

### Case 1: push predicates to storage layer

```sql
create table t(id int primary key, a int);
explain select * from t where a < 1;
+-------------------------+----------+-----------+---------------+--------------------------------+
| id                      | estRows  | task      | access object | operator info                  |
+-------------------------+----------+-----------+---------------+--------------------------------+
| TableReader_7           | 3323.33  | root      |               | data:Selection_6               |
| └─Selection_6           | 3323.33  | cop[tikv] |               | lt(test.t.a, 1)                |
|   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo |
+-------------------------+----------+-----------+---------------+--------------------------------+
3 rows in set (0.00 sec)
```

In this query，pushing down the predicate `a < 1` on TiKV to filter the data can reduce the overhead caused by network transmission.

### Case 1: push predicates to storage layer

```sql
create table t(id int primary key, a int not null);
explain select * from t where a < substring('123', 1, 1);
+-------------------------+----------+-----------+---------------+--------------------------------+
| id                      | estRows  | task      | access object | operator info                  |
+-------------------------+----------+-----------+---------------+--------------------------------+
| TableReader_7           | 3323.33  | root      |               | data:Selection_6               |
| └─Selection_6           | 3323.33  | cop[tikv] |               | lt(test.t.a, 1)                |
|   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo |
+-------------------------+----------+-----------+---------------+--------------------------------+
```

This query has the same execution plan as the query in case 1, because the input parameters of the `substring` of the predicate `a < substring('123', 1, 1)` are constants, so they can be calculated in advance. Then simplify to get the equivalent predicate `a < 1`. Further, TiDB can push `a < 1` down to TiKV.

### Case 3: push predicates below join operator

```sql
create table t(id int primary key, a int not null);
create table s(id int primary key, a int not null);
explain select * from t join s on t.a = s.a where t.a < 1;
+------------------------------+----------+-----------+---------------+--------------------------------------------+
| id                           | estRows  | task      | access object | operator info                              |
+------------------------------+----------+-----------+---------------+--------------------------------------------+
| HashJoin_8                   | 4154.17  | root      |               | inner join, equal:[eq(test.t.a, test.s.a)] |
| ├─TableReader_15(Build)      | 3323.33  | root      |               | data:Selection_14                          |
| │ └─Selection_14             | 3323.33  | cop[tikv] |               | lt(test.s.a, 1)                            |
| │   └─TableFullScan_13       | 10000.00 | cop[tikv] | table:s       | keep order:false, stats:pseudo             |
| └─TableReader_12(Probe)      | 3323.33  | root      |               | data:Selection_11                          |
|   └─Selection_11             | 3323.33  | cop[tikv] |               | lt(test.t.a, 1)                            |
|     └─TableFullScan_10       | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo             |
+------------------------------+----------+-----------+---------------+--------------------------------------------+
7 rows in set (0.00 sec)
```

In this query, the predicate `t.a < 1` is pushed below join to filter in advance, which can reduce the calculation of join.

In addition，This SQL executes an inner join, and the `ON` condition is `t.a = s.a`. The predicate `s.a <1` can be derived from `t.a < 1` and pushed down to `s` table below the join operator. Filtering the `s` table can further reduce the calculation of join.

### Case 4: predicates that are not supported by storage layers cannot be pushed down

```sql
create table t(id int primary key, a int not null);
desc select * from t where substring('123', a, 1) = '1';
+-------------------------+---------+-----------+---------------+----------------------------------------+
| id                      | estRows | task      | access object | operator info                          |
+-------------------------+---------+-----------+---------------+----------------------------------------+
| Selection_7             | 2.00    | root      |               | eq(substring("123", test.t.a, 1), "1") |
| └─TableReader_6         | 2.00    | root      |               | data:TableFullScan_5                   |
|   └─TableFullScan_5     | 2.00    | cop[tikv] | table:t       | keep order:false, stats:pseudo         |
+-------------------------+---------+-----------+---------------+----------------------------------------+
```

In this query, there is a predicate `substring('123', a, 1) = '1'`.

From the `explain` results, we can see that the predicate is not pushed down to TiKV for calculation. This is because the TiKV coprocessor does not support the built-in function `substring`.

### Case 5: predicates of inner tables on the outer join can't be pushed down

```sql
create table t(id int primary key, a int not null);
create table s(id int primary key, a int not null);
explain select * from t left join s on t.a = s.a where s.a is null;
+-------------------------------+----------+-----------+---------------+-------------------------------------------------+
| id                            | estRows  | task      | access object | operator info                                   |
+-------------------------------+----------+-----------+---------------+-------------------------------------------------+
| Selection_7                   | 10000.00 | root      |               | isnull(test.s.a)                                |
| └─HashJoin_8                  | 12500.00 | root      |               | left outer join, equal:[eq(test.t.a, test.s.a)] |
|   ├─TableReader_13(Build)     | 10000.00 | root      |               | data:TableFullScan_12                           |
|   │ └─TableFullScan_12        | 10000.00 | cop[tikv] | table:s       | keep order:false, stats:pseudo                  |
|   └─TableReader_11(Probe)     | 10000.00 | root      |               | data:TableFullScan_10                           |
|     └─TableFullScan_10        | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo                  |
+-------------------------------+----------+-----------+---------------+-------------------------------------------------+
6 rows in set (0.00 sec)
```

In this query，there is a predicate `s.a is null` on the inner table `s`。

From the `explain` results，we can see that the predicate is not pushed below join operator. This is because the outer join will fill the inner table with `NULL` values when the on condition isn't satisfied, and the predicate `s.a is null` is used to filter the results after the join. If it is pushed down to the inner table below join, the execution plan is not equivalent with the original one.

### Case 6: the predicates which contain user variables cannot be pushed down

```sql
create table t(id int primary key, a char);
set @a = 1;
explain select * from t where a < @a;
+-------------------------+----------+-----------+---------------+--------------------------------+
| id                      | estRows  | task      | access object | operator info                  |
+-------------------------+----------+-----------+---------------+--------------------------------+
| Selection_5             | 8000.00  | root      |               | lt(test.t.a, getvar("a"))      |
| └─TableReader_7         | 10000.00 | root      |               | data:TableFullScan_6           |
|   └─TableFullScan_6     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo |
+-------------------------+----------+-----------+---------------+--------------------------------+
3 rows in set (0.00 sec)
```

In this query，there is a predicate `a < @a` on table `t`. The `@a` of predicate is a user variable.

As can be seen from `explain` results, the predicate is not like case 2, which is simplified to `a < 1` and pushed down to TiKV. This is because the value of the user variable `@a` may changes during the computation, and TiKV is not aware of the changes. So TiDB will not replace `@a` with `1`, and will not be pushed down to TiKV.

An example to help understand is as follows：

```sql
create table t(id int primary key, a int);
insert into t values(1, 1), (2,2);
set @a = 1;
select id, a, @a:=@a+1 from t where a = @a;
+----+------+----------+
| id | a    | @a:=@a+1 |
+----+------+----------+
|  1 |    1 | 2        |
|  2 |    2 | 3        |
+----+------+----------+
2 rows in set (0.00 sec)
```

As you can see from this query, the value of `@a` will change during the query. So if you replace `a = @a` with `a = 1` and push it down to TiKV, it's not an equivalent execution plan. 