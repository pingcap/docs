---
title: DELETE
summary: 从表中删除一行或多行。
---

# DELETE

从表中删除一行或多行。

> **Tip:**
>
> {{{ .lake }}} 通过原子操作确保数据完整性。插入、修改、替换和删除要么全部成功，要么全部失败。

## 语法 {#syntax}

```sql
DELETE FROM <table_name> [AS <table_alias>]
[WHERE <condition>]
```

- `AS <table_alias>`：允许你为表设置别名，从而更方便地在查询中引用该表。这有助于简化并缩短 SQL 代码，尤其是在处理涉及多个表的复杂查询时。参见[使用 EXISTS / NOT EXISTS 子句和子查询删除](#deleting-with-subquery-using-exists--not-exists-clause)中的示例。

- DELETE 目前还不支持 USING 子句。如果你需要使用子查询来识别要删除的行，请直接将其包含在 WHERE 子句中。参见[基于子查询的删除](#example-2-subquery-based-deletions)中的示例。

## 示例 {#examples}

### 示例 1：直接删除行 {#example-1-direct-row-deletion}

本示例演示如何使用 DELETE 命令，直接从 `bookstore` 表中删除 ID 为 103 的图书记录。

```sql
-- Create a table and insert 5 book records
CREATE TABLE bookstore (
  book_id INT,
  book_name VARCHAR
);

INSERT INTO bookstore VALUES (101, 'After the death of Don Juan');
INSERT INTO bookstore VALUES (102, 'Grown ups');
INSERT INTO bookstore VALUES (103, 'The long answer');
INSERT INTO bookstore VALUES (104, 'Wartime friends');
INSERT INTO bookstore VALUES (105, 'Deconstructed');

-- Delete a book (Id: 103)
DELETE FROM bookstore WHERE book_id = 103;

-- Show all records after deletion
SELECT * FROM bookstore;

101|After the death of Don Juan
102|Grown ups
104|Wartime friends
105|Deconstructed
```

### 示例 2：基于子查询的删除 {#example-2-subquery-based-deletions}

当使用子查询来识别要删除的行时，可以使用[子查询运算符](/tidb-cloud-lake/sql/query-operators.md)和[比较运算符](/tidb-cloud-lake/sql/query-operators.md)来实现所需的删除操作。

本节中的示例基于以下两个表：

```sql
-- Create the 'employees' table
CREATE TABLE employees (
  id INT,
  name VARCHAR,
  department VARCHAR
);

-- Insert values into the 'employees' table
INSERT INTO employees VALUES (1, 'John', 'HR');
INSERT INTO employees VALUES (2, 'Mary', 'Sales');
INSERT INTO employees VALUES (3, 'David', 'IT');
INSERT INTO employees VALUES (4, 'Jessica', 'Finance');

-- Create the 'departments' table
CREATE TABLE departments (
  id INT,
  department VARCHAR
);

-- Insert values into the 'departments' table
INSERT INTO departments VALUES (1, 'Sales');
INSERT INTO departments VALUES (2, 'IT');
```

#### 使用 IN / NOT IN 子句和子查询删除 {#deleting-with-subquery-using-in-not-in-clause}

```sql
DELETE FROM EMPLOYEES
WHERE DEPARTMENT IN (
    SELECT DEPARTMENT
    FROM DEPARTMENTS
);
```

这会删除 `employees` 表中 `department` 与 `departments` 表中任一部门匹配的员工。在此情况下，将删除 ID 为 2 和 3 的员工。

#### 使用 EXISTS / NOT EXISTS 子句和子查询删除 {#deleting-with-subquery-using-exists-not-exists-clause}

```sql
DELETE FROM EMPLOYEES
WHERE EXISTS (
    SELECT *
    FROM DEPARTMENTS
    WHERE EMPLOYEES.DEPARTMENT = DEPARTMENTS.DEPARTMENT
);

-- Alternatively, you can delete employees using the alias 'e' for the 'EMPLOYEES' table and 'd' for the 'DEPARTMENTS' table when their department matches.
DELETE FROM EMPLOYEES AS e
WHERE EXISTS (
    SELECT *
    FROM DEPARTMENTS AS d
    WHERE e.DEPARTMENT = d.DEPARTMENT
);
```

这会删除所属部门存在于 `departments` 表中的员工。在此情况下，将删除 ID 为 2 和 3 的员工。

#### 使用 ALL 子句和子查询删除 {#deleting-with-subquery-using-all-clause}

```sql
DELETE FROM EMPLOYEES
WHERE DEPARTMENT = ALL (
    SELECT DEPARTMENT
    FROM DEPARTMENTS
);
```

这会删除 `department` 与 `departments` 表中所有部门都匹配的员工。在此情况下，不会删除任何员工。

#### 使用 ANY 子句和子查询删除 {#deleting-with-subquery-using-any-clause}

```sql
DELETE FROM EMPLOYEES
WHERE DEPARTMENT = ANY (
    SELECT DEPARTMENT
    FROM DEPARTMENTS
);
```

这会删除 `department` 与 `departments` 表中任一部门匹配的员工。在此情况下，将删除 ID 为 2 和 3 的员工。

#### 结合多个条件使用子查询删除 {#deleting-with-subquery-combining-multiple-conditions}

```sql
DELETE FROM EMPLOYEES
WHERE DEPARTMENT = ANY (
    SELECT DEPARTMENT
    FROM DEPARTMENTS
    WHERE EMPLOYEES.DEPARTMENT = DEPARTMENTS.DEPARTMENT
)
   OR ID > 2;
```

这会在以下任一条件满足时，从 `employees` 表中删除员工：`department` 列的值与 `departments` 表中 `department` 列的任一值匹配，或者 `id` 列的值大于 2。在此情况下，将删除 `id` 为 2、3 和 4 的行，因为 Mary 的部门是 `"Sales"`，该部门存在于 `departments` 表中，并且 ID 为 3 和 4 的行都大于 2。