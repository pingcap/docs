---
title: 创建 TiFlash 副本
summary: 了解如何创建 TiFlash 副本。
---

# 创建 TiFlash 副本

本文介绍如何为表和数据库创建 TiFlash 副本，以及如何为副本调度设置可用区。

## 为表创建 TiFlash 副本

TiFlash 连接到 TiKV 集群后，默认不会开始数据复制。你可以通过 MySQL 客户端向 TiDB 发送 DDL 语句，为指定表创建 TiFlash 副本：

```sql
ALTER TABLE table_name SET TIFLASH REPLICA count;
```

上述命令的参数说明如下：

- `count` 表示副本数量。当该值为 `0` 时，表示删除副本。

> **Note:**
>
> 对于 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 集群，TiFlash 副本的 `count` 只能为 `2`。如果你设置为 `1`，会自动调整为 `2` 执行。如果你设置为大于 2 的数值，则会报副本数量的错误。

如果你对同一张表执行多条 DDL 语句，只有最后一条语句会生效。如下例所示，对表 `tpch50` 执行了两条 DDL 语句，但只有第二条（删除副本）生效。

为表创建两个副本：

```sql
ALTER TABLE `tpch50`.`lineitem` SET TIFLASH REPLICA 2;
```

删除副本：

```sql
ALTER TABLE `tpch50`.`lineitem` SET TIFLASH REPLICA 0;
```

**注意事项：**

* 如果通过上述 DDL 语句将表 `t` 复制到 TiFlash，则使用如下语句创建的表也会自动复制到 TiFlash：

    ```sql
    CREATE TABLE table_name like t;
    ```

* 在 v4.0.6 之前的版本中，如果你在使用 TiDB Lightning 导入数据前就创建了 TiFlash 副本，数据导入会失败。你必须先向表中导入数据，再为该表创建 TiFlash 副本。

* 如果 TiDB 和 TiDB Lightning 都是 v4.0.6 或更高版本，无论表是否有 TiFlash 副本，你都可以使用 TiDB Lightning 向该表导入数据。需要注意的是，这可能会导致 TiDB Lightning 导入过程变慢，具体取决于 lightning 主机的网卡带宽、TiFlash 节点的 CPU 和磁盘负载，以及 TiFlash 副本的数量。

* 建议不要复制超过 1,000 张表，否则会降低 PD 的调度性能。该限制将在后续版本中移除。

* 在 v5.1 及以上版本，不再支持为系统表设置副本。在升级集群前，你需要清除相关系统表的副本。否则，升级到新版本后将无法修改系统表的副本设置。

* 当前，使用 TiCDC 将表同步到下游 TiDB 集群时，不支持为这些表创建 TiFlash 副本，即 TiCDC 不支持同步与 TiFlash 相关的 DDL 语句，例如：

    * `ALTER TABLE table_name SET TIFLASH REPLICA count;`
    * `ALTER DATABASE db_name SET TIFLASH REPLICA count;`

### 查看复制进度

你可以使用以下语句查看指定表的 TiFlash 副本状态。表通过 `WHERE` 子句指定。如果去掉 `WHERE` 子句，则会查看所有表的副本状态。

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = '<db_name>' and TABLE_NAME = '<table_name>';
```

上述语句的结果中：

* `AVAILABLE` 表示该表的 TiFlash 副本是否可用。`1` 表示可用，`0` 表示不可用。一旦副本变为可用，该状态不会再变化。如果你通过 DDL 语句修改副本数量，复制状态会重新计算。
* `PROGRESS` 表示复制进度。取值范围为 `0.0` 到 `1.0`。`1` 表示至少有一个副本已完成复制。

## 为数据库创建 TiFlash 副本

与为表创建 TiFlash 副本类似，你可以通过 MySQL 客户端向 TiDB 发送 DDL 语句，为指定数据库下的所有表创建 TiFlash 副本：

```sql
ALTER DATABASE db_name SET TIFLASH REPLICA count;
```

在该语句中，`count` 表示副本数量。当你设置为 `0` 时，表示删除副本。

示例：

- 为数据库 `tpch50` 下的所有表创建两个副本：

    ```sql
    ALTER DATABASE `tpch50` SET TIFLASH REPLICA 2;
    ```

- 删除为数据库 `tpch50` 创建的 TiFlash 副本：

    ```sql
    ALTER DATABASE `tpch50` SET TIFLASH REPLICA 0;
    ```

> **Note:**
>
> - 该语句实际会执行一系列 DDL 操作，资源消耗较大。如果执行过程中被中断，已执行的操作不会回滚，未执行的操作也不会继续。
>
> - 执行该语句后，在**所有表都完成副本复制之前**，不要再设置 TiFlash 副本数量或对该数据库执行 DDL 操作。否则，可能会出现以下异常情况：
>     - 如果你将 TiFlash 副本数设置为 2，但在所有表都复制完成前又改为 1，则最终所有表的 TiFlash 副本数不一定是 1 或 2。
>     - 执行该语句后，如果在语句执行完成前在该数据库中创建新表，这些新表**可能会**也可能不会创建 TiFlash 副本。
>     - 执行该语句后，如果在语句执行完成前为数据库中的表添加索引，语句可能会卡住，直到索引添加完成后才会继续。
>
> - 如果在语句执行**完成后**再在该数据库中创建新表，这些新表不会自动创建 TiFlash 副本。
>
> - 该语句会跳过系统表、视图、临时表以及 TiFlash 不支持字符集的表。

> - 你可以通过设置 [`tidb_batch_pending_tiflash_count`](/system-variables.md#tidb_batch_pending_tiflash_count-new-in-v60) 系统变量，控制执行过程中允许处于不可用状态的表的数量。降低该值有助于减少复制期间对集群的压力。需要注意的是，该限制并非实时生效，因此设置后仍有可能出现不可用表数量超过限制的情况。

### 查看复制进度

与为表创建 TiFlash 副本类似，DDL 语句执行成功并不代表复制已完成。你可以执行以下 SQL 语句，查看目标表的复制进度：

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = '<db_name>';
```

如需查看数据库中没有 TiFlash 副本的表，可以执行以下 SQL 语句：

```sql
SELECT TABLE_NAME FROM information_schema.tables where TABLE_SCHEMA = "<db_name>" and TABLE_NAME not in (SELECT TABLE_NAME FROM information_schema.tiflash_replica where TABLE_SCHEMA = "<db_name>");
```

## 加速 TiFlash 复制

<CustomContent platform="tidb-cloud">

> **Note:**
>
> 本节内容不适用于 TiDB Cloud。

</CustomContent>

当你执行以下任一操作时，TiDB 集群会触发 TiFlash 副本的复制流程：

* 为表添加 TiFlash 副本。
* 新增 TiFlash 实例，导致 PD 将 TiFlash 副本从原有实例调度到新 TiFlash 实例。

在此过程中，每个 TiKV 实例会对全表进行扫描，并将扫描到的数据快照发送到 TiFlash 以创建副本。默认情况下，为了尽量减少对 TiKV 和 TiFlash 生产负载的影响，TiFlash 以较慢的速率添加副本，并使用较少的资源。如果你的 TiKV 和 TiFlash 节点有充足的 CPU 和磁盘 I/O 资源，可以通过以下步骤加速 TiFlash 复制。

1. 通过 [动态配置 SQL 语句](https://docs.pingcap.com/tidb/stable/dynamic-config) 临时提升每个 TiKV 和 TiFlash 实例的快照写入速度上限：

    ```sql
    -- 这两个配置的默认值均为 100MiB，即写入快照的最大磁盘带宽不超过 100MiB/s。
    SET CONFIG tikv `server.snap-io-max-bytes-per-sec` = '300MiB';
    SET CONFIG tiflash `raftstore-proxy.server.snap-io-max-bytes-per-sec` = '300MiB';
    ```

    执行上述 SQL 语句后，配置会立即生效，无需重启集群。但由于复制速度仍受 PD 全局限制，目前还无法观察到加速效果。

2. 使用 [PD Control](https://docs.pingcap.com/tidb/stable/pd-control) 逐步放宽副本调度速率限制。

    新副本的默认速率限制为 30，即每分钟每个 TiFlash 实例大约有 30 个 Region 添加或移除 TiFlash 副本。执行以下命令可将所有 TiFlash 实例的限制调整为 60，速度提升一倍：

    ```shell
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 60 add-peer
    ```

    > 在上述命令中，你需要将 `v<CLUSTER_VERSION>` 替换为实际的集群版本，如 `v8.5.3`，将 `<PD_ADDRESS>:2379` 替换为任意 PD 节点的地址。例如：
    >
    > ```shell
    > tiup ctl:v8.5.3 pd -u http://192.168.1.4:2379 store limit all engine tiflash 60 add-peer
    > ```

    如果集群中旧 TiFlash 节点上有大量 Region，PD 需要将它们重新平衡到新 TiFlash 节点。你需要相应调整 `remove-peer` 的限制。

    ```shell
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 60 remove-peer
    ```

    几分钟后，你会观察到 TiFlash 节点的 CPU 和磁盘 IO 资源使用率明显上升，TiFlash 副本创建速度加快。同时，TiKV 节点的 CPU 和磁盘 IO 资源使用率也会提升。

    如果此时 TiKV 和 TiFlash 节点仍有剩余资源，且你的在线服务延迟没有明显增加，可以进一步放宽限制，例如将速度提升至原来的三倍：

    ```shell
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 90 add-peer
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 90 remove-peer
    ```

3. TiFlash 复制完成后，恢复默认配置以减少对在线服务的影响。

    执行以下 PD Control 命令，恢复副本调度速率的默认限制：

    ```shell
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 30 add-peer
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 30 remove-peer
    ```

    执行以下 SQL 语句，恢复快照写入速率的默认值：

    ```sql
    SET CONFIG tikv `server.snap-io-max-bytes-per-sec` = '100MiB';
    SET CONFIG tiflash `raftstore-proxy.server.snap-io-max-bytes-per-sec` = '100MiB';
    ```

## 设置可用区

<CustomContent platform="tidb-cloud">

> **Note:**
>
> 本节内容不适用于 TiDB Cloud。

</CustomContent>

在配置副本时，如果你需要将 TiFlash 副本分布到多个数据中心以实现容灾，可以按照以下步骤配置可用区：

1. 在集群配置文件中为 TiFlash 节点指定 labels。

    ```
    tiflash_servers:
      - host: 172.16.5.81
          logger.level: "info"
        learner_config:
          server.labels:
            zone: "z1"
      - host: 172.16.5.82
        config:
          logger.level: "info"
        learner_config:
          server.labels:
            zone: "z1"
      - host: 172.16.5.85
        config:
          logger.level: "info"
        learner_config:
          server.labels:
            zone: "z2"
    ```

    注意，早期版本中的 `flash.proxy.labels` 配置无法正确处理可用区名称中的特殊字符。建议使用 `learner_config` 下的 `server.labels` 配置可用区名称。

2. 启动集群后，指定 TiFlash 副本数量以实现高可用。语法如下：

    ```sql
    ALTER TABLE table_name SET TIFLASH REPLICA count;
    ```

    例如：

    ```sql
    ALTER TABLE t SET TIFLASH REPLICA 2;
    ```

3. PD 会根据 TiFlash 节点 `learner_config` 中的 `server.labels` 以及表副本数量（`count`），将表 `t` 的副本调度到不同的可用区，以保证可用性。更多信息可参考 [通过拓扑标签调度副本](https://docs.pingcap.com/tidb/stable/schedule-replicas-by-topology-labels/)。你可以使用以下 SQL 语句，验证某张表的 Region 在 TiFlash 节点上的分布情况：

    ```sql
    -- 非分区表
    SELECT table_id, p.store_id, address, COUNT(p.region_id) 
    FROM
      information_schema.tikv_region_status r,
      information_schema.tikv_region_peers p,
      information_schema.tikv_store_status s
    WHERE
      r.db_name = 'test' 
      AND r.table_name = 'table_to_check'
      AND r.region_id = p.region_id 
      AND p.store_id = s.store_id
      AND JSON_EXTRACT(s.label, '$[0].value') = 'tiflash'
    GROUP BY table_id, p.store_id, address;

    -- 分区表
    SELECT table_id, r.partition_name, p.store_id, address, COUNT(p.region_id)
    FROM
      information_schema.tikv_region_status r,
      information_schema.tikv_region_peers p,
      information_schema.tikv_store_status s
    WHERE 
      r.db_name = 'test' 
      AND r.table_name = 'table_to_check' 
      AND r.partition_name LIKE 'p202312%'
      AND r.region_id = p.region_id 
      AND p.store_id = s.store_id
      AND JSON_EXTRACT(s.label, '$[0].value') = 'tiflash'
    GROUP BY table_id, r.partition_name, p.store_id, address
    ORDER BY table_id, r.partition_name, p.store_id;
    ```

<CustomContent platform="tidb">

关于使用标签调度副本的更多信息，请参见 [通过拓扑标签调度副本](/schedule-replicas-by-topology-labels.md)、[同城多数据中心部署](/multi-data-centers-in-one-city-deployment.md) 和 [两地三中心部署](/three-data-centers-in-two-cities-deployment.md)。

TiFlash 支持为不同可用区配置副本选择策略。更多信息请参见 [`tiflash_replica_read`](/system-variables.md#tiflash_replica_read-new-in-v730)。

</CustomContent>

> **Note:**
>
> 在语法 `ALTER TABLE table_name SET TIFLASH REPLICA count LOCATION LABELS location_labels;` 中，如果你为 `location_labels` 指定了多个标签，TiDB 无法正确解析并设置 placement rules。因此，不要使用 `LOCATION LABELS` 配置 TiFlash 副本。