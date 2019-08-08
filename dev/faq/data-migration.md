---
title: TiDB Data Migration FAQ
summary: Learn about frequently asked questions (FAQs) about TiDB Data Migration (DM).
category: FAQ
---

# TiDB Data Migration FAQ

This document collects the frequently asked questions (FAQs) about TiDB Data Migration (DM).

## What can I do when a replication task is interrupted with the `invalid connection` error returned?

The `invalid connection` error indicates that anomalies have occurred in the connection between DM and the downstream TiDB database (such as network failure, TiDB restart, TiKV busy and so on) and that a part of the data for the current request has been sent to TiDB.

Because DM has the feature of concurrently replicating data to the downstream in replication tasks, several errors might occur when a task is interrupted. You can check these errors by using `query-status` or `query-error`.

- If only the `invalid connection` error occurs during the incremental replication process, DM retries the task automatically.
- If DM does not or fails to retry automatically because of version problems, use `stop-task` to stop the task and then use `start-task` to restart the task.

## What can I do when a replication task is interrupted with the `driver: bad connection` error returned?

The `driver: bad connection` error indicates that anomalies have occurred in the connection between DM and the upstream TiDB database (such as network failure, TiDB restart and so on) and that the data of the current request has not yet been sent to TiDB at that moment.

When this type of error occurs in the current version, use `stop-task` to stop the task and then use `start-task` to restart the task. The automatic retry mechanism of DM will be improved later.

## What can I do when a replication task is interrupted with failing to get or parse binlog error `get binlog error ERROR 1236 (HY000), binlog checksum mismatch, data may be corrupted` etc. returned?

This error may occur during the incremental replication process of the DM if the binlog file in the upstream exceeds 4 GB, and the DM encounters a replication interrupt in the processing of the file (including interrupt caused by abnormalities in common pause or stop tasks). It is because that the DM needs to store the replicated binlog position. However, MySQL officially uses unit32 to store it, so the offset value of binlog position of the part exceeding 4 GB overflows and a wrong binlog position is stored. After the task or DM-worker is restarted, this wrong binlog position is used to re-parse the binlog or relay log. In this case, you need to follow these steps to manually recover replication:

- First, determine whether the error occurs in the relay log write or the binlog replication/syncer unit replication(by the component information in the log error message). If the error occurs in the relay log module and the breakpoints saved by the binlog replication/syncer unit are correct, you can first stop the task and the DM-worker, then set the binlog position of the relay meta to `4`, and restart the DM-worker to re-pull the relay log. If the relay log writes, the replication will automatically continue from the breakpoint after restarting the task.
- If the relay log writes, and the next file is been written, the error occurs in an invalid binlog position when the binlog replication/syncer unit reads a relay log file exceeding 4 GB. At this time, you can stop the task and set the binlog position to a valid one of the relay log, such as `4`. Note that you need to adjust both the global checkpoint and the binlog position of each table checkpoint. Set the safe-mode of the task to `true` to ensure reentrant execution. Then, you can restart the replication task and observe the status. It works as soon as the larger than 4 GB file is replicated.