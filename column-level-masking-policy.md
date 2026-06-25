---
title: Column-Level Masking Policy
summary: This document describes how to use column-level masking policies to protect sensitive data in TiDB.
---

# Column-Level Masking Policy

In TiDB, column-level masking policy is a security feature that lets you create masking rules for specific table columns to protect sensitive data. When a masking policy is applied to a column, TiDB automatically masks the query result data returned to users according to the defined rules, while the original data remains unchanged in storage.

Column-level masking policies are suitable for scenarios where you need to restrict the visibility of sensitive data, such as credit card numbers, personal IDs, phone numbers, email addresses, and birth dates. This feature also helps meet compliance requirements such as Payment Card Industry Data Security Standard (PCI-DSS), and data privacy regulations such as General Data Protection Regulation (GDPR) and California Consumer Privacy Act (CCPA), which require access control for sensitive data.

## Overview

You can bind a masking policy to a single column in a table. Each column can have at most one masking policy. A policy expression typically uses a `CASE WHEN` SQL expression together with `CURRENT_USER()` or `CURRENT_ROLE()` to determine whether you can view the original value in the current session.

Key characteristics:

- **At-result masking**: TiDB applies masking logic when returning query results to the client, without modifying the original data.
- **User- or role-based visibility control**: different users or roles can view different levels of data based on their privileges.
- **Expression-based masking**: you can use `CASE WHEN` SQL expressions to define flexible masking logic.
- **Built-in masking functions**: TiDB provides built-in masking functions for common masking patterns, such as full masking, partial masking, returning `NULL`, and date replacement.
- **Operation restrictions**: you can use `RESTRICT ON` to prevent certain statements from copying or writing masked data to other tables.

## Privileges required

To manage masking policies, users need the following dynamic privileges (users with the `SUPER` privilege can also perform these operations):

| Privilege | Description |
|-----------|-------------|
| `CREATE MASKING POLICY` | Creates new masking policies |
| `ALTER MASKING POLICY` | Modifies existing policies, such as enabling or disabling a policy or changing an expression |
| `DROP MASKING POLICY` | Deletes masking policies |

You can grant these privileges by using the `GRANT` statement:

```sql
GRANT CREATE MASKING POLICY ON *.* TO 'security_admin'@'%';
GRANT ALTER MASKING POLICY ON *.* TO 'security_admin'@'%';
GRANT DROP MASKING POLICY ON *.* TO 'security_admin'@'%';
```

## Create a masking policy

### Basic syntax

```sql
CREATE [OR REPLACE] MASKING POLICY [IF NOT EXISTS] <policy_name>
  ON <table_name> (<column_name>)
  AS <masking_expression>
  [RESTRICT ON <operation_list>]
  [ENABLE | DISABLE];
```

Parameter descriptions:

- `policy_name`: the name of the masking policy, which must be unique within the table.
- `table_name`: the name of the table that contains the column to be masked.
- `column_name`: the name of the column to which the masking policy to be applied.
- `masking_expression`: A SQL expression that defines the masking logic.
- `RESTRICT ON`: optional. It blocks users who can only view the masked value of the column from performing certain operations. For example, it blocks such users from writing data from the column to other tables through statements such as `INSERT ... SELECT` and `CREATE TABLE ... AS SELECT`, which helps prevent masking policies from being bypassed.
- `ENABLE | DISABLE`: optional. It specifies whether the policy is enabled immediately after it is created. The default value is `ENABLE`.

### Example: Mask credit card numbers based on user identity

```sql
-- Create a table that contains sensitive data
CREATE TABLE customers (id INT PRIMARY KEY, name VARCHAR(100), email VARCHAR(100), credit_card VARCHAR(20));
INSERT INTO customers VALUES (1, 'Alice', 'alice@example.com', '4532111111111111');

-- Create a masking policy that shows full credit card numbers only to specific users
CREATE MASKING POLICY cc_mask_policy ON customers(credit_card)
  AS CASE
      WHEN CURRENT_USER() IN ('root@%', 'admin@%')
        THEN credit_card
      ELSE MASK_PARTIAL(credit_card, 4, 4, '*')
    END
  ENABLE;
```

After this policy is applied:

- Users `root@%` and `admin@%` can view the full credit card number: `4532111111111111`
- Other users can only view the masked credit card number: `4532********1111`

## Built-in masking functions

TiDB provides the following built-in functions for common data masking patterns:

- `MASK_PARTIAL()`
- `MASK_FULL()`
- `MASK_NULL()`
- `MASK_DATE()`

### MASK_PARTIAL

`MASK_PARTIAL()` masks part of a string.

**Syntax**

```sql
MASK_PARTIAL(column, preserve_left, preserve_right, mask_char)
```

Parameter descriptions:

- `column`: the string column to be masked.
- `preserve_left`: the number of characters to preserve at the beginning of the string.
- `preserve_right`: the number of characters to preserve at the end of the string.
- `mask_char`: the masking character, such as `'*'` or `'X'`.

**Logic and data types**

- **Logic**: masks the middle portion of a string while preserving the specified number of characters at the beginning and end, which provides granular control for partial masking of string data.
- **Types**: `VARCHAR`, `CHAR`, `TEXT` and its variants, and `BLOB` and its variants.

**Use cases and examples**

- **Use cases**: masks the middle digits or characters of a credit card number, phone number, or email address while preserving identifying characters at both ends.

```sql
-- Credit card: show the first 4 and last 4 digits
MASK_PARTIAL(credit_card, 4, 4, '*')
-- Input:  '4532111111111111'
-- Result: '4532********1111'

-- Phone: show the first 3 and last 4 digits
MASK_PARTIAL(phone, 3, 4, '*')
-- Input:  '13812345678'
-- Result: '138****5678'

-- Email: show the first character and domain
MASK_PARTIAL(email, 1, 12, '*')
-- Input:  'alice@example.com'
-- Result: 'a****@example.com'

-- SSN: show the first 3 and last 4 digits
MASK_PARTIAL(ssn, 3, 4, '*')
-- Input:  '123456789'
-- Result: '123**6789'
```

### MASK_FULL

`MASK_FULL()` fully masks a value.

**Syntax**

```sql
MASK_FULL(column)
```

**Logic and data types**

- **Logic**: replaces the entire value with a type-specific default masked value.
- **Types**: strings, `DATE`/`DATETIME`/`TIMESTAMP`, `Duration`, and `YEAR`.
- **Return rules**:
    - **Strings**: returns a string of the same length, with all characters replaced by `'X'`.
    - **`DATE`/`DATETIME`/`TIMESTAMP`**: returns `1970-01-01`, preserving the original type and fractional seconds precision.
    - **`Duration`**: returns `00:00:00`.
    - **`YEAR`**: returns `1970`.

**Use cases and examples**

- **Use cases**: completely hides sensitive IDs, phone numbers, or entire date values.

```sql
-- String: replace all characters with 'X'
MASK_FULL(customer_id)
-- Input:  'CUST12345'
-- Result: 'XXXXXXXXX'

-- String: hide an email address completely
MASK_FULL(email)
-- Input:  'alice@example.com'
-- Result: 'XXXXXXXXXXXXXXXX'

-- Date: replace with the default date
MASK_FULL(birth_date)
-- Input:  '1985-03-15'
-- Result: '1970-01-01'
```

### MASK_NULL

`MASK_NULL()` masks a value as `NULL`.

**Syntax**

```sql
MASK_NULL(column)
```

**Logic and data types**

- **Logic**: the most restrictive masking method. It always returns a literal `NULL` while preserving the column metadata.
- **Types**: [all supported column types](/column-level-masking-policy.md#supported-column-types), including strings, date and time types, and numeric types.

**Use cases and examples**

- **Use cases**: completely hides salaries, secret keys, or other highly sensitive data for which no partial disclosure is acceptable.

```sql
-- Hide salary completely
MASK_NULL(salary)
-- Input:  85000.00
-- Result: NULL

-- Hide an API key
MASK_NULL(api_key)
-- Input:  'sk_live_1234567890abcdef'
-- Result: NULL
```

### MASK_DATE

`MASK_DATE()` replaces a date or time value with a specific date literal.

**Syntax**

```sql
MASK_DATE(column, date_literal)
```

Parameter descriptions:

- `column`: the column to be masked.
- `date_literal`: the date used to replace the original value, in the `'YYYY-MM-DD'` format. The year, month, and day components can be preserved or fixed for masking purposes.

**Logic and data types**

- **Logic**: a type-aware operator for partially masking date components. It replaces the date with the specific literal while preserving the original column type.
- **Types**: `DATE`, `DATETIME`, and `TIMESTAMP`.
- **Return rules**:
    - For `DATE`, it returns the specified date.
    - For `DATETIME` or `TIMESTAMP`, it returns the specified date at midnight, that is, `YYYY-MM-DD 00:00:00`, while preserving the original type and fractional seconds precision.

**Use cases and examples**

- **Use cases**: preserves the year for trend analysis, or replaces birth dates with a fixed date, such as January 1.

```sql
-- Preserve only the year by setting the date to January 1
MASK_DATE(birth_date, '1985-01-01')
-- Input:  '1985-03-15'
-- Result: '1985-01-01'

-- Preserve the year and replace the month and day with fixed values
MASK_DATE(hire_date, '2020-01-01')
-- Input:  '2020-06-15'
-- Result: '2020-01-01'

-- For DATETIME, preserve the type but reset the time
MASK_DATE(created_at, '2020-01-01')
-- Input:  '2020-06-15 14:30:45'
-- Result: '2020-01-01 00:00:00'
```

**Complete example:**

```sql
-- Mask date of birth to show only the year
CREATE MASKING POLICY dob_mask ON customers(dob)
  AS CASE
      WHEN CURRENT_USER() = 'hr_admin@%' THEN dob
      ELSE MASK_DATE(dob, '1985-01-01')
    END
  ENABLE;
```

## Conditional masking based on users and roles

### Use CURRENT_USER()

You can use `CURRENT_USER()` in a masking expression to check the user account for the current session.

```sql
CREATE MASKING POLICY email_mask ON customers(email)
  AS CASE
      WHEN CURRENT_USER() = 'support_user@%' THEN email
      ELSE MASK_PARTIAL(email, 1, 7, '*')
    END
  ENABLE;
```

### Use CURRENT_ROLE()

For role-based access control, use `CURRENT_ROLE()`:

```sql
-- Create a role for users who can view unmasked data
CREATE ROLE data_viewer;

-- Create a masking policy based on the role
CREATE MASKING POLICY ssn_mask ON employees(ssn)
  AS CASE
      WHEN CURRENT_ROLE() = '`data_viewer`@`%`' THEN ssn
      ELSE MASK_PARTIAL(ssn, 3, 4, '*')
    END
  ENABLE;

-- Grant the role to authorized users
GRANT data_viewer TO 'analyst'@'%';

-- You must activate the role of users before they can view unmasked data based on the role condition
SET ROLE data_viewer;
```

> **Note:**
>
> `CURRENT_USER()` and `CURRENT_ROLE()` return values in different formats. This behavior is not a bug and is consistent with MySQL. For more information, see [#67227](https://github.com/pingcap/tidb/issues/67227).
>
> - `CURRENT_USER()` usually returns `'user_name@host_name'`, such as `'analyst@%'`.
> - `CURRENT_ROLE()` returns the currently active role, usually in a format that contains backticks, such as ``'`data_viewer`@`%`'``. If no role is active, it returns `'NONE'`.

## `RESTRICT ON` semantics

The `RESTRICT ON` clause lets you control whether masked data can be used in certain operations. With this clause, you can prevent users who can only view masked values from copying or using protected column data through specific SQL operations, helping avoid sensitive data leakage.

### Supported operations

| Operation | Description |
|-----------|-------------|
| `INSERT_INTO_SELECT` | Blocks inserting data from a protected column into another table through `INSERT ... SELECT` |
| `UPDATE_SELECT` | Blocks using data from a protected column to update another table through `UPDATE ... SET ... = (SELECT ...)` |
| `DELETE_SELECT` | Blocks using data from a protected column as a condition for deleting data through `DELETE ... WHERE ... (SELECT ...)` |
| `CTAS` | Blocks using data from a protected column to create a new table through `CREATE TABLE ... AS SELECT` |
| `NONE` | Does not restrict the preceding operations. This is the default value |

### Example: Use RESTRICT ON

```sql
-- Create a policy with restrictions
CREATE MASKING POLICY sensitive_mask ON sensitive_data(value)
  AS CASE
      WHEN CURRENT_USER() = 'admin@%' THEN value
      ELSE MASK_FULL(value)
    END
  RESTRICT ON (INSERT_INTO_SELECT, UPDATE_SELECT, DELETE_SELECT)
  ENABLE;

-- TiDB returns an error when regular users try the following operations:
-- 1. Copy data from the protected column to another table
INSERT INTO other_table SELECT value FROM sensitive_data;  -- Error

-- 2. Update another table by using data from the protected column
UPDATE some_table SET x = (SELECT value FROM sensitive_data);  -- Error

-- 3. Use data from the protected column as a deletion condition
DELETE FROM some_table WHERE x IN (SELECT value FROM sensitive_data);  -- Error
```

## Manage masking policies

### View masking policies

Use `SHOW MASKING POLICIES` to view policies on a table:

```sql
-- Show all masking policies on a specified table
SHOW MASKING POLICIES FOR customers;

-- Show the policy on a specific column
SHOW MASKING POLICIES FOR customers WHERE column_name = 'credit_card';

-- Show the table creation statement, including masking policy information
SHOW CREATE TABLE customers;
```

### Enable or disable a policy

```sql
-- Temporarily disable a policy
ALTER TABLE customers DISABLE MASKING POLICY cc_mask_policy;

-- Re-enable a disabled policy
ALTER TABLE customers ENABLE MASKING POLICY cc_mask_policy;
```

### Modify a policy expression

```sql
-- Change the masking expression
ALTER TABLE customers MODIFY MASKING POLICY cc_mask_policy
  SET EXPRESSION = CASE
                    WHEN CURRENT_USER() IN ('root@%', 'manager@%')
                      THEN credit_card
                    ELSE MASK_PARTIAL(credit_card, 4, 4, 'X')
                  END;
```

### Modify RESTRICT ON settings

```sql
-- Add restrictions to a policy
ALTER TABLE customers MODIFY MASKING POLICY cc_mask_policy
  SET RESTRICT ON (INSERT_INTO_SELECT, UPDATE_SELECT, DELETE_SELECT);

-- Remove all restrictions
ALTER TABLE customers MODIFY MASKING POLICY cc_mask_policy
  SET RESTRICT ON NONE;
```

### Drop a masking policy

```sql
-- Drop a masking policy from a column
ALTER TABLE customers DROP MASKING POLICY cc_mask_policy;
```

## Use CREATE OR REPLACE

To create a policy or replace an existing policy, use `CREATE OR REPLACE MASKING POLICY`:

```sql
-- Create or replace a policy with new rules
CREATE OR REPLACE MASKING POLICY email_mask ON customers(email)
  AS CASE
      WHEN CURRENT_USER() IN ('admin@%', 'support@%') THEN email
      ELSE MASK_PARTIAL(email, 1, 7, '*')
    END
  ENABLE;
```

If a policy with the same name already exists, TiDB replaces the original policy with the new definition.

## Behavior considerations

### At-result masking

TiDB applies masking policies at the phase of returning query results, which means:

1. **Original data in storage remains unchanged**: masking policies do not modify values stored in tables.
2. **Query processing uses original values**: operations such as `JOIN`, `WHERE`, `GROUP BY`, `HAVING`, and `ORDER BY` still use the original values for calculation.
3. **Only query results are masked**: before returning final results to the client, TiDB masks column values or returned expression results that reference the column according to the policy expression.

It is important to understand how it works:

```sql
-- Create a masked email column
CREATE MASKING POLICY email_mask ON users(email)
  AS CASE
      WHEN CURRENT_USER() = 'admin@%' THEN email
      ELSE MASK_FULL(email)
    END
  ENABLE;

-- Filtering still works even if the user enters the unmasked data in the WHERE condition
SELECT * FROM users WHERE email = 'user@example.com';
-- This statement returns the row even though the displayed email address is masked
```

### Supported column types

Masking policies support the following column types:

- **String types**: `VARCHAR`, `CHAR`, `TEXT`, and their variants.
- **Binary types**: `BINARY`, `VARBINARY`, and `BLOB`.
- **Date and time types**: `DATE`, `TIME`, `DATETIME`, `TIMESTAMP`, and `YEAR`.

For `LONGTEXT` and large `BLOB` types, TiDB only supports full masking with `MASK_FULL()` and returning `NULL` with `MASK_NULL()`.

### Limitations

You cannot create masking policies on the following objects or in the following scenarios:

- Views
- Generated columns
- Temporary tables
- System tables

In addition, if a masking policy exists on a column, TiDB blocks changes to the column type, length, or precision. To modify the column definition, drop the masking policy on the column first, and then recreate the policy after the column change is complete.

TiDB does not support creating masking policies directly on views. However, if a view references a column from a base table that already has a masking policy, the masking policy on the base table still applies when you query the column through the view.

### Cascade behavior

When you drop a column or table that has a masking policy, TiDB also drops the masking policies related to the column or table. When you rename a table or column, the masking policy remains bound to the renamed table or column.

## Complete example

The following example shows a typical workflow:

```sql
-- 1. Create the table
CREATE TABLE employees (
  id INT PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(100),
  salary DECIMAL(10,2),
  ssn VARCHAR(11)
);

INSERT INTO employees VALUES
  (1, 'John Doe', 'john.doe@company.com', 75000.00, '123456789'),
  (2, 'Jane Smith', 'jane.smith@company.com', 85000.00, '987654321');

-- 2. Create users
CREATE USER hr_admin;
CREATE USER hr_viewer;
CREATE USER regular_user;

GRANT SELECT ON employees TO hr_admin, hr_viewer, regular_user;

-- 3. Create roles
CREATE ROLE salary_access;

-- 4. Create masking policies
-- Email: show to HR staff, and partially show to others
CREATE MASKING POLICY email_policy ON employees(email)
  AS CASE
      WHEN CURRENT_USER() IN ('hr_admin@%', 'hr_viewer@%') THEN email
      ELSE MASK_PARTIAL(email, 1, 7, '*')
    END
  ENABLE;

-- Salary: show only to users with the salary_access role
CREATE MASKING POLICY salary_policy ON employees(salary)
  AS CASE
      WHEN CURRENT_ROLE() = 'salary_access' THEN salary
      ELSE NULL
    END
  ENABLE;

-- SSN: use strict masking and restrict copy operations
CREATE MASKING POLICY ssn_policy ON employees(ssn)
  AS CASE
      WHEN CURRENT_USER() = 'hr_admin@%' THEN ssn
      ELSE MASK_PARTIAL(ssn, 3, 4, '*')
    END
  RESTRICT ON (INSERT_INTO_SELECT, UPDATE_SELECT)
  ENABLE;

-- 5. Grant the role
GRANT salary_access TO hr_admin;

-- 6. Test the policies
-- Connect as regular_user: masked data is displayed
-- Connect as hr_viewer: email addresses are visible, but salary is masked
-- Connect as hr_admin and use SET ROLE salary_access: all data is visible
```

## MySQL compatibility

Column-level masking policy is a TiDB-specific feature and is incompatible with MySQL. The related DDL syntax, built-in masking functions, and runtime behavior are TiDB extensions.

If you need to migrate or replicate tables with masking policies between TiDB clusters by using tools such as BR (Backup & Restore) or TiCDC, note the following:

1. Make sure that the TiDB version of the target cluster and the tool versions used for data replication, such as BR and TiCDC, support column-level masking policies.
2. Masking policy DDL statements are replicated to the target cluster, but user and role definitions must be created separately on the target cluster.
3. If a policy expression depends on `CURRENT_USER()` or `CURRENT_ROLE()`, the corresponding users or roles must exist on the target cluster. Otherwise, masking behavior might differ from that on the source cluster.

## See also

- [Role-Based Access Control](/role-based-access-control.md)
- [Privilege Management](/privilege-management.md)
- [User Account Management](/user-account-management.md)
