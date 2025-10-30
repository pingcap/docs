---
title: CLUSTER_INFO
summary: 了解 `CLUSTER_INFO` 集群拓扑信息表。
---

# CLUSTER_INFO

`CLUSTER_INFO` 集群拓扑表提供了当前集群的拓扑信息、每个实例的版本信息、实例版本对应的 Git Hash、每个实例的启动时间以及每个实例的运行时间。

> **Note:**
>
> 该表在 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群中不可用。


```sql
USE information_schema;
desc cluster_info;
```

```sql
+----------------+-------------+------+------+---------+-------+
| Field          | Type        | Null | Key  | Default | Extra |
+----------------+-------------+------+------+---------+-------+
| TYPE           | varchar(64) | YES  |      | NULL    |       |
| INSTANCE       | varchar(64) | YES  |      | NULL    |       |
| STATUS_ADDRESS | varchar(64) | YES  |      | NULL    |       |
| VERSION        | varchar(64) | YES  |      | NULL    |       |
| GIT_HASH       | varchar(64) | YES  |      | NULL    |       |
| START_TIME     | varchar(32) | YES  |      | NULL    |       |
| UPTIME         | varchar(32) | YES  |      | NULL    |       |
| SERVER_ID      | bigint(21)  | YES  |      | NULL    |       |
+----------------+-------------+------+------+---------+-------+
8 rows in set (0.01 sec)
```

字段说明：

* `TYPE`：实例类型。可选值为 `tidb`、`pd` 和 `tikv`。
* `INSTANCE`：实例地址，格式为 `IP:PORT` 的字符串。
* `STATUS_ADDRESS`：HTTP API 的服务地址。tikv-ctl、pd-ctl 或 tidb-ctl 中的一些命令可能会使用该 API 及其地址。你也可以通过该地址获取更多集群信息。详细信息请参考 [TiDB HTTP API 文档](https://github.com/pingcap/tidb/blob/release-8.5/docs/tidb_http_api.md)。
* `VERSION`：对应实例的语义化版本号。为了兼容 MySQL 版本号，TiDB 版本以 `${mysql-version}-${tidb-version}` 的格式展示。
* `GIT_HASH`：编译该实例版本时的 Git Commit Hash，用于标识两个实例是否为绝对一致的版本。
* `START_TIME`：对应实例的启动时间。
* `UPTIME`：对应实例的运行时长。
* `SERVER_ID`：对应实例的 server ID。


```sql
SELECT * FROM cluster_info;
```

```sql
+------+-----------------+-----------------+--------------+------------------------------------------+---------------------------+---------------------+
| TYPE | INSTANCE        | STATUS_ADDRESS  | VERSION      | GIT_HASH                                 | START_TIME                | UPTIME              |
+------+-----------------+-----------------+--------------+------------------------------------------+---------------------------+---------------------+
| tidb | 0.0.0.0:4000    | 0.0.0.0:10080   | 4.0.0-beta.2 | 0df3b74f55f8f8fbde39bbd5d471783f49dc10f7 | 2020-07-05T09:25:53-06:00 | 26h39m4.352862693s  |
| pd   | 127.0.0.1:2379  | 127.0.0.1:2379  | 4.1.0-alpha  | 1ad59bcbf36d87082c79a1fffa3b0895234ac862 | 2020-07-05T09:25:47-06:00 | 26h39m10.352868103s |
| tikv | 127.0.0.1:20165 | 127.0.0.1:20180 | 4.1.0-alpha  | b45e052df8fb5d66aa8b3a77b5c992ddbfbb79df | 2020-07-05T09:25:50-06:00 | 26h39m7.352869963s  |
+------+-----------------+-----------------+--------------+------------------------------------------+---------------------------+---------------------+
3 rows in set (0.00 sec)
```