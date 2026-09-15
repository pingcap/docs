---
title: MAX_IF
summary: 后缀 `_IF` 可以附加到任何聚合函数的名称后。在这种情况下，聚合函数会接受一个额外的参数——条件。
---

# MAX_IF

## MAX_IF {#max-if}

后缀 `_IF` 可以附加到任何聚合函数的名称后。在这种情况下，聚合函数会接受一个额外的参数——条件。

```sql
MAX_IF(<column>, <cond>)
```

## 示例 {#example}

**创建表并插入示例数据**

```sql
CREATE TABLE sales (
  id INT,
  salesperson_id INT,
  product_id INT,
  revenue FLOAT
);

INSERT INTO sales (id, salesperson_id, product_id, revenue)
VALUES (1, 1, 1, 1000),
       (2, 1, 2, 2000),
       (3, 1, 3, 3000),
       (4, 2, 1, 1500),
       (5, 2, 2, 2500);
```

**查询示例：查找 ID 为 1 的销售人员的最大收入**

```sql
SELECT MAX_IF(revenue, salesperson_id = 1) AS max_revenue_salesperson_1
FROM sales;
```

**结果**

```sql
| max_revenue_salesperson_1 |
|---------------------------|
|           3000            |
```