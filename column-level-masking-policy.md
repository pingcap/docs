---
title: Column-Level Masking Policy
summary: This document introduces how to use column-level masking policies to protect sensitive data in TiDB.
aliases: ['/docs/dev/column-level-masking-policy/']
---

# Column-Level Masking Policy

Column-level masking policy is a security feature that allows you to protect sensitive data by applying masking rules at the column level. When a masking policy is applied to a column, TiDB automatically masks the data returned to users based on the defined rules, while the original data remains unchanged in storage.

This feature is particularly useful for compliance requirements such as PCI-DSS (Payment Card Industry Data Security Standard) and data privacy regulations (e.g., GDPR - General Data Protection Regulation, CCPA - California Consumer Privacy Act) that require strict control over who can view sensitive information like credit card numbers, personal identifiers, and other confidential data.

## Overview

A masking policy is bound to a table column and evaluated at query result time. The policy uses SQL expressions to determine how to mask the data based on the current user's identity or role.

Key characteristics:

- **At-result masking**: Data is masked when returned to the client, not stored in masked form
- **Role/user-aware**: Different users can see different levels of data based on their privileges
- **Flexible expressions**: Use SQL `CASE WHEN` expressions to define complex masking logic
- **Built-in functions**: Pre-defined functions for common masking patterns
- **Optional restrictions**: Control whether masked data can be used in certain operations

## Privileges required

To manage masking policies, users need the following dynamic privileges:

| Privilege | Description |
|-----------|-------------|
| `CREATE MASKING POLICY` | Create new masking policies |
| `ALTER MASKING POLICY` | Modify existing policies (enable/disable, change expression, etc.) |
| `DROP MASKING POLICY` | Remove masking policies |

These privileges can be granted using the `GRANT` statement:

{{< copyable "sql" >}}

```sql
GRANT CREATE MASKING POLICY ON *.* TO 'security_admin'@'%';
GRANT ALTER MASKING POLICY ON *.* TO 'security_admin'@'%';
GRANT DROP MASKING POLICY ON *.* TO 'security_admin'@'%';
```

## Create a masking policy

### Basic syntax

{{< copyable "sql" >}}

```sql
CREATE [OR REPLACE] MASKING POLICY [IF NOT EXISTS] <policy_name>
  ON <table_name> (<column_name>)
  AS <masking_expression>
  [RESTRICT ON <operation_list>]
  [ENABLE | DISABLE];
```

Parameters:

- `policy_name`: The name of the masking policy (must be unique within the table)
- `table_name`: The name of the table containing the column to mask
- `column_name`: The name of the column to apply the masking policy to
- `masking_expression`: A SQL expression that defines the masking logic
- `RESTRICT ON`: Optional. Specifies operations that should be blocked for users without access to unmasked data
- `ENABLE | DISABLE`: Optional. Whether the policy is active. Default is `ENABLE`.

### Example: Mask based on user identity

{{< copyable "sql" >}}

```sql
-- Create a table with sensitive data
CREATE TABLE customers (id INT PRIMARY KEY, name VARCHAR(100), email VARCHAR(100), credit_card VARCHAR(20));
INSERT INTO customers VALUES (1, 'Alice', 'alice@example.com', '4532111111111111');

-- Create a masking policy that shows full credit card numbers only to specific users
CREATE MASKING POLICY cc_mask_policy ON customers(credit_card)
  AS CASE
      WHEN current_user() IN ('root@%', 'admin@%')
        THEN credit_card
      ELSE MASK_PARTIAL(credit_card, 4, 4, '*')
    END
  ENABLE;
```

With this policy:
- Users `root@%` and `admin@%` see the full credit card number: `4532111111111111`
- Other users see a masked version: `4532********1111`

## Built-in masking functions

TiDB provides four built-in functions for common data masking patterns:

### MASK_PARTIAL

**Function & Syntax**

```sql
MASK_PARTIAL(column, preserve_left, preserve_right, mask_char)
```

**Logic & Data Types**

- **Logic**: Provides granular control for partial redaction of string data by masking the middle portion while preserving specified numbers of characters at the beginning and end.
- **Types**: VARCHAR, CHAR, TEXT family, BLOB family

**Use Case & Example**

- **Case**: Masking middle digits of a credit card, phone number, or email while preserving identifying characters at both ends.

{{< copyable "sql" >}}

```sql
-- Credit card: show first 4 and last 4 digits
MASK_PARTIAL(credit_card, 4, 4, '*')
-- Input:  '4532111111111111'
-- Result: '4532********1111'

-- Phone: show first 3 and last 4 digits
MASK_PARTIAL(phone, 3, 4, '*')
-- Input:  '13812345678'
-- Result: '138****5678'

-- Email: show first character and domain
MASK_PARTIAL(email, 1, 7, '*')
-- Input:  'alice@example.com'
-- Result: 'a********e.com'

-- SSN: show first 3 and last 4 digits
MASK_PARTIAL(ssn, 3, 4, '*')
-- Input:  '123456789'
-- Result: '123**6789'
```

### MASK_FULL

**Function & Syntax**

```sql
MASK_FULL(column)
```

**Logic & Data Types**

- **Logic**: Replaces the entire value with a type-specific default mask character.
- **Types**: String, Date/DATETIME/TIMESTAMP, Duration, YEAR
  - **String** → Returns a string of the same length with all characters replaced by `'X'`
  - **Date/DATETIME/TIMESTAMP** → Returns `1970-01-01` (preserving original type and fractional seconds precision)
  - **Duration** → Returns `00:00:00`
  - **YEAR** → Returns `1970`

**Use Case & Example**

- **Case**: Hiding sensitive IDs, phone numbers, or entire date values completely.

{{< copyable "sql" >}}

```sql
-- String: Replace all characters with 'X'
MASK_FULL(customer_id)
-- Input:  'CUST12345'
-- Result: 'XXXXXXXXX'

-- String: Hide email completely
MASK_FULL(email)
-- Input:  'alice@example.com'
-- Result:  'XXXXXXXXXXXXXXXX'

-- Date: Replace with default date
MASK_FULL(birth_date)
-- Input:  '1985-03-15'
-- Result: '1970-01-01'
```

### MASK_NULL

**Function & Syntax**

```sql
MASK_NULL(column)
```

**Logic & Data Types**

- **Logic**: The most restrictive method; always returns a literal NULL while maintaining column metadata.
- **Types**: All supported types (String, Date/Time, Numeric)

**Use Case & Example**

- **Case**: Completely hiding salary, secret keys, or other highly sensitive data where no partial disclosure is acceptable.

{{< copyable "sql" >}}

```sql
-- Hide salary completely
MASK_NULL(salary)
-- Input:  85000.00
-- Result: NULL

-- Hide API key
MASK_NULL(api_key)
-- Input:  'sk_live_1234567890abcdef'
-- Result: NULL
```

### MASK_DATE

**Function & Syntax**

```sql
MASK_DATE(column, date_literal)
```

**Logic & Data Types**

- **Logic**: Type-aware operator for partial redaction of date components. Replaces the date with a specified literal while preserving the original column type.
- **Types**: DATE, DATETIME, TIMESTAMP
- **Placeholders**: The `date_literal` follows format `'YYYY-MM-DD'` where Y/M/D components can be preserved or fixed values for redaction
- **Time Component**: Hours, minutes, and seconds are reset to `00:00:00`

**Use Case & Example**

- **Case**: Preserving year for trend analysis, or generalizing birth dates to a standard date (like January 1st).

{{< copyable "sql" >}}

```sql
-- Preserve only year (set to January 1st)
MASK_DATE(birth_date, '1985-01-01')
-- Input:  '1985-03-15'
-- Result: '1985-01-01'

-- Preserve year, generalize month and day
MASK_DATE(hire_date, '2020-01-01')
-- Input:  '2020-06-15'
-- Result: '2020-01-01'

-- For DATETIME, preserves type but resets time
MASK_DATE(created_at, '2020-01-01')
-- Input:  '2020-06-15 14:30:45'
-- Result: '2020-01-01 00:00:00'
```

**Complete example:**

{{< copyable "sql" >}}

```sql
-- Mask date of birth to show only the year
CREATE MASKING POLICY dob_mask ON customers(dob)
  AS CASE
      WHEN current_user() = 'hr_admin@%' THEN dob
      ELSE MASK_DATE(dob, '1985-01-01')
    END
  ENABLE;
```

## Conditional masking with users and roles

### Using current_user()

You can use `current_user()` in your masking expression to check the logged-in user:

{{< copyable "sql" >}}

```sql
CREATE MASKING POLICY email_mask ON customers(email)
  AS CASE
      WHEN current_user() = 'support_user@%' THEN email
      ELSE MASK_PARTIAL(email, 1, 7, '*')
    END
  ENABLE;
```

### Using current_role()

For role-based access control, use `current_role()`:

{{< copyable "sql" >}}

```sql
-- Create a role for users who can see unmasked data
CREATE ROLE data_viewer;

-- Create a masking policy based on role
CREATE MASKING POLICY ssn_mask ON customers(ssn)
  AS CASE
      WHEN current_role() = 'data_viewer@%' THEN ssn
      ELSE MASK_PARTIAL(ssn, 3, 4, '*')
    END
  ENABLE;

-- Grant the role to authorized users
GRANT data_viewer TO 'analyst'@'%';

-- Users must activate the role to see unmasked data
SET ROLE data_viewer;
```

## RESTRICT ON semantics

The `RESTRICT ON` clause allows you to control whether masked data can be used in certain operations. This provides additional security by preventing data exfiltration through specific SQL operations.

### Supported operations

| Operation | Description |
|-----------|-------------|
| `INSERT_INTO_SELECT` | Blocks inserting masked data into another table via `INSERT ... SELECT` |
| `UPDATE_SELECT` | Blocks updating with masked data via `UPDATE ... SET = (SELECT ...)` |
| `DELETE_SELECT` | Blocks deleting based on masked data via `DELETE ... WHERE ... IN (SELECT ...)` |
| `CTAS` | Blocks Create Table As Select with masked data |
| `NONE` | No restrictions (default) |

### Example: Using RESTRICT ON

{{< copyable "sql" >}}

```sql
-- Create a policy with restrictions
CREATE MASKING POLICY sensitive_mask ON sensitive_data(value)
  AS CASE
      WHEN current_user() = 'admin@%' THEN value
      ELSE MASK_FULL(value)
    END
  RESTRICT ON (INSERT_INTO_SELECT, UPDATE_SELECT, DELETE_SELECT)
  ENABLE;

-- Regular users will receive an error when attempting:
-- 1. Copy masked data to another table
INSERT INTO other_table SELECT value FROM sensitive_data;  -- Error

-- 2. Update using masked data
UPDATE some_table SET x = (SELECT value FROM sensitive_data);  -- Error

-- 3. Delete using masked data
DELETE FROM some_table WHERE x IN (SELECT value FROM sensitive_data);  -- Error
```

## Manage masking policies

### View masking policies

Use `SHOW MASKING POLICIES` to view policies on a table:

{{< copyable "sql" >}}

```sql
-- Show all masking policies for a table
SHOW MASKING POLICIES FOR customers;

-- Show policy for a specific column
SHOW MASKING POLICIES FOR customers WHERE column_name = 'credit_card';

-- Show table creation including masking policy info
SHOW CREATE TABLE customers;
```

### Enable or disable a policy

{{< copyable "sql" >}}

```sql
-- Disable a policy temporarily
ALTER TABLE customers DISABLE MASKING POLICY cc_mask_policy;

-- Re-enable a disabled policy
ALTER TABLE customers ENABLE MASKING POLICY cc_mask_policy;
```

### Modify a policy expression

{{< copyable "sql" >}}

```sql
-- Change the masking expression
ALTER TABLE customers MODIFY MASKING POLICY cc_mask_policy
  SET EXPRESSION = CASE
                    WHEN current_user() IN ('root@%', 'manager@%')
                      THEN credit_card
                    ELSE MASK_PARTIAL(credit_card, 4, 4, 'X')
                  END;
```

### Modify RESTRICT ON settings

{{< copyable "sql" >}}

```sql
-- Add restrictions to a policy
ALTER TABLE customers MODIFY MASKING POLICY cc_mask_policy
  SET RESTRICT ON (INSERT_INTO_SELECT, UPDATE_SELECT, DELETE_SELECT);

-- Remove all restrictions
ALTER TABLE customers MODIFY MASKING POLICY cc_mask_policy
  SET RESTRICT ON NONE;
```

### Drop a masking policy

{{< copyable "sql" >}}

```sql
-- Remove a masking policy from a column
ALTER TABLE customers DROP MASKING POLICY cc_mask_policy;
```

## Use CREATE OR REPLACE

To update an existing policy, use `CREATE OR REPLACE`:

{{< copyable "sql" >}}

```sql
-- Create or replace a policy with new rules
CREATE OR REPLACE MASKING POLICY email_mask ON customers(email)
  AS CASE
      WHEN current_user() IN ('admin@%', 'support@%') THEN email
      ELSE MASK_PARTIAL(email, 1, 7, '*')
    END
  ENABLE;
```

## Behavior considerations

### At-result masking

Masking policies are applied **at result time**, which means:

1. **Storage is unchanged**: The original data is stored without modification
2. **Query processing uses raw values**: Operations like `JOIN`, `WHERE`, `GROUP BY`, `HAVING`, `ORDER BY` all work with the original values
3. **Only output is masked**: The data returned to the client is masked according to the policy

This is important to understand:

{{< copyable "sql" >}}

```sql
-- Create a masked email column
CREATE MASKING POLICY email_mask ON users(email)
  AS CASE
      WHEN current_user() = 'admin@%' THEN email
      ELSE MASK_FULL(email)
    END
  ENABLE;

-- Even though the user sees masked data, filtering still works
SELECT * FROM users WHERE email = 'user@example.com';
-- This returns the row even though the email shown is masked
```

### Supported column types

Masking policies support the following column types:

- **String types**: `VARCHAR`, `CHAR`, `TEXT`, and their variants
- **Binary types**: `BINARY`, `VARBINARY`, `BLOB`
- **Date/time types**: `DATE`, `TIME`, `DATETIME`, `TIMESTAMP`, `YEAR`

For `LONGTEXT` and large `BLOB` types, only `MASK_FULL` and `MASK_NULL` are supported.

### Limitations

The following are **not supported**:

- Masking policies on views
- Masking policies on generated columns
- Masking policies on temporary tables
- Masking policies on system tables
- Modifying column type or length while a masking policy is active (drop the policy first)

### Cascade behavior

When you drop a column or table that has a masking policy, the policy is automatically removed from the system. When you rename a column or table, the masking policy remains bound to it.

## Complete example

Here's a complete example showing a typical workflow:

{{< copyable "sql" >}}

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
-- Email: show to HR staff, partial to others
CREATE MASKING POLICY email_policy ON employees(email)
  AS CASE
      WHEN current_user() IN ('hr_admin@%', 'hr_viewer@%') THEN email
      ELSE MASK_PARTIAL(email, 1, 7, '*')
    END
  ENABLE;

-- Salary: show only to those with the salary_access role
CREATE MASKING POLICY salary_policy ON employees(salary)
  AS CASE
      WHEN current_role() = 'salary_access' THEN salary
      ELSE NULL
    END
  ENABLE;

-- SSN: strict masking, restrict copy operations
CREATE MASKING POLICY ssn_policy ON employees(ssn)
  AS CASE
      WHEN current_user() = 'hr_admin@%' THEN ssn
      ELSE MASK_PARTIAL(ssn, 3, 4, '*')
    END
  RESTRICT ON (INSERT_INTO_SELECT, UPDATE_SELECT)
  ENABLE;

-- 5. Grant role
GRANT salary_access TO hr_admin;

-- 6. Test the policies
-- Connect as regular_user - sees masked data
-- Connect as hr_viewer - sees email but masked salary
-- Connect as hr_admin with SET ROLE salary_access - sees everything
```

## MySQL compatibility

Column-level masking policies are a TiDB-specific feature and are **not compatible with MySQL**. The syntax and behavior are unique to TiDB.

When using tools like BR (Backup & Restore) or TiCDC to replicate data:

1. Masking policy DDL statements are replicated
2. User and role definitions must be created separately on the target cluster
3. The target cluster must have the same users/roles for masking to work correctly

## See also

- [Role-Based Access Control](/role-based-access-control.md)
- [Privilege Management](/privilege-management.md)
- [User Account Management](/user-account-management.md)
