---
title: QUALIFY
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.262"/>

QUALIFY is a clause used to filter the results of a window function. Therefore, to successfully utilize the QUALIFY clause, there must be at least one window function in the SELECT list or the QUALIFY clause (See [Examples](#examples) for each case). In other words, QUALIFY is evaluated after window functions are computed. Here’s the typical order of execution for a query with a QUALIFY statement clause:

1. FROM
2. WHERE
3. GROUP BY
4. HAVING
5. WINDOW FUNCTION
6. QUALIFY
7. DISTINCT
8. ORDER BY
9. LIMIT

## Syntax

```sql
QUALIFY <predicate>
```

## Examples

This example demonstrates the use of ROW_NUMBER() to assign sequential numbers to employees within their departments, ordered by descending salary. Leveraging the QUALIFY clause, we filter the results to display only the top earner in each department.

```sql
-- Prepare the data
CREATE TABLE employees (
  employee_id INT,
  first_name VARCHAR,
  last_name VARCHAR,
  department VARCHAR,
  salary INT
);

INSERT INTO employees (employee_id, first_name, last_name, department, salary) VALUES
  (1, 'John', 'Doe', 'IT', 90000),
  (2, 'Jane', 'Smith', 'HR', 85000),
  (3, 'Mike', 'Johnson', 'IT', 82000),
  (4, 'Sara', 'Williams', 'Sales', 77000),
  (5, 'Tom', 'Brown', 'HR', 75000);

-- Select employee details along with the row number partitioned by department and ordered by salary in descending order.
SELECT
    employee_id,
    first_name,
    last_name,
    department,
    salary,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS row_num
FROM
    employees;

┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐
│   employee_id   │    first_name    │     last_name    │    department    │      salary     │ row_num │
├─────────────────┼──────────────────┼──────────────────┼──────────────────┼─────────────────┼─────────┤
│               2 │ Jane             │ Smith            │ HR               │           85000 │       1 │
│               5 │ Tom              │ Brown            │ HR               │           75000 │       2 │
│               1 │ John             │ Doe              │ IT               │           90000 │       1 │
│               3 │ Mike             │ Johnson          │ IT               │           82000 │       2 │
│               4 │ Sara             │ Williams         │ Sales            │           77000 │       1 │
└──────────────────────────────────────────────────────────────────────────────────────────────────────┘

-- Select employee details along with the row number partitioned by department and ordered by salary in descending order.
-- Add a filter to only include rows where the row number is 1, selecting the employee with the highest salary in each department.
SELECT
    employee_id,
    first_name,
    last_name,
    department,
    salary,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS row_num
FROM
    employees
QUALIFY row_num = 1;

┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐
│   employee_id   │    first_name    │     last_name    │    department    │      salary     │ row_num │
├─────────────────┼──────────────────┼──────────────────┼──────────────────┼─────────────────┼─────────┤
│               2 │ Jane             │ Smith            │ HR               │           85000 │       1 │
│               1 │ John             │ Doe              │ IT               │           90000 │       1 │
│               4 │ Sara             │ Williams         │ Sales            │           77000 │       1 │
└──────────────────────────────────────────────────────────────────────────────────────────────────────┘

-- Databend allows the direct use of window functions in the QUALIFY clause without requiring them to be explicitly named in the SELECT list.

SELECT
    employee_id,
    first_name,
    last_name,
    department,
    salary
FROM
    employees
QUALIFY ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) = 1;

┌────────────────────────────────────────────────────────────────────────────────────────────┐
│   employee_id   │    first_name    │     last_name    │    department    │      salary     │
├─────────────────┼──────────────────┼──────────────────┼──────────────────┼─────────────────┤
│               2 │ Jane             │ Smith            │ HR               │           85000 │
│               1 │ John             │ Doe              │ IT               │           90000 │
│               4 │ Sara             │ Williams         │ Sales            │           77000 │
└────────────────────────────────────────────────────────────────────────────────────────────┘
```
