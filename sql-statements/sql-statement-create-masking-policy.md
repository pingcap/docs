---
title: CREATE MASKING POLICY
summary: An overview of the usage of CREATE MASKING POLICY for the TiDB database.
---

# CREATE MASKING POLICY

`CREATE MASKING POLICY` creates a [data masking policy](column-level-masking-policy.md) for columns in a table. After you enable a masking policy for a column, TiDB masks the results of that column according to the policy definition when returning query results, preventing sensitive data from being viewed by unauthorized users.

A masking policy is bound to a column in a table. You can use the `CURRENT_USER()` or `CURRENT_ROLE()` function in the masking expression to implement conditional masking based on the user identity or role.

## Required privileges

To create a masking policy, you must have the `CREATE MASKING POLICY` privilege on the database where the target table resides or have the `SUPER` privilege.

## Syntax diagram

```ebnf+diagram
CreateMaskingPolicyStmt ::=
    'CREATE' OrReplace 'MASKING' 'POLICY' IfNotExists PolicyName 'ON' TableName '(' Identifier ')' 'AS' Expression MaskingPolicyRestrictOnOpt MaskingPolicyStateOpt

PolicyName ::=
    Identifier

MaskingPolicyRestrictOnOpt ::=
    ( 'RESTRICT' 'ON' '(' MaskingPolicyRestrictOperationList ')' )?
|   'RESTRICT' 'ON' 'NONE'

MaskingPolicyRestrictOperationList ::=
    MaskingPolicyRestrictOperation ( ',' MaskingPolicyRestrictOperation )*

MaskingPolicyRestrictOperation ::=
    Identifier

MaskingPolicyStateOpt ::=
    ( 'ENABLE' | 'DISABLE' )?
```

## Syntax description

| Syntax element | Description |
| -------- | ---- |
| `PolicyName` | The name of the masking policy, which must be unique within the same table. |
| `TableName` | The name of the target table. |
| `Identifier` (in parentheses) | The name of the target column. Each column can be bound to at most one masking policy. |
| `Expression` | The masking expression. You can use built-in masking functions such as `MASK_FULL`, `MASK_PARTIAL`, `MASK_NULL`, and `MASK_DATE`, or use a custom expression containing `CURRENT_USER()` or `CURRENT_ROLE()` to implement identity-based conditional masking. |
| `RESTRICT ON (...)` | Optional. Restricts specific operations on the masked column to prevent the original data from being obtained indirectly through these operations. The operations that can be restricted include `INSERT INTO SELECT`, `UPDATE SELECT`, `DELETE SELECT`, and `CTAS`. |
| `ENABLE` \| `DISABLE` | Optional. Specifies whether the policy is enabled immediately after creation. The default is `ENABLE`. |

### Built-in masking functions

| Function | Description | Example |
| ---- | ---- | ---- |
| `MASK_FULL(col)` | Full masking. Replaces the column value with fixed-length masking characters. | `MASK_FULL(ssn)` → `'XXXXXXXXX'` |
| `MASK_PARTIAL(col, prefix_len, suffix_len, mask_char)` | Partial masking. Preserves the first `prefix_len` characters and the last `suffix_len` characters of the column value, and replaces the middle part with `mask_char`. | `MASK_PARTIAL(phone, 3, 3, '*')` → `'123****890'` |
| `MASK_NULL(col)` | Null masking. Replaces the column value with `NULL`. | `MASK_NULL(salary)` → `NULL` |
| `MASK_DATE(col, date_literal)` | Date masking. Replaces the date column value with a fixed date literal. | `MASK_DATE(birth_date, '1970-01-01')` → `'1970-01-01'` |

## Examples

### Create a partial masking policy

The following example creates a masking policy that partially masks the `phone` column in the `contacts` table, preserving the first 3 characters and the last 3 characters, and replacing the rest with `*`:

```sql
CREATE TABLE contacts (
  id INT PRIMARY KEY,
  name VARCHAR(100),
  phone VARCHAR(20)
);

CREATE MASKING POLICY p_mask_phone
  ON contacts(phone)
  AS MASK_PARTIAL(phone, 3, 3, '*') ENABLE;
```

```
Query OK, 0 rows affected (0.10 sec)
```

Insert data and query it:

```sql
INSERT INTO contacts VALUES (1, 'Alice', '1234567890');
SELECT phone FROM contacts WHERE id = 1;
```

```
Query OK, 1 row affected (0.01 sec)

+-------------+
| phone       |
+-------------+
| 123****890  |
+-------------+
1 row in set (0.00 sec)
```

### Create a full masking policy

The following example creates a masking policy that fully masks the `ssn` column in the `employees` table:

```sql
CREATE MASKING POLICY p_mask_ssn
  ON employees(ssn)
  AS MASK_FULL(ssn) ENABLE;
```

### Create a masking policy with operation restrictions

The following example creates a masking policy that restricts `INSERT INTO SELECT` and `CTAS` operations on the masked column:

```sql
CREATE MASKING POLICY p_mask_credit_card
  ON users(credit_card)
  AS MASK_FULL(credit_card)
  RESTRICT ON (INSERT INTO SELECT, CTAS) ENABLE;
```

### Create a conditional masking policy

The following example creates a role-based conditional masking policy. Only users with the `hr_manager` or `ceo` role can view the original data, while other users can only view masked results:

```sql
CREATE MASKING POLICY p_mask_salary
  ON employees(salary)
  AS IF(CURRENT_ROLE() IN ('hr_manager', 'ceo'), salary, MASK_NULL(salary)) ENABLE;
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [ALTER TABLE](/sql-statements/sql-statement-alter-table.md)
* [SHOW MASKING POLICIES](/sql-statements/sql-statement-show-masking-policies.md)