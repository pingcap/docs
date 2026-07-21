---
title: Row Access Policy
summary: Row access policies protect data by filtering table rows at query time. They let you define centralized row-level predicates once, attach them to tables, and ensure users only see rows that satisfy the policy.
---

# Row Access Policy

Row access policies filter table rows at query time. Define a Boolean predicate once, attach it to a table, and users only see rows that pass the policy.

For column-level redaction instead of hiding rows, use a [Masking Policy](/tidb-cloud-lake/guides/masking-policy.md).

> **Note:**
>
> This is an **experimental** feature. Enable it with `SET enable_experimental_row_access_policy = 1` (session) or `SET GLOBAL enable_experimental_row_access_policy = 1` (account).

## When to Use

- Multi-tenant isolation — each tenant only sees its own rows
- Regional / department isolation — sales sees only its territory
- Time-window control — alerting can scan 1 day; offline analysis can scan 7 days
- Vector / RAG search — shared knowledge base, role-based document visibility
- Compliance — auditors only see an approved time range or subset

## Quick Start

```sql
SET enable_experimental_row_access_policy = 1;

CREATE TABLE employees (
  id INT,
  name STRING,
  department STRING
);

INSERT INTO employees VALUES
  (1, 'Alice', 'Engineering'),
  (2, 'Bob', 'Sales'),
  (3, 'Charlie', 'Engineering');

CREATE ROW ACCESS POLICY rap_engineering
AS (dept STRING)
RETURNS BOOLEAN ->
CASE
  WHEN IS_ROLE_IN_SESSION('admin') THEN true
  WHEN dept = 'Engineering' THEN true
  ELSE false
END;

-- ON (column) maps to the policy argument by position
ALTER TABLE employees ADD ROW ACCESS POLICY rap_engineering ON (department);

SELECT id, name, department FROM employees ORDER BY id;
```

```
id | name    | department
---|---------|-------------
 1 | Alice   | Engineering
 3 | Charlie | Engineering
```

**How it works**

- Query-time only — stored data is unchanged
- One policy per table; arguments map to columns by position in `ON (...)`
- Prefer `IS_ROLE_IN_SESSION()` over `current_role()` so users cannot bypass with `SET ROLE`

Multi-column policy:

```sql
CREATE ROW ACCESS POLICY rap_region_dept
AS (region STRING, dept STRING)
RETURNS BOOLEAN ->
  region = 'APAC' AND dept = 'Engineering';

ALTER TABLE employees
ADD ROW ACCESS POLICY rap_region_dept ON (office_region, department);
```

## Examples

### Vector / RAG document visibility

Shared knowledge-base table + vector search. Configure visibility once; search SQL does not carry document-ID filters. See [Vector Search](/tidb-cloud-lake/guides/vector-search-guide.md).

| Role | Sees |
|------|------|
| `admin` | All rows |
| `sales` | `dept = 'sales'` + public |
| `finance` | `dept = 'finance'` + public |

```sql
SET enable_experimental_row_access_policy = 1;

CREATE ROLE IF NOT EXISTS admin;
CREATE ROLE IF NOT EXISTS sales;
CREATE ROLE IF NOT EXISTS finance;

CREATE TABLE knowledge_docs (
  doc_id    BIGINT,
  title     STRING,
  dept      STRING,
  is_public BOOLEAN,
  embedding VECTOR(4),
  VECTOR INDEX idx_emb(embedding) distance='cosine'
);

INSERT INTO knowledge_docs VALUES
  (1, 'Sales contract template',  'sales',   false, [0.90, 0.10, 0.05, 0.05]),
  (2, 'Q2 financial draft',       'finance', false, [0.10, 0.90, 0.05, 0.05]),
  (3, 'Public company handbook',  'hr',      true,  [0.20, 0.20, 0.90, 0.10]),
  (4, 'Competitor pricing notes', 'sales',   false, [0.85, 0.15, 0.10, 0.05]),
  (5, 'Internal audit checklist', 'finance', false, [0.15, 0.85, 0.10, 0.05]);

CREATE ROW ACCESS POLICY rap_knowledge_docs
AS (dept STRING, is_public BOOLEAN)
RETURNS BOOLEAN ->
CASE
  WHEN IS_ROLE_IN_SESSION('admin') THEN true
  WHEN is_public THEN true
  WHEN IS_ROLE_IN_SESSION('sales') AND dept = 'sales' THEN true
  WHEN IS_ROLE_IN_SESSION('finance') AND dept = 'finance' THEN true
  ELSE false
END;

ALTER TABLE knowledge_docs
ADD ROW ACCESS POLICY rap_knowledge_docs ON (dept, is_public);

GRANT SELECT ON knowledge_docs TO ROLE sales;
GRANT SELECT ON knowledge_docs TO ROLE finance;

-- Activate one role for the session, then run the same search SQL
SET ROLE sales;
SET SECONDARY ROLES NONE;

SELECT doc_id, title,
       round(cosine_distance(embedding, [0.88, 0.12, 0.08, 0.05]::VECTOR(4)), 4) AS dist
FROM knowledge_docs
ORDER BY dist
LIMIT 10;
```

| As `sales` | As `finance` (`SET ROLE finance`) |
|------------|-------------------------------------|
| 1 Sales contract template `0.0009` | 3 Public company handbook `0.6731` |
| 4 Competitor pricing notes `0.0011` | 5 Internal audit checklist `0.6855` |
| 3 Public company handbook `0.6731` | 2 Q2 financial draft `0.7504` |

### Time-range access by role

Different service accounts may only scan different history windows.

| Account | Roles | Window |
|---------|-------|--------|
| `svc_realtime_alert` | `rap_role_1_day` | Last 1 day |
| `svc_offline_analysis` | `rap_role_1_day`, `rap_role_7_day` | Up to 7 days |

```sql
SET enable_experimental_row_access_policy = 1;

CREATE ROLE rap_role_7_day;
CREATE ROLE rap_role_1_day;

-- CASE is top-down: put the wider window first
CREATE ROW ACCESS POLICY rap_time_range
AS (start_time TIMESTAMP)
RETURNS BOOLEAN ->
CASE
  WHEN IS_ROLE_IN_SESSION('rap_role_7_day') THEN
    start_time >= now() - INTERVAL 7 DAY
  WHEN IS_ROLE_IN_SESSION('rap_role_1_day') THEN
    start_time >= now() - INTERVAL 1 DAY
  ELSE false
END;

CREATE TABLE metrics(id INT, start_time TIMESTAMP);
INSERT INTO metrics VALUES
  (1, now() - INTERVAL 15 DAY),
  (2, now() - INTERVAL 5 DAY),
  (3, now() - INTERVAL 12 HOUR),
  (4, now() - INTERVAL 1 HOUR),
  (5, now() - INTERVAL 8 DAY);

ALTER TABLE metrics ADD ROW ACCESS POLICY rap_time_range ON (start_time);

GRANT ROLE rap_role_1_day TO USER svc_realtime_alert;
GRANT ROLE rap_role_1_day TO USER svc_offline_analysis;
GRANT ROLE rap_role_7_day TO USER svc_offline_analysis;

SELECT id, start_time FROM metrics ORDER BY id;
```

After login, {{{ .lake }}} activates all granted roles (`SECONDARY ROLES ALL`).

| Session | Visible rows |
|---------|--------------|
| `svc_realtime_alert` (1-day only) | last 1 day |
| `svc_offline_analysis` (both roles) | last 7 days by default |

Narrow the offline account to 1 day:

```sql
SET ROLE rap_role_1_day;
SET SECONDARY ROLES NONE;
SELECT id, start_time FROM metrics ORDER BY id;
```

Widen again:

```sql
SET ROLE rap_role_7_day;
SELECT id, start_time FROM metrics ORDER BY id;
```

An account can only activate roles it was granted. `svc_realtime_alert` cannot `SET ROLE rap_role_7_day`.

## Read and Write Behavior

| Operation | Effect |
|-----------|--------|
| `SELECT` | Only policy-visible rows |
| `UPDATE` / `DELETE` / `MERGE` | Only match / modify visible target rows |
| `INSERT` | Not filtered — rows are stored even if currently invisible |

To inspect all stored rows, use a role that passes the policy, or temporarily detach it.

```sql
SET enable_experimental_row_access_policy = 1;

CREATE ROW ACCESS POLICY rap_sales_only
AS (dept STRING) RETURNS BOOLEAN -> dept = 'sales';

CREATE TABLE orders(id INT, dept STRING, amount INT);
ALTER TABLE orders ADD ROW ACCESS POLICY rap_sales_only ON (dept);

INSERT INTO orders VALUES (1, 'sales', 100), (2, 'eng', 200), (3, 'sales', 300);

SELECT * FROM orders ORDER BY id;
-- 1 sales 100
-- 3 sales 300

UPDATE orders SET amount = amount + 10;
DELETE FROM orders WHERE dept = 'eng';   -- no-op: eng rows are invisible
DELETE FROM orders WHERE id = 1;         -- deletes visible row 1

-- MERGE only matches visible targets
CREATE TABLE src(id INT, new_amount INT);
INSERT INTO src VALUES (2, 777), (3, 888);

MERGE INTO orders AS t
USING src AS s
ON t.id = s.id
WHEN MATCHED THEN UPDATE SET t.amount = s.new_amount;

-- Detach to inspect storage
ALTER TABLE orders DROP ROW ACCESS POLICY rap_sales_only;
SELECT * FROM orders ORDER BY id;
-- 2 eng 200   (never updated)
-- 3 sales 888 (merged)
```

## Manage Policies

```sql
DESC ROW ACCESS POLICY rap_engineering;

ALTER TABLE employees DROP ROW ACCESS POLICY rap_engineering;
DROP ROW ACCESS POLICY rap_engineering;

ALTER TABLE employees DROP ALL ROW ACCESS POLICIES;
```

Detach before `DROP ROW ACCESS POLICY`. Drop or detach before altering protected columns.

## Limits

- One row access policy per table
- Regular tables only — not views, streams, temporary tables, or ICE databases
- One security policy per column (masking **or** row access, not both)
- No `CREATE OR REPLACE` / `ALTER` policy — drop and recreate
- Policy names are globally unique across masking and row access policies
- Policy argument names are lowercased at create time

## Best Practices

1. Prefer `IS_ROLE_IN_SESSION()` over `current_role()`.
2. Order `CASE` branches widest → narrowest (admin first).
3. If a policy references a lookup table, keep it in the same database as the protected table.
4. Verify with multiple roles after attach — admin, restricted, and no-match.
5. Prefer a privileged role for full-data inspection over repeated detach/attach.

## Privileges & References

- `CREATE ROW ACCESS POLICY` on `*.*` to create policies (creator gets OWNERSHIP)
- `ALTER` on the table + `APPLY ROW ACCESS POLICY` (global) or `APPLY ON ROW ACCESS POLICY <name>` to attach/detach
- Audit: `SHOW GRANTS ON ROW ACCESS POLICY <name>`
- Usage: [`POLICY_REFERENCES`](/sql/sql-functions/table-functions/policy-references)

Also see:

- [User & Role](/tidb-cloud-lake/sql/user-role.md)
- [CREATE ROW ACCESS POLICY](/tidb-cloud-lake/sql/create-row-access-policy.md)
- [ALTER TABLE](/tidb-cloud-lake/sql/alter-table.md#row-access-policy-operations)
- [Row Access Policy Commands](/tidb-cloud-lake/sql/row-access-policy-overview.md)
