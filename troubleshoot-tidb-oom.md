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

- 如果 OOM 是由于 SQL 的执行计划不优，比如由于缺少合适的索引、统计信息过期、优化器 bug 等原因，导致选错了 SQL 的执行计划，进而出现巨大的中间结果集累积在内存中。这种情况下可以考虑采取以下措施：
    - 添加合适的索引
    - 使用算子的落盘功能
    - 调整表之间的 JOIN 顺序
    - 使用 hint 进行调优

- 一些算子和函数不支持下推到存储层，导致出现巨大的中间结果集累积。此时可能需要改写业务 SQL，或使用 hint 进行调优，来使用可下推的函数或算子。

- 执行计划中存在算子 HashAgg。HashAgg 是多线程并发执行，虽然执行速度较快，但会消耗较多内存。可以尝试使用 `STREAM_AGG()` hint 替代。

- 调小同时读取的 Region 的数量，或降低算子并发度，以避免因高并发导致的内存问题。对应的系统变量包括：
    - [`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency)
    - [`tidb_index_serial_scan_concurrency`](/system-variables.md#tidb_index_serial_scan_concurrency)
    - [`tidb_executor_concurrency`](/system-variables.md#tidb_executor_concurrency-从-v50-版本开始引入)

- 问题发生时间附近，session 的并发度过高。此时可能需要添加节点进行扩容。

