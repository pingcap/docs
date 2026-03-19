---
title: SHOW_VARIABLES
summary: Displays all session variables and their details, such as names, values, and types.
---

> **Note:**
>
> Introduced or updated in v1.2.634.

Displays all session variables and their details, such as names, values, and types.

See also: [SHOW VARIABLES](/tidb-cloud-lake/sql/show-variables.md)

## Syntax

```sql
SHOW_VARIABLES()
```

## Examples

```sql
SELECT name, value, type FROM SHOW_VARIABLES();

┌──────────────────────────┐
│  name  │  value │  type  │
├────────┼────────┼────────┤
│ y      │ 'yy'   │ String │
│ b      │ 55     │ UInt8  │
│ x      │ 'xx'   │ String │
│ a      │ 3      │ UInt8  │
└──────────────────────────┘
```