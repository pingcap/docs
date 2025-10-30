---
title: RESOURCE_GROUPS
summary: 了解 `RESOURCE_GROUPS` information_schema 表。
---

# RESOURCE_GROUPS

`RESOURCE_GROUPS` 表展示了所有资源组的信息。更多信息，参见 [使用资源管控实现资源组限制与流控](/tidb-resource-control-ru-groups.md)。

> **Note:**
>
> 该表在 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群中不可用。

```sql
USE information_schema;
DESC resource_groups;
```

```sql
+------------+-------------+------+------+---------+-------+
| Field      | Type        | Null | Key  | Default | Extra |
+------------+-------------+------+------+---------+-------+
| NAME       | varchar(32) | NO   |      | NULL    |       |
| RU_PER_SEC | bigint(21)  | YES  |      | NULL    |       |
| PRIORITY   | varchar(6)  | YES  |      | NULL    |       |
| BURSTABLE  | varchar(3)  | YES  |      | NULL    |       |
+------------+-------------+------+------+---------+-------+
3 rows in set (0.00 sec)
```

## 示例

```sql
SELECT * FROM information_schema.resource_groups; -- 查看所有资源组。TiDB 有一个 `default` 资源组。
```

```sql
+---------+------------+----------+-----------+
| NAME    | RU_PER_SEC | PRIORITY | BURSTABLE |
+---------+------------+----------+-----------+
| default | UNLIMITED  | MEDIUM   | YES       |
+---------+------------+----------+-----------+
```

```sql
CREATE RESOURCE GROUP rg1 RU_PER_SEC=1000; -- 创建资源组 `rg1`
```

```sql
Query OK, 0 rows affected (0.34 sec)
```

```sql
SHOW CREATE RESOURCE GROUP rg1; -- 查看资源组 `rg1` 的定义
```

```sql
+----------------+---------------------------------------------------------------+
| Resource_Group | Create Resource Group                                         |
+----------------+---------------------------------------------------------------+
| rg1            | CREATE RESOURCE GROUP `rg1` RU_PER_SEC=1000 PRIORITY="MEDIUM" |
+----------------+---------------------------------------------------------------+
1 row in set (0.00 sec)
```

```sql
SELECT * FROM information_schema.resource_groups WHERE NAME = 'rg1'; -- 查看资源组 `rg1`
```

```sql
+------+------------+----------+-----------+-------------+
| NAME | RU_PER_SEC | PRIORITY | BURSTABLE | QUERY_LIMIT |
+------+------------+----------+-----------+-------------+
| rg1  | 1000       | MEDIUM   | NO        | NULL        |
+------+------------+----------+-----------+-------------+
1 row in set (0.00 sec)
```

`RESOURCE_GROUPS` 表中各列的说明如下：

* `NAME`：资源组的名称。
* `RU_PER_SEC`：资源组的回填速度，单位为 RU/秒，其中 RU 表示 [Request Unit](/tidb-resource-control-ru-groups.md#what-is-request-unit-ru)。
* `PRIORITY`：在 TiKV 上待处理任务的绝对优先级。不同资源会根据 `PRIORITY` 设置进行调度。`PRIORITY` 高的任务会优先被调度。对于相同 `PRIORITY` 的资源组，任务会根据 `RU_PER_SEC` 配置按比例调度。如果未指定 `PRIORITY`，则默认优先级为 `MEDIUM`。
* `BURSTABLE`：是否允许该资源组超额使用系统可用资源。

> **Note:**
>
> TiDB 在集群初始化时会自动创建一个 `default` 资源组。对于该资源组，`RU_PER_SEC` 的默认值为 `UNLIMITED`（等同于 `INT` 类型的最大值，即 `2147483647`），并且处于 `BURSTABLE` 模式。所有未绑定到任何资源组的请求会自动绑定到该 `default` 资源组。当你为其他资源组创建新配置时，建议根据需要修改 `default` 资源组的配置。