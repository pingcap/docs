---
title: TIDB_HOT_REGIONS_HISTORY
summary: 了解 `TIDB_HOT_REGIONS_HISTORY` information_schema 表。
---

# TIDB_HOT_REGIONS_HISTORY

`TIDB_HOT_REGIONS_HISTORY` 表提供了由 PD 本地定期记录的历史热点 Region 的相关信息。

> **Note:**
>
> 该表在 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群中不可用。

<CustomContent platform="tidb">

你可以通过配置 [`hot-regions-write-interval`](/pd-configuration-file.md#hot-regions-write-interval-new-in-v540) 来指定记录的时间间隔，默认值为 10 分钟。你可以通过配置 [`hot-regions-reserved-days`](/pd-configuration-file.md#hot-regions-reserved-days-new-in-v540) 来指定保留热点 Region 历史信息的天数，默认值为 7 天。详细信息请参见 [PD 配置文件说明](/pd-configuration-file.md#hot-regions-write-interval-new-in-v540)。

</CustomContent>

<CustomContent platform="tidb-cloud">

默认情况下，记录间隔为 10 分钟，热点 Region 历史信息的保留周期为 7 天。

</CustomContent>


```sql
USE information_schema;
DESC tidb_hot_regions_history;
```

```sql
+-------------+--------------+------+------+---------+-------+
| Field       | Type         | Null | Key  | Default | Extra |
+-------------+--------------+------+------+---------+-------+
| UPDATE_TIME | timestamp(6) | YES  |      | NULL    |       |
| DB_NAME     | varchar(64)  | YES  |      | NULL    |       |
| TABLE_NAME  | varchar(64)  | YES  |      | NULL    |       |
| TABLE_ID    | bigint(21)   | YES  |      | NULL    |       |
| INDEX_NAME  | varchar(64)  | YES  |      | NULL    |       |
| INDEX_ID    | bigint(21)   | YES  |      | NULL    |       |
| REGION_ID   | bigint(21)   | YES  |      | NULL    |       |
| STORE_ID    | bigint(21)   | YES  |      | NULL    |       |
| PEER_ID     | bigint(21)   | YES  |      | NULL    |       |
| IS_LEARNER  | tinyint(1)   | NO   |      | 0       |       |
| IS_LEADER   | tinyint(1)   | NO   |      | 0       |       |
| TYPE        | varchar(64)  | YES  |      | NULL    |       |
| HOT_DEGREE  | bigint(21)   | YES  |      | NULL    |       |
| FLOW_BYTES  | double       | YES  |      | NULL    |       |
| KEY_RATE    | double       | YES  |      | NULL    |       |
| QUERY_RATE  | double       | YES  |      | NULL    |       |
+-------------+--------------+------+------+---------+-------+
16 rows in set (0.00 sec)
```

`TIDB_HOT_REGIONS_HISTORY` 表中的字段说明如下：

* UPDATE_TIME：热点 Region 的更新时间。
* DB_NAME：热点 Region 所在对象的数据库名。
* TABLE_ID：热点 Region 所在表的 ID。
* TABLE_NAME：热点 Region 所在表的名称。
* INDEX_NAME：热点 Region 所在索引的名称。
* INDEX_ID：热点 Region 所在索引的 ID。
* REGION_ID：热点 Region 的 ID。
* STORE_ID：热点 Region 所在 store 的 ID。
* PEER_ID：热点 Region 对应的 Peer 的 ID。
* IS_LEARNER：该 PEER 是否为 LEARNER。
* IS_LEADER：该 PEER 是否为 LEADER。
* TYPE：热点 Region 的类型。
* HOT_DEGREE：热点 Region 的热度值。
* FLOW_BYTES：Region 内的读写字节数。
* KEY_RATE：Region 内的读写 key 数。
* QUERY_RATE：Region 内的读写查询数。

> **Note:**
>
> `UPDATE_TIME`、`REGION_ID`、`STORE_ID`、`PEER_ID`、`IS_LEARNER`、`IS_LEADER` 和 `TYPE` 字段会下推到 PD 服务器执行。为了减少使用该表的开销，你必须指定查询的时间范围，并尽可能多地指定查询条件。例如：`select * from tidb_hot_regions_history where store_id = 11 and update_time > '2020-05-18 20:40:00' and update_time < '2020-05-18 21:40:00' and type='write'`。

## 常见使用场景

* 查询指定时间段内的热点 Region。请将 `update_time` 替换为你的实际时间。

    
    ```sql
    SELECT * FROM INFORMATION_SCHEMA.TIDB_HOT_REGIONS_HISTORY WHERE update_time >'2021-08-18 21:40:00' and update_time <'2021-09-19 00:00:00';
    ```

    > **Note:**
    >
    > `UPDATE_TIME` 也支持 Unix 时间戳。例如，`update_time >TIMESTAMP('2021-08-18 21:40:00')` 或 `update_time > FROM_UNIXTIME(1629294000.000)`。

* 查询指定时间段内某张表的热点 Region。请将 `update_time` 和 `table_name` 替换为你的实际值。

    
    ```SQL
    SELECT * FROM INFORMATION_SCHEMA.TIDB_HOT_REGIONS_HISTORY WHERE update_time >'2021-08-18 21:40:00' and update_time <'2021-09-19 00:00:00' and TABLE_NAME = 'table_name';
    ```

* 查询指定时间段内热点 Region 的分布情况。请将 `update_time` 和 `table_name` 替换为你的实际值。

    
    ```sql
    SELECT count(region_id) cnt, store_id FROM INFORMATION_SCHEMA.TIDB_HOT_REGIONS_HISTORY WHERE update_time >'2021-08-18 21:40:00' and update_time <'2021-09-19 00:00:00' and table_name = 'table_name' GROUP BY STORE_ID ORDER BY cnt DESC;
    ```

* 查询指定时间段内热点 Leader Region 的分布情况。请将 `update_time` 和 `table_name` 替换为你的实际值。

    
    ```sql
    SELECT count(region_id) cnt, store_id FROM INFORMATION_SCHEMA.TIDB_HOT_REGIONS_HISTORY WHERE update_time >'2021-08-18 21:40:00' and update_time <'2021-09-19 00:00:00' and table_name = 'table_name' and is_leader=1 GROUP BY STORE_ID ORDER BY cnt DESC;
    ```

* 查询指定时间段内热点索引 Region 的分布情况。请将 `update_time` 和 `table_name` 替换为你的实际值。

    
    ```sql
    SELECT count(region_id) cnt, index_name, store_id FROM INFORMATION_SCHEMA.TIDB_HOT_REGIONS_HISTORY WHERE update_time >'2021-08-18 21:40:00' and update_time <'2021-09-19 00:00:00' and table_name = 'table_name' group by index_name, store_id order by index_name,cnt desc;
    ```

* 查询指定时间段内热点索引 Leader Region 的分布情况。请将 `update_time` 和 `table_name` 替换为你的实际值。

    
    ```sql
    SELECT count(region_id) cnt, index_name, store_id FROM INFORMATION_SCHEMA.TIDB_HOT_REGIONS_HISTORY WHERE update_time >'2021-08-18 21:40:00' and update_time <'2022-09-19 00:00:00' and table_name = 'table_name' and is_leader=1 group by index_name, store_id order by index_name,cnt desc;
    ```