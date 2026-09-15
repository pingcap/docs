---
title: TOP
summary: 限制查询返回的最大行数。
---

# TOP

限制查询返回的最大行数。

另请参阅：[LIMIT 子句](/tidb-cloud-lake/sql/select.md#limit-clause)

## 语法 {#syntax}

```sql
SELECT
    [ TOP <n> ] <column1>, <column2>, ...
FROM ...
[ ORDER BY ... ]
```

| 参数 | 描述 |
|-----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| n         | 表示结果中返回行数的最大限制，并且必须是非负整数型。 |

- `TOP` 和 `LIMIT` 都是用于限制查询返回行数的等价关键字，但不能在同一条查询中同时使用。
- 如果使用 `TOP` 时未指定 `ORDER BY` 子句，则查询在选择前几行时缺乏有意义的顺序，因此可能导致结果不一致或不符合预期。

## 示例 {#examples}

以下示例按分数降序返回前 3 名学生：

```sql
CREATE TABLE Students (
    ID INT,
    Name VARCHAR(50),
    Score INT
);

INSERT INTO Students (ID, Name, Score) VALUES
(1, 'John', 85),
(2, 'Emily', 92),
(3, 'Michael', 78),
(4, 'Sophia', 95),
(5, 'William', 88),
(6, 'Emma', 90),
(7, 'James', 82),
(8, 'Olivia', 96),
(9, 'Alexander', 75),
(10, 'Ava', 96);

SELECT TOP 3 * FROM Students ORDER BY Score DESC;

┌──────────────────────────────────────────────────────┐
│        id       │       name       │      score      │
├─────────────────┼──────────────────┼─────────────────┤
│               8 │ Olivia           │              96 │
│              10 │ Ava              │              96 │
│               4 │ Sophia           │              95 │
└──────────────────────────────────────────────────────┘
```

上述查询等价于：

```sql
SELECT * FROM Students ORDER BY Score DESC LIMIT 3;

┌──────────────────────────────────────────────────────┐
│        id       │       name       │      score      │
├─────────────────┼──────────────────┼─────────────────┤
│               8 │ Olivia           │              96 │
│              10 │ Ava              │              96 │
│               4 │ Sophia           │              95 │
└──────────────────────────────────────────────────────┘
```

以下示例仅返回前 3 名学生的姓名和分数：

```sql
SELECT TOP 3 name, score FROM Students ORDER BY Score DESC;

┌────────────────────────────────────┐
│       name       │      score      │
├──────────────────┼─────────────────┤
│ Olivia           │              96 │
│ Ava              │              96 │
│ Sophia           │              95 │
└────────────────────────────────────┘
```

在同一条查询中同时使用 `TOP` 和 `LIMIT` 会导致报错：

```sql
SELECT TOP 3 name, score FROM Students ORDER BY Score DESC LIMIT 3;
error: APIError: ResponseError with 1065: Duplicate LIMIT: TopN and Limit cannot be used together
```