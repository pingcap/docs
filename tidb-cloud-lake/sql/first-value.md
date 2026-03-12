---
title: FIRST_VALUE
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.697"/>

Returns the first value in the window frame.

See also:

- [LAST_VALUE](last-value.md)
- [NTH_VALUE](nth-value.md)

## Syntax

```sql
FIRST_VALUE(expression) [ { RESPECT | IGNORE } NULLS ]
OVER (
    [ PARTITION BY partition_expression ]
    ORDER BY sort_expression [ ASC | DESC ]
    [ window_frame ]
)
```

**Arguments:**
- `expression`: Required. The column or expression to return the first value from.
- `PARTITION BY`: Optional. Divides rows into partitions.
- `ORDER BY`: Required. Determines the ordering within the window.
- `window_frame`: Optional. Defines the window frame. The default is `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`.

**Notes:**
- Returns the first value in the ordered window frame.
- Supports `IGNORE NULLS` to skip null values and `RESPECT NULLS` to keep the default behaviour.
- Specify an explicit window frame (for example, `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`) when you need row-based semantics instead of the default range frame.
- Useful for finding the earliest or lowest value in each group or time window.

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

**Example 1. First purchase per customer**

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

Result:
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

**Example 2. First order in the trailing 24 hours**

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

Result:
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

**Example 3. Skip nulls to find the first named sales rep**

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

Result:
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
