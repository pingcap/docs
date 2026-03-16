---
title: VALUES
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.65"/>

The VALUES clause creates an inline table by explicitly defining rows of data. This temporary table can be used directly or within other SQL statements.

## Syntax

```sql
SELECT ...
FROM ( VALUES ( <expr> [ , <expr> [ , ... ] ] ) [ , ( ... ) ] ) [ [ AS ] <table_alias> [ ( <column_alias> [, ... ] ) ] ]
[ ... ]
```

**Key Points:**
- The VALUES clause must be enclosed in parentheses when used in a FROM clause: `FROM (VALUES ...)`
- Each parenthesized group of expressions represents one row
- Column names are automatically assigned as **col0**, **col1**, etc. (zero-based indexing)
- You can provide custom column names using table aliases

## Examples

### Basic Usage

```sql
-- Direct usage with automatic column names (col0, col1)
VALUES ('Toronto', 2731571), ('Vancouver', 631486), ('Montreal', 1704694);

col0     |col1   |
---------+-------+
Toronto  |2731571|
Vancouver| 631486|
Montreal |1704694|

-- With ORDER BY
VALUES ('Toronto', 2731571), ('Vancouver', 631486), ('Montreal', 1704694) ORDER BY col1;

col0     |col1   |
---------+-------+
Vancouver| 631486|
Montreal |1704694|
Toronto  |2731571|
```

### In SELECT Statements

```sql
-- Select specific column - note the parentheses around VALUES
SELECT col1
FROM (VALUES ('Toronto', 2731571), ('Vancouver', 631486), ('Montreal', 1704694));

-- Custom column names - VALUES must be enclosed in parentheses
SELECT * FROM (
    VALUES ('Toronto', 2731571),
           ('Vancouver', 631486),
           ('Montreal', 1704694)
) AS CityPopulation(City, Population);

-- With column aliases and sorting
SELECT col0 AS City, col1 AS Population
FROM (VALUES ('Toronto', 2731571), ('Vancouver', 631486), ('Montreal', 1704694))
ORDER BY col1 DESC
LIMIT 1;
```

### With Common Table Expressions (CTE)

```sql
WITH citypopulation(city, population) AS (
    VALUES ('Toronto', 2731571),
           ('Vancouver', 631486),
           ('Montreal', 1704694)
)
SELECT city, population FROM citypopulation;
```

> **Important**: When using VALUES in a FROM clause or CTE, it must be enclosed in parentheses: `FROM (VALUES ...)` or `AS (VALUES ...)`. This is required syntax.
