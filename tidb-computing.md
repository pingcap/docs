---
title: TiDB database computation
summary: Understand the computation layer of the TiDB database.
category: introduction
---

# Computation of TiDB database

Bases on the distributed storage capability provided by TiKV, TiDB builds the computing engine that combines superior transaction processing with good data analysis capabilties. This article starts with a data mapping algorithm to describe how TiDB maps data from database tables to TiKV's (Key, Value) key-value pairs, then a description of how TiDB manages meta-information, and finally a description of the main architecture of the TiDB SQL layer.

For computation layer dependent storage schemes, this paper only introduces TiKV based row storage structures. For analytic services, TiDB introduces a column storage scheme as a TiKV extension [TiFlash](/tiflash/tiflash-overview.md).

## Mapping of table data to Key-Value

This section describes the scheme for mapping data to (Key, Value) key-value pairs in TiDB. Data here consists of the following two main aspects.

- Data for each row in the table, hereinafter referred to as table data.
- Data for all indexes in the table, hereinafter referred to as index data.

### Mapping of table data to Key-Value

In a relational database, a table may have many columns. To map the data from each column in a row to a (Key, Value) key-value pair, you need to consider how to construct the Key. First of all, OLTP scenarios have a large number of operations such as adding, deleting, changing and searching for single or multiple rows, which require database to read a line of data quickly. Therefore, it is best to have a unique ID (either displayed or implicit) for the corresponding key to facilitate quick location. Second, many OLAP queries require a full table scan. If you can encode the keys of all rows in a table into an interval, the whole table can be efficiently scanned by range queries. Scanning assignments.

Based on the above considerations, the mapping of table data to Key-Value in TiDB is designed as follows.

- To ensure that data from the same table is kept together for easy searching, TiDB assigns a table ID to each table, using the denoted by `TableID`. Table ID is an integer that is unique throughout the cluster.
- TiDB assigns a row ID, represented by `RowID`, to each row of data in the table. The row ID is also an integer, unique within the table. For row ID, TiDB has made a small optimization, if a table has integer type primary key, TiDB will use primary key value as the row ID of this row of data.

Each row of data is encoded as a (Key, Value) key-value pair according to the following rules.

```
Key:    tablePrefix{TableID}_recordPrefixSep{ RowID}
Value: [col1, col2, col3, col4]
```

where `tablePrefix` and `recordPrefixSep` are both specific to `tablePrefix` and `recordPrefixSep`. A string constant used to distinguish other data in Key space. The exact value is given in the summary that follows.

### Mapping of Indexed Data to Key-Values

TiDB supports both primary keys and secondary indexes (both unique and non-unique indexes). Similar to the table data mapping scheme, TiDB assigns an index ID to each index in the table, using ` IndexID` is indicated.

For primary keys and unique indexes, it is necessary to quickly locate the corresponding RowID based on the key value, so it is encoded as follows (Key, Value) Key-value pairs.

```
Key:    tablePrefix{tableID}_indexPrefixSep{ indexID}_indexedColumnsValue
Value: RowID
```

For ordinary secondary indexes that do not need to satisfy the uniqueness constraint, a single key may correspond to multiple rows, which need to be queried according to the range of keys. Therefore, it is encoded as a (Key, Value) key-value pair according to the following rules.

```
Key:    tablePrefix{TableID}_indexPrefixSep{ IndexID}_indexedColumnsValue_{RowID}
Value: null
```

### Summary of mapping relationships

`tablePrefix`, `recordPrefixSep` in all of the above encoding rules.  and `indexPrefixSep` are string constants that are used to distinguish between other Data, defined as follows.

```
tablePrefix      = []byte{'t'}
recordPrefixSep = []byte{'r'}
indexPrefixSep = []byte{'i'}
```

Also note that in the above scheme, all rows in a table are keyed, regardless of whether they are table data or index data. All have the same Key prefix, and all the data of an index also has the same prefix. Data with the same prefixes are thus arranged together in TiKV's key space. Therefore, by carefully designing the encoding scheme of the suffix section to ensure that the pre- and post-encoding comparisons remain the same, the table data can be or index data is stored in the TiKV in an ordered manner. With this encoding, all rows of data in a table are arranged in the TiKV's  In the key space, the data for a particular index will also be indexed according to the specific value of the index data (the ` indexedColumnsValue`) is sequentially arranged in the keyspace.

### Example of Key-Value mapping relationship

Finally, a simple example is used to understand the Key-Value mapping relationship of TiDB. Suppose the following table exists in TiDB.

``sql
CREATE TABLE User {
     ID int,
     Name varchar(20),
     Role varchar(20),
     Age int,
     PRIMARY KEY (ID),
     KEY idxAge (Age)
};
```

Suppose there are 3 rows of data in the table.

```
1, "TiDB", "SQL Layer", 10
2, "TiKV", "KV Engine", 20
3, "PD", "Manager", 30
```

First, each row of data is mapped to a (Key, Value) key-value pair, and the table has an ``int'' value. type `, so the value of `RowID` is the value of this primary key. Suppose the table has `TableID` of 10, then its table data stored on TiKV is.

```
t10_r1 --> ["TiDB", "SQL  Layer", 10]
t10_r2 --> ["TiKV", "KV  Engine", 20]
t10_r3 --> ["PD", " Manager", 30]
```

In addition to the primary key, the table has a non-unique ordinary secondary index, `idxAge`, which is assumed to have a ` IndexID` is 1, then its index data stored on TiKV is.

```
t10_i1_10_1 --> null
t10_i1_20_2 --> null
t10_i1_30_3 --> null
```

The above example shows the mapping rule from a relational model to a Key-Value model in TiDB, and the selection of this The considerations behind the program.

## Meta-information management

Each `Database` and `Table` in TiDB has meta information, i.e., its definition of the and various attributes. This information also needs to be persistent, and TiDB stores this information in TiKV as well.

Each `Database` / `Table` is assigned a unique ID, which is the ID of the  as a unique identifier, and when encoded as Key-Value, this ID is encoded in the Key and the `m_` prefix. This constructs a Key, which stores the serialized meta information in Value.

In addition, TiDB also uses a dedicated (Key, Value) key pair to store the current structure of all tables. The latest version number of the information. This key-value pair is global, and its version number is increased by 1 each time the state of the DDL operation changes.  Store this key-value pair persistently in the PD Server with a key of "/". tidb/ddl/global_schema_version", Value  is a version number value of type int64. TiDB references Google F1's  Online Schema change algorithm with a background thread constantly checking the PD Server  The version number of the table structure information stored in the

## Introduction to the SQL layer

TiDB's SQL layer, TiDB Server, is responsible for translating the SQL into Key- Value operation to the common distributed Key-Value storage layer TiKV, and then the Assembling the results returned by TiKV ultimately returns the query results to the client.

The nodes at this level are stateless, the nodes themselves do not store data, and the nodes are completely peer-to-peer.

### SQL algorithm

The simplest solution is through the [mapping of table data to Key-Value] as described in the previous section (#TableData mapping to -key-value-) scheme, mapping SQL queries to KV queries, and then the The KV interface acquires the corresponding data and performs various computations.

For example, `select count(*) from user where name =  "TiDB"` such a SQL statement, which takes all the data in the table and reads it. Then check if the `name` field is `TiDB`, and if so, return this line. The process is as follows.

1. construct the Key Range: all `RowID`s in a table are in `[0,  MaxInt64) `, use `0` and `MaxInt64` depending on the row data within the range of `0` and `MaxInt64`. The `Key` encoding rule constructs a `[StartKey, EndKey)` left-handed closure. Right open interval.
Scan Key Range: read TiKV according to the key range constructed above.  The data in.
3. filter data: for each row of data read, calculate `name = "TiDB& quot;` This expression returns up this line if true, otherwise discards this line of data.
4. Calculate `Count(*)`: for each line that meets the requirements, the total of the Results Above.

** The entire process is illustrated as follows:**

![naive sql flow](/media/tidb-computing-native-sql-flow.jpeg)

This solution is intuitive and feasible, but has some obvious problems in a distributed database scenario.

- As the data is being scanned, each row is read out of TiKV via a KV operation at least once  RPC overhead, which can be very high if there is a lot of data to scan.
- Not all rows meet the filter criteria `name = "TiDB"`. If the conditions are not met, you can actually not read them out.
- The value of the rows that meet the requirements doesn't mean anything, in fact all that's needed here is a few rows of data for this information.

### Distributed SQL operations

To solve the above problem, the computation should need to be as close to the storage node as possible to avoid a large number of RPC calls. First of all, the SQL predicate condition `name = "TiDB"` should be replaced by the is pushed down to the storage node for computation, so that only valid rows are returned, avoiding meaningless network transfers. Then, the aggregation function `Count(*)` can also be pushed down to the storage nodes for pre-aggregation, where each node only has You need to return a result of `Count(*)`, and the SQL layer will then return the results of the ` The result of Count(*) ` is summed up.

The following is a schematic representation of the data returned layer by layer.

![dist sql flow](/media/tidb-computing-dist-sql-flow.png)

### SQL layer architecture

With the above example, I hope you have a basic understanding of how SQL statements are handled. In fact, TiDB's SQL layer is much more complex, with many modules and layers. and calling relationships.

! [tidb sql layer](/media/tidb-computing-tidb -sql-layer.png)

The user's SQL request is sent to TiDB either directly or via `Load Balancer`.  Server, TiDB Server will parse `MySQL Protocol'  Packet`, getting the content of requests, parsing syntax and semantic analysis of SQL, developing and optimizing query plans. Execute a query plan and fetch and process the data. The data is all stored in the TiKV cluster, so in this process TiDB Server needs to work with the  TiKV interacts and gets the data. Finally, TiDB Server needs to return the query results to the user.