---
title: CASE
---

Handles IF/THEN logic. It is structured with at least one pair of `WHEN` and `THEN` statements. Every `CASE` statement must be concluded with the `END` keyword. The `ELSE` statement is optional, providing a way to capture values not explicitly specified in the `WHEN` and `THEN` statements.

## Syntax

```sql
CASE
    WHEN <condition_1> THEN <value_1>
  [ WHEN <condition_2> THEN <value_2> ]
  [ ... ]
  [ ELSE <value_n> ]
END AS <column_name>
```

## Examples

This example categorizes employee salaries using a CASE statement, presenting details with a dynamically assigned column named "SalaryCategory":

```sql
-- Create a sample table
CREATE TABLE Employee (
    EmployeeID INT,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Salary INT
);

-- Insert some sample data
INSERT INTO Employee VALUES (1, 'John', 'Doe', 50000);
INSERT INTO Employee VALUES (2, 'Jane', 'Smith', 60000);
INSERT INTO Employee VALUES (3, 'Bob', 'Johnson', 75000);
INSERT INTO Employee VALUES (4, 'Alice', 'Williams', 90000);

-- Add a new column 'SalaryCategory' using CASE statement
-- Categorize employees based on their salary
SELECT
    EmployeeID,
    FirstName,
    LastName,
    Salary,
    CASE
        WHEN Salary < 60000 THEN 'Low'
        WHEN Salary >= 60000 AND Salary < 80000 THEN 'Medium'
        WHEN Salary >= 80000 THEN 'High'
        ELSE 'Unknown'
    END AS SalaryCategory
FROM
    Employee;

┌──────────────────────────────────────────────────────────────────────────────────────────┐
│    employeeid   │     firstname    │     lastname     │      salary     │ salarycategory │
├─────────────────┼──────────────────┼──────────────────┼─────────────────┼────────────────┤
│               1 │ John             │ Doe              │           50000 │ Low            │
│               2 │ Jane             │ Smith            │           60000 │ Medium         │
│               4 │ Alice            │ Williams         │           90000 │ High           │
│               3 │ Bob              │ Johnson          │           75000 │ Medium         │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```