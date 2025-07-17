---
title: 优化规则黑名单与表达式下推
summary: 了解关于控制优化规则和表达式下推行为的黑名单机制。
---

# 优化规则黑名单与表达式下推

本文介绍如何使用优化规则黑名单和表达式下推黑名单来控制 TiDB 的行为。

## 优化规则黑名单

优化规则黑名单是一种调优优化规则的方法，主要用于手动禁用某些优化规则。

### 重要的优化规则

|**优化规则**|**规则名称**|**描述**|
| :--- | :--- | :--- |
| 列裁剪 | column_prune | 如果上层执行器不需要某列，则会裁剪该列。 |
| 去相关子查询 | decorrelate | 尝试将相关子查询重写为非相关的连接或聚合。 |
| 聚合消除 | aggregation_eliminate | 尝试从执行计划中移除不必要的聚合操作符。 |
| 投影消除 | projection_eliminate | 移除执行计划中不必要的投影操作符。 |
| Max/Min 消除 | max_min_eliminate | 将某些 Max/Min 函数重写为 `order by` + `limit 1` 形式。 |
| predicate 下推 | predicate_push_down | 尝试将谓词下推到更接近数据源的操作符。 |
| 外连接消除 | outer_join_eliminate | 尝试移除执行计划中不必要的左连接或右连接。 |
| 分区裁剪 | partition_processor | 裁剪被谓词拒绝的分区，并将分区表查询重写为 `UnionAll + Partition Datasource` 形式。 |
| 聚合下推 | aggregation_push_down | 尝试将聚合操作下推到其子节点。 |
| TopN 下推 | topn_push_down | 尝试将 TopN 操作符下推到更接近数据源的位置。 |
| 连接重排序 | join_reorder | 决定多表连接的执行顺序。 |
| 从窗口函数派生 TopN 或 Limit | derive_topn_from_window | 从窗口函数中派生出 TopN 或 Limit 操作符。 |

### 禁用优化规则

你可以使用优化规则黑名单禁用某些规则，以避免某些规则导致的特殊查询执行计划不理想。

#### 使用方法

> **注意：**
>
> 以下所有操作都需要拥有数据库的 `super privilege` 权限。每个优化规则都有一个名称，例如，列裁剪的名称是 `column_prune`。所有优化规则的名称可以在表 [重要优化规则](#important-optimization-rules) 的第二列中找到。

- 如果你想禁用某些规则，可以将其名称写入 `mysql.opt_rule_blacklist` 表。例如：

    
    ```sql
    INSERT INTO mysql.opt_rule_blacklist VALUES("join_reorder"), ("topn_push_down");
    ```

    执行以下 SQL 语句可以立即生效。生效范围包括所有旧连接的 TiDB 实例：

    
    ```sql
    admin reload opt_rule_blacklist;
    ```

    > **注意：**
    >
    > `admin reload opt_rule_blacklist` 只在执行该语句的 TiDB 服务器上生效。如果希望集群中的所有 TiDB 服务器都生效，需要在每个 TiDB 服务器上执行此命令。

- 如果想重新启用某个规则，可以删除对应的表中的数据，然后运行 `admin reload` 语句：

    
    ```sql
    DELETE FROM mysql.opt_rule_blacklist WHERE name IN ("join_reorder", "topn_push_down");
    ```

    
    ```sql
    admin reload opt_rule_blacklist;
    ```

## 表达式下推黑名单

表达式下推黑名单是一种调优表达式下推的方法，主要用于手动禁用某些特定数据类型的表达式。

### 支持下推的表达式

关于支持下推到 TiKV 的表达式的详细信息，请参见 [Supported expressions for pushdown to TiKV](/functions-and-operators/expressions-pushed-down.md#supported-expressions-for-pushdown-to-tikv)。

### 禁用特定表达式的下推

当因表达式下推导致结果错误时，你可以使用黑名单快速恢复应用的正确性。具体来说，可以将部分支持的函数或操作符添加到 `mysql.expr_pushdown_blacklist` 表中，以禁用特定表达式的下推。

`mysql.expr_pushdown_blacklist` 表的结构如下：

```sql
DESC mysql.expr_pushdown_blacklist;
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

每个字段的说明如下：

+ `name`：被禁用下推的函数或操作符的名称。
+ `store_type`：指定你希望阻止该函数在何种组件中被下推计算。可用的组件有 `tidb`、`tikv` 和 `tiflash`。`store_type` 不区分大小写。如果需要指定多个组件，用逗号分隔。
    - 当 `store_type` 为 `tidb` 时，表示在读取 TiDB 内存表时，是否允许在其他 TiDB 服务器上执行该函数。
    - 当 `store_type` 为 `tikv` 时，表示是否允许在 TiKV 服务器的 Coprocessor 组件中执行该函数。
    - 当 `store_type` 为 `tiflash` 时，表示是否允许在 TiFlash 服务器的 Coprocessor 组件中执行该函数。
+ `reason`：记录将该函数加入黑名单的原因。

### 使用方法

本节介绍如何使用表达式下推黑名单。

#### 添加到黑名单

将一个或多个表达式（函数或操作符）加入黑名单，步骤如下：

1. 将对应的函数名或操作符名，以及你希望禁用下推的组件集，插入到 `mysql.expr_pushdown_blacklist` 表中。

2. 执行 `admin reload expr_pushdown_blacklist`。

#### 从黑名单中移除

将一个或多个表达式从黑名单中移除，步骤如下：

1. 从 `mysql.expr_pushdown_blacklist` 表中删除对应的函数名或操作符名，以及你希望禁用下推的组件集。

2. 执行 `admin reload expr_pushdown_blacklist`。

> **注意：**
>
> `admin reload expr_pushdown_blacklist` 只在执行该语句的 TiDB 服务器上生效。如果希望集群中的所有 TiDB 服务器都生效，需要在每个 TiDB 服务器上执行此命令。

## 表达式黑名单使用示例

以下示例中，将 `<` 和 `>` 操作符加入黑名单，然后将 `>` 操作符从黑名单中移除。

为了判断黑名单是否生效，可以观察 `EXPLAIN` 的结果（详见 [TiDB 查询执行计划概述](/explain-overview.md)）。

1. 以下 SQL 语句的 `WHERE` 子句中的谓词 `a < 2` 和 `a > 2` 可以被下推到 TiKV。

    
    ```sql
    EXPLAIN SELECT * FROM t WHERE a < 2 AND a > 2;
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

2. 将表达式插入到 `mysql.expr_pushdown_blacklist` 表中，并执行 `admin reload expr_pushdown_blacklist`。

    
    ```sql
    INSERT INTO mysql.expr_pushdown_blacklist VALUES('<','tikv',''), ('>','tikv','');
    ```

    ```sql
    Query OK, 2 rows affected (0.01 sec)
    Records: 2  Duplicates: 0  Warnings: 0
    ```

    
    ```sql
    admin reload expr_pushdown_blacklist;
    ```

    ```sql
    Query OK, 0 rows affected (0.00 sec)
    ```

3. 再次观察执行计划，发现 `<` 和 `>` 操作符都没有被下推到 TiKV Coprocessor。

    
    ```sql
    EXPLAIN SELECT * FROM t WHERE a < 2 and a > 2;
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

4. 从黑名单中移除一个表达式（这里是 `>`），并执行 `admin reload expr_pushdown_blacklist`。

    
    ```sql
    DELETE FROM mysql.expr_pushdown_blacklist WHERE name = '>';
    ```

    ```sql
    Query OK, 1 row affected (0.01 sec)
    ```

    
    ```sql
    admin reload expr_pushdown_blacklist;
    ```

    ```sql
    Query OK, 0 rows affected (0.00 sec)
    ```

5. 再次观察执行计划，发现 `<` 不被下推，而 `>` 被下推到 TiKV Coprocessor。

    
    ```sql
    EXPLAIN SELECT * FROM t WHERE a < 2 AND a > 2;
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
    ```