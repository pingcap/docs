---
title: SQL Variables
sidebar_label: SQL Variables
---

SQL variables allow you to store and manage temporary data within a session, making scripts more dynamic and reusable.

## Variable Commands

| Command | Description |
|---------|-------------|
| [SET VARIABLE](set-variable.md) | Creates or modifies a session or user variable. |
| [UNSET VARIABLE](unset-variable.md) | Removes a user-defined variable. |
| [SHOW VARIABLES](show-variables.md) | Displays current values of system and user variables. |

The SHOW VARIABLES command also has a table function counterpart, [`SHOW_VARIABLES`](../../../20-sql-functions/17-table-functions/show-variables.md), which returns the same information in a tabular format for richer filtering and querying.

## Querying with Variables

You can reference variables in statements for dynamic value substitution or to build object names at runtime.

### Accessing Variables with `$` and `getvariable()`

Use the `$` symbol or the `getvariable()` function to embed variable values directly in a query.

```sql title='Example:'
-- Set a variable to use as a filter value
SET VARIABLE threshold = 100;

-- Use the variable in a query with $
SELECT * FROM sales WHERE amount > $threshold;

-- Alternatively, use the getvariable() function
SELECT * FROM sales WHERE amount > getvariable('threshold');
```

### Accessing Objects with `IDENTIFIER`

The `IDENTIFIER` keyword lets you reference database objects whose names are stored in variables, enabling flexible query construction. (Note: BendSQL does not yet support `IDENTIFIER`.)

```sql title='Example:'
-- Create a table with sales data
CREATE TABLE sales_data (region TEXT, sales_amount INT, month TEXT) AS
SELECT 'North', 5000, 'January' UNION ALL
SELECT 'South', 3000, 'January';

select * from sales_data;

-- Set variables for the table name and column name
SET VARIABLE table_name = 'sales_data';
SET VARIABLE column_name = 'sales_amount';

-- Use IDENTIFIER to dynamically reference the table and column in the query
SELECT region, IDENTIFIER($column_name)
FROM IDENTIFIER($table_name)
WHERE IDENTIFIER($column_name) > 4000;
```
