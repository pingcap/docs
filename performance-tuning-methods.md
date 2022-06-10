---
title: Performance Analysis and Tuning
summary: Learn how to optimize database system based on database time and how to utilize the TiDB Performance Overview dashboard for performance analysis and tuning.
---

# Performance Analysis and Tuning

This document describes a database time-based approach to system tuning and illustrates how to use the TiDB [Performance Overview dashboard](/grafana-performance-overview-dashboard.md) for performance analysis and tuning.

With the methods described in this document, you can analyze user response time and database time from a global and top-down perspective to confirm whether the bottleneck in user response time is caused by database issues. If the bottleneck is in the database, you can use the database time overview and SQL latency breakdowns to locate the bottleneck and tune performance.

## Performance tuning based on database time

TiDB is constantly measuring and collecting SQL processing paths and database time. Therefore, it is easy to locate database performance bottlenecks in TiDB. Based on database time metrics, you can achieve the following two goals even without data on user response time:

- Determine whether the bottleneck is in TiDB by comparing the average SQL processing latency with the idle time of a TiDB connection in a transaction.
- If the bottleneck is in TiDB, further locate the exact module in the distributed system based on database time overview, color-based performance data, key metrics, resource utilization, and top-down latency breakdowns.

### Is TiDB the bottleneck?

- If the average idle time of TiDB connections in transactions is higher than the average SQL processing latency, the database is not to blame for the transaction latency of applications. The database time takes only a small part of the user response time, indicating that the bottleneck does not lie in the database.

    In this case, check the external components of the database. For example, determine whether there are sufficient hardware resources in the application server, and whether the network latency from the application to the database is excessively high.

- If the average SQL processing latency is higher than the average idle time of TiDB connections in transactions, the bottleneck in transactions is in TiDB, and the database time takes a large percentage of the user response time.

### If the bottleneck is in TiDB, how to locate it?

The following figure shows a typical SQL process. You can see that most SQL processing paths are covered in TiDB performance metrics. The database time is broken down into different dimensions, which are colored accordingly. You can quickly understand the load characteristics and catch the bottlenecks inside the database if any.

![database time decomposition chart](/media/performance/dashboard-diagnostics-time-relation.png)

Database time is the sum of all SQL processing time. A breakdown of the database time into the following three dimensions helps you quickly locate bottlenecks in TiDB:

- By SQL processing type: Determine which type of SQL statement consumes the most database time. The formula is:

    `DB Time = Select Time + Insert Time + Update Time + Delete Time + Commit Time + ...`

- By the 4 steps of SQL processing (get_token/parse/compile/execute): Determine which step consumes the most time. The formula is:

    `DB Time = Get Token Time + Parse Time + Compile Time + Execute Time`

- By executor time, TSO wait time, KV request time, and execution retry time: Determine which execution step constitutes the bottleneck. The formula is:

    `Execute Time ~= TiDB Executor Time + KV Request Time + PD TSO Wait Time + Retried execution time`

## Performance analysis and tuning using the Performance Overview dashboard

This section describes how to perform performance analysis and tuning based on database time using the Performance Overview dashboard in Grafana.

The Performance Overview dashboard orchestrates the metrics of TiDB, PD, and TiKV, and presents each of them in the following sections:

- Database time and SQL execution time overview: Color-coded SQL types, database time by SQL execution phase, and database time of different requests help you quickly identify database load characteristics and performance bottlenecks.
- Key metrics and resource utilization: Contains database QPS, connection information and request command types of the applications and the database, database internal TSO and KV request OPS, and TiDB/TiKV resource usage.
- Top-down latency breakdown: Contains a comparison of query latency and connection idle time, breakdown of query latency, latency of TSO requests and KV requests in SQL execution, and breakdown of TiKV internal write latency, etc.

### Database time and SQL execution time overview

The database time metric is the sum of the latency that TiDB processes SQL per second, which is also the total time that TiDB concurrently processes application SQL requests per second (equal to the number of active connections).

The Performance Overview dashboard provides the following three stacked area graphs. They help you understand database load profile and quickly locate the bottleneck causes in terms of statements, execution phase, and TiKV or PD request type during SQL execution.

- Database Time By SQL Type
- Database Time By SQL Phase
- SQL Execute Time Overview

#### Tune by color

The diagrams of database time breakdown and execution time overview present both expected and unexpected time consumption intuitively. Therefore, you can quickly locate performance bottleneck and learn the load profile. Green and blue areas stand for normal time consumption and requests. If non-green or non-blue areas occupy a significant proportion in these two diagrams, the database time distribution is inappropriate.

- Database Time By SQL Type:

    - Blue: `Select` statement
    - Green: `Update`, `Insert`, `Commit` and other DML statements
    - Red: General SQL types, including `StmtPrepare`, `StmtReset`, `StmtFetch`, and `StmtClose`

- Database Time By SQL Phase: The SQL execution phase is in green and other phases are in red on general. If non-green areas are large, it means much database time is consumed in other phases than the execution phase and further cause analysis is required. A common scenario is that the compile phase shown in orange takes a large area due to unavailability of the execution plan cache feature.
- SQL Execute Time Overview: Green metrics stand for common KV write requests (such as Prewrite and Commit), blue metrics stand for common KV read requests (such as Cop and Get), and metrics in other colors stand for unexpected situations which you need to pay attention. For example, pessimistic lock KV requests are marked red and TSO waiting is marked dark brown. If non-blue or non-green areas are large, it means there is bottleneck during SQL execution. For example:

    - If serious lock conflicts occur, the red area will take a large proportion.
    - If excessive time is consumed in waiting TSO, the dark brown area will take a large proportion.

**Example 1: TPC-C load**

![TPC-C](/media/performance/tpcc_db_time.png)

- Database Time by SQL Type: Most time-consuming statements are commit, update, select and insert statements.
- Database Time by SQL Phase: The most time-consuming phase is SQL execution in green.
- SQL Execute Time Overview: The most time-consuming KV requests in SQL execution are Prewrite and Commit in green.

    > **Note:**
    >
    > It is normal that the total KV request time is greater than the execute time. Because the TiDB executor may send KV requests to multiple TiKVs concurrently, causing the total KV request wait time to be greater than the execute time. In the preceding TPC-C load, TiDB sends Prewrite and Commit requests concurrently to multiple TiKVs when a transaction is committed. Therefore, the total time for Prewrite, Commit and PessimisticsLock requests in this example is obviously longer than the execute time.
    >
    > - The execute time may also be significantly greater than the total time of the KV request plus the tso_wait time. This means that the SQL execution time is spent mostly inside the TiDB executor. Here are two common examples:
    >
        > - Example 1: After TiDB executor reads a large amount of data from TiKV, it needs to do complex association and aggregation inside TiDB, which consumes a lot of time.
        > - Example 2: The application experiences serious write statement lock conflicts. Frequent lock retries result in long `Retried execution time`.

**Example 2: OLTP read intensive load**

![OLTP](/media/performance/oltp_normal_db_time.png)

- Database Time by SQL Type: Major time-consuming statements are `SELECT`, `COMMIT`, `UPDATE`, and `INSERT`, among which `SELECT` consumes most database time.
- Database Time by SQL Phase: Most time is consumed in the execute phase in green.
- SQL Execute Time Overview: In SQL execution phase, pd tso_wait in dark brown, KV Get in blue, and Prewrite and Commit in green are time-consuming.

**Example 3: Read-only OLTP load**

![OLTP](/media/performance/oltp_long_compile_db_time.png)

- Database Time by SQL Type: Mainly are `SELECT` statements.
- Database Time by SQL Phase: Major time-consuming phases are compile in orange and execute in green. Latency in the compile phase is the highest, indicating that TiDB is taking too long to generate execution plans and the root cause needs to be further determined based on the subsequent performance data.
- SQL Execute Time Overview: The KV BatchGet requests in blue consume the most time during SQL execution.

> **Note:**
>
> In example 3, `SELECT` statements need to read thousands of rows concurrently from multiple TiKVs. Therefore, the total time of the BatchGet request is much longer than the execution time.

**Example 4: Lock contention load**

![OLTP](/media/performance/oltp_lock_contention_db_time.png)

- Database Time by SQL Type: Mainly are `UPDATE` statements.
- Database Time by SQL Phase: Most time is consumed in the execute phase in green.
- SQL Execute Time Overview: The KV request PessimisticLock shown in red consumes the most time during SQL execution, and the execution time is obviously longer than the total time of KV requests. This is caused by serious lock conflicts in write statements and frequent lock retries prolong `Retried execution time`. Currently, TiDB does not measure `Retried execution time`.

### TiDB key metrics and cluster resource utilization

#### Query Per Second, Command Per Second, and Prepared-Plan-Cache

The following three panels in Performance Overview present the application load profile, how the application interacts with TiDB, and whether the application fully utilizes TiDB's [execution plan cache](/sql-prepared-plan-cache.md).

- QPS: Short for Query Per Second. It shows the count distribution of SQL statements executed by the application.
- CPS By Type: CPS stands for Command Per Second. Command indicates MySQL protocol-specific commands. A query statement can be sent to TiDB either by a query command or a prepared statement.
- Queries Using Plan Cache OPS: The count that the TiDB cluster hits the execution plan cache per second. Execution plan cache only supports the `prepared statement` command. When execution plan cache is enabled in TiDB, the following three scenarios will occur:

    - No execution plan cache is hit: No execution plan is hit per second. This is because the cached execution plan is cleaned up by the application using the query command, or by calling the StmtClose command after each StmtExecute execution.
    - All execution plan cache is hit: The number of hits per second is equal to the number of times the StmtExecute command is executed per second.
    - Some execution plan cache is hit: The number of hits per second is fewer than the number of executed StmtExecute commands per second. Execution plan cache has limitations. For example, it does not support subqueries and SQL execution plans of subqueries cannot be cached.

**Example 1: TPC-C Load**

The TPC-C load are mainly `UPDATE`, `SELECT`, and `INSERT` statements. The total QPS is equal to the number of StmtExecute per second and the latter is almost equal to Queries Using Plan Cache OPS. Ideally, the client caches the object of the prepared statement it executes. In this way, the cached statement is called directly when a SQL statement is executed. All SQL executions hit the execution plan cache, and there is no need to recompile to generate execution plans.

![TPC-C](/media/performance/tpcc_qps.png)

**Example 2: Execution plan cache unavailable for query commands in read-only OLTP load**

In this load, `Commit QPS` = `Rollback QPS` = `Select QPS`. The application has enabled auto-commit concurrency, and rollback is performed every time a connection is fetched from the connection pool. As a result, these three statements are executed the same number of times.

![OLTP-Query](/media/performance/oltp_long_compile_qps.png)

- The red bold line in the QPS panel stands for failed queries, and the Y-axis on the right shows the number of failed queries. A value other than 0 means the presence of failed queries.
- If the total QPS is equal to the number of queries in the CPS By Type panel, the query command has been executed in the application.
- The Queries Using Plan Cache OPS panel has no data, because prepared plan cache is not enabled and TiDB execution plan cache is unavailable. This means that TiDB needs to parse every query of the application and generate an execution plan again. As a result, the compile time is longer with increasing CPU consumption by TiDB.

**Example 3: Execution plan cache unavailable with prepared statement enabled for OLTP load**

`StmtPreare` times = `StmtExecute` times = `StmtClose` times ~= `StmtFetch` times. The application uses the prepare > execute > fetch > close loop. To prevent data leak, many frameworks call `close` after the `execute` phase. This creates two problems.

- A SQL execution requires four commands and four network round trips.
- Queries Using Plan Cache OPS is 0, indicating zero hit of execution plan cache. The `StmtClose` command clears cached execution plans by default and the next `StmtPreare` command needs to generate the execution plan again.

> **Note:**
>
> As of TiDB v6.0.0, you can prevent the `StmtClose` command from clearing cached execution plans via the global variable (`set global tidb_ignore_prepared_cache_close_stmt=on;`). In this way, there is no need to generate the execution plan again for the next SQL execution.

![OLTP-Prepared](/media/performance/oltp_prepared_statement_no_plan_cache.png)

#### KV/TSO Request OPS and connection information

In the KV/TSO Request OPS panel, you can view the statistics of KV and TSO requests per second. Among the statistics, `kv request total` represents the sum of all requests from TiDB to TiKV. By observing the types of requests from TiDB to PD and TiKV, you can get an idea of the load profile within the cluster.

In the Connection Count panel, you can view the total number of connections and the number of connections per TiDB. The counts help you determine whether the total number of connections is normal and the number of connections per TiDB is even. `active connections` records the number of active connections, which is equal to the database time per second.

**Example 1: Busy load**

![TPC-C](/media/performance/tpcc_kv_conn.png)

In this TPC-C load:

- The total number of KV requests per second is 104,200. The top request types are `PessimisticsLock`, `Prewrite`, `Commit` and `BatchGet` in order of number of requests.
- The total number of connections is 810, which are evenly distributed in three TiDB instances. The number of active connections is 787.1. Therefore, 97% of the connections are active, indicating that the database is the performance bottleneck for this application.

**Example 2: Idle load**

![OLTP](/media/performance/cloud_long_idle_kv_conn.png)

In this load:

- The total number of KV requests per second is 2600 and the number of TSO requests per second is 1100.
- The total number of connections is 410, which are evenly distributed in three TiDB instances. The number of active connections is 2.5, indicating that the database system is relatively idle.

#### TiDB CPU, TiKV CPU, and IO usage

In the TiDB CPU and TiKV CPU/IO MBps panels, you can observe the logical CPU usage and IO throughput of TiDB and TiKV, including average, maximum, and delta (maximum CPU usage minus minimum CPU usage), based on which you can determine the overall CPU usage of TiDB and TiKV.

- Based on the `delta` value, you can determine if CPU usage in TiDB is unbalanced (usually accompanied by unbalanced application connections) and if TiKV has hot spots.
- With an overview of TiDB and TiKV resource usage, you can quickly determine if there are resource bottlenecks in your cluster and whether TiKV or TiDB needs scale-out.

**Example 1: High resource usage in TiDB**

In this load, each TiDB and TiKV is configured with 8 CPUs.

![TPC-C](/media/performance/tidb_high_cpu.png)

- The average, maximum, and delta CPU usage of TiDB are 575%, 643%, and 136%, respectively.
- The average, maximum, and delta CPU usage of TiKV are 146%, 215%, and 118%, respectively. The average, maximum, and delta I/O throughput of TiKV are 9.06 MB/s, 19.7 MB/s, and 17.1 MB/s, respectively.

Therefore, it can be determined that TiDB obviously consumes more CPU, which is near the bottleneck threshold of 8 CPUs. It is recommended that you scale out the TiDB.

**Example 2: High TiKV resource usage**

In the TPC-C load below, each TiDB and TiKV is configured with 16 CPUs.

![TPC-C](/media/performance/tpcc_cpu_io.png)

- The average, maximum, and delta CPU usage of TiDB are 883%, 962%, and 153%, respectively.
- The average, maximum, and delta CPU usage of TiKV are 1288%, 1360%, and 126%, respectively. The average, maximum, and delta I/O throughput of TiKV are 130 MB/s, 153 MB/s, and 53.7 MB/s, respectively.

Therefore, it can be determined that TiKV consumes more CPU, which is expected because TPC-C is a write-intensive scenario. It is recommended that you scale out the TiKV to improve performance.

### Query latency breakdown and key latency metrics

The latency panel provides average values and 99th percentile. The average values help locate the overall bottleneck, while the 99th percentile helps determine whether there is a significant latency jitter and what is the jitter range if any.

#### Duration and Connection Idle Duration

The Duration panel contains the P99 latency of all statements and the average latency of each SQL type. The Connection Idle Duration panel contains the average latency and the P99 latency. Connection idle includes the following two states:

- in-txn: The idle duration when the connection is within a transaction, i.e. the interval between processing the previous SQL and receiving the next SQL statement when the connection is within a transaction.
- not-in-txn: The interval between processing the previous SQL and receiving the next SQL statement when the connection is not within a transaction.

An applications connects to the same database when performing transactions. By comparing the average query latency with the connection idle duration, you can determine if TiDB is the bottleneck for overall system performance or if user response time jitter is caused by TiDB.

- If the application load is not read-only and contains transactions, by comparing the average query latency with `avg-in-txn`, you can determine the time proportion in processing transactions both inside and outside the database, based on which you can locate the bottleneck in user response time. metric, you can compare the average query latency with `avg-not-in-txn`.

In real customer scenarios, it is rare that the bottleneck is outside the database, for example:

- The client server configuration is too low and the CPU resources are not enough.
- HAProxy is used as a TiDB cluster proxy, and the HAProxy CPU resource is not enough.
- HAProxy is used as a TiDB cluster proxy, and the network bandwidth of the HAProxy server is used up under high load.
- The latency from the application server to the database is high. For example, the latency is high between geographically separated public-cloud applications and the TiDB cluster, or between the database DNS equalizer and the TiDB cluster.
- The bottleneck is in client applications. The application server's CPU cores and Numa resources cannot be fully utilized. For example, only one JVM is used to establish thousands of JDBC connections to TiDB.

**Example 1: TiDB is the bottleneck for user response time**

![TiDB is the Bottleneck](/media/performance/tpcc_duration_idle.png)

In this TPC-C load:

- The average latency and P99 latency of all SQL statements are 477 us and 3.13 ms, respectively. The average latencies of the commit statement, insert statement, and query statement are 2.02 ms, 609 ms, and 468 us, respectively.
- The average connection idle time in transactions `avg-in-txn` is 171 us.

It can be determined that the average query latency is significantly greater than `avg-in-txn`, which means the main bottleneck in transactions is inside the database.

**Example 2: The bottleneck in user response time is not in TiDB**

![TiDB is the Bottleneck](/media/performance/cloud_query_long_idle.png)

In this load, the average query latency is 1.69 ms and `avg-in-txn` is 18 ms, indicating that TiDB spends 1.69 ms on average to process a SQL statement in transactions, and then needs to wait for 18 ms to receive the next statement.

It can be determined that the bottleneck of user response time is not in TiDB. This example is in a public cloud environment, where high network latency between the application and the database results in extremely high connection idle time because the application and the database are not in the same region.

#### Parse, Compile, and Execute Duration

In TiDB, there is a [typical processing flow](/sql-tuning-concepts.md) from entering query statements to returning results.

SQL processing in TiDB consists of four stages, `get token`, `parse`, `compile`, and `execute`.

- `get token`: Usually only a few microseconds and can be ignored. The token is limited only when the number of connections to a single TiDB instance reaches the [token-limit](/tidb-configuration-file.md) limit.
- `parse`: The query statements are parsed into abstract syntax tree (AST).
- `compile`: Execution plans are compiled based on the AST and statistics of the `parse` phase. The `compile` phase contains logical optimization and physical optimization. Logical optimization optimizes query plans by rules, such as column pruning based on relational algebra. Physical optimization estimates the cost of the execution plans by statistical information and a cost-based optimizer, and selects the physical execution plan with the lowest cost.
- `execute`: The time consumption depends on the situation. TiDB first waits for the globally unique timestamp TSO. Then the executor constructs the TiKV API request based on the Key range in the operator of the execution plan and distributes it to TiKV. `execute` time includes the TSO wait time, the KV request time, and the time spent by TiDB executor in processing data.

If the application uses the `query` or `StmtExecute` MySQL command interface globally, you can use the following formula to locate the bottleneck in average latency.

```
avg Query Duration = avg Get Token + avg Parse Duration + avg Compile Duration + avg Execute Duration
```
