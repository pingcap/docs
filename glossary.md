---
title: Glossary
summary: Glossaries about TiDB.
---

# Glossary

This glossary provides definitions for key terms related to the TiDB platform.

Other available glossaries:

- [TiDB Data Migration Glossary](/dm/dm-glossary.md)
- [TiCDC Glossary](/ticdc/ticdc-glossary.md)
- [TiDB Lightning Glossary](/tidb-lightning/tidb-lightning-glossary.md)

## A

### ACID

ACID refers to the four key properties of a transaction: atomicity, consistency, isolation, and durability. Each of these properties is described below.

- **Atomicity** means that either all the changes of an operation are performed, or none of them are. TiDB ensures the atomicity of the [Region](#regionpeerraft-group) that stores the Primary Key to achieve the atomicity of transactions.

- **Consistency** means that transactions always bring the database from one consistent state to another. In TiDB, data consistency is ensured before writing data to the memory.

- **Isolation** means that a transaction in process is invisible to other transactions until it completes. This allows concurrent transactions to read and write data without sacrificing consistency. For more information, see [TiDB transaction isolation levels](/transaction-isolation-levels.md#tidb-transaction-isolation-levels).

- **Durability** means that once a transaction is committed, it remains committed even in the event of a system failure. TiKV uses persistent storage to ensure durability.

## B

### Backup & Restore (BR)

BR is the backup and restore tool for TiDB. For more information, see [BR Overview](/br/backup-and-restore-overview.md).

`br` is the [br command line tool](/br/use-br-command-line-tool.md) used for backups or restores in TiDB.

### Baseline Capturing

Baseline Capturing captures queries that meet capturing conditions and create bindings for them. It is used for [preventing regression of execution plans during an upgrade](/sql-plan-management.md#prevent-regression-of-execution-plans-during-an-upgrade).

### Batch Create Table

Batch Create Table is a feature introduced in TiDB v6.0.0. This feature is enabled by default. When restoring data with a large number of tables (nearly 50000) using BR (Backup & Restore), the feature can greatly speed up the restore process by creating tables in batches. For details, see [Batch Create Table](/br/br-batch-create-table.md).

### Bucket

A [Region](#regionpeerraft-group) is logically divided into several small ranges called bucket. TiKV collects query statistics by buckets and reports the bucket status to PD. For details, see the [Bucket design doc](https://github.com/tikv/rfcs/blob/master/text/0082-dynamic-size-region.md#bucket).

## C

### Cached Table

With the cached table feature, TiDB loads the data of an entire table into the memory of the TiDB server, and TiDB directly gets the table data from the memory without accessing TiKV, which improves the read performance.

### Coalesce Partition

Coalesce Partition is a way of decreasing the number of partitions in a Hash or Key partitioned table. For more information, see [Manage Hash and Key partitions](/partitioned-table.md#manage-hash-and-key-partitions).

### Column Family (CF)

In RocksDB and TiKV, a Column Family (CF) represents a logical grouping of key-value pairs within a database.

### Common Table Expression (CTE)

A Common Table Expression (CTE) enables you to define a temporary result set that can be referred to multiple times within a SQL statement using the [`WITH`](/sql-statements/sql-statement-with.md) clause. For more information, see [Common Table Expression](/develop/dev-guide-use-common-table-expression.md).

### Continuous Profiling

Introduced in TiDB 5.3.0, Continuous Profiling is a way to observe resource overhead at the system call level. With the support of Continuous Profiling, TiDB provides performance insight as clear as directly looking into the database source code, and helps R&D and operation and maintenance personnel to locate the root cause of performance problems using a flame graph. For details, see [TiDB Dashboard Instance Profiling - Continuous Profiling](/dashboard/continuous-profiling.md).

## D

### Data Definition Language (DDL)

Data Definition Language (DDL) is a part of the SQL standard that deals with creating, modifying, and dropping tables and other objects. For more information, see [DDL Introduction](/ddl-introduction.md).

### Data Migration (DM)

Data Migration (DM) is a tool for migrating data from MySQL-compatible databases into TiDB. DM reads data from a MySQL-compatible database instance and applies it to a TiDB target instance. For more information, see [DM Overview](/dm/dm-overview.md).

### Data Modification Language (DML)

Data Modification Language (DML) is a part of the SQL standard that deals with inserting, updating, and dropping rows in tables.

### Development Milestone Release (DMR)

Development Milestone Releases (DMR) are TiDB releases that introduce the latest features but do not offer long-term support. For more information, see [TiDB Versioning](/releases/versioning.md).

### Disaster Recovery (DR)

Disaster Recovery (DR) includes solutions that can be used to recover data and services from a disaster in the future. TiDB offers various Disaster Recovery solutions such as backups and replication to standby clusters. For more information, see [Overview of TiDB Disaster Recovery Solutions](/dr-solution-introduction.md).

### Distributed eXecution Framework (DXF)

Distributed eXecution Framework (DXF) is the framework used by TiDB to centrally schedule certain tasks (such as creating indexes or importing data) and execute them in a distributed manner. DXF is designed to efficiently use cluster resources while controlling resource usage and reducing the impact on core business transactions. For more information, see [DXF Introduction](/tidb-distributed-execution-framework.md).

### Dynamic Pruning

Dynamic pruning mode is one of the modes that TiDB accesses partitioned tables. In dynamic pruning mode, each operator supports direct access to multiple partitions. Therefore, TiDB no longer uses Union. Omitting the Union operation can improve the execution efficiency and avoid the problem of Union concurrent execution.

## G

### Garbage Collection (GC)

Garbage Collection (GC) is a process that clears obsolete data to free up resources. For information on TiKV GC process, see [GC Overview](/garbage-collection-overview.md).

### General Availability (GA)

General Availability (GA) of a feature means the feature is fully tested and is Generally Available for use in production environments. TiDB features can be released as GA in both [DMR](#development-milestone-release-dmr) and [LTS](#long-term-support-lts) releases. However, as TiDB does not provide patch releases for DMR it is generally recommended to use the LTS release for production use.

### Global Transaction Identifiers (GTIDs)

Global Transaction Identifiers (GTIDs) are unique transaction IDs used in MySQL binary logs to track which transactions have been replicated. [Data Migration (DM)](/dm/dm-overview.md) uses these IDs to ensure consistent replication.

## H

### Hybrid Transactional and Analytical Processing (HTAP)

Hybrid Transactional and Analytical Processing (HTAP) is a database feature that enables both OLTP (Online Transactional Processing) and OLAP (Online Analytical Processing) workloads within the same database. For TiDB, the HTAP feature is provided by using TiKV for row storage and TiFlash for columnar storage. For more information, see [the definition of HTAP on the Gartner website](https://www.gartner.com/en/information-technology/glossary/htap-enabling-memory-computing-technologies).

## I

### In-Memory Pessimistic Lock

The in-memory pessimistic lock is a new feature introduced in TiDB v6.0.0. When this feature is enabled, pessimistic locks are usually stored in the memory of the Region leader only, and are not persisted to disk or replicated through Raft to other replicas. This feature can greatly reduce the overhead of acquiring pessimistic locks and improve the throughput of pessimistic transactions.

### Index Merge

Index Merge is a method introduced in TiDB v4.0 to access tables. Using this method, the TiDB optimizer can use multiple indexes per table and merge the results returned by each index. In some scenarios, this method makes the query more efficient by avoiding full table scans. Since v5.4, Index Merge has become a GA feature.

## K

### Key Management Service (KMS)

Key Management Service (KMS) enables the storage and retrieval of secret keys in a secure way. Examples include AWS KMS, Google Cloud KMS, and HashiCorp Vault. Various TiDB components can use KMS to manage keys for storage encryption and related services.

### Key-Value (KV)

Key-Value (KV) is a way of storing information by associating values with unique keys, allowing quick data retrieval. TiDB uses TiKV to map tables and indexes into key-value pairs, enabling efficient data storage and access across the database.

## L

### Leader/Follower/Learner

Leader/Follower/Learner each corresponds to a role in a Raft group of [peers](#regionpeerraft-group). The leader services all client requests and replicates data to the followers. If the group leader fails, one of the followers will be elected as the new leader. Learners are non-voting followers that only serves in the process of replica addition.

### Lightweight Directory Access Protocol (LDAP)

Lightweight Directory Access Protocol (LDAP) is a standardized way of accessing a directory with information. It is commonly used for account and user data management. TiDB supports LDAP via [LDAP authentication plugins](/security-compatibility-with-mysql.md#authentication-plugin-status).

### Long Term Support (LTS)

Long Term Support (LTS) refers to software versions that are extensively tested and maintained for extended periods. For more information, see [TiDB Versioning](/releases/versioning.md).

## M

### Massively Parallel Processing (MPP)

Starting from v5.0, TiDB introduces Massively Parallel Processing (MPP) architecture through TiFlash nodes, which shares the execution workloads of large join queries among TiFlash nodes. When the MPP mode is enabled, TiDB, based on cost, determines whether to use the MPP framework to perform the calculation. In the MPP mode, the join keys are redistributed through the Exchange operation while being calculated, which distributes the calculation pressure to each TiFlash node and speeds up the calculation. For more information, see [Use TiFlash MPP Mode](/tiflash/use-tiflash-mpp-mode.md).

### Multi-version concurrency control (MVCC)

[MVCC](https://en.wikipedia.org/wiki/Multiversion_concurrency_control) is a concurrency control mechanism in TiDB and other databases. It processes the memory read by transactions to achieve concurrent access to TiDB, thereby avoiding blocking caused by conflicts between concurrent reads and writes.

## O

### Old value

The "original value" in the incremental change log output by TiCDC. You can specify whether the incremental change log output by TiCDC contains the "original value".

### Online Analytical Processing (OLAP)

Online Analytical Processing (OLAP) refers to database workloads focused on analytical tasks, such as data reporting and complex queries. OLAP is characterized by read-heavy queries that process large volumes of data across many rows.

### Online Transaction Processing (OLTP)

Online Transaction Processing (OLTP) refers to database workloads focused on transactional tasks, such as selecting, inserting, updating, and deleting small sets of records.

### Out of Memory (OOM)

Out of Memory (OOM) is a situation where a system fails due to insufficient memory. For more information, see [Troubleshoot TiDB OOM Issues](/troubleshoot-tidb-oom.md).

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

## P

### Partitioning

[Partitioning](/partitioned-table.md) refers to physically dividing a table into smaller table partitions, which can be done by partition methods such as RANGE, LIST, HASH, and KEY partitioning.

### Pending/Down

"Pending" and "down" are two special states of a peer. Pending indicates that the Raft log of followers or learners is vastly different from that of leader. Followers in pending cannot be elected as leader. "Down" refers to a state that a peer ceases to respond to leader for a long time, which usually means the corresponding node is down or isolated from the network.

### Placement Driver (PD)

Placement Driver (PD) is a core component in the [TiDB Architecture](/tidb-architecture.md#placement-driver-pd-server) responsible for storing metadata, assigning [Timestamp Oracle (TSO)](/tso.md) for transaction timestamps, orchestrating data placement on TiKV, and running [TiDB Dashboard](/dashboard/dashboard-overview.md). For more information, see [TiDB Scheduling](/tidb-scheduling.md).

### Point Get

Point get means reading a single row of data by a unique index or primary index, the returned resultset is up to one row.

### Point in Time Recovery (PITR)

Point in Time Recovery (PITR) enables you to restore data to a specific point in time (for example, just before an unintended `DELETE` statement). For more information, see [TiDB Log Backup and PITR Architecture](/br/br-log-architecture.md).

### Predicate columns

In most cases, when executing SQL statements, the optimizer only uses statistics of some columns (such as columns in the `WHERE`, `JOIN`, `ORDER BY`, and `GROUP BY` statements). These used columns are called predicate columns. For details, see [Collect statistics on some columns](/statistics.md#collect-statistics-on-some-columns).

## Q

### Queries Per Second (QPS)

Queries Per Second (QPS) is the number of queries a database service handles per second, serving as a key performance metric for database throughput.

### Quota Limiter

Quota Limiter is an experimental feature introduced in TiDB v6.0.0. If the machine on which TiKV is deployed has limited resources, for example, with only 4v CPU and 16 G memory, and the foreground of TiKV processes too many read and write requests, the CPU resources used by the background are occupied to help process such requests, which affects the performance stability of TiKV. To avoid this situation, the [quota-related configuration items](/tikv-configuration-file.md#quota) can be set to limit the CPU resources to be used by the foreground.

## R

### Raft Engine

Raft Engine is an embedded persistent storage engine with a log-structured design. It is built for TiKV to store multi-Raft logs. Since v5.4, TiDB supports using Raft Engine as the log storage engine. For details, see [Raft Engine](/tikv-configuration-file.md#raft-engine).

### Region Split

A region in a TiKV cluster is not divided at the beginning but is gradually split as data is written to it. The process is called Region split.

The mechanism of Region split is to use one initial Region to cover the entire key space, and generate new Regions through splitting existing ones every time the size of the Region or the number of keys has reached a threshold.

### Region/Peer/Raft Group

Region is the minimal piece of data storage in TiKV, each representing a range of data (256 MiB by default). Each Region has three replicas by default. A replica of a Region is called a peer. Multiple peers of the same Region replicate data via the Raft consensus algorithm, so peers are also members of a Raft instance. TiKV uses Multi-Raft to manage data. That is, for each Region, there is a corresponding, isolated Raft group.

### Remote Procedure Call (RPC)

Remote Procedure Call (RPC) is a communication way between software components. In a TiDB cluster, the gRPC standard is used for communication between different components such as TiDB, TiKV, and TiFlash.

### Request Unit (RU)

Request Unit (RU) is a unified abstraction unit for the resource usage in TiDB. It is used with [Resource Control](/tidb-resource-control.md) to manage resource usage.

### Restore

Restore is the reverse of the backup operation. It is the process of bringing back the system to an earlier state by retrieving data from a prepared backup.

## S

### Scheduler

Schedulers are components in PD that generate scheduling tasks. Each scheduler in PD runs independently and serves different purposes. The commonly used schedulers are:

- `balance-leader-scheduler`: Balances the distribution of leaders
- `balance-region-scheduler`: Balances the distribution of peers
- `hot-region-scheduler`: Balances the distribution of hot Regions
- `evict-leader-{store-id}`: Evicts all leaders of a node (often used for rolling upgrades)

### Static Sorted Table / Sorted String Table (SST)

Static Sorted Table or Sorted String Table is a file storage format used in RocksDB (a storage engine used by [TiKV](/storage-engine/rocksdb-overview.md)).

### Store

A store refers to the storage node in the TiKV cluster (an instance of `tikv-server`). Each store has a corresponding TiKV instance.

## T

### Timestamp Oracle (TSO)

Because TiKV is a distributed storage system, it requires a global timing service, Timestamp Oracle (TSO), to assign a monotonically increasing timestamp. In TiKV, such a feature is provided by PD, and in Google [Spanner](http://static.googleusercontent.com/media/research.google.com/en//archive/spanner-osdi2012.pdf), this feature is provided by multiple atomic clocks and GPS. For details, see [TSO](/tso.md).

### Top SQL

Top SQL helps locate SQL queries that contribute to a high load of a TiDB or TiKV node in a specified time range. For details, see [Top SQL user document](/dashboard/top-sql.md).

### Transactions Per Second (TPS)

Transactions Per Second (TPS) is the number of transactions a database processes per second, serving as a key metric for measuring database performance and throughput.

## U

### Uniform Resource Identifier (URI)

Uniform Resource Identifier (URI) is a standardized format for identifying a resource. For more information, see [Uniform Resource Identifier](https://en.wikipedia.org/wiki/Uniform_Resource_Identifier) on Wikipedia.

### Universally Unique Identifier (UUID)

Universally Unique Identifier (UUID) is a 128-bit (16-byte) generated ID used to uniquely identify records in a database. For more information, see [UUID](/best-practices/uuid.md).
