---
title: SHOW PROCEDURES
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.637"/>

Returns a list of all stored procedures in the system.

## Syntax

```sql
SHOW PROCEDURES
```

## Examples

```sql
SHOW PROCEDURES;

┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│       name       │ procedure_id │                        arguments                        │            comment           │       description      │         created_on         │
├──────────────────┼──────────────┼─────────────────────────────────────────────────────────┼──────────────────────────────┼────────────────────────┼────────────────────────────┤
│ convert_kg_to_lb │         2104 │ convert_kg_to_lb(Decimal(4, 2)) RETURN (Decimal(10, 2)) │ Converts kilograms to pounds │ user-defined procedure │ 2024-11-07 04:12:25.243143 │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
