---
title: Tiered Storage Limitations
summary: Learn about limitations, throttling, compatibility, and query performance uncertainty of tiered storage on TiDB Cloud Premium or BYOC.
---

# Tiered Storage Limitations

This document describes the current limitations and operational impact of Infrequent Access (IA) storage, including feature constraints, cold-read throttling, tool compatibility, and query performance uncertainty.

> **Note:**
>
> Tiered storage is in **Private Preview** for {{{ .premium }}} and {{{ .byoc }}}. The behavior described on this page reflects the current preview implementation and might change before general availability (GA).

## Feature limitations

| Limitation | Description |
|-|-|
| Hash / Key partitions | Cannot be set to IA |
| Index-independent setting | Cannot set IA on indexes independently |
| TTL auto-tiering | Automatic cold/hot tiering based on business fields is not supported |
| Syntax conflict | `STORAGE_CLASS` and `ENGINE_ATTRIBUTE` cannot be specified simultaneously |
| Partition selector mixing | `names_in` / `less_than` / `values_in` cannot be used simultaneously |
| TiFlash | Does not follow IA; data always remains local |
| Cache level scope | The IA cache level applies to the whole cluster. You cannot set a different cache level for an individual table or partition |
| Segment size adjustment | `kvengine.ia.segment-size` can be changed only on {{{ .byoc }}}, and takes effect only after a rolling restart of the TiKV nodes |
| Cache level provisioning | A cache level change takes effect as a hot update, but the underlying resources are provisioned automatically by TiDB Cloud, which might take some time |

## Access throttling constraints

Since shared physical clusters have limited object storage bandwidth, IA cold storage access must comply with the following limits:

| Constraint dimension | Limit | Reason |
|-|-|-|
| Single SQL cold read throughput | ≤ 100 MiB/s | Prevents one query from consuming excessive bandwidth |
| Total concurrent cold read throughput | ≤ 1 GiB/s (≤ 10 concurrent) | Protects other tenants in the cluster |
| TiKV single miss load size | ≤ ~3 MiB (estimated) | Segments from 3 LSM levels |

> **Note:**
>
> A single TiKV miss does not represent a single query miss! For example, a query may involve multiple (e.g., 1000) TiKV misses. If 5 TiKV nodes serve the query, each TiKV averages 200 misses, leading to 200 remote cold data queries. Although concurrent within each TiKV, 200 misses take a very long time, so the final query latency can be extremely high.

**If your business involves sustained heavy access to cold data, IA is not recommended; revert the table to Standard storage.** To ensure system stability, hard throttling for cold data access will be added in a future technical release. For now, you must comply with the constraints above.

You can monitor single SQL cold data access volume via the `IA Remote Read Segment Size` panel in Cloud Console → Monitoring → Diagnosis → Slow Query → Coprocessor. To monitor IA cache behavior for the whole cluster, use the **IA Cache Performance** panels described in [Tiered Storage Observability](/tidb-cloud/tiered-storage-observability.md).

## Impact on peripheral tools

| Tool | Impact | Compatibility |
|-|-|-|
| **TiCDC** | Logical data semantics unchanged; init scan/reading old data may have higher latency; region changes handled as normal | Compatible |
| **BR backup & restore** | Preserves storage class metadata; IA tables continue to load under IA semantics after restore | Compatible |
| **IMPORT INTO** | Imported data transitions to IA via flush/compaction; large-range validation after import may encounter cold cache | Compatible |
| **PITR** | Preserves storage class metadata; schema manager re-syncs after restore | Compatible |

## Risk isolation mechanisms

After setting IA on a table, the system uses the following measures to isolate IA and non-IA tables:

**Region level**:

- IA tables/partitions occupy dedicated regions, triggering necessary splits
- Adjacent regions with different storage classes are restricted from merging, preventing hot/cold data mixing
- A single region is either entirely IA or entirely non-IA

**Compute layer**:

- Standard and IA tables have no isolation at the compute layer — TiDB does not have separate isolation strategies for the two table types

**Storage layer**:

- Cold read rate limiting

> **Note:**
>
> Shared resources (CPU, network, local disk, object storage bandwidth) cannot be fully isolated. In extreme cases, a large IA scan may still affect other tenants. This is the fundamental reason for the access throttling constraints.

## Emergency recovery methods

If issues arise with IA tables, you and the TiDB Cloud team can use the following methods:

| Method | Scenario | Priority | Description |
|-|-|-|-|
| IA → Standard switch-back | You find performance unacceptable | **Your primary choice** | System reloads data locally, bypassing the remote path |
| **Flow Control (already available)** | Control traffic between IA tables and object storage | TiDB Cloud team's choice | Rate-limiting protects cluster stability; managed by the TiDB Cloud team |
| Contact TiDB Cloud Support | A storage class conversion is stuck: `DURATION` keeps growing while `COMPLETED_REPLICAS` does not increase | Required | You cannot resolve a stuck conversion yourself. For how to detect it, see [Tiered Storage Observability](/tidb-cloud/tiered-storage-observability.md) |

## IA local cache and query performance uncertainty

Tiered storage maintains a local IA data cache (managed by IaManager) to accelerate repeated access to recently accessed cold data. However, the following key facts should be understood:

- **Cache capacity is adjustable, but cache behavior is still system-managed**: You can select an IA cache level in the Cloud Console to control how much IA data is cached on local disks. Eviction policies remain managed by the system: you cannot specify which data stays in the cache, and the cache level applies to the whole cluster rather than to an individual table or partition. Cache hit rates depend on actual access patterns: concentrated access can exceed 95%, while scattered access may fall below 95%.
- **IA query response time is non-deterministic**: When a query hits the local cache, performance is close to Standard tables. However, when data must be loaded from remote object storage (cache miss), each remote request adds approximately 500ms~2s of latency. A single SQL execution may involve multiple remote loads, causing latency to accumulate. Therefore, IA table query response times are not as predictable as Standard tables — the business side should plan accordingly.
- **Recommended: use partitioned tables to precisely control cold data scope**: Use partitioned tables, setting only confirmed low-frequency historical partitions to IA while keeping active partitions as Standard. This limits the cache uncertainty to a well-defined data range, rather than exposing the entire table's query performance to cache miss risk.
- **Increasing cache space means increasing cost**: A higher cache level keeps more IA data on local disks, which consumes more local disk and TiKV resources. On {{{ .premium }}}, a higher cache level increases the billed IA storage amount. On {{{ .byoc }}}, the additional resources are provisioned in your own cloud account, are billed by your cloud provider, and take some time to provision. Balance cold-read performance against cost according to your business needs.

In short: IA storage trades lower cost for query performance uncertainty — this is an inherent design trade-off. Use partitioned tables to precisely manage cold data boundaries and confine this uncertainty to a well-defined scope. If your business has strict predictability requirements for query response times, keep that portion of data in Standard storage.
