---
title: Query Result Cache
---

Databend caches and persists the query results for every executed query when enabled. This can be used to great effect to dramatically reduce the time it takes to get an answer.

## Cache Usage Conditions

Query results are reused from cache only when **all** conditions are satisfied:

| Condition | Requirement |
|-----------|-------------|
| **Cache Enabled** | `enable_query_result_cache = 1` in current session |
| **Identical Query** | Query text must match exactly (case-sensitive) |
| **Execution Time** | Original query runtime ≥ `query_result_cache_min_execute_secs` |
| **Result Size** | Cached result ≤ `query_result_cache_max_bytes` |
| **TTL Valid** | Cache age < `query_result_cache_ttl_secs` |
| **Data Consistency** | Table data unchanged since caching (unless `query_result_cache_allow_inconsistent = 1`) |
| **Session Scope** | Cache is session-specific |

:::note Automatic Cache Invalidation
By default (`query_result_cache_allow_inconsistent = 0`), cached results are automatically invalidated when underlying table data changes. This ensures data consistency but may reduce cache effectiveness in frequently updated tables.
:::

## Quick Start

Enable query result caching in your session:

```sql
-- Enable query result cache
SET enable_query_result_cache = 1;

-- Optional: Cache all queries (including fast ones)
SET query_result_cache_min_execute_secs = 0;
```

## Configuration Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `enable_query_result_cache` | 0 | Enables/disables query result caching |
| `query_result_cache_allow_inconsistent` | 0 | Allow cached results even if underlying data changed |
| `query_result_cache_max_bytes` | 1048576 | Maximum size (bytes) for a single cached result |
| `query_result_cache_min_execute_secs` | 1 | Minimum execution time before caching |
| `query_result_cache_ttl_secs` | 300 | Cache expiration time (5 minutes) |

## Performance Example

This example demonstrates caching a TPC-H Q1 query:

### 1. Enable Caching
```sql
SET enable_query_result_cache = 1;
SET query_result_cache_min_execute_secs = 0;
```

### 2. First Execution (No Cache)
```sql
SELECT
    l_returnflag,
    l_linestatus,
    sum(l_quantity) as sum_qty,
    sum(l_extendedprice) as sum_base_price,
    sum(l_extendedprice * (1 - l_discount)) as sum_disc_price,
    sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) as sum_charge,
    avg(l_quantity) as avg_qty,
    avg(l_extendedprice) as avg_price,
    avg(l_discount) as avg_disc,
    count(*) as count_order
FROM lineitem
WHERE l_shipdate <= add_days(to_date('1998-12-01'), -90)
GROUP BY l_returnflag, l_linestatus
ORDER BY l_returnflag, l_linestatus;
```

**Result**: 4 rows in **21.492 seconds** (600M rows processed)

### 3. Verify Cache Entry
```sql
SELECT sql, query_id, result_size, num_rows FROM system.query_cache;
```

### 4. Second Execution (From Cache)
Run the same query again.

**Result**: 4 rows in **0.164 seconds** (0 rows processed)

## Cache Management

### Monitor Cache Usage
```sql
SELECT * FROM system.query_cache;
```

### Access Cached Results
```sql
SELECT * FROM RESULT_SCAN(LAST_QUERY_ID());
```

### Cache Lifecycle
Cached results are automatically removed when:
- **TTL expires** (default: 5 minutes)
- **Result size exceeds limit** (default: 1MB)
- **Session ends** (cache is session-scoped)
- **Underlying data changes** (automatic invalidation for consistency)
- **Table structure changes** (schema modifications invalidate cache)

:::note Session Scope
Query result cache is session-scoped. Each session maintains its own cache that's automatically cleaned up when the session ends.
:::
