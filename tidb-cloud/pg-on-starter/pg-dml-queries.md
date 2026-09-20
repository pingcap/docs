---
title: PostgreSQL DML and Queries
summary: Learn about the PostgreSQL data manipulation and query features supported by PostgreSQL-compatible TiDB Cloud Starter.
---

# PostgreSQL DML and Queries

PostgreSQL-compatible {{{ .starter }}} supports common PostgreSQL Data Manipulation Language (DML) statements and query features, including `INSERT`, `UPDATE`, `DELETE`, `RETURNING`, upsert, joins, aggregation, window functions, common table expressions (CTEs), subqueries, and set operations.

## Insert data

Insert a single row:

{{< copyable "sql" >}}

```sql
INSERT INTO users (name, email)
VALUES ('Alice', 'alice@example.com');
```

Insert multiple rows:

{{< copyable "sql" >}}

```sql
INSERT INTO users (name, email)
VALUES
    ('Alice', 'alice@example.com'),
    ('Bob', 'bob@example.com');
```

Insert rows from a query:

{{< copyable "sql" >}}

```sql
INSERT INTO archived_users (id, name, email)
SELECT id, name, email
FROM users
WHERE active = false;
```

### Use `RETURNING`

`INSERT`, `UPDATE`, and `DELETE` support `RETURNING`.

For example:

{{< copyable "sql" >}}

```sql
INSERT INTO users (name, email)
VALUES ('Carol', 'carol@example.com')
RETURNING id, name, email;
```

## Upsert with `ON CONFLICT`

Use `INSERT ... ON CONFLICT` to handle unique-key conflicts.

Skip a conflicting row:

{{< copyable "sql" >}}

```sql
INSERT INTO users (email, name)
VALUES ('alice@example.com', 'Alice')
ON CONFLICT (email) DO NOTHING;
```

Update the existing row on conflict:

{{< copyable "sql" >}}

```sql
INSERT INTO users (email, name)
VALUES ('alice@example.com', 'Alice Updated')
ON CONFLICT (email)
DO UPDATE SET name = excluded.name;
```

Use a named constraint as the conflict target:

{{< copyable "sql" >}}

```sql
INSERT INTO users (email, name)
VALUES ('alice@example.com', 'Alice')
ON CONFLICT ON CONSTRAINT users_email_key
DO UPDATE SET name = excluded.name;
```

The `excluded` pseudo-table represents the row proposed for insertion.

## Update data

Update rows matching a condition:

{{< copyable "sql" >}}

```sql
UPDATE users
SET active = true
WHERE name = 'Charlie';
```

Return the updated rows:

{{< copyable "sql" >}}

```sql
UPDATE users
SET active = true
WHERE name = 'Charlie'
RETURNING *;
```

## Delete data

Delete rows matching a condition:

{{< copyable "sql" >}}

```sql
DELETE FROM users
WHERE id = 1;
```

Return the deleted rows:

{{< copyable "sql" >}}

```sql
DELETE FROM users
WHERE id = 1
RETURNING *;
```

## Foreign-key referential actions

Foreign keys support the following `ON DELETE` and `ON UPDATE` actions:

- `CASCADE`
- `SET NULL`
- `SET DEFAULT`
- `RESTRICT`
- `NO ACTION`

For example:

{{< copyable "sql" >}}

```sql
CREATE TABLE orders (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE
);
```

PostgreSQL-compatible {{{ .starter }}} uses `MATCH SIMPLE` semantics by default. If any referencing column is `NULL`, the foreign-key check for that row is skipped.

## Query data

Use `SELECT` to query data:

{{< copyable "sql" >}}

```sql
SELECT id, name, email
FROM users
WHERE active = true
ORDER BY name
LIMIT 10;
```

## Joins

The following join forms are supported:

| Join type | Supported |
| --- | --- |
| `INNER JOIN` | Yes |
| `LEFT [OUTER] JOIN` | Yes |
| `RIGHT [OUTER] JOIN` | Yes |
| `FULL [OUTER] JOIN` | Yes |
| `CROSS JOIN` | Yes |
| `LATERAL JOIN` | Yes |
| Semi join using `EXISTS` | Yes |
| Anti join using `NOT EXISTS` | Yes |

For example:

{{< copyable "sql" >}}

```sql
SELECT
    u.id,
    u.name,
    o.id AS order_id
FROM users AS u
LEFT JOIN orders AS o
    ON o.user_id = u.id;
```

### Lateral joins

`LATERAL` subqueries can reference columns from preceding `FROM` items.

For example:

{{< copyable "sql" >}}

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

## Aggregation

The following aggregation features are supported:

- `GROUP BY`
- `HAVING`
- `COUNT(DISTINCT ...)`
- Aggregate `FILTER`
- `GROUPING()`

For example:

{{< copyable "sql" >}}

```sql
SELECT
    department,
    count(*) AS employee_count,
    avg(salary) AS average_salary
FROM employees
GROUP BY department
HAVING count(*) > 5;
```

Use `FILTER` to apply a condition to an aggregate:

{{< copyable "sql" >}}

```sql
SELECT
    count(*) AS total,
    count(*) FILTER (WHERE active = true) AS active_count
FROM users;
```

## Window functions

The following ranking window functions are supported:

- `ROW_NUMBER`
- `RANK`
- `DENSE_RANK`
- `NTILE`
- `PERCENT_RANK`
- `CUME_DIST`

The following value access functions are supported:

- `LAG`
- `LEAD`
- `FIRST_VALUE`
- `LAST_VALUE`
- `NTH_VALUE`

For example:

{{< copyable "sql" >}}

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

The following aggregate functions can also be used as window functions:

- `SUM`
- `AVG`
- `COUNT`
- `MIN`
- `MAX`
- `STRING_AGG`

For example:

{{< copyable "sql" >}}

```sql
SELECT
    department,
    name,
    salary,
    AVG(salary) OVER (PARTITION BY department) AS department_average
FROM employees;
```

## Common table expressions

Standard CTEs are supported:

{{< copyable "sql" >}}

```sql
WITH active_users AS (
    SELECT *
    FROM users
    WHERE active = true
)
SELECT *
FROM active_users;
```

Recursive CTEs are also supported:

{{< copyable "sql" >}}

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

Recursive CTEs are limited to 1,000 iterations.

Use a unique name for each CTE definition in the same `WITH` list. For compatibility details, see [PostgreSQL Compatibility](/tidb-cloud/pg-on-starter/postgresql-compatibility.md).

### Data-modifying CTEs

Data-modifying CTEs using `INSERT`, `UPDATE`, or `DELETE` with `RETURNING` are supported over the PostgreSQL wire protocol.

For example:

{{< copyable "sql" >}}

```sql
WITH inserted AS (
    INSERT INTO users (name, email)
    VALUES ('Dave', 'dave@example.com')
    RETURNING id
)
SELECT *
FROM inserted;
```

## Subqueries

The following subquery forms are supported:

- Scalar subqueries
- `EXISTS` and `NOT EXISTS`
- `IN` and `NOT IN` with a subquery
- `ANY` and `ALL` with a subquery
- Array subqueries
- Correlated subqueries

For example:

{{< copyable "sql" >}}

```sql
SELECT u.id, u.name
FROM users AS u
WHERE EXISTS (
    SELECT 1
    FROM orders AS o
    WHERE o.user_id = u.id
);
```

## Set operations

The following set operations are supported:

| Operation | Supported |
| --- | --- |
| `UNION` | Yes |
| `UNION ALL` | Yes |
| `INTERSECT` | Yes |
| `INTERSECT ALL` | Yes |
| `EXCEPT` | Yes |
| `EXCEPT ALL` | Yes |

For example:

{{< copyable "sql" >}}

```sql
SELECT email
FROM customers

UNION

SELECT email
FROM leads;
```

## DISTINCT and ordering

`SELECT DISTINCT` and `SELECT DISTINCT ON (...)` are supported:

{{< copyable "sql" >}}

```sql
SELECT DISTINCT department
FROM employees;
```

{{< copyable "sql" >}}

```sql
SELECT DISTINCT ON (department)
    department,
    name,
    salary
FROM employees
ORDER BY department, salary DESC;
```

Ordering supports `ASC`, `DESC`, `NULLS FIRST`, and `NULLS LAST`:

{{< copyable "sql" >}}

```sql
SELECT id, name
FROM users
ORDER BY name ASC NULLS LAST;
```

## Limit and offset

Use `LIMIT` and `OFFSET` to paginate query results:

{{< copyable "sql" >}}

```sql
SELECT id, name
FROM users
ORDER BY id
LIMIT 20
OFFSET 40;
```

## Explain a query

`EXPLAIN` and `EXPLAIN ANALYZE` are supported:

{{< copyable "sql" >}}

```sql
EXPLAIN
SELECT *
FROM users
WHERE email = 'alice@example.com';
```

{{< copyable "sql" >}}

```sql
EXPLAIN ANALYZE
SELECT *
FROM users
WHERE email = 'alice@example.com';
```

## Prepared statements

Use `PREPARE`, `EXECUTE`, and `DEALLOCATE` for SQL-level prepared statements:

{{< copyable "sql" >}}

```sql
PREPARE find_user (TEXT) AS
SELECT id, name, email
FROM users
WHERE email = $1;

EXECUTE find_user('alice@example.com');

DEALLOCATE find_user;
```

## Generate a series

The `generate_series()` table function is supported:

{{< copyable "sql" >}}

```sql
SELECT *
FROM generate_series(1, 5);
```