---
title: ALTER FUNCTION
summary: 修改用户定义函数。支持所有函数类型：Scalar SQL、Tabular SQL 和 Embedded functions。
---

# ALTER FUNCTION

修改用户定义函数。支持所有函数类型：Scalar SQL、Tabular SQL 和 Embedded functions。

## 语法 {#syntax}

### 对于 Scalar SQL Functions {#for-scalar-sql-functions}

```sql
ALTER FUNCTION [ IF EXISTS ] <function_name>
    ( [<parameter_list>] )
    RETURNS <return_type>
    AS $$ <expression> $$
    [ DESC='<description>' ]
```

### 对于 Tabular SQL Functions {#for-tabular-sql-functions}

```sql
ALTER FUNCTION [ IF EXISTS ] <function_name>
    ( [<parameter_list>] )
    RETURNS TABLE ( <column_definition_list> )
    AS $$ <sql_statement> $$
    [ DESC='<description>' ]
```

### 对于 Embedded Functions {#for-embedded-functions}

```sql
ALTER FUNCTION [ IF EXISTS ] <function_name>
    ( [<parameter_list>] )
    RETURNS <return_type>
    LANGUAGE <language>
    [IMPORTS = ('<import_path>', ...)]
    [PACKAGES = ('<package_path>', ...)]
    HANDLER = '<handler_name>'
    AS $$ <function_code> $$
    [ DESC='<description>' ]
```

## 示例 {#examples}

### 修改 Scalar SQL Function {#altering-scalar-sql-function}

```sql
-- Create a scalar function
CREATE FUNCTION calculate_tax(income DECIMAL)
RETURNS DECIMAL
AS $$ income * 0.2 $$;

-- Modify the function to use progressive tax rate
ALTER FUNCTION calculate_tax(income DECIMAL)
RETURNS DECIMAL
AS $$
  CASE
    WHEN income <= 50000 THEN income * 0.15
    ELSE income * 0.25
  END
$$;
```

### 修改 Tabular SQL Function {#altering-tabular-sql-function}

```sql
-- Create a table function
CREATE FUNCTION get_employees()
RETURNS TABLE (id INT, name VARCHAR(100))
AS $$ SELECT id, name FROM employees $$;

-- Modify to include department and salary
ALTER FUNCTION get_employees()
RETURNS TABLE (id INT, name VARCHAR(100), department VARCHAR(100), salary DECIMAL)
AS $$ SELECT id, name, department, salary FROM employees $$;
```

### 修改 Embedded Function {#altering-embedded-function}

```sql
-- Create a Python function
CREATE FUNCTION simple_calc(x INT)
RETURNS INT
LANGUAGE python
HANDLER = 'calc'
AS $$
def calc(x):
    return x * 2
$$;

-- Modify to use a different calculation
ALTER FUNCTION simple_calc(x INT)
RETURNS INT
LANGUAGE python
HANDLER = 'calc'
AS $$
def calc(x):
    return x * 3 + 1
$$;
```