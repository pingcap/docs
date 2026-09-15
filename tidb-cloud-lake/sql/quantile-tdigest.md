---
title: QUANTILE_TDIGEST
summary: 使用 t-digest 算法计算数值数据序列的近似分位数。
---

# QUANTILE_TDIGEST

使用 [t-digest](https://github.com/tdunning/t-digest/blob/master/docs/t-digest-paper/histo.pdf) 算法计算数值数据序列的近似分位数。

> **注意：**
>
> 计算中不包含 NULL 值。

## 语法 {#syntax}

```sql
QUANTILE_TDIGEST(<level1>[, <level2>, ...])(<expr>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|-------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| `<level n>` | 分位数级别表示一个范围从 0 到 1 的浮点常数。建议使用 [0.01, 0.99] 范围内的级别值。 |
| `<expr>`    | 任意数值表达式 |
 
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

SELECT QUANTILE_TDIGEST(0.5)(sales_amount) AS median_sales_amount
FROM sales_data;

median_sales_amount|
-------------------+
             6000.0|

SELECT QUANTILE_TDIGEST(0.5, 0.8)(sales_amount)
FROM sales_data;

quantile_tdigest(0.5, 0.8)(sales_amount)|
----------------------------------------+
[6000.0,7000.0]                         |
```