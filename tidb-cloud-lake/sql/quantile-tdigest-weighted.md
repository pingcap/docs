---
title: QUANTILE_TDIGEST_WEIGHTED
summary: 使用 [t-digest](https://github.com/tdunning/t-digest/blob/master/docs/t-digest-paper/histo.pdf) 算法计算数值数据序列的近似分位数。该函数会考虑序列中每个成员的权重。内存消耗为 log(n)，其中 n 是值的数量。
---

# QUANTILE_TDIGEST_WEIGHTED

使用 [t-digest](https://github.com/tdunning/t-digest/blob/master/docs/t-digest-paper/histo.pdf) 算法计算数值数据序列的近似分位数。

该函数会考虑序列中每个成员的权重。内存消耗为 **log(n)**，其中 **n** 是值的数量。

> **注意：**
>
> 计算时不包含 NULL 值。

## 语法 {#syntax}

```sql
QUANTILE_TDIGEST_WEIGHTED(<level1>[, <level2>, ...])(<expr>, <weight_expr>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|-----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| `<level n>`     | 分位数级别，表示一个范围从 0 到 1 的常数浮点数。建议使用 [0.01, 0.99] 范围内的级别值。 |
| `<expr>`        | 任意数值表达式 |
| `<weight_expr>` | 任意无符号整数表达式。权重表示某个值出现的次数。 |

## 返回类型 {#return-type}

根据指定的分位数级别数量，返回一个 Float64 值或一个 Float64 数组。

## 示例 {#example}

```sql
-- Create a table and insert sample data
CREATE TABLE sales_data (
  id INT,
  sales_person_id INT,
  sales_amount FLOAT
);

INSERT INTO sales_data (id, sales_person_id, sales_amount)
VALUES (1, 1, 5000),
       (2, 2, 5500),
       (3, 3, 6000),
       (4, 4, 6500),
       (5, 5, 7000);

SELECT QUANTILE_TDIGEST_WEIGHTED(0.5)(sales_amount, 1) AS median_sales_amount
FROM sales_data;

median_sales_amount|
-------------------+
             6000.0|

SELECT QUANTILE_TDIGEST_WEIGHTED(0.5, 0.8)(sales_amount, 1)
FROM sales_data;

quantile_tdigest_weighted(0.5, 0.8)(sales_amount)|
-------------------------------------------------+
[6000.0,7000.0]                                  |
```