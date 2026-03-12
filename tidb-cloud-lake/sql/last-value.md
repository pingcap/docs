---
title: LAST_VALUE
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.697"/>

Returns the last value in the window frame.

See also:

- [FIRST_VALUE](first-value.md)
- [NTH_VALUE](nth-value.md)

## Syntax

```sql
LAST_VALUE(expression) [ { RESPECT | IGNORE } NULLS ]
OVER (
    [ PARTITION BY partition_expression ]
    ORDER BY sort_expression [ ASC | DESC ]
    [ window_frame ]
)
```

**Arguments:**
- `expression`: Required. The column or expression to return the last value from.
- `PARTITION BY`: Optional. Divides rows into partitions.
- `ORDER BY`: Required. Determines the ordering within the window.
- `window_frame`: Optional. Defines the window frame. The default is `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`.

**Notes:**
- Returns the last value in the ordered window frame.
- Supports `IGNORE NULLS` to skip null values and `RESPECT NULLS` to keep the default behaviour.
- Use a frame that ends after the current row (for example, `ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING`) when you need the true last row of a partition.
- Useful for finding the latest value in each group, or the most recent value inside a look-ahead window.

## Examples

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

**Example 1. Latest order in each customer partition**

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

Result:
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

**Example 2. Peek 12 hours ahead within each customer**

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

Result:
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

**Example 3. Skip nulls when scanning forward for the last sales rep**

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

Result:
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
