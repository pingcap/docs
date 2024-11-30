---
title: TiFlash MinTSO Scheduler
summary: Learn the implementation principles of the TiFlash MinTSO Scheduler.
---

# TiFlash MinTSO Scheduler

The TiFlash MinTSO scheduler is a distributed scheduler for [MPP](/glossary.md#massively-parallel-processing-mpp) tasks in TiFlash. This document describes the implementation principles of the TiFlash MinTSO scheduler.

## Background

When processing an MPP query, TiDB splits the query into one or more MPP tasks and sends these MPP tasks to the corresponding TiFlash nodes for compilation and execution. Before TiFlash uses the [pipeline execution model](/tiflash/tiflash-pipeline-model.md), TiFlash needs to use several threads to execute each MPP task, with the specific number of threads depending on the complexity of the MPP task and the concurrency parameters set in TiFlash.

In high concurrency scenarios, TiFlash nodes receive multiple MPP tasks simultaneously. If the execution of MPP tasks is not controlled, the number of threads that TiFlash needs to request from the system will increase linearly along with the increasing number of MPP tasks. Too many threads can affect the execution efficiency of TiFlash, and because the operating system itself supports a limited number of threads, TiFlash will encounter errors when it requests more threads than the operating system can provide.

To improve TiFlash's processing capability in high concurrency scenarios, an MPP task scheduler needs to be introduced into TiFlash.

## Implementation principles

As mentioned in the [background](#background), the initial purpose of introducing the TiFlash task scheduler is to control the number of threads used during MPP query execution. A simple scheduling strategy is to specify the maximum number of threads TiFlash can request. For each MPP task, the scheduler decides whether the MPP task can be scheduled based on the current number of threads used by the system and the expected number of threads the MPP task will use:

![TiFlash MinTSO Scheduler v1](/media/tiflash/tiflash_mintso_v1.png)

Although the preceding scheduling strategy can effectively control the number of system threads, an MPP task is not the smallest independent execution unit, and dependencies exist between different MPP tasks:

```sql
EXPLAIN SELECT count(*) FROM t0 a JOIN t0 b ON a.id = b.id;
```

```
+--------------------------------------------+----------+--------------+---------------+----------------------------------------------------------+
| id                                         | estRows  | task         | access object | operator info                                            |
+--------------------------------------------+----------+--------------+---------------+----------------------------------------------------------+
| HashAgg_44                                 | 1.00     | root         |               | funcs:count(Column#8)->Column#7                          |
| └─TableReader_46                           | 1.00     | root         |               | MppVersion: 2, data:ExchangeSender_45                    |
|   └─ExchangeSender_45                      | 1.00     | mpp[tiflash] |               | ExchangeType: PassThrough                                |
|     └─HashAgg_13                           | 1.00     | mpp[tiflash] |               | funcs:count(1)->Column#8                                 |
|       └─Projection_43                      | 12487.50 | mpp[tiflash] |               | test.t0.id                                               |
|         └─HashJoin_42                      | 12487.50 | mpp[tiflash] |               | inner join, equal:[eq(test.t0.id, test.t0.id)]           |
|           ├─ExchangeReceiver_22(Build)     | 9990.00  | mpp[tiflash] |               |                                                          |
|           │ └─ExchangeSender_21            | 9990.00  | mpp[tiflash] |               | ExchangeType: Broadcast, Compression: FAST               |
|           │   └─Selection_20               | 9990.00  | mpp[tiflash] |               | not(isnull(test.t0.id))                                  |
|           │     └─TableFullScan_19         | 10000.00 | mpp[tiflash] | table:a       | pushed down filter:empty, keep order:false, stats:pseudo |
|           └─Selection_24(Probe)            | 9990.00  | mpp[tiflash] |               | not(isnull(test.t0.id))                                  |
|             └─TableFullScan_23             | 10000.00 | mpp[tiflash] | table:b       | pushed down filter:empty, keep order:false, stats:pseudo |
+--------------------------------------------+----------+--------------+---------------+----------------------------------------------------------+
```

For example, the preceding query generates two MPP tasks on each TiFlash node, where the MPP task containing the `ExchangeSender_45` executor depends on the MPP task containing the `ExchangeSender_21` executor. In high concurrency scenarios, if the scheduler schedules the MPP task containing `ExchangeSender_45` for each query, the system will enter a deadlock state.

To avoid deadlock, TiFlash introduces the following two levels of thread limits:

* thread_soft_limit: used to limit the number of threads used by the system. For specific MPP tasks, this limit can be broken to avoid deadlock.
* thread_hard_limit: used to protect the system. Once the number of threads used by the system exceeds the hard limit, TiFlash will report an error to avoid deadlock.

The soft limit and hard limit work together to avoid deadlock as follows: the soft limit restricts the total number of threads used by all queries, enabling full use of resources while avoiding thread resource exhaustion; the hard limit ensures that in any situation, at least one query in the system can break the soft limit and continue to acquire thread resources and run, thus avoiding deadlock. As long as the number of threads does not exceed the hard limit, there will always be one query in the system where all its MPP tasks can be executed normally, thus preventing deadlock.

The goal of the MinTSO scheduler is to control the number of system threads while ensuring that there is always one and only one special query in the system, where all its MPP tasks can be scheduled. The MinTSO scheduler is a fully distributed scheduler, with each TiFlash node scheduling MPP tasks based only on its own information. Therefore, all MinTSO schedulers on TiFlash nodes need to identify the same "special" query. In TiDB, each query carries a read timestamp (`start_ts`), and the MinTSO scheduler defines the "special" query as the query with the smallest `start_ts` on the current TiFlash node. Based on the principle that the global minimum is also the local minimum, the "special" query selected by all TiFlash nodes must be the same, called the MinTSO query.

The scheduling process of the MinTSO Scheduler is as follows:

![TiFlash MinTSO Scheduler v2](/media/tiflash/tiflash_mintso_v2.png)

By introducing soft limit and hard limit, the MinTSO scheduler effectively avoids system deadlock while controlling the number of system threads. In high concurrency scenarios, however, most queries might only have part of their MPP tasks scheduled. Queries with only part of MPP tasks scheduled cannot execute normally, leading to low system execution efficiency. To avoid this situation, TiFlash introduces a query-level limit for the MinTSO scheduler, called active_set_soft_limit. This limit allows only MPP tasks of up to active_set_soft_limit queries to participate in scheduling; MPP tasks of other queries do not participate in scheduling, and only after the current queries finish can new queries participate in scheduling. This limit is only a soft limit because for the MinTSO query, all its MPP tasks can be scheduled directly as long as the number of system threads does not exceed the hard limit.

## See also

- [Configure TiFlash](/tiflash/tiflash-configuration.md): learn how to configure the MinTSO scheduler.
