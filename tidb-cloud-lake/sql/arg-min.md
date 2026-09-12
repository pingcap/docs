---
title: ARG_MIN
summary: 计算最小 `val` 值对应的 `arg` 值。如果最小 `val` 值对应多个不同的 `arg` 值，则返回遇到的第一个值。
---

# ARG_MIN

计算最小 `val` 值对应的 `arg` 值。如果最小 `val` 值对应多个不同的 `arg` 值，则返回遇到的第一个值。

## 语法 {#syntax}

```sql
ARG_MIN(<arg>, <val>)
```

## 参数 {#arguments}

| 参数 | 描述                                                                                       |
| --------- | ------------------------------------------------------------------------------------------------- |
| `<arg>`   | [{{{ .lake }}} 支持的任意数据类型](/tidb-cloud-lake/sql/data-types.md)的参数 |
| `<val>`   | [{{{ .lake }}} 支持的任意数据类型](/tidb-cloud-lake/sql/data-types.md)的值    |

## 返回类型 {#return-type}

与最小 `val` 值对应的 `arg` 值。

与 `arg` 类型匹配。

## 示例 {#example}

创建一个包含 `id`、`name` 和 `score` 列的 `students` 表，并插入一些数据：

```sql
CREATE TABLE students (
  id INT,
  name VARCHAR,
  score INT
);

INSERT INTO students (id, name, score) VALUES
  (1, 'Alice', 80),
  (2, 'Bob', 75),
  (3, 'Charlie', 90),
  (4, 'Dave', 80);
```

现在，可以使用 ARG_MIN 查找分数最低的学生姓名：

```sql
SELECT ARG_MIN(name, score) AS student_name
FROM students;
```

结果：

```sql
| student_name |
|--------------|
| Bob      |
```