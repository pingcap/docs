---
title: 连接重排序（Join Reorder）简介
summary: 使用连接重排序算法在 TiDB 中对多个表进行连接。
---

# 连接重排序（Join Reorder）简介

在实际应用场景中，常常需要对多个表进行连接。连接的执行效率与每个表连接的顺序密切相关。

例如：


```sql
SELECT * FROM t1, t2, t3 WHERE t1.a=t2.a AND t3.a=t2.a;
```

在这个查询中，表可以按照以下两种顺序进行连接：

- t1 先连接 t2，然后再连接 t3
- t2 先连接 t3，然后再连接 t1

由于 t1 和 t3 的数据量和分布不同，这两种执行顺序可能会表现出不同的性能。

因此，优化器需要一种算法来确定连接顺序。目前，TiDB 中使用以下两种连接重排序算法：

- 贪心算法（Greedy Algorithm）：在所有参与连接的节点中，TiDB 选择行数最少的表，估算其与其他每个表的连接结果，然后选择连接结果最小的那一对。之后，TiDB 继续类似的过程，选择并连接其他节点，直到所有节点都完成连接。
- 动态规划算法（Dynamic Programming Algorithm）：在所有参与连接的节点中，TiDB 枚举所有可能的连接顺序，并选择最优的连接顺序。

## 例子：连接重排序的贪心算法

以前述的三个表（t1、t2 和 t3）为例。

首先，TiDB 获取所有参与连接的节点，并按行数升序排序。

![join-reorder-1](/media/join-reorder-1.png)

然后，选择行数最少的表，并分别与其他两个表进行连接。通过比较输出结果集的大小，TiDB 选择结果集较小的那一对。

![join-reorder-2](/media/join-reorder-2.png)

接着，TiDB 进入下一轮选择。如果要连接四个表，TiDB 会继续比较输出结果集的大小，选择结果集较小的那一对。

在本例中只连接了三个表，因此 TiDB 得到最终的连接结果。

![join-reorder-3](/media/join-reorder-3.png)

## 例子：连接重排序的动态规划算法

再次以前述的三个表（t1、t2 和 t3）为例，动态规划算法可以枚举所有可能性。因此，与必须从 `t1` 表（行数最少的表）开始的贪心算法相比，动态规划算法可以枚举出如下的连接顺序：

![join-reorder-4](/media/join-reorder-4.png)

当这个选择优于贪心算法时，动态规划算法可以选择更优的连接顺序。

由于枚举了所有可能性，动态规划算法的计算时间更长，也更依赖统计信息。

## 连接重排序算法的选择

TiDB 中连接重排序算法的选择由 [`tidb_opt_join_reorder_threshold`](/system-variables.md#tidb_opt_join_reorder_threshold) 变量控制。如果参与连接的节点数大于此阈值，TiDB 将使用贪心算法；否则，使用动态规划算法。

## 连接重排序算法的限制

当前的连接重排序算法存在以下限制：

- 由于结果集计算方法的限制，算法不能确保选择最优的连接顺序。
- 连接重排序算法对 Outer Join 的支持由 [`tidb_enable_outer_join_reorder`](/system-variables.md#tidb_enable_outer_join_reorder-new-in-v610) 系统变量控制。
- 目前，动态规划算法不能对 outer join 进行连接重排序。

目前，TiDB 支持 `STRAIGHT_JOIN` 语法以强制指定连接顺序。更多信息请参考 [语法元素的描述](/sql-statements/sql-statement-select.md#description-of-the-syntax-elements)。