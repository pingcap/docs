---
title: Troubleshoot Hotspot Issues
summary: Learn how to locate and resolve read or write hotspot issues in TiDB.
category: troubleshoot
aliases: ['/docs/dev/troubleshoot-hot-spot-issues/']
---
# Troubleshoot Hotspot Issues

This document describes how to locate and resolve the problem of read and write hotspots.

As a distributed database, TiDB has a load balancing mechanism to distribute the application loads as evenly as possible to different computing or storage nodes, to make better use of server resources.
However, the mechanism is not omnipotent. In some scenarios, some business loads may not be well dispersed, affecting performance, forming a single point of high load, and causing hot spots.

## Common hot spots

### TiDB encoding rules

TiDB assigns a TableID to each table,Each index is assigned an IndexID, and each row is assigned a RowID (By default, if the table USES an integer Primary Key, the value of the Primary Key is treated as RowID).Among them, TableID is unique in the entire cluster, and IndexID/RowID is unique in the table. These IDs are all int64 types.

Each row of data is encoded as a key-value pair according to the following rules:

```text
Key: tablePrefix{tableID}_recordPrefixSep{rowID}
Value: [col1, col2, col3, col4]
```

The TablePrefix/recordPrefixSep of Key are specific string constants, which are used to distinguish other data in the KV space.

For Index data, key-value pair is encoded according to the following rules:

```text
Key: tablePrefix{tableID}_indexPrefixSep{indexID}_indexedColumnsValue_rowID
Value: null
```

### Table of hot spots

From TiDB coding rules, The data of the same table will be in a range prefixed by the beginning of the table id, and the order of the data is arranged in the order of the RowID values. When RowID values are incremented during table insert, The inserted line can only be appended at the end. When the region reaches a certain size, it will split, then it can only be appended at the end of the range range, and can always be insert on one region to form a hot spot.

The common increment type self-increment primary key is the sequential increment, by default, when the primary key is integer type, will use the primary key value as the RowID, at this time the RowID is the sequential increment, in a large number of insert to form writing hot spot of the table.

Meanwhile, RowID default in the TiDB is incremented in the order of self-increment. When the primary key is not an integer type, the writing hot spot will also be encountered.

### Index hot spots

Index hot spots are similar to table hot spots, and common hot spots appear in fields that are monotonously increasing in time order, or insert scenes with a large number of repeated values.

## Identify hotspot issues

Performance problems are not necessarily caused by hot spots, there may be a number of factors together, before checking need to confirm whether it is related to hot spots.

- The basis for judging and writing hot spots:Open the Hot Write panel in the TiKV-Trouble-Shooting of the monitoring panel (as shown in the figure below) to observe whether there is a phenomenon that the index of individual TiKV nodes is significantly higher than that of other nodes in the monitoring Raftstore CPU.

- Read hot spot basis: open the monitor panel TIKV-Details Thread_CPU, see if there is any obvious tikv particularly high.

### Use TiDB Dashboard to locate hotspot tables

The "Key Visualizer" feature in TiDB Dashboard helps users narrow down hot spot screening to table level,  Here is an example of the thermal diagram shown by the Hotspot Visualization function, where the horizontal coordinates are time, and the vertical coordinates arrange tables and indexes, The brighter the color, the greater the flow. You can switch to display read or write traffic in the toolbar.

![Dashboard Example 1](/media/troubleshoot-hot-spot-issues-1.png)

When the following bright slashes (diagonal up or diagonal down) appear in the write flow graph, Since writing only appears at the end, As the number region tables increases, they appear ladder-shaped. This shows that the table constitutes a writing hotspot:

![Dashboard Example 2](/media/troubleshoot-hot-spot-issues-2.png)

For reading hot spots, a bright horizontal line is generally shown in the thermodynamic diagram, Usually small tables with a large number of accesses, as shown in the figure below:

![Dashboard Example 3](/media/troubleshoot-hot-spot-issues-3.png)

Move the mouse over the bright block, You can see what table or index has a lot of traffic, for example:

![Dashboard Example 4](/media/troubleshoot-hot-spot-issues-4.png)

> [Prior to version 4.0 hot spot location can refer to this document](https://book.tidb.io/session4/chapter7/hotspot-resolved.html)

## Use `SHARD_ROW_ID_BITS` to process hotspots

 When a primary key is non-integer or a table without a primary key or a joint primary key, TiDB use an implicit self-increasing RowID. A large number of writes write a data set to a single Region, resulting in writing hot spots.

 By setting SHARD_ROW_ID_BITS, RowID can be broken out and written to multiple different regions, Alleviate write hot issues. However, excessively large Settings cause the number of RPC requests to be enlarged, increasing CPU and network overhead.

SHARD_ROW_ID_BITS = 4 represents 16 slices 
SHARD_ROW_ID_BITS = 6 represents 64 slices 
SHARD_ROW_ID_BITS = 0 represents the default value of 1 sharding

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

> The function is currently experimental and is not recommended for use in the production environment. Can be enabled using the following configuration:
>
> [experimental]\
> allow-auto-random = true

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
