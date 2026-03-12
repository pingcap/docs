---
title: CREATE SEQUENCE
sidebar_position: 1
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.807"/>

Creates a new sequence in Databend.

A sequence is an object that automatically generates unique numeric identifiers, commonly used for assigning distinct values to table rows (e.g., user IDs). While sequences guarantee unique values, they **do not** ensure contiguity (i.e., gaps may occur).

## Syntax

```sql
CREATE [ OR REPLACE ] SEQUENCE [ IF NOT EXISTS ] <sequence>
    [ START [ = ] <start_value> ]
    [ INCREMENT [ = ] <increment_value> ]
```

| Parameter           | Description                                           | Default |
|---------------------|-------------------------------------------------------|---------|
| `<sequence>`        | The name of the sequence to be created.               | -       |
| `START`             | The initial value of the sequence.                    | 1       |
| `INCREMENT`         | The increment value for each call to NEXTVAL.         | 1       |

## Access control requirements

| Privilege       | Object Type | Description           |
|:----------------|:------------|:----------------------|
| CREATE SEQUENCE | Global      | Creates a sequence. |


To create a sequence, the user performing the operation or the [current_role](/guides/security/access-control/roles) must have the CREATE SEQUENCE [privilege](/guides/security/access-control/privileges).

:::note

The enable_experimental_sequence_rbac_check settings governs sequence-level access control. It is disabled by default.
sequence creation solely requires the user to possess superuser privileges, bypassing detailed RBAC checks.
When enabled, granular permission verification is enforced during sequence establishment.

This is an experimental feature and may be enabled by default in the future.

:::

## Examples

### Basic Sequence

Create a sequence with default settings (starts at 1, increments by 1):

```sql
CREATE SEQUENCE staff_id_seq;

CREATE TABLE staff (
    staff_id INT,
    name VARCHAR(50),
    department VARCHAR(50)
);

INSERT INTO staff (staff_id, name, department)
VALUES (NEXTVAL(staff_id_seq), 'John Doe', 'HR');

INSERT INTO staff (staff_id, name, department)
VALUES (NEXTVAL(staff_id_seq), 'Jane Smith', 'Finance');

SELECT * FROM staff;

┌───────────────────────────────────────────────────────┐
│     staff_id    │       name       │    department    │
├─────────────────┼──────────────────┼──────────────────┤
│               2 │ Jane Smith       │ Finance          │
│               1 │ John Doe         │ HR               │
└───────────────────────────────────────────────────────┘
```

### Custom Start and Increment

Create a sequence starting at 1000 with increment of 10:

```sql
CREATE SEQUENCE order_id_seq START = 1000 INCREMENT = 10;

CREATE TABLE orders (
    order_id BIGINT,
    order_name VARCHAR(100)
);

INSERT INTO orders (order_id, order_name)
VALUES (NEXTVAL(order_id_seq), 'Order A');

INSERT INTO orders (order_id, order_name)
VALUES (NEXTVAL(order_id_seq), 'Order B');

SELECT * FROM orders;

┌──────────────────────────────────┐
│    order_id    │    order_name   │
├────────────────┼─────────────────┤
│           1000 │ Order A         │
│           1010 │ Order B         │
└──────────────────────────────────┘
```