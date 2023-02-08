---
title: DR Solution based on Primary and Secondary Clusters
summary: Learn how to implement primary-secondary disaster recovery based on TiCDC.
---

# DR Solution based on Primary and Secondary Clusters

Disaster recovery (DR) based on primary and secondary databases is a common solution. In this solution, the DR system has a primary cluster and a secondary cluster. The primary cluster handles user requests, while the secondary cluster backs up the data of the primary database. When the primary cluster fails, the system switches to the secondary cluster and continues to provide services using the backed up data. In this way, the system continues to run normally even when a failure occurs, instead of being interrupted by the failure.

The primary-secondary DR solution has the following benefits:

- High availability: The primary-secondary architecture enhances the availability of the system essentially. This guarantees quick system recovery from any failure.
- Fast switchover: When the primary cluster fails, the system can quickly switches to the secondary cluster and continues to provide services.
- Data consistency: The secondary cluster backs up the data of the primary cluster in almost real time. In this way, the data is basically up-to-date when the system switches to the secondary cluster due to a failure.

This document includes the following contents:

- Set up a primary cluster and a secondary cluster.
- Replicate data from the primary cluster to the secondary cluster.
- Monitor the cluster.
- Perform a DR switchover.

Meanwhile, this document also describes how to query the business data on the secondary cluster and how to perform bidirectional replication between the primary and secondary clusters.

## Set up primary and secondary clusters based on TiCDC

### Architecture

![TiCDC secondary cluster architecture](/media/dr/dr-ticdc-secondary-cluster.png)

The preceding architecture includes two TiDB clusters: Primary Cluster and Secondary Cluster.

- Primary Cluster: The active cluster that runs in Region 1 and has three replicas. This cluster handles read and write requests.
- Secondary Cluster: The standby cluster that runs in Region 2 and replicates data from Primary Cluster through TiCDC.

This DR architecture is simple and easy to use. Being capable of tolerating failures at the Region level, the DR system guarantees that the write performance of the primary cluster does not deteriorate, and the secondary cluster can handle some read-only business that is not sensitive to latency. The Recovery Point Objective (RPO) of this solution is in seconds, and the Recovery Time Objective (RTO) can be minutes or even lower. This is a solution recommended by many database vendors for important production systems.

> **Note:**
>
> Do not run multiple changefeeds to replicate data to the secondary cluster, or run another secondary cluster with the presence of a secondary cluster already. Otherwise, integrity of data transactions of the secondary cluster cannot be guaranteed.

### Set up primary and secondary clusters

In this document, the TiDB primary and secondary clusters are deployed in two different regions (Region 1 and Region 2). TiCDC is deployed together with the TiDB secondary cluster, because there is a certain network latency between the primary and secondary clusters. Deploying TiCDC with the secondary cluster can avoid the impact of network latency, which helps achieve optimal replication performance. The deployment topology of the example provided in this document is as follows (one component node is deployed on each server):

|**Region** | **Host** | **Cluster** | **Component** |
| --- | --- | --- | --- |
| Region 1 | 10.0.1.1/10.0.1.2/10.0.1.3 | Primary | PD |
| Region 1 | 10.0.1.4/10.0.1.5 | Primary| TiDB |
| Region 1 | 10.0.1.6/10.0.1.7/10.0.1.8 | Primary | TiKV |
| Region 1 | 10.0.1.9 | Primary | Monitor、Grafana 或 AlterManager |
| Region 2 | 10.1.1.9/10.1.1.10 | Primary | TiCDC |
| Region 2 | 10.1.1.1/10.1.1.2/10.1.1.3 | Secondary | PD |
| Region 2 | 10.1.1.4/10.1.1.5 | Secondary | TiDB |
| Region 2 | 10.1.1.6/10.1.1.7/10.1.1.8 | Secondary | TiKV |
| Region 2 | 10.0.1.11 | Secondary | Monitor、Grafana 或 AlterManager |

For server configurations, see the following documents:

- [Software and hardware recommendations for TiDB](/hardware-and-software-requirements.md)
- [Software and hardware recommendations for TiCDC](/ticdc/deploy-ticdc.md#software-and-hardware-recommendations)

For details about how to deploy TiDB primary and secondary clusters, see [Deploy a TiDB Cluster](/production-deployment-using-tiup.md).

When deploying TiCDC, note that the Secondary Cluster and TiCDC must be deployed and managed together, and the network between them must be connected.

- To deploy TiCDC on an existing primary cluster, see [Deploy TiCDC](/ticdc/deploy-ticdc.md#add-or-scale-out-ticdc-to-an-existing-tidb-cluster-using-tiup).
- To deploy a new primary cluster and TiCDC, use the following deployment template and modify the configuration parameters as needed:

    ```shell
    global:
    user: "tidb"
    ssh_port: 22
    deploy_dir: "/tidb-deploy"
    data_dir: "/tidb-data"
    server_configs: {}
    pd_servers:
    - host: 10.0.1.1
    - host: 10.0.1.2
    - host: 10.0.1.3
    tidb_servers:
    - host: 10.0.1.4
    - host: 10.0.1.5
    tikv_servers:
    - host: 10.0.1.6
    - host: 10.0.1.7
    - host: 10.0.1.8
    monitoring_servers:
    - host: 10.0.1.9
    grafana_servers:
    - host: 10.0.1.9
    alertmanager_servers:
    - host: 10.0.1.9
    cdc_servers:
    - host: 10.1.1.9
        gc-ttl: 86400
        data_dir: "/cdc-data"
        ticdc_cluster_id: "DR_TiCDC"
    - host: 10.1.1.10
        gc-ttl: 86400
        data_dir: "/cdc-data"
        ticdc_cluster_id: "DR_TiCDC"
    ```

### Replicate data from the primary cluster to the secondary cluster

After setting up the TiDB primary and secondary clusters, you need to first migrate the data from the primary cluster to the secondary cluster, and then create a replication task to replicate real-time change data from the primary cluster to the secondary cluster.

#### Select the external storage

External storage is used when migrating data and replicating real-time change data. Amazon S3 is a recommended choice. If the TiDB cluster is deployed in a self-built data center, the following methods are recommended:

* Build [MinIO](https://docs.min.io/docs/minio-quickstart-guide.html) as the backup storage system, and use the S3 protocol to back up data to MinIO.
* Mount Network File System (NFS, such as NAS) disks to br command-line tool, TiKV and TiCDC instances, and use the POSIX file system interface to write backup data to the corresponding NFS directory.

The following example uses MinIO as the storage system and is for reference only. Note that you need to prepare a separate server to deploy MinIO in Region 1 or Region 2.

```shell
wget https://dl.min.io/server/minio/release/linux-amd64/minio
chmod +x minio
# Configure access-key access-screct-id to access MinIO
export HOST_IP='10.0.1.10' # Replace it with the IP address of MinIO
export MINIO_ROOT_USER='minio'
export MINIO_ROOT_PASSWORD='miniostorage'
# Create the redo and backup directories. `backup` and `redo` are bucket names.
mkdir -p data/redo
mkdir -p data/backup
# Start minio at port 6060
nohup ./minio server ./data --address :6060 &
```

The preceding command starts a MinIO server on one node to simulate S3 services. Parameters in the command are configured as follows:

* `endpoint`: `http://10.0.1.10:6060/`
* `access-key`: `minio`
* `secret-access-key`: `miniostorage`
* `bucket`: `redo`/`backup`

The link is as follows:

```
s3://backup?access-key=minio&secret-access-key=miniostorage&endpoint=http://10.0.1.10:6060&force-path-style=true
```

#### Migrate data

Use the [backup and restore feature]((/br/backup-and-restore-overview.md)) to migrate data from the primary cluster to the secondary cluster.

1. Disable GC. To ensure that newly written data is not deleted during incremental migration, you should disable GC for the upstream cluster before backup. In this way, history data is not deleted.

    Run the following command to disable GC:

    ```sql
    MySQL [test]> SET GLOBAL tidb_gc_enable=FALSE;
    ```

    To verify that the change takes effect, query the value of `tidb_gc_enable`:

    ```sql
    MySQL [test]> SELECT @@global.tidb_gc_enable;
    ```

    ```
    +-------------------------+
    | @@global.tidb_gc_enable |
    +-------------------------+
    |                       0 |
    +-------------------------+
    1 row in set (0.00 sec)
    ```

    > **Note:**
    >
    > In production clusters, performing a backup with GC disabled might affect cluster performance. It is recommended that you back up data in off-peak hours, and set `RATE_LIMIT` to a proper value to avoid performance degradation.

2. Back up data. Run the `BACKUP` statement in the upstream cluster to back up data:

    ```sql
    MySQL [(none)]> BACKUP DATABASE * TO '`s3://backup?access-key=minio&secret-access-key=miniostorage&endpoint=http://10.0.1.10:6060&force-path-style=true`';
    ```

    ```
    +----------------------+----------+--------------------+---------------------+---------------------+
    | Destination          | Size     | BackupTS           | Queue Time          | Execution Time      |
    +----------------------+----------+--------------------+---------------------+---------------------+
    | s3://backup          | 10315858 | 431434047157698561 | 2022-02-25 19:57:59 | 2022-02-25 19:57:59 |
    +----------------------+----------+--------------------+---------------------+---------------------+
    1 row in set (2.11 sec)
    ```

    After the `BACKUP` command is executed, TiDB returns metadata about the backup data. Pay attention to `BackupTS`, because data generated before it is backed up. In this document, we use `BackupTS` as **the end of data check** and **the start of incremental migration scanning by TiCDC**.

3. Restore data. Run the `RESTORE` command in the secondary cluster to restore data:

    ```sql
    mysql> RESTORE DATABASE * FROM '`s3://backup?access-key=minio&secret-access-key=miniostorage&endpoint=http://10.0.1.10:6060&force-path-style=true`';
    ```

    ```
    +----------------------+----------+----------+---------------------+---------------------+
    | Destination          | Size     | BackupTS | Queue Time          | Execution Time      |
    +----------------------+----------+----------+---------------------+---------------------+
    | s3://backup          | 10315858 | 0        | 2022-02-25 20:03:59 | 2022-02-25 20:03:59 |
    +----------------------+----------+----------+---------------------+---------------------+
    1 row in set (41.85 sec)
    ```

#### Replicate incremental data

After migrating data as described in the preceding section, you can replicate incremental data from the primary cluster to the secondary cluster starting from the **BackupTS**.

1. Create a changefeed.

    Create a changefeed configuration file `changefeed.toml`.

    ```toml
    [consistent]
    # eventual consistency: Redo logs are used to ensure the eventual consistency in disaster scenarios.
    level = "eventual"
    # The size of a single redo log, in MiB. The default value is 64, and the recommended value is less than 128.
    max-log-size = 64
    # Interval for refreshing or uploading redo logs to Amazon S3, in milliseconds. The default value is 1000, and the recommended value range is 500-2000.
    flush-interval = 2000
    # The path where redo logs are saved.
    storage = "s3://redo?access-key=minio&secret-access-key=miniostorage&endpoint=http://10.0.1.10:6060&force-path-style=true"
    ```

    In the primary cluster, run the following command to create a changefeed from the primary to the secondary clusters:

    ```shell
    tiup cdc cli changefeed create --server=http://10.1.1.9:8300 --sink-uri="mysql://{username}:{password}@10.1.1.4:4000" --changefeed-id="dr-primary-to-secondary" --start-ts="431434047157698561"
    ```

    For more information about the changefeed configurations, see [TiCDC Changefeed Configurations](/ticdc/ticdc-changefeed-config.md).

2. To check whether a changefeed task runs properly, run the `changefeed query` command. The query result includes the task information and the task state. You can specify the `--simple` or `-s` argument to simplify the query result so that only the basic replication state and the checkpoint information are displayed. If you do not specify this argument, detailed task configuration, replication states, and replication table information are output.

    ```shell
    tiup cdc cli changefeed query -s --server=http://10.1.1.9:8300 --changefeed-id="dr-primary-to-secondary"
    ```

    ```shell
    {
    "state": "normal",
    "tso": 431434047157998561,  # The TSO to which the changefeed has been replicated
    "checkpoint": "2020-08-27 10:12:19.579", # The physical time corresponding to the TSO
    "error": null
    }
    ```

3. Enable GC.

    TiCDC ensures that history data is not garbage collected before it is replicated. Therefore, after creating a changefeed from the primary cluster to the secondary cluster, you can run the following command to enable GC again.

    ```sql

   Run the following command to enable GC:

    ```sql
    MySQL [test]> SET GLOBAL tidb_gc_enable=TRUE;
    ```

    To verify that the change takes effect, query the value of `tidb_gc_enable`:

    ```sql
    MySQL [test]> SELECT @@global.tidb_gc_enable;
    ```

    ```
    +-------------------------+
    | @@global.tidb_gc_enable |
    +-------------------------+
    |                       1 |
    +-------------------------+
    1 row in set (0.00 sec)
    ```

### Monitor the primary and secondary clusters

Currently, TiDB DR Dashboard is unavailable. You can check the status of TiDB primary and secondary cluster using the following dashboards and decide whether to perform a DR switchover:

- [TiDB Key Metrics](/grafana-overview-dashboard.md)
- [Changefeed Metrics](/ticdc/monitor-ticdc.md#changefeed)

### Perform DR Switchovers

This section describes planned DR switchovers, unplanned DR switchovers upon disasters, and the steps to rebuild a secondary cluster.

#### Planned primary and secondary switchover

定期对非常重要的业务系统进行容灾演练，检验系统的可靠性是非常有必要的。下面是容灾演练推荐的操作步骤，因为没有考虑演练中业务写入是否为模拟、业务访问数据库是否使用 proxy 服务等，与实际的演练场景会有出入，请根据你的实际情况进行修改。

1. 停止主集群上的业务写入。
2. 业务写入完全停止后，查询 TiDB 集群当前最新的 TSO: {Position}：

    ```sql
    mysql> show master status;
    +-------------+--------------------+--------------+------------------+-------------------+
    | File        | Position           | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
    +-------------+--------------------+--------------+------------------+-------------------+
    | tidb-binlog | 438223974697009153 |              |                  |                   |
    +-------------+--------------------+--------------+------------------+-------------------+
    1 row in set (0.33 sec)
    ```

3. 轮询 Changefeed (dr-primary-to-secondary) 的同步位置时间点 {TSO}，一直到满足 {TSO} >= {Position}。

    ```shell
    tiup cdc cli changefeed query -s --server=http://10.1.1.9:8300 --changefeed-id="dr-primary-to-secondary"

    {
        "state": "normal",
        "tso": 438224029039198209,  # Changefeed 已经同步到的时间点
        "checkpoint": "2022-12-22 14:53:25.307", # TSO 对应的物理时间点
        "error": null
    }
    ```

4. 停止 Changefeed (dr-primary-to-secondary)。通过删除 changefeed 的方式，暂停 Changefeed (dr-primary-to-secondary)：

    ```shell
    tiup cdc cli changefeed remove --server=http://10.1.1.9:8300 --changefeed-id="dr-primary-to-secondary"
    ```

5. 创建 Changefeed (dr-secondary-to-primary)。不需要指定 Changefeed `start-ts` 参数，Changefeed 从当前时间开始同步即可。
6. 修改业务应用的数据库访问配置，并重启业务应用，使得业务访问备用集群。
7. 检查业务状态是否正常。

容灾演练后，再重复一遍以上步骤，即可恢复原有的系统主备配置。

#### 真正灾难中主备切换

当发生真正的灾难，比如主集群所在区域停电，主备集群的同步链路可能会突然中断，从而导致备用集群数据处于事务不一致的状态。

1. 恢复备用集群到事务一致的状态。在 Region 2 的任意 TiCDC 节点执行以下命令，以向备用集群重放 redo log，使下游达到最终一致性状态：

    ```shell
    tiup cdc redo apply --storage "s3://redo?access-key=minio&secret-access-key=miniostorage&endpoint=http://10.0.1.10:6060&force-path-style=true" --tmp-dir /tmp/redo --sink-uri "mysql://{username}:{password}@10.1.1.4:4000"
    ```

    其中

    - `--storage`：指定 redo log 所在的 S3 位置
    - `--tmp-dir`：为从 S3 下载 redo log 的缓存目录
    - `--sink-uri`：指定下游集群的地址

2. 修改业务应用的数据库访问配置，并重启业务应用，使得业务访问备用集群。
3. 检查业务状态是否正常。

#### 灾难后重建主备集群

当 TiDB 主集群所遭遇的灾难解决后，或者主集群暂时不能恢复，此时 TiDB 集群是脆弱的，只有一个备用集群临时作为新的主集群提供服务。为了维持系统的可靠性，需要重建灾备集群保护系统的可靠性。

目前，重建 TiDB 主备集群，通用的方案是重新部署一个新的集群，组成新的容灾主备机群。操作请参考：

- [搭建主备集群](#搭建主备集群)。
- [从主集群复制数据到备用集群](#从主集群复制数据到备用集群)。
- 完成以上操作步骤后，如果你希望新集群成为主集群，那么请参考[主从切换](#容灾演练中主备切换)。

> **注意：**
>
> 如果在业务上能够修正灾难发生后主集群和备用集群的数据不一致的问题，那么也可以使用修正后的集群重建主备集群，而不需要重建新集群。

### 在备用集群上进行业务查询

在主备集群容灾场景中，将备用集群作为只读集群来运行一些延迟不敏感的查询是常见的需求，TiDB 主备集群容灾方案也提供了这种功能。

创建 changefeed 时候，你只需要在配置文件开启 Syncpoint 功能，Changefeed 就会定期 (`sync-point-interval`) 在备用集群中通过执行 `SET GLOBAL tidb_external_ts = @@tidb_current_ts` 设置已复制完成的一致性快照点。

当业务需要从备用集群查询数据的时候，在业务应用中设置 `SET GLOBAL|SESSION tidb_enable_external_ts_read = ON;` 就可以在备用集群上获得事务状态完成的数据。

```toml
# Starting from v6.4.0, only the changefeed with the SYSTEM_VARIABLES_ADMIN or SUPER privilege can use the TiCDC Syncpoint feature.
enable-sync-point = true

# Specifies the interval at which Syncpoint aligns the primary and secondary snapshots. It also indicates the maximum latency at which you can read the complete transaction, for example, read the transaction data generated on the primary cluster two minutes ago from the secondary cluster.
# The format is in h m s. For example, "1h30m30s". The default value is "10m" and the minimum value is "30s".
sync-point-interval = "10m"

# Specifies how long the data is retained by Syncpoint in the downstream table. When this duration is exceeded, the data is cleaned up.
# The format is in h m s. For example, "24h30m30s". The default value is "24h".
sync-point-retention = "1h"

[consistent]
# eventual consistency: Redo logs are used to ensure the eventual consistency in disaster scenarios.
level = "eventual"
# The size of a single redo log, in MiB. The default value is 64, and the recommended value is less than 128.
max-log-size = 64
# Interval for refreshing or uploading redo logs to Amazon S3, in milliseconds. The default value is 1000, and the recommended value range is 500-2000.
flush-interval = 2000
# The path where redo logs are saved.
storage = "s3://redo?access-key=minio&secret-access-key=miniostorage&endpoint=http://10.0.1.10:6060&force-path-style=true"
```

> **注意：**
>
> 在主备集群容灾架构中，每个备用集群只能被一个 changefeed 同步数据，否则就无法保证备用集群的数据事务完整性。

### 在主备集群之间进行双向复制

在主备集群容灾场景中，部分用户希望让两个区域的 TiDB 集群互为灾备集群：用户的业务流量按其区域属性写入对应的 TiDB 集群，同时两套 TiDB 集群备份对方集群的数据。

![TiCDC bidirectional replication](/media/dr/dr-ticdc.png)

在双向复制容灾集群方案中，两个区域的 TiDB 集群互相备份对方的数据，使得它们可以在故障发生时互为灾备集群。这种方案既能满足安全性和可靠性的需求，同时也能保证数据库的写入性能。在计划中的主备切换场景中，不需要停止正在运行的 changefeed 和启动新的 changefeed 等操作，在运维上也更加简单。

搭建双向容灾复制集群的步骤，请参考教程 [TiCDC 双向复制](/ticdc/ticdc-bidirectional-replication.md)。

## 常见问题处理

以上任何步骤遇到问题，可以先通过 [TiDB FAQ](/faq/faq-overview.md) 查找问题的处理方法。如果问题仍不能解决，请在 TiDB 项目中中提出 [issue](https://github.com/pingcap/tidb/issues/new/choose)，我们会尽快帮你解决。
