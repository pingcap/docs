---
title: PostgreSQL DML とクエリ
summary: PostgreSQL 互換の TiDB Cloud Starter でサポートされる PostgreSQL のデータ操作およびクエリ機能について説明します。
---

# PostgreSQL DML とクエリ

PostgreSQL 互換の {{{ .starter }}} は、`INSERT`、`UPDATE`、`DELETE`、`RETURNING`、upsert、テーブル結合、集計、ウィンドウ関数、共通テーブル式（CTE）、サブクエリ、集合演算など、一般的な PostgreSQL のデータ操作言語（DML）文とクエリ機能をサポートしています。

## サンプルテーブルを準備する {#prepare-sample-tables}

このページの一部の例では、サンプルテーブルを使用します。例を実行する前に、テストデータベースに次のテーブルを作成してください。

このページのテーブル定義は、他の例で使用されているものとは異なります。テストデータベースにすでに以下の名前のテーブルが存在する場合は、このページ用に別のテストデータベースを使用してください。

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

集計、ウィンドウ関数、再帰 CTE、集合演算の例で使用するサンプルテーブルにデータを投入するには、次を実行します。

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

このページの例を実行する前に、これらのセットアップ文を一度実行してください。`users` テーブルは初期状態では空であるため、`INSERT` の例で競合なくデータを投入できます。

前の例で挿入または変更されたデータによっては、一部のクエリが行を返さない場合があります。

## データを挿入する {#insert-data}

1 行を挿入します。

```sql
INSERT INTO users (name, email)
VALUES ('Alice', 'alice@example.com');
```

複数行を挿入します。

```sql
INSERT INTO users (name, email)
VALUES
    ('Charlie', 'charlie@example.com'),
    ('Bob', 'bob@example.com');
```

クエリ結果から行を挿入します。

```sql
INSERT INTO archived_users (id, name, email)
SELECT id, name, email
FROM users
WHERE active = false;
```

### `RETURNING` を使用する {#use-returning}

`INSERT`、`UPDATE`、`DELETE` は `RETURNING` をサポートしています。

例:

```sql
INSERT INTO users (name, email)
VALUES ('Carol', 'carol@example.com')
RETURNING id, name, email;
```

## `ON CONFLICT` を使用した upsert {#upsert-with-on-conflict}

一意キーの競合を処理するには、`INSERT ... ON CONFLICT` を使用します。

競合した行をスキップします。

```sql
INSERT INTO users (email, name)
VALUES ('alice@example.com', 'Alice')
ON CONFLICT (email) DO NOTHING;
```

競合時に既存の行を更新します。

```sql
INSERT INTO users (email, name)
VALUES ('alice@example.com', 'Alice Updated')
ON CONFLICT (email)
DO UPDATE SET name = excluded.name;
```

競合対象として名前付き制約を使用します。

```sql
INSERT INTO users (email, name)
VALUES ('alice@example.com', 'Alice')
ON CONFLICT ON CONSTRAINT users_email_key
DO UPDATE SET name = excluded.name;
```

`excluded` 疑似テーブルは、挿入対象として提案された行を表します。

## データを更新する {#update-data}

PostgreSQL 互換の {{{ .starter }}} では、`UPDATE` を実行するには対象テーブルに主キーが必要です。PostgreSQL とは異なり、主キーのないテーブルに対する更新は、`WHERE` 条件に一致する行が 0 件であっても、`ERROR: No PK` で失敗します。

テーブルにすでにデータが存在し、かつ主キーがない場合、データが入ったままのテーブルに直接主キーを追加することはサポートされていません。更新を可能にするには、既存の行をバックアップするか別のテーブルにコピーし、元のテーブルから行を削除して主キーを追加した後、データを再挿入してください。行を復元する前に、主キーの値が一意であり、NULL でないことを確認してください。

条件に一致する行を更新します。

```sql
UPDATE users
SET active = true
WHERE name = 'Charlie';
```

更新された行を返します。

```sql
UPDATE users
SET active = true
WHERE name = 'Charlie'
RETURNING *;
```

## データを削除する {#delete-data}

条件に一致する行を削除します。

```sql
DELETE FROM users
WHERE name = 'Bob';
```

削除された行を返します。

```sql
DELETE FROM users
WHERE name = 'Charlie'
RETURNING *;
```

## 外部キーの参照アクション {#foreign-key-referential-actions}

外部キーは、次の `ON DELETE` および `ON UPDATE` アクションをサポートしています。

- `CASCADE`
- `SET NULL`
- `SET DEFAULT`
- `RESTRICT`
- `NO ACTION`

例:

```sql
CREATE TABLE orders_with_cascade (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE
);
```

PostgreSQL 互換の {{{ .starter }}} では、デフォルトで `MATCH SIMPLE` セマンティクスを使用します。参照しているいずれかのカラムが `NULL` の場合、その行に対する外部キーチェックはスキップされます。

## データをクエリする {#query-data}

データをクエリするには `SELECT` を使用します。

```sql
SELECT id, name, email
FROM users
WHERE active = true
ORDER BY name
LIMIT 10;
```

## テーブル結合 {#joins}

次のテーブル結合および関連するクエリパターンをサポートしています。

| テーブル結合またはクエリパターン | サポート |
| --- | --- |
| `INNER JOIN` | はい |
| `LEFT [OUTER] JOIN` | はい |
| `RIGHT [OUTER] JOIN` | はい |
| `FULL [OUTER] JOIN` | はい |
| `CROSS JOIN` | はい |
| `LATERAL` サブクエリ | はい |
| `EXISTS` を使用したセミ結合 | はい |
| `NOT EXISTS` を使用したアンチ結合 | はい |

例:

```sql
SELECT
    u.id,
    u.name,
    o.id AS order_id
FROM users AS u
LEFT JOIN orders AS o
    ON o.user_id = u.id;
```

### Lateral テーブル結合 {#lateral-joins}

`LATERAL` サブクエリは、先行する `FROM` 項目のカラムを参照できます。

例:

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

## 集計 {#aggregation}

次の集計機能をサポートしています。

- `GROUP BY`
- `HAVING`
- `COUNT(DISTINCT ...)`
- 集計 `FILTER`
- `GROUPING()`

例:

```sql
SELECT
    department,
    count(*) AS employee_count,
    avg(salary) AS average_salary
FROM employees
GROUP BY department
HAVING count(*) > 5;
```

`FILTER` を使用すると、集計に条件を適用できます。

```sql
SELECT
    count(*) AS total,
    count(*) FILTER (WHERE active = true) AS active_count
FROM users;
```

## ウィンドウ関数 {#window-functions}

次のランキング用ウィンドウ関数をサポートしています。

- `ROW_NUMBER`
- `RANK`
- `DENSE_RANK`
- `NTILE`
- `PERCENT_RANK`
- `CUME_DIST`

次の値アクセス関数をサポートしています。

- `LAG`
- `LEAD`
- `FIRST_VALUE`
- `LAST_VALUE`
- `NTH_VALUE`

例:

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

次の集計関数もウィンドウ関数として使用できます。

- `SUM`
- `AVG`
- `COUNT`
- `MIN`
- `MAX`
- `STRING_AGG`

例:

```sql
SELECT
    department,
    name,
    salary,
    AVG(salary) OVER (PARTITION BY department) AS department_average
FROM employees;
```

## 共通テーブル式 {#common-table-expressions}

非再帰 CTE がサポートされています。

```sql
WITH active_users AS (
    SELECT *
    FROM users
    WHERE active = true
)
SELECT *
FROM active_users;
```

再帰 CTE もサポートされています。

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

再帰 CTE は 1,000 回の反復に制限されています。

同じ `WITH` リスト内では、各 CTE 定義に一意の名前を使用してください。再帰 CTE の制限については、[PostgreSQL の制限事項と制約](/tidb-cloud/starter/pg-limits-constraints.md) を参照してください。

### データ変更 CTE {#data-modifying-ctes}

`RETURNING` を伴う `INSERT`、`UPDATE`、または `DELETE` を使用するデータ変更 CTE は、PostgreSQL ワイヤプロトコル経由でサポートされています。

例:

```sql
WITH inserted AS (
    INSERT INTO users (name, email)
    VALUES ('Dave', 'dave@example.com')
    RETURNING id
)
SELECT *
FROM inserted;
```

## サブクエリ {#subqueries}

以下のサブクエリ形式がサポートされています。

- スカラーサブクエリ
- `EXISTS` と `NOT EXISTS`
- サブクエリを伴う `IN` と `NOT IN`
- サブクエリを伴う `ANY` と `ALL`
- 配列サブクエリ
- 相関サブクエリ

例:

```sql
SELECT u.id, u.name
FROM users AS u
WHERE EXISTS (
    SELECT 1
    FROM orders AS o
    WHERE o.user_id = u.id
);
```

## 集合演算 {#set-operations}

以下の集合演算がサポートされています。

| 演算 | サポート |
| --- | --- |
| `UNION` | はい |
| `UNION ALL` | はい |
| `INTERSECT` | はい |
| `INTERSECT ALL` | はい |
| `EXCEPT` | はい |
| `EXCEPT ALL` | はい |

例:

```sql
SELECT email
FROM customers

UNION

SELECT email
FROM leads;
```

## DISTINCT と並び順 {#distinct-and-ordering}

`SELECT DISTINCT` と `SELECT DISTINCT ON (...)` がサポートされています。

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

並び順では、`ASC`、`DESC`、`NULLS FIRST`、`NULLS LAST` がサポートされています。

```sql
SELECT id, name
FROM users
ORDER BY name ASC NULLS LAST;
```

## LIMIT と OFFSET {#limit-and-offset}

クエリ結果をページ分割するには、`LIMIT` と `OFFSET` を使用します。

```sql
SELECT id, name
FROM users
ORDER BY id
LIMIT 20
OFFSET 40;
```

## クエリを EXPLAIN する {#explain-a-query}

`EXPLAIN` と `EXPLAIN ANALYZE` がサポートされています。

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

## プリペアドステートメント {#prepared-statements}

SQL レベルのプリペアドステートメントには、`PREPARE`、`EXECUTE`、`DEALLOCATE` を使用します。

```sql
PREPARE find_user (TEXT) AS
SELECT id, name, email
FROM users
WHERE email = $1;

EXECUTE find_user('alice@example.com');

DEALLOCATE find_user;
```

## 連番を生成する {#generate-a-series}

`generate_series()` テーブル関数がサポートされています。

```sql
SELECT *
FROM generate_series(1, 5);
```