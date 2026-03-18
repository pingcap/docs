---
title: system.functions
summary: Contains information about the supported built-in scalar and aggregate.
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.315"/>

Contains information about the supported built-in scalar and aggregate.

See also: [SHOW FUNCTIONS](/tidb-cloud-lake/sql/show-functions.md).

## Example

```sql
SELECT * FROM system.functions LIMIT 10;

┌──────────────────────────────────────────────────────────────┐
│     name     │ is_aggregate │ description │ syntax │ example │
├──────────────┼──────────────┼─────────────┼────────┼─────────┤
│ abs          │ false        │             │        │         │
│ acos         │ false        │             │        │         │
│ add          │ false        │             │        │         │
│ add_days     │ false        │             │        │         │
│ add_hours    │ false        │             │        │         │
│ add_minutes  │ false        │             │        │         │
│ add_months   │ false        │             │        │         │
│ add_quarters │ false        │             │        │         │
│ add_seconds  │ false        │             │        │         │
│ add_years    │ false        │             │        │         │
└──────────────────────────────────────────────────────────────┘
```
