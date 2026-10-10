---
title: DESC VIEW
summary: ビューのカラム一覧を返します。
---

# DESC VIEW

ビューのカラム一覧を返します。

## 構文 {#syntax}

```sql
DESC[RIBE] VIEW [<database_name>.]<view_name>
```

## 出力 {#output}

このコマンドは、次のカラムを持つテーブルを出力します。

| カラム  | 説明                                                                                                             |
|---------|------------------------------------------------------------------------------------------------------------------|
| Field   | ビュー内のカラム名です。                                                                                         |
| Type    | カラムのデータ型です。                                                                                           |
| Null    | カラムが NULL 値を許可するかどうかを示します（NULL を許可する場合は YES、許可しない場合は NO）。                |
| Default | カラムのデフォルト値を指定します。                                                                               |
| Extra   | 計算カラムであるかどうかや、その他の特別な属性など、カラムに関する追加情報を提供します。                        |

## 例 {#examples}

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