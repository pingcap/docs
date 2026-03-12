---
title: ANY_VALUE
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.815"/>

Aggregate function.

The `ANY_VALUE()` function returns an arbitrary non-NULL value from the input expression. It's used in `GROUP BY` queries when you need to select a column that isn't grouped or aggregated.

> **Alias:** `ANY()` returns the same result as `ANY_VALUE()` and remains available for compatibility.

## Syntax

```sql
ANY_VALUE(<expr>)
```

## Arguments

| Arguments | Description    |
|-----------|----------------|
| `<expr>`  | Any expression |

## Return Type

The type of `<expr>`. If all values are NULL, the return value is NULL.

:::note
- `ANY_VALUE()` is non-deterministic and may return different values across executions.
- For predictable results, use `MIN()` or `MAX()` instead.
:::

## Example

**Sample Data:**
```sql
CREATE TABLE sales (
  region VARCHAR,
  manager VARCHAR,
  sales_amount DECIMAL(10, 2)
);

INSERT INTO sales VALUES
  ('North', 'Alice', 15000.00),
  ('North', 'Alice', 12000.00),
  ('South', 'Bob', 20000.00);
```

**Problem:** This query fails because `manager` isn't in GROUP BY:
```sql
SELECT region, manager, SUM(sales_amount)  -- ❌ Error
FROM sales GROUP BY region;
```

**Old approach:** Add `manager` to GROUP BY, but this creates more groups than needed and hurts performance:
```sql
SELECT region, manager, SUM(sales_amount)
FROM sales GROUP BY region, manager;  -- ❌ Poor performance due to extra grouping
```

**Better solution:** Use `ANY_VALUE()` to select the manager:
```sql
SELECT
  region,
  ANY_VALUE(manager) AS manager,  -- ✅ Works
  SUM(sales_amount) AS total_sales
FROM sales
GROUP BY region;
```

**Result:**
```text
| region | manager | total_sales |
|--------|---------|-------------|
| North  | Alice   | 27000.00    |
| South  | Bob     | 20000.00    |
```
