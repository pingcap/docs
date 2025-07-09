---
title: TIKV_REGION_STATUS
summary: 了解 `TIKV_REGION_STATUS` information_schema 表格。
---

# TIKV_REGION_STATUS

`TIKV_REGION_STATUS` 表格通过 PD 的 API 展示了 TiKV Region 的一些基本信息，如 Region ID、起始和结束键值，以及读写流量。

> **Note:**
>
> 该表在 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

```sql
USE INFORMATION_SCHEMA;
DESC TIKV_REGION_STATUS;
```

输出结果如下：

```sql
+---------------------------+-------------+------+------+---------+-------+
| Field                     | Type        | Null | Key  | Default | Extra |
+---------------------------+-------------+------+------+---------+-------+
| REGION_ID                 | bigint(21)  | YES  |      | NULL    |       |
| START_KEY                 | text        | YES  |      | NULL    |       |
| END_KEY                   | text        | YES  |      | NULL    |       |
| TABLE_ID                  | bigint(21)  | YES  |      | NULL    |       |
| DB_NAME                   | varchar(64) | YES  |      | NULL    |       |
| TABLE_NAME                | varchar(64) | YES  |      | NULL    |       |
| IS_INDEX                  | tinyint(1)  | NO   |      | 0       |       |
| INDEX_ID                  | bigint(21)  | YES  |      | NULL    |       |
| INDEX_NAME                | varchar(64) | YES  |      | NULL    |       |
| IS_PARTITION              | tinyint(1)  | NO   |      | 0       |       |
| PARTITION_ID              | bigint(21)  | YES  |      | NULL    |       |
| PARTITION_NAME            | varchar(64) | YES  |      | NULL    |       |
| EPOCH_CONF_VER            | bigint(21)  | YES  |      | NULL    |       |
| EPOCH_VERSION             | bigint(21)  | YES  |      | NULL    |       |
| WRITTEN_BYTES             | bigint(21)  | YES  |      | NULL    |       |
| READ_BYTES                | bigint(21)  | YES  |      | NULL    |       |
| APPROXIMATE_SIZE          | bigint(21)  | YES  |      | NULL    |       |
| APPROXIMATE_KEYS          | bigint(21)  | YES  |      | NULL    |       |
| REPLICATIONSTATUS_STATE   | varchar(64) | YES  |      | NULL    |       |
| REPLICATIONSTATUS_STATEID | bigint(21)  | YES  |      | NULL    |       |
+---------------------------+-------------+------+------+---------+-------+
20 rows in set (0.00 sec)
```

`TIKV_REGION_STATUS` 表中各列的描述如下：

* `REGION_ID`: Region 的 ID。
* `START_KEY`: Region 的起始键值。
* `END_KEY`: Region 的结束键值。
* `TABLE_ID`: 所属表的 ID。
* `DB_NAME`: 所属数据库的名称。
* `TABLE_NAME`: 所属表的名称。
* `IS_INDEX`: Region 数据是否为索引。0 表示不是索引，1 表示是索引。如果当前 Region 同时包含表数据和索引数据，则会有多行记录，`IS_INDEX` 分别为 0 和 1。
* `INDEX_ID`: 所属索引的 ID。如果 `IS_INDEX` 为 0，该列值为 NULL。
* `INDEX_NAME`: 所属索引的名称。如果 `IS_INDEX` 为 0，该列值为 NULL。
* `IS_PARTITION`: 所属表是否为分区表。
* `PARTITION_ID`: 如果所属表为分区表，则显示该 Region 所属分区的 ID。
* `PARTITION_NAME`: 如果所属表为分区表，则显示该 Region 所属分区的名称。
* `EPOCH_CONF_VER`: Region 配置的版本号。添加或删除副本时版本号会增加。
* `EPOCH_VERSION`: 当前 Region 的版本号。Region 分裂或合并时版本号会增加。
* `WRITTEN_BYTES`: 写入到该 Region 的数据量（字节数）。
* `READ_BYTES`: 从该 Region 读取的数据量（字节数）。
* `APPROXIMATE_SIZE`: 该 Region 的近似数据大小（MB）。
* `APPROXIMATE_KEYS`: 该 Region 的近似键数量。
* `REPLICATIONSTATUS_STATE`: 当前 Region 的复制状态。状态可能为 `UNKNOWN`、`SIMPLE_MAJORITY` 或 `INTEGRITY_OVER_LABEL`。
* `REPLICATIONSTATUS_STATEID`: 与 `REPLICATIONSTATUS_STATE` 对应的标识符。

此外，你可以通过在 pd-ctl 中对 `EPOCH_CONF_VER`、`WRITTEN_BYTES` 和 `READ_BYTES` 列使用 `ORDER BY X LIMIT Y` 操作，实现 `top confver`、`top read` 和 `top write` 的功能。

你可以使用以下 SQL 语句查询写入数据最多的前 3 个 Region：

```sql
SELECT * FROM tikv_region_status ORDER BY written_bytes DESC LIMIT 3;
```