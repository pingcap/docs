---
title: GROUP BY Modifiers
summary: 学习如何使用 TiDB 的 GROUP BY 修饰符。
---

# GROUP BY 修饰符

从 v7.4.0 版本开始，TiDB 的 `GROUP BY` 子句支持 `WITH ROLLUP` 修饰符。

在 `GROUP BY` 子句中，你可以指定一个或多个列作为分组列表，并在列表后面添加 `WITH ROLLUP` 修饰符。然后，TiDB 将基于分组列表中的列进行多维降序分组，并在输出中为每个分组提供汇总结果。

- 分组方法：

    - 第一个分组维度包括所有在分组列表中的列。
    - 后续的分组维度从分组列表的右端开始，每次排除一个列，形成新的分组。

- 聚合汇总：对于每个维度，查询执行聚合操作，然后将该维度的结果与之前所有维度的结果进行汇总。这意味着你可以获得不同维度的聚合数据，从详细到整体。

采用这种分组方法，如果分组列表中有 `N` 个列，TiDB 会在 `N+1` 个分组上进行结果的聚合。

例如：

```sql
SELECT count(1) FROM t GROUP BY a,b,c WITH ROLLUP;
```

在这个例子中，TiDB 会在 4 个分组（即 `{a, b, c}`、`{a, b}`、`{a}` 和 `{}`）上对 `count(1)` 的计算结果进行聚合，并输出每个分组的汇总结果。

> **Note:**
>
> 目前，TiDB 不支持 Cube 语法。

## 使用场景

对多列数据进行聚合和汇总，常用于 OLAP（联机分析处理）场景。通过使用 `WITH ROLLUP` 修饰符，你可以获得额外的行，显示来自其他高层维度的超级汇总信息。在此基础上，可以进行更高级的数据分析和报表生成。

## 前提条件

<CustomContent platform="tidb">

在 v8.3.0 版本之前，TiDB 仅支持在 [TiFlash MPP 模式](/tiflash/use-tiflash-mpp-mode.md)下生成 `WITH ROLLUP` 语法的有效执行计划。因此，你的 TiDB 集群需要包含 TiFlash 节点，并且目标表必须配置正确的 TiFlash 副本。更多信息请参见 [扩展 TiFlash 集群](/scale-tidb-using-tiup.md#scale-out-a-tiflash-cluster)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 v8.3.0 版本之前，TiDB 仅支持在 [TiFlash MPP 模式](/tiflash/use-tiflash-mpp-mode.md)下生成 `WITH ROLLUP` 语法的有效执行计划。因此，你的 TiDB 集群需要包含 TiFlash 节点，并且目标表必须配置正确的 TiFlash 副本。更多信息请参见 [更改节点数](/tidb-cloud/scale-tidb-cluster.md#change-node-number)。

</CustomContent>

从 v8.3.0 版本开始，以上限制被移除。无论你的 TiDB 集群是否包含 TiFlash 节点，TiDB 都支持生成 `WITH ROLLUP` 语法的有效执行计划。

要判断 `Expand` 操作符由 TiDB 还是 TiFlash 执行，可以检查执行计划中 `Expand` 操作符的 `task` 属性。更多信息请参见 [如何解读 ROLLUP 执行计划](#how-to-interpret-the-rollup-execution-plan)。

## 示例

假设你有一个名为 `bank` 的利润表，包含 `year`、`month`、`day` 和 `profit` 列。

```sql
CREATE TABLE bank
(
    year    INT,
    month   VARCHAR(32),
    day     INT,
    profit  DECIMAL(13, 7)
);

ALTER TABLE bank SET TIFLASH REPLICA 1; -- 为表添加 TiFlash 副本以支持 TiFlash MPP 模式。

INSERT INTO bank VALUES(2000, "Jan", 1, 10.3),(2001, "Feb", 2, 22.4),(2000,"Mar", 3, 31.6)
```

要获取每年银行的利润，可以使用如下简单的 `GROUP BY` 子句：

```sql
SELECT year, SUM(profit) AS profit FROM bank GROUP BY year;
+------+--------------------+
| year | profit             |
+------+--------------------+
| 2001 | 22.399999618530273 |
| 2000 |  41.90000057220459 |
+------+--------------------+
2 rows in set (0.15 sec)
```

除了年度利润外，银行报告通常还需要包括所有年份的总利润或按月划分的详细利润，以便进行更细致的利润分析。在 v7.4.0 之前，你需要在多个查询中使用不同的 `GROUP BY` 子句，并通过 UNION 连接结果以获得汇总。自 v7.4.0 起，你可以在单个查询中通过在 `GROUP BY` 后添加 `WITH ROLLUP` 来实现。

```sql
SELECT year, month, SUM(profit) AS profit from bank GROUP BY year, month WITH ROLLUP ORDER BY year desc, month desc;
+------+-------+--------------------+
| year | month | profit             |
+------+-------+--------------------+
| 2001 | Feb   | 22.399999618530273 |
| 2001 | NULL  | 22.399999618530273 |
| 2000 | Mar   | 31.600000381469727 |
| 2000 | Jan   | 10.300000190734863 |
| 2000 | NULL  |  41.90000057220459 |
| NULL | NULL  |  64.30000019073486 |
+------+-------+--------------------+
6 rows in set (0.025 sec)
```

上述结果包含不同维度的聚合数据：按年和月、按年、以及整体。在结果中，没有 `NULL` 的行表示该行的 `profit` 是通过同时按年和月分组计算得出。`month` 列中的 `NULL` 表示该行的 `profit` 是按年汇总的所有月份的结果，而 `year` 列中的 `NULL` 表示所有年份的总和。

具体来说：

- 第一行的 `profit` 来自 2 维分组 `{year, month}`，代表细粒度 `{2000, "Jan"}` 组的聚合结果。
- 第二行的 `profit` 来自 1 维分组 `{year}`，代表中间层 `{2001}` 组的聚合结果。
- 最后一行的 `profit` 来自 0 维分组 `{}`，代表整体的聚合结果。

在 `WITH ROLLUP` 结果中，`NULL` 值是在应用聚合操作之前生成的。因此，你可以在 `SELECT`、`HAVING` 和 `ORDER BY` 子句中使用 `NULL` 来进一步筛选聚合结果。

例如，可以在 `HAVING` 子句中使用 `NULL` 来只筛选出 2 维分组的结果：

```sql
SELECT year, month, SUM(profit) AS profit FROM bank GROUP BY year, month WITH ROLLUP HAVING year IS NOT null AND month IS NOT null;
+------+-------+--------------------+
| year | month | profit             |
+------+-------+--------------------+
| 2000 | Mar   | 31.600000381469727 |
| 2000 | Jan   | 10.300000190734863 |
| 2001 | Feb   | 22.399999618530273 |
+------+-------+--------------------+
3 rows in set (0.02 sec)
```

注意，如果 `GROUP BY` 列表中的某个列本身包含原生 `NULL` 值，`WITH ROLLUP` 的聚合结果可能会误导查询结果。为解决此问题，可以使用 `GROUPING()` 函数区分原生 `NULL` 和由 `WITH ROLLUP` 生成的 `NULL`。该函数接受一个分组表达式作为参数，返回 `0` 或 `1`，以指示当前结果中该表达式是否被聚合。`1` 表示已聚合，`0` 表示未聚合。

以下示例演示如何使用 `GROUPING()` 函数：

```sql
SELECT year, month, SUM(profit) AS profit, grouping(year) as grp_year, grouping(month) as grp_month FROM bank GROUP BY year, month WITH ROLLUP ORDER BY year DESC, month DESC;
+------+-------+--------------------+----------+-----------+
| year | month | profit             | grp_year | grp_month |
+------+-------+--------------------+----------+-----------+
| 2001 | Feb   | 22.399999618530273 |        0 |         0 |
| 2001 | NULL  | 22.399999618530273 |        0 |         1 |
| 2000 | Mar   | 31.600000381469727 |        0 |         0 |
| 2000 | Jan   | 10.300000190734863 |        0 |         0 |
| 2000 | NULL  |  41.90000057220459 |        0 |         1 |
| NULL | NULL  |  64.30000019073486 |        1 |         1 |
+------+-------+--------------------+----------+-----------+
6 rows in set (0.028 sec)
```

从输出中可以直接通过 `grp_year` 和 `grp_month` 来理解每行的聚合维度，避免原生 `NULL` 值的干扰。

`GROUPING()` 函数最多接受 64 个分组表达式作为参数。在多参数输出中，每个参数会生成 `0` 或 `1`，这些参数共同组成一个 64 位的 `UNSIGNED LONGLONG`，每一位对应一个参数的值。可以用以下公式计算每个参数对应的位位置：

```go
GROUPING(day, month, year):
  result for GROUPING(year)
+ result for GROUPING(month) << 1
+ result for GROUPING(day) << 2
```

通过在 `GROUPING()` 中使用多个参数，可以高效地筛选任何高维度的聚合结果。例如，可以快速筛选每年及所有年份的聚合结果，使用 `GROUPING(year, month)`：

```sql
SELECT year, month, SUM(profit) AS profit, grouping(year) as grp_year, grouping(month) as grp_month FROM bank GROUP BY year, month WITH ROLLUP HAVING GROUPING(year, month) <> 0 ORDER BY year DESC, month DESC;
+------+-------+--------------------+----------+-----------+
| year | month | profit             | grp_year | grp_month |
+------+-------+--------------------+----------+-----------+
| 2001 | NULL  | 22.399999618530273 |        0 |         1 |
| 2000 | NULL  |  41.90000057220459 |        0 |         1 |
| NULL | NULL  |  64.30000019073486 |        1 |         1 |
+------+-------+--------------------+----------+-----------+
3 rows in set (0.023 sec)
```

## 如何解读 ROLLUP 执行计划

多维数据聚合使用 `Expand` 操作符复制数据，以满足多维分组的需求。每次数据复制对应一个特定维度的分组。在 MPP 模式下，`Expand` 操作符可以促进数据洗牌，快速在多个节点之间重组和计算大量数据，充分利用每个节点的计算能力。在没有 TiFlash 节点的 TiDB 集群中，由于 `Expand` 只在单个 TiDB 节点上执行，随着维度分组（`grouping set`）的增加，数据冗余也会增加。

`Expand` 操作符的实现类似于 `Projection` 操作符，不同之处在于 `Expand` 是多层次的 `Projection`，包含多层投影表达式。对于每一行原始数据，`Projection` 只生成一行结果，而 `Expand` 会生成多行（行数等于投影表达式的层数）。

以下示例展示了没有 TiFlash 节点的 TiDB 集群中的执行计划，其中 `Expand` 操作符的 `task` 为 `root`，表示在 TiDB 中执行：

```sql
EXPLAIN SELECT year, month, grouping(year), grouping(month), SUM(profit) AS profit FROM bank GROUP BY year, month WITH ROLLUP;
+--------------------------------+---------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id                             | estRows | task      | access object | operator info                                                                                                                                                                                                                        |
+--------------------------------+---------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Projection_7                   | 2.40    | root      |               | Column#6->Column#12, Column#7->Column#13, grouping(gid)->Column#14, grouping(gid)->Column#15, Column#9->Column#16                                                                                                                    |
| └─HashAgg_8                    | 2.40    | root      |               | group by:Column#6, Column#7, gid, funcs:sum(test.bank.profit)->Column#9, funcs:firstrow(Column#6)->Column#6, funcs:firstrow(Column#7)->Column#7, funcs:firstrow(gid)->gid                                                            |
|   └─Expand_12                  | 3.00    | root      |               | level-projection:[test.bank.profit, <nil>->Column#6, <nil>->Column#7, 0->gid],[test.bank.profit, Column#6, <nil>->Column#7, 1->gid],[test.bank.profit, Column#6, Column#7, 3->gid]; schema: [test.bank.profit,Column#6,Column#7,gid] |
|     └─Projection_14            | 3.00    | root      |               | test.bank.profit, test.bank.year->Column#6, test.bank.month->Column#7                                                                                                                                                                |
|       └─TableReader_16         | 3.00    | root      |               | data:TableFullScan_15                                                                                                                                                                                                                |
|         └─TableFullScan_15     | 3.00    | cop[tikv] | table:bank    | keep order:false, stats:pseudo                                                                                                                                                                                                       |
+--------------------------------+---------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
6 rows in set (0.00 sec)
```

以下示例展示了在 TiFlash MPP 模式下的执行计划，其中 `Expand` 操作符的 `task` 为 `mpp[tiflash]`，表示在 TiFlash 中执行：

```sql
EXPLAIN SELECT year, month, grouping(year), grouping(month), SUM(profit) AS profit FROM bank GROUP BY year, month WITH ROLLUP;
+----------------------------------------+---------+--------------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id                                     | estRows | task         | access object | operator info                                                                                                                                                                                                                        |
+----------------------------------------+---------+--------------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| TableReader_44                         | 2.40    | root         |               | MppVersion: 2, data:ExchangeSender_43                                                                                                                                                                                                |
| └─ExchangeSender_43                    | 2.40    | mpp[tiflash] |               | ExchangeType: PassThrough                                                                                                                                                                                                            |
|   └─Projection_8                       | 2.40    | mpp[tiflash] |               | Column#6->Column#12, Column#7->Column#13, grouping(gid)->Column#14, grouping(gid)->Column#15, Column#9->Column#16                                                                                                                    |
|     └─Projection_38                    | 2.40    | mpp[tiflash] |               | Column#9, Column#6, Column#7, gid                                                                                                                                                                                                    |
|       └─HashAgg_36                     | 2.40    | mpp[tiflash] |               | group by:Column#6, Column#7, gid, funcs:sum(test.bank.profit)->Column#9, funcs:firstrow(Column#6)->Column#6, funcs:firstrow(Column#7)->Column#7, funcs:firstrow(gid)->gid, stream_count: 8                                           |
|         └─ExchangeReceiver_22          | 3.00    | mpp[tiflash] |               | stream_count: 8                                                                                                                                                                                                                      |
|           └─ExchangeSender_21          | 3.00    | mpp[tiflash] |               | ExchangeType: HashPartition, Compression: FAST, Hash Cols: [name: Column#6, collate: binary], [name: Column#7, collate: utf8mb4_bin], [name: gid, collate: binary], stream_count: 8                                                  |
|             └─Expand_20                | 3.00    | mpp[tiflash] |               | level-projection:[test.bank.profit, <nil>->Column#6, <nil>->Column#7, 0->gid],[test.bank.profit, Column#6, <nil>->Column#7, 1->gid],[test.bank.profit, Column#6, Column#7, 3->gid]; schema: [test.bank.profit,Column#6,Column#7,gid] |
|               └─Projection_16          | 3.00    | mpp[tiflash] |               | test.bank.profit, test.bank.year->Column#6, test.bank.month->Column#7                                                                                                                                                                |
|                 └─TableFullScan_17     | 3.00    | mpp[tiflash] | table:bank    | keep order:false, stats:pseudo                                                                                                                                                                                                       |
+----------------------------------------+---------+--------------+---------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
10 rows in set (0.05 sec)
```

在此执行计划示例中，你可以在 `Expand_20` 行的 `operator info` 列中看到 `Expand` 操作符的多层表达式。它由 2 维表达式组成，你可以在该行末尾看到 `schema: [test.bank.profit, Column#6, Column#7, gid]`，这是 `Expand` 操作符的 schema 信息。

在 `Expand` 操作符的 schema 信息中，`GID` 被作为额外的列生成。其值由 `Expand` 操作符根据不同维度的分组逻辑计算得出，反映了当前数据副本与 `grouping set` 之间的关系。在大多数情况下，`Expand` 使用位与操作（Bit-And），可以表示 63 种分组项的组合，对应 64 个分组维度。在此模式下，TiDB 根据当前数据副本是否包含所需维度的分组表达式，生成 `GID` 值，并以列的顺序填充一个 64 位的 `UINT64`。

在前述示例中，分组列表的列顺序为 `[year, month]`，由 ROLLUP 语法生成的维度组为 `{year, month}`、`{year}` 和 `{}`。对于 `{year, month}` 维度组，`year` 和 `month` 都是必需列，因此 TiDB 会将它们对应的位位置填充为 1 和 1，形成十进制为 3 的 `UINT64`（二进制为 `11...0`）。因此，投影表达式为 `[test.bank.profit, Column#6, Column#7, 3->gid]`（其中 `column#6` 对应 `year`，`column#7` 对应 `month`）。

以下是原始数据的一行示例：

```sql
+------+-------+------+------------+
| year | month | day  | profit     |
+------+-------+------+------------+
| 2000 | Jan   |    1 | 10.3000000 |
+------+-------+------+------------+
```

经过 `Expand` 操作符后，可以得到以下三行结果：

```sql
+------------+------+-------+-----+
| profit     | year | month | gid |
+------------+------+-------+-----+
| 10.3000000 | 2000 | Jan   |  3  |
| 10.3000000 | 2000 | NULL  |  1  |
| 10.3000000 | NULL | NULL  |  0  |
+------------+------+-------+-----+
```

注意，查询中的 `SELECT` 子句使用了 `GROUPING` 函数。当在 `SELECT`、`HAVING` 或 `ORDER BY` 子句中使用 `GROUPING` 时，TiDB 会在逻辑优化阶段对其进行重写，将 `GROUPING` 函数与 `GROUP BY` 项之间的关系转换为与维度分组（也称为 `grouping set`）相关的 `GID`，并将此 `GID` 作为元数据填充到新的 `GROUPING` 函数中。