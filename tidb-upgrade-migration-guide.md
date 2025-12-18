---
title: Migrate and Upgrade a TiDB Cluster
summary: Learn how to migrate and upgrade a TiDB cluster using BR for full backup and restore, along with TiCDC for incremental data replication.
---

# Migrate and Upgrade a TiDB Cluster

This document describes how to migrate and upgrade a TiDB cluster (also known as a blue-green upgrade) using [BR](/br/backup-and-restore-overview.md) for full backup and restore, along with [TiCDC](/ticdc/ticdc-overview.md) for incremental data replication. This solution uses dual-cluster redundancy and incremental replication to enable smooth traffic switchover and fast rollback, providing a reliable and low-risk upgrade path for critical systems. It is recommended to regularly upgrade the database version to continuously benefit from performance improvements and new features, helping you maintain a secure and efficient database system. The key advantages of this solution include:

- **Controllable risk**: supports rollback to the original cluster within minutes, ensuring business continuity.
- **Data integrity**: uses a multi-stage verification mechanism to prevent data loss.
- **Minimal business impact**: requires only a brief maintenance window for the final switchover.

The core workflow for migration and upgrade is as follows:

1. **Pre-check risks**: verify cluster status and solution feasibility.
2. **Prepare the new cluster**: create a new cluster from a full backup of the old cluster and upgrade it to the target version.
3. **Replicate incremental data**: establish a forward data replication channel using TiCDC.
4. **Switch and verify**: perform multi-dimensional verification, switch business traffic to the new cluster, and set up a TiCDC reverse replication channel.
5. **Observe status**: maintain the reverse replication channel. After the observation period, clean up the environment.

**Rollback plan**: if the new cluster encounters issues during the migration and upgrade process, you can switch business traffic back to the original cluster at any time.

The following sections describe the standardized process and general steps for migrating and upgrading a TiDB cluster. The example commands are based on a TiDB Self-Managed environment.

## Step 1: Evaluate solution feasibility

Before migrating and upgrading, evaluate the compatibility of relevant components and check cluster health status.

- Check the TiDB cluster version: this solution applies to TiDB v6.5.0 or later versions.

- Verify TiCDC compatibility:

    - **Table schema requirements**: ensure that tables to be replicated contain valid indexes. For more information, see [TiCDC valid index](/ticdc/ticdc-overview.md#best-practices).
    - **Feature limitations**: TiCDC does not support Sequence or TiFlash DDL replication. For more information, see [TiCDC unsupported scenarios](/ticdc/ticdc-overview.md#unsupported-scenarios).
    - **Best practices**: avoid executing DDL operations on the upstream cluster of TiCDC during switchover.

- Verify BR compatibility:

    - Review the compatibility matrix of BR full backup. For more information, see [BR version compatibility matrix](/br/backup-and-restore-overview.md#version-compatibility).
    - Check the known limitations of BR backup and restore. For more information, see [BR usage restrictions](/br/backup-and-restore-overview.md#restrictions).

- Check the health status of the cluster, such as [Region](/glossary.md#regionpeerraft-group) health and node resource utilization.

## Step 2: Prepare the new cluster

### 1. Adjust the GC lifetime of the old cluster

To ensure data replication stability, adjust the system variable [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50) to a value that covers the total duration of the following operations and intervals: BR backup, BR restore, cluster upgrade, and TiCDC Changefeed replication setup. Otherwise, the replication task might enter an unrecoverable `failed` state, requiring a restart of the entire migration and upgrade process from a new full backup.

The following example sets `tidb_gc_life_time` to `60h`:

```sql
-- Check the current GC lifetime setting.
SHOW VARIABLES LIKE '%tidb_gc_life_time%';
-- Set GC lifetime.
SET GLOBAL tidb_gc_life_time=60h;
```

> **Note:**
>
> Increasing `tidb_gc_life_time` increases storage usage for [MVCC](/glossary.md#multi-version-concurrency-control-mvcc) data and might affect query performance. For more information, see [GC Overview](/garbage-collection-overview.md). Adjust the GC duration based on estimated operation time while considering storage and performance impacts.

### 2. Migrate full data to the new cluster

When migrating full data to the new cluster, note the following:

- **Version compatibility**: the BR version used for backup and restore must match the major version of the old cluster.
- **Performance impact**: BR backup consumes system resources. To minimize business impact, perform backups during off-peak hours.
- **Time estimation**: under optimal hardware conditions (no disk I/O or network bandwidth bottlenecks), estimated times are:

    - Backup speed: backing up 1 TiB of data per TiKV node with 8 threads takes approximately 1 hour.
    - Restore speed: restoring 1 TiB of data per TiKV node takes approximately 20 minutes.

- **Configuration consistency**: ensure that the [`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap) configuration is identical between the old and new clusters. Otherwise, BR restore will fail.
- **System table restore**: Use the `--with-sys-table` option during BR restore to recover system table data.

To migrate full data to the new cluster, take the following steps:

1. Perform a full backup on the old cluster:

    ```shell
    tiup br:${cluster_version} backup full --pd ${pd_host}:${pd_port} -s ${backup_location}
    ```

2. Record the TSO of the old cluster for later TiCDC Changefeed creation:

    ```shell
    tiup br:${cluster_version} validate decode --field="end-version" \
    --storage "s3://xxx?access-key=${access-key}&secret-access-key=${secret-access-key}" | tail -n1
    ```

3. Deploy the new cluster:

    ```shell
    tiup cluster deploy ${new_cluster_name} ${cluster_version} tidb-cluster.yaml
    ```

4. Restore the full backup to the new cluster:

    ```shell
    tiup br:${cluster_version} restore full --pd ${pd_host}:${pd_port} -s ${backup_location} --with-sys-table
    ```

### 3. Upgrade the new cluster to the target version

To save time, you can perform an offline upgrade using the following commands. For more upgrade methods, see [Upgrade TiDB Using TiUP](/upgrade-tidb-using-tiup.md).

```shell
tiup cluster stop <new_cluster_name>      # Stop the cluster
tiup cluster upgrade <new_cluster_name> <v_target_version> --offline  # Perform offline upgrade
tiup cluster start <new_cluster_name>     # Start the cluster
```

To maintain business continuity, you need to replicate essential configurations from the old cluster to the new cluster, such as configuration items and system variables.

## Step 3: Replicate incremental data

### 1. Establish a forward data replication channel

At this stage, the old cluster remains at its original version, while the new cluster has been upgraded to the target version. In this step, you need to establish a forward data replication channel from the old cluster to the new cluster.

> **Note:**
>
> The TiCDC component version must match the major version of the old cluster.

- Create a Changefeed task and set the incremental replication starting point (`${tso}`) to the exact backup TSO recorded in [Step 2](#step-2-prepare-the-new-cluster) to prevent data loss:

    ```shell
    tiup ctl:${cluster_version} cdc changefeed create --server http://${cdc_host}:${cdc_port} --sink-uri="mysql://${username}:${password}@${tidb_endpoint}:${port}" --config config.toml --start-ts ${tso}
    ```

- Check the replication task status and confirm that `tso` or `checkpoint` is continuously advancing:

    ```shell
    tiup ctl:${cluster_version} cdc changefeed list --server http://${cdc_host}:${cdc_port}
    ```

    The output is as follows:

    ```shell
    [{
        "id": "cdcdb-cdc-task-standby",
        "summary": {
          "state": "normal",
          "tso": 417886179132964865,
          "checkpoint": "202x-xx-xx xx:xx:xx.xxx",
          "error": null
        }
    }]
    ```

During incremental data replication, continuously monitor the replication channel status and adjust settings if needed:

- Latency metrics: ensure that `Changefeed checkpoint lag` remains within an acceptable range, such as within 5 minutes.
- Throughput health: ensure that `Sink flush rows/s` consistently exceeds the business write rate.
- Errors and alerts: regularly check TiCDC logs and alert information.
- (Optional) Test data replication: update test data and verify that Changefeed correctly replicates it to the new cluster.
- (Optional) Adjust the TiCDC configuration item [`gc-ttl`](/ticdc/ticdc-server-config.md) (defaults to 24 hours).

    If a replication task is unavailable or interrupted and cannot be resolved in time, `gc-ttl` ensures that data needed by TiCDC is retained in TiKV without being cleaned by garbage collection (GC). If this duration is exceeded, the replication task enters a `failed` state and cannot recover. In this case, PD's GC safe point continues advancing, requiring a new backup to restart the process.

    Increasing the value of `gc-ttl` accumulates more MVCC data, similar to increasing `tidb_gc_life_time`. It is recommended to set it to a reasonably long but appropriate value.

### 2. Verify data consistency

After data replication is complete, verify data consistency between the old and new clusters using the following methods:

- Use the [sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md) tool:

    ```shell
    ./sync_diff_inspector --config=./config.toml
    ```

- Use the snapshot configuration of [sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md) with the [Syncpoint](/ticdc/ticdc-upstream-downstream-check.md) feature of TiCDC to verify data consistency without stopping Changefeed replication. For more information, see [Upstream and Downstream Clusters Data Validation and Snapshot Read](/ticdc/ticdc-upstream-downstream-check.md).

- Perform manual validation of business data, such as comparing table row counts.

### 3. Finalize the environment setup

This migration procedure restores some system table data using the BR `--with-sys-table` option. For tables that are not included in the scope, you need to manually restore. Common items to check and supplement include:

- User privileges: compare the `mysql.user` table.
- Configuration settings: ensure that configuration items and system variables are consistent.
- Auto-increment columns: clear auto-increment ID caches in the new cluster.
- Statistics: collect statistics manually or enable automatic collection in the new cluster.

Additionally, you can scale out the new cluster to handle expected workloads and migrate operational tasks, such as alert subscriptions, scheduled statistics collection scripts, and data backup scripts.

## Step 4: Switch business traffic and rollback

### 1. Prepare for the switchover

- Confirm replication status:

    - Monitor the latency of TiCDC Changefeed replication.
    - Ensure that the incremental replication throughput is greater than or equal to the peak business write rate.

- Perform multi-dimensional validation, such as:

    - Ensure that all data validation steps are complete and perform any necessary additional checks.
    - Conduct sanity or integration tests on the application in the new cluster.

### 2. Execute the switchover

1. Stop application services to prevent the old cluster from handling business traffic. To further restrict access, you can use one of the following methods:

    - Lock user accounts in the old cluster:

        ```sql
        ALTER USER ACCOUNT LOCK;
        ```

    - Set the old cluster to read-only mode. It is recommended to restart TiDB nodes in the old cluster to clear active business sessions and prevent connections that have not entered read-only mode:

        ```sql
        SET GLOBAL tidb_super_read_only=ON;
        ```

2. Ensure TiCDC catches up:

    - After setting the old cluster to read-only mode, retrieve the current `up-tso`:

        ```sql
        BEGIN; SELECT TIDB_CURRENT_TSO(); ROLLBACK;
        ```

    - Monitor the Changefeed `checkpointTs` to confirm it has surpassed `up-tso`, indicating that TiCDC has completed data replication.

3. Verify data consistency between the new and old clusters:

    - After TiCDC catches up, obtain the `down-tso` from the new cluster.
    - Use the [sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md) tool to compare data consistency between the new and old clusters at `up-tso` and `down-tso`.

4. Pause the forward Changefeed replication task:

    ```shell
    tiup ctl:${cluster_version} cdc changefeed pause --server http://${cdc_host}:${cdc_port} -c <changefeedid>
    ```

5. Restart the TiDB nodes in the new cluster to clear the auto-increment ID cache.

6. Check the operational status of the new cluster using the following methods:

    - Verify that the TiDB version matches the target version:

        ```shell
        tiup cluster display <cluster-name>
        ```

    - Log into the database and confirm component versions:

        ```sql
        SELECT * FROM INFORMATION_SCHEMA.CLUSTER_INFO;
        ```

    - Use Grafana to monitor service status: navigate to [**Overview > Services Port Status**](/grafana-overview-dashboard.md) and confirm that all services are in the **Up** state.

7. Set up reverse replication from the new cluster to the old cluster.

    1. Unlock user accounts in the old cluster and restore read-write mode:

        ```sql
        ALTER USER ACCOUNT UNLOCK;
        SET GLOBAL tidb_super_read_only=OFF;
        ```

    2. Record the current TSO of the new cluster:

        ```sql
        BEGIN; SELECT TIDB_CURRENT_TSO(); ROLLBACK;
        ```

    3. Configure the reverse replication link and ensure the Changefeed task is running properly:

        - Because business operations are stopped at this stage, you can use the current TSO.
        - Ensure that `sink-uri` is set to the address of the old cluster to avoid loopback writing risks.

        ```shell
        tiup ctl:${cluster_version} cdc changefeed create --server http://${cdc_host}:${cdc_port} --sink-uri="mysql://${username}:${password}@${tidb_endpoint}:${port}" --config config.toml --start-ts ${tso}

        tiup ctl:${cluster_version} cdc changefeed list --server http://${cdc_host}:${cdc_port}
        ```

8. Redirect business traffic to the new cluster.

9. Monitor the load and operational status of the new cluster using the following Grafana panels:

    - [**TiDB Dashboard > Query Summary**](/grafana-tidb-dashboard.md#query-summary): check the Duration, QPS, and Failed Query OPM metrics.
    - [**TiDB Dashboard > Server**](/grafana-tidb-dashboard.md#server): monitor the **Connection Count** metric to ensure even distribution of connections across nodes.

At this point, business traffic has successfully switched to the new cluster, and the TiCDC reverse replication channel is established.

### 3. Execute emergency rollback

The rollback plan is as follows:

- Check data consistency between the new and old clusters regularly to ensure the reverse replication link is operating properly.
- Monitor the system for a specified period, such as one week. If issues occur, switch back to the old cluster.
- After the observation period, remove the reverse replication link and delete the old cluster.

The following introduces the usage scenario and steps for an emergency rollback, which redirects traffic back to the old cluster:

- Usage scenario: execute the rollback plan if critical issues cannot be resolved.
- Steps:

    1. Stop business access to the new cluster.
    2. Reauthorize business accounts and restore read-write access to the old cluster.
    3. Check the reverse replication link, confirm TiCDC has caught up, and verify data consistency between the new and old clusters.
    4. Redirect business traffic back to the old cluster.

## Step 5: Clean up

After monitoring the new cluster for a period and confirming stable business operations, you can remove the TiCDC reverse replication and delete the old cluster.

- Remove the TiCDC reverse replication:

    ```shell
    tiup ctl:${cluster_version} cdc changefeed remove --server http://${cdc_host}:${cdc_port} -c <changefeedid>
    ```

- Delete the old cluster. If you choose to retain it, restore `tidb_gc_life_time` to its original value:

    ```sql
    -- Restore to the original value before modification.
    SET GLOBAL tidb_gc_life_time=10m;
    ```
