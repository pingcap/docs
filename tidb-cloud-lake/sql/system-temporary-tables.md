---
title: system.temporary_tables
summary: Provides information about all existing temporary tables in the current session.
---

# system.temporary_tables

> **Note:**
>
> Introduced or updated in v1.2.666.

Provides information about all existing temporary tables in the current session.

```sql title='Examples:'
SELECT * FROM system.temporary_tables;

┌────────────────────────────────────────────────────┐
│ database │   name   │       table_id      │ engine │
├──────────┼──────────┼─────────────────────┼────────┤
│ default  │ my_table │ 4611686018427407904 │ FUSE   │
└────────────────────────────────────────────────────┘
```
