---
title: Masking Policies
summary: Learn how to use column masking policies in TiDB to control sensitive query results, manage masking rules, and restrict data copying.
---

# Masking Policies

Masking policies control how sensitive column values appear in query results. You can replace a value with a fully masked value, preserve selected characters, return `NULL`, or mask date components. A policy can use the current user or active roles to decide whether to return the original value.

<!-- TODO: Confirm the first TiDB release that includes masking policies. The source PRs target release-8.5. -->

Masking does not change stored data. TiDB applies policies when producing query results, while ordinary filtering, joins, grouping, and sorting use original values. Use masking policies to limit exposure of phone numbers, identifiers, and other sensitive fields in applications that share a database.

> **Warning**
>
> Masking policies do not replace access privileges or encrypt data. Users can still filter and sort by original values. By default, a policy does not prevent copying original values through write statements. To restrict these operations, configure [`RESTRICT ON`](#restrict-operations-that-read-protected-columns) and grant only the privileges each user needs.

## Prerequisites and privileges

Policies apply to columns in persistent base tables. Temporary tables, system tables, views, sequences, and generated columns cannot be policy targets. You can query a view over a table with masking policies; the policies on the underlying columns still apply.

To manage a policy, you need `ALTER` on the target table and the corresponding global [dynamic privilege](/privilege-management.md#dynamic-privileges):

| Operation | Dynamic privilege |
| --- | --- |
| Create a policy with `CREATE MASKING POLICY` or `ALTER TABLE ... ADD MASKING POLICY` | `CREATE MASKING POLICY` |
| Replace a policy with `CREATE OR REPLACE MASKING POLICY` | Both `CREATE MASKING POLICY` and `ALTER MASKING POLICY` |
| Change an expression or restrictions, or enable or disable a policy | `ALTER MASKING POLICY` |
| Drop a policy | `DROP MASKING POLICY` |

For example, grant policy management privileges to an existing administrator account:

```sql
GRANT CREATE MASKING POLICY ON *.* TO 'security_admin'@'%';
GRANT ALTER MASKING POLICY ON *.* TO 'security_admin'@'%';
GRANT DROP MASKING POLICY ON *.* TO 'security_admin'@'%';
GRANT ALTER ON app.contacts TO 'security_admin'@'%';
```

The `SUPER` privilege also satisfies these dynamic privilege checks. Policy management privileges do not exempt a user from masking when querying data. The policy expression determines which values the user sees. Ordinary query privileges, such as `SELECT`, are still required.

## Create and use a policy

The following example lets an auditor read full phone numbers and masks the middle digits for other users.

1. As an administrator, create a table and two accounts. Replace the password placeholders before running the statements.

    ```sql
    CREATE DATABASE masking_demo;
    CREATE TABLE masking_demo.contacts (
        id INT PRIMARY KEY,
        name VARCHAR(50),
        phone VARCHAR(20)
    );
    INSERT INTO masking_demo.contacts VALUES
        (1, 'Alice', '13812345678'),
        (2, 'Bob', '13987654321');

    CREATE USER 'masking_reader'@'%' IDENTIFIED BY '<reader-password>';
    CREATE USER 'masking_auditor'@'%' IDENTIFIED BY '<auditor-password>';
    GRANT SELECT ON masking_demo.contacts TO 'masking_reader'@'%';
    GRANT SELECT ON masking_demo.contacts TO 'masking_auditor'@'%';
    ```

2. Create a policy on the `phone` column:

    ```sql
    CREATE MASKING POLICY mask_phone
      ON masking_demo.contacts (phone)
      AS CASE
           WHEN CURRENT_USER() = 'masking_auditor@%' THEN phone
           ELSE MASK_PARTIAL(phone, 3, 4, '*')
         END
      RESTRICT ON (INSERT_INTO_SELECT, UPDATE_SELECT, DELETE_SELECT)
      ENABLE;
    ```

    `CURRENT_USER()` identifies the authenticated account, including its host component. Use the value returned by `SELECT CURRENT_USER()` for the account you want to exempt. This policy also masks results for administrators unless the expression explicitly exempts them.

3. Connect as `masking_reader` and query the protected column:

    ```sql
    SELECT id, phone
    FROM masking_demo.contacts
    ORDER BY id;
    ```

    ```text
    +----+-------------+
    | id | phone       |
    +----+-------------+
    |  1 | 138****5678 |
    |  2 | 139****4321 |
    +----+-------------+
    ```

    A predicate still matches the original phone number, while a result expression uses its masked value:

    ```sql
    SELECT phone, RIGHT(phone, 4) AS phone_suffix
    FROM masking_demo.contacts
    WHERE phone = '13812345678';
    ```

    ```text
    +-------------+--------------+
    | phone       | phone_suffix |
    +-------------+--------------+
    | 138****5678 | 5678         |
    +-------------+--------------+
    ```

4. Connect as `masking_auditor` and run the same queries. The `phone` column returns its original values, such as `13812345678`.

For role-based conditions, use [`CURRENT_ROLE()`](/functions-and-operators/information-functions.md#current_role) in the expression and activate the intended roles with [`SET ROLE`](/sql-statements/sql-statement-set-role.md). The function reports active roles, rather than all granted roles. Successful role changes take effect for subsequent queries, including prepared statements.

## Manage policies

### Create or replace a policy

```sql
CREATE [OR REPLACE] MASKING POLICY [IF NOT EXISTS] policy_name
  ON [database_name.]table_name (column_name)
  AS masking_expression
  [RESTRICT ON (operation [, operation] ...) | RESTRICT ON NONE]
  [ENABLE | DISABLE];
```

You can also create a policy using `ALTER TABLE`:

```sql
ALTER TABLE [database_name.]table_name
  ADD MASKING POLICY policy_name ON (column_name)
  AS masking_expression
  [RESTRICT ON (operation [, operation] ...) | RESTRICT ON NONE]
  [ENABLE | DISABLE];
```

The following rules apply:

- Each column can have at most one policy, including a disabled policy.
- Policy names are unique within a table. Different tables can use the same policy name.
- The expression can reference only the target column, constants, and functions. It cannot reference another column in the table.
- Policies are enabled by default. The default restriction setting is `NONE`.
- `OR REPLACE` replaces an existing policy with the same name on the same column. It cannot move that policy to another column.
- `IF NOT EXISTS` keeps an existing policy unchanged and reports a warning instead of a duplicate-policy error.
- `OR REPLACE` and `IF NOT EXISTS` are mutually exclusive and are available only with `CREATE MASKING POLICY`.

### Change a policy

Change the expression:

```sql
ALTER TABLE masking_demo.contacts
  MODIFY MASKING POLICY mask_phone
  SET EXPRESSION = CASE
    WHEN CURRENT_USER() = 'masking_auditor@%' THEN phone
    ELSE MASK_FULL(phone)
  END;
```

Change the restricted operations:

```sql
ALTER TABLE masking_demo.contacts
  MODIFY MASKING POLICY mask_phone
  SET RESTRICT ON (INSERT_INTO_SELECT, UPDATE_SELECT, DELETE_SELECT);
```

Remove the operation restrictions while keeping result masking enabled:

```sql
ALTER TABLE masking_demo.contacts
  MODIFY MASKING POLICY mask_phone SET RESTRICT ON NONE;
```

Disable or enable a policy:

```sql
ALTER TABLE masking_demo.contacts DISABLE MASKING POLICY mask_phone;
ALTER TABLE masking_demo.contacts ENABLE MASKING POLICY mask_phone;
```

Disabling a policy stops both its result masking and its operation restrictions. The definition remains available for inspection and re-enabling.

### Inspect or drop a policy

```sql
SHOW MASKING POLICIES FOR masking_demo.contacts;
SHOW MASKING POLICIES FOR masking_demo.contacts WHERE column_name = 'phone';
SHOW CREATE TABLE masking_demo.contacts;
```

`SHOW MASKING POLICIES` returns `Policy_name`, `Column_name`, `Expression`, `Status`, `Function_type`, and `Restrict_on`. `SHOW CREATE TABLE` adds a comment such as ``/* MASKING POLICY `mask_phone` ENABLED */`` to the protected column. This comment indicates the policy name and status; it does not contain the full definition or recreate the policy when you replay the table DDL.

To remove a policy:

```sql
ALTER TABLE masking_demo.contacts DROP MASKING POLICY mask_phone;
```

Dropping a policy stops its masking and restrictions. Dropping a protected column, table, or database removes the associated policies. Renaming a table or column preserves its policy binding and updates the stored names and column references. `TRUNCATE TABLE` preserves the policy for the truncated table.

## Masking functions

You can use the following functions in policies or call them directly in SQL. For valid arguments, `NULL` input returns `NULL`.

### `MASK_FULL(value)`

Replaces the entire value according to its type:

| Input type | Result |
| --- | --- |
| Character strings | One `X` per character |
| Binary strings and `BLOB` values | One `X` per byte |
| `DATE` | `1970-01-01` |
| `DATETIME` and `TIMESTAMP` | `1970-01-01 00:00:00`, with the input temporal type and precision |
| `TIME` | Zero duration, with the input precision |
| `YEAR`, floating-point types, and `DECIMAL` | Zero, with the input type |

Ordinary integer types, including `INT`, `BIGINT`, and their unsigned variants, are not accepted by `MASK_FULL`. Use `MASK_NULL` or a custom expression for those columns. `MASK_FULL` accepts exactly one argument; the replacement character is always `X` for strings.

For example, `MASK_FULL('secret')` returns `XXXXXX`.

### `MASK_PARTIAL(value, preserve_left, preserve_right, mask_char)`

Preserves the specified number of characters at each end and replaces the middle characters with `mask_char`.

- `value` must be a string.
- `preserve_left` and `preserve_right` must be non-negative integers.
- `mask_char` must contain exactly one character for character strings, or one byte for binary strings.
- Character strings are processed by character, including multibyte characters. Binary strings are processed by byte.
- If the preserved portions cover the whole input, the function returns the original value. Choose counts that also mask short values in your data.

For example, `MASK_PARTIAL('13812345678', 3, 4, '*')` returns `138****5678`, and `MASK_PARTIAL('abcdef', 1, 2, '*')` returns `a***ef`.

### `MASK_NULL(value)`

Returns SQL `NULL`. You can use it with any column type supported by masking policies, including integer columns.

For example, `MASK_NULL(12345)` returns `NULL`.

### `MASK_DATE(value, date_template)`

Replaces components of a `DATE`, `DATETIME`, or `TIMESTAMP` value. For `DATETIME` and `TIMESTAMP`, the time portion becomes midnight. `TIME` and `YEAR` are not accepted.

`date_template` has three components separated by hyphens. Each component is either a fixed number or the corresponding uppercase placeholder: `Y` to preserve the year, `M` to preserve the month, or `D` to preserve the day. Fixed components can omit leading zeroes. The resulting date must be valid.

For an input date of `1990-05-15`:

| Template | Result |
| --- | --- |
| `'1970-01-01'` | `1970-01-01` |
| `'Y-01-01'` | `1990-01-01` |
| `'Y-M-1'` | `1990-05-01` |
| `'2000-1-1'` | `2000-01-01` |

## Restrict operations that read protected columns

`RESTRICT ON` prevents selected operations from using protected source values when the current session is not exempt from masking. Without these restrictions, result masking alone does not prevent statements such as `INSERT ... SELECT` from copying original values into another table.

| Operation | Scope |
| --- | --- |
| `INSERT_INTO_SELECT` | Reads of protected source columns in `INSERT ... SELECT` |
| `UPDATE_SELECT` | Reads through subqueries in `UPDATE`, and assignments that copy or compute values from protected source columns |
| `DELETE_SELECT` | Reads of protected source columns through subqueries in `DELETE` |
| `CTAS` | Reserved restriction name for `CREATE TABLE ... SELECT`; the statement is not supported in this implementation |
| `NONE` | No operation restrictions; the default |

Specify one or more operation names in parentheses, or use `RESTRICT ON NONE` to clear them.

To try `INSERT_INTO_SELECT` with the policy from [Create and use a policy](#create-and-use-a-policy), first create a destination table and grant the reader permission to write to it. Run these statements as an administrator:

```sql
CREATE TABLE masking_demo.phone_copy (phone VARCHAR(20));
GRANT INSERT ON masking_demo.phone_copy TO 'masking_reader'@'%';
```

With `mask_phone` enabled and restricting `INSERT_INTO_SELECT`, connect as `masking_reader` and attempt to copy the protected column:

```sql
INSERT INTO masking_demo.phone_copy (phone)
SELECT phone FROM masking_demo.contacts;
```

```text
ERROR 8277 (HY000): Access to masked column 'phone' is blocked by the masking policy RESTRICT ON setting. Contact the policy administrator to check the expression and current user or role.
```

For a restricted operation, TiDB evaluates session-constant user or role conditions and permits access only if the resulting policy expression is the original column. A data-dependent expression, or another expression that TiDB cannot establish as returning the original column, does not authorize the operation.

`UPDATE_SELECT` also covers direct assignments such as `UPDATE t SET other_column = phone`, assignments in joined updates, and `INSERT ... ON DUPLICATE KEY UPDATE` assignments that read a protected column of the existing row. Assigning a column directly to itself, such as `SET phone = phone`, is allowed. Computing a new value from it, such as `SET phone = UPPER(phone)`, is restricted. Comparisons that use the column only in `WHERE` or `JOIN ... ON` are not blocked by this assignment check.

## Query behavior and limitations

Masking policies use **AT RESULT** semantics:

- Ordinary `WHERE`, `JOIN`, `GROUP BY`, `HAVING`, and `ORDER BY` processing uses original values. Grouping and deduplication happen before result masking, so different original values can appear as identical masked values in separate result rows.
- Result expressions such as `CONCAT(phone, '!')` are evaluated using the masked column value after filtering and sorting.
- A scalar, `IN`, or quantified-comparison subquery used in a predicate can expose a masked output to the outer comparison. This differs from a direct predicate on a base column. `MIN` and `MAX` outputs in predicate subqueries retain their original aggregate values. Unsupported predicate-output shapes can also retain original values; do not use predicate subqueries as an access-control boundary.
- Snapshot and stale reads use the policy state at the read timestamp. A read from before a policy was created is not protected by that policy.

The following limitations apply:

- Supported policy target types include character and binary strings, the `TEXT` and `BLOB` families, integer, floating-point, and decimal types, and `DATE`, `TIME`, `DATETIME`, `TIMESTAMP`, and `YEAR`. Other types, such as `JSON`, are not supported. Individual masking functions have narrower input requirements, as described above.
- You cannot change the type, length, or precision of a column that has a policy, even if the policy is disabled. Drop the policy before changing the column, then recreate it with an expression appropriate for the new type.
- TiDB rejects result shapes when it cannot preserve a policy, with an error starting with `masking policy cannot be preserved through`. Examples include scalar subqueries that return a protected column in the result list, window functions over protected values, recursive CTE outputs that require masking, and `UNION` outputs with incompatible protected sources.
- `MIN` and `MAX` over a directly protected column can return a masked result. Other aggregates over protected values, such as `GROUP_CONCAT`, are rejected when their result cannot preserve the policy. `COUNT(*)` can still return row counts.
- Result expressions over protected columns that contain functions such as `RAND()`, variable assignments, or advisory lock functions are rejected because TiDB cannot safely rebuild them for result masking. These query-shape restrictions also apply to exempt users while the policy is enabled.
- Plan-cache eligibility depends on the policy expression. The masking built-ins and supported identity conditions can use cached plans, but a policy containing `CONCAT`, for example, bypasses plan caches with the warning `masking policy contains a function that cannot be safely cached`. Do not assume all protected queries can use a cached plan.

## Backup, restore, and replication

BR backs up `mysql.tidb_masking_policy` with other system tables when the table filter selects it. A full backup includes it by default. However, BR does not restore masking policies:

- Snapshot restore skips the policy system table, including when `--with-sys-table` is specified. It does not create or change policies, and preserves policies already present on the target cluster.
- Incremental restore does not replay `CREATE`, `ALTER`, or `DROP` masking-policy DDL. You must apply policy changes made after the base backup manually on the target cluster.
- Point-in-time recovery does not rebuild source-cluster masking policies on the target cluster.

Policy records reference table and column IDs, which can change during restore. Directly copying rows from `mysql.tidb_masking_policy` does not preserve the bindings.

Before giving users access to restored data:

1. Inspect source policies using `SHOW MASKING POLICIES FOR table_name` and save their expressions, restrictions, and status.
2. Recreate the policies on the target tables using policy DDL, and configure the accounts and roles referenced by the expressions.
3. Verify query results and restricted operations using both exempt and non-exempt accounts.

Log-backup files can contain policy metadata because log backup records changes across the data key range. Masking does not redact stored backup data.

For TiCDC deployments, configure and verify policies, accounts, and roles on the downstream cluster separately. Do not assume that source policies are transferred automatically. SQL-based export and validation tools can receive masked values when they run as a non-exempt account.

## See also

- [Privilege Management](/privilege-management.md)
- [Role-Based Access Control](/role-based-access-control.md)
- [BR Overview](/br/backup-and-restore-overview.md)
