---
title: system.temporary_tables
summary: Provides information about all existing temporary tables in the current session.
---

# system.temporary_tables

import FunctionDescription from '@site/src/components/FunctionDescription';

## system.temporary_tables

<FunctionDescription description="Introduced or updated: v1.2.666"/>

Provides information about all existing temporary tables in the current session.

```sql title='Examples:'
SELECT * FROM system.temporary_tables;

┌────────────────────────────────────────────────────┐
│ database │   name   │       table_id      │ engine │
├──────────┼──────────┼─────────────────────┼────────┤
│ default  │ my_table │ 4611686018427407904 │ FUSE   │
└────────────────────────────────────────────────────┘
```
