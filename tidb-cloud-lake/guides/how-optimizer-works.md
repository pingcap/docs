---
title: How Databend Optimizer Works
---

Databend's query optimizer orchestrates a series of transformations that turn SQL text into an executable plan. The optimizer builds an abstract representation of the query, enriches it with real-time statistics, applies rule-based rewrites, explores join alternatives, and finally picks the cheapest physical operators.

The same optimizer pipeline powers analytic reporting, JSON search, vector retrieval, and geospatial search—**Databend maintains one optimizer that understands every data type it stores.**

## What Makes Databend’s Optimizer Tick

- Statistics stay up to date automatically: when data is written, Databend immediately maintains row counts, value ranges, and NDVs, so the optimizer can use fresh information for selectivity, join ordering, and costing without any manual maintenance.
- Shape first, cost second: the pipeline decorrelates, pushes predicates/limits, and splits aggregates before global search, shrinking the space and moving work to storage.
- DP + Cascades together: DPhpy finds good join orders; a memo‑driven Cascades pass selects the cheapest physical operators over the same SExpr memo.
- Distribution‑aware by design: planning decides local vs distributed and rewrites broadcasts into key‑based shuffles to avoid hotspots.

## Example Query

We’ll use the following analytics query and show how each stage transforms it.

```sql
WITH recent_orders AS (
  SELECT *
  FROM orders
  WHERE order_date >= DATE_TRUNC('month', today()) - INTERVAL '3' MONTH
    AND fulfillment_status <> 'CANCELLED'
)
SELECT c.region,
       COUNT(*) AS order_count,
       COUNT(o.id) AS row_count,
       COUNT(DISTINCT o.product_id) AS product_count,
       MIN(o.total_amount) AS min_amount,
       AVG(o.total_amount) AS avg_amount
FROM recent_orders o
JOIN customers c ON o.customer_id = c.id
LEFT JOIN products p ON o.product_id = p.id
WHERE c.status = 'ACTIVE'
  AND o.total_amount > 0
  AND p.is_active = TRUE
  AND EXISTS (
        SELECT 1
        FROM support_tickets t
        WHERE t.customer_id = c.id
          AND t.created_at > DATE_TRUNC('month', today()) - INTERVAL '1' MONTH
      )
GROUP BY c.region
HAVING COUNT(*) > 100
ORDER BY order_count DESC
LIMIT 10;
```

## Phase 1: Prep & Stats

Phase 1 makes the query easy to reason about and equips it with the data needed for costing. On our example, the optimizer performs these concrete steps:

### 1. Flatten the subquery

Turn the `EXISTS (...)` check into a regular join so the rest of the pipeline sees a single join tree.

```
# Before (correlated)
customers ─┐
           ├─ JOIN ─ orders
support ───┘        │
                    └─ EXISTS (references customers)

# After (semi-join)
customers ─┐
support ───┴─ SEMI JOIN ─ orders
```

Equivalent SQL (semantics preserved):

```sql
FROM (
  SELECT *
  FROM orders
  WHERE order_date >= DATE_TRUNC('month', today()) - INTERVAL '3' MONTH
    AND fulfillment_status <> 'CANCELLED'
) o
JOIN customers c ON o.customer_id = c.id
LEFT JOIN products p ON o.product_id = p.id
JOIN (
  SELECT DISTINCT customer_id
  FROM support_tickets
  WHERE created_at > DATE_TRUNC('month', today()) - INTERVAL '1' MONTH
) t ON t.customer_id = c.id
```

### 2. Check metadata shortcuts

If an aggregate such as `MIN(o.total_amount)` has no filtering, the optimizer fetches it from table statistics instead of scanning:

```
-- Conceptual replacement when no filters apply
SELECT MIN(total_amount)
FROM orders

# becomes

SELECT table_stats.min_total_amount
```

In our query filters apply, so we keep the real computation.

### 3. Attach statistics

During planning, Databend collects row counts, value ranges, and distinct counts for the scanned tables. No SQL changes, but later selectivity and cost estimates stay accurate without any `ANALYZE` jobs.

### 4. Normalize aggregates

After statistics are attached, the optimizer rewrites counters it can share. `COUNT(o.id)` becomes `COUNT(*)`, so the engine maintains a single counter for both usages. Only the SELECT list changes:

```sql
SELECT c.region,
       COUNT(*)            AS order_count,
       COUNT(*)            AS row_count,      -- was COUNT(o.id)
       COUNT(DISTINCT o.product_id) AS product_count,
       MIN(o.total_amount) AS min_amount,
       AVG(o.total_amount) AS avg_amount
...
```

## Phase 2: Refine the Logic

Phase 2 runs targeted rewrites that keep only the work we truly need:

### 1. Push filters/limits down

```
# Before
Filter (o.total_amount > 0)
└─ Scan (recent_orders)

# After
Scan (recent_orders, pushdown_predicates=[total_amount > 0])
```

Sorting with a limit also tightens up:

```
# Before
Limit (10)
└─ Sort (order_count DESC)
   └─ Join (...)

# After
Sort (order_count DESC)
└─ Limit (10)
   └─ Join (...)
```

### 2. Drop redundancies

```
# Before
Filter (1 = 1 AND c.status = 'ACTIVE')
└─ ...

# After
Filter (c.status = 'ACTIVE')
└─ ...
```

### 3. Split aggregates

```
# Before
Aggregate (COUNT/AVG)
└─ Scan (recent_orders)

# After
Aggregate (final)
└─ Aggregate (partial)
   └─ Scan (recent_orders)
```

Partial aggregates run close to the data, then a single final step merges the results.

### 4. Push filters into the CTE

Predicates that reference only CTE columns are pushed inside the definition of `recent_orders`, shrinking the data before joins:

```sql
WITH recent_orders AS (
  SELECT *
  FROM orders
  WHERE order_date >= DATE_TRUNC('month', today()) - INTERVAL '3' MONTH
    AND fulfillment_status <> 'CANCELLED'
    AND total_amount > 0              -- pushed from outer query
)
```

## Phase 3: Cost & Physical Plan

With a tidy logical plan and fresh statistics, the optimizer makes three decisions:

### 1. Choose the join order

A statistics-guided dynamic program (`DPhpyOptimizer`) evaluates join permutations. It prefers building hash tables on the smaller filtered tables (`customers`, `products`, `support_tickets`) while the large fact table (`recent_orders`) probes them:

```
    customers      products
           \      /
            HASH JOIN (build)
                 |
        recent_orders  (probe)
                 |
        SEMI JOIN support_tickets
```

### 2. Tighten join semantics

Rule-based passes adjust joins discovered above.

#### a. Turn safe LEFT joins into INNER joins

Our query starts with `LEFT JOIN products p`, but the predicate `p.is_active = TRUE` guarantees we only keep rows with a matching product. The optimizer flips the join type:

```
# Before
recent_orders ──⊗── products   (LEFT)
            filter: p.is_active = TRUE

# After
recent_orders ──⋈── products   (INNER)
```

#### b. Drop duplicate predicates

If a join condition repeats (for example `o.customer_id = c.id` listed twice), `DeduplicateJoinConditionOptimizer` keeps just one copy so the executor evaluates it once.

#### c. Optionally swap join sides

If join reordering remains enabled, `CommuteJoin` can flip the join inputs so the optimizer aligns with the desired build/probe orientation (for example, making sure the smaller table builds the hash table or matching a distribution strategy):

```
# Before                     # After (smaller table builds)
customers ──⋈── recent_orders   recent_orders ──⋈── customers
```

### 3. Pick the physical plan and distribution

`CascadesOptimizer` picks between hash, merge, or nested-loop implementations using Databend’s cost model. The pipeline also decides whether the plan should remain local; if a warehouse cluster is available and joins are large, broadcast exchanges are rewritten into hash shuffles so work spreads evenly. Final cleanups drop redundant projections and unused CTEs.

## Observability

- `EXPLAIN` shows the final optimized plan.
- `EXPLAIN PIPELINE` reveals the execution topology.
- `SET enable_optimizer_trace = 1` records every optimizer step in the query log.
