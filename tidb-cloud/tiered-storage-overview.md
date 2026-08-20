---
title: Tiered Storage Overview
summary: Learn about tiered storage on TiDB Cloud Essential, Premium, BYOC, including its concept, architecture, use cases, and implementation principles.
---

# Tiered Storage Overview

Tiered storage helps you move infrequently accessed table or partition data to a lower-cost storage tier while keeping SQL semantics unchanged. This page explains the architecture, trade-offs, and scenario guidelines to help you decide when to use Infrequent Access (IA) storage.

> **Note:**
>
> Tiered storage is in **Private Preview** for {{{ .essential }}}, {{{ .premium }}}, and {{{ .byoc }}}. The behavior described on this page reflects the current preview implementation and might change before general availability (GA).

## Introduction

Tiered storage is a **storage tiering capability at the table and partition levels** available in {{{ .essential }}}, {{{ .premium }}}, and {{{ .byoc }}}. It is designed for infrequently accessed data. You can assign a table or partition to the Infrequent Access (IA) storage class. The system stores the complete dataset in remote object storage (such as Amazon S3 or Alibaba Cloud OSS), while keeping only metadata and on-demand cached hot data segments on local storage.

From the application’s perspective, an IA table behaves like a standard table. All query, transaction, backup, and recovery semantics remain unchanged. The primary difference is in the cost-performance tradeoff: local storage usage is significantly reduced, but cold reads (when the required data is not available in the local cache) incur higher latency because data must first be fetched from remote object storage.

Key features:

- **Transparent semantics**: All SQL operations, including `SELECT`, `INSERT`, `UPDATE`, and `DELETE`, behave the same as on standard tables.
- **Lower storage cost**: Data is stored in low-cost object storage, while only hot data is cached locally. In typical scenarios, storage costs can be reduced by approximately 50%.
- **Fine-grained control**: Supports both table-level and partition-level storage tiering. Partition-level settings take precedence over table-level settings.
- **Flexible conversion**: Supports bidirectional conversion between IA and standard storage classes without data loss.
- **Seamless integration**: Fully integrated with Raft Regions, MVCC, BR backup and restore, TiCDC, and other TiDB components.

## Usage scenarios

This section describes the recommended and not recommended scenarios for using IA storage, as well as a checklist to help you decide whether to use IA.

### Recommended scenarios

| Business Scenario | Data Characteristics | Recommended Cold/Hot Boundary |
|-|-|-|
| E-commerce historical orders / financial transactions | Frequent writes, heavy read/write of recent data, rare historical modifications | 6 months |
| Financial vouchers / audit logs / invoices | Write-once, rarely modified, 7-15 year retention | 2 years |
| Application logs / monitoring metrics / API calls | High-throughput writes, frequent recent troubleshooting | 90 days |
| Social media posts / comments / photo metadata | Initial peak, declining over time | 30-90 days |
| Industrial sensors / connected vehicles | Very high write throughput, real-time recent monitoring | 1 year |
| Data warehouse historical analysis | Bulk writes, few updates, historical trend analysis | 90 days |
| AI dialogue history / memory | Session-based writes, high-frequency recent access, historical user profiling | 180 days |
| LLM training datasets | High frequency during training, steep drop-off after completion | Training end + 30 days |
| AI inference logs / results | High-concurrency writes, recent monitoring, historical optimization | 90 days |
| Vector databases | Rare updates, frequent recent queries | 30-90 days |

**General rule of thumb**: Large data volume + decreasing access frequency over time + occasional queries with no strict response time requirement → suitable for IA.

### Not recommended scenarios

- **Hot OLTP tables** with strict latency sensitivity (core online transaction tables sensitive to every millisecond)
- Datasets requiring **frequent large-range scans** (AP queries that continuously access large amounts of cold data)
- Tables that need **frequent switching** between IA and Standard
- Data with **highly scattered** access patterns and almost no locality
- Scenarios where the access pattern does not follow a "decreasing over time" trend

### Decision checklist

Before setting IA, verify each item:

- [ ] The data access frequency of the table/partition has been confirmed to be declining from a business perspective
- [ ] The table can be changed to a partitioned table, because cold/hot data separation is easier to manage with partitioned tables
- [ ] For regular table cold/hot separation, hot data accounts for less than 10% of the table
- [ ] Cold data access frequency is very low, e.g., query QPS does not exceed 10 concurrent (to avoid saturating object storage bandwidth)
- [ ] No need for frequent large-range AP scans on IA tables
- [ ] Cold-read latency is acceptable: a SQL execution may issue multiple remote requests, and latency varies with cache state, request parallelism, and the amount of cold data accessed
- [ ] Awareness that cold reads have read amplification: a single 100-byte record can exhibit up to 30,000× amplification (approximately 3 MiB of cold data)
- [ ] Single query involves no more than 100 MiB of cold data
- [ ] Single query accesses no more than 100 rows of cold data
- [ ] An observation period has been planned (at least one full business day for the first partition)
- [ ] Awareness that switching back IA → Standard takes a long time with significant bandwidth cost

## Implementation principles

This section describes the architecture, data storage hierarchy, read amplification analysis, and LSM-Tree write path of tiered storage.

### Architecture overview

Tiered storage implementation spans the TiDB → TiKV → Object Store three-layer architecture:

```
┌──────────────────────────────────────────────────────────────────┐
│ TiDB Schema Layer                                                 │
│ · STORAGE_CLASS / ENGINE_ATTRIBUTE written to TiDB schema         │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ TiKV Region Management Layer                                     │
│ · IA tables/partitions occupy dedicated regions, avoiding        │
│   hot/cold data in the same shard                                │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ TiKV IA Cache Management Layer (IaManager)                       │
│ · Local cache for cold storage data                              │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ Remote Object Storage (S3/OSS)                                    │
│ · Full SST data organized and stored by segment                  │
└──────────────────────────────────────────────────────────────────┘
```

**Raft ChangeSet ensures consistency**: Storage class changes are replicated to all replicas via Raft ChangeSet. This ensures that every related shard maintains a consistent storage class state across restarts, recovery, splits, and merges, preventing data loss or corruption due to region topology changes.

### Data storage hierarchy

The internal hierarchy of an SSTable from top to bottom:

```
SSTable ──→ Segment ──→ Block ──→ KV Pair
(file)      (1 MiB)     (32 KiB)    (single record)
```

| Layer | Default Size | Role |
|-|-|-|
| **Segment** | 1 MiB | The **minimum unit** TiKV reads from object storage; avoids excessive small requests that could incur API call costs and QPS throttling |
| **Block** | 32 KiB | The basic unit for local file reading, compression, and **memory/disk caching** |

This means a cache miss does not fetch just a single KV record — it loads an entire Segment to local storage. If subsequent queries hit data within the same segment, they benefit from hot-read performance. However, for one-time queries with no subsequent access, the read amplification penalty is relatively high.

### Read amplification analysis

**Read amplification path on a cache miss**:

```Plaintext
User queries 1 record (100 Bytes)
→ Block cache miss
→ TiKV loads segments from 3 LSM levels from object storage
→ Approximately 3 MiB data fetched from object storage to local
→ Read amplification: ~30,000×
```

This amplification manifests differently in two scenarios:

- **With subsequent reuse**: The loaded segment stays in the IA cache; subsequent hits become hot reads, amortizing the initial amplification cost
- **One-time query**: e.g., an ad-hoc analysis running a large-range scan — the loaded data is never reused, making the read cost very high. Additionally, newly loaded data evicts "old data" from the local cache — this old data might be real hot spots, and their eviction can trigger new cache misses, creating a cascading performance impact

Therefore, tiered storage is best suited for **small, concentrated query patterns** rather than frequent large-range scans.

### LSM-Tree write path

The write path remains the same as Standard tables:

```Plaintext
INSERT/UPDATE/DELETE
→ Memtable (hot write, unaffected by IA)
→ L0 SST (hot write, unaffected by IA)
→ L1+ SST (after compaction, opened in IA mode based on storage class)
```

- Writes still enter memtable/L0 first — the local hot path does not directly become a remote write
- L1+ files matching IA conditions are opened in IA mode after reload/compaction
- Hot write paths like `memtable` and `L0` do not directly enter IA
- The primary IA target is the Write CF L1+ layer

## Conversion efficiency

### Standard → IA

Test reference: Approximately 1 TB of logical data (including indexes) completed conversion within 5 minutes, with negligible impact on QPS and latency during the process. Single TiKV CPU increased by about 0.5c and recovered within approximately 5 minutes.

```
TiDB schema takes effect → Schema Manager sync (30s) → TiKV broadcast
→ Region alignment / Split → ChangeSet updates Shard → Reload files
```

### IA → Standard

Test reference: 2.09 TB of logical data (including indexes) took approximately 3 hours 10 minutes (~1.61k regions/hour per TiKV), object storage GET throughput was approximately 1.6 GiB/s. During conversion, Standard partition QPS dropped by about 3.78%, P99 increased by about 18.63%, and single TiKV CPU increased by about 0.5c.

```Plaintext
Same chain as above + full object storage data download to local
```

> These figures are from test environments and do not represent real-world production scenarios. You should obtain accurate data based on your own business testing.
