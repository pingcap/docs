---
title: FIRST_VALUE
summary: 返回窗口框架中的第一个值。
---

# FIRST_VALUE

返回窗口框架中的第一个值。

另请参阅：

- [LAST_VALUE](/tidb-cloud-lake/sql/last-value.md)
- [NTH_VALUE](/tidb-cloud-lake/sql/nth-value.md)

## 语法 {#syntax}

```sql
FIRST_VALUE(expression) [ { RESPECT | IGNORE } NULLS ]
OVER (
    [ PARTITION BY partition_expression ]
    ORDER BY sort_expression [ ASC | DESC ]
    [ window_frame ]
)
```

**参数：**

- `expression`：必需。要从中返回第一个值的列或表达式。
- `PARTITION BY`：可选。将行划分为多个分区。
- `ORDER BY`：必需。确定窗口内的排序顺序。
- `window_frame`：可选。定义窗口框架。默认值为 `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`。

**说明：**

- 返回有序窗口框架中的第一个值。
- 支持 `IGNORE NULLS` 以跳过空值，支持 `RESPECT NULLS` 以保留默认行为。
- 当你需要基于行的语义而不是默认的范围框架时，请显式指定窗口框架（例如，`ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`）。
- 适用于查找每个分组或时间窗口中的最早值或最小值。

## 示例 {#examples}

```sql
-- Sample order data
CREATE OR REPLACE TABLE orders_window_demo (
    customer VARCHAR,
    order_id INT,
    order_time TIMESTAMP,
    amount INT,
    sales_rep VARCHAR
);

INSERT INTO orders_window_demo VALUES
    ('Alice', 1001, to_timestamp('2024-05-01 09:00:00'), 120, 'Erin'),
    ('Alice', 1002, to_timestamp('2024-05-01 11:00:00'), 135, NULL),
    ('Alice', 1003, to_timestamp('2024-05-02 14:30:00'), 125, 'Glen'),
    ('Bob',   1004, to_timestamp('2024-05-01 08:30:00'),  90, NULL),
    ('Bob',   1005, to_timestamp('2024-05-01 20:15:00'), 105, 'Kai'),
    ('Bob',   1006, to_timestamp('2024-05-03 10:00:00'),  95, NULL),
    ('Carol', 1007, to_timestamp('2024-05-04 09:45:00'),  80, 'Lily');
```

**示例 1：每个客户的首次购买**

```sql
SELECT customer,
       order_id,
       order_time,
       amount,
       FIRST_VALUE(amount) OVER (
           PARTITION BY customer
           ORDER BY order_time
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS first_order_amount
FROM orders_window_demo
ORDER BY customer, order_time;
```

结果：

```
customer | order_id | order_time           | amount | first_order_amount
---------+----------+----------------------+--------+--------------------
Alice    |     1001 | 2024-05-01 09:00:00  |    120 |                120
Alice    |     1002 | 2024-05-01 11:00:00  |    135 |                120
Alice    |     1003 | 2024-05-02 14:30:00  |    125 |                120
Bob      |     1004 | 2024-05-01 08:30:00  |     90 |                 90
Bob      |     1005 | 2024-05-01 20:15:00  |    105 |                 90
Bob      |     1006 | 2024-05-03 10:00:00  |     95 |                 90
Carol    |     1007 | 2024-05-04 09:45:00  |     80 |                 80
```

**示例 2：过去 24 小时内的第一笔订单**

```sql
SELECT customer,
       order_id,
       order_time,
       FIRST_VALUE(order_id) OVER (
           PARTITION BY customer
           ORDER BY order_time
           RANGE BETWEEN INTERVAL 1 DAY PRECEDING AND CURRENT ROW
       ) AS first_order_in_24h
FROM orders_window_demo
ORDER BY customer, order_time;
```

结果：

```
customer | order_id | order_time           | first_order_in_24h
---------+----------+----------------------+--------------------
Alice    |     1001 | 2024-05-01 09:00:00  |               1001
Alice    |     1002 | 2024-05-01 11:00:00  |               1001
Alice    |     1003 | 2024-05-02 14:30:00  |               1003
Bob      |     1004 | 2024-05-01 08:30:00  |               1004
Bob      |     1005 | 2024-05-01 20:15:00  |               1004
Bob      |     1006 | 2024-05-03 10:00:00  |               1006
Carol    |     1007 | 2024-05-04 09:45:00  |               1007
```

**示例 3：跳过空值以查找第一个有姓名的销售代表**

```sql
SELECT customer,
       order_id,
       sales_rep,
       FIRST_VALUE(sales_rep) RESPECT NULLS OVER (
           PARTITION BY customer
           ORDER BY order_time
       ) AS first_rep_respect,
       FIRST_VALUE(sales_rep) IGNORE NULLS OVER (
           PARTITION BY customer
           ORDER BY order_time
       ) AS first_rep_ignore
FROM orders_window_demo
ORDER BY customer, order_id;
```

结果：

```
customer | order_id | sales_rep | first_rep_respect | first_rep_ignore
---------+----------+-----------+-------------------+------------------
Alice    |     1001 | Erin      | Erin              | Erin
Alice    |     1002 | NULL      | Erin              | Erin
Alice    |     1003 | Glen      | Erin              | Erin
Bob      |     1004 | NULL      | NULL              | NULL
Bob      |     1005 | Kai       | NULL              | Kai
Bob      |     1006 | NULL      | NULL              | Kai
Carol    |     1007 | Lily      | Lily              | Lily
```