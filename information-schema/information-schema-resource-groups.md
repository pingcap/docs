---
title: RESOURCE_GROUPS
summary: 了解 `RESOURCE_GROUPS` information_schema 表格。
---

# RESOURCE_GROUPS

`RESOURCE_GROUPS` 表显示所有资源组的相关信息。更多信息请参见 [Use Resource Control to Achieve Resource Isolation](/tidb-resource-control.md)。

> **Note:**
>
> 该表在 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

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
SELECT * FROM information_schema.resource_groups; -- 查看所有资源组。TiDB 默认有一个 `default` 资源组。
```

```sql
+---------+------------+----------+-----------+
| NAME    | RU_PER_SEC | PRIORITY | BURSTABLE |
+---------+------------+----------+-----------+
| default | UNLIMITED  | MEDIUM   | YES       |
+---------+------------+----------+-----------+
```

```sql
CREATE RESOURCE GROUP rg1 RU_PER_SEC=1000; -- 创建一个资源组 `rg1`
```

```sql
Query OK, 0 rows affected (0.34 sec)
```

```sql
SHOW CREATE RESOURCE GROUP rg1; -- 查看 `rg1` 资源组的定义
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

`RESOURCE_GROUPS` 表中各列的描述如下：

* `NAME`：资源组的名称。
* `RU_PER_SEC`：资源组的回填速度，单位为 RU/秒，其中 RU 表示 [Request Unit](/tidb-resource-control.md#what-is-request-unit-ru)。
* `PRIORITY`：在 TiKV 上待处理任务的绝对优先级。不同的资源根据 `PRIORITY` 设置进行调度。`PRIORITY` 高的任务会优先调度。对于具有相同 `PRIORITY` 的资源组，任务将根据 `RU_PER_SEC` 配置按比例调度。如果未指定 `PRIORITY`，则默认优先级为 `MEDIUM`。
* `BURSTABLE`：是否允许资源组超出系统可用资源的限制。

> **Note:**
>
> TiDB 在集群初始化时会自动创建一个 `default` 资源组。该资源组的 `RU_PER_SEC` 默认值为 `UNLIMITED`（等同于 `INT` 类型的最大值，即 `2147483647`），且处于 `BURSTABLE` 模式。所有未绑定到任何资源组的请求会自动绑定到此 `default` 资源组。当你为其他资源组创建新配置时，建议根据需要修改 `default` 资源组的配置。