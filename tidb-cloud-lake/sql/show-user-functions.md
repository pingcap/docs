---
title: SHOW USER FUNCTIONS
sidebar_position: 4
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.558"/>

Lists all user-defined functions including scalar functions, table functions, embedded functions, and external functions.

## Syntax

```sql
SHOW USER FUNCTIONS
```

## Output Columns

| Column | Description |
|--------|-------------|
| `name` | Function name |
| `is_aggregate` | Whether it's an aggregate function (NULL for UDFs) |
| `description` | Function description if provided |
| `arguments` | Function parameters in JSON format |
| `language` | Programming language: SQL, python, javascript, wasm, or external |
| `created_on` | Function creation timestamp |

## Examples

```sql
SHOW USER FUNCTIONS;

┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  name  │    is_aggregate   │ description │           arguments           │ language │         created_on         │
│ String │ Nullable(Boolean) │    String   │            Variant            │  String  │          Timestamp         │
├────────┼───────────────────┼─────────────┼───────────────────────────────┼──────────┼────────────────────────────┤
│ get_v1 │ NULL              │             │ {"parameters":["input_json"]} │ SQL      │ 2024-11-18 23:20:28.432842 │
│ get_v2 │ NULL              │             │ {"parameters":["input_json"]} │ SQL      │ 2024-11-18 23:21:46.838744 │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```