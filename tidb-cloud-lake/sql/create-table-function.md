---
title: CREATE TABLE FUNCTION
summary: 创建表格 SQL UDF（UDTF），将 SQL 查询封装为表函数。表函数使用 SQL 编写；不涉及外部语言。
---

# CREATE TABLE FUNCTION

创建表格 SQL UDF（UDTF），将 SQL 查询封装为表函数。表函数使用 SQL 编写；不涉及外部语言。

## 支持的语言 {#supported-languages}

- 仅支持 SQL 查询（不支持外部运行时）

## 语法 {#syntax}

```sql
CREATE [ OR REPLACE ] FUNCTION [ IF NOT EXISTS ] <function_name>
    ( [<parameter_list>] )
    RETURNS TABLE ( <column_definition_list> )
    AS $$ <sql_statement> $$
```

其中：

- `<parameter_list>`：可选的输入参数列表，参数之间以逗号分隔，并带有各自的类型（例如：`x INT, name VARCHAR`）
- `<column_definition_list>`：函数返回的列名及其类型列表，列之间以逗号分隔
- `<sql_statement>`：定义函数逻辑的 SQL 查询

## 统一函数语法 {#unified-function-syntax}

{{{ .lake }}} 对标量函数和表函数统一使用 `$$` 语法：

| 函数类型 | 返回值 | 用法 |
|---------------|---------|-------|
| **标量函数** | 单个值 | `RETURNS <type>` + `AS $$ <expression> $$` |
| **表函数** | 结果集 | `RETURNS TABLE(...)` + `AS $$ <query> $$` |

这种一致性使你能够更容易理解不同函数类型，并在它们之间切换。

## 示例 {#examples}

### 基本表函数 {#basic-table-function}

```sql
-- Create a sample table
CREATE OR REPLACE TABLE employees (
    id INT,
    name VARCHAR(100),
    department VARCHAR(100),
    salary DECIMAL(10,2)
);

INSERT INTO employees VALUES
    (1, 'John', 'Engineering', 75000),
    (2, 'Jane', 'Marketing', 65000),
    (3, 'Bob', 'Engineering', 80000),
    (4, 'Alice', 'Marketing', 70000);

-- Create a simple table function to get all employees
CREATE OR REPLACE FUNCTION get_all_employees()
RETURNS TABLE (id INT, name VARCHAR(100), department VARCHAR(100), salary DECIMAL(10,2))
AS $$ SELECT id, name, department, salary FROM employees $$;

-- Test the function
SELECT * FROM get_all_employees();
```

### 带参数的表函数 {#parameterized-table-function}

```sql
-- Create a table function that filters employees by department
CREATE OR REPLACE FUNCTION get_employees_by_dept(dept_name VARCHAR)
RETURNS TABLE (id INT, name VARCHAR(100), department VARCHAR(100), salary DECIMAL(10,2))
AS $$ SELECT id, name, department, salary FROM employees WHERE department = dept_name $$;

-- Use the parameterized table function
SELECT * FROM get_employees_by_dept('Engineering');
```

### 复杂表函数 {#complex-table-function}

```sql
-- Create a table function that aggregates data
CREATE OR REPLACE FUNCTION get_department_stats()
RETURNS TABLE (department VARCHAR(100), employee_count INT, avg_salary DECIMAL(10,2))
AS $$ SELECT department, COUNT(*) as employee_count, AVG(salary) as avg_salary FROM employees GROUP BY department $$;

-- Use the complex table function
SELECT * FROM get_department_stats();
```