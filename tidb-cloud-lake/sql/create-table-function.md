---
title: CREATE TABLE FUNCTION
sidebar_position: 3
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.799"/>

Creates a tabular SQL UDF (UDTF) that encapsulates SQL queries as a table function. Table functions are written in SQL; no external languages are involved.

### Supported Languages

- SQL queries only (no external runtimes)

## Syntax

```sql
CREATE [ OR REPLACE ] FUNCTION [ IF NOT EXISTS ] <function_name> 
    ( [<parameter_list>] ) 
    RETURNS TABLE ( <column_definition_list> ) 
    AS $$ <sql_statement> $$
```

Where:
- `<parameter_list>`: Optional comma-separated list of input parameters with their types (e.g., `x INT, name VARCHAR`)
- `<column_definition_list>`: Comma-separated list of column names and their types that the function returns
- `<sql_statement>`: The SQL query that defines the function logic

## Unified Function Syntax

Databend uses a unified `$$` syntax for both scalar and table functions:

| Function Type | Returns | Usage |
|---------------|---------|-------|
| **Scalar Function** | Single value | `RETURNS <type>` + `AS $$ <expression> $$` |
| **Table Function** | Result set | `RETURNS TABLE(...)` + `AS $$ <query> $$` |

This consistency makes it easy to understand and switch between function types.

## Examples

### Basic Table Function

```sql
-- Create a sample table
CREATE OR REPLACE TABLE employees (
    id INT, 
    name VARCHAR(100), 
    department VARCHAR(100),
    salary DECIMAL(10,2)
);

INSERT INTO employees VALUES 
    (1, 'John', 'Engineering', 75000), 
    (2, 'Jane', 'Marketing', 65000),
    (3, 'Bob', 'Engineering', 80000),
    (4, 'Alice', 'Marketing', 70000);

-- Create a simple table function to get all employees
CREATE OR REPLACE FUNCTION get_all_employees() 
RETURNS TABLE (id INT, name VARCHAR(100), department VARCHAR(100), salary DECIMAL(10,2))
AS $$ SELECT id, name, department, salary FROM employees $$;

-- Test the function
SELECT * FROM get_all_employees();
```

### Parameterized Table Function

```sql
-- Create a table function that filters employees by department
CREATE OR REPLACE FUNCTION get_employees_by_dept(dept_name VARCHAR)
RETURNS TABLE (id INT, name VARCHAR(100), department VARCHAR(100), salary DECIMAL(10,2))
AS $$ SELECT id, name, department, salary FROM employees WHERE department = dept_name $$;

-- Use the parameterized table function
SELECT * FROM get_employees_by_dept('Engineering');
```

### Complex Table Function

```sql
-- Create a table function that aggregates data
CREATE OR REPLACE FUNCTION get_department_stats()
RETURNS TABLE (department VARCHAR(100), employee_count INT, avg_salary DECIMAL(10,2))
AS $$ SELECT department, COUNT(*) as employee_count, AVG(salary) as avg_salary FROM employees GROUP BY department $$;

-- Use the complex table function
SELECT * FROM get_department_stats();
```
