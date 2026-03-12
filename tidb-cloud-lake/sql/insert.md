---
title: INSERT
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.738"/>

Inserts one or more rows into a table.

:::tip atomic operations
Databend ensures data integrity with atomic operations. Inserts, updates, replaces, and deletes either succeed completely or fail entirely.
:::

See also: [INSERT (multi-table)](dml-insert-multi.md)

## Syntax

```sql
INSERT { OVERWRITE [ INTO ] | INTO } <table>
    -- Optionally specify the columns to insert into
    ( <column> [ , ... ] )
    -- Insertion options:
    {
        -- Directly insert values or default values
        VALUES ( <value> | DEFAULT ) [ , ... ] |
        -- Insert the result of a query
        SELECT ...
    }
```

| Parameter          | Description                                                                      |
|--------------------|----------------------------------------------------------------------------------|
| `OVERWRITE [INTO]` | Indicates whether existing data should be truncated before insertion.            |
| `VALUES`           | Allows direct insertion of specific values or the default values of the columns. |

## Important Notes

- Aggregate functions, external UDFs, and window functions are not allowed in the `VALUES(...)` expressions.

## Examples

### Example-1: Insert Values with OVERWRITE

In this example, the INSERT OVERWRITE statement is utilized to truncate the employee table and insert new data, replacing all existing records with the values provided for an employee with ID 100.

```sql
CREATE TABLE employee (
    employee_id INT,
    employee_name VARCHAR(50)
);

-- Inserting initial data into the employee table
INSERT INTO employee(employee_id, employee_name) VALUES
    (101, 'John Doe'),
    (102, 'Jane Smith');

-- Inserting new data with OVERWRITE
INSERT OVERWRITE employee VALUES (100, 'John Johnson');

-- Displaying the contents of the employee table
SELECT * FROM employee;

┌────────────────────────────────────┐
│   employee_id   │   employee_name  │
├─────────────────┼──────────────────┤
│             100 │ John Johnson     │
└────────────────────────────────────┘
```

### Example-2: Insert Query Results

When inserting the results of a SELECT statement, the mapping of columns follows their positions in the SELECT clause. Therefore, the number of columns in the SELECT statement must be equal to or greater than the number of columns in the INSERT table. In cases where the data types of the columns in the SELECT statement and the INSERT table differ, type casting will be performed as needed.

```sql
-- Creating a table named 'employee_info' with three columns: 'employee_id', 'employee_name', and 'department'
CREATE TABLE employee_info (
    employee_id INT,
    employee_name VARCHAR(50),
    department VARCHAR(50)
);

-- Inserting a record into the 'employee_info' table
INSERT INTO employee_info VALUES ('101', 'John Doe', 'Marketing');

-- Creating a table named 'employee_data' with three columns: 'ID', 'Name', and 'Dept'
CREATE TABLE employee_data (
    ID INT,
    Name VARCHAR(50),
    Dept VARCHAR(50)
);

-- Inserting data from 'employee_info' into 'employee_data'
INSERT INTO employee_data SELECT * FROM employee_info;

-- Displaying the contents of the 'employee_data' table
SELECT * FROM employee_data;

┌───────────────────────────────────────────────────────┐
│        id       │       name       │       dept       │
├─────────────────┼──────────────────┼──────────────────┤
│             101 │ John Doe         │ Marketing        │
└───────────────────────────────────────────────────────┘
```

This example demonstrates creating a summary table named "sales_summary" to store aggregated sales data such as total quantity sold and revenue for each product by aggregating information from the sales table:

```sql
-- Creating a table for sales data
CREATE TABLE sales (
    product_id INT,
    quantity_sold INT,
    revenue DECIMAL(10, 2)
);

-- Inserting some sample sales data
INSERT INTO sales (product_id, quantity_sold, revenue) VALUES
    (1, 100, 500.00),
    (2, 150, 750.00),
    (1, 200, 1000.00),
    (3, 50, 250.00);

-- Creating a summary table to store aggregated sales data
CREATE TABLE sales_summary (
    product_id INT,
    total_quantity_sold INT,
    total_revenue DECIMAL(10, 2)
);

-- Inserting aggregated sales data into the summary table
INSERT INTO sales_summary (product_id, total_quantity_sold, total_revenue)
SELECT 
    product_id,
    SUM(quantity_sold) AS total_quantity_sold,
    SUM(revenue) AS total_revenue
FROM 
    sales
GROUP BY 
    product_id;

-- Displaying the contents of the sales_summary table
SELECT * FROM sales_summary;

┌──────────────────────────────────────────────────────────────────┐
│    product_id   │ total_quantity_sold │       total_revenue      │
├─────────────────┼─────────────────────┼──────────────────────────┤
│               1 │                 300 │ 1500.00                  │
│               3 │                  50 │ 250.00                   │
│               2 │                 150 │ 750.00                   │
└──────────────────────────────────────────────────────────────────┘
```

### Example-3: Insert Default Values

This example illustrates creating a table called "staff_records", with default values set for columns such as department and status. Data is then inserted, showcasing default value usage.

```sql
-- Creating a table 'staff_records' with columns 'employee_id', 'department', 'salary', and 'status' with default values
CREATE TABLE staff_records (
    employee_id INT NULL,
    department VARCHAR(50) DEFAULT 'HR',
    salary FLOAT,
    status VARCHAR(10) DEFAULT 'Active'
);

-- Inserting data into 'staff_records' with default values
INSERT INTO staff_records
VALUES
    (DEFAULT, DEFAULT, DEFAULT, DEFAULT),
    (101, DEFAULT, 50000.00, DEFAULT),
    (102, 'Finance', 60000.00, 'Inactive'),
    (103, 'Marketing', 70000.00, 'Active');

-- Displaying the contents of the 'staff_records' table
SELECT * FROM staff_records;

┌───────────────────────────────────────────────────────────────────────────┐
│   employee_id   │    department    │       salary      │      status      │
├─────────────────┼──────────────────┼───────────────────┼──────────────────┤
│            NULL │ HR               │              NULL │ Active           │
│             101 │ HR               │             50000 │ Active           │
│             102 │ Finance          │             60000 │ Inactive         │
│             103 │ Marketing        │             70000 │ Active           │
└───────────────────────────────────────────────────────────────────────────┘
```

### Example-4: Insert with Staged Files

Databend enables you to insert data into a table from staged files with the INSERT INTO statement. This is achieved through Databend's capacity to [Query Staged Files](/guides/load-data/transform/querying-stage) and subsequently incorporate the query result into the table. 

1. Create a table called `sample`:

```sql
CREATE TABLE sample
(
    id      INT,
    city    VARCHAR,
    score   INT,
    country VARCHAR DEFAULT 'China'
);
```

2. Set up an internal stage with sample data

We'll establish an internal stage named `mystage` and then populate it with sample data.

```sql
CREATE STAGE mystage;
       
COPY INTO @mystage
FROM 
(
    SELECT * 
    FROM 
    (
        VALUES 
        (1, 'Chengdu', 80),
        (3, 'Chongqing', 90),
        (6, 'Hangzhou', 92),
        (9, 'Hong Kong', 88)
    )
)
FILE_FORMAT = (TYPE = PARQUET);
```

3. Insert data from the staged Parquet file with `INSERT INTO`

:::tip
You can specify the file format and various copy-related settings with the FILE_FORMAT and COPY_OPTIONS available in the [COPY INTO](dml-copy-into-table.md) command. When `purge` is set to `true`, the original file will only be deleted if the data update is successful. 
:::

```sql
INSERT INTO sample 
    (id, city, score) 
ON
    (Id)
SELECT
    $1, $2, $3
FROM
    @mystage
    (FILE_FORMAT => 'parquet');
```

4. Verify the data insert

```sql
SELECT * FROM sample;
```

The results should be:
```sql
┌─────────────────────────────────────────────────────────────────────────┐
│        id       │       city       │      score      │      country     │
├─────────────────┼──────────────────┼─────────────────┼──────────────────┤
│               1 │ Chengdu          │              80 │ China            │
│               3 │ Chongqing        │              90 │ China            │
│               6 │ Hangzhou         │              92 │ China            │
│               9 │ Hong Kong        │              88 │ China            │
└─────────────────────────────────────────────────────────────────────────┘
```