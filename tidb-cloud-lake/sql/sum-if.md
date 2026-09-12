---
title: SUM_IF
summary: 后缀 -If 可以附加到任何聚合函数的名称后。在这种情况下，聚合函数会接受一个额外的参数——条件。
---

# SUM_IF

## SUM_IF {#sum-if}

后缀 -If 可以附加到任何聚合函数的名称后。在这种情况下，聚合函数会接受一个额外的参数——条件。

```
SUM_IF(<column>, <cond>)
```

## 示例 {#example}

**创建表并插入示例数据**

```sql
CREATE TABLE order_data (
  id INT,
  customer_id INT,
  amount FLOAT,
  status VARCHAR
);

INSERT INTO order_data (id, customer_id, amount, status)
VALUES (1, 1, 100, 'Completed'),
       (2, 2, 50, 'Completed'),
       (3, 3, 80, 'Cancelled'),
       (4, 4, 120, 'Completed'),
       (5, 5, 75, 'Cancelled');
```

**查询示例：计算已完成订单的总金额**

```sql
SELECT SUM_IF(amount, status = 'Completed') AS total_amount_completed
FROM order_data;
```

**结果**

```sql
| total_amount_completed |
|------------------------|
|         270.0          |
```