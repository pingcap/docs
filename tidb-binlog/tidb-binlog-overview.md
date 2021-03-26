---
title: TiDB Binlog Overview
summary: Learn overview of the cluster version of TiDB Binlog.
aliases: ['/docs/dev/tidb-binlog/tidb-binlog-overview/','/docs/dev/reference/tidb-binlog/overview/','/docs/dev/reference/tidb-binlog-overview/','/docs/dev/reference/tools/tidb-binlog/overview/']
---

# TiDB Binlog Cluster Overview

This document introduces the architecture and the deployment of the cluster version of TiDB Binlog.

TiDB Binlog is a tool used to collect binlog data from TiDB and provide near real-time backup and replication to downstream platforms.

TiDB Binlog has the following features:

* **Data replication:** replicate the data in the TiDB cluster to other databases
* **Real-time backup and restoration:** back up the data in the TiDB cluster and restore the TiDB cluster when the cluster fails

> **Note:**
>
> TiDB Binlog is not compatible with some features introduced in TiDB v5.0.0-rc and cannot be used together. For details, see [Notes](#notes). It is recommended to use [TiCDC](/ticdc/ticdc-overview.md) instead.

## TiDB Binlog architecture

The TiDB Binlog architecture is as follows:

![TiDB Binlog architecture](/media/tidb-binlog-cluster-architecture.png)

The TiDB Binlog cluster is composed of Pump and Drainer.

### Pump

[Pump](https://github.com/pingcap/tidb-binlog/blob/master/pump) is used to record the binlogs generated in TiDB, sort the binlogs based on the commit time of the transaction, and send binlogs to Drainer for consumption.

### Drainer

[Drainer](https://github.com/pingcap/tidb-binlog/tree/master/drainer) collects and merges binlogs from each Pump, converts the binlog to SQL or data of a specific format, and replicates the data to a specific downstream platform.

### `binlogctl` guide

[`binlogctl`](https://github.com/pingcap/tidb-binlog/tree/master/binlogctl) is an operations tool for TiDB Binlog with the following features:

* Obtaining the current `tso` of TiDB cluster
* Checking the Pump/Drainer state
* Modifying the Pump/Drainer state
* Pausing or closing Pump/Drainer

## Main features

* Multiple Pumps form a cluster which can scale out horizontally
* TiDB uses the built-in Pump Client to send the binlog to each Pump
* Pump stores binlogs and sends the binlogs to Drainer in order
* Drainer reads binlogs of each Pump, merges and sorts the binlogs, and sends the binlogs downstream
* Drainer supports [relay log](/tidb-binlog/tidb-binlog-relay-log.md). By the relay log, Drainer ensures that the downstream clusters are in a consistent state.

## Notes

* TiDB Binlog is not compatible with the following features introduced in TiDB v5.0.0-rc and cannot be used together:

    - [TiDB Clustered Index](/clustered-indexes.md#limitations): After TiDB Binlog is enabled, TiDB does not allow creating clustered indexes with non-single integer columns as primary keys; data insertion, deletion, and update for created clustered index tables will not be replicated downstream via TiDB Binlog. To replicate clustered index tables, you can use [TiCDC](/ticdc/ticdc-overview.md).
    - TiDB system variable [tidb_enable_async_commit](/system-variables.md#tidb_enable_async_commit-new-in-v500-rc): After TiDB Binlog is enabled, performance cannot be improved by enabling this option. To improve performance, it is recommended to use [TiCDC](/ticdc/ticdc-overview.md) instead.
    - TiDB system variable [tidb_enable_1pc](/system-variables.md#tidb_enable_1pc-new-in-v500-rc): After TiDB Binlog is enabled, performance cannot be improved by enabling this option. To improve performance, it is recommended to use [TiCDC](/ticdc/ticdc-overview.md) instead.

* TiDB Binlog is incompatible with the following feature introduced in TiDB v4.0.7 and cannot be used together:

    - TiDB system variable [tidb_enable_amend_pessimistic_txn](/system-variables.md#tidb_enable_amend_pessimistic_txn-new-in-v407): The two features have compatibility issues. Using them together will cause correctness issues with inconsistent replication data of TiDB Binlog.
