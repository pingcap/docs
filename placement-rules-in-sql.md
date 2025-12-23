---
title: SQL 中的放置规则
summary: 了解如何使用 SQL 语句调度表和分区的放置位置。
---

# SQL 中的放置规则

SQL 中的放置规则是一项功能，允许你通过 SQL 语句指定数据在 TiKV 集群中的存储位置。通过该功能，你可以将集群、数据库、表或分区的数据调度到特定的 region、数据中心、机架或主机。

该功能可以满足以下使用场景：

- 跨多个数据中心部署数据，并配置规则以优化高可用策略。
- 合并来自不同应用的多个数据库，并物理隔离不同用户的数据，满足同一实例下不同用户的隔离需求。
- 为重要数据增加副本数量，提高应用可用性和数据可靠性。

> **注意：**
>
> 该功能不适用于 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群。

## 概述

通过 SQL 中的放置规则功能，你可以[创建放置策略](#创建并绑定放置策略)，并为不同级别的数据配置所需的放置策略，粒度从粗到细如下：

| 级别            | 描述                                                                          |
|------------------|--------------------------------------------------------------------------------------|
| 集群          | 默认情况下，TiDB 为集群配置 3 个副本的策略。你可以为集群配置全局放置策略。详见 [为集群全局指定副本数](#为集群全局指定副本数)。 |
| 数据库         | 你可以为特定数据库配置放置策略。详见 [为数据库指定默认放置策略](#为数据库指定默认放置策略)。 |
| 表            | 你可以为特定表配置放置策略。详见 [为表指定放置策略](#为表指定放置策略)。 |
| 分区        | 你可以为表中的不同行创建分区，并分别为分区配置放置策略。详见 [为分区表指定放置策略](#为分区表指定放置策略)。 |

> **提示：**
>
> *SQL 中的放置规则* 的实现依赖于 PD 的 *placement rules feature*。详情参见 [配置放置规则](https://docs.pingcap.com/tidb/stable/configure-placement-rules)。在 SQL 中的放置规则上下文中，*placement rules* 可能指的是附加到其他对象的 *placement policies*，也可能指的是 TiDB 发送到 PD 的规则。

## 限制

- 为简化维护，建议每个集群内的放置策略数量限制在 10 个以内。
- 建议附加放置策略的表和分区总数限制在 10,000 个以内。为过多的表和分区附加策略会增加 PD 的计算负载，从而影响服务性能。
- 建议按照本文档提供的示例使用 SQL 中的放置规则功能，而不是使用其他复杂的放置策略。

## 前提条件

放置策略依赖于 TiKV 节点上的 label 配置。例如，`PRIMARY_REGION` 放置选项依赖于 TiKV 中的 `region` label。

<CustomContent platform="tidb">

当你创建放置策略时，TiDB 不会检查策略中指定的 label 是否存在，而是在你绑定策略时进行检查。因此，在绑定放置策略前，请确保每个 TiKV 节点都已正确配置 label。TiDB 自建集群的配置方法如下：

```
tikv-server --labels region=<region>,zone=<zone>,host=<host>
```

详细配置方法请参见以下示例：

| 部署方法 | 示例 |
| --- | --- |
| 手动部署 | [通过拓扑 label 调度副本](/schedule-replicas-by-topology-labels.md) |
| 使用 TiUP 部署 | [跨地域部署拓扑](/geo-distributed-deployment-topology.md) |
| 使用 TiDB Operator 部署 | [在 Kubernetes 中配置 TiDB 集群](https://docs.pingcap.com/tidb-in-kubernetes/stable/configure-a-tidb-cluster#high-availability-of-data) |

> **注意：**
>
> 对于 TiDB Cloud Dedicated 集群，可以跳过这些 label 配置步骤，因为 TiDB Cloud Dedicated 集群中的 TiKV 节点 label 会自动配置。

</CustomContent>

<CustomContent platform="tidb-cloud">

对于 TiDB Cloud Dedicated 集群，TiKV 节点上的 label 会自动配置。

</CustomContent>

要查看当前 TiKV 集群中所有可用的 label，可以使用 [`SHOW PLACEMENT LABELS`](/sql-statements/sql-statement-show-placement-labels.md) 语句：

```sql
SHOW PLACEMENT LABELS;
+--------+----------------------------+
| Key    | Values                     |
+--------+----------------------------+
| disk   | ["ssd"]                    |
| region | ["us-east-1", "us-west-1"] |
| zone   | ["us-east-1a"]             |
+--------+----------------------------+
3 rows in set (0.00 sec)
```

## 使用方法

本节介绍如何通过 SQL 语句创建、绑定、查看、修改和删除放置策略。

### 创建并绑定放置策略

1. 要创建放置策略，使用 [`CREATE PLACEMENT POLICY`](/sql-statements/sql-statement-create-placement-policy.md) 语句：

    ```sql
    CREATE PLACEMENT POLICY myplacementpolicy PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1";
    ```

    在该语句中：

    - `PRIMARY_REGION="us-east-1"` 选项表示将 Raft Leader 放置在 `region` label 为 `us-east-1` 的节点上。
    - `REGIONS="us-east-1,us-west-1"` 选项表示将 Raft Follower 放置在 `region` label 为 `us-east-1` 和 `us-west-1` 的节点上。

    更多可配置的放置选项及其含义，参见 [放置选项参考](#放置选项参考)。

2. 要将放置策略绑定到表或分区表，使用 `CREATE TABLE` 或 `ALTER TABLE` 语句为该表或分区表指定放置策略：

    ```sql
    CREATE TABLE t1 (a INT) PLACEMENT POLICY=myplacementpolicy;
    CREATE TABLE t2 (a INT);
    ALTER TABLE t2 PLACEMENT POLICY=myplacementpolicy;
    ```

   `PLACEMENT POLICY` 不属于任何数据库 schema，可以在全局作用域内绑定。因此，使用 `CREATE TABLE` 指定放置策略不需要额外的权限。

### 查看放置策略

- 要查看已存在的放置策略，可以使用 [`SHOW CREATE PLACEMENT POLICY`](/sql-statements/sql-statement-show-create-placement-policy.md) 语句：

    ```sql
    SHOW CREATE PLACEMENT POLICY myplacementpolicy\G
    *************************** 1. row ***************************
           Policy: myplacementpolicy
    Create Policy: CREATE PLACEMENT POLICY myplacementpolicy PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1"
    1 row in set (0.00 sec)
    ```

- 要查看某个表绑定的放置策略，可以使用 [`SHOW CREATE TABLE`](/sql-statements/sql-statement-show-create-table.md) 语句：

    ```sql
    SHOW CREATE TABLE t1\G
    *************************** 1. row ***************************
           Table: t1
    Create Table: CREATE TABLE `t1` (
      `a` int DEFAULT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin /*T![placement] PLACEMENT POLICY=`myplacementpolicy` */
    1 row in set (0.00 sec)
    ```

- 要查看集群中放置策略的定义，可以查询 [`INFORMATION_SCHEMA.PLACEMENT_POLICIES`](/information-schema/information-schema-placement-policies.md) 系统表：

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

- 要查看集群中所有已绑定放置策略的表，可以查询 `information_schema.tables` 系统表的 `tidb_placement_policy_name` 列：

    ```sql
    SELECT * FROM information_schema.tables WHERE tidb_placement_policy_name IS NOT NULL;
    ```

- 要查看集群中所有已绑定放置策略的分区，可以查询 `information_schema.partitions` 系统表的 `tidb_placement_policy_name` 列：

    ```sql
    SELECT * FROM information_schema.partitions WHERE tidb_placement_policy_name IS NOT NULL;
    ```

- 所有对象绑定的放置策略都是*异步*生效的。要检查放置策略的调度进度，可以使用 [`SHOW PLACEMENT`](/sql-statements/sql-statement-show-placement.md) 语句：

    ```sql
    SHOW PLACEMENT;
    ```

### 修改放置策略

要修改放置策略，可以使用 [`ALTER PLACEMENT POLICY`](/sql-statements/sql-statement-alter-placement-policy.md) 语句。该修改会应用到所有绑定了该策略的对象。

```sql
ALTER PLACEMENT POLICY myplacementpolicy FOLLOWERS=4;
```

在该语句中，`FOLLOWERS=4` 选项表示为数据配置 5 个副本（4 个 Follower 和 1 个 Leader）。更多可配置的放置选项及其含义，参见 [放置选项参考](#放置选项参考)。

### 删除放置策略

要删除未绑定到任何表或分区的策略，可以使用 [`DROP PLACEMENT POLICY`](/sql-statements/sql-statement-drop-placement-policy.md) 语句：

```sql
DROP PLACEMENT POLICY myplacementpolicy;
```

## 放置选项参考

在创建或修改放置策略时，你可以根据需要配置放置选项。

> **注意：**
>
> `PRIMARY_REGION`、`REGIONS` 和 `SCHEDULE` 选项不能与 `CONSTRAINTS` 选项同时指定，否则会报错。

### 常规放置选项

常规放置选项可以满足数据放置的基本需求。

| 选项名                | 描述                                                                                    |
|----------------------------|------------------------------------------------------------------------------------------------|
| `PRIMARY_REGION`           | 指定将 Raft Leader 放置在 `region` label 与该选项值匹配的节点上。     |
| `REGIONS`                  | 指定将 Raft Follower 放置在 `region` label 与该选项值匹配的节点上。 |
| `SCHEDULE`                 | 指定 Follower 放置的调度策略。可选值为 `EVEN`（默认）或 `MAJORITY_IN_PRIMARY`。 |
| `FOLLOWERS`                | 指定 Follower 的数量。例如，`FOLLOWERS=2` 表示数据有 3 个副本（2 个 Follower 和 1 个 Leader）。 |

### 高级放置选项

高级配置选项为数据放置提供了更高的灵活性，以满足复杂场景的需求。但配置高级选项比常规选项更复杂，需要你对集群拓扑结构和 TiDB 数据分片有深入了解。

| 选项名                | 描述                                                                                    |
| --------------| ------------ |
| `CONSTRAINTS`              | 适用于所有角色的约束列表。例如，`CONSTRAINTS="[+disk=ssd]"`。 |
| `LEADER_CONSTRAINTS`       | 仅适用于 Leader 的约束列表。                                      |
| `FOLLOWER_CONSTRAINTS`     | 仅适用于 Follower 的约束列表。                                   |
| `LEARNER_CONSTRAINTS`      | 仅适用于 learner 的约束列表。                                     |
| `LEARNERS`                 | learner 的数量。 |
| `SURVIVAL_PREFERENCE`      | 按 label 容灾级别指定副本放置优先级。例如，`SURVIVAL_PREFERENCE="[region, zone, host]"`。 |

### CONSTRAINTS 格式

你可以使用以下任一格式配置 `CONSTRAINTS`、`FOLLOWER_CONSTRAINTS` 和 `LEARNER_CONSTRAINTS` 放置选项：

| CONSTRAINTS 格式 | 描述 |
|----------------------------|-----------------------------------------------------------------------------------------------------------|
| 列表格式  | 如果要指定的约束适用于所有副本，可以使用键值列表格式。每个键以 `+` 或 `-` 开头。例如：<br/><ul><li>`[+region=us-east-1]` 表示将数据放置在 `region` label 为 `us-east-1` 的节点上。</li><li>`[+region=us-east-1,-type=fault]` 表示将数据放置在 `region` label 为 `us-east-1` 且 `type` label 不为 `fault` 的节点上。</li></ul><br/>  |
| 字典格式 | 如果需要为不同约束指定不同数量的副本，可以使用字典格式。例如：<br/><ul><li>`FOLLOWER_CONSTRAINTS="{+region=us-east-1: 1,+region=us-east-2: 1,+region=us-west-1: 1}";` 表示在 `us-east-1`、`us-east-2` 和 `us-west-1` 各放置一个 Follower。</li><li>`FOLLOWER_CONSTRAINTS='{"+region=us-east-1,+type=scale-node": 1,"+region=us-west-1": 1}';` 表示在 `us-east-1` 且 `type` label 为 `scale-node` 的节点上放置一个 Follower，在 `us-west-1` 放置一个 Follower。</li></ul>字典格式支持每个键以 `+` 或 `-` 开头，并允许你配置特殊的 `#evict-leader` 属性。例如，`FOLLOWER_CONSTRAINTS='{"+region=us-east-1":1, "+region=us-east-2": 2, "+region=us-west-1,#evict-leader": 1}'` 表示在灾难恢复期间，尽量驱逐 `us-west-1` 选举出的 Leader。|

> **注意：**
>
> - `LEADER_CONSTRAINTS` 放置选项仅支持列表格式。
> - 列表和字典格式都基于 YAML 解析器，但 YAML 语法在某些情况下可能被错误解析。例如，`"{+region=east:1,+region=west:2}"`（冒号后无空格）可能被错误解析为 `'{"+region=east:1": null, "+region=west:2": null}'`，这不是预期结果。而 `"{+region=east: 1,+region=west: 2}"`（冒号后有空格）可以被正确解析为 `'{"+region=east": 1, "+region=west": 2}'`。因此，建议在冒号后加一个空格。

## 基本示例

### 为集群全局指定副本数

集群初始化后，默认副本数为 `3`。如果集群需要更多副本，可以通过配置放置策略增加副本数，并使用 [`ALTER RANGE`](/sql-statements/sql-statement-alter-range.md) 在集群级别应用该策略。例如：

```sql
CREATE PLACEMENT POLICY five_replicas FOLLOWERS=4;
ALTER RANGE global PLACEMENT POLICY five_replicas;
```

注意，由于 TiDB 默认 Leader 数量为 `1`，`five replicas` 表示 4 个 Follower 和 1 个 Leader。

### 为数据库指定默认放置策略

你可以为数据库指定默认放置策略。这类似于为数据库设置默认字符集或排序规则。如果数据库中的表或分区未指定其他放置策略，则会应用数据库的放置策略。例如：

```sql
CREATE PLACEMENT POLICY p1 PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-east-2";  -- 创建放置策略

CREATE PLACEMENT POLICY p2 FOLLOWERS=4;

CREATE PLACEMENT POLICY p3 FOLLOWERS=2;

CREATE TABLE t1 (a INT);  -- 创建表 t1，未指定放置策略。

ALTER DATABASE test PLACEMENT POLICY=p2;  -- 将数据库的默认放置策略更改为 p2，不影响已存在的表 t1。

CREATE TABLE t2 (a INT);  -- 创建表 t2，默认放置策略 p2 应用于 t2。

CREATE TABLE t3 (a INT) PLACEMENT POLICY=p1;  -- 创建表 t3。由于该语句指定了其他放置规则，默认放置策略 p2 不会应用于 t3。

ALTER DATABASE test PLACEMENT POLICY=p3;  -- 再次更改数据库的默认策略，不影响已存在的表。

CREATE TABLE t4 (a INT);  -- 创建表 t4，默认放置策略 p3 应用于 t4。

ALTER PLACEMENT POLICY p3 FOLLOWERS=3; -- `FOLLOWERS=3` 应用于绑定了策略 p3 的表（即表 t4）。
```

注意，表到分区的策略继承与上述示例中的策略继承不同。当你更改表的默认策略时，新策略也会应用于该表中的分区。但表只有在创建时未指定任何策略时才会继承数据库的策略。一旦表继承了数据库的策略，修改数据库的默认策略不会影响该表。

### 为表指定放置策略

你可以为表指定默认放置策略。例如：

```sql
CREATE PLACEMENT POLICY five_replicas FOLLOWERS=4;

CREATE TABLE t (a INT) PLACEMENT POLICY=five_replicas;  -- 创建表 t，并绑定 'five_replicas' 放置策略。

ALTER TABLE t PLACEMENT POLICY=default; -- 从表 t 移除 'five_replicas' 放置策略，重置为默认放置策略。
```

### 为分区表指定放置策略

你也可以为分区表或分区指定放置策略。例如：

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

如果表中的分区未指定放置策略，则分区会尝试继承表（如有）的策略。如果表有 [全局索引](/global-indexes.md)，索引会应用与表相同的放置策略。在上述示例中：

- `p0` 分区会应用 `storageforhistorydata` 策略。
- `p4` 分区会应用 `storagefornewdata` 策略。
- `p1`、`p2` 和 `p3` 分区会继承表 `t1` 的 `companystandardpolicy` 放置策略。
- 全局索引 `idx` 会应用与表 `t1` 相同的 `companystandardpolicy` 放置策略。
- 如果表 `t1` 未指定放置策略，则 `p1`、`p2`、`p3` 分区和全局索引 `idx` 会继承数据库默认策略或全局默认策略。

为这些分区绑定放置策略后，你可以像下面这样更改某个分区的放置策略：

```sql
ALTER TABLE t1 PARTITION p1 PLACEMENT POLICY=storageforhistorydata;
```

## 高可用示例

假设有如下拓扑结构的集群，TiKV 节点分布在 3 个 region，每个 region 包含 3 个可用 zone：

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

### 指定生存优先级

如果你对数据的具体分布没有特殊要求，而更关注容灾需求，可以使用 `SURVIVAL_PREFERENCES` 选项指定数据生存优先级。

如上例，TiDB 集群分布在 3 个 region，每个 region 包含 3 个 zone。为该集群创建放置策略时，假设你配置 `SURVIVAL_PREFERENCES` 如下：

``` sql
CREATE PLACEMENT POLICY multiaz SURVIVAL_PREFERENCES="[region, zone, host]";
CREATE PLACEMENT POLICY singleaz CONSTRAINTS="[+region=us-east-1]" SURVIVAL_PREFERENCES="[zone]";
```

创建放置策略后，可以根据需要将其绑定到相应的表：

- 绑定了 `multiaz` 放置策略的表，数据会以 3 个副本分布在不同 region，优先满足跨 region 的数据隔离生存目标，其次是跨 zone，最后是跨主机。
- 绑定了 `singleaz` 放置策略的表，数据会优先以 3 个副本分布在 `us-east-1` region，然后满足跨 zone 的数据隔离生存目标。

<CustomContent platform="tidb">

> **注意：**
>
> `SURVIVAL_PREFERENCES` 等价于 PD 的 `location-labels`。详见 [通过拓扑 label 调度副本](/schedule-replicas-by-topology-labels.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注意：**
>
> `SURVIVAL_PREFERENCES` 等价于 PD 的 `location-labels`。详见 [通过拓扑 label 调度副本](https://docs.pingcap.com/tidb/stable/schedule-replicas-by-topology-labels)。

</CustomContent>

### 指定 5 副本按 2:2:1 分布在多个数据中心

如果你需要特定的数据分布，比如 5 副本按 2:2:1 分布，可以通过配置 [字典格式](#constraints-格式) 的 `CONSTRAINTS`，为不同约束指定不同数量的副本：

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

为集群设置全局 `deploy221` 放置策略后，TiDB 会按照该策略分布数据：在 `us-east-1` region 放置两个副本，在 `us-east-2` region 放置两个副本，在 `us-west-1` region 放置一个副本。

### 指定 Leader 和 Follower 的分布

你可以通过约束或 `PRIMARY_REGION` 指定 Leader 和 Follower 的具体分布。

#### 使用约束

如果你对 Raft Leader 在节点间的分布有特殊要求，可以使用如下语句指定放置策略：

```sql
CREATE PLACEMENT POLICY deploy221_primary_east1 LEADER_CONSTRAINTS="[+region=us-east-1]" FOLLOWER_CONSTRAINTS='{"+region=us-east-1": 1, "+region=us-east-2": 2, "+region=us-west-1": 1}';
```

创建并绑定该放置策略后，数据的 Raft Leader 副本会放置在 `LEADER_CONSTRAINTS` 选项指定的 `us-east-1` region，其他副本会放置在 `FOLLOWER_CONSTRAINTS` 选项指定的 region。注意，如果集群发生故障，比如 `us-east-1` region 节点宕机，新的 Leader 仍会从其他 region 选举产生，即使这些 region 被指定为 `FOLLOWER_CONSTRAINTS`。也就是说，保证服务可用性优先级最高。

如果在 `us-east-1` region 故障时，不希望在 `us-west-1` 选举新的 Leader，可以配置特殊的 `evict-leader` 属性，驱逐该 region 的新 Leader：

```sql
CREATE PLACEMENT POLICY deploy221_primary_east1 LEADER_CONSTRAINTS="[+region=us-east-1]" FOLLOWER_CONSTRAINTS='{"+region=us-east-1": 1, "+region=us-east-2": 2, "+region=us-west-1,#evict-leader": 1}';
```

#### 使用 `PRIMARY_REGION`

如果你的集群拓扑已配置 `region` label，也可以通过 `PRIMARY_REGION` 和 `REGIONS` 选项为 Follower 指定放置策略：

```sql
CREATE PLACEMENT POLICY eastandwest PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-east-2,us-west-1" SCHEDULE="MAJORITY_IN_PRIMARY" FOLLOWERS=4;
CREATE TABLE t1 (a INT) PLACEMENT POLICY=eastandwest;
```

- `PRIMARY_REGION` 指定 Leader 的分布 region。该选项只能指定一个 region。
- `SCHEDULE` 选项指定 TiDB 如何平衡 Follower 的分布。
    - 默认的 `EVEN` 调度规则保证 Follower 在所有 region 均衡分布。
    - 如果希望保证足够数量的 Follower 副本放置在 `PRIMARY_REGION`（即 `us-east-1`），可以使用 `MAJORITY_IN_PRIMARY` 调度规则。该规则以牺牲部分可用性为代价，提供更低延时的事务。如果主 region 故障，`MAJORITY_IN_PRIMARY` 不会自动切换。

## 数据隔离示例

如下例所示，在创建放置策略时，可以为每个策略配置一个约束，要求数据放置在带有指定 `app` label 的 TiKV 节点上。

```sql
CREATE PLACEMENT POLICY app_order CONSTRAINTS="[+app=order]";
CREATE PLACEMENT POLICY app_list CONSTRAINTS="[+app=list_collection]";
CREATE TABLE order (id INT, name VARCHAR(50), purchased DATE)
PLACEMENT POLICY=app_order
CREATE TABLE list (id INT, name VARCHAR(50), purchased DATE)
PLACEMENT POLICY=app_list
```

在该示例中，约束使用列表格式指定，如 `[+app=order]`。你也可以使用字典格式指定，如 `{+app=order: 3}`。

执行上述语句后，TiDB 会将 `app_order` 数据放置在 `app` label 为 `order` 的 TiKV 节点上，将 `app_list` 数据放置在 `app` label 为 `list_collection` 的 TiKV 节点上，从而实现存储层面的物理数据隔离。

## 兼容性

## 与其他功能的兼容性

- 临时表不支持放置策略。
- 放置策略只保证静态数据存储在正确的 TiKV 节点上，但不保证数据在传输过程中（无论是用户查询还是内部操作）只发生在特定 region。
- 若要为数据配置 TiFlash 副本，需要[创建 TiFlash 副本](/tiflash/create-tiflash-replicas.md)，而不是使用放置策略。
- 允许为 `PRIMARY_REGION` 和 `REGIONS` 设置语法糖规则。未来计划增加 `PRIMARY_RACK`、`PRIMARY_ZONE` 和 `PRIMARY_HOST` 等变体。参见 [issue #18030](https://github.com/pingcap/tidb/issues/18030)。

## 与工具的兼容性

<CustomContent platform="tidb">

| 工具名称 | 最低支持版本 | 描述 |
| --- | --- | --- |
| 备份与恢复（BR） | 6.0 | v6.0 之前，BR 不支持备份和恢复放置策略。详见 [为什么恢复放置规则到集群时报错](/faq/backup-and-restore-faq.md#why-does-an-error-occur-when-i-restore-placement-rules-to-a-cluster)。 |
| TiDB Lightning | 暂不兼容 | TiDB Lightning 导入包含放置策略的备份数据时会报错  |
| TiCDC | 6.0 | 忽略放置策略，不会将策略同步到下游 |

</CustomContent>

<CustomContent platform="tidb-cloud">

| 工具名称 | 最低支持版本 | 描述 |
| --- | --- | --- |
| TiDB Lightning | 暂不兼容 | TiDB Lightning 导入包含放置策略的备份数据时会报错  |
| TiCDC | 6.0 | 忽略放置策略，不会将策略同步到下游 |

</CustomContent>
