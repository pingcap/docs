---
title: LISTAGG
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.725"/>

Concatenates values from multiple rows into a single string, separated by a specified delimiter. This operation can be performed using two different function types:
- Aggregate Function: The concatenation happens across all rows in the entire result set.
- Window Function: The concatenation happens within each partition of the result set, as defined by the `PARTITION BY` clause.

## Syntax

```sql
-- Aggregate Function
LISTAGG([DISTINCT] <expr> [, <delimiter>])
  [WITHIN GROUP (ORDER BY <order_by_expr>)]

-- Window Function
LISTAGG([DISTINCT] <expr> [, <delimiter>])
  [WITHIN GROUP (ORDER BY <order_by_expr>)]
  OVER ([PARTITION BY <partition_expr>])
```

| Parameter                       | Description                                                                                       |
|---------------------------------|---------------------------------------------------------------------------------------------------|
| `DISTINCT`                      | Optional. Removes duplicate values before concatenation.                                          |
| `<expr>`                        | The expression to concatenate (typically a column or an expression).                              |
| `<delimiter>`                   | Optional. The string to separate each concatenated value. Defaults to an empty string if omitted. |
| `ORDER BY <order_by_expr>`      | Defines the order in which the values are concatenated.                                           |
| `PARTITION BY <partition_expr>` | Divides rows into partitions to perform aggregation separately within each group.                 |

## Aliases

- [STRING_AGG](aggregate-string-agg.md)
- [GROUP_CONCAT](aggregate-group-concat.md)

## Return Type

String.

## Examples

In this example, we have a table of customer orders. Each order belongs to a customer, and we want to create a list of all products each customer has purchased.

```sql
CREATE TABLE orders (
  customer_id INT,
  product_name VARCHAR
);

INSERT INTO orders (customer_id, product_name) VALUES
(1, 'Laptop'),
(1, 'Mouse'),
(1, 'Laptop'),
(2, 'Phone'),
(2, 'Headphones');
```

The following uses `LISTAGG` as an aggregate function with GROUP BY to concatenate all products purchased by each customer into a single string:

```sql
SELECT
  customer_id,
  LISTAGG(product_name, ', ') WITHIN GROUP (ORDER BY product_name) AS product_list
FROM orders
GROUP BY customer_id;
```

```sql
┌─────────────────────────────────────────┐
│   customer_id   │      product_list     │
├─────────────────┼───────────────────────┤
│               2 │ Headphones, Phone     │
│               1 │ Laptop, Laptop, Mouse │
└─────────────────────────────────────────┘
```

The following uses `LISTAGG` as a window function, so each row keeps its original details but also displays the full product list for the customer's group:

```sql
SELECT
  customer_id,
  product_name,
  LISTAGG(product_name, ', ') WITHIN GROUP (ORDER BY product_name)
    OVER (PARTITION BY customer_id) AS product_list
FROM orders;
```

```sql
┌────────────────────────────────────────────────────────────┐
│   customer_id   │   product_name   │      product_list     │
├─────────────────┼──────────────────┼───────────────────────┤
│               2 │ Phone            │ Headphones, Phone     │
│               2 │ Headphones       │ Headphones, Phone     │
│               1 │ Laptop           │ Laptop, Laptop, Mouse │
│               1 │ Mouse            │ Laptop, Laptop, Mouse │
│               1 │ Laptop           │ Laptop, Laptop, Mouse │
└────────────────────────────────────────────────────────────┘
```