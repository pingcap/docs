---
title: INSERT
summary: 向表中插入一行或多行数据。
---

# INSERT

向表中插入一行或多行数据。

> **Tip:**
>
> {{{ .lake }}} 通过原子操作确保数据完整性。插入、修改、替换和删除操作要么全部成功，要么全部失败。

另请参阅：[INSERT（多表）](/tidb-cloud-lake/sql/insert-multi-table.md)

## 语法 {#syntax}

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

| 参数               | 描述                                                                             |
|--------------------|----------------------------------------------------------------------------------|
| `OVERWRITE [INTO]` | 指示在插入前是否应截断现有数据。                                                 |
| `VALUES`           | 允许直接插入指定值或列的默认值。                                                 |

## 重要说明 {#important-notes}

- 在 `VALUES(...)` 表达式中，不允许使用聚合函数、外部 UDF 和窗口函数。

## 示例 {#examples}

### 示例 1：使用 OVERWRITE 插入值 {#example-1-insert-values-with-overwrite}

在此示例中，使用 INSERT OVERWRITE 语句截断 employee 表并插入新数据，用 employee_id 为 100 的员工数据替换所有现有记录。

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

### 示例 2：插入查询结果 {#example-2-insert-query-results}

插入 SELECT 语句的结果时，列映射遵循它们在 SELECT 子句中的位置。因此，SELECT 语句中的列数必须等于或大于 INSERT 目标表中的列数。如果 SELECT 语句中的列与 INSERT 目标表中的列数据类型不同，则会根据需要执行类型转换。

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

以下示例展示了如何创建一个名为 "sales_summary" 的汇总表，通过聚合 sales 表中的信息，存储每个产品的销售汇总数据，例如销售总数量和总收入：

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

### 示例 3：插入默认值 {#example-3-insert-default-values}

本示例展示了如何创建一个名为 "staff_records" 的表，并为 department 和 status 等列设置默认值。随后插入数据，以演示默认值的用法。

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

### 示例-4：使用 staged files 插入数据 {#example-4-insert-with-staged-files}

{{{ .lake }}} 支持你使用 `INSERT INTO` 语句将 staged files 中的数据插入到表中。这是通过 {{{ .lake }}} 查询 [查询 Stage 文件](/tidb-cloud-lake/sql/stage.md) 并将查询结果进一步写入表中来实现的。

1. 创建一个名为 `sample` 的表：

    ```sql
    CREATE TABLE sample
    (
        id      INT,
        city    VARCHAR,
        score   INT,
        country VARCHAR DEFAULT 'China'
    );
    ```

2. 设置一个包含示例数据的内部 stage

    我们将创建一个名为 `mystage` 的内部 stage，然后用示例数据填充它。

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

3. 使用 `INSERT INTO` 从 stage 中的 Parquet 文件插入数据

    > **Tip:**
    >
    > 你可以使用 [COPY INTO](/tidb-cloud-lake/sql/copy-into-table.md) 命令中提供的 `FILE_FORMAT` 和 `COPY_OPTIONS` 来指定文件格式以及各种与复制相关的设置。当 `purge` 设置为 `true` 时，只有在数据修改成功后，原始文件才会被删除。

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

4. 验证插入的数据

```sql
SELECT * FROM sample;
```

结果应如下所示：

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