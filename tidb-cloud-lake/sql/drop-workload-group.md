---
title: DROP WORKLOAD GROUP
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.743"/>

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