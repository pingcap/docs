---
title: DROP FUNCTION
summary: 删除用户定义函数。适用于所有函数类型：Scalar SQL、Tabular SQL 和 Embedded functions。
---

# DROP FUNCTION

删除用户定义函数。适用于所有函数类型：Scalar SQL、Tabular SQL 和 Embedded functions。

## 语法 {#syntax}

```sql
DROP FUNCTION [ IF EXISTS ] <function_name>
```

## 示例 {#examples}

### 删除 Scalar SQL 函数 {#dropping-scalar-sql-function}

```sql
-- Create a scalar function
CREATE FUNCTION calculate_bmi(weight FLOAT, height FLOAT)
RETURNS FLOAT
AS $$ weight / (height * height) $$;

-- Drop the function
DROP FUNCTION calculate_bmi;
```

### 删除 Tabular SQL 函数 {#dropping-tabular-sql-function}

```sql
-- Create a table function
CREATE FUNCTION get_employees_by_dept(dept_name VARCHAR)
RETURNS TABLE (id INT, name VARCHAR, department VARCHAR)
AS $$ SELECT id, name, department FROM employees WHERE department = dept_name $$;

-- Drop the function
DROP FUNCTION get_employees_by_dept;
```

### 删除 Embedded 函数 {#dropping-embedded-function}

```sql
-- Create a Python function
CREATE FUNCTION custom_hash(input_str VARCHAR)
RETURNS VARCHAR
LANGUAGE python
HANDLER = 'hash_func'
AS $$
import hashlib
def hash_func(s):
    return hashlib.md5(s.encode()).hexdigest()
$$;

-- Drop the function
DROP FUNCTION custom_hash;
```

### 使用 IF EXISTS {#using-if-exists}

```sql
-- Safe drop - won't error if function doesn't exist
DROP FUNCTION IF EXISTS non_existent_function;

-- This will succeed without error even if the function doesn't exist
```