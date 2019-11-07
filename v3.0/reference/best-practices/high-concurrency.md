---
title: Best Practice for High Concurrent and Write Intensive Scenario
summary: Learn the best practice for high concurrent and write intensive scenario.
category: reference
---

# Best Practice for High Concurrent and Write Intensive Scenario

A typical scenario for TiDB users is to write data intensively to TiDB in high concurrent situations. This document explains the common problems encountered in this scenario and provides a best practice guide to facilitate user applications.

## Target reader

This document assumes that you have a basic understanding of TiDB. It is recommended that you first read the following three blog articles that explain TiDB fundamentals and [TiDB Best Practices](https://pingcap.com/blog/2017-07-24-tidbbestpractice/):

+ [Data Storage](https://pingcap.com/blog/2017-07-11-tidbinternal1/)
+ [Computing](https://pingcap.com/blog/2017-07-11-tidbinternal2/)
+ [Scheduling](https://pingcap.com/blog/2017-07-20-tidbinternal3/)

## High concurrent and write intensive scenario

The high concurrent and write intensive scenario often occurs in the batch task in applications such as liquidation, account settlement and so on. This scenario has the following features:

+ A Huge volume of data
+ The need to import historical data into database in a short time
+ The need to read a huge volume of data from database in a short time

These features pose these challenges to TiDB:

+ The write or read capacity must be linearly scalable.
+ Database performance is stable and does not decrease as a huge volume of data is written concurrently.

For a distributed database, it is crucial to fully leverage the capacity of all nodes and to prevent single node from becoming the bottleneck.

## How data is distributed in TiDB

To address the above challenges, it is necessary to start with the data segmentation and scheduling principle of TiDB. Refer to [Scheduling](https://pingcap.com/blog/2017-07-20-tidbinternal3/) for more details.

TiDB segments data into Regions, each representing a range of data with a size limit of 96M by default. Each Region has multiple replicas, and each group of replicas is called a Raft Group. In a Raft Group, the Region Leader executes the read and write tasks involving the data range. The Region Leader is automatically scheduled by the PD component to different physical nodes evenly to distribute the read and write pressure.

![TiDB Data Overview](/media/best-practices/tidb-data-overview.png)

Theoretically, by the virtue of this architecture, TiDB is able to linearly scale its read and write capacities and make full use of the distributed resources so long as there is no `AUTO_INCREMENT` primary key in the write scenario, or there is no monotonically increasing index. From this point of view, TiDB is especially suitable for the high concurrent and write intensive scenario.

> **Note:**
>
> No `AUTO_INCREMENT` primary key in the write scenario or no monotonically increasing index means no write hotspot in the application.

However, this theoretical assumption often differs from the actual situation. The following case explains how a hotspot is caused.

## Hotspot case

Take the table below as an example for the case:

```sql
CREATE TABLE IF NOT EXISTS TEST_HOTSPOT(
      id         BIGINT PRIMARY KEY,
      age        INT,
      user_name  VARCHAR(32),
      email      VARCHAR(128)
)
```

This table is simple in structure. Besides the primary key `id`, there is no secondary index. Execute the following statement to write data into this table. `id` is discretely generated as radom numbers.

{{< copyable "sql" >}}

```sql
INSERT INTO TEST_HOTSPOT(id, age, user_name, email) values(%v, %v, '%v', '%v');
```

The load comes from executing the above statement intensively in a short time.

Theoretically, the above operation seems to comply with the TiDB best practices, and there is no hotspot caused in the application. So long as there are enough machines, the distributed capacity of TiDB can be fully used. To verify whether it is truly in line with the best practices, a test is conducted, which is described as follows:

For the cluster topology, 2 TiDB nodes, 3 PD nodes and 6 TiKV nodes are deployed. Ignore the QPS performance, because this test is to clarify the principle rather than for benchmark.

![QPS1](/media/best-practices/QPS1.png)

The client starts "intensive" write requests in a short time which is 3K QPS received by TiDB. Theoretically, the load pressure is evenly distributed to 6 TiKV nodes. However, if you look at the CPU usage of each node, the load distribution are clearly lopsided. The `tikv-3` node is the write hotspot.

![QPS2](/media/best-practices/QPS2.png)

![QPS3](/media/best-practices/QPS3.png)：

[Raft store CPU](/v3.0/reference/key-monitoring-metrics/tikv-dashboard.md) is the CPU usage rate for the `raftstore` thread, usually representing the write load. In this scenario, `tikv-3` is the Leader of this Raft Group; `tikv-0` and `tikv-1` are the followers. The loads of other nodes are almost empty.

The monitoring record from PD also confirms that hotspot has been caused.

![QPS4](/media/best-practices/QPS4.png)

## Why hotspot is caused

In the above test, the operation does not reach the ideal performance expected in the best practices. This is because for each new table created in TiDB, only one Region is segmented by default to store the data of this table. The data range is:

```
[CommonPrefix + TableID, CommonPrefix + TableID + 1)
```

In a short period of time, a huge volume of data will be continuously written to the same Region.

![TiKV Region Split](/media/best-practices/tikv-Region-split.png)

The above image illustrates the Region split process. As data is continuously written into TiKV, TiKV splits a Region into multiple Regions. Because the leader election is started on the store where the Region Leader to be split is located, the two newly split Region Leaders is likely to stay on the same store. This split process might also happens to the newly split Region 2 and Region 3. In this way, write pressure will concentrate on TiKV-Node 1.

During the continuous write, after finding that hotspot is caused on Node 1, PD evenly distributes the concentrated Leaders to other nodes. If the number of TiKV nodes is more than the number of Region replicas, TiKV will try to migrate these Regions to idle nodes. These two actions during the write are also reflected in the PD's monitoring record:

![QPS5](/media/best-practices/QPS5.png)

After a period of continuous write, PD automatically schedules the entire TiKV cluster to a state where pressure is evenly distributed. By that time, the capacity of the whole cluster can be fully used.

In most situations, the above process of causing hotspot is normal, which is the warm-up phase of database. However, this phase should be avoided in the high concurrent and write intensive scenario.

## Avoid hotspot

To achieve the ideal performance expected in the theoretical scenario, one method is to skip the warm-up phase by directly splitting a Region into the desired number of Regions and scheduling these Regions in advance to other nodes in the cluster.

In v3.0.x and since v2.1.13, TiDB supports a new feature called [Split Region](/v3.0/reference/sql/statements/split-region.md). This new feature provides the following new syntaxes:

{{< copyable "sql" >}}

```sql
SPLIT TABLE table_name [INDEX index_name] BETWEEN (lower_value) AND (upper_value) REGIONS region_num
```

{{< copyable "sql" >}}

```sql
SPLIT TABLE table_name [INDEX index_name] BY (value_list) [, (value_list)]
```

However, TiDB does not automatically perform this pre-split operation. The reasons are related to the data distribution in TiDB as one of its feature:

![Table Region Range](/media/best-practices/table-Region-range.png)

As can be seen from Image 3, the key of the row data is so encoded that `rowID` is the only variable. In TiDB, `rowID` is an `Int64` integer. However, the user might not need to evenly split the `Int64` integer range to the desired number of ranges and then to distribute the ranges to different nodes, because Region split must also be based on the actual situation.

If the write of `rowID` is completely discrete, the above method will not cause hotspot. If the row ID or index has a fixed range or prefix (for example, discretely insert data into the range of `[2000w, 5000w)`), no hotspot will be caused either. However, if you split a Region using the above method, data might still be written to the same Region at the beginning.

TiDB is a database for general usage and does not make assumptions about the data distribution. So it segments only one Region at the beginning to store the data of a table and automatically splits the Region according to the data distribution after real data is inserted.

Given this feature and the need to avoid the hotspot problem, TiDB offers the `Split Region` syntaxes for optimizing the data write in the high concurrent and write intensive scenario. Based on the above case, now you can try to scatter Regions using the `Split Region` syntaxes and observe the load distribution.

Because the data to be written in the test is entirely discrete within the positive range, you can use the following statement to pre-split the table into 128 Regions within the range of `minInt64` and `maxInt64`:

{{< copyable "sql" >}}

```sql
SPLIT TABLE TEST_HOTSPOT BETWEEN (0) AND (9223372036854775807) REGIONS 128;
```

After the pre-split operation, execute the `SHOW TABLE test_hotspot REGIONS;` statement to check the status of Region scattering. If the values of the `SCATTERING` column are all `0`, the scheduling is successful.

You can also check the Region distribution using the [table-regions.py](https://github.com/pingcap/tidb-ansible/blob/dabf60baba5e740a4bee9faf95e77563d8084be1/scripts/table-regions.py) script. Currently, the Region distribution is relatively even:

```
[root@172.16.4.4 scripts]# python table-regions.py --host 172.16.4.3 --port 31453 test test_hotspot
[RECORD - test.test_hotspot] - Leaders Distribution:
  total leader count: 127
  store: 1, num_leaders: 21, percentage: 16.54%
  store: 4, num_leaders: 20, percentage: 15.75%
  store: 6, num_leaders: 21, percentage: 16.54%
  store: 46, num_leaders: 21, percentage: 16.54%
  store: 82, num_leaders: 23, percentage: 18.11%
  store: 62, num_leaders: 21, percentage: 16.54%
```

Then operate the write load again:

![QPS6](/media/best-practices/QPS6.png)

![QPS7](/media/best-practices/QPS7.png)

![QPS8](/media/best-practices/QPS8.png)

You can see that the hotspot has been eliminated now.

In this case, the table is simple. In other cases, you might also need to consider the hotspot problem of index. For more details on how to pre-split the index Region, refer to [Split Region](/v3.0/reference/sql/statements/split-region.md).

## More complex hotspot problem

If a table does not have a primary key, or the primary key is not the `Int` type and you do not want to generate a randomly distributed primary key ID, TiDB provides an implicit `_tidb_rowid` column as the row ID. If you do not use the `SHARD_ROW_ID_BITS` parameter, the values of the `_tidb_rowid` column might be monotonically increasing, which also causes hotspot. Refer to [`SHARD_ROW_ID_BITS` description](/v3.0/reference/configuration/tidb-server/tidb-specific-variables.md#shard_row_id_bits) for more detail.

To avoid the hotspot problem in this situation, you can use `SHARD_ROW_ID_BITS` and `PRE_SPLIT_REGIONS` when creating a table. For more details about `PRE_SPLIT_REGIONS`, refer to [here](/v3.0/reference/sql/statements/split-region.md#pre_split_regions).

`SHARD_ROW_ID_BITS` is used to randomly scatter the row ID generated in the `_tidb_rowid` column. `pre_split_regions` is used to pre-split the Region after a table is created.

> **Note:**
>
> The value of `pre_split_regions` must be smaller or equal to that of `shard_row_id_bits`.

Example:

{{< copyable "sql" >}}

```sql
create table t (a int, b int) shard_row_id_bits = 4 pre_split_regions=·3;
```

- `SHARD_ROW_ID_BITS = 4` means that the values of `tidb_rowid` will be randomly distributed into 16 (16=2^4) ranges.
- `pre_split_regions=3` means that the table will be pre-split into 8 (2^3) Regions after it is created.

When data starts to be written into table t, the data is written into the pre-split 8 Regions, which avoids the hotspot problem that might be caused if there is only one Region after the table creation.

## Parameter configuration

In v2.1, the [latch mechanism](/v3.0/reference/configuration/tidb-server/configuration-file.md#txn-local-latches) is introduced in TiDB to identify transaction conflicts in advance in scenarios where write conflicts frequently appear. The aim is to reduce the retry of transaction commits in TiDB and TiKV caused by write conflicts. Generally, batch tasks use the data already stored in TiDB, so the write conflicts of transaction do not exist. In this situation, you can disable the latch in TiDB to reduce memory allocation for small objects:

```
[txn-local-latches]
enabled = false
```
