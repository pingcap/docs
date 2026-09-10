---
title: GET_LINEAGE
summary: Returns upstream or downstream lineage for a table, view, stage, or column. Each returned row represents one source-to-target relationship in the lineage path.
---

# GET_LINEAGE

Returns upstream or downstream lineage for a table, view, stage, or column. Each returned row represents one source-to-target relationship in the lineage path.

## Syntax

```sql
GET_LINEAGE(
    '<object_name>',
    '<object_domain>',
    '<direction>'
    [, <distance> ]
)
```

## Arguments

| Argument | Description |
|----------|-------------|
| `object_name` | Object to start from. Use `[catalog.]database.object` for a table or view, `stage_name` for a stage, and `[catalog.]database.object.column` for a column. Names that omit the catalog or database use the current session values. |
| `object_domain` | Object type: `TABLE`, `VIEW`, `STAGE`, or `COLUMN`. |
| `direction` | `UPSTREAM` traces toward sources; `DOWNSTREAM` traces toward consumers. |
| `distance` | Optional maximum number of hops to traverse, from `1` to `5`. Defaults to `5`. |

Arguments are positional.

## Output Columns

| Column | Type | Description |
|--------|------|-------------|
| `source_object_catalog` | Nullable(String) | Catalog containing the source object; `NULL` for a stage. |
| `source_object_database` | Nullable(String) | Database containing the source object; `NULL` for a stage. |
| `source_object_name` | Nullable(String) | Name of the source object. |
| `source_object_domain` | Nullable(String) | Domain of the source object: `TABLE`, `VIEW`, or `STAGE`. |
| `source_column_name` | Nullable(String) | Source column for column lineage; otherwise `NULL`. |
| `source_status` | String | `ACTIVE`, or `MASKED` when the source column has a masking policy. |
| `target_object_catalog` | Nullable(String) | Catalog containing the target object; `NULL` for a stage. |
| `target_object_database` | Nullable(String) | Database containing the target object; `NULL` for a stage. |
| `target_object_name` | Nullable(String) | Name of the target object. |
| `target_object_domain` | Nullable(String) | Domain of the target object: `TABLE`, `VIEW`, or `STAGE`. |
| `target_column_name` | Nullable(String) | Target column for column lineage; otherwise `NULL`. |
| `target_status` | String | `ACTIVE`, or `MASKED` when the target column has a masking policy. |
| `distance` | Int32 | Number of hops from the requested object. A direct relationship has distance `1`. |
| `process` | Nullable(String) | JSON-formatted metadata about the operation that created the relationship, such as its query ID, query text, user, time, and lineage kind. |

## Examples

This section provides example queries for tracing lineage.

### Find Upstream Tables

This query returns up to two upstream hops for `agg_customer_sales`:

```sql
SELECT
    distance,
    source_object_catalog,
    source_object_database,
    source_object_name,
    source_object_domain,
    target_object_database,
    target_object_name
FROM GET_LINEAGE(
    'lineage_demo.agg_customer_sales',
    'TABLE',
    'UPSTREAM',
    2
)
ORDER BY distance;
```

### Find Downstream Columns

This query traces where `fact_orders.amount` is used:

```sql
SELECT
    distance,
    source_object_name,
    source_column_name,
    target_object_name,
    target_column_name
FROM GET_LINEAGE(
    'lineage_demo.fact_orders.amount',
    'COLUMN',
    'DOWNSTREAM',
    5
)
ORDER BY distance, target_object_name, target_column_name;
```

## Usage Notes

- If the object exists but has no recorded lineage, the function returns no rows.
- Results are filtered according to the current role's object visibility.
- Stage relationships are object-level only; staged file fields are not returned as stable columns.
- System and `information_schema` objects are not recorded as lineage sources.
- External-catalog objects are returned as terminal endpoints and are not traversed further.
- Use [`REFRESH LINEAGE`](/tidb-cloud-lake/sql/refresh-lineage.md) to backfill lineage for views that existed before lineage was enabled.
