---
title: NTH_VALUE
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.697"/>

Returns the value at the specified position (N) within the window frame.

See also:

- [FIRST_VALUE](first-value.md)
- [LAST_VALUE](last-value.md)

## Syntax

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

**Arguments:**
- `expression`: Required. The column or expression to evaluate.
- `n`: Required. Position number (1-based) of the value to return.
- `IGNORE NULLS`: Optional. Skips null values when counting positions.
- `RESPECT NULLS`: Optional. Keeps null values when counting positions (default).
- `window_frame`: Optional. Defines the window frame. The default is `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`.

**Notes:**
- `n` must be a positive integer; `n = 1` is equivalent to `FIRST_VALUE`.
- Returns `NULL` if the specified position does not exist in the frame.
- Combine with `ROWS BETWEEN ...` to control whether the position is evaluated over the whole partition or the rows seen so far.
- For window frame syntax, see [Window Frame Syntax](index.md#window-frame-syntax).

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

**Find the second order and illustrate null-handling for the second sales rep:**

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

Result:
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
