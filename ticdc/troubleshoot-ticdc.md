---
title: TiCDC FAQ and Troubleshooting
category: reference
summary: Summarizes some common issues and the solutions you might encounter when using TiCDC.
aliases: ['/docs/dev/reference/tools/ticdc/troubleshoot/']
---

# TiCDC FAQ and Troubleshooting

This document summarizes some common issues and the solutions you might encounter when using TiCDC.

## How to select `start-ts` when starting a task?

`start-ts` used in the replication task corresponds to a TSO in the upstream TiDB cluster. The replication task starts to request data from this TSO. Therefore, `start-ts` must meet the following requirements:

- The value of `start-ts` is greater than the current `tikv_gc_safe_point` of the TiDB cluster; otherwise, creating a task triggers an error.
- When you start a task, make sure that all data before `start-ts` are available downstream. In some scenarios, for example, when you replicate data to message queues, you do not need to ensure the consistency of upstream and downstream data. In this case, you can relax this requirement accordingly.

If you do not specify `start-ts` or set `start-ts=0` instead, go to PD to get a current TSO when starting a task. Then start the replication from the TSO.

## What can I do if some tables cannot be replicated when the replication task is started?

When you use `cdc cli changefeed create` to create a replication task, cli first checks whether the upstream tables comply with the [replication restrictions](/ticdc/ticdc-overview.md#restrictions). If there is any table that does not meet the restrictions, you can receive the message `some tables are not eligible to replicate`, with these tables listed in the message.

If you select `Y` or `y`, the replication task continues to be created, and all updates of these tables are automatically ignored during replication. Fo other input, the replication task is not created.

## Troubleshoot replication interrupt

The replication interrupt might occur in the following scenarios:

- The downstream continues to be abnormal, and TiCDC fails after many retries.

    - In this scenario, TiCDC stores the task information. Since TiCDC has set the `service GC safepoint` in PD, the data after the replication task checkpoint are not cleared by TiKV GC within the validity period of `gc-ttl`.

    - Solution: You can resume the replication task using the HTTP API after the downstream gets back to normal.

- The replication cannot continue due to incompatible SQL statements in the downstream.

    - In this scenario, TiCDC stores the task information. Since TiCDC has set the `service GC safepoint` in PD, the data after the replication task checkpoint are not cleared by TiKV GC within the validity period of `gc-ttl`.

    - Solution:

        1. Query the status information of the replication task by executing the `cdc cli changefeed query` command, and record the value of `checkpoint-ts`.
        2. Use the new task configuration file and add the `ignore-txn-start-ts` parameter to skip the transaction corresponding to the specified `start-ts`.
        3. Stop the old replication task using HTTP API.
        4. Execute the `cdc cli changefeed create` command.
        5. Specify the new task configuration file, and set `start-ts` to the value identical to that of `checkpoint-ts` recorded in step 1.

        Now a new replication task is started to resume replication.

## `gc-ttl` and file sorting

Starting from TiDB v4.0.0-rc.1, PD allows external services to set the GC safepoint. Any service can register and update its GC safepoint. PD makes sure that any KV data smaller than the GC safepoint can not be cleared by TiKV GC. TiCDC enables this feature. This ensures that the data consumed by TiCDC in TiKV cannot be cleaned up by the GC in the case of unavailable TiCDC or interrupted replication tasks.

When starting the CDC server, you can specify the TTL of GC safepoint using `gc-ttl`. TTL represents the maximum time that TiCDC saves data smaller than the GC safepoint set by PD after the TiCDC service is stopped. The default value is `86400` (in seconds).

If the replication task is interrupted for a long time, the accumulated unconsumed data is large. OOM might occur at the initial start of TiCDC. In this case, you can enable the file sorting feature provided by TiCDC. This feature sorts files using the file system. To enable this feature, you need to pass `--sort-engine=file` and `--sort-dir=/path/to/sort_dir` into `cdc cli` when creating a replication task. An example is as follows:

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed create --pd=http://10.0.10.25:2379 --start-ts=415238226621235200 --sink-uri="mysql://root:123456@127.0.0.1:3306/" --sort-engine="file" --sort-dir="/data/cdc/sort"
```

> **Note:**
>
> TiCDC v4.0 does not support dynamic modification of file sorting and memory sorting.
