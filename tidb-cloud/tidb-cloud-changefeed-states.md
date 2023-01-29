---
title: Changefeed States
summary: Learn the meaning of each changefeed state in TiDB Cloud.
---

# Changefeed States

A [changefeed](/tidb-cloud/changefeed-overview.md) is a replication task in TiCDC, which replicates the data change logs of specified tables in a TiDB cluster to the designated downstream. You can run and manage multiple changefeeds in a TiCDC cluster.

The state of a replication task represents the running status of the replication task. During the running of TiCDC, replication tasks might fail with errors, be manually paused, resumed, or reach the specified `TargetTs`. These behaviors can lead to the change of the replication task state. This document describes the states of TiCDC replication tasks and the transfer relationships between states.

The states are described as follows:

- `CREATING`: the replication task is being created.
- `RUNNING`：the replication task runs normally and the checkpoint-ts proceeds normally.
- `EDITING`: the replication task is being edited.
- `PAUSING`: the replication task is being paused.
- `PAUSED`: the replication task is paused.
- `RESUMING`: the replication task is being resumed.
- `DELETING`: the replication task is being deleted.
- `DELETED`: the replication task is deleted.
- `WARNING`: the replication task returns an error. The replication cannot continue due to some recoverable errors. The changefeed in this state keeps trying to resume until the state transfers to `Normal`. The changefeed in this state blocks GC operations.
- `FAILED`: the replication task fails. Due to some unrecoverable errors, the replication task cannot resume and cannot be recovered. The changefeed in this state does not block GC operations.
