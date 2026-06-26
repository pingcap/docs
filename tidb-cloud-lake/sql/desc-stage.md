---
title: DESC STAGE
summary: Describes the properties of a stage.
---

# DESC STAGE

Describes the properties of a stage.

## Syntax

```sql
DESC STAGE <name>
```

## Examples

```sql
CREATE STAGE my_int_stage;
```

```sql
DESC STAGE my_int_stage;

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│     name     │ stage_type │ storage_type │ url  │ endpoint │ has_credentials │ has_encryption_key │ storage_params │ file_format_options │ creator │         created_on         │ comment │     owner     │
├──────────────┼────────────┼──────────────┼──────┼──────────┼─────────────────┼────────────────────┼────────────────┼─────────────────────┼─────────┼────────────────────────────┼─────────┼───────────────┤
│ my_int_stage │ Internal   │ NULL         │ NULL │ NULL     │ false           │ false              │ NULL           │ {"compression":...} │ root@%  │ 2026-06-16 22:21:19.000000 │         │ account_admin │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
