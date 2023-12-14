---
title: Glossary
summary: Glossaries about TiDB.
aliases: ['/docs/dev/glossary/']
---

# Glossary

## A

### ACID

ACID refers to the four key properties of a transaction: atomicity, consistency, isolation, and durability. Each of these properties is described below.

- **Atomicity** means that either all the changes of an operation are performed, or none of them are. TiDB ensures the atomicity of the [Region](#regionpeerraft-group) that stores the Primary Key to achieve the atomicity of transactions.

- **Consistency** means that transactions always bring the database from one consistent state to another. In TiDB, data consistency is ensured before writing data to the memory.

- **Isolation** means that a transaction in process is invisible to other transactions until it completes. This allows concurrent transactions to read and write data without sacrificing consistency. TiDB currently supports the isolation level of `REPEATABLE READ`.

- **Durability** means that once a transaction is committed, it remains committed even in the event of a system failure. TiKV uses persistent storage to ensure durability.

## B

### Batch Create Table

Batch Create Table is a feature introduced in TiDB v6.0.0. This feature is enabled default. When restoring data with a large number of tables (nearly 50000) using BR (Backup & Restore), the feature can greatly speed up the restore process by creating tables in batches. For details, see [Batch Create Table](/br/br-batch-create-table.md).

### Baseline Capturing

Baseline Capturing captures queries that meet capturing conditions and create bindings for them. It is used for [preventing regression of execution plans during an upgrade](/sql-plan-management.md#prevent-regression-of-execution-plans-during-an-upgrade).

### Binlog

Binlog is short for binary logging. In MySQL and MariaDB, it is used to record changes in table structure (such as `CREATE` and `ALTER TABLE` statements) and table data (such as `INSERT`, `DELETE`, and `UPDATE` statements). The binlogs can be used to replace data or as part of a point-in-time recovery procedure. The binary log is what [Data Migration](/dm/dm-overview.md) uses to fetch changes from MySQL or MariaDB.

In TiDB, there is [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md) that performed similar functions in TiDB; however, it has been deprecated and replaced by [PITR](/br/br-pitr-guide.md) and [TiCDC](/ticdc/ticdc-overview.md).

### Bucket

A [Region](#regionpeerraft-group) is logically divided into several small ranges called bucket. TiKV collects query statistics by buckets and reports the bucket status to PD. For details, see the [Bucket design doc](https://github.com/tikv/rfcs/blob/master/text/0082-dynamic-size-region.md#bucket).

## C

### Cached Table

With the cached table feature, TiDB loads the data of an entire table into the memory of the TiDB server, and TiDB directly gets the table data from the memory without accessing TiKV, which improves the read performance.

### Cluster

A set of nodes that form a group that fulfills a common task of providing a platform that provides services. A cluster typically includes different type of nodes, for example, a TiDB cluster usually consists of TiDB nodes, TiKV nodes, and PD nodes, and a DM cluster usually consists of DM Master nodes and DM Worker nodes.

### Coalesce Partition

Coalesce Partition is a way of decreasing the number of partitions in a Hash or Key partitioned table. For more information, see [Manage Hash and Key partitions](/partitioned-table.md#manage-hash-and-key-partitions).

### Common table expression (CTE)

A Common Table Expression (CTE) is a temporary result set that can be referred to multiple times within a SQL statement to improve the statement readability and execution efficiency. You can use the [`WITH` statement](/sql-statements/sql-statement-with.md) to use CTEs.

Common Table Expressions can be classified into two types: non-recursive CTE and recursive CTE.

For details, see [Common Table Expression (CTE)](/develop/dev-guide-use-common-table-expression.md).

### Continuous Profiling

Introduced in TiDB 5.3.0, Continuous Profiling is a way to observe resource overhead at the system call level. With the support of Continuous Profiling, TiDB provides performance insight as clear as directly looking into the database source code, and helps R&D and operation and maintenance personnel to locate the root cause of performance problems using a flame graph. For details, see [TiDB Dashboard Instance Profiling - Continuous Profiling](/dashboard/continuous-profiling.md).

### Coprocessor

A coprocessing mechanism that shares the computation workload with TiDB. It is located in the storage layer (TiKV or TiFlash) and collaboratively processes computations [pushed down](/functions-and-operators/expressions-pushed-down.md) from TiDB on a per-region basis.

## D

### Dumpling

Dumpling is a data export tool for exporting data stored in TiDB, MySQL or MariaDB as SQL or CSV data files and can be used to make a logical full backup or export. Dumpling also supports exporting data to Amazon S3.

For details, see [Use Dumpling to Export Data](/dumpling-overview.md).

### Dynamic Pruning

Dynamic pruning mode is one of the modes that TiDB accesses partitioned tables. In dynamic pruning mode, each operator supports direct access to multiple partitions. Therefore, TiDB no longer uses Union. Omitting the Union operation can improve the execution efficiency and avoid the problem of Union concurrent execution.

## E

### Expression index

The expression index is a type of special index that can be created on an expression. Once an expression index is created, TiDB can use the index for the expression-based query, which significantly improves the query performance.

For details, see [CREATE INDEX - Expression index](/sql-statements/sql-statement-create-index.md#expression-index).

## G

### GC (Garbage Collection)

Garbage collection (GC) is the memory resource management mechanism in TiDB. When old data in dynamic memory is no longer needed, it is cleaned up to free up memory.

For details, see [GC Overview](/garbage-collection-overview.md).

## H

### Hotspot

Hotspot refers to the phenomenon where the read and/or write workload of TiKV is concentrated on one or several regions or nodes, which might cause performance bottlenecks and prevent optimal performance. To solve hotspot issues, refer to [Troubleshoot Hotspot Issues](/troubleshoot-hot-spot-issues.md).

### HTAP

HTAP stands for "Hybrid Transactional and Analytical Processing". This combines online transaction processing (OLTP) workloads with online analytical processing (OLAP) on the same platform. One of the features that this brings is real-time analytics. This is done by combining row-based data in TiKV and columnar data in TiFlash that is kept in sync by replicating data between the two storage engines in a way that can maintain strong consistency.

For details, refer to [Quick Start Guide for TiDB HTAP](/quick-start-with-htap.md) and [Explore HTAP](/explore-htap.md).

## I

### Index Merge

Index Merge is a method introduced in TiDB v4.0 to access tables. Using this method, the TiDB optimizer can use multiple indexes per table and merge the results returned by each index. In some scenarios, this method makes the query more efficient by avoiding full table scans. Since v5.4, Index Merge has become a GA feature.

### In-Memory Pessimistic Lock

The in-memory pessimistic lock is a new feature introduced in TiDB v6.0.0. When this feature is enabled, pessimistic locks are usually stored in the memory of the Region leader only, and are not persisted to disk or replicated through Raft to other replicas. This feature can greatly reduce the overhead of acquiring pessimistic locks and improve the throughput of pessimistic transactions.

## L

### leader/follower/learner

Leader/Follower/Learner each corresponds to a role in a Raft group of [peers](#regionpeerraft-group). The leader services all client requests and replicates data to the followers. If the group leader fails, one of the followers will be elected as the new leader. Learners are non-voting followers that only serves in the process of replica addition.

### Lock View

The Lock View feature is used to provide more information about lock conflicts and lock waits in pessimistic locking, making it convenient for DBAs to observe transaction locking situations and troubleshoot deadlock issues.

For details, see system table documentation: [`TIDB_TRX`](/information-schema/information-schema-tidb-trx.md), [`DATA_LOCK_WAITS`](/information-schema/information-schema-data-lock-waits.md), and [`DEADLOCKS`](/information-schema/information-schema-deadlocks.md).
## M

### MPP

Starting from v5.0, TiDB introduces Massively Parallel Processing (MPP) architecture through TiFlash nodes, which shares the execution workloads of large join queries among TiFlash nodes. When the MPP mode is enabled, TiDB, based on cost, determines whether to use the MPP framework to perform the calculation. In the MPP mode, the join keys are redistributed through the Exchange operation while being calculated, which distributes the calculation pressure to each TiFlash node and speeds up the calculation. For more information, see [Use TiFlash MPP Mode](/tiflash/use-tiflash-mpp-mode.md).

### Multi-version concurrency control (MVCC)

[MVCC](https://en.wikipedia.org/wiki/Multiversion_concurrency_control) is a concurrency control mechanism in TiDB and other databases. It processes the memory read by transactions to achieve concurrent access to TiDB, thereby avoiding blocking caused by conflicts between concurrent reads and writes.

## O

### Old value

The "original value" in the incremental change log output by TiCDC. You can specify whether the incremental change log output by TiCDC contains the "original value".

### Online transactional processing (OLTP)

Online transactional processing (OLTP) refers to the use of computer systems to process transactional data.

### Operator

An operator is a collection of actions that applies to a Region for scheduling purposes. Operators perform scheduling tasks such as "migrate the leader of Region 2 to Store 5" and "migrate replicas of Region 2 to Store 1, 4, 5".

An operator can be computed and generated by a [scheduler](#scheduler), or created by an external API.

### Operator step

An operator step is a step in the execution of an operator. An operator normally contains multiple Operator steps.

Currently, available steps generated by PD include:

- `TransferLeader`: Transfers leadership to a specified member
- `AddPeer`: Adds peers to a specified store
- `RemovePeer`: Removes a peer of a Region
- `AddLearner`: Adds learners to a specified store
- `PromoteLearner`: Promotes a specified learner to a voting member
- `SplitRegion`: Splits a specified Region into two

### Optimistic transaction

Optimistic transactions are transactions that use optimistic concurrency control and generally do not cause conflicts in concurrent environments. After enabling optimistic transactions, TiDB only checks for conflicts when the transaction is finally committed. The optimistic transaction mode is suitable for concurrent scenarios with more reads and fewer writes, which can improve the performance of TiDB.


## P

### Partitioning

[Partitioning](/partitioned-table.md) refers to physically dividing a table into smaller table partitions, which can be done by partition methods such as RANGE, LIST, HASH, and KEY partitioning.

### PD Control (pd-ctl)

PD Control (pd-ctl) is a command-line tool to interface with the placement driver (PD) of the cluster. This can be used to obtain cluster status information and configuration and modify the cluster. For details, see [PD Control User Guide](/pd-control.md).

### pending/down

"Pending" and "down" are two special states of a peer. Pending indicates that the Raft log of followers or learners is vastly different from that of leader. Followers in pending cannot be elected as leader. "Down" refers to a state that a peer ceases to respond to leader for a long time, which usually means the corresponding node is down or isolated from the network.

### Placement Rules

Placement rules are used to configure the placement of data in a TiKV cluster through the SQL interface. With this feature, you can specify the deployment of tables and partitions to different regions, data centers, cabinets, and hosts. Use cases include optimizing data availability strategies at low cost, ensuring that local data replicas are available for local stale reads, and complying with local data compliance requirements.

For details, see [Placement Rules in SQL](/placement-rules-in-sql.md).

### Point Get

Point get means reading a single row of data by a unique index or primary index, the returned resultset is up to one row.

### Predicate columns

In most cases, when executing SQL statements, the optimizer only uses statistics of some columns (such as columns in the `WHERE`, `JOIN`, `ORDER BY`, and `GROUP BY` statements). These used columns are called predicate columns. For details, see [Collect statistics on some columns](/statistics.md#collect-statistics-on-some-columns).

## Q

### Quota Limiter

Quota Limiter is an experimental feature introduced in TiDB v6.0.0. If the machine on which TiKV is deployed has limited resources, for example, with only 4v CPU and 16 G memory, and the foreground of TiKV processes too many read and write requests, the CPU resources used by the background are occupied to help process such requests, which affects the performance stability of TiKV. To avoid this situation, the [quota-related configuration items](/tikv-configuration-file.md#quota) can be set to limit the CPU resources to be used by the foreground.

## R

### Raft Engine

Raft Engine is an embedded persistent storage engine with a log-structured design. It is built for TiKV to store multi-Raft logs. Since v5.4, TiDB supports using Raft Engine as the log storage engine. For details, see [Raft Engine](/tikv-configuration-file.md#raft-engine).

### Region/peer/Raft group

Region is the minimal piece of data storage in TiKV, each representing a range of data (96 MiB by default). Each Region has three replicas by default. A replica of a Region is called a peer. Multiple peers of the same Region replicate data via the Raft consensus algorithm, so peers are also members of a Raft instance. TiKV uses Multi-Raft to manage data. That is, for each Region, there is a corresponding, isolated Raft group.

### Region split

Regions are generated as data writes increase. The process of splitting is called Region split.

The mechanism of Region split is to use one initial Region to cover the entire key space, and generate new Regions through splitting existing ones every time the size of the Region or the number of keys has reached a threshold.

### restore

Restore is the reverse of the backup operation. It is the process of bringing back the system to an earlier state by retrieving data from a prepared backup.

### RocksDB

[RocksDB](https://rocksdb.org/) is an LSM-tree structured engine that provides key-value storage and read-write functionality. It was developed by Facebook and is based on LevelDB. RocksDB is the core storage engine of TiKV.

## S

### scheduler

Schedulers are components in PD that generate scheduling tasks. Each scheduler in PD runs independently and serves different purposes. The commonly used schedulers are:

- `balance-leader-scheduler`: Balances the distribution of leaders
- `balance-region-scheduler`: Balances the distribution of peers
- `hot-region-scheduler`: Balances the distribution of hot Regions
- `evict-leader-{store-id}`: Evicts all leaders of a node (often used for rolling upgrades)

### Security Enhanced Mode (SEM)

The Security Enhanced Mode (SEM) is used for finer-grained permission control of TiDB administrators. SEM is inspired by the design of systems such as [Security-Enhanced Linux](https://en.wikipedia.org/wiki/Security-Enhanced_Linux). It reduces the abilities of users with the `SUPER` privilege and instead requires `RESTRICTED` fine-grained privileges to be granted as a replacement.

For details, see [System Variables documentation - `tidb_enable_enhanced_security`](/system-variables.md#tidb_enable_enhanced_security).

### Stale Read

Stale Read is a mechanism that TiDB applies to read historical versions of data stored in TiDB. Using this mechanism, you can read the corresponding historical data of a specific point in time or within a specified time range, and thus save the latency brought by data replication between storage nodes. When you are using Stale Read, TiDB will randomly select a replica for data reading, which means that all replicas are available for data reading.

For details, see [Stale Read](/stale-read.md).

### Store

A store refers to the storage node in the TiKV cluster (an instance of `tikv-server`). Each store has a corresponding TiKV instance.

## T

### Temporary table

Temporary tables solve the issue of temporarily storing the intermediate results of an application, which frees you from frequently creating and dropping tables. You can store the intermediate calculation data in temporary tables. When the intermediate data is no longer needed, TiDB automatically cleans up and recycles the temporary tables. This avoids user applications being too complicated, reduces table management overhead, and improves performance.

For details, see [Temporary Tables](/temporary-tables.md).

### TiCDC

[TiCDC](/ticdc/ticdc-overview.md) is a tool for incrementally replicating data in TiDB. It pulls the data change logs from the upstream TiKV and parses them into ordered row-level change data, which it then outputs to the downstream. For more information about the concepts and terms of TiCDC, see [TiCDC Glossary](/ticdc/ticdc-glossary.md).

### TiDB Data Migration (DM)

[TiDB Data Migration](https://github.com/pingcap/tiflow/tree/master/dm) (DM) is a data migration tool that supports full data migration and incremental data replication from databases compatible with the MySQL protocol (MySQL, MariaDB, Aurora MySQL) to TiDB.

For more information about the concepts and terms of DM, see [TiDB Data Migration Glossary](/dm/dm-glossary.md).

### TiDB Lightning

[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) is a tool for importing Terabyte-level data from static files into TiDB clusters. It is commonly used for the initial data import into TiDB clusters.

For more information on the concepts and terminology of TiDB Lightning, see [TiDB Lightning Glossary](/tidb-lightning/tidb-lightning-glossary.md).

### TiFlash

[TiFlash](/tiflash/tiflash-overview.md) is a key component of TiDB's HTAP architecture. It is a columnar extension of TiKV that provides both strong consistency and good isolation. Columnar replicas are asynchronously replicated through the Raft Learner protocol. When reading, the replicas use the Raft consensus index along with MVCC to achieve Snapshot Isolation consistency level. This architecture effectively solves the isolation and synchronization issues in HTAP scenarios.

### TiUP

[TiUP](/tiup/tiup-overview.md) is a management tool used for deploying, upgrading, and managing TiDB clusters, as well as managing various components within the TiDB ecosystem including TiDB, PD, and TiKV. With TiUP, you can easily run any component within TiDB by executing just one command, greatly simplifying the management process.

### Top SQL

Top SQL helps locate SQL queries that contribute to a high load of a TiDB or TiKV node in a specified time range. For details, see [Top SQL user document](/dashboard/top-sql.md).

### TSO

Because TiKV is a distributed storage system, it requires a global timing service, Timestamp Oracle (TSO), to assign a monotonically increasing timestamp. In TiKV, such a feature is provided by PD, and in Google [Spanner](http://static.googleusercontent.com/media/research.google.com/en//archive/spanner-osdi2012.pdf), this feature is provided by multiple atomic clocks and GPS.

### TTL

[Time to live (TTL)](/time-to-live.md) is a feature that allows you to manage TiDB data lifetime at the row level. For a table with the TTL attribute, TiDB automatically checks data lifetime and deletes expired data at the row level.
