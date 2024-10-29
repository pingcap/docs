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

- **Isolation** means that a transaction in process is invisible to other transactions until it completes. This allows concurrent transactions to read and write data without sacrificing consistency. For more information, see [TiDB transaction isolation levels](/transaction-isolation-levels.md#tidb-transaction-isolation-levels).

- **Durability** means that once a transaction is committed, it remains committed even in the event of a system failure. TiKV uses persistent storage to ensure durability.

## B

### Batch Create Table

Batch Create Table is a feature introduced in TiDB v6.0.0. This feature is enabled default. When restoring data with a large number of tables (nearly 50000) using BR (Backup & Restore), the feature can greatly speed up the restore process by creating tables in batches. For details, see [Batch Create Table](/br/br-batch-create-table.md).

### Baseline Capturing

Baseline Capturing captures queries that meet capturing conditions and create bindings for them. It is used for [preventing regression of execution plans during an upgrade](/sql-plan-management.md#prevent-regression-of-execution-plans-during-an-upgrade).

### BR

BR is the Backup and Restore tool for TiDB. See [BR Overview](/br/backup-and-restore-overview.md) for more information.

### Bucket

A [Region](#regionpeerraft-group) is logically divided into several small ranges called bucket. TiKV collects query statistics by buckets and reports the bucket status to PD. For details, see the [Bucket design doc](https://github.com/tikv/rfcs/blob/master/text/0082-dynamic-size-region.md#bucket).

## C

### Cached Table

With the cached table feature, TiDB loads the data of an entire table into the memory of the TiDB server, and TiDB directly gets the table data from the memory without accessing TiKV, which improves the read performance.

### CF

CF is short for Column Family as used by RocksDB / TiKV.

### Coalesce Partition

Coalesce Partition is a way of decreasing the number of partitions in a Hash or Key partitioned table. For more information, see [Manage Hash and Key partitions](/partitioned-table.md#manage-hash-and-key-partitions).

### Continuous Profiling

Introduced in TiDB 5.3.0, Continuous Profiling is a way to observe resource overhead at the system call level. With the support of Continuous Profiling, TiDB provides performance insight as clear as directly looking into the database source code, and helps R&D and operation and maintenance personnel to locate the root cause of performance problems using a flame graph. For details, see [TiDB Dashboard Instance Profiling - Continuous Profiling](/dashboard/continuous-profiling.md).

### CTE

A Common Table Expression (CTE) is part of the SQL standard and uses [`WITH`](/sql-statements/sql-statement-with.md) statements.

## D

### DDL

Data Definition Language (DDL) is the part of the SQL standard that deals with creating, modifying and deleting tables, indexes, columns and other objects.

### DM

Data Migration is the tool that allows MySQL to TiDB migration by reading data from a source instance and applying it to a target MySQL instance. See [DM Overview](/dm/dm-overview.md) for more information.

### DML

Data Modification Language (DML) is the part of the SQL standard that deals with inserting, updating and deleting rows in tables.

### DMR

Development Milestone Release (DMR) is a version of TiDB that provides users with the latest features but doesn't provide long term support. See [TiDB Versioning](/releases/versioning.md) for more information.

### DR

Disaster Recovery (DR) describes solutions that can be used to recover from a disaster in the future. This includes things like backups and standby clusters.

### DXF

Distributed eXecution Framework (DXF) is the framework used by TiDB to speedup index creation and data import by distributing tasks over all available resources. See [DXF Introduction](/tidb-distributed-execution-framework.md) for more details

### Dynamic Pruning

Dynamic pruning mode is one of the modes that TiDB accesses partitioned tables. In dynamic pruning mode, each operator supports direct access to multiple partitions. Therefore, TiDB no longer uses Union. Omitting the Union operation can improve the execution efficiency and avoid the problem of Union concurrent execution.

## E

### EC2

Elastic Compute Cloud (EC2) is an AWS service that provides compute resources. This can be used with TiUP to run a TiDB Cluster.

## G

### GA

General Available (GA) is the first non-beta version of a software product.

### GC

Garbage Collection (GC) is the process to cleanup unused resources. See [GC](/garbage-collection-overview.md) for the GC process of TiKV.

### GTID

Global Transactions ID's (GTIDs) are used by recent MySQL versions binary log to indicate what transactions have been replicated and which have not. This information can be used by DM.

## H

### HTAP

Hybrid Transactional Analytical Process (HTAP) is a database feature that allows both OLTP and OLAP workloads on the same database. For TiDB the HTAP feature is provided by using both TiKV for row storage and TiFlash for columnar storage. See [the definition of HTAP on the Gartner website](https://www.gartner.com/en/information-technology/glossary/htap-enabling-memory-computing-technologies) for more information.

## I

### IMDS

Instance Metadata Service (IMDS) is a AWS service that can be used to manage EC2 instances. See [Instance metadata](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html) for more information.

### Index Merge

Index Merge is a method introduced in TiDB v4.0 to access tables. Using this method, the TiDB optimizer can use multiple indexes per table and merge the results returned by each index. In some scenarios, this method makes the query more efficient by avoiding full table scans. Since v5.4, Index Merge has become a GA feature.

### In-Memory Pessimistic Lock

The in-memory pessimistic lock is a new feature introduced in TiDB v6.0.0. When this feature is enabled, pessimistic locks are usually stored in the memory of the Region leader only, and are not persisted to disk or replicated through Raft to other replicas. This feature can greatly reduce the overhead of acquiring pessimistic locks and improve the throughput of pessimistic transactions.

## K

### KMS

Key Management Service (KMS) allows the storage and retrieval of secret keys in a secure way. Examples of this are the AWS KMS, GCP KMS and HashiCorp Vault. Various TiDB components can use this to manage the keys that are used for storage encryption and related services.

### KV

Key-Value (KV) is a way storing information that allows easy store and retrieval by specifying the key. Multiple values can be stored under a single key by encoding them. TiKV is implementing this by TiDB mapping tables and indexes into Key-Value entries.

## L

### LDAP

Lightweight Directory Access Protocol (LDAP) is a standardized way of accessing a directory with information. This is often used to store information on accounts. This is used in TiDB by [LDAP authentication plugins](/security-compatibility-with-mysql.md#authentication-plugin-status).

### LTS

Long Term Support (LTS) are software versions that are well tested, production ready and are supported for a long term. See [TiDB Versioning](/releases/versioning.md) for more details.

### leader/follower/learner

Leader/Follower/Learner each corresponds to a role in a Raft group of [peers](#regionpeerraft-group). The leader services all client requests and replicates data to the followers. If the group leader fails, one of the followers will be elected as the new leader. Learners are non-voting followers that only serves in the process of replica addition.

## M

### MPP

Starting from v5.0, TiDB introduces Massively Parallel Processing (MPP) architecture through TiFlash nodes, which shares the execution workloads of large join queries among TiFlash nodes. When the MPP mode is enabled, TiDB, based on cost, determines whether to use the MPP framework to perform the calculation. In the MPP mode, the join keys are redistributed through the Exchange operation while being calculated, which distributes the calculation pressure to each TiFlash node and speeds up the calculation. For more information, see [Use TiFlash MPP Mode](/tiflash/use-tiflash-mpp-mode.md).

### Multi-version concurrency control (MVCC)

[MVCC](https://en.wikipedia.org/wiki/Multiversion_concurrency_control) is a concurrency control mechanism in TiDB and other databases. It processes the memory read by transactions to achieve concurrent access to TiDB, thereby avoiding blocking caused by conflicts between concurrent reads and writes.

## O

### OLAP

OnLine Analytical Processing (OLAP) are describing database workloads that mostly deal with analytical workloads like reporting. The characteristics of this is read heavy queries that process many rows.

### Old value

The "original value" in the incremental change log output by TiCDC. You can specify whether the incremental change log output by TiCDC contains the "original value".

### OLTP

OnLine Transaction Processing (OLTP) are describing database workloads that mostly deal with transactional workloads like selecting, inserting, updating and deleting small sets of records.

## OOM

Out of Memory (OOM) is a situation where a system fails due to a a lack of available memory. See [Troubleshoot TiDB OOM Issues](/troubleshoot-tidb-oom.md) for more details.

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

### PD

Placement Driver (PD) is an important component of the [TiDB Architecture](/tidb-architecture.md#placement-driver-pd-server) that is responsible to store metadata and run the [TSO](/tso.md) that hands out timestamps that are used for transactions. It also orchestrates the data placement on TiKV and runs the [TiDB Dashboard](/dashboard/dashboard-overview.md).

### pending/down

"Pending" and "down" are two special states of a peer. Pending indicates that the Raft log of followers or learners is vastly different from that of leader. Followers in pending cannot be elected as leader. "Down" refers to a state that a peer ceases to respond to leader for a long time, which usually means the corresponding node is down or isolated from the network.

### PiTR

Point in Time Recovery (PiTR) is a database feature that allows the user to restore to a specific point in time (for example just before an accidental `DELETE` statement). See [TiDB Log Backup and PITR Architecture](/br/br-log-architecture.md) for more details.

### Point Get

Point get means reading a single row of data by a unique index or primary index, the returned resultset is up to one row.

### Predicate columns

In most cases, when executing SQL statements, the optimizer only uses statistics of some columns (such as columns in the `WHERE`, `JOIN`, `ORDER BY`, and `GROUP BY` statements). These used columns are called predicate columns. For details, see [Collect statistics on some columns](/statistics.md#collect-statistics-on-some-columns).

## Q

### QPS

Queries Per Second (QPS) is a performance metric of a database service.

### Quota Limiter

Quota Limiter is an experimental feature introduced in TiDB v6.0.0. If the machine on which TiKV is deployed has limited resources, for example, with only 4v CPU and 16 G memory, and the foreground of TiKV processes too many read and write requests, the CPU resources used by the background are occupied to help process such requests, which affects the performance stability of TiKV. To avoid this situation, the [quota-related configuration items](/tikv-configuration-file.md#quota) can be set to limit the CPU resources to be used by the foreground.

## R

### Raft Engine

Raft Engine is an embedded persistent storage engine with a log-structured design. It is built for TiKV to store multi-Raft logs. Since v5.4, TiDB supports using Raft Engine as the log storage engine. For details, see [Raft Engine](/tikv-configuration-file.md#raft-engine).

### RAG

Retrieval-Augmented Generation (RAG). See [Vector Search Overview](/vector-search-overview.md#use-cases) for more details.

### Region/peer/Raft group

Region is the minimal piece of data storage in TiKV, each representing a range of data (256 MiB by default). Each Region has three replicas by default. A replica of a Region is called a peer. Multiple peers of the same Region replicate data via the Raft consensus algorithm, so peers are also members of a Raft instance. TiKV uses Multi-Raft to manage data. That is, for each Region, there is a corresponding, isolated Raft group.

### Region split

Regions are generated as data writes increase. The process of splitting is called Region split.

The mechanism of Region split is to use one initial Region to cover the entire key space, and generate new Regions through splitting existing ones every time the size of the Region or the number of keys has reached a threshold.

### Restore

Restore is the reverse of the backup operation. It is the process of bringing back the system to an earlier state by retrieving data from a prepared backup.

### RPC

Remote Procedure Call (RPC) is a way for software components to communicate. In a TiDB cluster gRPC standard is used for communication between different components such as TiDB, TiKV and TiFlash.

### RU

Request Unit (RU) is used in TiDB to describe the unit for the resource usage. This is used with [Resource Control](/tidb-resource-control.md) to manage resource usage.

## S

### scheduler

Schedulers are components in PD that generate scheduling tasks. Each scheduler in PD runs independently and serves different purposes. The commonly used schedulers are:

- `balance-leader-scheduler`: Balances the distribution of leaders
- `balance-region-scheduler`: Balances the distribution of peers
- `hot-region-scheduler`: Balances the distribution of hot Regions
- `evict-leader-{store-id}`: Evicts all leaders of a node (often used for rolling upgrades)

### SST

Static Sorted Table, Sorted String Table or Sorted Sequence Table (SST) is the file storage format of RocksDB.

### Store

A store refers to the storage node in the TiKV cluster (an instance of `tikv-server`). Each store has a corresponding TiKV instance.

## T

### Top SQL

Top SQL helps locate SQL queries that contribute to a high load of a TiDB or TiKV node in a specified time range. For details, see [Top SQL user document](/dashboard/top-sql.md).

### TPS

Transactions Per Second (TPS) is a performance metric of a database.

### TSO

Because TiKV is a distributed storage system, it requires a global timing service, Timestamp Oracle (TSO), to assign a monotonically increasing timestamp. In TiKV, such a feature is provided by PD, and in Google [Spanner](http://static.googleusercontent.com/media/research.google.com/en//archive/spanner-osdi2012.pdf), this feature is provided by multiple atomic clocks and GPS. For details, see [TSO](/tso.md).

## U

### URI

Uniform Resource Identifier (URI) is a uniform way of describing a resource. See [Uniform Resource Identifier](https://en.wikipedia.org/wiki/Uniform_Resource_Identifier) on Wikipedia for more information.

### UUID

Universally Unique Identifier (UUID) is a 128-bit (16 byte) generated ID that can be used to identify records in a database. See [UUID](/best-practices/uuid.md) for more information on how UUID's are used in TiDB.