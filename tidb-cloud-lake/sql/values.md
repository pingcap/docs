---
title: VALUES
summary: VALUES 句は、データの行を明示的に定義することでインラインテーブルを作成します。この一時テーブルは、直接使用することも、他の SQL 文の中で使用することもできます。
---

# VALUES

VALUES 句は、データの行を明示的に定義することでインラインテーブルを作成します。この一時テーブルは、直接使用することも、他の SQL 文の中で使用することもできます。

## 構文 {#syntax}

```sql
SELECT ...
FROM ( VALUES ( <expr> [ , <expr> [ , ... ] ] ) [ , ( ... ) ] ) [ [ AS ] <table_alias> [ ( <column_alias> [, ... ] ) ] ]
[ ... ]
```

**主なポイント:**

- VALUES 句を `FROM` 句で使用する場合は、`FROM (VALUES ...)` のように必ず括弧で囲む必要があります
- 括弧で囲まれた各式のグループは 1 行を表します
- カラム名は **col0**、**col1** のように自動的に割り当てられます（0 始まりのインデックス）
- テーブルエイリアスを使用してカスタムのカラム名を指定できます

## 例 {#examples}

### 基本的な使い方 {#basic-usage}

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

### SELECT 文での使用 {#in-select-statements}

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

### Common Table Expressions (CTE) での使用 {#with-common-table-expressions-cte}

```sql
WITH citypopulation(city, population) AS (
    VALUES ('Toronto', 2731571),
           ('Vancouver', 631486),
           ('Montreal', 1704694)
)
SELECT city, population FROM citypopulation;
```

> **Important:**
>
> `VALUES` を `FROM` 句または CTE で使用する場合は、`FROM (VALUES ...)` または `AS (VALUES ...)` のように必ず括弧で囲む必要があります。これは必須の構文です。