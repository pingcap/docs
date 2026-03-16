---
title: Aggregating Index
---

# Aggregating Index: Precomputed Results for Instant Analytics

Aggregating indexes dramatically accelerate analytical queries by precomputing and storing aggregation results, eliminating the need to scan entire tables for common analytics operations.

## What Problem Does It Solve?

Analytical queries on large datasets face significant performance challenges:

| Problem | Impact | Aggregating Index Solution |
|---------|--------|---------------------------|
| **Full Table Scans** | SUM, COUNT, MIN, MAX queries scan millions of rows | Read precomputed results instantly |
| **Repeated Calculations** | Same aggregations computed over and over | Store results once, reuse many times |
| **Slow Dashboard Queries** | Analytics dashboards take minutes to load | Sub-second response for common metrics |
| **High Compute Costs** | Heavy aggregation workloads consume resources | Minimal compute for cached results |
| **Poor User Experience** | Users wait for reports and analytics | Instant results for business intelligence |

**Example**: A sales analytics query `SELECT SUM(revenue), COUNT(*) FROM sales WHERE region = 'US'` on 100M rows. Without aggregating index, it scans all US sales records. With aggregating index, it returns precomputed results instantly.

## How It Works

1. **Index Creation** → Define aggregation queries to precompute
2. **Result Storage** → Databend stores aggregated results in optimized blocks
3. **Query Matching** → Incoming queries automatically use precomputed results
4. **Automatic Updates** → Results refresh when underlying data changes

## Quick Setup

```sql
-- Create table with sample data
CREATE TABLE sales(region VARCHAR, product VARCHAR, revenue DECIMAL, quantity INT);

-- Create aggregating index for common analytics
CREATE AGGREGATING INDEX sales_summary AS 
SELECT region, SUM(revenue), COUNT(*), AVG(quantity) 
FROM sales 
GROUP BY region;

-- Refresh the index (manual mode)
REFRESH AGGREGATING INDEX sales_summary;

-- Verify the index is used
EXPLAIN SELECT region, SUM(revenue) FROM sales GROUP BY region;
```

## Supported Operations

| ✅ Supported | ❌ Not Supported |
|-------------|-----------------|
| SUM, COUNT, MIN, MAX, AVG | Window Functions |
| GROUP BY clauses | GROUPING SETS |
| WHERE filters | ORDER BY, LIMIT |
| Simple aggregations | Complex subqueries |

## Refresh Strategies

| Strategy | When to Use | Configuration |
|----------|-------------|---------------|
| **Automatic (SYNC)** | Real-time analytics, small datasets | `CREATE AGGREGATING INDEX ... SYNC` |
| **Manual** | Large datasets, batch processing | `CREATE AGGREGATING INDEX ...` (default) |
| **Background (Cloud)** | Production workloads | Automatic in Databend Cloud |

### Automatic vs Manual Refresh

```sql
-- Automatic refresh (updates with every data change)
CREATE AGGREGATING INDEX auto_summary AS 
SELECT region, SUM(revenue) FROM sales GROUP BY region SYNC;

-- Manual refresh (update on demand)
CREATE AGGREGATING INDEX manual_summary AS 
SELECT region, SUM(revenue) FROM sales GROUP BY region;

REFRESH AGGREGATING INDEX manual_summary;
```

## Performance Example

This example shows the dramatic performance improvement:

```sql
-- Prepare data
CREATE TABLE agg(a int, b int, c int);
INSERT INTO agg VALUES (1,1,4), (1,2,1), (1,2,4), (2,2,5);

-- Create an aggregating index
CREATE AGGREGATING INDEX my_agg_index AS SELECT MIN(a), MAX(c) FROM agg;

-- Refresh the aggregating index
REFRESH AGGREGATING INDEX my_agg_index;

-- Verify if the aggregating index works
EXPLAIN SELECT MIN(a), MAX(c) FROM agg;

-- Key indicators in the execution plan:
-- ├── aggregating index: [SELECT MIN(a), MAX(c) FROM default.agg]
-- ├── rewritten query: [selection: [index_col_0 (#0), index_col_1 (#1)]]
-- This shows the query uses precomputed results instead of scanning raw data
```

## Best Practices

| Practice | Benefit |
|----------|---------|
| **Index Common Queries** | Focus on frequently executed analytics |
| **Use Manual Refresh** | Better control over update timing |
| **Monitor Index Usage** | Use EXPLAIN to verify index utilization |
| **Clean Up Unused Indexes** | Remove indexes that aren't being used |
| **Match Query Patterns** | Index filters should match actual queries |

## Management Commands

| Command | Purpose |
|---------|---------|
| `CREATE AGGREGATING INDEX` | Create new aggregating index |
| `REFRESH AGGREGATING INDEX` | Update index with latest data |
| `DROP AGGREGATING INDEX` | Remove index (use VACUUM TABLE to clean storage) |
| `SHOW AGGREGATING INDEXES` | List all indexes |

## Important Notes

:::tip
**When to Use Aggregating Indexes:**
- Frequent analytical queries (dashboards, reports)
- Large datasets with repeated aggregations
- Stable query patterns
- Performance-critical applications

**When NOT to Use:**
- Frequently changing data
- One-time analytical queries
- Simple queries on small tables
:::

## Configuration

```sql
-- Enable/disable aggregating index feature
SET enable_aggregating_index_scan = 1;  -- Enable (default)
SET enable_aggregating_index_scan = 0;  -- Disable
```

---

*Aggregating indexes are most effective for repetitive analytical workloads on large datasets. Start with your most common dashboard and reporting queries.*
