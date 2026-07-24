---
title: Data Protection Policies
summary: Learn the masking policy and row access policy that safeguard sensitive information without altering stored values.
---

# Data Protection Policies

{{{ .lake }}} protects sensitive data at query time without changing stored values:

| Policy | What it does |
|--------|----------------|
| [Masking Policy](/tidb-cloud-lake/guides/masking-policy.md) | Transforms column values — unauthorized users see redacted data |
| [Row Access Policy](/tidb-cloud-lake/guides/row-access-policy.md) | Filters entire rows — unauthorized users never see them |

Both are transparent to applications: no code changes, no extra views, no data copies.

## Choose the Right Policy

| Scenario | Use |
|----------|-----|
| Hide entire rows | Row Access |
| Keep the row, redact a column | Masking |
| Different roles see different precision of the same column | Masking |
| Multi-tenant / regional isolation | Row Access |
| Time-window control by role | Row Access |
| Hide keys inside JSON / VARIANT | Masking |
| Row isolation + column redaction | Both (not on the same column) |

Example: an `orders` table with phone, amount, and region.

| Requirement | Policy |
|-------------|--------|
| Support only sees its region | Row Access on `region` |
| Analysts see `138****1234` | Masking on `phone` |
| Admins see everything | Roles that pass both policies |

## How They Work Together

```
Query
  → Row Access Policy filters rows
  → Masking Policy transforms surviving columns
  → Result returned
```

Row filtering runs first. Masking applies only to remaining rows.

| | Masking | Row Access |
|---|---|---|
| Scope | Column values | Entire rows |
| Return type | Match column type | BOOLEAN |
| Limit | One per column | One per table |
| Affects | `SELECT` | `SELECT`, `UPDATE`, `DELETE`, `MERGE` |
| Stored data / `INSERT` | Unchanged / not filtered | Unchanged / not filtered |

Same table can use both. The same **column** cannot be bound to both.

```sql
-- Rows: sales only see their region
CREATE ROW ACCESS POLICY rap_region
AS (r STRING) RETURNS BOOLEAN ->
CASE
  WHEN is_role_in_session('admin') THEN true
  ELSE is_role_in_session(r)
END;

ALTER TABLE customers ADD ROW ACCESS POLICY rap_region ON (region);

-- Columns: non-HR see redacted SSN
CREATE MASKING POLICY mask_ssn
AS (val STRING) RETURNS STRING ->
CASE
  WHEN is_role_in_session('hr') THEN val
  ELSE '***-**-****'
END;

ALTER TABLE customers MODIFY COLUMN ssn SET MASKING POLICY mask_ssn;
```

## End-to-End: Separation of Duties

Combine RBAC with both policies so creators, appliers, and readers stay separated.

| Role | Job | Sees |
|------|-----|------|
| `security_admin` | Create / own policies | No table SELECT |
| `data_engineer` | Own table, attach policies | All rows, raw phone |
| `analyst_apac` | Analyze APAC | APAC rows, masked phone |
| `support_global` | Global support | All rows, raw phone |

```sql
-- account_admin: roles, users, CREATE privileges
CREATE ROLE security_admin;
CREATE ROLE data_engineer;
CREATE ROLE analyst_apac;
CREATE ROLE support_global;

CREATE USER sec_user IDENTIFIED BY 'password123';
CREATE USER eng_user IDENTIFIED BY 'password123';
CREATE USER analyst_user IDENTIFIED BY 'password123';
CREATE USER support_user IDENTIFIED BY 'password123';

GRANT ROLE security_admin TO USER sec_user;
GRANT ROLE data_engineer TO USER eng_user;
GRANT ROLE analyst_apac TO USER analyst_user;
GRANT ROLE support_global TO USER support_user;

GRANT CREATE DATABASE ON *.* TO ROLE data_engineer;
GRANT CREATE MASKING POLICY ON *.* TO ROLE security_admin;
GRANT CREATE ROW ACCESS POLICY ON *.* TO ROLE security_admin;
GRANT GRANT ON *.* TO ROLE security_admin;

-- data_engineer: table ownership
SET ROLE data_engineer;
CREATE DATABASE ecommerce;
CREATE TABLE ecommerce.orders (
  order_id INT,
  customer_name STRING,
  phone STRING,
  region STRING,
  amount DECIMAL(10,2),
  created_at TIMESTAMP
);
INSERT INTO ecommerce.orders VALUES
  (1, 'Alice',   '13812345678', 'APAC', 299.00, '2025-01-15 10:00:00'),
  (2, 'Bob',     '14987654321', 'EMEA', 150.00, '2025-01-16 11:00:00'),
  (3, 'Charlie', '13698765432', 'APAC', 520.00, '2025-01-17 09:30:00'),
  (4, 'Diana',   '15012349876', 'AMER',  89.00, '2025-01-18 14:00:00');

-- security_admin: create policies (auto OWNERSHIP)
SET ROLE security_admin;
SET enable_experimental_row_access_policy = 1;

CREATE MASKING POLICY mask_phone
AS (val STRING) RETURNS STRING ->
CASE
  WHEN is_role_in_session('data_engineer') OR is_role_in_session('support_global') THEN val
  ELSE CONCAT(SUBSTRING(val, 1, 3), '****', SUBSTRING(val, 8))
END;

CREATE ROW ACCESS POLICY rap_region
AS (r STRING) RETURNS BOOLEAN ->
CASE
  WHEN is_role_in_session('data_engineer') OR is_role_in_session('support_global') THEN true
  WHEN is_role_in_session('analyst_apac') AND r = 'APAC' THEN true
  ELSE false
END;

GRANT APPLY ON MASKING POLICY mask_phone TO ROLE data_engineer;
GRANT APPLY ON ROW ACCESS POLICY rap_region TO ROLE data_engineer;

-- data_engineer: attach (needs table ALTER + policy APPLY)
SET ROLE data_engineer;
SET enable_experimental_row_access_policy = 1;
ALTER TABLE ecommerce.orders MODIFY COLUMN phone SET MASKING POLICY mask_phone;
ALTER TABLE ecommerce.orders ADD ROW ACCESS POLICY rap_region ON (region);

-- account_admin: grant table access through roles
GRANT USAGE ON ecommerce.* TO ROLE analyst_apac;
GRANT USAGE ON ecommerce.* TO ROLE support_global;
GRANT SELECT ON ecommerce.orders TO ROLE analyst_apac;
GRANT SELECT ON ecommerce.orders TO ROLE support_global;
```

Results:

| Role | Rows | Phone |
|------|------|-------|
| `analyst_apac` | APAC only | Masked (`138****5678`) |
| `support_global` | All | Raw |
| `security_admin` | — | Permission denied (no SELECT) |

```sql
SET ROLE analyst_apac;
SELECT * FROM ecommerce.orders;
-- Alice / Charlie only, phones masked

SET ROLE support_global;
SELECT * FROM ecommerce.orders;
-- all 4 rows, phones visible

SET ROLE security_admin;
SELECT * FROM ecommerce.orders;
-- ERROR: Permission denied
```

Revoking the role removes access without changing table grants:

```sql
REVOKE ROLE analyst_apac FROM USER analyst_user;
```

**Rules of thumb:**

- Creating policies ≠ querying data; attaching needs **both** policy `APPLY` and table `ALTER`
- Prefer grants to roles, not users
- Creator roles get OWNERSHIP automatically
- `CREATE MASKING/ROW ACCESS POLICY` is granted to roles, not users
- Audit with `SHOW GRANTS ON MASKING POLICY ...`, `SHOW GRANTS ON ROW ACCESS POLICY ...`, and `POLICY_REFERENCES(...)`

## Next Steps

- [Masking Policy](/tidb-cloud-lake/guides/masking-policy.md) — conditional masking, VARIANT keys
- [Row Access Policy](/tidb-cloud-lake/guides/row-access-policy.md) — vector / RAG visibility, time windows, DML
