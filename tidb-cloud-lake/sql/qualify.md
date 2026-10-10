---
title: QUALIFY
summary: QUALIFY は、ウィンドウ関数の結果をフィルタするために使用される句です。そのため、QUALIFY 句を正しく利用するには、SELECT リストまたは QUALIFY 句に少なくとも 1 つのウィンドウ関数が存在している必要があります（それぞれのケースについては Examples を参照してください）。言い換えると、QUALIFY はウィンドウ関数の計算後に評価されます。以下は、QUALIFY 文句を含むクエリの一般的な実行順序です。
---

# QUALIFY

QUALIFY は、ウィンドウ関数の結果をフィルタするために使用される句です。そのため、QUALIFY 句を正しく利用するには、SELECT リストまたは QUALIFY 句に少なくとも 1 つのウィンドウ関数が存在している必要があります（それぞれのケースについては [例](#examples) を参照してください）。言い換えると、QUALIFY はウィンドウ関数の計算後に評価されます。以下は、QUALIFY 文句を含むクエリの一般的な実行順序です。

1. FROM
2. WHERE
3. GROUP BY
4. HAVING
5. WINDOW FUNCTION
6. QUALIFY
7. DISTINCT
8. ORDER BY
9. LIMIT

## 構文 {#syntax}

```sql
QUALIFY <predicate>
```

## 例 {#examples}

この例では、ROW_NUMBER() を使用して、各部門内の従業員に対して給与の降順で連番を割り当てる方法を示します。QUALIFY 句を利用することで、各部門で最も給与の高い従業員のみを表示するように結果をフィルタします。

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

-- {{{ .lake }}} allows the direct use of window functions in the QUALIFY clause without requiring them to be explicitly named in the SELECT list.

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