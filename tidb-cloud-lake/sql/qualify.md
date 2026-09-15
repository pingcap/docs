---
title: QUALIFY
summary: QUALIFY 是一个用于过滤窗口函数结果的子句。因此，要成功使用 QUALIFY 子句，SELECT 列表或 QUALIFY 子句中必须至少包含一个窗口函数（每种情况请参见示例）。换句话说，QUALIFY 会在窗口函数计算完成后再进行求值。以下是包含 QUALIFY 语句子句的查询的典型执行顺序。
---

# QUALIFY

QUALIFY 是一个用于过滤窗口函数结果的子句。因此，要成功使用 QUALIFY 子句，SELECT 列表或 QUALIFY 子句中必须至少包含一个窗口函数（每种情况请参见[示例](#examples)）。换句话说，QUALIFY 会在窗口函数计算完成后再进行求值。以下是包含 QUALIFY 语句子句的查询的典型执行顺序：

1. FROM
2. WHERE
3. GROUP BY
4. HAVING
5. WINDOW FUNCTION
6. QUALIFY
7. DISTINCT
8. ORDER BY
9. LIMIT

## 语法 {#syntax}

```sql
QUALIFY <predicate>
```

## 示例 {#examples}

本示例演示了如何使用 ROW_NUMBER() 按部门为员工分配连续编号，并按薪资降序排序。借助 QUALIFY 子句，我们可以过滤结果，仅显示每个部门中薪资最高的员工。

```sql
-- Prepare the data
CREATE TABLE employees (
  employee_id INT,
  first_name VARCHAR,
  last_name VARCHAR,
  department VARCHAR,
  salary INT
);

INSERT INTO employees (employee_id, first_name, last_name, department, salary) VALUES
  (1, 'John', 'Doe', 'IT', 90000),
  (2, 'Jane', 'Smith', 'HR', 85000),
  (3, 'Mike', 'Johnson', 'IT', 82000),
  (4, 'Sara', 'Williams', 'Sales', 77000),
  (5, 'Tom', 'Brown', 'HR', 75000);

-- Select employee details along with the row number partitioned by department and ordered by salary in descending order.
SELECT
    employee_id,
    first_name,
    last_name,
    department,
    salary,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS row_num
FROM
    employees;

┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐
│   employee_id   │    first_name    │     last_name    │    department    │      salary     │ row_num │
├─────────────────┼──────────────────┼──────────────────┼──────────────────┼─────────────────┼─────────┤
│               2 │ Jane             │ Smith            │ HR               │           85000 │       1 │
│               5 │ Tom              │ Brown            │ HR               │           75000 │       2 │
│               1 │ John             │ Doe              │ IT               │           90000 │       1 │
│               3 │ Mike             │ Johnson          │ IT               │           82000 │       2 │
│               4 │ Sara             │ Williams         │ Sales            │           77000 │       1 │
└──────────────────────────────────────────────────────────────────────────────────────────────────────┘

-- Select employee details along with the row number partitioned by department and ordered by salary in descending order.
-- Add a filter to only include rows where the row number is 1, selecting the employee with the highest salary in each department.
SELECT
    employee_id,
    first_name,
    last_name,
    department,
    salary,
    ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS row_num
FROM
    employees
QUALIFY row_num = 1;

┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐
│   employee_id   │    first_name    │     last_name    │    department    │      salary     │ row_num │
├─────────────────┼──────────────────┼──────────────────┼──────────────────┼─────────────────┼─────────┤
│               2 │ Jane             │ Smith            │ HR               │           85000 │       1 │
│               1 │ John             │ Doe              │ IT               │           90000 │       1 │
│               4 │ Sara             │ Williams         │ Sales            │           77000 │       1 │
└──────────────────────────────────────────────────────────────────────────────────────────────────────┘

-- {{{ .lake }}} 允许在 QUALIFY 子句中直接使用窗口函数，而无需在 SELECT 列表中显式命名它们。

SELECT
    employee_id,
    first_name,
    last_name,
    department,
    salary
FROM
    employees
QUALIFY ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) = 1;

┌────────────────────────────────────────────────────────────────────────────────────────────┐
│   employee_id   │    first_name    │     last_name    │    department    │      salary     │
├─────────────────┼──────────────────┼──────────────────┼──────────────────┼─────────────────┤
│               2 │ Jane             │ Smith            │ HR               │           85000 │
│               1 │ John             │ Doe              │ IT               │           90000 │
│               4 │ Sara             │ Williams         │ Sales            │           77000 │
└────────────────────────────────────────────────────────────────────────────────────────────┘
```