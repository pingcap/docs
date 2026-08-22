---
title: Tiered Storage FAQ
summary: Learn about common tiered storage questions on TiDB Cloud BYOC/Premium/Essential, including DML, replicas, and object storage outages.
---

# Tiered Storage FAQ

This document answers common questions about Infrequent Access (IA) storage, including DML behavior, replica handling, and operational impacts such as object storage outages.

> **Note:**
>
> Tiered storage is in **Private Preview** for {{{ .essential }}}, {{{ .premium }}}, and {{{ .byoc }}}. The behavior described on this page reflects the current preview implementation and might change before general availability (GA).

## Can IA tables execute `UPDATE`/`DELETE`?

Yes. An `UPDATE` operation first loads the corresponding data from object storage into the IA cache, performs the modification, and writes a new SST file, the same flow as a regular `UPDATE`. Performance is affected by cold reads.

## Can TiFlash replicas of IA tables be set to IA?

No. TiFlash does not follow the IA attribute of the source table.

## What happens to IA tables when the object storage experiences an outage?

IA tables will be affected and become unavailable, since all data resides remotely, read requests must fetch from object storage. Additionally, if object storage bandwidth is saturated, IA read/write performance will also be impacted.

## Can the system tell me which data is cold before I set IA?

TiDB does not provide built-in cold/hot detection tools. You need to assess data access patterns based on your own business knowledge. A general rule of thumb: for time-partitioned tables, older partitions tend to have lower access frequency.

## When data is stored in cold storage (IA tier), are all three replicas stored, or just one copy?

Only one copy is stored on Amazon S3, and all three replicas share the same object.

In the cloud storage engine architecture, SST/blob data files have only one copy on object storage (S3/DFS) to begin with: files are uploaded once by flush/compaction, the S3 key contains no node/replica information, and the three Raft replicas reference the same file id through the Raft-replicated ChangeSet. The three-replica mechanism applies only to Raft logs, metadata, and each node's local cache, never to the data on object storage.

**Cost implications**: The storage volume on S3 is always about 1x the data size (it does not multiply with the replica count). What the IA tier saves is local disk usage on each node; data durability is guaranteed by the object storage itself, independent of the replica count.
