---
title: CASE
summary: 处理 IF/THEN 逻辑。它由至少一对 `WHEN` 和 `THEN` 语句组成。每个 `CASE` 语句都必须以 `END` 关键字结束。`ELSE` 语句是可选的，用于捕获未在 `WHEN` 和 `THEN` 语句中显式指定的值。
---

# CASE

处理 IF/THEN 逻辑。它由至少一对 `WHEN` 和 `THEN` 语句组成。每个 `CASE` 语句都必须以 `END` 关键字结束。`ELSE` 语句是可选的，用于捕获未在 `WHEN` 和 `THEN` 语句中显式指定的值。

## 语法 {#syntax}

```sql
CASE
    WHEN <condition_1> THEN <value_1>
  [ WHEN <condition_2> THEN <value_2> ]
  [ ... ]
  [ ELSE <value_n> ]
END AS <column_name>
```

## 示例 {#examples}

以下示例使用 CASE 语句对员工薪资进行分类，并通过动态分配的列 `"SalaryCategory"` 展示结果详情：

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