# Tiered Storage on TiDB Cloud Essential — Capability Notes

> This is a supplementary note for customers who have been granted tiered storage on a TiDB Cloud Essential instance through a special allowlist request. Tiered storage is not sold on Essential by default. For the full feature description, always refer to the official tiered storage documentation written for Premium and BYOC.

## Availability

- Tiered storage (Infrequent Access (IA) storage class) is in private preview on **Premium** and **BYOC**, and is not offered on **Essential** by default.
- For essential-tier customers with a strong cold-data cost-reduction need, PingCAP can enable tiered storage on an Essential instance through an allowlist upon request. Once enabled, the DDL syntax and SQL semantics are identical to those documented for Premium.
- The private-preview caveat still applies: behavior might change before general availability (GA).

## What is the same on Essential

All capabilities described in the official documentation work the same on an allowlisted Essential instance:

| Capability | Reference |
|-|-|
| Table-level and partition-level IA storage class, `STORAGE_CLASS` / `ENGINE_ATTRIBUTE` DDL, partition selectors | [Configure and Manage Tiered Storage](/tidb-cloud/tiered-storage-guide.md) |
| Transparent SQL semantics; bidirectional IA ⇄ Standard conversion | [Tiered Storage Overview](/tidb-cloud/tiered-storage-overview.md) |
| Conversion progress and history: `SHOW STORAGE_CLASS TRANSITIONS`, `mysql.tidb_storage_class_transition_history` | [Tiered Storage Observability](/tidb-cloud/tiered-storage-observability.md) |
| Statement-level IA metrics: `ia_remote_read_segment_*` fields in `EXPLAIN ANALYZE`, `IA_EXEC_COUNT` and related columns in statement summary tables, IA fields in slow query details | [Tiered Storage Observability](/tidb-cloud/tiered-storage-observability.md) |
| Storage usage metrics: `Row-based IA Storage` and `Row-based Standard Storage` in the console | [Configure and Manage Tiered Storage](/tidb-cloud/tiered-storage-guide.md) |
| Compatibility with BR, TiCDC, PITR, and IMPORT INTO; TiFlash remaining local | [Tiered Storage Limitations](/tidb-cloud/tiered-storage-limitations.md) |
| Cold-read throttling constraints (≤ 100 MiB/s per SQL, ≤ 1 GiB/s total) | [Tiered Storage Limitations](/tidb-cloud/tiered-storage-limitations.md) |

## What is different on Essential

Two tuning capabilities and one set of observability data are **not available** on Essential:

| Capability | Essential (allowlisted) | Premium | BYOC |
|-|-|-|-|
| IA cache level (local cache ratio): Economy / Default / Balanced / Deep | ✗ Fixed at the system default (`Default`), not adjustable | ✓ Adjustable in the console (requires a separate allowlist) | ✓ |
| IA segment size (`kvengine.ia.segment-size`) | ✗ Fixed at the default 1 MiB | ✗ Not exposed (per current official docs) | ✓ Configurable, rolling restart required |
| Cluster-level IA cache hit rate / miss rate panels in the console | ✗ Not displayed | ✓ Displayed | ✓ Displayed |

Detailed impact:

1. **No local cache ratio adjustment.** On Premium, you can select a higher IA cache level in **Overview** > **Capacity** > **Update Capacity** > **Storage Acceleration** to cache more IA data on local disks and improve cold-read performance. On Essential, the cache level is fixed at the system default and cannot be changed. If cold reads degrade performance, the only self-service options are to narrow the IA scope (switch partitions back to Standard) or optimize the queries.
2. **No segment size adjustment.** The segment size stays at the default 1 MiB. Note that per the current official documentation this parameter is configurable only on BYOC; Premium also uses the default.
3. **No cache hit rate in observability.** The **IA Cache Hit Rate (%)** and **IA Cache Miss Rate (ops/s)** panels are not shown in the Monitoring dashboards on Essential. The tuning loop documented for Premium ("if the hit rate stays below 85%, raise the cache level") does not apply. Instead, judge IA health from the statement-level signals that remain available:
    - Rising `IA_EXEC_COUNT / EXEC_COUNT` ratio in the statement summary tables — more executions are hitting cold data.
    - Rising `AVG_IA_REMOTE_READ_SEGMENT_SIZE` / `AVG_IA_REMOTE_READ_SEGMENT_WAIT_TIME` — heavier or slower cold reads.
    - `IA_remote_read_segment_*` fields in slow query details and `EXPLAIN ANALYZE`.
    - If these signals indicate sustained pressure, contact TiDB Cloud Support; do not assume you can relieve it by enlarging the cache.

## Recommendations for Essential customers

Because the cache is system-fixed and the hit rate is not visible, be more conservative than the general guidance suggests:

- Prefer partition-level IA on partitioned tables; tier only confirmed low-frequency historical partitions, and keep hot and future partitions in Standard.
- Roll out gradually: convert the smallest oldest partition first, observe for at least one full business day using the statement-level metrics above, then proceed.
- Strictly respect the cold-read decision checklist and the throttling constraints in [Tiered Storage Limitations](/tidb-cloud/tiered-storage-limitations.md), since you cannot compensate with a larger cache.
- Avoid large-range scans and `SELECT *` on IA tables; keep queries within no more than 3 IA partitions.
- Keep storage class settings stable; avoid frequent IA ⇄ Standard switching.

## Billing note

On Premium, each cache level applies a distinct IA storage equivalent coefficient (0.9x–1.8x) to billed IA storage usage. On Essential, the cache level is fixed; billing follows the Essential pricing terms in your agreement. See [TiDB Cloud Billing](/tidb-cloud/tidb-cloud-billing.md) for details.
