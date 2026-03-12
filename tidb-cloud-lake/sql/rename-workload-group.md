---
title: RENAME WORKLOAD GROUP
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.743"/>

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

