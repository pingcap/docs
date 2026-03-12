---
title: USE WAREHOUSE
sidebar_position: 2
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.687"/>

Binds the current session to a specific warehouse. Subsequent queries in the session will use this warehouse for execution.

## Syntax

```sql
USE WAREHOUSE <warehouse_name>
```

| Parameter      | Description                                                                                          |
| -------------- | ---------------------------------------------------------------------------------------------------- |
| warehouse_name | The name of the warehouse to use. The command validates that the warehouse exists and is accessible. |

## Examples

Set a warehouse as active for the current session:

```sql
USE WAREHOUSE my_warehouse;
```
