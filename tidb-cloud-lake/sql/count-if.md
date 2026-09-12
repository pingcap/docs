---
title: COUNT_IF
summary: 后缀 `_IF` 可以附加到任何聚合函数的名称后。在这种情况下，聚合函数会接受一个额外的参数——条件。
---

# COUNT_IF

## COUNT_IF {#count-if}

后缀 `_IF` 可以附加到任何聚合函数的名称后。在这种情况下，聚合函数会接受一个额外的参数——条件。

```sql
COUNT_IF(<column>, <cond>)
```

## 示例 {#example}

**创建表并插入示例数据**

```sql
CREATE TABLE orders (
  id INT,
  customer_id INT,
  status VARCHAR,
  total FLOAT
);

INSERT INTO orders (id, customer_id, status, total)
VALUES (1, 1, 'completed', 100),
       (2, 2, 'completed', 200),
       (3, 1, 'pending', 150),
       (4, 3, 'completed', 250),
       (5, 2, 'pending', 300);
```

**查询示例：统计已完成订单数**

```sql
SELECT COUNT_IF(status, status = 'completed') AS completed_orders
FROM orders;
```

**结果**

```sql
| completed_orders |
|------------------|
|        3         |
```