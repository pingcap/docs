---
title: RENAME WORKLOAD GROUP
summary: Renames an existing workload group to a new name.
---

# RENAME WORKLOAD GROUP

> **Note:**
>
> Introduced or updated in v1.2.743.

Renames an existing workload group to a new name.

## Syntax

```sql
RENAME WORKLOAD GROUP <current_name> TO <new_name>
```

## Examples

This example renames `test_workload_group_1` to `test_workload_group`:

```sql
RENAME WORKLOAD GROUP test_workload_group_1 TO test_workload_group;
```
