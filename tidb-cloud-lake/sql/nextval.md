---
title: NEXTVAL
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.784"/>

Retrieves the next value from a sequence.

## Syntax

```sql
NEXTVAL(<sequence_name>)
```

## Return Type

Integer.

## Access control requirements

| Privilege       | Object Type | Description        |
|:----------------|:------------|:-------------------|
| ACCESS SEQUENCE | SEQUENCE    | Access a sequence. |


To access a sequence, the user performing the operation or the roles must have the ACCESS SEQUENCE [privilege](/guides/security/access-control/privileges).

:::note

The enable_experimental_sequence_rbac_check settings governs sequence-level access control. It is disabled by default.
sequence creation solely requires the user to possess superuser privileges, bypassing detailed RBAC checks.
When enabled, granular permission verification is enforced during sequence establishment.

This is an experimental feature and may be enabled by default in the future.

:::


## Examples

This example demonstrates how the NEXTVAL function works with a sequence:

```sql
CREATE SEQUENCE my_seq;

SELECT
  NEXTVAL(my_seq),
  NEXTVAL(my_seq),
  NEXTVAL(my_seq);

┌─────────────────────────────────────────────────────┐
│ nextval(my_seq) │ nextval(my_seq) │ nextval(my_seq) │
├─────────────────┼─────────────────┼─────────────────┤
│               1 │               2 │               3 │
└─────────────────────────────────────────────────────┘
```

This example showcases how sequences and the NEXTVAL function are employed to automatically generate and assign unique identifiers to rows in a table.

```sql
-- Create a new sequence named staff_id_seq
CREATE SEQUENCE staff_id_seq;

-- Create a new table named staff with an auto-generated staff_id
CREATE TABLE staff (
    staff_id INT DEFAULT NEXTVAL(staff_id_seq),
    name VARCHAR(50),
    department VARCHAR(50)
);

--  Insert a new staff member with an auto-generated staff_id into the staff table
INSERT INTO staff (name, department)
VALUES ('John Doe', 'HR');

-- Insert another row
INSERT INTO staff (name, department)
VALUES ('Jane Smith', 'Finance');

SELECT * FROM staff;

┌───────────────────────────────────────────────────────┐
│     staff_id    │       name       │    department    │
├─────────────────┼──────────────────┼──────────────────┤
│               3 │ Jane Smith       │ Finance          │
│               2 │ John Doe         │ HR               │
└───────────────────────────────────────────────────────┘
```