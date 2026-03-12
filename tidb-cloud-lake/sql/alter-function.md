---
title: ALTER FUNCTION
sidebar_position: 5
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.116"/>

Alters a user-defined function. Supports all function types: Scalar SQL, Tabular SQL, and Embedded functions.

## Syntax

### For Scalar SQL Functions
```sql
ALTER FUNCTION [ IF EXISTS ] <function_name> 
    ( [<parameter_list>] ) 
    RETURNS <return_type>
    AS $$ <expression> $$
    [ DESC='<description>' ]
```

### For Tabular SQL Functions
```sql
ALTER FUNCTION [ IF EXISTS ] <function_name> 
    ( [<parameter_list>] ) 
    RETURNS TABLE ( <column_definition_list> ) 
    AS $$ <sql_statement> $$
    [ DESC='<description>' ]
```

### For Embedded Functions
```sql
ALTER FUNCTION [ IF EXISTS ] <function_name> 
    ( [<parameter_list>] ) 
    RETURNS <return_type>
    LANGUAGE <language>
    [IMPORTS = ('<import_path>', ...)]
    [PACKAGES = ('<package_path>', ...)]
    HANDLER = '<handler_name>'
    AS $$ <function_code> $$
    [ DESC='<description>' ]
```

## Examples

### Altering Scalar SQL Function
```sql
-- Create a scalar function
CREATE FUNCTION calculate_tax(income DECIMAL)
RETURNS DECIMAL
AS $$ income * 0.2 $$;

-- Modify the function to use progressive tax rate
ALTER FUNCTION calculate_tax(income DECIMAL)
RETURNS DECIMAL
AS $$ 
  CASE 
    WHEN income <= 50000 THEN income * 0.15
    ELSE income * 0.25
  END
$$;
```

### Altering Tabular SQL Function
```sql
-- Create a table function
CREATE FUNCTION get_employees() 
RETURNS TABLE (id INT, name VARCHAR(100)) 
AS $$ SELECT id, name FROM employees $$;

-- Modify to include department and salary
ALTER FUNCTION get_employees() 
RETURNS TABLE (id INT, name VARCHAR(100), department VARCHAR(100), salary DECIMAL)
AS $$ SELECT id, name, department, salary FROM employees $$;
```

### Altering Embedded Function
```sql
-- Create a Python function
CREATE FUNCTION simple_calc(x INT)
RETURNS INT
LANGUAGE python
HANDLER = 'calc'
AS $$
def calc(x):
    return x * 2
$$;

-- Modify to use a different calculation
ALTER FUNCTION simple_calc(x INT)
RETURNS INT
LANGUAGE python
HANDLER = 'calc'
AS $$
def calc(x):
    return x * 3 + 1
$$;
```