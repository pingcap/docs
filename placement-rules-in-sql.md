---
title: Placement Rules in SQL
summary: 学习如何使用 SQL 语句调度表和分区的存放位置。
---

# Placement Rules in SQL

Placement Rules in SQL 是一项允许你通过 SQL 语句指定数据在 TiKV 集群中的存放位置的功能。借助此功能，你可以将集群、数据库、表或分区的数据调度到特定的区域、数据中心、机架或主机。

此功能可以满足以下用例：

- 在多个数据中心部署数据，并配置规则以优化高可用性策略。
- 合并来自不同应用的多个数据库，物理隔离不同用户的数据，满足实例内不同用户的隔离需求。
- 增加重要数据的副本数，以提升应用的可用性和数据的可靠性。

> **Note:**
>
> 该功能在 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

## 概述

借助 SQL 中的 Placement Rules 功能，你可以 [创建调度策略](#create-and-attach-placement-policies) 并为不同层级的数据配置期望的调度策略，粒度从粗到细如下：

| 层级            | 描述                                                                                     |
|------------------|------------------------------------------------------------------------------------------|
| Cluster          | 默认情况下，TiDB 为集群配置了 3 副本的策略。你可以为你的集群配置全局调度策略。更多信息，见 [Specify the number of replicas globally for a cluster](#specify-the-number-of-replicas-globally-for-a-cluster)。 |
| Database         | 你可以为特定数据库配置调度策略。更多信息，见 [Specify a default placement policy for a database](#specify-a-default-placement-policy-for-a-database)。 |
| Table            | 你可以为特定表配置调度策略。更多信息，见 [Specify a placement policy for a table](#specify-a-placement-policy-for-a-table)。 |
| Partition        | 你可以为表中的不同行创建分区，并分别配置分区的调度策略。更多信息，见 [Specify a placement policy for a partitioned table](#specify-a-placement-policy-for-a-partitioned-table)。 |

> **Tip:**
>
> *Placement Rules in SQL* 的实现依赖于 PD 的 *placement rules feature*。详情请参考 [Configure Placement Rules](https://docs.pingcap.com/tidb/stable/configure-placement-rules)。在 SQL 中的 Placement Rules 语境下，*placement rules* 可能指附加到其他对象的 *placement policies*，也可能指从 TiDB 发送到 PD 的规则。

## 限制

- 为简化维护，建议集群内的调度策略数量限制在 10 个或以下。
- 建议附加调度策略的表和分区总数限制在 1 万个或以下。附加过多的表和分区可能会增加 PD 的计算负载，从而影响服务性能。
- 建议按照本文提供的示例使用 SQL 中的 Placement Rules 功能，而非使用其他复杂的调度策略。

## 前提条件

调度策略依赖于 TiKV 节点上的标签配置。例如，`PRIMARY_REGION` 调度选项依赖于 TiKV 的 `region` 标签。

<CustomContent platform="tidb">

在创建调度策略时，TiDB 不会检查策略中指定的标签是否存在，而是在你附加策略时进行检查。因此，在附加调度策略之前，确保每个 TiKV 节点都已配置正确的标签。TiDB 自管理集群的配置方法如下：

```
tikv-server --labels region=<region>,zone=<zone>,host=<host>
```

详细配置方法请参考以下示例：

| 部署方式 | 示例 |
| --- | --- |
| 手动部署 | [Schedule replicas by topology labels](/schedule-replicas-by-topology-labels.md) |
| 使用 TiUP 部署 | [Geo-distributed deployment topology](/geo-distributed-deployment-topology.md) |
| 使用 TiDB Operator 部署 | [Configure a TiDB cluster in Kubernetes](https://docs.pingcap.com/tidb-in-kubernetes/stable/configure-a-tidb-cluster#high-availability-of-data) |

> **Note:**
>
> 对于 TiDB Cloud Dedicated 集群，可以跳过这些标签配置步骤，因为 TiKV 节点上的标签在 TiDB Cloud Dedicated 集群中会自动配置。

</CustomContent>

<CustomContent platform="tidb-cloud">

对于 TiDB Cloud Dedicated 集群，TiKV 节点上的标签会自动配置。

</CustomContent>

要查看当前 TiKV 集群中所有可用的标签，可以使用 [`SHOW PLACEMENT LABELS`](/sql-statements/sql-statement-show-placement-labels.md) 语句：

```sql
SHOW PLACEMENT LABELS;
+--------+----------------+
| Key    | Values         |
+--------+----------------+
| disk   | ["ssd"]        |
| region | ["us-east-1"]  |
| zone   | ["us-east-1a"] |
+--------+----------------+
3 rows in set (0.00 sec)
```

## 使用方法

本节介绍如何使用 SQL 语句创建、附加、查看、修改和删除调度策略。

### 创建并附加调度策略

1. 使用 [`CREATE PLACEMENT POLICY`](/sql-statements/sql-statement-create-placement-policy.md) 语句创建调度策略：

```sql
CREATE PLACEMENT POLICY myplacementpolicy PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1";
```

在此语句中：

- `PRIMARY_REGION="us-east-1"` 表示将 Raft Leader 放置在标签为 `region` 且值为 `us-east-1` 的节点上。
- `REGIONS="us-east-1,us-west-1"` 表示将 Raft Follower 放置在标签为 `region` 且值为 `us-east-1` 和 `us-west-1` 的节点上。

更多可配置的调度选项及其含义，见 [Placement options](#placement-option-reference)。

2. 使用 `CREATE TABLE` 或 `ALTER TABLE` 语句为表或分区表指定调度策略，从而将调度策略附加到表或分区表：

```sql
CREATE TABLE t1 (a INT) PLACEMENT POLICY=myplacementpolicy;
CREATE TABLE t2 (a INT);
ALTER TABLE t2 PLACEMENT POLICY=myplacementpolicy;
```

`PLACEMENT POLICY` 不与任何数据库 schema 关联，可以在全局范围内附加。因此，使用 `CREATE TABLE` 指定调度策略不需要额外权限。

### 查看调度策略

- 查看已有的调度策略，可以使用 [`SHOW CREATE PLACEMENT POLICY`](/sql-statements/sql-statement-show-create-placement-policy.md) 语句：

```sql
SHOW CREATE PLACEMENT POLICY myplacementpolicy\G
*************************** 1. row ***************************
       Policy: myplacementpolicy
Create Policy: CREATE PLACEMENT POLICY myplacementpolicy PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1"
1 row in set (0.00 sec)
```

- 查看某个表附加的调度策略，可以使用 [`SHOW CREATE TABLE`](/sql-statements/sql-statement-show-create-table.md) 语句：

```sql
SHOW CREATE TABLE t1\G
*************************** 1. row ***************************
       Table: t1
Create Table: CREATE TABLE `t1` (
  `a` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin /*T![placement] PLACEMENT POLICY=`myplacementpolicy` */
1 row in set (0.00 sec)
```

- 查询集群中定义的调度策略，可以访问 [`INFORMATION_SCHEMA.PLACEMENT_POLICIES`](/information-schema/information-schema-placement-policies.md) 系统表：

```sql
SELECT * FROM information_schema.placement_policies\G
***************************[ 1. row ]***************************
POLICY_ID            | 1
CATALOG_NAME         | def
POLICY_NAME          | p1
PRIMARY_REGION       | us-east-1
REGIONS              | us-east-1,us-west-1
CONSTRAINTS          |
LEADER_CONSTRAINTS   |
FOLLOWER_CONSTRAINTS |
LEARNER_CONSTRAINTS  |
SCHEDULE             |
FOLLOWERS            | 4
LEARNERS             | 0
1 row in set
```

- 查看集群中所有附加了调度策略的表，可以查询 `information_schema.tables` 系统表中的 `tidb_placement_policy_name` 列：

```sql
SELECT * FROM information_schema.tables WHERE tidb_placement_policy_name IS NOT NULL;
```

- 查看集群中所有附加了调度策略的分区，可以查询 `information_schema.partitions` 系统表中的 `tidb_placement_policy_name` 列：

```sql
SELECT * FROM information_schema.partitions WHERE tidb_placement_policy_name IS NOT NULL;
```

- 所有对象附加的调度策略会异步生效。若要检查调度策略的调度进度，可以使用 [`SHOW PLACEMENT`](/sql-statements/sql-statement-show-placement.md) 语句：

```sql
SHOW PLACEMENT;
```

### 修改调度策略

要修改调度策略，可以使用 [`ALTER PLACEMENT POLICY`](/sql-statements/sql-statement-alter-placement-policy.md) 语句。修改会应用到所有附加了该策略的对象。

```sql
ALTER PLACEMENT POLICY myplacementpolicy FOLLOWERS=4;
```

在此语句中，`FOLLOWERS=4` 表示配置数据的副本数为 5 个，包括 4 个 Follower 和 1 个 Leader。更多可配置的调度选项及其含义，见 [Placement option reference](#placement-option-reference)。

### 删除调度策略

删除未附加到任何表或分区的策略，可以使用 [`DROP PLACEMENT POLICY`](/sql-statements/sql-statement-drop-placement-policy.md) 语句：

```sql
DROP PLACEMENT POLICY myplacementpolicy;
```

## Placement option reference

在创建或修改调度策略时，可以根据需要配置调度选项。

> **Note:**
>
> `PRIMARY_REGION`、`REGIONS` 和 `SCHEDULE` 选项不能与 `CONSTRAINTS` 选项同时指定，否则会报错。

### 常规调度选项

常规调度选项可以满足数据存放的基本需求。

| 选项名                | 描述                                                                                     |
|------------------------|------------------------------------------------------------------------------------------|
| `PRIMARY_REGION`       | 指定将 Raft Leader 放置在标签为 `region` 且值为此选项值的节点上。                        |
| `REGIONS`              | 指定将 Raft Follower 放置在标签为 `region` 且值为此选项值的节点上。                        |
| `SCHEDULE`             | 指定 Follower 的调度策略。值选项为 `EVEN`（默认）或 `MAJORITY_IN_PRIMARY`。             |
| `FOLLOWERS`            | 指定 Follower 数量。例如，`FOLLOWERS=2` 表示数据有 3 个副本（2 个 Follower 和 1 个 Leader）。 |

### 高级调度选项

高级配置选项提供了更大的灵活性，以满足复杂场景的需求。然而，配置高级选项比常规选项更复杂，需要你对集群拓扑和 TiDB 数据分片有深入理解。

| 选项名                | 描述                                                                                     |
|------------------------|------------------------------------------------------------------------------------------|
| `CONSTRAINTS`        | 一组适用于所有角色的约束。例如，`CONSTRAINTS="[+disk=ssd]"`。                          |
| `LEADER_CONSTRAINTS` | 仅适用于 Leader 的约束列表。                                                          |
| `FOLLOWER_CONSTRAINTS` | 仅适用于 Follower 的约束列表。                                                        |
| `LEARNER_CONSTRAINTS`  | 仅适用于 Learner 的约束列表。                                                          |
| `LEARNERS`             | Learner 数量。                                                                           |
| `SURVIVAL_PREFERENCE`  | 根据标签的灾难容错级别，定义副本的存活优先级。例如，`SURVIVAL_PREFERENCE="[region, zone, host]"`。 |

### CONSTRAINTS 格式

你可以使用以下任意一种格式配置 `CONSTRAINTS`、`FOLLOWER_CONSTRAINTS` 和 `LEARNER_CONSTRAINTS`：

| CONSTRAINTS 格式 | 描述 |
|----------------------------|-----------------------------------------------------------------------------------------------------------|
| 列表格式  | 如果某个约束适用于所有副本，可以使用键值对列表格式。每个键以 `+` 或 `-` 开头。例如：<br/><ul><li>`[+region=us-east-1]` 表示将数据放置在标签为 `region` 且值为 `us-east-1` 的节点上。</li><li>`[+region=us-east-1,-type=fault]` 表示将数据放置在标签为 `region` 且值为 `us-east-1`，但不具有 `type` 标签且值为 `fault` 的节点上。</li></ul><br/>  |
| 字典格式 | 如果需要为不同的约束指定不同的副本数，可以使用字典格式。例如：<br/><ul><li>`FOLLOWER_CONSTRAINTS="{+region=us-east-1: 1,+region=us-east-2: 1,+region=us-west-1: 1}";` 表示在 `us-east-1` 放置 1 个 Follower，在 `us-east-2` 放置 1 个 Follower，在 `us-west-1` 放置 1 个 Follower。</li><li>`FOLLOWER_CONSTRAINTS='{"+region=us-east-1,+type=scale-node": 1,"+region=us-west-1": 1}';` 表示在标签为 `region` 且值为 `us-east-1`，且标签为 `type` 且值为 `scale-node` 的节点上放置 1 个 Follower，在 `us-west-1` 放置 1 个 Follower。</li></ul>字典格式支持每个键以 `+` 或 `-` 开头，并允许配置特殊的 `#evict-leader` 属性。例如：`FOLLOWER_CONSTRAINTS='{"+region=us-east-1":1, "+region=us-east-2": 2, "+region=us-west-1,#evict-leader": 1}'` 表示在 `us-west-1` 选举出的 Leader 在灾难恢复时会尽可能被驱逐。

> **Note:**
>
> - `LEADER_CONSTRAINTS` 仅支持列表格式。
> - 列表和字典格式都基于 YAML 解析器，但在某些情况下可能会误解析 YAML 语法。例如，`"{+region=east:1,+region=west:2}"`（`:` 后无空格）可能会被误解析为 `'{"+region=east:1": null, "+region=west:2": null}'`，这不是预期的。相反，`"{+region=east: 1,+region=west: 2}"`（`:` 后有空格）可以正确解析为 `'{"+region=east": 1, "+region=west": 2}'`。因此，建议在 `:` 后添加空格。

## 基本示例

### 全局指定集群的副本数

集群初始化后，默认副本数为 `3`。如果需要更多副本，可以通过配置调度策略增加副本数，然后使用 [`ALTER RANGE`](/sql-statements/sql-statement-alter-range.md) 在集群层面应用。例如：

```sql
CREATE PLACEMENT POLICY five_replicas FOLLOWERS=4;
ALTER RANGE global PLACEMENT POLICY five_replicas;
```

注意，由于 TiDB 默认将 Leader 数量设为 `1`，`five replicas` 表示 `4` 个 Follower 和 `1` 个 Leader。

### 为数据库指定默认调度策略

你可以为数据库指定默认调度策略。这类似于为数据库设置默认字符集或排序规则。如果没有为数据库中的表或分区指定其他调度策略，则会应用数据库的调度策略。例如：

```sql
CREATE PLACEMENT POLICY p1 PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-east-2";  -- 创建调度策略

CREATE PLACEMENT POLICY p2 FOLLOWERS=4;

CREATE PLACEMENT POLICY p3 FOLLOWERS=2;

CREATE TABLE t1 (a INT);  -- 创建表 t1，未指定调度策略。

ALTER DATABASE test PLACEMENT POLICY=p2;  -- 将数据库的默认调度策略改为 p2，但不影响已存在的表 t1。

CREATE TABLE t2 (a INT);  -- 创建表 t2，调度策略 p2 会应用到 t2。

CREATE TABLE t3 (a INT) PLACEMENT POLICY=p1;  -- 创建表 t3，指定了其他调度规则，默认调度策略 p2 不会应用到 t3。

ALTER DATABASE test PLACEMENT POLICY=p3;  -- 再次更改数据库的默认策略，不影响已存在的表。

CREATE TABLE t4 (a INT);  -- 创建表 t4，调度策略 p3 会应用到 t4。

ALTER PLACEMENT POLICY p3 FOLLOWERS=3; -- `FOLLOWERS=3` 会应用到附加策略为 p3 的表（即 t4）。
```

注意，从表到其分区的策略继承不同于前例中的继承方式。当你更改表的默认策略时，新的策略也会应用到该表的分区中。但只有在创建表时未指定任何策略时，表才会继承数据库的策略。一旦表继承了数据库的策略，修改数据库的默认策略不会影响该表。

### 为表指定调度策略

你可以为表指定默认调度策略。例如：

```sql
CREATE PLACEMENT POLICY five_replicas FOLLOWERS=4;

CREATE TABLE t (a INT) PLACEMENT POLICY=five_replicas;  -- 创建表 t 并附加 `five_replicas` 调度策略。

ALTER TABLE t PLACEMENT POLICY=default; -- 移除表 t 上的调度策略 `five_replicas`，恢复为默认策略。
```

### 为分区表指定调度策略

你也可以为分区表或分区指定调度策略。例如：

```sql
CREATE PLACEMENT POLICY storageforhistorydata CONSTRAINTS="[+node=history]";
CREATE PLACEMENT POLICY storagefornewdata CONSTRAINTS="[+node=new]";
CREATE PLACEMENT POLICY companystandardpolicy CONSTRAINTS="";

CREATE TABLE t1 (id INT, name VARCHAR(50), purchased DATE, UNIQUE INDEX idx(id) GLOBAL)
PLACEMENT POLICY=companystandardpolicy
PARTITION BY RANGE( YEAR(purchased) ) (
  PARTITION p0 VALUES LESS THAN (2000) PLACEMENT POLICY=storageforhistorydata,
  PARTITION p1 VALUES LESS THAN (2005),
  PARTITION p2 VALUES LESS THAN (2010),
  PARTITION p3 VALUES LESS THAN (2015),
  PARTITION p4 VALUES LESS THAN MAXVALUE PLACEMENT POLICY=storagefornewdata
);
```

如果没有为分区指定调度策略，分区会尝试继承表的策略（如果有的话）。如果表有 [global index](/partitioned-table.md#global-indexes)，索引会应用与表相同的调度策略。在上述示例中：

- `p0` 分区会应用 `storageforhistorydata` 策略。
- `p4` 分区会应用 `storagefornewdata` 策略。
- `p1`、`p2` 和 `p3` 分区会应用从表 `t1` 继承的 `companystandardpolicy` 策略。
- 全局索引 `idx` 会应用与表 `t1` 相同的 `companystandardpolicy` 策略。
- 如果没有为表 `t1` 指定调度策略，则 `p1`、`p2`、`p3` 分区和索引 `idx` 会继承数据库的默认策略或全局默认策略。

在这些分区附加调度策略后，你可以像下面这样为某个分区单独更改调度策略：

```sql
ALTER TABLE t1 PARTITION p1 PLACEMENT POLICY=storageforhistorydata;
```

## 高可用性示例

假设存在如下拓扑的集群，其中 TiKV 节点分布在 3 个区域，每个区域包含 3 个可用区：

```sql
SELECT store_id,address,label from INFORMATION_SCHEMA.TIKV_STORE_STATUS;
+----------+-----------------+--------------------------------------------------------------------------------------------------------------------------+
| store_id | address         | label                                                                                                                    |
+----------+-----------------+--------------------------------------------------------------------------------------------------------------------------+
|        1 | 127.0.0.1:20163 | [{"key": "region", "value": "us-east-1"}, {"key": "zone", "value": "us-east-1a"}, {"key": "host", "value": "host1"}]     |
|        2 | 127.0.0.1:20162 | [{"key": "region", "value": "us-east-1"}, {"key": "zone", "value": "us-east-1b"}, {"key": "host", "value": "host2"}]     |
|        3 | 127.0.0.1:20164 | [{"key": "region", "value": "us-east-1"}, {"key": "zone", "value": "us-east-1c"}, {"key": "host", "value": "host3"}]     |
|        4 | 127.0.0.1:20160 | [{"key": "region", "value": "us-east-2"}, {"key": "zone", "value": "us-east-2a"}, {"key": "host", "value": "host4"}]     |
|        5 | 127.0.0.1:20161 | [{"key": "region", "value": "us-east-2"}, {"key": "zone", "value": "us-east-2b"}, {"key": "host", "value": "host5"}]     |
|        6 | 127.0.0.1:20165 | [{"key": "region", "value": "us-east-2"}, {"key": "zone", "value": "us-east-2c"}, {"key": "host", "value": "host6"}]     |
|        7 | 127.0.0.1:20166 | [{"key": "region", "value": "us-west-1"}, {"key": "zone", "value": "us-west-1a"}, {"key": "host", "value": "host7"}]     |
|        8 | 127.0.0.1:20167 | [{"key": "region", "value": "us-west-1"}, {"key": "zone", "value": "us-west-1b"}, {"key": "host", "value": "host8"}]     |
|        9 | 127.0.0.1:20168 | [{"key": "region", "value": "us-west-1"}, {"key": "zone", "value": "us-west-1c"}, {"key": "host", "value": "host9"}]     |
+----------+-----------------+--------------------------------------------------------------------------------------------------------------------------+

```

### 指定存活偏好

如果你不特别关心数据的具体分布，而更重视满足灾难恢复需求，可以使用 `SURVIVAL_PREFERENCES` 选项指定数据存活偏好。

如前例所示，集群分布在 3 个区域，每个区域包含 3 个可用区。当为此集群创建调度策略时，假设配置如下：

``` sql
CREATE PLACEMENT POLICY multiaz SURVIVAL_PREFERENCES="[region, zone, host]";
CREATE PLACEMENT POLICY singleaz CONSTRAINTS="[+region=us-east-1]" SURVIVAL_PREFERENCES="[zone]";
```

创建调度策略后，可以根据需要将其附加到对应的表：

- 附加 `multiaz` 策略的表，数据会在不同区域的 3 个副本中存放，优先满足跨区域存活目标，其次是跨区存活目标，最后是跨主机存活目标。
- 附加 `singleaz` 策略的表，数据会在 `us-east-1` 区域的 3 个副本中存放，优先满足跨区存活目标。

<CustomContent platform="tidb">

> **Note:**
>
> `SURVIVAL_PREFERENCES` 等同于 PD 中的 `location-labels`。更多信息，见 [Schedule Replicas by Topology Labels](/schedule-replicas-by-topology-labels.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> `SURVIVAL_PREFERENCES` 等同于 PD 中的 `location-labels`。更多信息，见 [Schedule Replicas by Topology Labels](https://docs.pingcap.com/tidb/stable/schedule-replicas-by-topology-labels)。

</CustomContent>

### 指定多个数据中心的 5 副本分布（2:2:1）

如果你需要特定的数据分布，例如 2:2:1 的 5 副本分布，可以在 [字典格式](#constraints-formats)中为不同的约束配置不同的副本数：

```sql
CREATE PLACEMENT POLICY `deploy221` CONSTRAINTS='{"+region=us-east-1":2, "+region=us-east-2": 2, "+region=us-west-1": 1}';

ALTER RANGE global PLACEMENT POLICY = "deploy221";

SHOW PLACEMENT;
+-------------------+---------------------------------------------------------------------------------------------+------------------+
| Target            | Placement                                                                                   | Scheduling_State |
+-------------------+---------------------------------------------------------------------------------------------+------------------+
| POLICY deploy221  | CONSTRAINTS="{\"+region=us-east-1\":2, \"+region=us-east-2\": 2, \"+region=us-west-1\": 1}" | NULL             |
| RANGE TiDB_GLOBAL | CONSTRAINTS="{\"+region=us-east-1\":2, \"+region=us-east-2\": 2, \"+region=us-west-1\": 1}" | SCHEDULED        |
+-------------------+---------------------------------------------------------------------------------------------+------------------+
```

设置集群的全局调度策略后，TiDB 会根据此策略分布数据：在 `us-east-1` 放置 2 个副本，在 `us-east-2` 放置 2 个副本，在 `us-west-1` 放置 1 个副本。

### 指定 Leader 和 Follower 的分布

你可以使用约束或 `PRIMARY_REGION` 指定 Leader 和 Follower 的具体分布。

#### 使用约束

如果你对 Raft Leader 在节点间的分布有特殊要求，可以使用如下语句配置调度策略：

```sql
CREATE PLACEMENT POLICY deploy221_primary_east1 LEADER_CONSTRAINTS="[+region=us-east-1]" FOLLOWER_CONSTRAINTS='{"+region=us-east-1": 1, "+region=us-east-2": 2, "+region=us-west-1": 1}';
```

创建后，将数据的 Raft Leader 副本放置在 `LEADER_CONSTRAINTS` 指定的 `us-east-1` 区域，其他副本放置在 `FOLLOWER_CONSTRAINTS` 指定的区域。注意：如果集群发生故障（如 `us-east-1` 区域的节点宕机），仍会从其他区域选举 Leader，优先保证服务可用性。

在 `us-east-1` 区域发生故障时，如果不希望在 `us-west-1` 放置新 Leader，可以配置特殊的 `evict-leader` 属性，将新选举出的 Leader 驱逐出该区域：

```sql
CREATE PLACEMENT POLICY deploy221_primary_east1 LEADER_CONSTRAINTS="[+region=us-east-1]" FOLLOWER_CONSTRAINTS='{"+region=us-east-1": 1, "+region=us-east-2": 2, "+region=us-west-1,#evict-leader": 1}';
```

#### 使用 `PRIMARY_REGION`

如果你的集群拓扑中配置了 `region` 标签，也可以使用 `PRIMARY_REGION` 和 `REGIONS` 选项指定 Follower 的调度策略：

```sql
CREATE PLACEMENT POLICY eastandwest PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-east-2,us-west-1" SCHEDULE="MAJORITY_IN_PRIMARY" FOLLOWERS=4;
CREATE TABLE t1 (a INT) PLACEMENT POLICY=eastandwest;
```

- `PRIMARY_REGION` 指定 Leader 的分布区域。此选项只能指定一个区域。
- `SCHEDULE` 选项定义 TiDB 如何平衡 Follower 的分布。
  - 默认的 `EVEN` 调度规则确保 Follower 在所有区域均衡分布。
  - 若希望在 `PRIMARY_REGION`（即 `us-east-1`）中放置足够数量的 Follower 副本，可以使用 `MAJORITY_IN_PRIMARY` 调度规则。此规则在提供较低延迟的同时，牺牲部分可用性。若主区域失效，`MAJORITY_IN_PRIMARY` 不会自动故障转移。

## 数据隔离示例

在创建调度策略时，你可以为每个策略配置约束，要求数据放置在具有特定 `app` 标签的 TiKV 节点上。

```sql
CREATE PLACEMENT POLICY app_order CONSTRAINTS="[+app=order]";
CREATE PLACEMENT POLICY app_list CONSTRAINTS="[+app=list_collection]";
CREATE TABLE order (id INT, name VARCHAR(50), purchased DATE)
PLACEMENT POLICY=app_order
CREATE TABLE list (id INT, name VARCHAR(50), purchased DATE)
PLACEMENT POLICY=app_list
```

在此示例中，约束使用列表格式，如 `[+app=order]`。也可以使用字典格式，如 `{+app=order: 3}`。

执行上述语句后，TiDB 会将 `app_order` 数据放置在标签为 `app=order` 的 TiKV 节点上，将 `app_list` 数据放置在标签为 `app=list_collection` 的节点上，从而实现存储层面的物理数据隔离。

## 兼容性

## 与其他功能的兼容性

- 临时表不支持调度策略。
- 调度策略仅确保静态存储的数据在正确的 TiKV 节点上，但不能保证数据在传输过程中（无论是用户查询还是内部操作）只发生在特定区域。
- 若要为数据配置 TiFlash 副本，需 [创建 TiFlash 副本](/tiflash/create-tiflash-replicas.md)，而非使用调度策略。
- 允许为 `PRIMARY_REGION` 和 `REGIONS` 设置语法糖规则。未来计划增加 `PRIMARY_RACK`、`PRIMARY_ZONE` 和 `PRIMARY_HOST` 的变体。详见 [issue #18030](https://github.com/pingcap/tidb/issues/18030)。

## 与工具的兼容性

<CustomContent platform="tidb">

| Tool Name | Minimum supported version | Description |
| --- | --- | --- |
| Backup & Restore (BR) | 6.0 | 6.0 之前版本的 BR 不支持备份和还原调度策略。更多信息，见 [Why does an error occur when I restore placement rules to a cluster](/faq/backup-and-restore-faq.md#why-does-an-error-occur-when-i-restore-placement-rules-to-a-cluster)。 |
| TiDB Lightning | Not compatible yet | 导入包含调度策略的备份数据时，TiDB Lightning 会报错  |
| TiCDC | 6.0 | 忽略调度策略，不会将策略复制到下游 |

</CustomContent>

<CustomContent platform="tidb-cloud">

| Tool Name | Minimum supported version | Description |
| --- | --- | --- |
| TiDB Lightning | Not compatible yet | 导入包含调度策略的备份数据时，TiDB Lightning 会报错  |
| TiCDC | 6.0 | 忽略调度策略，不会将策略复制到下游 |

</CustomContent>