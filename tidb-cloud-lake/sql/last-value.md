---
title: LAST_VALUE
summary: 返回窗口框架中的最后一个值。
---

# LAST_VALUE

返回窗口框架中的最后一个值。

另请参阅：

- [FIRST_VALUE](/tidb-cloud-lake/sql/first-value.md)
- [NTH_VALUE](/tidb-cloud-lake/sql/nth-value.md)

## 语法 {#syntax}

```sql
LAST_VALUE(expression) [ { RESPECT | IGNORE } NULLS ]
OVER (
    [ PARTITION BY partition_expression ]
    ORDER BY sort_expression [ ASC | DESC ]
    [ window_frame ]
)
```

**参数：**

- `expression`：必需。要返回其最后一个值的列或表达式。
- `PARTITION BY`：可选。将行划分为多个分区。
- `ORDER BY`：必需。确定窗口内的排序顺序。
- `window_frame`：可选。定义窗口框架。默认值为 `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`。

**说明：**

- 返回已排序窗口框架中的最后一个值。
- 支持 `IGNORE NULLS` 以跳过空值，支持 `RESPECT NULLS` 以保留默认行为。
- 当你需要分区中真正的最后一行时，请使用在当前行之后结束的框架（例如 `ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING`）。
- 适用于查找每个组中的最新值，或前瞻窗口中的最近值。

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

**示例 1：每个客户分区中的最新订单**

```sql
SELECT customer,
       order_id,
       order_time,
       LAST_VALUE(order_id) OVER (
           PARTITION BY customer
           ORDER BY order_time
           ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING
       ) AS last_order_for_customer
FROM orders_window_demo
ORDER BY customer, order_time;
```

结果：

```
customer | order_id | order_time           | last_order_for_customer
---------+----------+----------------------+-------------------------
Alice    |     1001 | 2024-05-01 09:00:00  |                    1003
Alice    |     1002 | 2024-05-01 11:00:00  |                    1003
Alice    |     1003 | 2024-05-02 14:30:00  |                    1003
Bob      |     1004 | 2024-05-01 08:30:00  |                    1006
Bob      |     1005 | 2024-05-01 20:15:00  |                    1006
Bob      |     1006 | 2024-05-03 10:00:00  |                    1006
Carol    |     1007 | 2024-05-04 09:45:00  |                    1007
```

**示例 2：在每个客户内向前查看 12 小时**

```sql
SELECT customer,
       order_id,
       order_time,
       amount,
       LAST_VALUE(amount) OVER (
           PARTITION BY customer
           ORDER BY order_time
           RANGE BETWEEN CURRENT ROW AND INTERVAL 12 HOUR FOLLOWING
       ) AS last_amount_next_12h
FROM orders_window_demo
ORDER BY customer, order_time;
```

结果：

```
customer | order_id | order_time           | amount | last_amount_next_12h
---------+----------+----------------------+--------+----------------------
Alice    |     1001 | 2024-05-01 09:00:00  |    120 |                  135
Alice    |     1002 | 2024-05-01 11:00:00  |    135 |                  135
Alice    |     1003 | 2024-05-02 14:30:00  |    125 |                  125
Bob      |     1004 | 2024-05-01 08:30:00  |     90 |                  105
Bob      |     1005 | 2024-05-01 20:15:00  |    105 |                  105
Bob      |     1006 | 2024-05-03 10:00:00  |     95 |                   95
Carol    |     1007 | 2024-05-04 09:45:00  |     80 |                   80
```

**示例 3：向前扫描最后一个销售代表时跳过空值**

```sql
SELECT customer,
       order_id,
       sales_rep,
       LAST_VALUE(sales_rep) RESPECT NULLS OVER (
           PARTITION BY customer
           ORDER BY order_time
           ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING
       ) AS last_rep_respect,
       LAST_VALUE(sales_rep) IGNORE NULLS OVER (
           PARTITION BY customer
           ORDER BY order_time
           ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING
       ) AS last_rep_ignore
FROM orders_window_demo
ORDER BY customer, order_id;
```

结果：

```
customer | order_id | sales_rep | last_rep_respect | last_rep_ignore
---------+----------+-----------+------------------+-----------------
Alice    |     1001 | Erin      | Glen             | Glen
Alice    |     1002 | NULL      | Glen             | Glen
Alice    |     1003 | Glen      | Glen             | Glen
Bob      |     1004 | NULL      | NULL             | Kai
Bob      |     1005 | Kai       | NULL             | Kai
Bob      |     1006 | NULL      | NULL             | Kai
Carol    |     1007 | Lily      | Lily             | Lily
```