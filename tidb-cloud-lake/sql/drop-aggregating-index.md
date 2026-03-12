---
title: DROP AGGREGATING INDEX
sidebar_position: 4
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.151"/>

Deletes an existing aggregating index. Please note that deleting an aggregating index does NOT remove the associated storage blocks. To delete the blocks as well, use the [VACUUM TABLE](../01-table/91-vacuum-table.md) command. To disable the aggregating indexing feature, set `enable_aggregating_index_scan` to 0.

## Syntax

```sql
DROP AGGREGATING INDEX <index_name>
```

## Examples

This example deleted an aggregating index named *my_agg_index*:

```sql
DROP AGGREGATING INDEX my_agg_index;
```
