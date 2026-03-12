---
title: DROP WAREHOUSE
sidebar_position: 5
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.687"/>

Removes a warehouse and frees up the resources associated with it.

## Syntax

```sql
DROP WAREHOUSE [ IF EXISTS ] <warehouse_name>
```

| Parameter      | Description                                                                                                                                        |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `IF EXISTS`    | Optional. If specified, the command succeeds silently when the warehouse does not exist. Without it, the command fails if the warehouse is absent. |
| warehouse_name | The name of the warehouse to remove.                                                                                                               |

## Examples

Drop a warehouse:

```sql
DROP WAREHOUSE my_warehouse;
```

Drop a warehouse only if it exists:

```sql
DROP WAREHOUSE IF EXISTS my_warehouse;
```
