---
title: REFRESH AGGREGATING INDEX
sidebar_position: 2
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.151"/>

Databend automatically maintains aggregating indexes in `SYNC` mode as new data is ingested. Run `REFRESH AGGREGATING INDEX` when you introduce an index on a table that already contains data so earlier rows are backfilled.

## Syntax

```sql
REFRESH AGGREGATING INDEX <index_name>
```

## Examples

This example creates an aggregating index on a table that already contains data, then runs `REFRESH` once to backfill those rows:

```sql
-- Prepare a table and load data before the index exists
CREATE TABLE agg(a int, b int, c int);
INSERT INTO agg VALUES (1,1,4), (1,2,1), (1,2,4);

-- Declare the aggregating index (existing rows are not indexed yet)
CREATE AGGREGATING INDEX my_agg_index AS SELECT MIN(a), MAX(c) FROM agg;

-- Backfill previously inserted rows
REFRESH AGGREGATING INDEX my_agg_index;

-- Insert new data after the index exists (no manual refresh needed)
INSERT INTO agg VALUES (2,2,5);
-- SYNC mode keeps the index current automatically
```
