---
title: VALUES
summary: VALUES 子句通过显式定义数据行来创建内联表。这个临时表可以直接使用，也可以在其他 SQL 语句中使用。
---

# VALUES

`VALUES` 子句通过显式定义数据行来创建内联表。这个临时表可以直接使用，也可以在其他 SQL 语句中使用。

## 语法 {#syntax}

```sql
SELECT ...
FROM ( VALUES ( <expr> [ , <expr> [ , ... ] ] ) [ , ( ... ) ] ) [ [ AS ] <table_alias> [ ( <column_alias> [, ... ] ) ] ]
[ ... ]
```

**关键点：**

- 当 `VALUES` 子句用于 `FROM` 子句中时，必须用括号括起来：`FROM (VALUES ...)`
- 每组用括号括起来的表达式表示一行
- 列名会自动分配为 **col0**、**col1** 等（从 0 开始索引）
- 你可以使用表别名提供自定义列名

## 示例 {#examples}

### 基本用法 {#basic-usage}

```sql
-- Direct usage with automatic column names (col0, col1)
VALUES ('Toronto', 2731571), ('Vancouver', 631486), ('Montreal', 1704694);

col0     |col1   |
---------+-------+
Toronto  |2731571|
Vancouver| 631486|
Montreal |1704694|

-- With ORDER BY
VALUES ('Toronto', 2731571), ('Vancouver', 631486), ('Montreal', 1704694) ORDER BY col1;

col0     |col1   |
---------+-------+
Vancouver| 631486|
Montreal |1704694|
Toronto  |2731571|
```

### 在 SELECT 语句中使用 {#in-select-statements}

```sql
-- Select specific column - note the parentheses around VALUES
SELECT col1
FROM (VALUES ('Toronto', 2731571), ('Vancouver', 631486), ('Montreal', 1704694));

-- Custom column names - VALUES must be enclosed in parentheses
SELECT * FROM (
    VALUES ('Toronto', 2731571),
           ('Vancouver', 631486),
           ('Montreal', 1704694)
) AS CityPopulation(City, Population);

-- With column aliases and sorting
SELECT col0 AS City, col1 AS Population
FROM (VALUES ('Toronto', 2731571), ('Vancouver', 631486), ('Montreal', 1704694))
ORDER BY col1 DESC
LIMIT 1;
```

### 与公共表表达式（CTE）一起使用 {#with-common-table-expressions-cte}

```sql
WITH citypopulation(city, population) AS (
    VALUES ('Toronto', 2731571),
           ('Vancouver', 631486),
           ('Montreal', 1704694)
)
SELECT city, population FROM citypopulation;
```

> **重要：**
>
> 当在 `FROM` 子句或 CTE 中使用 `VALUES` 时，必须将其用括号括起来：`FROM (VALUES ...)` 或 `AS (VALUES ...)`。这是必需的语法。