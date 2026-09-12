---
title: NTH_VALUE
summary: 返回窗口框架内指定位置（N）处的值。
---

# NTH_VALUE

返回窗口框架内指定位置（N）处的值。

另请参阅：

- [FIRST_VALUE](/tidb-cloud-lake/sql/first-value.md)
- [LAST_VALUE](/tidb-cloud-lake/sql/last-value.md)

## 语法 {#syntax}

```sql
NTH_VALUE(
    expression,
    n
)
[ { RESPECT | IGNORE } NULLS ]
OVER (
    [ PARTITION BY partition_expression ]
    ORDER BY order_expression
    [ window_frame ]
)
```

**参数：**

- `expression`：必需。要计算的列或表达式。
- `n`：必需。要返回的值的位置编号（从 1 开始）。
- `IGNORE NULLS`：可选。计算位置时跳过空值。
- `RESPECT NULLS`：可选。计算位置时保留空值（默认）。
- `window_frame`：可选。定义窗口框架。默认值为 `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`。

**说明：**

- `n` 必须是正整数；`n = 1` 等价于 `FIRST_VALUE`。
- 如果指定位置在框架中不存在，则返回 `NULL`。
- 可结合 `ROWS BETWEEN ...` 使用，以控制该位置是在整个分区上计算，还是仅在截至当前行为止已看到的行上计算。
- 有关窗口框架语法，请参阅 [窗口框架语法](/tidb-cloud-lake/sql/window-functions-overview.md#basic-syntax)。

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

**查找第二个订单，并演示对第二个销售代表的空值处理：**

```sql
SELECT customer,
       order_id,
       order_time,
       NTH_VALUE(order_id, 2) OVER (
           PARTITION BY customer
           ORDER BY order_time
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS second_order_so_far,
       NTH_VALUE(sales_rep, 2) RESPECT NULLS OVER (
           PARTITION BY customer
           ORDER BY order_time
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS second_rep_respect,
       NTH_VALUE(sales_rep, 2) IGNORE NULLS OVER (
           PARTITION BY customer
           ORDER BY order_time
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS second_rep_ignore
FROM orders_window_demo
ORDER BY customer, order_time;
```

结果：

```
customer | order_id | order_time           | second_order_so_far | second_rep_respect | second_rep_ignore
---------+----------+----------------------+---------------------+--------------------+-------------------
Alice    |     1001 | 2024-05-01 09:00:00  |                NULL | NULL               | NULL
Alice    |     1002 | 2024-05-01 11:00:00  |                1002 | NULL               | NULL
Alice    |     1003 | 2024-05-02 14:30:00  |                1002 | NULL               | Glen
Bob      |     1004 | 2024-05-01 08:30:00  |                NULL | NULL               | NULL
Bob      |     1005 | 2024-05-01 20:15:00  |                1005 | Kai                | Kai
Bob      |     1006 | 2024-05-03 10:00:00  |                1005 | Kai                | Kai
Carol    |     1007 | 2024-05-04 09:45:00  |                NULL | NULL               | NULL
```