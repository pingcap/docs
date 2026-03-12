---
title: SHOW VARIABLES
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.634"/>

Displays all session variables and their details, such as names, values, and types.

See also: [SHOW_VARIABLES](/sql/sql-functions/table-functions/show-variables)

## Syntax

```sql
SHOW VARIABLES [ LIKE '<pattern>' | WHERE <expr> ]
```

## Examples

The following example lists all session variables with their values and types:

```sql
SHOW VARIABLES;

┌──────────────────────────┐
│  name  │  value │  type  │
├────────┼────────┼────────┤
│ a      │ 3      │ UInt8  │
│ b      │ 55     │ UInt8  │
│ x      │ 'xx'   │ String │
│ y      │ 'yy'   │ String │
└──────────────────────────┘
```

To filter and return only the variable named `a`, use one of the following queries:

```sql
SHOW VARIABLES LIKE 'a';

SHOW VARIABLES WHERE name = 'a';
```