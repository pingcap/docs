---
title: TIKV_STORE_STATUS
summary: 了解 `TIKV_STORE_STATUS` INFORMATION_SCHEMA 表。
---

# TIKV_STORE_STATUS

`TIKV_STORE_STATUS` 表通过 PD 的 API 展示了 TiKV 节点的一些基本信息，比如在集群中分配的 ID、地址和端口，以及当前节点的状态、容量和 Region 领导者的数量。

> **Note:**
>
> 该表在 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群中不可用。

```sql
USE INFORMATION_SCHEMA;
DESC TIKV_STORE_STATUS;
```

输出结果如下：

```sql
+-------------------+-------------+------+------+---------+-------+
| Field             | Type        | Null | Key  | Default | Extra |
+-------------------+-------------+------+------+---------+-------+
| STORE_ID          | bigint(21)  | YES  |      | NULL    |       |
| ADDRESS           | varchar(64) | YES  |      | NULL    |       |
| STORE_STATE       | bigint(21)  | YES  |      | NULL    |       |
| STORE_STATE_NAME  | varchar(64) | YES  |      | NULL    |       |
| LABEL             | json        | YES  |      | NULL    |       |
| VERSION           | varchar(64) | YES  |      | NULL    |       |
| CAPACITY          | varchar(64) | YES  |      | NULL    |       |
| AVAILABLE         | varchar(64) | YES  |      | NULL    |       |
| LEADER_COUNT      | bigint(21)  | YES  |      | NULL    |       |
| LEADER_WEIGHT     | double      | YES  |      | NULL    |       |
| LEADER_SCORE      | double      | YES  |      | NULL    |       |
| LEADER_SIZE       | bigint(21)  | YES  |      | NULL    |       |
| REGION_COUNT      | bigint(21)  | YES  |      | NULL    |       |
| REGION_WEIGHT     | double      | YES  |      | NULL    |       |
| REGION_SCORE      | double      | YES  |      | NULL    |       |
| REGION_SIZE       | bigint(21)  | YES  |      | NULL    |       |
| START_TS          | datetime    | YES  |      | NULL    |       |
| LAST_HEARTBEAT_TS | datetime    | YES  |      | NULL    |       |
| UPTIME            | varchar(64) | YES  |      | NULL    |       |
+-------------------+-------------+------+------+---------+-------+
19 rows in set (0.00 sec)
```

`TIKV_STORE_STATUS` 表中各列的描述如下：

* `STORE_ID`: Store 的 ID。
* `ADDRESS`: Store 的地址。
* `STORE_STATE`: Store 状态的标识符，对应 `STORE_STATE_NAME`。
* `STORE_STATE_NAME`: Store 状态的名称。名称可能为 `Up`、`Offline` 或 `Tombstone`。
* `LABEL`: 设置在 Store 上的标签。
* `VERSION`: Store 的版本号。
* `CAPACITY`: Store 的存储容量。
* `AVAILABLE`: Store 的剩余存储空间。
* `LEADER_COUNT`: Store 上的领导者数量。
* `LEADER_WEIGHT`: Store 的领导者权重。
* `LEADER_SCORE`: Store 的领导者得分。
* `LEADER_SIZE`: Store 上所有领导者的近似总数据大小（MB）。
* `REGION_COUNT`: Store 上的 Region 数量。
* `REGION_WEIGHT`: Store 的 Region 权重。
* `REGION_SCORE`: Store 的 Region 得分。
* `REGION_SIZE`: Store 上所有 Region 的近似总数据大小（MB）。
* `START_TS`: Store 启动的时间戳。
* `LAST_HEARTBEAT_TS`: Store 发送的最后一次心跳的时间戳。
* `UPTIME`: Store 启动以来的总运行时间。