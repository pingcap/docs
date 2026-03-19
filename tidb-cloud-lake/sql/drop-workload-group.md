---
title: DROP WORKLOAD GROUP
summary: Removes the specified workload group.
---

# DROP WORKLOAD GROUP

> **Note:**
>
> Introduced or updated in v1.2.743.

Removes the specified workload group.

## Syntax

```sql
DROP WORKLOAD GROUP [IF EXISTS] <workload_group_name>
```

## Examples

This example removes the `test_workload_group` workload group:

```sql
DROP WORKLOAD GROUP test_workload_group;
```
