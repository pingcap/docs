---
title: COUNT
summary: COUNT() 函数返回 SELECT 查询返回的记录数。
---

# COUNT

COUNT() 函数返回 SELECT 查询返回的记录数。

> **注意：**
>
> 不会统计 NULL 值。

## 语法 {#syntax}

```sql
COUNT(<expr>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|-----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `<expr>`  | 任意表达式。<br />可以是列名、另一个函数的结果，或数学运算。<br />也允许使用 `*`，表示仅统计行数。 |

## 返回类型 {#return-type}

整数型。

## 示例 {#example}

**创建表并插入示例数据**

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

**查询示例：统计具有有效成绩的学生数量**

```sql
SELECT COUNT(grade) AS count_valid_grades
FROM students;
```

**结果**

```sql
| count_valid_grades |
|--------------------|
|          4         |
```