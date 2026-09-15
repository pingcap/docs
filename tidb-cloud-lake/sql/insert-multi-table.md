---
title: INSERT（多表）
summary: 在单个事务中向多个表插入行，并且可以选择让插入依赖某些条件（有条件）或不受任何条件限制（无条件）。
---

# INSERT（多表）

在单个事务中向多个表插入行，并且可以选择让插入依赖某些条件（有条件）或不受任何条件限制（无条件）。

> **Tip:**
>
> {{{ .lake }}} 通过原子操作确保数据完整性。插入、修改、替换和删除要么全部成功，要么全部失败。

另请参阅：[INSERT](/tidb-cloud-lake/sql/insert.md)

## 语法 {#syntax}

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

| 参数                                     | 描述                                                                                                                                                                                                                                                                                                                                 |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `OVERWRITE`                              | 指示在插入前是否应截断现有数据。                                                                                                                                                                                                                                                                                                     |
| `( <target_col_name> [ , ... ] )`        | 指定目标表中将要插入数据的列名。<br/>- 如果省略，则会将数据插入目标表中的所有列。                                                                                                                                                                                                                                                    |
| `VALUES ( <source_col_name> [ , ... ] )` | 指定将数据插入目标表时所使用的源列名。<br/>- 如果省略，则子查询返回的所有列都会被插入目标表。<br/>- `<source_col_name>` 中列出的列的数据类型必须与 `<target_col_name>` 中指定的列匹配或兼容。                                                                                                                                      |
| `SELECT ...`                             | 为目标表提供待插入数据的子查询。<br/>- 你可以选择在子查询中为列显式指定别名。这样就可以在 WHEN 子句和 VALUES 子句中通过这些别名引用列。                                                                                                                                                                                              |
| `WHEN`                                   | 用于确定何时向特定目标表插入数据的条件语句。<br/>- 有条件的多表插入至少需要一个 WHEN 子句。<br/>- 一个 WHEN 子句可以包含多个 INTO 子句，并且这些 INTO 子句可以指向同一个表。<br/>- 如果要无条件执行某个 WHEN 子句，可以使用 `WHEN 1 THEN ...`。                                                                                     |
| `ELSE`                                   | 指定当 WHEN 子句中定义的条件都不满足时要执行的操作。                                                                                                                                                                                                                                                                                 |

## 重要说明 {#important-notes}

- `VALUES(...)` 表达式中不允许使用聚合函数、外部 UDF 和窗口函数。

## 示例 {#examples}

### 示例 1：无条件 INSERT ALL {#example-1-unconditional-insert-all}

本示例演示无条件 INSERT ALL 操作，将 `employee_data_source` 表中的每一行同时插入到 `employees` 和 `employee_history` 表中。

1. 创建用于管理员工数据的表，包括员工详细信息及其雇佣历史，然后向源表中填充示例员工信息。

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

2. 通过无条件 INSERT ALL 操作，将 `employee_data_source` 表中的数据同时传输到 `employees` 和 `employee_history` 表中。

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

### 示例-2：条件 INSERT ALL 和 FIRST {#example-2-conditional-insert-all-first}

本示例演示条件 INSERT ALL：根据特定条件将销售数据插入到不同的表中。满足多个条件的记录会被插入到所有对应的表中。

1. 创建三个表：products、`high_quantity_sales`、`high_price_sales` 和 `sales_data_source`。然后，向 `sales_data_source` 表中插入三条销售记录。

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

2. 使用条件 INSERT ALL 根据特定条件将行插入到多个表中。数量大于 4 的记录会插入到 `high_quantity_sales` 表中，总价大于 50 的记录会插入到 `high_price_sales` 表中。

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

3. 清空 high_quantity_sales 和 high_price_sales 表中的数据。

    ```sql
    TRUNCATE TABLE high_quantity_sales;
    
    TRUNCATE TABLE high_price_sales;
    ```

4. 使用条件 INSERT FIRST 根据特定条件将行插入到多个表中。对于每一行，在第一次成功插入后就会停止。因此，与步骤 2 中条件 INSERT ALL 的结果相比，ID 为 1 和 3 的销售记录只会插入到 `high_quantity_sales` 表中。

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

### 示例-3：使用显式别名插入 {#example-3-insert-with-explicit-alias}

本示例演示如何在 VALUES 子句中使用别名，根据入职日期晚于 '2023-02-01' 的条件，将 `employees` 表中的行有条件地插入到 `employee_history` 表中。

1. 创建两个表 `employees` 和 `employee_history`，并向 `employees` 表中插入示例员工数据。

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

2. 使用带别名的条件插入，将记录从 employees 表转移到 `employee_history` 表中，并筛选入职日期晚于 '2023-02-01' 的记录。

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