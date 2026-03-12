---
title: CREATE AGGREGATING INDEX
sidebar_position: 1
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.339"/>

Create a new aggregating index in Databend.

## Syntax

```sql
CREATE [ OR REPLACE ] AGGREGATING INDEX <index_name> AS SELECT ...
```

- When creating aggregating indexes, limit their usage to standard [Aggregate Functions](../../../20-sql-functions/07-aggregate-functions/index.md) (e.g., AVG, SUM, MIN, MAX, COUNT and GROUP BY), while keeping in mind that GROUPING SETS, [Window Functions](../../../20-sql-functions/08-window-functions/index.md), [LIMIT](../../20-query-syntax/01-query-select.md#limit-clause), and [ORDER BY](../../20-query-syntax/01-query-select.md#order-by-clause) are not accepted, or you will get an error: `Currently create aggregating index just support simple query, like: SELECT ... FROM ... WHERE ... GROUP BY ...`.

- The query filter scope defined when creating aggregating indexes should either match or encompass the scope of your actual queries.

- To confirm if an aggregating index works for a query, use the [EXPLAIN](../../40-explain-cmds/explain.md) command to analyze the query.

## Examples

This example creates an aggregating index named *my_agg_index* for the query "SELECT MIN(a), MAX(c) FROM agg":

```sql
-- Prepare data
CREATE TABLE agg(a int, b int, c int);
INSERT INTO agg VALUES (1,1,4), (1,2,1), (1,2,4), (2,2,5);

-- Create an aggregating index
CREATE AGGREGATING INDEX my_agg_index AS SELECT MIN(a), MAX(c) FROM agg;
```
