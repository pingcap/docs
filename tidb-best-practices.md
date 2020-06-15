---
title: TiDB Best Practice
summary:
category: reference
---

# TiDB Best Practice

This document summarizes the best practices of using TiDB, including the use of SQL and optimization tips for OLAP/OLTP scenarios, especially the optimization switches specific for TiDB.

Before you read this document, it is recommended that you read three blog posts that introduces the technical principle of TiDB:

* [TiDB Internal (I) - Data Storage](https://pingcap.com/blog/2017-07-11-tidbinternal1/)
* [TiDB Internal (II) - Computing](https://pingcap.com/blog/2017-07-11-tidbinternal2/)
* [TiDB Internal (III) - Scheduling](https://pingcap.com/blog/2017-07-20-tidbinternal3/)

## Foreword

The database is a generic component of infrastructure. When building a database, developers must have multiple target scenarios in mind. In a specific scenario, users need to adjust the parameters or usage according to the application.

TiDB is a distributed database compatible with the MySQL protocol. However, due to TiDB's internal implementation, especially because TiDB supports distributed storage and distributed transactions, some usage is different from that of MySQL.

## Concept

TiDB's best practices are closely related to its implementation principles. It is recommended that you learn some of the basic mechanisms, including the Raft consensus algorithm, distributed transactions, data sharding, load balancing, the mapping scheme from SQL to KV, the implementation method of secondary indexes, and distributed execution engines.

This section is an introduction to these concepts. For detailed information, refer to [PingCAP blog posts](https://pingcap.com/blog/).

### Raft

Raft is a consensus algorithm that guarantees strongly consistent data replication. TiDB replicates data at the bottom layer by using Raft. Each write operation writes into a majority of replicas before TiDB returns externally that the write operation is successful. In this way, even if a few replicas are lost, TiDB still has the latest data.

For example, when there are 3 replicas in the system, a write operation is considered successful only when the data is written into at least 2 replicas. Whenever 1 replica is lost, at least one of the two surviving replicas has the latest data.

Compared to the master-slave replication method, which also keeps three replicas, Raft is more efficient. The latency of a write operation depends on the two fastest replicas, not on the slowest one. So with Raft replication, the geo-distributed multi-active scenario is made possible. In a typical scenario of three data centers in two cities, each write operation only needs to be successful in this data center and the closest one to ensure data consistency, without the need for successful writes in all three data centers.

However, this doesn't mean that you can build a cross-center deployment in every scenario. When writes are heavy, the bandwidth and latency between data centers become critical factors. if the write speed exceeds the bandwidth between the data centers, or if latency is too large between data centers, the Raft replication mechanism does not work well.

### Distributed transactions

TiDB provides a fully distributed transaction model, which is optimized on top of the [Google Percolator](https://research.google.com/pubs/pub36726.html). This document introduces the following features:

* Optimistic transaction model

    In TiDB, the optimistic transaction model performs conflict checks only when the transaction is committed. If conflicts exist, the transaction needs retry. In highly contention scenarios, this model is inefficient, because all operations before the retry becomes invalid and must be done repeatedly.

    Take an extreme case as example. When the database is used as a counter, in a highly concurrent scenario, serious conflicts will cause a large number of retries and even timeout.
    
    If the conflicts are not serious, the optimistic transaction model is efficient. Otherwise, it is recommended that you use the pessimistic transaction model, or solve the issue in the system architecture, such as putting the counter in Redis.

* Pessimistic transaction model

    In TiDB, the pessimistic transaction model has almost the same behavior as in MySQL. The transaction applies a lock during the execution phase, which avoids retries in conflict situations and ensures a higher success ratio. By applying the pessimistic locking, you can also lock data in advance using `select for update`.
    
    However, if the business scenario itself has fewer conflicts, the optimistic transaction model has better performance.

* Transaction size limit

    Distributed transactions must perform two-phase commit (2PC), and data is replicated at the bottom layer via the Raft consensus algorithm. Therefore, if a transaction is large, the commit process becomes so slow that it blocks the Raft replication.

    To avoid the system being blocked, the size of transaction has the following limit:

    - A single transaction contains no more than 5,000 SQL statements (default)
    - A single KV entry is not larger than 6 MB.
    - The total size KV entry is not larger than 10 GB.

    Similar limits can also be found in [Cloud Spanner](https://cloud.google.com/spanner/quotas) of Google.

### Data sharding

TiKV automatically shards the bottom data by the range of keys. Each Region is a range of keys, which is a left-closed and right-open interval from `StartKey` to `EndKey`. When the number of Key-Value pairs exceeds a certain limit, the Region is automatically split into two.

### Load balancing

PD schedules the load of the cluster according to the status of the entire TiKV cluster. Scheduling is automatically performed in the unit of Region and takes the policy of the PD configuration as the scheduling logic.

### SQL on KV

TiDB automatically maps SQL to Key-Value. For details, see [TiDB Internal (II) - Computing](https://pingcap.com/blog/2017-07-11-tidbinternal2/).

Briefly speaking, TiDB performs the following operations:

* A row of data is mapped to a Key-Value pair. The key takes `TableID` to form the prefix and the row ID to form the suffix.
* An index is mapped to a Key-Value pair. The key takes `TableID+IndexID` to form the prefix and the index value to form the suffix.

The data or indexes in the same table have the same prefix. In the Key space of TiKV, these Key-Value pairs are located in adjacent places. When heavy writes are on the same table, this leads to write hotspots. Especially when the data that are being written consecutively has some consecutive index values (for example, some time-incremental fields like `update time`), hotspots occur on several Regions, which becomes the bottleneck of the whole system.

Similarly, if all read operations focus on a small range (such as several tens of thousands of consecutive rows), this leads to read hotspots.

### Secondary index

TiDB provides full support for global secondary indexes, and many queries can be optimized through indexes. Thus, it is important for applications to make good use of secondary indexes.

A large amount of experience with MySQL is applicable to TiDB, but note that TiDB also has some exclusive features. This section introduces some considerations when you use secondary indexes in TiDB.

* The more secondary indexes, the better?

    Secondary indexes can accelerate queries, but adding an index has some side effects. The previous section introduces the storage model of indexes: when a new index is added, each insert of data requires one more Key-Value pair. Therefore, the more indexes, the slower the write operation is and the more space it occupies.

    In addition, too many indexes also affects the optimizer runtime. Inappropriate indexes might mislead the optimizer. Thus, it is not necessarily true that the more indexes, the better.

* Which column is better to create index on

    As is mentioned above, indexes are important, but not the more the better, so you need to create the right indexes for your application. In principle, you need to create indexes on the columns used in query to improve performance. The following situations are suitable for creating indexes:

    - Columns that has large differences. By using indexes, you can significantly reduce the number of filtered rows.
    - When there are multiple query conditions, you can select the combined index. Note that you need to put the column of equivalent conditions in front of the combined index.

    For example, assume that a frequent query is `select * from t where c1 = 10 and c2 = 100 and c3 > 10`. You might create a combined index `Index cidx (c1, c2, c3)`, and the query conditions can be used to construct an index prefix for scan.

* The difference between querying through index and directly scanning the table



## Scenarios and practices

### Deploy

### Import data

### Write data 

### Query

### Monitoring and log

### Documentation

## Best scenarios of TiDB 