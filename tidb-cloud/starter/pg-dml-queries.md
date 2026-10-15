---
title: PostgreSQL DML 和查询
summary: 了解 PostgreSQL 兼容的 TiDB Cloud Starter 支持的 PostgreSQL 数据操纵和查询功能。
---

# PostgreSQL DML 和查询

PostgreSQL 兼容的 {{{ .starter }}} 支持常见的 PostgreSQL 数据操纵语言（DML）语句和查询功能，包括 `INSERT`、`UPDATE`、`DELETE`、`RETURNING`、upsert、连接、聚合、窗口函数、公用表表达式（CTEs）、子查询以及集合操作。

## 准备示例表 {#prepare-sample-tables}

本页中的一些示例会使用示例表。在运行这些示例之前，请先在测试数据库中创建以下表。

本页中的表定义与其他示例中的定义不同。如果你的测试数据库中已经包含了下方所示名称的表，请为本页使用单独的测试数据库。

```sql
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT CONSTRAINT users_email_key UNIQUE,
    active BOOLEAN NOT NULL DEFAULT true
);

CREATE TABLE archived_users (
    id BIGINT PRIMARY KEY,
    name TEXT,
    email TEXT
);

CREATE TABLE employees (
    id BIGSERIAL PRIMARY KEY,
    name TEXT,
    department TEXT,
    salary NUMERIC
);

CREATE TABLE customers (
    id BIGSERIAL PRIMARY KEY,
    email TEXT
);

CREATE TABLE leads (
    id BIGSERIAL PRIMARY KEY,
    email TEXT
);

CREATE TABLE categories (
    id BIGINT PRIMARY KEY,
    parent_id BIGINT,
    name TEXT
);

CREATE TABLE orders (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id)
);
```

要填充聚合、窗口函数、递归 CTE 和集合操作示例中使用的示例表，请运行：

```sql
INSERT INTO employees (name, department, salary) VALUES
    ('Alice', 'Engineering', 90000),
    ('Bob', 'Engineering', 85000),
    ('Charlie', 'Engineering', 95000),
    ('David', 'Engineering', 88000),
    ('Emma', 'Engineering', 92000),
    ('Frank', 'Engineering', 87000),
    ('Grace', 'Sales', 75000);

INSERT INTO categories (id, parent_id, name) VALUES
    (1, NULL, 'Electronics'),
    (2, 1, 'Computers'),
    (3, 2, 'Laptops');

INSERT INTO customers (email) VALUES
    ('alice@example.com'),
    ('bob@example.com');

INSERT INTO leads (email) VALUES
    ('charlie@example.com'),
    ('david@example.com');
```

在执行本页中的示例之前，请先运行一次这些初始化语句。`users` 表初始为空，因此 `INSERT` 示例可以在不发生冲突的情况下向其中填充数据。

根据前面示例插入或修改的数据不同，某些查询可能不会返回任何行。

## 插入数据 {#insert-data}

插入单行：

```sql
INSERT INTO users (name, email)
VALUES ('Alice', 'alice@example.com');
```

插入多行：

```sql
INSERT INTO users (name, email)
VALUES
    ('Charlie', 'charlie@example.com'),
    ('Bob', 'bob@example.com');
```

通过查询插入行：

```sql
INSERT INTO archived_users (id, name, email)
SELECT id, name, email
FROM users
WHERE active = false;
```

### 使用 `RETURNING` {#use-returning}

`INSERT`、`UPDATE` 和 `DELETE` 都支持 `RETURNING`。

例如：

```sql
INSERT INTO users (name, email)
VALUES ('Carol', 'carol@example.com')
RETURNING id, name, email;
```

## 使用 `ON CONFLICT` 进行 upsert {#upsert-with-on-conflict}

使用 `INSERT ... ON CONFLICT` 处理唯一键冲突。

跳过发生冲突的行：

```sql
INSERT INTO users (email, name)
VALUES ('alice@example.com', 'Alice')
ON CONFLICT (email) DO NOTHING;
```

发生冲突时修改现有行：

```sql
INSERT INTO users (email, name)
VALUES ('alice@example.com', 'Alice Updated')
ON CONFLICT (email)
DO UPDATE SET name = excluded.name;
```

使用命名约束作为冲突目标：

```sql
INSERT INTO users (email, name)
VALUES ('alice@example.com', 'Alice')
ON CONFLICT ON CONSTRAINT users_email_key
DO UPDATE SET name = excluded.name;
```

`excluded` 伪表表示建议插入的那一行。

## 修改数据 {#update-data}

在 PostgreSQL 兼容的 {{{ .starter }}} 中，`UPDATE` 要求目标表必须具有主键。与 PostgreSQL 不同，即使 `WHERE` 条件没有匹配到任何行，修改没有主键的表也会失败，并返回 `ERROR: No PK`。

如果一个表已经包含数据但没有主键，则不支持直接为这个已填充数据的表添加主键。要启用修改操作，请先将现有行备份或复制到另一张表中，从原表中删除这些行，添加主键，然后再重新插入数据。在恢复这些行之前，请确保主键值唯一且非空值。

修改匹配条件的行：

```sql
UPDATE users
SET active = true
WHERE name = 'Charlie';
```

返回已修改的行：

```sql
UPDATE users
SET active = true
WHERE name = 'Charlie'
RETURNING *;
```

## 删除数据 {#delete-data}

删除匹配条件的行：

```sql
DELETE FROM users
WHERE name = 'Bob';
```

返回已删除的行：

```sql
DELETE FROM users
WHERE name = 'Charlie'
RETURNING *;
```

## 外键引用操作 {#foreign-key-referential-actions}

外键支持以下 `ON DELETE` 和 `ON UPDATE` 操作：

- `CASCADE`
- `SET NULL`
- `SET DEFAULT`
- `RESTRICT`
- `NO ACTION`

例如：

```sql
CREATE TABLE orders_with_cascade (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE
);
```

与 PostgreSQL 兼容的 {{{ .starter }}} 默认使用 `MATCH SIMPLE` 语义。如果任一引用列为 `NULL`，则会跳过该行的外键检查。

## 查询数据 {#query-data}

使用 `SELECT` 查询数据：

```sql
SELECT id, name, email
FROM users
WHERE active = true
ORDER BY name
LIMIT 10;
```

## 连接 {#joins}

支持以下连接及相关查询模式：

| 连接或查询模式 | 是否支持 |
| --- | --- |
| `INNER JOIN` | 是 |
| `LEFT [OUTER] JOIN` | 是 |
| `RIGHT [OUTER] JOIN` | 是 |
| `FULL [OUTER] JOIN` | 是 |
| `CROSS JOIN` | 是 |
| `LATERAL` 子查询 | 是 |
| 使用 `EXISTS` 的 Semi join | 是 |
| 使用 `NOT EXISTS` 的 Anti join | 是 |

例如：

```sql
SELECT
    u.id,
    u.name,
    o.id AS order_id
FROM users AS u
LEFT JOIN orders AS o
    ON o.user_id = u.id;
```

### LATERAL 连接 {#lateral-joins}

`LATERAL` 子查询可以引用前面 `FROM` 项中的列。

例如：

```sql
SELECT
    u.id,
    u.name,
    recent.order_id
FROM users AS u
LEFT JOIN LATERAL (
    SELECT o.id AS order_id
    FROM orders AS o
    WHERE o.user_id = u.id
    ORDER BY o.id DESC
    LIMIT 1
) AS recent ON true;
```

## 聚合 {#aggregation}

支持以下聚合功能：

- `GROUP BY`
- `HAVING`
- `COUNT(DISTINCT ...)`
- 聚合 `FILTER`
- `GROUPING()`

例如：

```sql
SELECT
    department,
    count(*) AS employee_count,
    avg(salary) AS average_salary
FROM employees
GROUP BY department
HAVING count(*) > 5;
```

使用 `FILTER` 为聚合应用条件：

```sql
SELECT
    count(*) AS total,
    count(*) FILTER (WHERE active = true) AS active_count
FROM users;
```

## 窗口函数 {#window-functions}

支持以下排名窗口函数：

- `ROW_NUMBER`
- `RANK`
- `DENSE_RANK`
- `NTILE`
- `PERCENT_RANK`
- `CUME_DIST`

支持以下值访问函数：

- `LAG`
- `LEAD`
- `FIRST_VALUE`
- `LAST_VALUE`
- `NTH_VALUE`

例如：

```sql
SELECT
    name,
    department,
    salary,
    ROW_NUMBER() OVER (
        PARTITION BY department
        ORDER BY salary DESC
    ) AS rank
FROM employees;
```

以下聚合函数也可以用作窗口函数：

- `SUM`
- `AVG`
- `COUNT`
- `MIN`
- `MAX`
- `STRING_AGG`

例如：

```sql
SELECT
    department,
    name,
    salary,
    AVG(salary) OVER (PARTITION BY department) AS department_average
FROM employees;
```

## 公用表表达式 {#common-table-expressions}

支持非递归 CTE：

```sql
WITH active_users AS (
    SELECT *
    FROM users
    WHERE active = true
)
SELECT *
FROM active_users;
```

也支持递归 CTE：

```sql
WITH RECURSIVE category_tree AS (
    SELECT id, parent_id, name, 1 AS depth
    FROM categories
    WHERE parent_id IS NULL

    UNION ALL

    SELECT
        c.id,
        c.parent_id,
        c.name,
        t.depth + 1
    FROM categories AS c
    JOIN category_tree AS t
        ON c.parent_id = t.id
)
SELECT *
FROM category_tree;
```

递归 CTE 最多限制为 1,000 次迭代。

在同一个 `WITH` 列表中，请为每个 CTE 定义使用唯一名称。关于递归 CTE 的限制，请参见[PostgreSQL 限制与约束](/tidb-cloud/starter/pg-limits-constraints.md)。

### 修改数据的 CTE {#data-modifying-ctes}

支持通过 PostgreSQL wire 协议使用带有 `RETURNING` 的 `INSERT`、`UPDATE` 或 `DELETE` 的修改数据 CTE。

例如：

```sql
WITH inserted AS (
    INSERT INTO users (name, email)
    VALUES ('Dave', 'dave@example.com')
    RETURNING id
)
SELECT *
FROM inserted;
```

## 子查询 {#subqueries}

支持以下子查询形式：

- 标量子查询
- `EXISTS` 和 `NOT EXISTS`
- 带子查询的 `IN` 和 `NOT IN`
- 带子查询的 `ANY` 和 `ALL`
- 数组子查询
- 相关子查询

例如：

```sql
SELECT u.id, u.name
FROM users AS u
WHERE EXISTS (
    SELECT 1
    FROM orders AS o
    WHERE o.user_id = u.id
);
```

## 集合操作 {#set-operations}

支持以下集合操作：

| 操作 | 是否支持 |
| --- | --- |
| `UNION` | 是 |
| `UNION ALL` | 是 |
| `INTERSECT` | 是 |
| `INTERSECT ALL` | 是 |
| `EXCEPT` | 是 |
| `EXCEPT ALL` | 是 |

例如：

```sql
SELECT email
FROM customers

UNION

SELECT email
FROM leads;
```

## DISTINCT 和排序 {#distinct-and-ordering}

支持 `SELECT DISTINCT` 和 `SELECT DISTINCT ON (...)`：

```sql
SELECT DISTINCT department
FROM employees;
```

```sql
SELECT DISTINCT ON (department)
    department,
    name,
    salary
FROM employees
ORDER BY department, salary DESC;
```

排序支持 `ASC`、`DESC`、`NULLS FIRST` 和 `NULLS LAST`：

```sql
SELECT id, name
FROM users
ORDER BY name ASC NULLS LAST;
```

## Limit 和 offset {#limit-and-offset}

使用 `LIMIT` 和 `OFFSET` 对查询结果进行分页：

```sql
SELECT id, name
FROM users
ORDER BY id
LIMIT 20
OFFSET 40;
```

## 解释查询 {#explain-a-query}

支持 `EXPLAIN` 和 `EXPLAIN ANALYZE`：

```sql
EXPLAIN
SELECT *
FROM users
WHERE email = 'alice@example.com';
```

```sql
EXPLAIN ANALYZE
SELECT *
FROM users
WHERE email = 'alice@example.com';
```

## 预处理语句 {#prepared-statements}

使用 `PREPARE`、`EXECUTE` 和 `DEALLOCATE` 来处理 SQL 级别的预处理语句：

```sql
PREPARE find_user (TEXT) AS
SELECT id, name, email
FROM users
WHERE email = $1;

EXECUTE find_user('alice@example.com');

DEALLOCATE find_user;
```

## 生成序列 {#generate-a-series}

支持 `generate_series()` 表函数：

```sql
SELECT *
FROM generate_series(1, 5);
```