---
title: QUANTILE_CONT
summary: `QUANTILE_CONT()` 函数用于计算数值数据序列的插值分位数。
---

# QUANTILE_CONT

`QUANTILE_CONT()` 函数用于计算数值数据序列的插值分位数。

> **注意：**
>
> NULL 值不计入统计。

## 语法 {#syntax}

```sql
QUANTILE_CONT(<levels>)(<expr>)
QUANTILE_CONT(level1, level2, ...)(<expr>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|-------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| `<level(s)` | 分位数的级别。每个级别都是 0 到 1 之间的常数浮点数。建议使用 [0.01, 0.99] 范围内的级别值 |
| `<expr>`    | 任意数值表达式 |

## 返回类型 {#return-type}

根据级别数量，返回 Float64 或 float64 数组。

## 示例 {#example}

**创建表并插入示例数据**

```sql
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
```

**查询示例：使用插值计算销售额的第 50 百分位数（中位数）**

```sql
SELECT QUANTILE_CONT(0.5)(sales_amount) AS median_sales_amount
FROM sales_data;
```

**结果**

```sql
|  median_sales_amount  |
|-----------------------|
|        6000.0         |
```