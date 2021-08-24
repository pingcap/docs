---
title: Incremental data replication between TiDB clusters in real time
summary: Learns how to replicate incremental data from one TiDB cluster to another cluster in real time
---

# Incremental data replication between TiDB clusters in real time

This document describes how to configure a TiDB cluster and its downstream MySQL or downstream TiDB, and then replicate the incremental data from an upstream cluster to a downstream cluster in real time .

## Usage scenarios

If you need to configure a running TiDB cluster and its downstream cluster for the incremental data replication in real time, use the [Backup & Restore (BR)](/br/backup-and-restore-tool.md), [Dumpling](/dumpling-overview.md) or [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md).

## Implementation principles

Each transaction written to TiDB is specified with a unique commit timestamp (commit TS). The global consistency status of a TiDB cluster is provided by a TS.

You need to use BR or Dumpling to export the cluster data at a specific point in time when the cluster is in global consistency status. Then, you need to use TiDB Binlog to start incremental replication right after the global consistent time. That is, the replication process is divided into two processes: full replication and incremental replication.

1. Perform a full backup restoration and get a commit TS of the data backup.
2. Perform incremental replication. Make sure that the start time of incremental replication is the commit TS of the data backup.

> **Note:**
>
> The commit TS obtained after exporting the backup data is a closed interval. The initial-commit-ts obtained after starting the replication process using TiDB Binlog is an open interval.

## Replication process

Suppose that the existing cluster A works properly. First, you need to create a new cluster B as the downstream cluster of cluster A and then replicate the incremental data in cluster A to cluster B in real time as the following steps:

### Step 1: enable TiDB Binlog

Make sure cluster A has deployed and enabled TiDB Binlog(/tidb-binlog/deploy-tidb-binlog.md).

### Step 2: full export the cluster data

1. Export data in cluster A global consistently to the specified path by using any of the following tools:

    - Use [BR for full backup](/br/use-br-command-line-tool.md#back-up-all-the-cluster-data)

    - Use [Dumpling to import full data](/dumpling-overview.md)

2. Obtain a global consistant timestamp `COMMIT_TS`:

    - Use the BR `validate` command to obtain the backup timestamp as following:

        {{< copyable "shell-regular" >}}

        ```shell
        COMMIT_TS=`br validate decode --field="end-version" -s local:///home/tidb/backupdata | tail -n1`
        ```

    - Or check the Dumpling metadata and obtain Pos (`COMMIT_TS`).

        {{< copyable "shell-regular" >}}

        ```shell
        cat metadata
        ```

        ```shell
        Started dump at: 2020-11-10 10:40:19
        SHOW MASTER STATUS:
                Log: tidb-binlog
                Pos: 420747102018863124

        Finished dump at: 2020-11-10 10:40:20
        ```

3. Export the data in cluster A to cluster B.

### Step 3: replicate incremental data

1. Modify the `drainer.toml` configuration file of TiDB Binlog and add the following configurations to specify the location that `COMMIT_TS` starts the replication to cluster B.

{{< copyable "" >}}

```toml
initial-commit-ts = COMMIT_TS
[syncer.to]
host = {the IP address of cluster B}
port = 3306
```
