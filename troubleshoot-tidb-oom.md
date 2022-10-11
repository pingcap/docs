---
title: Troubleshoot OOM Issues
summary: Learn how to diagnose and resolve TiDB Out Of Memory (OOM) issues.
---

# Troubleshoot OOM Issues

This document describes how to troubleshoot TiDB Out Of Memory (OOM) problems, including phenomena, causes, and solutions.

## Overall troubleshooting process

When you troubleshoot OOM issues, follow this process:

1. First, confirm whether it is an OOM issue.

    Execute the following command to check the operating system logs. If the result has the OOM-killer logs near the time point when the problem occurs, then it is likely that an OOM problem has occurred.

    ```shell
    dmesg -T | grep tidb-server
    ```

    The following is an example of the log that contains oom-killer:

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

2. After confirming that it is an OOM issue, you can further investigate whether OOM is caused by a deployment issue or a database issue.

    - If OOM is caused by a deployment issue, you need to investigate the resource configuration and impact of hybrid deployment.
    - If OOM is caused by a database issue, the following are some possible causes:
        - TiDB handles large data traffic, such as large queries, large writes, and data import.
        - TiDB is in a high concurrency scenario, where multiple SQL concurrency consumes resources or operator concurrency is high.
        - TiDB has a memory leak and resources are not freed.

## Typical OOM phenomena

Typical OOM phenomena include (but are not limited to) the following:

- The client side reports the following error: `SQL error, errno = 2013, state = 'HY000': Lost connection to MySQL server during query`

- Check Grafana, and you can find the following problems:
    - **TiDB** > **Server** > **Memory Usage** shows that process/heapInUse keeps rising, and suddenly drops to zero after reaching the threshold.
    - **TiDB** > **Server** > **Uptime** suddenly drops to zero.
    - **TiDB-Runtime** > **Memory Usage** shows that `estimate-inuse` keeps rising.

- Check `tidb.log`, and you can find the following log entries:
    - An alarm about OOM: `[WARN] [memory_usage_alarm.go:139] ["tidb-server has the risk of OOM. Running SQLs and heap profile will be recorded in record path"]`. For more information, see [`memory-usage-alarm-ratio`](/system-variables.md#tidb_memory_usage_alarm_ratio).
    - A log entry about restart: `[INFO] [printer.go:33] ["Welcome to TiDB."]`

## Typical causes and solutions

Depending on the reasons for OOM issues, it can be divided into the following scenarios.

- [Deployment issues](#deployment-issues)
- [Database issues](#database-issues)
- [Client side issues](#client-side-issues)

### Deployment issues

The following are common causes of OOM caused by deployment issues:

- The memory capacity of the operating system is too small.
- The TiUP configuration [`resource_control`](/tiup/tiup-cluster-topology-reference.md#global) is not appropriate.
- In the case of hybrid deployments (meaning that TiDB and other applications are deployed on the same server), TiDB is killed accidentally by the oom-killer.

### Database issues

This section describes the causes and solutions for OOM caused by database issues.

> **Note:**
>
> If you have configured [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query), an error occurs: `ERROR 1105 (HY000): Out Of Memory Quota![conn_id=54]`. It is caused by the memory usage control behavior of the database. You can safely ignore it.

#### Executing SQL statements consumes too much memory

You can take the following measures to reduce the memory usage of SQL statements, depending on the different causes of OOM issues.

- If the execution plan of SQL is not optimal, for example, due to lack of proper indexes, outdated statistics, or optimizer bugs, a wrong execution plan of SQL might be selected. A huge intermediate result set will then be accumulated in the memory. In this case, consider the following measures.
    - Add appropriate indexes
    - Use the [disk spill](/configure-memory-usage.md#disk-spill) feature for execution operators
    - Adjust the JOIN order between tables
    - Use hints to optimize SQL statements

- Some operators and functions do not support pushing down to the storage level, resulting in a huge accumulation of intermediate result sets. In this case, you need to refine the business SQL statements or use hints to tune, and use the functions or operators that support pushing down.

- The execution plan contains the operator HashAgg. HashAgg is executed concurrently by multiple threads, which is faster but consumes more memory. Instead, you can use the `STREAM_AGG()`.

- Reduce the number of regions to be read simultaneously or reduce the concurrency of operators to avoid memory problems caused by high concurrency. The corresponding system variables include:
    - [`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency)
    - [`tidb_index_serial_scan_concurrency`](/system-variables.md#tidb_index_serial_scan_concurrency)
    - [`tidb_executor_concurrency`](/system-variables.md#tidb_executor_concurrency-span-classversion-marknew-in-v50span)

- The concurrency of sessions is too high near the time point when the problem occurs. In this case, consider scaling out the TiDB cluster by adding more TiDB nodes.

#### Large transactions or large writes consume too much memory

You need to plan in advance for memory capacity. TiDB can consume up to two to three times more memory than the size of a committed transaction when processing a transaction.

For a single large transaction, you can split the transaction to make it smaller in size.

#### The process of collecting and loading statistical information consumes too much memory

A TiDB node needs to load statistics into memory after it starts. Since TiDB v6.1.0, [`enable_tidb_stats_cache_mem_quota`](/tidb-configuration-file.md#enable-stats-cache-mem-quota-span-classversion-marknew-in-v610span) has been introduced to improve memory usage for statistical information.

TiDB consumes memory when collecting statistical information. You can control memory usage by the following ways:

- Specify a sampling rate, only collect statistics for specific columns, and reduce analyze concurrency.
- Since TiDB v6.1.0, the system variable [`tidb_mem_quota_analyze`](/system-variables.md#tidb_mem_quota_analyze-span-classversion-marknew-in-v610span) has been introduced to control the maximum memory usage when TiDB updates statistics.

For more information, see [Introduction to Statistics](/statistics.md).

#### Prepared statements are overused

The client side keeps creating prepared statements but does not execute [`deallocate prepare stmt`](/sql-prepared-plan-cache.md#ignore-the-com_stmt_close-command-and-the-deallocate-prepare-statement), which causes memory consumption to continue to rise and eventually triggers TiDB OOM. The reason is that the memory occupied by a prepared statement is not released until the session is closed. This is especially important in the case of long connections.

To solve the problem, consider the following measures:

- Adjust the session lifecycle.
- Adjust the life time of the connection pool.
- Use the system variable [`max_prepared_stmt_count`](/system-variables.md#max_prepared_stmt_count) to control the maximum number of prepared statements in a session.

#### `tidb_enable_rate_limit_action` is not configured properly

The system variable [`tidb_enable_rate_limit_action`](/system-variables.md#tidb_enable_rate_limit_action) controls memory usage effectively when an SQL statement only reads data. If computing operations (such as join or aggregation operations) are required, memory usage might not be under the control of [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query), which increases the risk of OOM.

It is recommended that you disable this system variable. Since TiDB v6.3.0, this system variable is disabled by default.

### Client side issues

If OOM occurs on the client side, investigate the following:

- Check the trend and speed on **Grafana TiDB Details** > **Server** > **Client Data Traffic** to see if there is a network blockage.
- Check whether there is an application OOM caused by wrong JDBC configuration parameters. For example, if the parameter related to streaming read `defaultFetchSize` is incorrectly configured, it can cause data to be heavily accumulated on the client side.

## Diagnostic information to be collected to address OOM issues

To locate an OOM failure, you need to collect the following information:

- Collect the memory-related configuration of the operating system
    - TiUP configuration: `resource_control.memory_limit`
    - Operating system configuration:
        - Memory information: `cat /proc/meminfo`
        - Kernel parameters: `vm.overcommit_memory`
    - NUMA information:
        - `numactl --hardware`
        - `numactl --show`

- Collect the memory-related configuration of the database
    - tidb version
    - `tidb_mem_quota_query`,
    - `memory-usage-alarm-ratio`
    - `mem-quota-query`
    - `oom-action`
    - `tidb_enable_rate_limit_action`
    - `server-memory-quota`
    - `oom-use-tmp-storage`
    - `tmp-storage-path`
    - `tmp-storage-quota`
    - `tidb_analyze_version`

- Check the daily usage of TiDB memory on Grafana: **TiDB** > **Server** > **Memory Usage**

- Check the SQL statements that consume more memory.

    - View SQL statement analysis, slow queries and memory usage from TiDB Dashboard.
    - Check `SLOW_QUERY` and `CLUSTER_SLOW_QUERY` in `INFORMATION_SCHEMA`.
    - Check `tidb_slow_query.log` on each TiDB node.
    - Run `grep "expensive_query" tidb.log` to check the corresponding log entries.
    - Run `EXPLAIN ANALYZE` to check memory usage of operators.
    - Run `SELECT * FROM information_schema.processlist;` to check the value of the  `MEM`column.

- Run the following command to collect TiDB Profile information when memory usage is high:

    ```shell
    curl -G http://{TiDBIP}:10080/debug/zip?seconds=10" > profile.zip
    ```

- Run `grep "tidb-server has the risk of OOM" tidb.log` to check the path of the alert file collected by TiDB Server. The following is an example:

    ```shell
    ["tidb-server has the risk of OOM. Running SQLs and heap profile will be recorded in record path"] ["is server-memory-quota set"=false] ["system memory total"=14388137984] ["system memory usage"=11897434112] ["tidb-server memory usage"=11223572312] [memory-usage-alarm-ratio=0.8] ["record path"="/tmp/0_tidb/MC4wLjAuMDo0MDAwLzAuMC4wLjA6MTAwODA=/tmp-storage/record"]
    ```

## See also

- [TiDB Memory Control](/configure-memory-usage.md)
- [Tune TiKV Memory Parameter Performance](/tune-tikv-memory-performance.md)