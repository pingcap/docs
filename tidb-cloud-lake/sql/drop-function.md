---
title: DROP FUNCTION
sidebar_position: 6
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.116"/>

Drops a user-defined function. Works with all function types: Scalar SQL, Tabular SQL, and Embedded functions.

## Syntax

```sql
DROP FUNCTION [ IF EXISTS ] <function_name>
```

## Examples

### Dropping Scalar SQL Function
```sql
-- Create a scalar function
CREATE FUNCTION calculate_bmi(weight FLOAT, height FLOAT)
RETURNS FLOAT
AS $$ weight / (height * height) $$;

-- Drop the function
DROP FUNCTION calculate_bmi;
```

### Dropping Tabular SQL Function
```sql
-- Create a table function
CREATE FUNCTION get_employees_by_dept(dept_name VARCHAR)
RETURNS TABLE (id INT, name VARCHAR, department VARCHAR)
AS $$ SELECT id, name, department FROM employees WHERE department = dept_name $$;

-- Drop the function
DROP FUNCTION get_employees_by_dept;
```

### Dropping Embedded Function
```sql
-- Create a Python function
CREATE FUNCTION custom_hash(input_str VARCHAR)
RETURNS VARCHAR
LANGUAGE python
HANDLER = 'hash_func'
AS $$
import hashlib
def hash_func(s):
    return hashlib.md5(s.encode()).hexdigest()
$$;

-- Drop the function
DROP FUNCTION custom_hash;
```

### Using IF EXISTS
```sql
-- Safe drop - won't error if function doesn't exist
DROP FUNCTION IF EXISTS non_existent_function;

-- This will succeed without error even if the function doesn't exist
```