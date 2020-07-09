---
title: Troubleshoot Hotspot Issues
summary: Learn how to locate and resolve read or write hotspot issues in TiDB.
category: troubleshoot
---

# Troubleshoot Hotspot Issues

This document describes how to locate and resolve the problem of read and write hotspots.

As a distributed database, TiDB has a load balancing mechanism to distribute the application loads as evenly as possible to different computing or storage nodes, to make better use of server resources.
However, in certain scenarios, some application loads cannot be well distributed, which can affect the performance and form a single point of high load, also known as a hotspot.

TiDB provides a complete solution to troubleshooting, resolving or avoiding hotspots. By balancing load hotspots, overall performance can be improved, including improving QPS and reducing latency.

## Common hotspots

This section describes TiDB encoding rules, table hotspots, and index hotspots.

### TiDB encoding rules

TiDB assigns a TableID to each table, an IndexID to each index, and a RowID to each row. By default, if the table uses an integer primary key, the value of the primary key is treated as the RowID. Among these IDs, TableID is unique in the entire cluster, while IndexID and RowID are unique in the table. The type of all these IDs is int64.

Each row of data is encoded as a key-value pair according to the following rule:

```
Key: tablePrefix{tableID}_recordPrefixSep{rowID}
Value: [col1, col2, col3, col4]
```

The `tablePrefix` and `recordPrefixSep` of the key are specific string constants, used to distinguish from other data in the KV space.

For Index data, the key-value pair is encoded according to the following rule:

```
Key: tablePrefix{tableID}_indexPrefixSep{indexID}_indexedColumnsValue
Value: rowID
```

Index data has two types: the unique index and the non-unique index.

- For unique indexes, you can follow the coding rules above. 
- For non-unique indexes, a unique key cannot be constructed through this encoding, because the `tablePrefix{tableID}_indexPrefixSep{indexID}` of the same index is the same and the `ColumnsValue` of multiple rows might be the same. The encoding rule for non-unique indexes is as follows:

    ```
    Key: tablePrefix{tableID}_indexPrefixSep{indexID}_indexedColumnsValue_rowID
    Value: null
    ```

### Table hotspots

According to TiDB coding rules, the data of the same table is in a range prefixed by the beginning of the TableID, and the data is arranged in the order of RowID values. When RowID values are incremented during table inserting, the inserted line can only be appended to the end. The Region will split after it reaches a certain size, and then it still can only be appended to the end of the range. The `INSERT` operation can only be executed on one Region, forming a hotspot.

The common auto-increment primary key is sequentially increasing. When the primary key is of the integer type, the value of the primary key is used as the RowID by default. At this time, the RowID is sequentially increasing, and a write hotspot of the table forms when a large number of `INSERT` operations exist.

Meanwhile, the RowID in TiDB is also sequentially auto-incremental by default. When the primary key is not an integer type, you might also encounter the problem of write hotspots.

### Index hotspots

Index hotspots are similar to table hotspots. Common index hotspots appear in fields that are monotonously increasing in time order, or `INSERT` scenarios with a large number of repeated values.

## Identify hotspot issues

Performance problems are not necessarily caused by hotspots and might be caused by multiple factors. Before troubleshooting issues, confirm whether it is related to hotspots.

- To judge write hotspots, open **Hot Write** in the **TiKV-Trouble-Shooting** monitoring panel to check whether the Raftstore CPU metric value of any TiKV node is significantly higher than that of other nodes.

- To judge read hotspots, open **Thread_CPU** in the **TiKV-Details** monitoring panel to check whether the coprocessor CPU metric value of any TiKV node is particularly high.

### Use TiDB Dashboard to locate hotspot tables

The **Key Visualizer** feature in [TiDB Dashboard](/dashboard/dashboard-intro.md) helps users narrow down hotspot troubleshooting scope to the table level. The following is an example of the thermal diagram shown by **Key Visualizer**. The horizontal axis of the graph is time, and the vertical axis are various tables and indexes. The brighter the color, the greater the load. You can switch the read or write flow in the toolbar.

![Dashboard Example 1](/media/troubleshoot-hot-spot-issues-1.png)

The following bright diagonal lines (oblique upward or downward) can appear in the write flow graph. Because the write only appears at the end, as the number of table Regions becomes larger, it appears as a ladder. This indicates that a write hotspot shows in this table:

![Dashboard Example 2](/media/troubleshoot-hot-spot-issues-2.png)

For read hotspots, a bright horizontal line is generally shown in the thermal diagram. Usually these are caused by small tables with a large number of accesses, shown as follows:

![Dashboard Example 3](/media/troubleshoot-hot-spot-issues-3.png)

Hover over the bright block, you can see what table or index has a heavy load. For example:

![Dashboard Example 4](/media/troubleshoot-hot-spot-issues-4.png)

## Use `SHARD_ROW_ID_BITS` to process hotspots

When a primary key is non-integer or a table without a primary key or a joint primary key, TiDB use an implicit self-increasing RowID. A large number of writes write a data set to a single Region, resulting in writing hot spots.

By setting SHARD_ROW_ID_BITS, RowID can be broken out and written to multiple different regions, Alleviate write hot issues. However, excessively large Settings cause the number of RPC requests to be enlarged, increasing CPU and network overhead.

```
SHARD_ROW_ID_BITS = 4 represents 16 slices 
SHARD_ROW_ID_BITS = 6 represents 64 slices 
SHARD_ROW_ID_BITS = 0 represents the default value of 1 sharding
```

For example:

```sql
CREATE TABLE：CREATE TABLE t (c int) SHARD_ROW_ID_BITS = 4;
ALTER TABLE：ALTER TABLE t SHARD_ROW_ID_BITS = 4;
```

> SHARD_ROW_ID_BITS values can be dynamically modified, after each modification, only for newly written data.
>
> When TiDB alter-primary-key parameter is set to false, the table's integer primary key is used as the RowID. The SHARD_ROW_ID_BITS option can not be used at this time because SHARD_ROW_ID_BITS changes the RowID generation rules. When the alter-primary-key parameter is set to true, the TiDB no longer uses the integer primary key as the table when building the table RowID, and the table with the integer primary key can also use the SHARD_ROW_ID_BITS feature.

Here are two flow charts that use SHARD_ROW_ID_BITS to scatter hot spots without primary keys, The first shows the situation before the break-up, the second shows the situation after the break-up.

![Dashboard Example 5](/media/troubleshoot-hot-spot-issues-5.png)

![Dashboard Example 6](/media/troubleshoot-hot-spot-issues-6.png)

Visible from the flow chart, after setting the SHARD_ROW_ID_BITS, the flow hotspots become very scattered from the previous only on one Region.

## Handle self-increasing primary key hotspots using AUTO_RANDOM

AUTO_RANDOM processing of self-increased primary key hot spot table is suitable to replace self-increased primary key and solve the writing hot spot brought by self-increased primary key.

> **Note:**
>
> Currently, this is an experimental feature, so it is not recommended to use it in the production environment. To enable this feature, use the following configuration:
>
> ```
> [experimental]\
> allow-auto-random = true
> ```

After using this function, the TiDB will generate randomly distributed and non-repeated primary keys to achieve the purpose of discrete write, scattered write hot spots.

> Note that the primary key generated by the TiDB is no longer a self-increased primary key and LAST_INSERT_ID() can be used to obtain the primary key value assigned last time.

This function can be used by changing the AUTO_INCREMENT in the built predicative sentence to the AUTO_RANDOM, which applies to scenarios where the primary key only needs to be guaranteed to be unique and does not contain business meaning.
For examples:

```sql
> CREATE TABLE t (a BIGINT PRIMARY KEY AUTO_RANDOM, b varchar(255));
> INSERT INTO t (b) VALUES ("foo");
> SELECT * FROM t;
+------------+---+
| a          | b |
+------------+---+
| 1073741825 | b |
+------------+---+

> SELECT LAST_INSERT_ID();
+------------------+
| LAST_INSERT_ID() |
+------------------+
| 1073741825       |
+------------------+
```

The following is to change the AUTO_INCREMENT table to the flow chart after AUTO_RANDOM scattered hot spots, the first is AUTO_INCREMENT, the second is the AUTO_RANDOM.

![Dashboard Example 7](/media/troubleshoot-hot-spot-issues-7.png)

![Dashboard Example 8](/media/troubleshoot-hot-spot-issues-8.png)

Visible from the flow chart, the use of AUTO_RANDOM instead of AUTO_INCREMENT can well disperse hot spots.

More detailed instructions can be read [AUTO_RANDOM](https://pingcap.com/docs/stable/reference/sql/attributes/auto-random/) documentation.

## Optimization of small table hotspots

TiDB supports push-down computing results caching from 4.0(i.e. Coprocessor Cache functionality). When this function is turned on, the result of TiKV calculation will be pushed back on the TiDB instance side.

A more detailed description can be read in the [push-down results cache](https://pingcap.com/docs/stable/coprocessor-cache/#configuration) document.

**Other relevant information**

[Highly Concurrent Write Best Practices](https://pingcap.com/docs/dev/reference/best-practices/high-concurrency/)

[Split Region](https://pingcap.com/docs/stable/sql-statements/sql-statement-split-region/)
