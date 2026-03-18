---
title: CREATE AGGREGATING INDEX
summary: Create a new aggregating index in Databend.
---

> **Note:**
>
> Introduced or updated in v1.2.339.

Create a new aggregating index in Databend.

## Syntax

```sql
CREATE [ OR REPLACE ] AGGREGATING INDEX <index_name> AS SELECT ...
```

- When creating aggregating indexes, limit their usage to standard [Aggregate Functions](/tidb-cloud-lake/_index.md) (e.g., AVG, SUM, MIN, MAX, COUNT and GROUP BY), while keeping in mind that GROUPING SETS, [Window Functions](/tidb-cloud-lake/_index.md), [LIMIT](/tidb-cloud-lake/sql/select.md#limit-clause), and [ORDER BY](/tidb-cloud-lake/sql/select.md#order-by-clause) are not accepted, or you will get an error: `Currently create aggregating index just support simple query, like: SELECT ... FROM ... WHERE ... GROUP BY ...`.

- The query filter scope defined when creating aggregating indexes should either match or encompass the scope of your actual queries.

- To confirm if an aggregating index works for a query, use the [EXPLAIN](/tidb-cloud-lake/sql/explain.md) command to analyze the query.

## Examples

This example creates an aggregating index named *my_agg_index* for the query "SELECT MIN(a), MAX(c) FROM agg":

```sql
-- Prepare data
CREATE TABLE agg(a int, b int, c int);
INSERT INTO agg VALUES (1,1,4), (1,2,1), (1,2,4), (2,2,5);

-- Create an aggregating index
CREATE AGGREGATING INDEX my_agg_index AS SELECT MIN(a), MAX(c) FROM agg;
```
