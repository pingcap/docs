---
title: MERGE
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.241"/>

Performs **INSERT**, **UPDATE**, or **DELETE** operations on rows within a target table, all in accordance with conditions and matching criteria specified within the statement, using data from a specified source.

The data source, which can be a subquery, is linked to the target data via a JOIN expression. This expression assesses whether each row in the source can find a match in the target table and then determines which type of clause (MATCHED or NOT MATCHED) it should move to in the next execution step.

![Alt text](/img/sql/merge-into-single-clause.jpeg)

A MERGE statement usually contains a MATCHED and / or a NOT MATCHED clause, instructing Databend on how to handle matched and unmatched scenarios. For a MATCHED clause, you have the option to choose between performing an **UPDATE** or **DELETE** operation on the target table. Conversely, in the case of a NOT MATCHED clause, the available choice is **INSERT**.

## Multiple MATCHED & NOT MATCHED Clauses

A MERGE statement can include multiple MATCHED and / or NOT MATCHED clauses, giving you the flexibility to specify different actions to be taken based on the conditions met during the MERGE operation.

![Alt text](/img/sql/merge-into-multi-clause.jpeg)

If a MERGE statement includes multiple MATCHED clauses, a condition needs to be specified for each clause EXCEPT the last one. These conditions determine the criteria under which the associated operations are executed. Databend evaluates the conditions in the specified order. Once a condition is met, it triggers the specified operation, skips any remaining MATCHED clauses, then moves on to the next row in the source. If the MERGE statement also includes multiple NOT MATCHED clauses, Databend handles them in a similar way.

## Syntax

```sql
MERGE INTO <target_table>
    USING (SELECT ... ) [AS] <alias> ON <join_expr> { matchedClause | notMatchedClause } [ ... ]

matchedClause ::=
  WHEN MATCHED [ AND <condition> ] THEN
  {
    UPDATE SET <col_name> = <expr> [ , <col_name2> = <expr2> ... ] |
    UPDATE * |
    DELETE  /* Removes matched rows from the target table */
  }

notMatchedClause ::=
  WHEN NOT MATCHED [ AND <condition> ] THEN
  { INSERT ( <col_name> [ , <col_name2> ... ] ) VALUES ( <expr> [ , ... ] ) | INSERT * }
```

| Parameter | Description                                                                                                                                                                                                                                                                                   |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| UPDATE \* | Updates all columns of the matched row in the target table with values from the corresponding row in the source. This requires the column names between the source and target are consistent (though their order can be different) because during the update process, matching is done based on column names. |
| INSERT \* | Inserts a new row into the target table with values from the source row.                                                                                                                                                                                                                                      |
| DELETE    | Removes the matched row from the target table. This is a powerful operation that can be used for data cleanup, removing obsolete records, or implementing conditional deletion logic based on source data.                                                                                                     |

## Output

MERGE provides a summary of the data merge results with these columns:

| Column                  | Description                                          |
| ----------------------- | ---------------------------------------------------- |
| number of rows inserted | Count of new rows added to the target table.         |
| number of rows updated  | Count of existing rows modified in the target table. |
| number of rows deleted  | Count of rows deleted from the target table.         |

## Examples

### Example 1: Merge with Multiple Matched Clauses

This example uses MERGE to synchronize employee data from 'employees' into 'salaries', allowing for inserting and updating salary information based on specified criteria.

```sql
-- Create the 'employees' table as the source for merging
CREATE TABLE employees (
    employee_id INT,
    employee_name VARCHAR(255),
    department VARCHAR(255)
);

-- Create the 'salaries' table as the target for merging
CREATE TABLE salaries (
    employee_id INT,
    salary DECIMAL(10, 2)
);

-- Insert initial employee data
INSERT INTO employees VALUES
    (1, 'Alice', 'HR'),
    (2, 'Bob', 'IT'),
    (3, 'Charlie', 'Finance'),
    (4, 'David', 'HR');

-- Insert initial salary data
INSERT INTO salaries VALUES
    (1, 50000.00),
    (2, 60000.00);

-- Enable MERGE INTO

-- Merge data into 'salaries' based on employee details from 'employees'
MERGE INTO salaries
    USING (SELECT * FROM employees) AS employees
    ON salaries.employee_id = employees.employee_id
    WHEN MATCHED AND employees.department = 'HR' THEN
        UPDATE SET
            salaries.salary = salaries.salary + 1000.00
    WHEN MATCHED THEN
        UPDATE SET
            salaries.salary = salaries.salary + 500.00
    WHEN NOT MATCHED THEN
        INSERT (employee_id, salary)
            VALUES (employees.employee_id, 55000.00);

┌──────────────────────────────────────────────────┐
│ number of rows inserted │ number of rows updated │
├─────────────────────────┼────────────────────────┤
│                      2  │                      2 │
└──────────────────────────────────────────────────┘

-- Retrieve all records from the 'salaries' table after merging
SELECT * FROM salaries;

┌────────────────────────────────────────────┐
│   employee_id   │          salary          │
├─────────────────┼──────────────────────────┤
│               3 │ 55000.00                 │
│               4 │ 55000.00                 │
│               1 │ 51000.00                 │
│               2 │ 60500.00                 │
└────────────────────────────────────────────┘
```

### Example 2: Merge with UPDATE \* & INSERT \*

This example uses MERGE to synchronize data between the target_table and source_table, updating matching rows with values from the source and inserting non-matching rows.

```sql
-- Create the target table target_table
CREATE TABLE target_table (
    ID INT,
    Name VARCHAR(50),
    Age INT,
    City VARCHAR(50)
);

-- Insert initial data into target_table
INSERT INTO target_table (ID, Name, Age, City)
VALUES
    (1, 'Alice', 25, 'Toronto'),
    (2, 'Bob', 30, 'Vancouver'),
    (3, 'Carol', 28, 'Montreal');

-- Create the source table source_table
CREATE TABLE source_table (
    ID INT,
    Name VARCHAR(50),
    Age INT,
    City VARCHAR(50)
);

-- Insert initial data into source_table
INSERT INTO source_table (ID, Name, Age, City)
VALUES
    (1, 'David', 27, 'Calgary'),
    (2, 'Emma', 29, 'Ottawa'),
    (4, 'Frank', 32, 'Edmonton');

-- Enable MERGE INTO

-- Merge data from source_table into target_table
MERGE INTO target_table AS T
    USING (SELECT * FROM source_table) AS S
    ON T.ID = S.ID
    WHEN MATCHED THEN
        UPDATE *
    WHEN NOT MATCHED THEN
    INSERT *;

┌──────────────────────────────────────────────────┐
│ number of rows inserted │ number of rows updated │
├─────────────────────────┼────────────────────────┤
│                      1  │                      2 │
└──────────────────────────────────────────────────┘

-- Retrieve all records from the 'target_table' after merging
SELECT * FROM target_table order by ID;

┌─────────────────────────────────────────────────────────────────────────┐
│        id       │       name       │       age       │       city       │
├─────────────────┼──────────────────┼─────────────────┼──────────────────┤
│               1 │ David            │              27 │ Calgary          │
│               2 │ Emma             │              29 │ Ottawa           │
│               3 │ Carol            │              28 │ Montreal         │
│               4 │ Frank            │              32 │ Edmonton         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Example 3: Merge with DELETE Operation

This example demonstrates how to use MERGE to delete records from the target table based on specific conditions from the source table.

```sql
-- Create the customers table (target)
CREATE TABLE customers (
    customer_id INT,
    customer_name VARCHAR(50),
    status VARCHAR(20),
    last_purchase_date DATE
);

-- Insert initial customer data
INSERT INTO customers VALUES
    (101, 'John Smith', 'Active', '2023-01-15'),
    (102, 'Emma Johnson', 'Active', '2023-02-20'),
    (103, 'Michael Brown', 'Inactive', '2022-11-05'),
    (104, 'Sarah Wilson', 'Active', '2023-03-10'),
    (105, 'David Lee', 'Inactive', '2022-09-30');

-- Create the removals table (source with customers to be removed)
CREATE TABLE removals (
    customer_id INT,
    removal_reason VARCHAR(50),
    removal_date DATE
);

-- Insert data for customers to be removed
INSERT INTO removals VALUES
    (103, 'Account Closed', '2023-04-01'),
    (105, 'Customer Request', '2023-04-05');

-- Enable MERGE INTO

-- Use MERGE to delete inactive customers that appear in the removals table
MERGE INTO customers AS c
    USING removals AS r
    ON c.customer_id = r.customer_id
    WHEN MATCHED AND c.status = 'Inactive' THEN
        DELETE;

┌────────────────────────┐
│ number of rows deleted │
├────────────────────────┤
│                     2  │
└────────────────────────┘
```
