---
title: DROP FUNCTION
summary: ユーザー定義関数を削除します。Scalar SQL、Tabular SQL、Embedded 関数のすべての関数タイプで動作します。
---

# DROP FUNCTION

ユーザー定義関数を削除します。対応する関数タイプは、Scalar SQL、Tabular SQL、Embedded 関数です。

## 構文 {#syntax}

```sql
DROP FUNCTION [ IF EXISTS ] <function_name>
```

## 例 {#examples}

### Scalar SQL 関数の削除 {#dropping-scalar-sql-function}

```sql
-- Create a scalar function
CREATE FUNCTION calculate_bmi(weight FLOAT, height FLOAT)
RETURNS FLOAT
AS $$ weight / (height * height) $$;

-- Drop the function
DROP FUNCTION calculate_bmi;
```

### Tabular SQL 関数の削除 {#dropping-tabular-sql-function}

```sql
-- Create a table function
CREATE FUNCTION get_employees_by_dept(dept_name VARCHAR)
RETURNS TABLE (id INT, name VARCHAR, department VARCHAR)
AS $$ SELECT id, name, department FROM employees WHERE department = dept_name $$;

-- Drop the function
DROP FUNCTION get_employees_by_dept;
```

### Embedded 関数の削除 {#dropping-embedded-function}

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

### IF EXISTS の使用 {#using-if-exists}

```sql
-- Safe drop - won't error if function doesn't exist
DROP FUNCTION IF EXISTS non_existent_function;

-- This will succeed without error even if the function doesn't exist
```