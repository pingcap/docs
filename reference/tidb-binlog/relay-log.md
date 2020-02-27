---
title: TiDB Binlog Relay Log
category: reference
aliases: ['/docs-cn/dev/reference/tools/tidb-binlog/relay-log/']
---

# TiDB Binlog Relay Log

When replicating binlogs, Drainer splits transactions from the upstream and replicates the split transactions concurrently to the downstream.

In extreme cases where the upstream clusters are not available and Drainer exits abnormally, the downstream clusters (MySQL or TiDB) may be in the intermediate states with inconsistent data. In such cases, Drainer can use the relay log to ensure that the downstream clusters are in a consistent state.

## Consistent state during Drainer replication

The downstream clusters reaching a consistent state means the data of the downstream clusters are the same as the snapshot of the upstream which sets `tidb_snapshot = ts`.

The checkpoint consistency means Drainer checkpoint saves the consistent state of replication in `consistent`. When Drainer runs, `consistent` is `false`. After Drainer exits normally, `consistent` is set to `true`.

You can query the downstream checkpoint table as follows:

```
mysql> select  * from tidb_binlog.checkpoint;
+---------------------+----------------------------------------------------------------+
| clusterID           | checkPoint                                                     |
+---------------------+----------------------------------------------------------------+
| 6791641053252586769 | {"consistent":false,"commitTS":414529105591271429,"ts-map":{}} |
+---------------------+----------------------------------------------------------------+
```

## Implementation principles

After Drainer enables the relay log, it first writes the binlog events to the disks and then replicates the events to the downstream clusters.

If the upstream clusters are not available, Drainer can restore the downstream clusters to a consistent state by reading the relay log.

> **Note:**
>
> If the relay log data is lost at the same time, this method does not work, but its incidence is very low.
> Besides, you can use the Network File System to ensure data security of the relay log.

### Trigger scenarios where Drainer consumes binlogs from the relay log

Where Drainer is started, if it fails to connect to the Placement Drivers (PD) of the upstream clusters, and if it detects that `consistent = false` in checkpoint, Drainer will try to read the relay log, and restore the downstream clusters to a consistent state. After that, the Drainer process sets the checkpoint `status` to `0` and then exits.

### GC mechanism of relay log

While Drainer is running, if it confirms that the whole data of a relay log file has been successfully replicated to the downstream, the file is deleted immediately. Therefore, the relay log does not occupy too much space.

If the size of a relay log file reaches 10MB (by default), the file is split, and data is written in the new relay log file.

## Configuration

To enable the relay log, add the following configuration in Drainer:

{{< copyable "" >}}

```
[syncer.relay]
# It saves the catalog of the relay log. The relay log is not enabled if the value is empty.
# The configuration only comes to effect if the downstream is TiDB or MySQL.
log-dir = "/dir/to/save/log"
```
