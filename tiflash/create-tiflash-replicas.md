---
title: 创建 TiFlash 副本
summary: 了解如何创建 TiFlash 副本。
---

# 创建 TiFlash 副本

本文介绍如何为表和数据库创建 TiFlash 副本，以及设置可用区域以进行副本调度。

## 为表创建 TiFlash 副本

在 TiFlash 连接到 TiKV 集群后，默认情况下数据复制尚未开始。你可以通过 MySQL 客户端向 TiDB 发送 DDL 语句，为特定表创建 TiFlash 副本：

```sql
ALTER TABLE table_name SET TIFLASH REPLICA count;
```

上述命令参数说明如下：

- `count` 表示副本的数量。当值为 `0` 时，表示删除副本。

> **Note:**
>
> 对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群，TiFlash 副本的 `count` 只能是 `2`。如果你设置为 `1`，系统会自动调整为 `2` 进行执行。如果设置为大于 2 的数字，则会出现关于副本数量的错误。

如果你在同一张表上执行多条 DDL 语句，只有最后一条语句会生效。在以下示例中，针对表 `tpch50` 执行了两条 DDL 语句，但只有第二条（删除副本）生效。

为表创建两个副本：

```sql
ALTER TABLE `tpch50`.`lineitem` SET TIFLASH REPLICA 2;
```

删除副本：

```sql
ALTER TABLE `tpch50`.`lineitem` SET TIFLASH REPLICA 0;
```

**注意事项：**

* 如果通过上述 DDL 语句为表 `t` 创建了 TiFlash 副本，使用以下语句创建的表也会自动复制到 TiFlash：

    ```sql
    CREATE TABLE table_name like t;
    ```

* 对于版本早于 v4.0.6 的系统，如果在使用 TiDB Lightning 导入数据之前创建了 TiFlash 副本，数据导入将会失败。必须在为表创建 TiFlash 副本之前先导入数据。

* 如果 TiDB 和 TiDB Lightning 都是 v4.0.6 或更高版本，无论表是否已有 TiFlash 副本，都可以使用 TiDB Lightning 导入数据。注意，这可能会减慢 TiDB Lightning 的流程，具体取决于 lightning 主机的 NIC 带宽、TiFlash 节点的 CPU 和磁盘负载，以及 TiFlash 副本的数量。

* 建议不要为超过 1000 张表创建副本，因为这会降低 PD 的调度性能。此限制将在后续版本中取消。

* 在 v5.1 及更高版本中，不再支持为系统表设置副本。在升级集群之前，需清除相关系统表的副本，否则升级后无法修改系统表的副本设置。

* 当前，当你使用 TiCDC 将表复制到下游 TiDB 集群时，不支持为表创建 TiFlash 副本，也就是说，TiCDC 不支持复制与 TiFlash 相关的 DDL 语句，例如：

    * `ALTER TABLE table_name SET TIFLASH REPLICA count;`
    * `ALTER DATABASE db_name SET TIFLASH REPLICA count;`

### 检查复制进度

你可以使用以下语句检查某个表的 TiFlash 副本状态。通过 `WHERE` 子句指定表名。如果移除 `WHERE` 子句，则会检查所有表的副本状态。

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = '<db_name>' and TABLE_NAME = '<table_name>';
```

在上述语句的结果中：

* `AVAILABLE` 表示该表的 TiFlash 副本是否可用。`1` 表示可用，`0` 表示不可用。一旦副本变为可用，该状态不会变化。如果你用 DDL 语句修改副本数量，副本状态会重新计算。
* `PROGRESS` 表示复制的进度。值在 `0.0` 到 `1.0` 之间。`1` 表示至少有一个副本已完成复制。

## 为数据库创建 TiFlash 副本

与为表创建 TiFlash 副本类似，你可以通过 MySQL 客户端向 TiDB 发送 DDL 语句，为某个数据库中的所有表创建 TiFlash 副本：

```sql
ALTER DATABASE db_name SET TIFLASH REPLICA count;
```

其中，`count` 表示副本数量。设置为 `0` 表示删除副本。

示例：

- 为数据库 `tpch50` 中的所有表创建两个副本：

    ```sql
    ALTER DATABASE `tpch50` SET TIFLASH REPLICA 2;
    ```

- 删除为数据库 `tpch50` 创建的 TiFlash 副本：

    ```sql
    ALTER DATABASE `tpch50` SET TIFLASH REPLICA 0;
    ```

> **Note:**
>
> - 该语句实际上会执行一系列资源密集型的 DDL 操作。如果在执行过程中中断，已执行的操作不会回滚，未执行的操作也不会继续。
>
> - 执行完毕后，在所有表都完成复制之前，不要再为该数据库设置 TiFlash 副本数量或进行其他 DDL 操作，否则可能出现以下异常：
>     - 如果你将副本数设置为 2，然后在所有表完成复制之前将其改为 1，所有表的最终副本数不一定是 1 或 2。
>     - 执行完毕后，如果在复制完成之前在该数据库中创建新表，可能会或不会为新表自动创建 TiFlash 副本。
>     - 执行完毕后，如果在复制完成之前为数据库中的表添加索引，操作可能会挂起，直到索引添加完成后才会继续。
>
> - 如果在执行完毕后在该数据库中创建新表，TiFlash 副本不会自动为新表创建。
>
> - 该语句会跳过系统表、视图、临时表以及字符集不被 TiFlash 支持的表。

> - 你可以通过设置 [`tidb_batch_pending_tiflash_count`](/system-variables.md#tidb_batch_pending_tiflash_count-new-in-v60) 系统变量，控制在执行过程中允许保持不可用的表的最大数量。降低该值有助于减轻复制过程中的集群压力。注意，该限制不是实时的，设置后不可用表的数量仍可能超过限制。

### 检查复制进度

与为表创建 TiFlash 副本类似，DDL 语句成功执行并不代表复制已完成。你可以执行以下 SQL 语句，检查目标表的复制进度：

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = '<db_name>';
```

若要检查数据库中没有 TiFlash 副本的表，可以执行：

```sql
SELECT TABLE_NAME FROM information_schema.tables where TABLE_SCHEMA = "<db_name>" and TABLE_NAME not in (SELECT TABLE_NAME FROM information_schema.tiflash_replica where TABLE_SCHEMA = "<db_name>");
```

## 加快 TiFlash 复制速度

<CustomContent platform="tidb-cloud">

> **Note:**
>
> 本节内容不适用于 TiDB Cloud。

</CustomContent>

在添加 TiFlash 副本之前，每个 TiKV 实例会进行全表扫描，并将扫描到的数据作为“快照”发送给 TiFlash，以创建副本。默认情况下，TiFlash 副本的添加速度较慢，资源使用较少，以尽量减少对线上服务的影响。如果你的 TiKV 和 TiFlash 节点有剩余的 CPU 和磁盘 IO 资源，可以通过以下步骤加快 TiFlash 复制速度。

1. 临时提高每个 TiKV 和 TiFlash 实例的快照写入速度限制，使用 [动态配置 SQL 语句](https://docs.pingcap.com/tidb/stable/dynamic-config)：

    ```sql
    -- 两个配置的默认值都是 100MiB，即写入快照的最大磁盘带宽不超过 100MiB/s。
    SET CONFIG tikv `server.snap-io-max-bytes-per-sec` = '300MiB';
    SET CONFIG tiflash `raftstore-proxy.server.snap-io-max-bytes-per-sec` = '300MiB';
    ```

    执行完这些 SQL 语句后，配置立即生效，无需重启集群。但由于复制速度仍受 PD 全局限制，暂时无法观察到加速效果。

2. 使用 [PD Control](https://docs.pingcap.com/tidb/stable/pd-control) 逐步放宽新副本的速度限制。

    默认新副本速度限制为 30，意味着每分钟大约添加 30 个 Regions 的 TiFlash 副本。执行以下命令可以将限制调整为 60，速度翻倍：

    ```shell
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 60 add-peer
    ```

    > 在上述命令中，将 `v<CLUSTER_VERSION>` 替换为实际的集群版本，例如 `v8.1.2`，将 `<PD_ADDRESS>:2379` 替换为任意 PD 节点的地址。例如：
    >
    > ```shell
    > tiup ctl:v8.1.2 pd -u http://192.168.1.4:2379 store limit all engine tiflash 60 add-peer
    > ```

    几分钟内，你会观察到 TiFlash 节点的 CPU 和磁盘 IO 资源使用显著增加，副本创建速度加快。同时，TiKV 节点的 CPU 和磁盘 IO 资源使用也会增加。

    如果此时 TiKV 和 TiFlash 节点仍有剩余资源，且线上服务延迟没有明显增加，可以进一步放宽限制，例如将速度提高三倍：

    ```shell
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 90 add-peer
    ```

3. TiFlash 副本创建完成后，恢复到默认配置以减轻线上服务压力。

    执行以下 PD Control 命令，恢复默认的新副本速度限制：

    ```shell
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 30 add-peer
    ```

    执行以下 SQL 语句，恢复默认的快照写入速度限制：

    ```sql
    SET CONFIG tikv `server.snap-io-max-bytes-per-sec` = '100MiB';
    SET CONFIG tiflash `raftstore-proxy.server.snap-io-max-bytes-per-sec` = '100MiB';
    ```

## 设置可用区域

<CustomContent platform="tidb-cloud">

> **Note:**
>
> 本节内容不适用于 TiDB Cloud。

</CustomContent>

在配置副本时，如果需要将 TiFlash 副本分布到多个数据中心以实现灾备，可以按照以下步骤配置可用区域：

1. 在集群配置文件中为 TiFlash 节点指定标签。

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

    注意，早期版本中的 `flash.proxy.labels` 配置不能正确处理可用区域名称中的特殊字符。建议使用 `learner_config` 中的 `server.labels` 来配置可用区域的名称。

2. 启动集群后，在创建副本时指定标签。

    ```sql
    ALTER TABLE table_name SET TIFLASH REPLICA count LOCATION LABELS location_labels;
    ```

    例如：

    ```sql
    ALTER TABLE t SET TIFLASH REPLICA 2 LOCATION LABELS "zone";
    ```

3. PD 根据标签调度副本。在此示例中，PD 会将表 `t` 的两个副本分别调度到两个可用区域。你可以使用 pd-ctl 查看调度情况。

    ```shell
    > tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store

        ...
        "address": "172.16.5.82:23913",
        "labels": [
          { "key": "engine", "value": "tiflash"},
          { "key": "zone", "value": "z1" }
        ],
        "region_count": 4,

        ...
        "address": "172.16.5.81:23913",
        "labels": [
          { "key": "engine", "value": "tiflash"},
          { "key": "zone", "value": "z1" }
        ],
        "region_count": 5,
        ...

        "address": "172.16.5.85:23913",
        "labels": [
          { "key": "engine", "value": "tiflash"},
          { "key": "zone", "value": "z2" }
        ],
        "region_count": 9,
        ...
    ```

<CustomContent platform="tidb">

关于使用标签调度副本的更多信息，请参见 [Schedule Replicas by Topology Labels](/schedule-replicas-by-topology-labels.md)、[Multiple Data Centers in One City Deployment](/multi-data-centers-in-one-city-deployment.md) 和 [Three Data Centers in Two Cities Deployment](/three-data-centers-in-two-cities-deployment.md)。

TiFlash 支持为不同区域配置副本选择策略。更多信息请参见 [`tiflash_replica_read`](/system-variables.md#tiflash_replica_read-new-in-v730)。

</CustomContent>