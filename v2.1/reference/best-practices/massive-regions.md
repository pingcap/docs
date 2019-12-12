---
title: TiKV Performance Tuning with Massive Region Amount Best Practices
summary: Learn how a massive amount of Regions cause TiKV performance problem and how to tune TiKV performance in this situation.
category: reference
---

# TiKV Performance Tuning with Massive Region Amount Best Practices

In the TiDB architecture, data is segmented into key ranges that are called Regions distributed among multiple TiKV instances. As data is written into a cluster, millions or even tens of millions of Regions are created. Too many Regions on a single TiKV instance brings heavy burden to the cluster, encumbering the performance of the whole cluster.

This document introduces the workflow of Raftstore (a core module of TiKV), explains why a massive amount of Regions cause performance problem, and offers the methods for tuning TiKV performance.

## Raftstore workflow

A TiKV instance has multiple Regions on it. The Raftstore module drives the Raft state machine to process the messages for Regions. These messages include processing the read and write requests on Regions, persisting and replicating Raft logs, processing heartbeat, and so on. However, an increasing number of Regions might influence the performance of the whole cluster. To explain this, it is necessary to first learn the workflow of Raftstore, a core module of TiKV.

![Raftstore Workflow](/media/best-practices/raft-process.png)

> **Note:**
>
> This diagram only illustrates the working principle of Raftstore and does not represent the actual code structure.

From this diagram, requests from TiDB, through the gRPC and storage modules, become the final read and write messages of key-value pairs, and are sent to the corresponding Regions. These messages are not immediately processed but are temporarily stored instead. Raftstore polls to check if each Region has messages to process. If a Region has messages to process, Raftstore drives the Raft state machine of the Region to process these messages and perform subsequent operations according to the state changes generated from these messages. For example, with a write request, the Raft state machine stores logs into the disk and sends the logs to other Region replicas; sends the heartbeat information to other Region replicas when the heartbeat interval is reached.

## Performance problem

From the diagram of Raftstore workflow, the messages for each Region are processed in turn. When Regions are in huge numbers, it takes Raftstore sometime to process the heartbeats of these Regions, which can cause some delays. As a result, some read and write requests are not processed in time. If the read and write pressure is high, the CPU usage of the Raftstore thread might easily reach the bottleneck, which further increases the delay and affects the performance.

Generally, if the CPU usage of the loaded Raftstore reaches 85% or higher, Raftstore is in the busy state and becomes the bottleneck. At the same time, `propose wait duration` can be as high as hundreds of milliseconds.

> **Note:**
>
> + For the CPU usage of Raftstore as mentioned above, Raftstore is single-threaded. If Raftstore is multi-threaded, the CPU usage threshold (85%) can be increased proportionally.
> + Because I/O operations exist in the Raftstore thread, the CPU usage cannot reach 100%.

### Performance monitoring

You can check the following monitoring metrics in Grafana's TiKV panel:

+ `Raft store CPU` in the Thread-CPU panel

    Reference value: lower than `raftstore.store-pool-size * 85%`. TiDB v2.1 does not have `raftstore.store-pool-size`, so you can regard `raftstore.store-pool-size = 1` in v2.1.

    ![Check Raftstore CPU](/media/best-practices/raft-store-cpu.png)

+ `Propose wait duration` in the Raft Propose panel

    `Propose wait duration` is the delay time between sending a request to Raftstore and Raftstore actually starting processing the request. Long delay time means that Raftstore is busy, or that processing the append log is time-consuming so that Raftstore cannot process the request in time.

    Reference value: lower than 50-100 ms according to the cluster size

    ![Check Propose wait duration](/media/best-practices/propose-wait-duration.png)

## Performance tuning method

After finding out the root cause of the performance problem, the solutions are in two types:

+ Reduce the number of Regions on a single TiKV instance
+ Reduce the number of messages for a single Region

In TiDB v2.1, the Raftstore is single-threaded. Therefore, when the number of Regions exceeds a hundred thousand, the CPU usage of the Raftstore thread gradually becomes the bottleneck.

### Method 1: Increase TiKV instance

If I/O resources and CPU resources are sufficient, you can deploy multiple TiKV instances on a single machine to reduce the number of Regions on a single TiKV instance; or you can increase the number of machines in the TiKV cluster.

### Method 2: Enable `Region Merge`

> **Note:**
>
> `Region Merge` is enabled in TiDB v3.0 by default.

You can also reduce the number of Regions by enabling `Region Merge`. Contrary to `Region Split`, `Region Merge` is the process of merging adjacent small Regions by scheduling. After deleting data or executing the `Drop Table` or `Truncate Table` statement, you can merge small Regions or even empty Regions to reduce resource consumption.

Enable `Region Merge` by setting the following configurations:

{{< copyable "" >}}

```
>> pd-ctl config set max-merge-region-size 20
>> pd-ctl config set max-merge-region-keys 200000
>> pd-ctl config set merge-schedule-limit 8
```

Refer to [Region Merge](https://github.com/tikv/tikv/blob/master/docs/how-to/configure/region-merge.md) for more details.

The default configuration of the `Region Merge` parameter is rather reserved. You can speed up the `Region Merge` process by referring to the method provided in [PD Scheduling Best Practices](/v2.1/reference/best-practices/pd-scheduling.md#region-merge-is-slow).

### Method 3: Adjust `raft-base-tick-interval`

In addition to reducing the number of Regions, you can also reduce pressure on Raftstore by reducing the number of messages for each Region in a unit of time. For example, you can properly increase the value of the `raft-base-tick-interval` configuration:

{{< copyable "" >}}

```
[raftstore]
raft-base-tick-interval = "2s"
```

`raft-base-tick-interval` is the time interval at which Raftstore drives the Raft state machine of each Region, which means at this time interval, Raftstore sends a tick message to the Raft state machine. Increasing this interval can effectively reduce the number of messages from Raftstore.

Note that this interval between tick messages also determines the intervals of `election timeout` and `heartbeat`. See the following example:

{{< copyable "" >}}

```
raft-election-timeout = raft-base-tick-interval * raft-election-timeout-ticks
raft-heartbeat-interval = raft-base-tick-interval * raft-heartbeat-ticks
```

If Region Followers does not receive the heartbeat from the Leader within the `raft-election-timeout` interval, they determine that the Leader has failed and start a new election. `raft-heartbeat-interval` is the interval at which a Leader sends heartbeat to Followers. Therefore, increasing the value of `raft-base-tick-interval` can reduce the number of network messages sent from Raft state machines but also makes it longer for Raft state machines to detect the Leader failure.

## Other problems and solutions

### Switching PD Leader is slow

PD needs to persist the Region Meta information on etcd to ensure that PD can quickly resume to provide Region routing services after switching the PD Leader node. As the number of Regions increases, the performance problem of etcd appears, making it slower for PD to get the Region Meta information from etcd when PD is switching the Leader. With millions of Regions, it might take dozens or even tens of seconds to get the meta information from etcd.

To address this problem, `use-region-storage` is enabled by default in PD since TiDB v3.0. With this feature enabled, PD stores the Region Meta information on the local LevelDB and synchronizes the information among PD nodes through other mechanism. If you encounter similar problems in v2.1, upgrade to v3.0.

### PD routing information is not updated in time

In TiKV, pd-worker periodically reports the Region Meta information to PD. When TiKV is restarted or switches the Region Leader, PD needs to recalculate Region's `approximate size / keys` through statistics. Therefore, with a large number of Regions, the single-threaded pd-worker might become the bottleneck, causing tasks to be piled up without being processed in time. In this situation, PD cannot obtain certain Region Meta information in time so that the routing information is not updated in time. This problem does not affect the actual reads and writes, but might cause inaccurate PD scheduling and require several round trips when TiDB updates the Region cache.

You can check `Worker pending tasks` under Task in the TiKV Grafana panel to determine whether pd-worker has tasks piled up. Generally, `pending tasks` should be kept at a relatively low value.

![Check pd-worker](/media/best-practices/pd-worker-metrics.png)

Currently, pd-worker is optimized for efficiency in [#5620](https://github.com/tikv/tikv/pull/5620) on [TiKV master](https://github.com/tikv/tikv/tree/master), which is applied in versions later than [3.0.5](https://pingcap.com/docs/stable/releases/3.0.5/#tikv) (included). If you encounter the similar problem, it is recommended to upgrade to v3.0.5.

### Prometheus is slow to query metrics

In a large-scale cluster, as the number of TiKV instances increases, Prometheus has greater pressure when querying metrics, making it slower for you to view metrics in Grafana. This problem is eased by configuring pre-calculations in v3.0.
