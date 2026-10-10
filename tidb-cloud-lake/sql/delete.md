---
title: DELETE
summary: テーブルから1行以上を削除します。
---

# DELETE

テーブルから1行以上を削除します。

> **Tip:**
>
> {{{ .lake }}} は、アトミックな操作によってデータ整合性を保証します。insert、update、replace、delete は、完全に成功するか、完全に失敗するかのいずれかです。

## 構文 {#syntax}

```sql
DELETE FROM <table_name> [AS <table_alias>]
[WHERE <condition>]
```

- `AS <table_alias>`: テーブルにエイリアスを設定できるため、クエリ内でそのテーブルを参照しやすくなります。これは、特に複数のテーブルを含む複雑なクエリを扱う場合に、SQL コードの簡略化と短縮に役立ちます。例については、[EXISTS / NOT EXISTS 句を使用したサブクエリによる削除](#deleting-with-subquery-using-exists--not-exists-clause) を参照してください。

- DELETE はまだ USING 句をサポートしていません。削除する行を特定するためにサブクエリを使用する必要がある場合は、それを WHERE 句内に直接含めてください。例については、[サブクエリベースの削除](#example-2-subquery-based-deletions) を参照してください。

## 例 {#examples}

### 例 1: 行の直接削除 {#example-1-direct-row-deletion}

この例では、DELETE コマンドを使用して、"bookstore" テーブルから ID が 103 の書籍レコードを直接削除する方法を示します。

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

### 例 2: サブクエリベースの削除 {#example-2-subquery-based-deletions}

削除対象の行を特定するためにサブクエリを使用する場合は、[サブクエリ演算子](/tidb-cloud-lake/sql/query-operators.md) および [比較演算子](/tidb-cloud-lake/sql/query-operators.md) を使用して、目的の削除を実現できます。

このセクションの例は、次の 2 つのテーブルに基づいています。

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

#### IN / NOT IN 句を使用したサブクエリによる削除 {#deleting-with-subquery-using-in-not-in-clause}

```sql
DELETE FROM EMPLOYEES
WHERE DEPARTMENT IN (
    SELECT DEPARTMENT
    FROM DEPARTMENTS
);
```

これは、departments テーブル内のいずれかの department と一致する department を持つ従業員を削除します。この場合、ID が 2 と 3 の従業員が削除されます。

#### EXISTS / NOT EXISTS 句を使用したサブクエリによる削除 {#deleting-with-subquery-using-exists-not-exists-clause}

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

これは、departments テーブルに存在する department に所属する従業員を削除します。この場合、ID が 2 と 3 の従業員が削除されます。

#### ALL 句を使用したサブクエリによる削除 {#deleting-with-subquery-using-all-clause}

```sql
DELETE FROM EMPLOYEES
WHERE DEPARTMENT = ALL (
    SELECT DEPARTMENT
    FROM DEPARTMENTS
);
```

これは、department テーブル内のすべての department と一致する department を持つ従業員を削除します。この場合、削除される従業員はいません。

#### ANY 句を使用したサブクエリによる削除 {#deleting-with-subquery-using-any-clause}

```sql
DELETE FROM EMPLOYEES
WHERE DEPARTMENT = ANY (
    SELECT DEPARTMENT
    FROM DEPARTMENTS
);
```

これは、departments テーブル内のいずれかの department と一致する department を持つ従業員を削除します。この場合、ID が 2 と 3 の従業員が削除されます。

#### 複数条件を組み合わせたサブクエリによる削除 {#deleting-with-subquery-combining-multiple-conditions}

```sql
DELETE FROM EMPLOYEES
WHERE DEPARTMENT = ANY (
    SELECT DEPARTMENT
    FROM DEPARTMENTS
    WHERE EMPLOYEES.DEPARTMENT = DEPARTMENTS.DEPARTMENT
)
   OR ID > 2;
```

これは、employees テーブルにおいて、department カラムの値が departments テーブルの department カラム内のいずれかの値と一致する場合、または id カラムの値が 2 より大きい場合に、従業員を削除します。この場合、Mary の department は departments テーブルに存在する "Sales" であり、さらに ID 3 と 4 は 2 より大きいため、id が 2、3、4 の行が削除されます。