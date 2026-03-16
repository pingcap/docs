---
title: SUM
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.697"/>

Calculates the sum of a set of values.

- NULL values are ignored.
- Supports numeric and interval types.

## Syntax

```sql
SUM(<expr>)
```

## Return Type

Same as the input type.

## Examples

This example demonstrates how to create a table with INTEGER, DOUBLE, and INTERVAL columns, insert data, and use SUM to calculate the total for each column:

```sql
-- Create a table with integer, double, and interval columns
CREATE TABLE sum_example (
    id INT,
    int_col INTEGER,
    double_col DOUBLE,
    interval_col INTERVAL
);

-- Insert data
INSERT INTO sum_example VALUES 
(1, 10, 15.5, INTERVAL '2 days'),
(2, 20, 25.7, INTERVAL '3 days'),
(3, NULL, 5.2, INTERVAL '1 day'),  
(4, 30, 40.1, INTERVAL '4 days');

-- Calculate the sum for each column
SELECT 
    SUM(int_col) AS total_integer,
    SUM(double_col) AS total_double,
    SUM(interval_col) AS total_interval
FROM sum_example;
```

Expected Output:

```sql
-- NULL values are ignored.
-- SUM(interval_col) returns 240:00:00 (10 days).

┌──────────────────────────────────────────────────────────┐
│  total_integer  │    total_double   │   total_interval   │
├─────────────────┼───────────────────┼────────────────────┤
│              60 │              86.5 │ 240:00:00          │
└──────────────────────────────────────────────────────────┘
```