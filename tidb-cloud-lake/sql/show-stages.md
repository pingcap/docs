---
title: SHOW STAGES
summary: Returns a list of the created stages. The output list does not include the user stage.
---

# SHOW STAGES

Returns a list of the created stages. The output list does not include the user stage.

## Syntax

```sql
SHOW STAGES;
```

## Examples

```sql
SHOW STAGES;

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ name │ stage_type │ storage_type │ url  │ endpoint │ has_credentials │ has_encryption_key │ storage_params │ file_format_options │ creator │         created_on         │ comment │     owner     │
├──────┼────────────┼──────────────┼──────┼──────────┼─────────────────┼────────────────────┼────────────────┼─────────────────────┼─────────┼────────────────────────────┼─────────┼───────────────┤
│ eric │ Internal   │ NULL         │ NULL │ NULL     │ false           │ false              │ NULL           │ {"compression":...} │ root@%  │ 2026-06-16 22:21:19.000000 │         │ account_admin │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
