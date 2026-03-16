---
title: DESC VIEW
sidebar_position: 3
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.383"/>

Returns the list of columns for a view.

## Syntax

```sql
DESC[RIBE] VIEW [<database_name>.]<view_name>
```

## Output

The command outputs a table with the following columns:

| Column  | Description                                                                                                             |
|---------|-------------------------------------------------------------------------------------------------------------------------|
| Field   | The name of the column in the view.                                                                                     |
| Type    | The data type of the column.                                                                                            |
| Null    | Indicates whether the column allows NULL values (YES for allowing NULL, NO for not allowing NULL).                      |
| Default | Specifies the default value for the column.                                                                             |
| Extra   | Provides additional information about the column, such as whether it is a computed column, or other special attributes. |

## Examples

```sql
-- Create the employees table
CREATE TABLE employees (
    employee_id INT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    hire_date DATE,
    department_id INT
);

-- Insert data into the employees table
INSERT INTO employees (employee_id, first_name, last_name, email, hire_date, department_id)
VALUES
(1, 'John', 'Doe', 'john@example.com', '2020-01-01', 101),
(2, 'Jane', 'Smith', 'jane@example.com', '2020-02-01', 102),
(3, 'Alice', 'Johnson', 'alice@example.com', '2020-03-01', 103);

-- Create the employee_info view
CREATE VIEW employee_info AS
SELECT employee_id, CONCAT(first_name, ' ', last_name) AS full_name, email, hire_date, department_id
FROM employees;

-- Describe the structure of the employee_info view
DESC employee_info;

┌─────────────────────────────────────────────────────┐
│     Field     │   Type  │  Null  │ Default │  Extra │
├───────────────┼─────────┼────────┼─────────┼────────┤
│ employee_id   │ INT     │ YES    │ NULL    │        │
│ full_name     │ VARCHAR │ YES    │ NULL    │        │
│ email         │ VARCHAR │ YES    │ NULL    │        │
│ hire_date     │ DATE    │ YES    │ NULL    │        │
│ department_id │ INT     │ YES    │ NULL    │        │
└─────────────────────────────────────────────────────┘
```