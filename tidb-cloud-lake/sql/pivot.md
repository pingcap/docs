---
title: PIVOT
summary: {{{ .lake }}} 中的 PIVOT 操作允许你通过旋转表并基于指定列聚合结果来转换表。
---

# PIVOT

{{{ .lake }}} 中的 `PIVOT` 操作允许你通过旋转表并基于指定列聚合结果来转换表。

它是一个非常有用的操作，可以用更易读的格式对大量数据进行汇总和分析。本文将介绍其语法，并提供一个如何使用 `PIVOT` 操作的示例。

**另请参阅：** [UNPIVOT](/tidb-cloud-lake/sql/unpivot.md)

## 语法 {#syntax}

```sql
SELECT ...
FROM ...
   PIVOT ( <aggregate_function> ( <pivot_column> )
            FOR <value_column> IN ( <pivot_value_1> [ , <pivot_value_2> ... ] ) )

[ ... ]
```

其中：

* `<aggregate_function>`：用于合并来自 `pivot_column` 的分组值的聚合函数。
* `<pivot_column>`：将使用指定的 `<aggregate_function>` 进行聚合的列。
* `<value_column>`：其唯一值将在透视结果集中成为新列的列。
* `<pivot_value_N>`：来自 `<value_column>` 的一个唯一值，它将在透视结果集中成为一个新列。

## 示例 {#examples}

假设我们有一个名为 monthly_sales 的表，其中包含不同员工在不同月份的销售数据。我们可以使用 `PIVOT` 操作来汇总这些数据，并计算每位员工在每个月的销售总额。

### 创建并插入数据 {#creating-and-inserting-data}

```sql
-- Create the monthly_sales table
CREATE TABLE monthly_sales(
  empid INT,
  amount INT,
  month VARCHAR
);

-- Insert sales data
INSERT INTO monthly_sales VALUES
  (1, 10000, 'JAN'),
  (1, 400, 'JAN'),
  (2, 4500, 'JAN'),
  (2, 35000, 'JAN'),
  (1, 5000, 'FEB'),
  (1, 3000, 'FEB'),
  (2, 200, 'FEB'),
  (2, 90500, 'FEB'),
  (1, 6000, 'MAR'),
  (1, 5000, 'MAR'),
  (2, 2500, 'MAR'),
  (2, 9500, 'MAR'),
  (1, 8000, 'APR'),
  (1, 10000, 'APR'),
  (2, 800, 'APR'),
  (2, 4500, 'APR');
```

### 使用 PIVOT {#using-pivot}

现在，我们可以使用 `PIVOT` 操作来计算每位员工在每个月的销售总额。我们将使用 `SUM` 聚合函数来计算销售总额，并将 MONTH 列进行透视，为每个月创建一个新列。

```sql
SELECT *
FROM monthly_sales
PIVOT(SUM(amount) FOR MONTH IN ('JAN', 'FEB', 'MAR', 'APR'))
ORDER BY EMPID;
```

输出：

```sql
+-------+-------+-------+-------+-------+
| empid | jan   | feb   | mar   | apr   |
+-------+-------+-------+-------+-------+
|     1 | 10400 |  8000 | 11000 | 18000 |
|     2 | 39500 | 90700 | 12000 |  5300 |
+-------+-------+-------+-------+-------+
```