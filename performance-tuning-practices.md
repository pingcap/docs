---
title: OLTP Load Performance Optimization Practices
summary: This document describes how to perform performance analysis and optimization of OLTP loads.
---

# OLTP Load Performance Optimization Practices

TiDB provides comprehensive performance diagnostics and analysis features, such as the [Top SQL](/dashboard/top-sql.md) and [Continuous Profiling](/dashboard/continuous-profiling.md) features of the TiDB Dashboard, and TiDB [Performance Overview dashboard](/grafana-performance-overview-dashboard.md).

This article describes how to use these features together to analyze and compare the performance of the same OLTP load in seven different runtime scenarios, and demonstrates the optimization process for specific OLTP loads to help you analyze and optimize the performance of TiDB more quickly.

> **Note:**
>
> [Top SQL](/dashboard/top-sql.md) and [Continuous Profiling](/dashboard/continuous-profiling.md) are turned off by default and need to be enabled in advance.

In these scenarios, by running the same application with different JDBC configurations, you can observe how different ways of interacting between the application and the database will affect the overall performance of the system to get a better handle on [best practices for developing Java applications using TiDB](/best-practices/java-app-best-practices.md). practices.md).

## Load Environment

This article uses a bank transaction system OLTP simulation load for demonstration. The following is the simulation environment configuration for this load.

- Development language for load applications: JAVA
- SQL statements involving business: 200 statements in total, 90% of which are SELECT statements, which are typical read-intensive OLTP scenarios.
- Tables involved in transactions: 60 tables in total, 12 tables with modification operations, and 48 tables read-only.
- The isolation level used by the application: `read committed`.
- TiDB cluster configuration: 3 TiDB nodes and 3 TiKV nodes with 16 CPUs allocated to each node.
- Client server configuration: 36 CPU.

## Scenario 1: Using the Query Interface

### Application configuration

The application uses the following JDBC configuration to connect to the database through the Query interface.

```
useServerPrepStmts=false
```

### Performance Analysis

#### TiDB Dashboard

As you can observe from the Top SQL page in the Dashboard below, the non-business SQL type `SELECT @@session.tx_isolation` consumes the most resources. Although TiDB processes these types of SQL statements quickly, the highest number of executions results in the highest overall CPU time consumption.

! [dashboard-for-query-interface](/media/performance/case1.png)

Looking at the following flame chart of TiDB, you can see that the CPU consumption of functions such as Compile and Optimize is significant during the execution of SQL. Because the application uses the Query interface, TiDB cannot use the execution plan cache, resulting in the need to compile and generate the execution plan for each SQL.

! [flame-graph-for-query-interface](/media/performance/7.1.png)

- ExecuteStmt cpu = 38% cpu time = 23.84s
- Compile cpu = 27% cpu time = 17.17s
- Optimize cpu = 26% cpu time = 16.41s

#### Performance Overview panel

Observe the data for the database time overview and QPS in the following Performance Overview panel.

! [performance-overview-1-for-query-interface](/media/performance/j-1.png)

- The Select statement in Database Time by SQL Type takes the most time
- Database Time by SQL Phase execute and compile account for most of the time.
- The SQL Execute Time Overview has the highest percentage of Get, Cop and tso wait.
- CPS By Type Only query is the command
- Queries Using Plan Cache OPS No data, indicating that the execution plan cache could not be hit
- Execute and compile delays account for the highest percentage of query duration
- avg QPS = 56.8k

Looking at the resource consumption of the cluster, the average utilization of TiDB CPU is 925%, the average utilization of TiKV CPU is 201%, and the average throughput of TiKV IO is 18.7 MB/s. The resource consumption of TiDB is significantly higher.

! [performance-overview-2-for-query-interface](/media/performance/5.png)

### Analysis conclusion

There is a need to block a lot of these useless non-business SQL statements.

## Scenario 2: Using maxPerformance Configuration

### Application configuration

Add a new parameter `useConfigs=maxPerformance` to the JDBC connection string in Scenario 1. This parameter can be used to block some query setting type SQL statements sent by JDBC to the database (e.g. `select @@session.transaction_read_only`), the full configuration is as follows.

```
useServerPrepStmts=false&useConfigs=maxPerformance
```

### Performance Analysis

#### TiDB Dashboard

On the Top SQL page of Dashboard, you can see that `SELECT @@session.tx_isolation`, which used to be the most dominant, has disappeared.

! [dashboard-for-maxPerformance](/media/performance/case2.png)

Looking at the following flame chart of TiDB, you can see that the CPU consumption of functions such as Compile and Optimize is high in the execution of SQL statements.

! [flame-graph-for-maxPerformance](/media/performance/20220507-145257.jpg)

- ExecuteStmt cpu = 43% cpu time =35.84s
- Compile cpu = 31% cpu time =25.61s
- Optimize cpu = 30% cpu time = 24.74s

#### Performance Overview panel

The data for the database time overview and QPS are as follows.

! [performance-overview-1-for-maxPerformance](/media/performance/j-2.png)

- Database Time by SQL Type select statement takes the most time
- Database Time by SQL Phase execute and compile account for most of the time.
- The most popular SQL Execute Time Overviews are Get, Cop, Prewrite, and tso_wait.
- Execute and compile delays are the highest percentage of db time
- CPS By Type Only query is the command
- avg QPS = 24.2k (56.3k->24.2k))
- Unable to hit plan cache

From Scenario 1 to Scenario 2, the average TiDB CPU utilization drops from 925% to 874%, and the average TiKV CPU utilization rises from 201% to about 250%.

! [performance-overview-2-for-maxPerformance](/media/performance/9.1.1.png)

The key delay indicators changed as follows.

! [performance-overview-3-for-maxPerformance](/media/performance/9.2.2.png)

- avg query duration = 1.12ms (479?s->1.12ms)
- avg parse duration = 84.7?s (37.2?s->84.7?s)
- avg compile duration = 370?s (166?s->370?s)
- avg execution duration = 626?s (251?s->626?s)

### Analysis conclusion

Compared with Scenario 1, the QPS of Scenario 2 has significantly decreased, and the average query duration and parse, compile and execute duration have significantly increased. This is because SQL statements like `select @@session.transaction_read_only` in Scenario 1, which are executed many times and have fast processing time, lower the performance average, and only pure business SQL remains after blocking such statements in Scenario 2, which leads to the increase of the average duration.

When the application uses query interface, TiDB cannot use execution plan cache and compile execution plan consumes high. In this case, it is recommended to use Prepared Statement pre-compiled interface to reduce TiDB CPU consumption and latency caused by compile by using TiDB execution plan cache.

## Scenario 3: Using Prepared Statement interface without execution plan caching enabled

### Application configuration

The application uses the following connection configuration, and in contrast to scenario 2, the value of the `useServerPrepStmts` parameter of JDBC is modified to `true`, indicating that the interface for pre-compiled statements is enabled.

```
useServerPrepStmts=true&useConfigs=maxPerformance"
```

### Performance Analysis

#### TiDB Dashboard

Looking at the following flame chart for TiDB, you can see that the CPU footprint of CompileExecutePreparedStmt and Optimize is still significant after enabling the Prepared Statement interface.

! [flame-graph-for-PrepStmts](/media/performance/3.1.1.png)

- ExecutePreparedStmt cpu = 31% cpu time = 23.10s
- preparedStmtExec cpu = 30% cpu time = 22.92s
- CompileExecutePreparedStmt cpu = 24% cpu time = 17.83s
- Optimize cpu = 23% cpu time = 17.29s

#### Performance Overview panel

After using the Prepared Statement interface, the database time overview and QPS data are as follows.

! [performance-overview-1-for-PrepStmts](/media/performance/j-3.png)

The Database Time Overview shows the general statement type (which includes the execution time of commands such as StmtPrepare and StmtClose), which is the second most popular. This indicates that even when Prepared is used, the time taken to execute the commands is still very small. This means that even with the Prepared Statement interface, the execution plan cache is not hit because TiDB internally processes the StmtClose command and clears the execution plan cache for the modified statement.

- Database Time by SQL Type select statement takes the most time, followed by general statement
- Database Time by SQL Phase execute and compile account for most of the time.
- The most popular SQL Execute Time Overviews are Get, Cop, Prewrite, and tso_wait.
- CPS By Type becomes 3 kinds of command: StmtPrepare, StmtExecute, StmtClose
- avg QPS = 19.7k (24.4k->19.7k)
- Unable to hit plan cache

TiDB average CPU utilization increased from 874% to 936%

! [performance-overview-1-for-PrepStmts](/media/performance/3-2.png)

The main latency data are as follows.

! [performance-overview-2-for-PrepStmts](/media/performance/3.4.png)

- avg query duration = 528?s (1.12ms->528?s)
- avg parse duration = 14.9?s (84.7?s->14.9?s)
- avg compile duration = 374?s (370?s->374?s)
- avg execution duration = 649?s (626?s->649?s)

### Analysis conclusion

Unlike Scenario 2, Scenario 3 enables the prepare pre-compile interface but still fails to hit the cache. In addition, scenario 2 has only one CPS By Type command type, query, while scenario 3 has three more command types (StmtPrepare, StmtExecute, StmtClose). Compared with Scenario 2, it is equivalent to two more network round trips.

- Analysis of the reason for the decrease in QPS: From the CPS By Type panel, we can see that scenario 2 has only one command type, query, but scenario 3 has three new command types, namely StmtPrepare, StmtExecute and StmtClose. StmtPrepare and StmtClose are non-conventional commands that are not counted by QPS, so QPS is reduced. StmtPrepare and StmtClose for non-conventional commands are counted in the general sql type, so you can see that there is more general time in the database overview, and it accounts for more than a quarter of the database time.
- The average query duration is significantly lower because of the new command types StmtPrepare and StmtClose in Scenario 3, and the query duration is calculated separately when TiDB processes them internally.

Although scenario 3 uses the Prepare precompiled interface, many application frameworks also call the close method after execute to prevent memory leaks because of the StmtClose that causes cache invalidation. Starting with v6.0.0, you can set the global variable `tidb_ignore_prepared_cache_close_stmt=on;`. After setting, TiDB will not clear the cached execution plan even if the application calls the StmtClose method, so that the next SQL execution can reuse the existing execution plan and avoid compiling the execution plan repeatedly.

## Scenario 4: Using the Prepared Statement interface to enable execution plan caching

### Application configuration

The application configuration remains unchanged. Set the following parameters to resolve the issue of not hitting the cache even if the application triggers StmtClose.

- Set TiDB global variable `set global tidb_ignore_prepared_cache_close_stmt=on;` (officially used since TiDB v6.0.0, off by default)
- Set the TiDB configuration item `prepared-plan-cache: {enabled: true}` to enable the plan cache feature

### Performance Analysis

#### TiDB Dashboard

Looking at TiDB's CPU flame chart, you can see that CompileExecutePreparedStmt and Optimize have no significant CPU consumption. 25% of the CPU is consumed by the Prepare command, which contains Prepare parsing-related functions such as PlanBuilder and parseSQL.

PreparseStmt cpu = 25% cpu time = 12.75s

! [flame-graph-for-3-commands](/media/performance/4.2.png)

#### Performance Overview panel

In the Performance Overview panel, the most significant change comes in the percentage of Compile phases, which is reduced from 8.95 seconds per second in Scenario 3 to 1.18 seconds per second. The number of hits in the execution plan cache is roughly equal to the number of StmtExecute hits. With the increase in QPS, the database time consumed per second for Select statements has decreased, and general type statements have become longer.

! [performance-overview-1-for-3-commands](/media/performance/j-4.png)

- Database Time by SQL Type select statement takes the most time
- Database Time by SQL Phase has the highest percentage of execute
- The SQL Execute Time Overview has the highest percentage of tso wait, Get and Cop respectively.
- Hit plan cache, Queries Using Plan Cache OPS roughly equal to StmtExecute per second
- CPS By Type is still 3 commands
- The general time is longer compared to scenario 3 because the QPS has increased
- avg QPS = 22.1k (19.7k->22.1k)

The average TiDB CPU utilization dropped from 936% to 827%.

! [performance-overview-2-for-3-commands](/media/performance/4.4.png)

The average Compile time dropped significantly, from 374 us to 53.3 us, as the average execute time increased due to the rise in QPS.

! [performance-overview-3-for-3-commands](/media/performance/4.5.png)

- avg query duration = 426?s (528?s->426?s)
- avg parse duration = 12.3?s (14.8?s->12.3?s)
- avg compile duration = 53.3?s (374?s->53.3?s)
- avg execution duration = 699?s (649?s->699us)

### Analysis conclusion

Compared with Scenario 3, Scenario 4 also has 3 command types, but the difference is that Scenario 4 can hit the execution plan cache, so it greatly reduces the compile duration, and reduces the query duration, and improves QPS.

Because the StmtPrepare and StmtClose commands consume significant database time and increase the number of interactions the application needs to have with TiDB for each SQL statement executed. The next scenario will optimize away these two commands through JDBC configuration.

## Scenario 5: Client-side caching of prepared objects

### Application configuration

Compared with Scenario 4, 3 new JDBC parameters are configured `cachePrepStmts=true&prepStmtCacheSize=1000&prepStmtCacheSqlLimit=20480`, as explained below.

- `cachePrepStmts = true`: caches prepared statement objects on the client side, eliminating StmtPrepare and StmtClose calls.
- `prepStmtCacheSize`: needs to be configured to a value greater than 0
- `prepStmtCacheSqlLimit`: needs to be set to a length greater than the SQL text

The complete JDBC parameter configuration is as follows.

```
useServerPrepStmts=true&cachePrepStmts=true&prepStmtCacheSize=1000&prepStmtCacheSqlLimit=20480&useConfigs= maxPerformance
```

### Performance Analysis

#### TiDB Dashboard

Looking at the following flame chart for TiDB, you can see that the high CPU consumption of the Prepare command is no longer present.

- ExecutePreparedStmt cpu = 22% cpu time = 8.4s

! [flame-graph-for-1-command](/media/performance/5.1.1.png)

#### Performance Overview panel

In the Performance Overview panel, the most notable changes are that the three Stmt command types in the CPS By Type panel have become one, the general statement type in the Database Time by SQL Type panel has disappeared, and the QPS in the QSP panel has gone up to 30.9k.

! [performance-overview-for-1-command](/media/performance/j-5.png)

- Database Time by SQL Type select statement takes the most time, general statement type disappears
- Database Time by SQL Phase is mainly for execute
- The SQL Execute Time Overview has the highest percentage of tso wait, Get and Cop respectively.
- Hit plan cache, Queries Using Plan Cache OPS roughly equal to StmtExecute per second
- CPS By Type has only one command, namely StmtExecute
- avg QPS = 30.9k (22.1k->30.9k)

The average TiDB CPU utilization dropped from 827% to 577%, and as the QPS increased, the average TiKV CPU utilization increased to 313%.

! [performance-overview-for-2-command](/media/performance/j-5-cpu.png)

The key latency indicators are as follows.

! [performance-overview-for-3-command](/media/performance/j-5-duration.png)

- avg query duration = 690?s (426->690?s)
- avg parse duration = 13.5?s (12.3?s->13.5?s )
- avg compile duration = 49.7?s (53.3?s->49.7?s)
- avg execution duration = 623?s (699us->623?s)
- avg pd tso wait duration = 196?s (224?s->196?s)
- connection idle duration avg-in-txn = 608?s (250?s->608?s)

### Analysis conclusion

- Compared with Scenario 4, Scenario 5 has only one CPS By Type command, StmtExecute, which reduces two network round trips and increases the overall system QPS.
- In the case of rising QPS, the latency decreases in terms of parse duration, compile duration, and execution duration, but the query duration increases instead. This is because StmtPrepare and StmtClose are processed very fast, and eliminating these two command types increases the average query duration.
- Database Time by SQL Phase in execute is very high close to database time, while SQL Execute Time Overview in the most proportion is tso wait, more than a quarter of execute time is waiting for tso.
- The total tso wait time per second is 5.46 s. The average tso wait time is 196 us, and the number of tso cmd times per second is 28k, which is very close to the QPS of 30.9k. Because of TiDB's implementation of the `read committed` isolation level, every SQL statement in a transaction needs to request tso from the PD.

TiDB v6.0 provides `rc read`, which is optimized for the `read committed` isolation level with reduced tso cmd. This feature is controlled by the global variable `set global tidb_rc_read_check_ts=on;`. When this variable is enabled, the default behavior of TiDB is the same as the `repeatable-read` isolation level, only the start-ts and commit-ts are obtained from the PD. statements in the transaction use the start-ts to read data from TiKV first. If the data read is less than start-ts, the data is returned directly; if the data read is greater than start-ts, the data is discarded and tso is requested from the PD to retry. The for update ts of subsequent statements use the latest PD tso.

## Scenario 6: Turn on the tidb_rc_read_check_ts variable to reduce TSO requests

### Application configuration

The application configuration remains the same, unlike scenario 5, set `set global tidb_rc_read_check_ts=on;` to reduce TSO requests.

### Performance Analysis

#### Dashboard

TiDB's CPU flame chart has not changed significantly.

- ExecutePreparedStmt cpu = 22% cpu time = 8.4s

! [flame-graph-for-rc-read](/media/performance/6.2.2.png)

#### Performance Overview panel

After using RC read, QPS increases from 30.9k to 34.9k, and the tso wait time per second consumed decreases from 5.46 s to 456 ms.

! [performance-overview-1-for-rc-read](/media/performance/j-6.png)

- Database Time by SQL Type select statement takes the most time
- Database Time by SQL Phase has the highest percentage of execute
- Get, Cop, and Prewrite are the most popular in SQL Execute Time Overview.
- Hit plan cache, Queries Using Plan Cache OPS roughly equal to StmtExecute per second
- CPS By Type There is only one command
- avg QPS = 34.9k (30.9k->34.9k)

The tso cmd per second drops from 28.3k to 2.7k.

! [performance-overview-2-for-rc-read](/media/performance/j-6-cmd.png)

The average TiDB CPU uplift was 603% (577%->603%).

! [performance-overview-3-for-rc-read](/media/performance/j-6-cpu.png)

The key latency indicators are as follows.

! [performance-overview-4-for-rc-read](/media/performance/j-6-duration.png)

- avg query duration = 533?s (690?s->533?s)
- avg parse duration = 13.4?s (13.5?s->13.4?s )
- avg compile duration = 50.3?s (49.7?s->50.3?s)
- avg execution duration = 466?s (623?s->466?s)
- avg pd tso wait duration = 171?s (196?s->171?s)

### Analysis conclusion

After enabling RC Read by `set global tidb_rc_read_check_ts=on;`, RC Read significantly reduces the number of tso cmd times, thus reducing tso wait and average query duration, and improving QPS.

The current database time and latency bottlenecks are in the execute phase, and the highest percentage of the execute phase are Get and Cop read requests. Most of the tables in this load are read-only or rarely modified, so you can use the small table caching feature in v6.0.0 to cache the data of these small tables using TiDB to reduce the waiting time and resource consumption of KV read requests.

## Scenario 7: Using Small Table Cache

### Application configuration

The application configuration remains unchanged, and the read-only table for the business is set up to cache `alter table t1 cache;` on top of scenario 6.

### Performance Analysis

#### Dashboard

The TiDB CPU flame chart has not changed significantly.

! [flame-graph-for-table-cache](/media/performance/7.2.png)

#### Performance Overview panel

QPS increased from 34.9k to 40.9k, and the KV request types with the highest percentage of execute time became Prewrite and Commit. get per second decreased from 5.33 seconds to 1.75 seconds, and Cop per second decreased from 3.87 seconds to 1.09 seconds.

! [performance-overview-1-for-table-cache](/media/performance/j-7.png)

- Database Time by SQL Type select statement takes the most time
- Database Time by SQL Phase execute and compile account for most of the time.
- The most popular SQL Execute Time Overviews are Prewrite, Commit, and Get.
- Hit plan cache, Queries Using Plan Cache OPS roughly equal to StmtExecute per second
- CPS By Type has only 1 type of command
- avg QPS = 40.9k (34.9k->40.9k)

The average TiDB CPU utilization dropped from 603% to 478% and the average TiKV CPU utilization dropped from 346% to 256%.

! [performance-overview-2-for-table-cache](/media/performance/j-7-cpu.png)

Average Query latency dropped from 533 us to 313 us. average execute latency dropped from 466 us to 250 us.

! [performance-overview-3-for-table-cache](/media/performance/j-7-duration.png)

- avg query duration = 313?s (533?s->313?s)
- avg parse duration = 11.9?s (13.4?s->11.9?s)
- avg compile duration = 47.7?s (50.3?s->47.7?s)
- avg execution duration = 251?s (466?s->251?s)

### Analysis conclusion

After caching all read-only tables, you can see that the execute duration drops significantly because all read-only tables are cached in TiDB and you no longer need to query data in TiKV, so the query duration drops and the QPS goes up.

This is a more optimistic result, the actual business may have a larger amount of read-only table data can not be all cached in TiDB. Another limitation is that although the current small table caching feature supports write operations, the write operation requires a default wait of 3 seconds to ensure that the cache of all TiDB nodes is invalidated, which may not be friendly to applications with high latency requirements for the time being.

## Summary

The following table shows the performance of seven different scenarios.

| Metrics | Scene 1 | Scene 2 | Scene 3 | Scene 4 | Scene 5 | Scene 6 | Scene 7 | Compare Scene 5 and Scene 2 (%) | Compare Scene 7 and Scene 3 (%) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---
| query duration | 479?s | 1120?s | 528?s | 426?s | 690?s | 533?s | 313?s | -38% | -51% |
| QPS | 56.3k | 24.2k | 19.7k | 22.1k | 30.9k | 34.9k | 40.9k | +28% | +108% |

Scenario 2 is a common scenario where applications use the query interface, and Scenario 5 is an ideal scenario where applications use the Prepared Statement interface.

- Comparing Scenario 2 and Scenario 5, you can see that by using best practices for Java application development and client-side caching of Prepared Statement objects, each SQL requires only one command and database interaction to hit the execution plan cache, resulting in a 38% drop in Query latency and a 28% increase in QPS, while the average TiDB CPU utilization dropped from 936% to 577%.
- Comparing Scenario 2 and Scenario 7, you can see that with the latest TiDB optimizations such as RC Read and small table cache on top of Scenario 5, latency is reduced by 51% and QPS is increased by 108%, while the average TiDB CPU utilization drops from 936% to 478%.

By comparing the performance of each scenario, the following conclusions can be drawn.

- TiDB's execution plan caching plays a critical role for OLTP. The RC Read and small table caching features introduced from v6.0.0 also play an important role in the deep optimization of this load.
- TiDB is compatible with different commands of the MySQL protocol and the best performance comes from the application using the Prepared Statement interface and setting the following JDBC connection parameters.

    ```
    useServerPrepStmts=true&cachePrepStmts=true&prepStmtCacheSize=1000&prepStmtCacheSqlLimit=20480&useConfigs= maxPerformance
    ```

- During performance analysis and optimization, it is recommended to use TiDB Dashboard (e.g. Top SQL feature and Continuous Performance Analysis feature) and Performance Overview panel.

    - The     [Top SQL](/dashboard/top-sql.md) feature allows you to visually monitor and explore the CPU overhead of each SQL statement in your database during execution, so that you can optimize and address database performance issues.
    - Continuous performance analysis function](/dashboard/continuous-profiling.md) can continuously collect performance data from each instance of TiDB, TiKV, PD. There is a huge difference in the CPU consumption of TiDB when applications use different interfaces to interact with TiDB.
    - The [Performance Overview dashboard](/grafana-performance-overview-dashboard.md) provides an overview of database time and SQL execution time breakdown information. With this dashboard, you can perform database time-based performance analysis and diagnostics to determine if the performance bottleneck for the entire system is in TiDB. If the bottleneck is in TiDB, you can use the database time and latency breakdowns, along with cluster key metrics and resource usage, to identify performance bottlenecks within TiDB and perform targeted optimizations.

Using a combination of these features, you can perform efficient performance analysis and optimization for real-world applications.
