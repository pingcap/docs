---
title: Tiered Storage FAQ
summary: Learn about common tiered storage questions on TiDB Cloud Premium and BYOC, including DML, replicas, and object storage outages.
---

# Tiered Storage FAQ

This document answers common questions about Infrequent Access (IA) storage, including DML behavior, replica handling, conversion progress, cache configuration, and operational impacts such as object storage outages.

> **Note:**
>
> Tiered storage is in **Private Preview** for {{{ .premium }}} and {{{ .byoc }}}. The behavior described on this page reflects the current preview implementation and might change before general availability (GA).

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

## How long does a storage class conversion take, and how do I track its progress?

Run `SHOW STORAGE_CLASS TRANSITIONS` while the conversion is in progress. Compare `COMPLETED_REPLICAS` with `TOTAL_REPLICAS` to get the progress, and read `DURATION` for the elapsed time in seconds.

Conversion duration depends mainly on the data volume and the conversion direction. Setting a table to IA updates metadata and is fast, while switching back to Standard downloads all data from object storage and takes much longer. To estimate the duration for your own cluster, query the `DURATION` of similar past conversions in `mysql.tidb_storage_class_transition_history`, filtered on `STATE = 'COMPLETED'`.

For the full column reference and query examples, see [Tiered Storage Observability](/tidb-cloud/tiered-storage-observability.md).

## What if a conversion stays in `RUNNING` and the progress does not increase?

The conversion might be stuck because of a system exception, such as a TiKV rolling restart, temporarily insufficient resources, or short-term object storage unavailability. You can tell the two cases apart by watching `DURATION` and `COMPLETED_REPLICAS` together: if both keep moving, the conversion is progressing normally and the data volume is simply large.

You cannot resolve a stuck conversion yourself. Contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md). After the issue is resolved, the conversion continues without any additional action from you.

## What happens if I run the reverse `ALTER TABLE` before the previous conversion finishes?

The previous conversion is voided. In `SHOW STORAGE_CLASS TRANSITIONS`, the row for that table or partition is replaced by the new conversion: the direction changes, and the progress counts from the beginning again.

The voided conversion is recorded in `mysql.tidb_storage_class_transition_history` with `STATE = 'SUPERSEDED'`. Its `FINISH_TIME` is the start time of the new conversion, and its `COMPLETED_REPLICAS` and `TOTAL_REPLICAS` are the last values observed before it was voided. Because the work already done is discarded, reversing mid-way takes longer overall than waiting for the first conversion to finish.

When you calculate conversion duration statistics, filter on `STATE = 'COMPLETED'`: the `DURATION` of a `SUPERSEDED` record covers only the time until it was voided, not a full conversion.

## Can I increase the local cache for IA data, and does it cost more?

Yes. Select a higher IA cache level in **Overview** > **Capacity** > **Update Capacity** > **Storage Acceleration**. The available levels are **Economy**, **Default**, **Balanced**, and **Deep**. A higher level caches more IA data on local disks, which improves cold-read performance.

It does cost more. On {{{ .premium }}}, a higher cache level increases the billed IA storage amount. On {{{ .byoc }}}, the additional resources are provisioned in your own cloud account and are billed by your cloud provider. The change is a hot update and does not require a restart.

## Does changing the cache level or the segment size rewrite data in object storage?

No. Changing the cache level only adjusts how much data is kept in the local cache, and takes effect as a hot update.

The segment size (`kvengine.ia.segment-size`, available only on {{{ .byoc }}}) only changes the granularity at which data is read from object storage and written to the local cache. SST files are stored in object storage as whole objects and are not organized by segment, so nothing in object storage is rewritten. This parameter takes effect only at startup, so a rolling restart of the TiKV nodes is required, after which the local cache is gradually rebuilt at the new granularity.

## How do I decide whether a table should stay in IA?

Compare `IA_EXEC_COUNT` with `EXEC_COUNT` in the statement summary tables to get the proportion of executions that read IA data, and check the cluster-level **IA Cache Hit Rate** panel.

- If most statements that access the table keep a high cold-read ratio, the cache hit rate is too low for IA. Consider switching the table back to Standard, or raising the cache level.
- If the cold-read ratio is low but a few statements read a large volume each time, optimize those statements instead of switching the whole table back.

## Where can I see the IA cache hit rate?

In the Cloud Console, go to **Monitoring** > **Metrics** > **Instance Overview** and open the **IA Cache Performance** panel group. It includes the cache hit rate, the cache miss rate, the remote read segment count and volume, and the remote read wait time.

A yellow indicator appears when the hit rate drops below 85%. If the cluster has no IA tables, the panels show **No IA data**.
