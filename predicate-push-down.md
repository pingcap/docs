---
title: Predicates Push Down
summary: 介绍 TiDB 的一种逻辑优化规则——Predicate Push Down (PPD)。
---

# Predicates Push Down (PPD)

本文介绍 TiDB 的一种逻辑优化规则——Predicate Push Down (PPD)。旨在帮助你理解谓词下推，并了解其适用和不适用的场景。

PPD 将筛选操作符尽可能下推到数据源，尽早完成数据过滤，从而显著降低数据传输或计算的开销。

## 示例

以下案例描述了 PPD 的优化过程。案例 1、2 和 3 是 PPD 适用的场景，案例 4、5 和 6 是 PPD 不适用的场景。

### 案例 1：将谓词下推到存储层

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

在此查询中，将谓词 `a < 1` 下推到 TiKV 层进行数据过滤，可以减少网络传输的开销。

### 案例 2：将谓词下推到存储层

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

此查询的执行计划与案例 1 相同，因为谓词 `a < substring('123', 1, 1)` 的输入参数是常量，可以提前计算。计算后，谓词简化为等价的 `a < 1`，然后 TiDB 可以将其下推到 TiKV。

### 案例 3：将谓词下推到连接操作符以下

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

在此查询中，将谓词 `t.a < 1` 下推到连接操作符以下进行提前过滤，可以减少连接的计算开销。

此外，该 SQL 语句执行了内连接，`ON` 条件为 `t.a = s.a`。由 `t.a < 1` 推导出的谓词 `s.a < 1` 也可以下推到连接操作符下的 `s` 表，从而进一步减少连接的计算开销。

### 案例 4：存储层不支持的谓词不能下推

```sql
create table t(id int primary key, a varchar(10) not null);
desc select * from t where truncate(a, " ") = '1';
+-------------------------+----------+-----------+---------------+---------------------------------------------------+
| id                      | estRows  | task      | access object | operator info                                     |
+-------------------------+----------+-----------+---------------+---------------------------------------------------+
| Selection_5             | 8000.00  | root      |               | eq(truncate(cast(test.t.a, double BINARY), 0), 1) |
| └─TableReader_7         | 10000.00 | root      |               | data:TableFullScan_6                              |
|   └─TableFullScan_6     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo                    |
+-------------------------+----------+-----------+---------------+---------------------------------------------------+
```

在此查询中，存在谓词 `truncate(a, " ") = '1'`。

从 `explain` 结果可以看出，该谓词未被下推到 TiKV 进行计算。这是因为 TiKV 的协处理器不支持内置函数 `truncate`。

### 案例 5：内表在外连接中的谓词不能下推

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
|   └─TableReader_11(Probe)     | 10000.00 | root      |               | data:TableFullScan_10                          |
|     └─TableFullScan_10        | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo                  |
+-------------------------------+----------+-----------+---------------+-------------------------------------------------+
6 rows in set (0.00 sec)
```

在此查询中，存在谓词 `s.a is null`，作用于内表 `s`。

从 `explain` 结果可以看出，该谓词未被下推到连接操作符以下。这是因为外连接在未满足 `on` 条件时，会用 `NULL` 填充内表的对应列，`s.a is null` 用于在连接后过滤结果。如果将其下推到内表以下，得到的执行计划将不等同于原始计划。

### 案例 6：包含用户变量的谓词不能下推

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

在此查询中，存在谓词 `a < @a`，其中 `@a` 为用户变量。

从 `explain` 结果可以看出，该谓词未像案例 2 那样被简化为 `a < 1` 并下推到 TiKV。这是因为用户变量 `@a` 的值在计算过程中可能会发生变化，TiKV 不会感知到这些变化。因此，TiDB 不会用具体值替换 `@a`，也不会将其下推到 TiKV。

一个示例帮助理解如下：

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

由此可见，`@a` 的值在查询过程中会发生变化。因此，如果将 `a = @a` 替换为 `a = 1` 并下推到 TiKV，得到的执行计划将不等同于原始计划。