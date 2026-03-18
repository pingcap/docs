---
title: SET VARIABLE
summary: Sets the value of one or more SQL variables within a session. The values can be simple constants, expressions, query results, or database objects. Variables persist for the duration of your session and can be used in subsequent queries.
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.609"/>

Sets the value of one or more SQL variables within a session. The values can be simple constants, expressions, query results, or database objects. Variables persist for the duration of your session and can be used in subsequent queries.

## Syntax

```sql
-- Set one variable
SET VARIABLE <variable_name> = <expression>

-- Set more than one variable
SET VARIABLE (<variable1>, <variable2>, ...) = (<expression1>, <expression2>, ...)

-- Set multiple variables from a query result
SET VARIABLE (<variable1>, <variable2>, ...) = <query>
```

## Accessing Variables

Variables can be accessed using the dollar sign syntax: `$variable_name`

## Examples

### Setting a Single Variable

```sql
-- Sets variable a to the string 'databend'
SET VARIABLE a = 'databend'; 

-- Access the variable
SELECT $a;
┌─────────┐
│ $a      │
├─────────┤
│ databend│
└─────────┘
```

### Setting Multiple Variables

```sql
-- Sets variable x to 'xx' and y to 'yy'
SET VARIABLE (x, y) = ('xx', 'yy');

-- Access multiple variables
SELECT $x, $y;
┌────┬────┐
│ $x │ $y │
├────┼────┤
│ xx │ yy │
└────┴────┘
```

### Setting Variables from Query Results

```sql
-- Sets variable a to 3 and b to 55
SET VARIABLE (a, b) = (SELECT 3, 55); 

-- Access the variables
SELECT $a, $b;
┌────┬────┐
│ $a │ $b │
├────┼────┤
│ 3  │ 55 │
└────┴────┘
```

### Dynamic Table References

Variables can be used with the `IDENTIFIER()` function to dynamically reference database objects:

```sql
-- Create a sample table
CREATE OR REPLACE TABLE monthly_sales(empid INT, amount INT, month TEXT) AS SELECT 1, 2, '3';

-- Set a variable 't' to the name of the table 'monthly_sales'
SET VARIABLE t = 'monthly_sales';

-- Access the variable directly
SELECT $t;
┌──────────────┐
│ $t           │
├──────────────┤
│ monthly_sales│
└──────────────┘

-- Use IDENTIFIER to dynamically reference the table name stored in the variable 't'
SELECT * FROM IDENTIFIER($t);
┌───────┬────────┬───────┐
│ empid │ amount │ month │
├───────┼────────┼───────┤
│     1 │      2 │ 3     │
└───────┴────────┴───────┘
```
