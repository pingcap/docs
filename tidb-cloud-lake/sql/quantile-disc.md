---
title: QUANTILE_DISC
summary: QUANTILE_DISC() 函数用于计算数值数据序列的精确分位数。
---

# QUANTILE_DISC

`QUANTILE_DISC()` 函数用于计算数值数据序列的精确分位数。`QUANTILE` 是 `QUANTILE_DISC` 的别名。

> **Note:**
>
> NULL 值不计入统计。

## 语法 {#syntax}

```sql
QUANTILE_DISC(<levels>)(<expr>)
QUANTILE_DISC(level1, level2, ...)(<expr>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| `level(s)` | 分位数的级别。每个级别都是从 0 到 1 的常数浮点数。建议使用 [0.01, 0.99] 范围内的级别值。 |
| `<expr>`   | 任意数值表达式 |

## 返回类型 {#return-type}

根据 level 的数量，返回 InputType 或 InputType 数组。

## 示例 {#example}

**创建表并插入示例数据**

```sql
CREATE TABLE salary_data (
  id INT,
  employee_id INT,
  salary FLOAT
);

INSERT INTO salary_data (id, employee_id, salary)
VALUES (1, 1, 50000),
       (2, 2, 55000),
       (3, 3, 60000),
       (4, 4, 65000),
       (5, 5, 70000);
```

**查询示例：计算薪资的第 25 和第 75 百分位数**

```sql
SELECT QUANTILE_DISC(0.25, 0.75)(salary) AS salary_quantiles
FROM salary_data;
```

**结果**

```sql
|  salary_quantiles   |
|---------------------|
| [55000.0, 65000.0]  |
```