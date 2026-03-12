---
title: INSERT (multi-table)
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.396"/>

Inserts rows into multiple tables in a single transaction, with the option for the insertion to be dependent on certain conditions (conditionally) or to occur regardless of any conditions (unconditionally).

:::tip atomic operations
Databend ensures data integrity with atomic operations. Inserts, updates, replaces, and deletes either succeed completely or fail entirely.
:::

See also: [INSERT](dml-insert.md)

## Syntax

```sql
-- Unconditional INSERT ALL: Inserts each row into multiple tables without any conditions or restrictions.
INSERT [ OVERWRITE ] ALL
    INTO <target_table> [ ( <target_col_name> [ , ... ] ) ] [ VALUES ( <source_col_name> [ , ... ] ) ]
    ...
SELECT ...


-- Conditional INSERT ALL: Inserts each row into multiple tables, but only if certain conditions are met.
INSERT [ OVERWRITE ] ALL
    WHEN <condition> THEN
        INTO <target_table> [ ( <target_col_name> [ , ... ] ) ] [ VALUES ( <source_col_name> [ , ... ] ) ]
      [ INTO ... ]

  [ WHEN ... ]

  [ ELSE INTO ... ]
SELECT ...


-- Conditional INSERT FIRST: Inserts each row into multiple tables, but stops after the first successful insertion.
INSERT [ OVERWRITE ] FIRST
    WHEN <condition> THEN
        INTO <target_table> [ ( <target_col_name> [ , ... ] ) ] [ VALUES ( <source_col_name> [ , ... ] ) ]
      [ INTO ... ]

  [ WHEN ... ]

  [ ELSE INTO ... ]
SELECT ...
```

| Parameter                                | Description                                                                                                                                                                                                                                                                                                                                           |
| ---------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `OVERWRITE`                              | Indicates whether existing data should be truncated before insertion.                                                                                                                                                                                                                                                                                 |
| `( <target_col_name> [ , ... ] )`        | Specifies the column names in the target table where data will be inserted.<br/>- If omitted, data will be inserted into all columns in the target table.                                                                                                                                                                                             |
| `VALUES ( <source_col_name> [ , ... ] )` | Specifies the source column names from which data will be inserted into the target table.<br/>- If omitted, all columns returned by the subquery will be inserted into the target table.<br/>- The data types of the columns listed in `<source_col_name>` must match or be compatible with those specified in `<target_col_name>`.                   |
| `SELECT ...`                             | A subquery that provides the data to be inserted into the target table(s).<br/>- You have the option to explicitly assign aliases to columns within the subquery. This allows you to reference the columns by their aliases within WHEN clauses and VALUES clauses.                                                                                   |
| `WHEN`                                   | Conditional statement to determine when to insert data into specific target tables.<br/>- A conditional multi-table insert requires at least one WHEN clause.<br/>- A WHEN clause can include multiple INTO clauses, and these INTO clauses can target the same table.<br/>- To unconditionally execute a WHEN clause, you can use `WHEN 1 THEN ...`. |
| `ELSE`                                   | Specifies the action to take if none of the conditions specified in the WHEN clauses are met.                                                                                                                                                                                                                                                        |
## Important Notes

- Aggregate functions, external UDFs, and window functions are not allowed in the `VALUES(...)` expressions.

## Examples

### Example-1: Unconditional INSERT ALL

This example demonstrates an Unconditional INSERT ALL operation, inserting each row from the `employee_data_source` table into both the `employees` and `employee_history` tables.

1. Create tables for managing employee data, including employee details and their employment history, then populate a source table with sample employee information.

```sql
-- Create the employees table
CREATE TABLE employees (
    employee_id INT,
    employee_name VARCHAR(100),
    hire_date DATE
);

-- Create the employee_history table
CREATE TABLE employee_history (
    employee_id INT,
    hire_date DATE,
    termination_date DATE
);

-- Create the employee_data_source table
CREATE TABLE employee_data_source (
    employee_id INT,
    employee_name VARCHAR(100),
    hire_date DATE
);

-- Insert data into the employee_data_source table
INSERT INTO employee_data_source (employee_id, employee_name, hire_date)
VALUES
    (1, 'Alice', '2023-01-15'),
    (2, 'Bob', '2023-02-20'),
    (3, 'Charlie', '2023-03-25');
```

2. Transfer data from the `employee_data_source` table into both the `employees` and `employee_history` tables with an unconditional INSERT ALL operation.

```sql
-- Unconditional INSERT ALL: Insert data into the employees and employee_history tables
INSERT ALL
    INTO employees (employee_id, employee_name, hire_date) VALUES (employee_id, employee_name, hire_date)
    INTO employee_history (employee_id, hire_date) VALUES (employee_id, hire_date)
SELECT employee_id, employee_name, hire_date FROM employee_data_source;

-- Query the employees table
SELECT * FROM employees;

┌─────────────────────────────────────────────────────┐
│   employee_id   │   employee_name  │    hire_date   │
├─────────────────┼──────────────────┼────────────────┤
│               1 │ Alice            │ 2023-01-15     │
│               2 │ Bob              │ 2023-02-20     │
│               3 │ Charlie          │ 2023-03-25     │
└─────────────────────────────────────────────────────┘

-- Query the employee_history table
SELECT * FROM employee_history;

┌─────────────────────────────────────────────────────┐
│   employee_id   │    hire_date   │ termination_date │
├─────────────────┼────────────────┼──────────────────┤
│               1 │ 2023-01-15     │ NULL             │
│               2 │ 2023-02-20     │ NULL             │
│               3 │ 2023-03-25     │ NULL             │
└─────────────────────────────────────────────────────┘
```

### Example-2: Conditional INSERT ALL & FIRST

This example demonstrates conditional INSERT ALL, inserting sales data into separate tables based on specific conditions, where records satisfying multiple conditions are inserted into all corresponding tables.

1. Create three tables: products, `high_quantity_sales`, `high_price_sales`, and `sales_data_source`. Then, insert three sales records into the `sales_data_source` table.

```sql
-- Create the high_quantity_sales table
CREATE TABLE high_quantity_sales (
    sale_id INT,
    product_id INT,
    sale_date DATE,
    quantity INT,
    total_price DECIMAL(10, 2)
);

-- Create the high_price_sales table
CREATE TABLE high_price_sales (
    sale_id INT,
    product_id INT,
    sale_date DATE,
    quantity INT,
    total_price DECIMAL(10, 2)
);

-- Create the sales_data_source table
CREATE TABLE sales_data_source (
    sale_id INT,
    product_id INT,
    sale_date DATE,
    quantity INT,
    total_price DECIMAL(10, 2)
);

-- Insert data into the sales_data_source table
INSERT INTO sales_data_source (sale_id, product_id, sale_date, quantity, total_price)
VALUES
    (1, 101, '2023-01-15', 5, 100.00),
    (2, 102, '2023-02-20', 3, 75.00),
    (3, 103, '2023-03-25', 10, 200.00);
```

2. Insert rows into multiple tables based on specific conditions using conditional INSERT ALL. Records with a quantity greater than 4 are inserted into the `high_quantity_sales` table, and those with a total price exceeding 50 are inserted into the `high_price_sales` table.

```sql
-- Conditional INSERT ALL: Inserts each row into multiple tables, but only if certain conditions are met.
INSERT ALL
    WHEN quantity > 4 THEN INTO high_quantity_sales
    WHEN total_price > 50 THEN INTO high_price_sales
SELECT * FROM sales_data_source;

SELECT * FROM high_quantity_sales;

┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│     sale_id     │    product_id   │    sale_date   │     quantity    │        total_price       │
├─────────────────┼─────────────────┼────────────────┼─────────────────┼──────────────────────────┤
│               1 │             101 │ 2023-01-15     │               5 │ 100.00                   │
│               3 │             103 │ 2023-03-25     │              10 │ 200.00                   │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘

SELECT * FROM high_price_sales;

┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│     sale_id     │    product_id   │    sale_date   │     quantity    │        total_price       │
├─────────────────┼─────────────────┼────────────────┼─────────────────┼──────────────────────────┤
│               1 │             101 │ 2023-01-15     │               5 │ 100.00                   │
│               2 │             102 │ 2023-02-20     │               3 │ 75.00                    │
│               3 │             103 │ 2023-03-25     │              10 │ 200.00                   │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

3. Empty the data from the high_quantity_sales and high_price_sales tables.

```sql
TRUNCATE TABLE high_quantity_sales;

TRUNCATE TABLE high_price_sales;
```

4. Insert rows into multiple tables based on specific conditions using conditional INSERT FIRST. For each row, it stops after the first successful insertion, therefore, the sales records with IDs 1 and 3 are inserted into the `high_quantity_sales` table only, compared to the conditional INSERT ALL results in Step 2.

```sql
-- Conditional INSERT FIRST: Inserts each row into multiple tables, but stops after the first successful insertion.
INSERT FIRST
    WHEN quantity > 4 THEN INTO high_quantity_sales
    WHEN total_price > 50 THEN INTO high_price_sales
SELECT * FROM sales_data_source;


SELECT * FROM high_quantity_sales;

┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│     sale_id     │    product_id   │    sale_date   │     quantity    │        total_price       │
├─────────────────┼─────────────────┼────────────────┼─────────────────┼──────────────────────────┤
│               1 │             101 │ 2023-01-15     │               5 │ 100.00                   │
│               3 │             103 │ 2023-03-25     │              10 │ 200.00                   │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘

SELECT * FROM high_price_sales;

┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│     sale_id     │    product_id   │    sale_date   │     quantity    │        total_price       │
├─────────────────┼─────────────────┼────────────────┼─────────────────┼──────────────────────────┤
│               2 │             102 │ 2023-02-20     │               3 │ 75.00                    │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Example-3: Insert with Explicit Alias

This example demonstrates using alias in VALUES clause to conditionally insert rows from the employees table into the `employee_history` table based on the hire date being after '2023-02-01'.

1. Create two tables, `employees` and `employee_history`, and insert sample employee data into the `employees` table.

```sql
-- Create tables
CREATE TABLE employees (
    employee_id INT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    hire_date DATE
);

CREATE TABLE employee_history (
    employee_id INT,
    full_name VARCHAR(100),
    hire_date DATE
);

INSERT INTO employees (employee_id, first_name, last_name, hire_date)
VALUES
    (1, 'John', 'Doe', '2023-01-01'),
    (2, 'Jane', 'Smith', '2023-02-01'),
    (3, 'Michael', 'Johnson', '2023-03-01');
```

2. Utilize conditional insertion with an alias to transfer records from the employees table to the `employee_history` table, filtering for hire dates after '2023-02-01'.

```sql
INSERT ALL
    WHEN hire_date >= '2023-02-01' THEN INTO employee_history
        VALUES (employee_id, full_name, hire_date) -- Insert with the alias 'full_name'
SELECT employee_id, CONCAT(first_name, ' ', last_name) AS full_name, hire_date -- Alias the concatenated full name as 'full_name'
FROM employees;

SELECT * FROM employee_history;

┌─────────────────────────────────────────────────────┐
│   employee_id   │     full_name    │    hire_date   │
│ Nullable(Int32) │ Nullable(String) │ Nullable(Date) │
├─────────────────┼──────────────────┼────────────────┤
│               2 │ Jane Smith       │ 2023-02-01     │
│               3 │ Michael Johnson  │ 2023-03-01     │
└─────────────────────────────────────────────────────┘
```
