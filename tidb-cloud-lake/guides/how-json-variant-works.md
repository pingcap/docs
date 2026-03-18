---
title: How TiDB Cloud Lake JSON (Variant) Works
summary: TiDB Cloud Lake reimagines JSON analytics by pairing a native binary layout with automatic JSON indexing so semi-structured data behaves like first-class columns.
---
See also:

- [Variant Data Type](/tidb-cloud-lake/sql/variant.md)
- [Semi-Structured Functions](/tidb-cloud-lake/guides/load-semi-structured-formats.md)

Databend reimagines JSON analytics by pairing a native binary layout with automatic JSON indexing so semi-structured data behaves like first-class columns.

## Why Variant Matters

Databend keeps JSON flexible while delivering MPP speed: you ingest documents as-is, query with familiar SQL, and the engine stitches together the performance story behind the scenes. Two pillars make it possible:

- A compact **JSONB** layout keeps types visible to the execution engine.
- Automatic **virtual columns**—Databend’s JSON indexes—surface hot paths without manual work.

From storage to queries, the rest of this guide follows how those two ideas turn a raw JSON payload (think `orders.data`) into optimised, typed columns.

## JSON Storage Layout

Databend stores Variant values in JSONB, a binary format optimised for analytics. In practice this means:

- **Typed storage** – numbers, booleans, timestamps, and decimals remain native, so comparisons stay binary-safe.
- **Predictable layout** – fields carry length prefixes and canonical key order, eliminating reparsing overhead.
- **Zero-copy access** – operators read JSONB buffers directly during scans and sorts instead of rebuilding JSON text.

Every Variant column keeps the raw JSONB document for fidelity. When paths like `data['user']['id']` show up repeatedly, Databend tucks them into typed sidecar columns ready for pushdown.

## Automatic JSON Index Generation

When new data lands in Databend, a lightweight indexing pipeline immediately scans the JSON blocks to discover hot paths worth materialising as virtual columns—Databend’s built-in JSON indexes.

### Ingestion Flow

Databend inspects the incoming batch and converts recurring access patterns into typed columns:

```
┌───────────────────────────────────────────────┐
│ Variant Ingestion Flow                        │
├──────────────┬────────────────────────────────┤
│ Sample Rows  │ Peek at the first rows in block │
│ Detect Paths │ Keep stable leaf key paths      │
│ Infer Types  │ Pick native column types        │
│ Materialize  │ Write values to virtual Parquet │
│ Register     │ Attach metadata to base column  │
└──────────────┴────────────────────────────────┘
```

### Lightweight by Design

The pipeline relies on a handful of lightweight heuristics:

```
┌─────────────────────────────┬──────────────────────────────────────────────┐
│ Step                        │ Heuristic                                    │
├─────────────────────────────┼──────────────────────────────────────────────┤
│ Sampling                    │ Inspect only the first 10 rows of each block │
│ Null & non-leaf filtering   │ Skip paths dominated by NULL or pointing to  │
│                             │ objects/arrays                               │
│ Stability check             │ Promote only leaf paths that stay consistent │
│                             │ across the sample (max 1,000 per block)      │
│ Deduplication               │ Use hashing to avoid analysing the same path │
│                             │ repeatedly                                    │
│ Fallback                    │ Keep the original JSONB document when no     │
│                             │ candidate survives                           │
└─────────────────────────────┴──────────────────────────────────────────────┘
```

The result: you load JSON once, and recurring patterns quietly turn into optimised, typed columns with no DDL and no tuning.

### Virtual Columns Are Automatic JSON Indexes

In this context, a “virtual column” is simply **Databend’s JSON index**. The ingestion flow decides whether a path such as `data['items'][0]['price']` is stable enough, infers a native type, and writes those values to a columnar sidecar with metadata—no DDL, no knobs. Nested JSON remains in compact JSONB form, while primitive paths become native numbers, strings, or booleans.

```
Raw JSON block ──(auto sampling)──▶ Candidate paths ──(stable?)──▶ JSON index
```

Instead of building a separate B-tree, Databend snapshots the values for a JSON path into a columnar structure:

```
JSON Path    ───────────▶  Virtual Column (typed values + stats + location)
```

During queries the planner can jump directly to those pre-extracted values, just like hitting an index, while still falling back to the full JSON if an index entry is missing.

### JSON Index Metadata

Metadata stored alongside each block summarises the extra columns:

```
┌────────────────────────────┬───────────────────────┐
│ Virtual Column Metadata    │ Example               │
├────────────────────────────┼───────────────────────┤
│ Column Id & JSON Path      │ v123 -> ['user']['id'] │
│ Type Code                  │ UInt64 / String       │
│ Byte Offset & Length       │ Where values live     │
│ Row Count                  │ Matches base block    │
│ Statistics                 │ Min / Max / NDV       │
└────────────────────────────┴───────────────────────┘
```

The writer packages these details into the table snapshot and stores the sidecar alongside the main block. Each entry remembers the JSON path, native type, byte offsets, and statistics so Databend can jump straight to the extracted values—or fall back to the original JSON—on demand.

## Query Execution with JSON Indexes

Once the indexes exist, the read path reduces to three quick decisions:

```
┌──────────────┐   rewrite paths   ┌────────────────────┐
│ SQL Planner  │------------------>│ Virtual Column Map │
└──────┬───────┘                   └─────────┬──────────┘
       │ pushdown request                   │ per-block check
       ▼                                    ▼
┌──────────────┐   has virtual?   ┌────────────────────┐
│ Fuse Storage │----------------->│ Virtual File Read  │
└──────┬───────┘        │        └─────────┬──────────┘
       │ no             └------------------┘ fallback
       ▼
┌──────────────┐
│ JSONB Reader │
└──────┬───────┘
       ▼
┌──────────────┐
│ Query Output │
└──────────────┘
```

- During planning, Databend rewrites calls such as `get_by_keypath` into direct virtual-column reads whenever metadata says an index exists.
- Storage hits the virtual column when it exists and reads only that Parquet slice, and it can even skip the original JSON column when every requested path is indexed.
- Otherwise it falls back to evaluating `get_by_keypath` on the JSONB column, keeping semantics intact.
- Filters, projections, and statistics operate on native types instead of reparsing JSON strings.

Behind the scenes Databend keeps track of which JSON path produced each virtual column, so it knows exactly when the raw document can be skipped and when it needs to re-open it.

## Working with Variant Data

With indexing handled behind the scenes, you interact with Variant columns using familiar syntax and functions.

### Inspect Virtual Columns

Use [`SHOW VIRTUAL COLUMNS`](/tidb-cloud-lake/sql/show-virtual-columns.md) to list the automatically generated virtual columns for a table when you want to verify what JSON paths Databend has materialised.

### Access Syntax

Databend understands both Snowflake-style and PostgreSQL-style selectors; whichever style you prefer, the engine routes them through the same key-path parser and reuses the JSON indexes. Continuing with an `orders` example, you can reach nested fields like this:

```sql title="Snowflake-style examples"
SELECT data['user']['profile']['name'],
       data:user:profile.settings.theme,
       data['items'][0]['price']
FROM orders;
```

```sql title="PostgreSQL-style examples"
SELECT data->'user'->'profile'->>'name',
       data#>>'{user,profile,settings,theme}',
       data @> '{"user":{"id":123}}'
FROM orders;
```

### Function Highlights

Beyond path accessors, Databend ships a rich Variant toolkit:

- **Parsing & casting**: `parse_json`, `try_parse_json`, `to_variant`, `to_jsonb_binary`
- **Navigation & projection**: `get_path`, `get_by_keypath`, `flatten`, arrow (`->`, `->>`), path (`#>`, `#>>`) and containment operators (`@>`, `?`)
- **Modification**: `object_insert`, `object_remove_keys`, concatenation (`||`), `array_*` helpers
- **Analytics**: `json_extract_keys`, `json_length`, `jsonb_array_elements`, aggregates such as `json_array_agg`

All functions operate directly on JSONB buffers inside the vectorised engine.

## Performance Characteristics

- Internal benchmarks vs. raw JSON scanning:
  - Single-path lookups: **≈3× faster**, **≈26×** less data scanned.
  - Multi-path projections: **≈1.4× faster**, **≈5.5×** less data read.
  - Predicate pushdown composes with bloom/inverted indexes to prune blocks.
- The steadier the JSON shape, the more paths qualify for indexing.

## Databend Advantages for Variant Data

- **Snowflake-compatible surface area** – Bring existing queries and UDFs over intact.
- **Native JSONB execution** – Typed encoding plus vectorised operators avoid string shuffling.
- **Automatic JSON indexes** – Sampling, metadata, and pushdown make semi-structured data feel structured.
- **Operational efficiency** – Virtual blocks share lifecycle tooling with regular Fuse blocks, keeping storage and compute predictable.

With automatic JSON indexing, Databend narrows the gap between flexible documents and high-performance analytics—semi-structured data becomes a first-class citizen in your warehouse.
