---
title: Data Protection Policies
summary: Learn the masking policy and row access policy that safeguard sensitive information without altering stored values.
---

# Data Protection Policies

{{{ .lake }}} provides two complementary policy types that protect sensitive data without changing stored values:

- **Masking Policy** — transforms column values at query time so unauthorized users see redacted data.
- **Row Access Policy** — filters entire rows at query time so unauthorized users never see them.

Both policies are transparent to applications: no code changes, no extra views, no data duplication.

## Choosing the Right Policy

Consider an `orders` table with customer phone numbers, order amounts, and regions. Three roles query it:

- **Support agents** need phone numbers (to contact customers) but should only see orders in their own region.
- **Analysts** need all regions for reporting but phone numbers must be redacted.
- **Admins** see everything.

This single requirement splits into two policies:

| Requirement | Policy Type |
|---|---|
| Support agents only see their region's rows | Row Access Policy |
| Analysts see `138****1234` instead of real phone numbers | Masking Policy |

## When to Use Each

| Scenario | Use |
|----------|-----|
| Users should not see certain rows at all | Row Access Policy |
| All users see the row, but a sensitive column is redacted | Masking Policy |
| Different roles see different precision of the same column | Masking Policy |
| Multi-tenant isolation — tenants only see their own data | Row Access Policy |
| Restrict queryable time range by role | Row Access Policy |
| Hide specific keys inside a JSON/VARIANT column | Masking Policy |
| Row-level isolation + column-level redaction together | Both (but the same column cannot have both) |

## How They Work Together

```
Query
  → Row Access Policy filters rows (rows that fail the predicate disappear)
  → Masking Policy transforms column values (sensitive fields are replaced)
  → Result returned to user
```

Row filtering happens first. Masking applies only to the surviving rows.

## Quick Comparison

| | Masking Policy | Row Access Policy |
|---|---|---|
| Protection granularity | Column (values replaced) | Row (entire row hidden) |
| Return type | Must match column type | Always BOOLEAN |
| Limit per table | One policy per column | One policy per table |
| Affected operations | SELECT | SELECT, UPDATE, DELETE, MERGE |
| Stored data changed? | No | No |
| INSERT affected? | No | No |

## Combining Both Policies

You can attach a masking policy to one column and a row access policy to the same table — they compose naturally. The only constraint is that a single column cannot be referenced in both a masking policy binding and a row access policy binding simultaneously.

**Example**: a `customers` table where:

- Row access policy on `region` ensures each sales rep only sees their territory
- Masking policy on `ssn` ensures non-HR roles see `***-**-****`

```sql
-- Row-level: filter by region
CREATE ROW ACCESS POLICY rap_region
AS (r STRING) RETURNS BOOLEAN ->
  CASE
    WHEN is_role_in_session('admin') THEN true
    ELSE is_role_in_session(r)
  END;

ALTER TABLE customers ADD ROW ACCESS POLICY rap_region ON (region);

-- Column-level: mask SSN
CREATE MASKING POLICY mask_ssn
AS (val STRING) RETURNS STRING ->
  CASE
    WHEN is_role_in_session('hr') THEN val
    ELSE '***-**-****'
  END;

ALTER TABLE customers MODIFY COLUMN ssn SET MASKING POLICY mask_ssn;
```

## Advanced Practice: End-to-End Access Control

This section walks through a production-ready setup combining RBAC, ownership, table privileges, and policy privileges. By the end, you'll see how separation of duties works in practice — who creates policies, who attaches them, and who queries the protected data.

### Scenario

An e-commerce company has an `orders` table with sensitive customer data. Four roles need different levels of access:

| Role | Responsibility | Data Visibility |
|------|---------------|-----------------|
| `security_admin` | Creates and manages all policies | Cannot query data directly |
| `data_engineer` | Creates tables, attaches policies | Sees all data (admin-level) |
| `analyst_apac` | Analyzes APAC region data | Only APAC rows, phone numbers masked |
| `support_global` | Global customer support | All rows, phone numbers visible |

<details>
<summary>How It All Fits Together (click to expand)</summary>

```text
+--------------------------------------------------------------------------------+
| ecommerce.orders (raw data)                                                    |
+----------+---------------+-------------+--------+--------+---------------------+
| order_id | customer_name | phone       | region | amount | created_at          |
+----------+---------------+-------------+--------+--------+---------------------+
| 1        | Alice         | 13812345678 | APAC   | 299.00 | 2025-01-15 10:00:00 |
| 2        | Bob           | 14987654321 | EMEA   | 150.00 | 2025-01-16 11:00:00 |
| 3        | Charlie       | 13698765432 | APAC   | 520.00 | 2025-01-17 09:30:00 |
| 4        | Diana         | 15012349876 | AMER   |  89.00 | 2025-01-18 14:00:00 |
+---------------------------------------+----------------------------------------+
                                        |
                                        v
                   +------------------------------------------------+
                   | 1) Row Access Policy: rap_region               |
                   |    ON (region)                                 |
                   |                                                |
                   |    data_engineer / support_global -> ALL       |
                   |    analyst_apac -> region = 'APAC' only        |
                   |    others -> NONE                              |
                   +------------------------+-----------------------+
                                            |
                                            v
                   +------------------------------------------------+
                   | 2) Masking Policy: mask_phone                  |
                   |    ON (phone)                                  |
                   |                                                |
                   |    data_engineer / support_global -> raw       |
                   |    others -> CONCAT(LEFT(3), '****', ...)      |
                   +------------------------+-----------------------+
                                            |
                                            v
          +-------------------------+-----------------------------+-----------------------------+
          |                         |                             |                             |
          v                         v                             v                             v
+--------------------+ +---------------------------+ +---------------------------+ +---------------------------+
| security_admin     | | data_engineer             | | analyst_apac              | | support_global            |
+--------------------+ +---------------------------+ +---------------------------+ +---------------------------+
| permission denied  | | id name    phone          | | id name    phone          | | id name    phone          |
| no SELECT          | | 1  Alice   13812345678    | | 1  Alice   138****5678    | | 1  Alice   13812345678    |
|                    | | 2  Bob     14987654321    | | 3  Charlie 136****5432    | | 2  Bob     14987654321    |
|                    | | 3  Charlie 13698765432    | |                           | | 3  Charlie 13698765432    |
|                    | | 4  Diana   15012349876    | |                           | | 4  Diana   15012349876    |
|                    | |                           | |                           | |                           |
| 0 rows             | | 4 rows, all regions       | | 2 rows, APAC only         | | 4 rows, all regions       |
|                    | | phone: visible            | | phone: masked             | | phone: visible            |
+--------------------+ +---------------------------+ +---------------------------+ +---------------------------+
```

</details>

The following steps show how to build this setup from scratch.

### Step 1: Create Roles and Users

```sql
-- Run as account_admin

CREATE ROLE security_admin;
CREATE ROLE data_engineer;
CREATE ROLE analyst_apac;
CREATE ROLE support_global;

CREATE USER 'sec_user' IDENTIFIED BY 'password123';
CREATE USER 'eng_user' IDENTIFIED BY 'password123';
CREATE USER 'analyst_user' IDENTIFIED BY 'password123';
CREATE USER 'support_user' IDENTIFIED BY 'password123';

GRANT ROLE security_admin TO USER 'sec_user';
GRANT ROLE data_engineer TO USER 'eng_user';
GRANT ROLE analyst_apac TO USER 'analyst_user';
GRANT ROLE support_global TO USER 'support_user';
```

### Step 2: Set Up Table and Ownership

Grant `data_engineer` the ability to create databases, then create the table as that role. Ownership is automatically assigned to the creating role.

```sql
-- Run as account_admin
GRANT CREATE DATABASE ON *.* TO ROLE data_engineer;

-- Switch to data_engineer
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
    (1, 'Alice', '13812345678', 'APAC', 299.00, '2025-01-15 10:00:00'),
    (2, 'Bob', '14987654321', 'EMEA', 150.00, '2025-01-16 11:00:00'),
    (3, 'Charlie', '13698765432', 'APAC', 520.00, '2025-01-17 09:30:00'),
    (4, 'Diana', '15012349876', 'AMER', 89.00, '2025-01-18 14:00:00');
```

At this point, `data_engineer` owns `ecommerce.orders` and has full control over it.

### Step 3: Grant Policy Creation Privileges

Policy creation privileges are global (on `*.*`) and must be granted to roles, not users. Grant `GRANT` to `security_admin` if it should delegate policy APPLY privileges itself.

```sql
-- Run as account_admin
GRANT CREATE MASKING POLICY ON *.* TO ROLE security_admin;
GRANT CREATE ROW ACCESS POLICY ON *.* TO ROLE security_admin;
GRANT GRANT ON *.* TO ROLE security_admin;
```

Now `security_admin` can create policies and delegate APPLY privileges, but still cannot query any table.

### Step 4: Create Policies (as security_admin)

```sql
SET ROLE security_admin;
SET enable_experimental_row_access_policy = 1;

-- Masking policy: hide phone numbers from roles without 'support_global' or 'data_engineer'
CREATE MASKING POLICY mask_phone
AS (val STRING)
RETURNS STRING ->
  CASE
    WHEN is_role_in_session('data_engineer') OR is_role_in_session('support_global') THEN val
    ELSE CONCAT(SUBSTRING(val, 1, 3), '****', SUBSTRING(val, 8))
  END;

-- Row access policy: filter by region
CREATE ROW ACCESS POLICY rap_region
AS (r STRING)
RETURNS BOOLEAN ->
  CASE
    WHEN is_role_in_session('data_engineer') OR is_role_in_session('support_global') THEN true
    WHEN is_role_in_session('analyst_apac') AND r = 'APAC' THEN true
    ELSE false
  END;
```

`security_admin` now owns both policies (OWNERSHIP auto-granted). But it cannot attach them to `ecommerce.orders` because it does not have ALTER on the table.

### Step 5: Grant Policy Apply Privileges

The policy owner (`security_admin`) delegates APPLY to `data_engineer`, who owns the table and can attach policies.

```sql
-- Run as security_admin (owner of the policies)
GRANT APPLY ON MASKING POLICY mask_phone TO ROLE data_engineer;
GRANT APPLY ON ROW ACCESS POLICY rap_region TO ROLE data_engineer;
```

### Step 6: Attach the Masking Policy First (as data_engineer)

`data_engineer` has both ALTER on the table (via ownership) and APPLY on the masking policy. Both are required.

```sql
SET ROLE data_engineer;
ALTER TABLE ecommerce.orders MODIFY COLUMN phone SET MASKING POLICY mask_phone;
```

At this point, the table has column masking but no row filtering. Users with SELECT can still see all rows, but unauthorized phone numbers are masked.

### Step 7: Grant Table Access Through Roles

Grant table access to roles, not directly to users. The users received these roles in Step 1, so their table access flows through role membership.

```sql
-- Run as account_admin
GRANT SELECT ON ecommerce.orders TO ROLE analyst_apac;
GRANT SELECT ON ecommerce.orders TO ROLE support_global;
GRANT USAGE ON ecommerce.* TO ROLE analyst_apac;
GRANT USAGE ON ecommerce.* TO ROLE support_global;
```

### Step 8: Verify Without Row Access Policy

**analyst_user** has the `analyst_apac` role, so it can query the table. Because the row access policy is not attached yet, it sees all rows. Because the masking policy is already attached, phone numbers are masked.

```sql
-- Connect as analyst_user
SET ROLE analyst_apac;
SELECT * FROM ecommerce.orders;
```

```
order_id | customer_name | phone       | region | amount | created_at
---------|---------------|-------------|--------|--------|--------------------
       1 | Alice         | 138****5678 | APAC   | 299.00 | 2025-01-15 10:00:00
       2 | Bob           | 149****4321 | EMEA   | 150.00 | 2025-01-16 11:00:00
       3 | Charlie       | 136****5432 | APAC   | 520.00 | 2025-01-17 09:30:00
       4 | Diana         | 150****9876 | AMER   | 89.00  | 2025-01-18 14:00:00
```

### Step 9: Attach Row Access Policy

Now attach the row access policy. This adds row filtering on top of the existing phone masking.

```sql
-- Run as data_engineer
SET ROLE data_engineer;
SET enable_experimental_row_access_policy = 1;

ALTER TABLE ecommerce.orders ADD ROW ACCESS POLICY rap_region ON (region);
```

### Step 10: Verify With Row Access Policy

**analyst_user** — only APAC rows, phone masked:

```sql
-- Connect as analyst_user
SET ROLE analyst_apac;
SELECT * FROM ecommerce.orders;
```

```
order_id | customer_name | phone       | region | amount | created_at
---------|---------------|-------------|--------|--------|--------------------
       1 | Alice         | 138****5678 | APAC   | 299.00 | 2025-01-15 10:00:00
       3 | Charlie       | 136****5432 | APAC   | 520.00 | 2025-01-17 09:30:00
```

**support_user** — all rows, phone visible:

```sql
-- Connect as support_user
SET ROLE support_global;
SELECT * FROM ecommerce.orders;
```

```
order_id | customer_name | phone       | region | amount | created_at
---------|---------------|-------------|--------|--------|--------------------
       1 | Alice         | 13812345678 | APAC   | 299.00 | 2025-01-15 10:00:00
       2 | Bob           | 14987654321 | EMEA   | 150.00 | 2025-01-16 11:00:00
       3 | Charlie       | 13698765432 | APAC   | 520.00 | 2025-01-17 09:30:00
       4 | Diana         | 15012349876 | AMER   | 89.00  | 2025-01-18 14:00:00
```

**sec_user** — no SELECT privilege, access denied:

```sql
-- Connect as sec_user
SET ROLE security_admin;
SELECT * FROM ecommerce.orders;
-- ERROR: Permission denied
```

### Step 11: Revoke Role Access

Because table privileges were granted to roles, removing the role from a user removes the user's table access without changing table grants.

```sql
-- Run as account_admin
REVOKE ROLE analyst_apac FROM USER 'analyst_user';

-- Start a new session as analyst_user
SELECT * FROM ecommerce.orders;
-- ERROR: Permission denied
```

### Privilege Flow

```
account_admin
  │
  ├─ GRANT CREATE MASKING POLICY ON *.* ─────────► security_admin
  ├─ GRANT CREATE ROW ACCESS POLICY ON *.* ─────► security_admin
  ├─ GRANT GRANT ON *.* ────────────────────────► security_admin
  └─ GRANT CREATE DATABASE ON *.* ──────────────► data_engineer
                                                     │
security_admin                                       │
  │ (owns policies via auto-OWNERSHIP)               │
  ├─ GRANT APPLY ON MASKING POLICY ─────────────► data_engineer
  └─ GRANT APPLY ON ROW ACCESS POLICY ─────────► data_engineer
                                                     │
data_engineer                                        │
  │ (owns table via auto-OWNERSHIP)                  │
  │ (has APPLY on policies)                          │
  ├─ ALTER TABLE ... SET MASKING POLICY              │
  └─ ALTER TABLE ... ADD ROW ACCESS POLICY           │
                                                     │
account_admin                                        │
  ├─ GRANT SELECT ON ecommerce.orders ─────────► analyst_apac ──► analyst_user
  ├─ GRANT SELECT ON ecommerce.orders ─────────► support_global ─► support_user
  └─ REVOKE ROLE analyst_apac FROM USER ───────► analyst_user loses access
```

### Key Takeaways

- **Separation of duties**: the role that creates policies (`security_admin`) cannot query data; the role that queries data (`analyst_apac`) cannot modify policies.
- **Least privilege**: attaching a policy requires BOTH `APPLY` on the policy AND `ALTER` on the table — neither alone is sufficient.
- **Masking and row access are independent**: masking alone hides column values but does not remove rows; adding row access policy filters rows before masking is applied.
- **Grant table access through roles**: users query through roles such as `analyst_apac`; revoking the role from a user removes access without changing table grants.
- **Ownership is automatic**: the creator's role receives OWNERSHIP on the new policy/table. No extra GRANT needed.
- **CREATE privileges go to roles, not users**: `CREATE MASKING POLICY` and `CREATE ROW ACCESS POLICY` cannot be granted directly to users.
- **Audit your setup**: use `SHOW GRANTS ON MASKING POLICY mask_phone`, `SHOW GRANTS ON ROW ACCESS POLICY rap_region`, and `POLICY_REFERENCES(POLICY_NAME => 'mask_phone')` to verify who has access and where policies are attached.

## Next Steps

- [Masking Policy](/tidb-cloud-lake/guides/masking-policy.md) — full syntax, conditional masking, VARIANT sub-field masking
- [Row Access Policy](/tidb-cloud-lake/guides/row-access-policy.md) — full syntax, DML behavior, multi-argument policies, time-range examples
