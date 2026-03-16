---
title: How Fuse Engine Works
---

## Fuse Engine

Fuse Engine is Databend's core storage engine, optimized for managing **petabyte-scale** data efficiently on **cloud object storage**. By default, tables created in Databend automatically use this engine (`ENGINE=FUSE`). Inspired by Git, its snapshot-based design enables powerful data versioning (like Time Travel) and provides **high query performance** through advanced pruning and indexing.

This document explains its core concepts and how it works.


## Core Concepts

Fuse Engine organizes data using three core structures, mirroring Git:

*   **Snapshots (Like Git Commits):** Immutable references defining the table's state at a point in time by pointing to specific Segments. Enables Time Travel.
*   **Segments (Like Git Trees):** Collections of Blocks with summary statistics used for fast data skipping (pruning). Can be shared across Snapshots.
*   **Blocks (Like Git Blobs):** Immutable data files (Parquet format) holding the actual rows and detailed column-level statistics for fine-grained pruning.


```
                         Table HEAD
                             │
                             ▼
     ┌───────────────┐     ┌───────────────┐     ┌───────────────┐
     │  SEGMENT A    │◄────│  SNAPSHOT 2   │────►│  SEGMENT B    │
     │               │     │ Previous:     │     │               │
     └───────┬───────┘     │ SNAPSHOT 1    │     └───────┬───────┘
             │             └───────────────┘             │
             │                     │                     │
             │                     ▼                     │
             │             ┌───────────────┐             │
             │             │  SNAPSHOT 1   │             │
             │             │               │             │
             │             └───────────────┘             │
             │                                           │
             ▼                                           ▼
     ┌───────────────┐                           ┌───────────────┐
     │   BLOCK 1     │                           │   BLOCK 2     │
     │ (cloud.txt)   │                           │(warehouse.txt)│
     └───────────────┘                           └───────────────┘
```



## How Writing Works

When you add data to a table, Fuse Engine creates a chain of objects. Let's walk through this process step by step:

### Step 1: Create a table

```sql
CREATE TABLE git(file VARCHAR, content VARCHAR);
```

At this point, the table exists but contains no data:

```
(Empty table with no data)
```

### Step 2: Insert first data

```sql
INSERT INTO git VALUES('cloud.txt', '2022/05/06, Databend, Cloud');
```

After the first insert, Fuse Engine creates the initial snapshot, segment, and block:

```
         Table HEAD
             │
             ▼
     ┌───────────────┐
     │  SNAPSHOT 1   │
     │               │
     └───────┬───────┘
             │
             ▼
     ┌───────────────┐
     │  SEGMENT A    │
     │               │
     └───────┬───────┘
             │
             ▼
     ┌───────────────┐
     │   BLOCK 1     │
     │ (cloud.txt)   │
     └───────────────┘
```

### Step 3: Insert more data

```sql
INSERT INTO git VALUES('warehouse.txt', '2022/05/07, Databend, Warehouse');
```

When we insert more data, Fuse Engine creates a new snapshot that references both the original segment and a new segment:

```
                         Table HEAD
                             │
                             ▼
     ┌───────────────┐     ┌───────────────┐     ┌───────────────┐
     │  SEGMENT A    │◄────│  SNAPSHOT 2   │────►│  SEGMENT B    │
     │               │     │ Previous:     │     │               │
     └───────┬───────┘     │ SNAPSHOT 1    │     └───────┬───────┘
             │             └───────────────┘             │
             │                     │                     │
             │                     ▼                     │
             │             ┌───────────────┐             │
             │             │  SNAPSHOT 1   │             │
             │             │               │             │
             │             └───────────────┘             │
             │                                           │
             ▼                                           ▼
     ┌───────────────┐                           ┌───────────────┐
     │   BLOCK 1     │                           │   BLOCK 2     │
     │ (cloud.txt)   │                           │(warehouse.txt)│
     └───────────────┘                           └───────────────┘
```

## How Reading Works

When you query data, Fuse Engine uses smart pruning to find your data efficiently:

```
Query: SELECT * FROM git WHERE file = 'cloud.txt';

                         Table HEAD
                             │
                             ▼
     ┌───────────────┐     ┌───────────────┐     ┌───────────────┐
     │  SEGMENT A    │◄────│  SNAPSHOT 2   │────►│  SEGMENT B    │
     │    CHECK      │     │               │     │    CHECK      │
     └───────┬───────┘     └───────────────┘     └───────────────┘
             │                                          ✗
             │                                    (Skip - doesn't contain
             │                                     'cloud.txt')
             ▼
     ┌───────────────┐
     │   BLOCK 1     │
     │    CHECK      │
     └───────┬───────┘
             │
             │ ✓ (Contains 'cloud.txt')
             ▼
        Read this block
```

### Smart Pruning Process

```
┌─────────────────────────────────────────┐
│ Query: WHERE file = 'cloud.txt'         │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│ Check SEGMENT A                         │
│ Min file value: 'cloud.txt'             │
│ Max file value: 'cloud.txt'             │
│                                         │
│ Result: ✓ Might contain 'cloud.txt'     │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│ Check SEGMENT B                         │
│ Min file value: 'warehouse.txt'         │
│ Max file value: 'warehouse.txt'         │
│                                         │
│ Result: ✗ Cannot contain 'cloud.txt'    │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│ Check BLOCK 1 in SEGMENT A              │
│ Min file value: 'cloud.txt'             │
│ Max file value: 'cloud.txt'             │
│                                         │
│ Result: ✓ Contains 'cloud.txt'          │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│ Read only BLOCK 1                       │
└─────────────────────────────────────────┘
```

## Snapshot-Based Features

Fuse Engine's snapshot architecture enables powerful data management capabilities:

### Time Travel

Query data as it existed at any point in time. Enables data branching, tagging, and governance with complete audit trails and error recovery.

### Zero-Copy Schema Evolution

Modify your table's structure (add columns, drop columns, rename, change types) **without rewriting any underlying data files**.

- Changes are metadata-only operations recorded in new Snapshots.
- This is instantaneous, requires no downtime, and avoids costly data migration tasks. Older data remains accessible with its original schema.


## Advanced Indexing for Query Acceleration (Fuse Engine)

Beyond basic block/segment pruning using statistics, Fuse Engine offers specialized secondary indexes to further accelerate specific query patterns:

| Index Type          | Brief Description                                         | Accelerates Queries Like...                         | Example Query Snippet                   |
| :------------------ | :-------------------------------------------------------- | :-------------------------------------------------- | :-------------------------------------- |
| **Aggregate Index** | Pre-computes aggregate results for specified groups       | Faster `COUNT`, `SUM`, `AVG`... + `GROUP BY`          | `SELECT COUNT(*)... GROUP BY city`      |
| **Full-Text Index** | Inverted index for fast keyword search within text        | Text search using `MATCH` (e.g., logs)              | `WHERE MATCH(log_entry, 'error')`     |
| **JSON Index**      | Indexes specific paths/keys within JSON documents       | Filtering on specific JSON paths/values             | `WHERE event_data:user.id = 123`      |
| **Bloom Filter Index** | Probabilistic check to quickly skip non-matching blocks | Fast point lookups (`=`) & `IN` list filtering      | `WHERE user_id = 'xyz'` |



## Comparison: Databend Fuse Engine vs. Apache Iceberg

_**Note:** This comparison focuses specifically on **table format features**. As Databend's native table format, Fuse evolves, aiming to improve **usability and performance**. Features shown are current; expect changes._

| Feature                 | Apache Iceberg                     | Databend Fuse Engine                 |
| :---------------------- | :--------------------------------- | :----------------------------------- |
| **Metadata Structure**  | Manifest Lists -> Manifest Files -> Data Files | **Snapshot** -> Segments -> Blocks   |
| **Statistics Levels**   | File-level (+Partition)            | **Multi-level** (Snapshot, Segment, Block) → Finer pruning |
| **Pruning Power**       | Good (File/Partition stats)      | **Excellent** (Multi-level stats + Secondary indexes) |
| **Schema Evolution**    | Supported (Metadata change)        | **Zero-Copy** (Metadata-only, Instant) |
| **Data Clustering**     | Sorting (On write)     | **Automatic** Optimization (Background) |
| **Streaming Support**   | Basic streaming ingestion          | **Advanced Incremental** (Insert/Update tracking) |