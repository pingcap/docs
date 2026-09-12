---
title: SUM
summary: 计算一组值的总和。
---

# SUM

计算一组值的总和。

- 空值会被忽略。
- 支持数值和 interval 类型。

## 语法 {#syntax}

```sql
SUM(<expr>)
```

## 返回类型 {#return-type}

与输入类型相同。

## 示例 {#examples}

以下示例演示了如何创建一个包含 INTEGER、DOUBLE 和 INTERVAL 列的表，插入数据，并使用 SUM 计算每一列的总和：

```sql
-- Create a table with integer, double, and interval columns
CREATE TABLE sum_example (
    id INT,
    int_col INTEGER,
    double_col DOUBLE,
    interval_col INTERVAL
);

-- Insert data
INSERT INTO sum_example VALUES
(1, 10, 15.5, INTERVAL '2 days'),
(2, 20, 25.7, INTERVAL '3 days'),
(3, NULL, 5.2, INTERVAL '1 day'),
(4, 30, 40.1, INTERVAL '4 days');

-- Calculate the sum for each column
SELECT
    SUM(int_col) AS total_integer,
    SUM(double_col) AS total_double,
    SUM(interval_col) AS total_interval
FROM sum_example;
```

预期输出：

```sql
-- NULL values are ignored.
-- SUM(interval_col) returns 240:00:00 (10 days).

┌──────────────────────────────────────────────────────────┐
│  total_integer  │    total_double   │   total_interval   │
├─────────────────┼───────────────────┼────────────────────┤
│              60 │              86.5 │ 240:00:00          │
└──────────────────────────────────────────────────────────┘
```