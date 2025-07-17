---
title: TopN and Limit Operator Push Down
summary: 了解 TopN 和 Limit 操作符下推的实现方式。
---

# TopN 和 Limit 操作符下推

本文档描述了 TopN 和 Limit 操作符下推的实现。

在 TiDB 执行计划树中，SQL 中的 `LIMIT` 子句对应 Limit 操作符节点，`ORDER BY` 子句对应 Sort 操作符节点。相邻的 Limit 操作符和 Sort 操作符会合并为 TopN 操作符节点，表示根据某种排序规则返回前 N 条记录。也就是说，Limit 操作符等同于一个排序规则为空的 TopN 操作符节点。

类似于谓词下推，TopN 和 Limit 会被下推到执行计划树中尽可能靠近数据源的位置，以便在早期对所需数据进行过滤。这样，推下可以显著减少数据传输和计算的开销。

若要禁用此规则，请参考 [Expression Pushdown 的优化规则和黑名单](/blocklist-control-plan.md)。

## 示例

本节通过一些示例说明 TopN 下推的过程。

### 示例 1：下推到存储层的协处理器（Coprocessors）


```sql
create table t(id int primary key, a int not null);
explain select * from t order by a limit 10;
```

```
+----------------------------+----------+-----------+---------------+--------------------------------+
| id                         | estRows  | task      | access object | operator info                  |
+----------------------------+----------+-----------+---------------+--------------------------------+
| TopN_7                     | 10.00    | root      |               | test.t.a, offset:0, count:10   |
| └─TableReader_15           | 10.00    | root      |               | data:TopN_14                   |
|   └─TopN_14                | 10.00    | cop[tikv] |               | test.t.a, offset:0, count:10   |
|     └─TableFullScan_13     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo |
+----------------------------+----------+-----------+---------------+--------------------------------+
```

在此查询中，TopN 操作符节点被下推到 TiKV 进行数据过滤，每个协处理器（Coprocessor）只返回 10 条记录到 TiDB。TiDB 汇总数据后，进行最终过滤。

### 示例 2：TopN 可以下推到 Join（排序规则仅依赖外表中的列）


```sql
create table t(id int primary key, a int not null);
create table s(id int primary key, a int not null);
explain select * from t left join s on t.a = s.a order by t.a limit 10;
```

```
+----------------------------------+----------+-----------+---------------+-------------------------------------------------+
| id                               | estRows  | task      | access object | operator info                                   |
+----------------------------------+----------+-----------+---------------+-------------------------------------------------+
| TopN_12                          | 10.00    | root      |               | test.t.a, offset:0, count:10                    |
| └─HashJoin_17                    | 12.50    | root      |               | left outer join, equal:[eq(test.t.a, test.s.a)] |
|   ├─TopN_18(Build)               | 10.00    | root      |               | test.t.a, offset:0, count:10                    |
|   │ └─TableReader_26             | 10.00    | root      |               | data:TopN_25                                    |
|   │   └─TopN_25                  | 10.00    | cop[tikv] |               | test.t.a, offset:0, count:10                    |
|   │     └─TableFullScan_24       | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo                  |
|   └─TableReader_30(Probe)        | 10000.00 | root      |               | data:TableFullScan_29                           |
|     └─TableFullScan_29           | 10000.00 | cop[tikv] | table:s       | keep order:false, stats:pseudo                  |
+----------------------------------+----------+-----------+---------------+-------------------------------------------------+
```

在此查询中，TopN 操作符的排序规则仅依赖于外表 `t` 中的列，因此可以在下推 TopN 之前先进行计算，以减少 Join 操作的计算成本。此外，TiDB 也会将 TopN 下推到存储层。

### 示例 3：TopN 不能在 Join 之前下推


```sql
create table t(id int primary key, a int not null);
create table s(id int primary key, a int not null);
explain select * from t join s on t.a = s.a order by t.id limit 10;
```

```
+-------------------------------+----------+-----------+---------------+--------------------------------------------+
| id                            | estRows  | task      | access object | operator info                              |
+-------------------------------+----------+-----------+---------------+--------------------------------------------+
| TopN_12                       | 10.00    | root      |               | test.t.id, offset:0, count:10              |
| └─HashJoin_16                 | 12500.00 | root      |               | inner join, equal:[eq(test.t.a, test.s.a)] |
|   ├─TableReader_21(Build)     | 10000.00 | root      |               | data:TableFullScan_20                      |
|   │ └─TableFullScan_20        | 10000.00 | cop[tikv] | table:s       | keep order:false, stats:pseudo             |
|   └─TableReader_19(Probe)     | 10000.00 | root      |               | data:TableFullScan_18                      |
|     └─TableFullScan_18        | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo             |
+-------------------------------+----------+-----------+---------------+--------------------------------------------+
```

TopN 不能在 `Inner Join` 之前下推。以上述查询为例，如果 Join 后得到 100 条记录，TopN 后剩 10 条；但如果先执行 TopN 获取 10 条，再进行 Join，最后只剩 5 条。在这种情况下，下推会导致结果不同。

类似地，TopN 既不能下推到外连接（Outer Join）的内表，也不能在排序规则涉及多表列（如 `t.a + s.a`）时下推。只有当 TopN 的排序规则完全依赖于外表的列时，才能进行下推。

### 示例 4：将 TopN 转换为 Limit


```sql
create table t(id int primary key, a int not null);
create table s(id int primary key, a int not null);
explain select * from t left join s on t.a = s.a order by t.id limit 10;
```

```
+----------------------------------+----------+-----------+---------------+-------------------------------------------------+
| id                               | estRows  | task      | access object | operator info                                   |
+----------------------------------+----------+-----------+---------------+-------------------------------------------------+
| TopN_12                          | 10.00    | root      |               | test.t.id, offset:0, count:10                   |
| └─HashJoin_17                    | 12.50    | root      |               | left outer join, equal:[eq(test.t.a, test.s.a)] |
|   ├─Limit_21(Build)              | 10.00    | root      |               | offset:0, count:10                              |
|   │ └─TableReader_31             | 10.00    | root      |               | data:Limit_30                                   |
|   │   └─Limit_30                 | 10.00    | cop[tikv] |               | offset:0, count:10                              |
|   │     └─TableFullScan_29       | 10.00    | cop[tikv] | table:t       | keep order:true, stats:pseudo                   |
|   └─TableReader_35(Probe)        | 10000.00 | root      |               | data:TableFullScan_34                           |
|     └─TableFullScan_34           | 10000.00 | cop[tikv] | table:s       | keep order:false, stats:pseudo                  |
+----------------------------------+----------+-----------+---------------+-------------------------------------------------+
```

在上述查询中，TopN 首先被下推到外表 `t`。由于 TopN 需要根据 `t.id` 排序，而 `t.id` 是主键，可以直接按顺序读取（`keep order: true`），无需在 TopN 中额外排序。因此，TopN 被简化为 Limit。