---
title: CASE
summary: IF/THEN ロジックを処理します。少なくとも 1 組の WHEN と THEN 文で構成されます。すべての CASE 文は END キーワードで終了する必要があります。ELSE 文は省略可能で、WHEN および THEN 文で明示的に指定されていない値を扱うための方法を提供します。
---

# CASE

IF/THEN ロジックを処理します。少なくとも 1 組の `WHEN` 文と `THEN` 文で構成されます。すべての `CASE` 文は `END` キーワードで終了する必要があります。`ELSE` 文は省略可能で、`WHEN` 文および `THEN` 文で明示的に指定されていない値を扱うための方法を提供します。

## 構文 {#syntax}

```sql
CASE
    WHEN <condition_1> THEN <value_1>
  [ WHEN <condition_2> THEN <value_2> ]
  [ ... ]
  [ ELSE <value_n> ]
END AS <column_name>
```

## 例 {#examples}

この例では、CASE 文を使用して従業員の給与を分類し、"SalaryCategory" という名前の動的に割り当てられたカラムとともに詳細を表示します。

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