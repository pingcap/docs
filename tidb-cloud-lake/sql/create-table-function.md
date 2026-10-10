---
title: CREATE TABLE FUNCTION
summary: SQL クエリをテーブル関数としてカプセル化する表形式の SQL UDF（UDTF）を作成します。テーブル関数は SQL で記述され、外部言語は使用しません。
---

# CREATE TABLE FUNCTION

SQL クエリをテーブル関数としてカプセル化する表形式の SQL UDF（UDTF）を作成します。テーブル関数は SQL で記述され、外部言語は使用しません。

## サポートされる言語 {#supported-languages}

- SQL クエリのみ（外部ランタイムは使用不可）

## 構文 {#syntax}

```sql
CREATE [ OR REPLACE ] FUNCTION [ IF NOT EXISTS ] <function_name>
    ( [<parameter_list>] )
    RETURNS TABLE ( <column_definition_list> )
    AS $$ <sql_statement> $$
```

説明:

- `<parameter_list>`: 省略可能な、入力パラメータとその型のカンマ区切りリスト（例: `x INT, name VARCHAR`）
- `<column_definition_list>`: 関数が返すカラム名とその型のカンマ区切りリスト
- `<sql_statement>`: 関数ロジックを定義する SQL クエリ

## 統一された関数構文 {#unified-function-syntax}

{{{ .lake }}} は、スカラー関数とテーブル関数の両方で統一された `$$` 構文を使用します。

| 関数タイプ | 戻り値 | 使用方法 |
|---------------|---------|-------|
| **スカラー関数** | 単一の値 | `RETURNS <type>` + `AS $$ <expression> $$` |
| **テーブル関数** | 結果セット | `RETURNS TABLE(...)` + `AS $$ <query> $$` |

この一貫性により、関数タイプの理解や切り替えが容易になります。

## 例 {#examples}

### 基本的なテーブル関数 {#basic-table-function}

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

### パラメータ付きテーブル関数 {#parameterized-table-function}

```sql
-- Create a table function that filters employees by department
CREATE OR REPLACE FUNCTION get_employees_by_dept(dept_name VARCHAR)
RETURNS TABLE (id INT, name VARCHAR(100), department VARCHAR(100), salary DECIMAL(10,2))
AS $$ SELECT id, name, department, salary FROM employees WHERE department = dept_name $$;

-- Use the parameterized table function
SELECT * FROM get_employees_by_dept('Engineering');
```

### 複雑なテーブル関数 {#complex-table-function}

```sql
-- Create a table function that aggregates data
CREATE OR REPLACE FUNCTION get_department_stats()
RETURNS TABLE (department VARCHAR(100), employee_count INT, avg_salary DECIMAL(10,2))
AS $$ SELECT department, COUNT(*) as employee_count, AVG(salary) as avg_salary FROM employees GROUP BY department $$;

-- Use the complex table function
SELECT * FROM get_department_stats();
```