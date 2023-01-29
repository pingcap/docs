---
title: Changefeed States
summary: Learn the meaning of each changefeed state in TiDB Cloud.
---

# Changefeed States

A changefeed is a replication task in TiCDC, which replicates the data change logs of specified tables in a TiDB cluster to the designated downstream. You can run and manage multiple changefeeds in a TiCDC cluster.

The state of a replication task represents the running status of the replication task. During the running of TiCDC, replication tasks might fail with errors, be manually paused, resumed, or reach the specified `TargetTs`. These behaviors can lead to the change of the replication task state. This document describes the states of TiCDC replication tasks and the transfer relationships between states.

The states in the preceding state transfer diagram are described as follows:

- `RUNNING`：The replication task runs normally and the checkpoint-ts proceeds normally.
- "FAILED",同步任务失败。由于发生了某些不可恢复的错误，导致同步无法继续进行，并且无法恢复。处于这个状态的 changefeed 不会阻挡 GC 推进。
- "CREATING",创建同步任务 Changefeed 中
- "RESUMING",同步任务 Changefeed 正在从暂停中进行恢复
- "PAUSING",同步任务 Changefeed 任务暂停中
- "PAUSED":The replication task
- "DELETING", 同步任务 Changefeed 正在删除中
- "DELETED", 同步任务 Changefeed 已删除
- "EDITING", 编辑同步任务 Changefeed 中
- "WARNING", 同步任务报错，由于某些可恢复的错误导致同步无法继续进行，处于这个状态的 changefeed 会不断尝试继续推进，直到状态转为 Normal。处于这个状态的 changefeed 会阻挡 GC 推进。

