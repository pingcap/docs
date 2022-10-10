---
title: Troubleshoot OOM Issues
summary: Learn how to diagnose and resolve TiDB Out Of Memory (OOM) issues.
---

# Troubleshoot OOM Issues

This document describes how to troubleshoot TiDB Out Of Memory (OOM) problems, including phenomenon, cuases, and solutions.

## General troubleshooting process

When you troubleshoot OOM issues, follow this process:

1. First, confirm whether it is an OOM issue. Execute the following command to check the operating system logs. If the result has the OOM-killer logs near the time point when the problem occurs, then it is likely that an OOM problem has occured.

    ```shell
    dmesg -T | grep tidb-server
    ```

    The following is an example of the result:

    ```shell
    ......
    Mar 14 16:55:03 localhost kernel: tidb-server invoked oom-killer: gfp_mask=0x201da, order=0, oom_score_adj=0
    Mar 14 16:55:03 localhost kernel: tidb-server cpuset=/ mems_allowed=0
    Mar 14 16:55:03 localhost kernel: CPU: 14 PID: 21966 Comm: tidb-server Kdump: loaded Not tainted 3.10.0-1160.el7.x86_64 #1
    Mar 14 16:55:03 localhost kernel: Hardware name: QEMU Standard PC (i440FX + PIIX, 1996), BIOS rel-1.14.0-0-g155821a1990b-prebuilt.qemu.org 04/01/2014
    ......
    Mar 14 16:55:03 localhost kernel: Out of memory: Kill process 21945 (tidb-server) score 956 or sacrifice child
    Mar 14 16:55:03 localhost kernel: Killed process 21945 (tidb-server), UID 1000, total-vm:33027492kB, anon-rss:31303276kB, file-rss:0kB, shmem-rss:0kB
    Mar 14 16:55:07 localhost systemd: tidb-4000.service: main process exited, code=killed, status=9/KILL
    ......
    ```

2. After confirming that it is an OOM issue, you can further investigate whether the OOM is caused by a deployment issue or a database issue.

    - If the OOM is caused by deployment issues, you need to investigate the resource configuration and impact of hybrid deployment.
    - If the OOM is caused by a database problem, the following are some possible causes:
        - TiDB handles large data traffic, such as large queries, large writes, and data import.
        - TiDB is in a high concurrency scenario, where multiple SQL concurrency consumes resources or operator concurrency is high.
        - TiDB has a memory leak and resources are not being freed.

## Typical OOM phenomena

Typical failure phenomena of OOM include (but are not limited to) the following:

- The client side reports the following error: `SQL error, errno = 2013, state = 'HY000': Lost connection to MySQL server during query`

- Check Grafana, you can find the following problems.
    - **TiDB** > **Server** > **Memory Usage** 达到某一阈值的锯齿形 reaches a certain threshold of sawtooth
    - **TiDB** > **Server** > **Uptime** suddenly and quickly becomes 0.
    - **TiDB-Runtime** > **Memory Usage** shows that `estimate-inuse` keeps rising.
    - **TiDB** > **Server** > **Memory Usage** shows that process/heapInuse keeps rising.

- Check `tidb.log`, you can find the following log entries:
    - Alerm about OOM: [WARN] [memory_usage_alarm.go:139] ["tidb-server has the risk of OOM. Running SQLs and heap profile will be recorded in record path"]. For more information, see [`memory-usage-alarm-ratio`](/system-variables.md#tidb_memory_usage_alarm_ratio).
    - Log entries about restart: [INFO] [printer.go:33] ["Welcome to TiDB."]

## Typical causes and solutions

You can troubleshoot TiDB OOM issues in the following ways:

- [Deployment issues](#deployment-issues)
- [Database issues](#database-issues)
- [Client side issues](#client-side-issues)

### Deployment issues

The following are common causes of OOM problems caused by deployment issues:

- The memory capacity of the operating system is too small, and results in insufficient memory.
- The TiUP [`resource_control`](/tiup/tiup-cluster-topology-reference.md#global) configuration is not appropriate.
- In the case of hybrid deployments (meaning that TiDB and other applications are deployed on the same server), TiDB is killed accidentially by the OOM-killer.

### Database issues

This section describes the OOM issues and solutions caused by database issues.

> **Note:**
>
> If SQL returns an error: `ERROR 1105 (HY000): Out Of Memory Quota![conn_id=54]`, it is because you have configured [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query). This error is caused by the memory usage control behavior of the database. You can safely ignore it.

#### Executing SQL statements consumes too much memory on TiDB nodes

You can take the following measures to reduce the memory usage of SQL, depending on the different causes of OOM issues.

- 如果 SQL 的执行计划不优，比如由于缺少合适的索引、统计信息过期、优化器 bug 等原因，会导致选错 SQL 的执行计划，进而出现巨大的中间结果集累积在内存中。这种情况下可以考虑采取以下措施：
- If the execution plan of SQL is not optimal, for example, due to lack of proper indexes, outdated statistics, and optimizer bugs, a wrong execution plan of SQL might be selected. A huge intermediate result set will then be accumulated in the memory. In this case, consider the following measures.
    - Add appropriate indexes
    - Use the [disk spill](/configure-memory-usage.md#disk-spill) feature for execution operators
    - Adjust the JOIN order between tables
    - Use hints to optimize SQL

- 一些算子和函数不支持下推到存储层，导致出现巨大的中间结果集累积。此时可能需要改写业务 SQL，或使用 hint 进行调优，来使用可下推的函数或算子。
- Some operators and functions do not support pushing down to the storage level, resulting in a huge accumulation of intermediate result sets. In this case, you need to refine the business SQL statements or use hints to tune and use the functions or operators that can be pushed down.

- 执行计划中存在算子 HashAgg。HashAgg 是多线程并发执行，虽然执行速度较快，但会消耗较多内存。可以尝试使用 `STREAM_AGG()` hint 替代。
- The execution plan contains the operator HashAgg. HashAgg is executed concurrently by multiple threads. It is faster but consumes more memory. You can use the `STREAM_AGG()` hint instead.

- 调小同时读取的 Region 的数量，或降低算子并发度，以避免因高并发导致的内存问题。对应的系统变量包括：
- Reduce the number of regions to be read simultaneously or reduce the concurrency of operators to avoid memory problems caused by high concurrency. The corresponding system variables include:
    - [`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency)
    - [`tidb_index_serial_scan_concurrency`](/system-variables.md#tidb_index_serial_scan_concurrency)
    - [`tidb_executor_concurrency`](/system-variables.md#tidb_executor_concurrency-span-classversion-marknew-in-v50span)

- 问题发生时间附近，session 的并发度过高。此时可能需要添加节点进行扩容。
- The concurrency of sessions is too high near the time point when the problem occurs. In this case, consider scaling up the TiDB nodes.

#### 大事务或大写入在 TiDB 节点上消耗太多内存 Large transactions or large writes consume too much memory on TiDB nodes

需要提前进行内存的容量规划，这是因为执行事务时 TiDB 进程的内存消耗相对于事务大小会存在一定程度的放大，最大可以达到提交事务大小的 2 倍到 3 倍以上。

针对单个大事务，可以通过拆分的方式调小事务大小。
