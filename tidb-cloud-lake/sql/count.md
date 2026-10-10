---
title: COUNT
summary: COUNT() 関数は、SELECT クエリによって返されるレコード数を返します。
---

# COUNT

COUNT() 関数は、SELECT クエリによって返されるレコード数を返します。

> **Note:**
>
> NULL 値はカウントされません。

## 構文 {#syntax}

```sql
COUNT(<expr>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `<expr>`  | 任意の式です。<br />カラム名、別の関数の結果、または数学演算を指定できます。<br />純粋な行数カウントを示すために `*` も使用できます。 |

## 戻り値の型 {#return-type}

整数です。

## 例 {#example}

**Create a Table and Insert Sample Data**

```sql
CREATE TABLE students (
  id INT,
  name VARCHAR,
  age INT,
  grade FLOAT NULL
);

INSERT INTO students (id, name, age, grade)
VALUES (1, 'John', 21, 85),
       (2, 'Emma', 22, NULL),
       (3, 'Alice', 23, 90),
       (4, 'Michael', 21, 88),
       (5, 'Sophie', 22, 92);

```

**Query Demo: Count Students with Valid Grades**

```sql
SELECT COUNT(grade) AS count_valid_grades
FROM students;
```

**結果**

```sql
| count_valid_grades |
|--------------------|
|          4         |
```