---
title: MODE
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.647"/>

Returns the value that appears most frequently in a group of values.

## Syntax

```sql
MODE(<expr>)
```

## Examples

This example identifies the best-selling product for each month from the sales data:

```sql
CREATE OR REPLACE TABLE sales (
    sale_date DATE,
    product_id INT,
    quantity INT
);

INSERT INTO sales (sale_date, product_id, quantity) VALUES
    ('2024-01-01', 101, 10),
    ('2024-01-02', 102, 15),
    ('2024-01-02', 101, 10),
    ('2024-01-03', 103, 8),
    ('2024-01-03', 101, 10),
    ('2024-02-01', 101, 20),
    ('2024-02-02', 102, 15),
    ('2024-02-03', 102, 15);

SELECT MONTH(sale_date) AS month, MODE(product_id) AS most_sold_product
FROM sales
GROUP BY month
ORDER BY month;

┌─────────────────────────────────────┐
│      month      │ most_sold_product │
├─────────────────┼───────────────────┤
│               1 │               101 │
│               2 │               102 │
└─────────────────────────────────────┘
```