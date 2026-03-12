---
title: WITH Clause
---

The WITH clause is an optional clause that precedes the body of the SELECT statement, and defines one or more CTEs (common table expressions) that can be referenced later in the statement.


## Syntax

### Basic CTE

```sql
[ WITH
    cte_name1 [ ( cte_column_list ) ] AS ( SELECT ... )
  [ , cte_name2 [ ( cte_column_list ) ] AS ( SELECT ... ) ]
  [ , cte_nameN [ ( cte_column_list ) ] AS ( SELECT ... ) ]
]
SELECT ...
```

### Recursive CTE

```sql
[ WITH [ RECURSIVE ]
    cte_name1 ( cte_column_list ) AS ( anchorClause UNION ALL recursiveClause )
  [ , cte_name2 ( cte_column_list ) AS ( anchorClause UNION ALL recursiveClause ) ]
  [ , cte_nameN ( cte_column_list ) AS ( anchorClause UNION ALL recursiveClause ) ]
]
SELECT ...
```

Where:
- `anchorClause`: `SELECT anchor_column_list FROM ...`
- `recursiveClause`: `SELECT recursive_column_list FROM ... [ JOIN ... ]`

## Parameters

| Parameter | Description |
|-----------|-------------|
| `cte_name` | The CTE name must follow standard identifier rules |
| `cte_column_list` | The names of the columns in the CTE |
| `anchor_column_list` | The columns used in the anchor clause for the recursive CTE |
| `recursive_column_list` | The columns used in the recursive clause for the recursive CTE |

## Examples

### Basic CTE

```sql
WITH high_value_customers AS (
    SELECT customer_id, customer_name, total_spent
    FROM customers 
    WHERE total_spent > 10000
)
SELECT c.customer_name, o.order_date, o.order_amount
FROM high_value_customers c
JOIN orders o ON c.customer_id = o.customer_id
ORDER BY o.order_date DESC;
```

### Multiple CTEs

```sql
WITH
  regional_sales AS (
    SELECT region, SUM(sales_amount) as total_sales
    FROM sales_data
    GROUP BY region
  ),
  top_regions AS (
    SELECT region, total_sales
    FROM regional_sales
    WHERE total_sales > 1000000
  )
SELECT r.region, r.total_sales
FROM top_regions r
ORDER BY r.total_sales DESC;
```

### Recursive CTE

```sql
WITH RECURSIVE countdown AS (
    -- Anchor clause: starting point
    SELECT 10 as num
    
    UNION ALL
    
    -- Recursive clause: repeat until condition
    SELECT num - 1
    FROM countdown 
    WHERE num > 1  -- Stop condition
)
SELECT num FROM countdown 
ORDER BY num DESC;
```

## Usage Notes

- CTEs are temporary named result sets that exist only for the duration of the query
- CTE names must be unique within the same WITH clause
- A CTE can reference previously defined CTEs in the same WITH clause
- Recursive CTEs require both an anchor clause and a recursive clause connected by UNION ALL
- The RECURSIVE keyword is required when using recursive CTEs