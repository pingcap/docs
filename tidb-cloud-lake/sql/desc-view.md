---
title: DESC VIEW
summary: 返回视图的列列表。
---

# DESC VIEW

返回视图的列列表。

## 语法 {#syntax}

```sql
DESC[RIBE] VIEW [<database_name>.]<view_name>
```

## 输出 {#output}

该命令会输出一个包含以下列的表：

| 列名 | 描述 |
|---------|-------------------------------------------------------------------------------------------------------------------------|
| Field   | 视图中列的名称。                                                                                     |
| Type    | 列的数据类型。                                                                                            |
| Null    | 指示该列是否允许 NULL 值（YES 表示允许 NULL，NO 表示不允许 NULL）。                      |
| Default | 指定列的默认值。                                                                             |
| Extra   | 提供有关该列的附加信息，例如它是否为计算列，或其他特殊属性。 |

## 示例 {#examples}

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