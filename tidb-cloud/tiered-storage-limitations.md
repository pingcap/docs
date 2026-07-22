---
title: Tiered Storage Limitations and Impact
summary: Learn about the limitations, access throttling, tool compatibility, and query performance uncertainty of Tiered Storage on TiDB Cloud Essential.
---

# Tiered Storage Limitations and Impact

> **Note:**
>
> - **Version:** Private Preview
> - **Platform:** TiDB Cloud Essential
> - This document reflects the current system state only. Some behaviors may change when the feature reaches GA.

---

## Feature limitations

| Limitation | Description |
|-|-|
| Hash / Key partitions | Cannot be set to IA |
| Index-independent setting | Cannot set IA on indexes independently |
| TTL auto-tiering | Automatic cold/hot tiering based on business fields is not supported |
| Syntax conflict | `STORAGE_CLASS` and `ENGINE_ATTRIBUTE` cannot be specified simultaneously |
| Partition selector mixing | `names_in` / `less_than` / `values_in` cannot be used simultaneously |
| TiFlash | Does not follow IA; data always remains local |

---

## Access throttling constraints

Since shared physical clusters have limited object storage bandwidth, IA cold storage access must comply with the following limits:

| Constraint Dimension | Limit | Reason |
|-|-|-|
| Single SQL cold read throughput | ≤ 100 MiB/s | Prevents one query from consuming excessive bandwidth |
| Total concurrent cold read throughput | ≤ 1 GiB/s (≤ 10 concurrent) | Protects other tenants in the cluster |
| TiKV single miss load size | ≤ ~3 MiB (estimated) | Segments from 3 LSM levels |

**Note**: A single TiKV miss does not represent a single query miss! For example, a query may involve multiple (e.g., 1000) TiKV misses. If 5 TiKV nodes serve the query, each TiKV averages 200 misses, leading to 200 remote cold data queries. Although concurrent within each TiKV, 200 misses take a very long time, so the final query latency can be extremely high.

**If your business involves sustained heavy access to cold data, IA is not recommended; revert the table to Standard storage.** To ensure system stability, hard throttling for cold data access will be added in a future technical release. For now, you must comply with the constraints above.

You can monitor single SQL cold data access volume via the `IA Remote Read Segment Size` panel in Cloud Console → Monitoring → Diagnosis → Slow Query → Coprocessor.

---

## Impact on peripheral tools

| Tool | Impact | Compatibility |
|-|-|-|
| **TiCDC** | Logical data semantics unchanged; init scan/reading old data may have higher latency; region changes handled as normal | Compatible |
| **BR backup & restore** | Preserves storage class metadata; IA tables continue to load under IA semantics after restore | Compatible |
| **IMPORT INTO** | Imported data transitions to IA via flush/compaction; large-range validation after import may encounter cold cache | Compatible |
| **PITR** | Preserves storage class metadata; schema manager re-syncs after restore | Compatible |

---

## Risk isolation mechanisms

After setting IA on a table, the system uses the following measures to isolate IA and non-IA tables:

**Region Level**:

- IA tables/partitions occupy dedicated regions, triggering necessary splits
- Adjacent regions with different storage classes are restricted from merging, preventing hot/cold data mixing
- A single region is either entirely IA or entirely non-IA

**Compute Layer**:

- Standard and IA tables have no isolation at the compute layer — TiDB does not have separate isolation strategies for the two table types

**Storage Layer**:

- Cold read rate limiting

> Shared resources (CPU, network, local disk, object storage bandwidth) cannot be fully isolated. In extreme cases, a very large IA scan may still affect other tenants. This is the fundamental reason for the access throttling constraints.

---

## Emergency recovery methods

If issues arise with IA tables, you and the TiDB Cloud team can use the following methods:

| Method | Scenario | Priority | Description |
|-|-|-|-|
| IA → Standard switch-back | You find performance unacceptable | **Your primary choice** | System reloads data locally, bypassing the remote path |
| **Flow Control (already available)** | Control traffic between IA tables and S3 | TiDB Cloud team's choice | Rate-limiting protects cluster stability; managed by the TiDB Cloud team |

---

## IA local cache and query performance uncertainty

Tiered Storage maintains a local IA data cache (managed by IaManager) to accelerate repeated access to recently accessed cold data. However, the following key facts should be understood:

- **Cache behavior is system-controlled, not user-configurable**: Cache size and eviction policies are managed uniformly by the system. You cannot adjust cache capacity or specify which data stays in the cache. Cache hit rates depend on actual access patterns — concentrated access can exceed 90%, while scattered access may fall below 90%. Even if only one partition is set to IA, its local cache behavior is still system-managed — you cannot exercise fine-grained control.
- **IA query response time is non-deterministic**: When a query hits the local cache, performance is close to Standard tables. However, when data must be loaded from remote object storage (cache miss), each remote request adds approximately 500ms~2s of latency. A single SQL execution may involve multiple remote loads, causing latency to accumulate. Therefore, IA table query response times are not as predictable as Standard tables — the business side should plan accordingly.
- **Recommended: use partitioned tables to precisely control cold data scope**: Use partitioned tables, setting only confirmed low-frequency historical partitions to IA while keeping active partitions as Standard. This limits the cache uncertainty to a well-defined data range, rather than exposing the entire table's query performance to cache miss risk.
- **Increasing cache space means increasing cost**: In a future product iteration, TiDB Cloud will offer the option to configure larger local cache space for IA tables to improve cold data access efficiency. However, larger cache space requires additional TiKV nodes and local disk resources, incurring corresponding resource costs. You will be able to balance performance and cost according to your business needs.

In short: IA storage trades lower cost for query performance uncertainty — this is an inherent design trade-off. Use partitioned tables to precisely manage cold data boundaries and confine this uncertainty to a well-defined scope. If your business has strict predictability requirements for query response times, keep that portion of data in Standard storage.
