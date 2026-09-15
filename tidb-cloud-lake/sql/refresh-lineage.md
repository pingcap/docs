---
title: REFRESH LINEAGE
summary: Backfills or reconciles lineage for existing views in {{{ .lake }}}.
---

# REFRESH LINEAGE

Backfills or reconciles lineage for existing views in the `default` catalog. Use this command after enabling data lineage on a deployment that already contains views. Views created after lineage is enabled are tracked automatically.

This command requires the global `SUPER` privilege and lineage must be enabled. See [Data Lineage](/tidb-cloud-lake/guides/data-lineage.md#enable-data-lineage).

## Syntax

```sql
REFRESH LINEAGE FOR ALL VIEWS [ DRY RUN ]
```

`DRY RUN` calculates and reports the changes without writing them. Run it first to review the work that a refresh would perform.

## Output Columns

| Column | Description |
|--------|-------------|
| `object_domain` | Object domain; currently `VIEW`. |
| `catalog` | Catalog containing the view; currently `default`. |
| `database` | Database containing the view. |
| `object_name` | View name. |
| `status` | `DRY_RUN`, `REFRESHED`, or `ERROR`. |
| `edge_count` | Number of lineage edges found in the current view definition. |
| `upsert_count` | Number of missing or changed edges to add or update. |
| `delete_count` | Number of stale edges to remove. |
| `error` | Error details when `status` is `ERROR`; otherwise `NULL`. |

Successful views with no changes are omitted from the result.

## Examples

Preview the changes required for existing views:

```sql
REFRESH LINEAGE FOR ALL VIEWS DRY RUN;
```

Apply the changes:

```sql
REFRESH LINEAGE FOR ALL VIEWS;
```

After the command completes, query a view's upstream lineage with [`GET_LINEAGE`](/tidb-cloud-lake/sql/get-lineage.md):

```sql
SELECT
    distance,
    source_object_database,
    source_object_name,
    target_object_database,
    target_object_name
FROM GET_LINEAGE(
    'lineage_demo.sales_view',
    'VIEW',
    'UPSTREAM',
    1
);
```

> **Note:**
>
> To change a logical view definition, use [`CREATE OR REPLACE VIEW`](/tidb-cloud-lake/sql/create-view.md). `ALTER VIEW ... AS ...` is not supported because changing the definition without recreating the view could leave persisted lineage inconsistent.
