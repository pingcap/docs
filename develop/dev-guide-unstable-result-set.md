---
title: 不稳定的结果集
summary: 学习如何处理不稳定的结果集错误。
---

# 不稳定的结果集

本文档描述了如何解决不稳定的结果集错误。

## GROUP BY

为了方便起见，MySQL “扩展” 了 `GROUP BY` 语法，允许 `SELECT` 子句引用未在 `GROUP BY` 子句中声明的非聚合字段，即所谓的 `NON-FULL GROUP BY` 语法。在其他数据库中，这被视为语法 **_错误_**，因为它会导致不稳定的结果集。

例如，你有两个表：

- `stu_info` 存储学生信息
- `stu_score` 存储学生考试成绩。

然后你可以写出如下的 SQL 查询语句：

```sql
SELECT
    `a`.`class`,
    `a`.`stuname`,
    max( `b`.`courscore` )
FROM
    `stu_info` `a`
    JOIN `stu_score` `b` ON `a`.`stuno` = `b`.`stuno`
GROUP BY
    `a`.`class`,
    `a`.`stuname`
ORDER BY
    `a`.`class`,
    `a`.`stuname`;
```

结果：

```sql
+------------+--------------+------------------+
| class      | stuname      | max(b.courscore) |
+------------+--------------+------------------+
| 2018_CS_01 | MonkeyDLuffy |             95.5 |
| 2018_CS_03 | PatrickStar  |             99.0 |
| 2018_CS_03 | SpongeBob    |             95.0 |
+------------+--------------+------------------+
3 rows in set (0.00 sec)
```

`a`.`class` 和 `a`.`stuname` 字段在 `GROUP BY` 语句中已明确指定，所选择的列为 `a`.`class`、`a`.`stuname` 和 `b`.`courscore`。唯一未在 `GROUP BY` 条件中的列 `b`.`courscore`，通过 `max()` 函数指定了唯一值。满足此 SQL 语句的 **_ONLY ONE_** 结果没有歧义，这被称为 `FULL GROUP BY` 语法。

反例是 `NON-FULL GROUP BY` 语法。例如，在这两个表中，写出以下 SQL 查询（删除 `a`.`stuname` 在 `GROUP BY` 中）：

```sql
SELECT
    `a`.`class`,
    `a`.`stuname`,
    max( `b`.`courscore` )
FROM
    `stu_info` `a`
    JOIN `stu_score` `b` ON `a`.`stuno` = `b`.`stuno`
GROUP BY
    `a`.`class`
ORDER BY
    `a`.`class`,
    `a`.`stuname`;
```

此时会返回两个符合此 SQL 的值。

第一个返回值：

```sql
+------------+--------------+------------------------+
| class      | stuname      | max( `b`.`courscore` ) |
+------------+--------------+------------------------+
| 2018_CS_01 | MonkeyDLuffy |                   95.5 |
| 2018_CS_03 | PatrickStar  |                   99.0 |
+------------+--------------+------------------------+
```

第二个返回值：

```sql
+------------+--------------+------------------+
| class      | stuname      | max(b.courscore) |
+------------+--------------+------------------+
| 2018_CS_01 | MonkeyDLuffy |             95.5 |
| 2018_CS_03 | SpongeBob    |             99.0 |
+------------+--------------+------------------+
```

出现两个结果的原因是你**_没有_** 指定如何获取 `a`.`stuname` 字段的值，两个结果都符合 SQL 语义，导致结果不稳定。因此，为了保证 `GROUP BY` 语句的结果稳定性，应使用 `FULL GROUP BY` 语法。

MySQL 提供了 `sql_mode` 开关 `ONLY_FULL_GROUP_BY` 来控制是否启用 `FULL GROUP BY` 语法。TiDB 也兼容此 `sql_mode` 开关。

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

**运行结果**：上述示例展示了在设置 `ONLY_FULL_GROUP_BY` 后的效果。

## ORDER BY

在 SQL 语义中，只有使用 `ORDER BY` 语法，结果集才会按指定顺序输出。对于单实例数据库，由于数据存储在同一台服务器上，多次执行的结果通常是稳定的（没有数据重排）。一些数据库（尤其是 MySQL 的 InnoDB 存储引擎）甚至可以按照主键或索引的顺序输出结果集。

作为分布式数据库，TiDB 将数据存储在多台服务器上。此外，TiDB 层不会缓存数据页，因此没有 `ORDER BY` 的 SQL 语句的结果集顺序很容易被感知为不稳定。为了输出有序的结果集，你需要显式在 `ORDER BY` 子句中添加排序字段，这符合 SQL 语义。

在以下示例中，只在 `ORDER BY` 中添加了一个字段，TiDB 仅按该字段排序结果。

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

当 `ORDER BY` 的值相同时，结果会不稳定。为了减少随机性，`ORDER BY` 的值应具有唯一性。如果不能保证唯一性，则需要添加更多的 `ORDER BY` 字段，直到 `ORDER BY` 字段的组合在排序中唯一，结果才会稳定。

## `GROUP_CONCAT()` 中未使用 `ORDER BY` 导致结果不稳定

结果集不稳定的原因是 TiDB 从存储层并行读取数据，因此没有 `ORDER BY` 的 `GROUP_CONCAT()` 返回的结果集顺序很容易被感知为不稳定。

为了让 `GROUP_CONCAT()` 按顺序输出结果集，你需要在 `ORDER BY` 子句中添加排序字段，这符合 SQL 语义。在以下示例中，`GROUP_CONCAT()` 拼接 `customer_id` 时未使用 `ORDER BY`，导致结果集不稳定。

1. 不包含 `ORDER BY`

    第一次查询：

    
    ```sql
    mysql>  select GROUP_CONCAT( customer_id SEPARATOR ',' ) FROM customer where customer_id like '200002%';
    +-------------------------------------------------------------------------+
    | GROUP_CONCAT(customer_id  SEPARATOR ',')                                |
    +-------------------------------------------------------------------------+
    | 20000200992,20000200993,20000200994,20000200995,20000200996,20000200... |
    +-------------------------------------------------------------------------+
    ```

    第二次查询：

    
    ```sql
    mysql>  select GROUP_CONCAT( customer_id SEPARATOR ',' ) FROM customer where customer_id like '200002%';
    +-------------------------------------------------------------------------+
    | GROUP_CONCAT(customer_id  SEPARATOR ',')                                |
    +-------------------------------------------------------------------------+
    | 20000203040,20000203041,20000203042,20000203043,20000203044,20000203... |
    +-------------------------------------------------------------------------+
    ```

2. 包含 `ORDER BY`

    第一次查询：

    
    ```sql
    mysql>  select GROUP_CONCAT( customer_id order by customer_id SEPARATOR ',' ) FROM customer where customer_id like '200002%';
    +-------------------------------------------------------------------------+
    | GROUP_CONCAT(customer_id  SEPARATOR ',')                                |
    +-------------------------------------------------------------------------+
    | 20000200000,20000200001,20000200002,20000200003,20000200004,20000200... |
    +-------------------------------------------------------------------------+
    ```

    第二次查询：

    
    ```sql
    mysql>  select GROUP_CONCAT( customer_id order by customer_id SEPARATOR ',' ) FROM customer where customer_id like '200002%';
    +-------------------------------------------------------------------------+
    | GROUP_CONCAT(customer_id  SEPARATOR ',')                                |
    +-------------------------------------------------------------------------+
    | 20000200000,20000200001,20000200002,20000200003,20000200004,20000200... |
    +-------------------------------------------------------------------------+
    ```

## 在 `SELECT * FROM T LIMIT N` 中结果不稳定

返回的结果与存储节点（TiKV）上的数据分布有关。如果执行多次查询，不同存储单元（Region）返回结果的速度不同，可能导致结果不稳定。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>