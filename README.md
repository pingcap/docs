# TiDB Documentation

## Documentation List

+ About TiDB
  - [TiDB Introduction](overview.md#tidb-introduction)
  - [TiDB Architecture](overview.md#tidb-architecture)
- [TiDB Quick Start Guide](QUICKSTART.md)
+ TiDB User Guide
  + TiDB Server Administration
    - [The TiDB Server](sql/tidb-server.md)
    - [The TiDB Command Options](sql/server-command-option.md)
    - [The TiDB Data Directory](sql/tidb-server.md#tidb-data-directory)
    - [The TiDB System Database](sql/system-database.md)
    - [The TiDB System Variables](sql/variable.md)
    - [The Proprietary System Variables and Syntax in TiDB](sql/tidb-specific.md)
    - [The TiDB Server Logs](sql/tidb-server.md#tidb-server-logs)
    - [The TiDB Access Privilege System](sql/privilege.md)
    - [TiDB User Account Management](sql/user-account-management.md)
    - [Use Encrypted Connections](sql/encrypted-connections.md)
  + SQL Optimization
    - [Understand the Query Execution Plan](sql/understanding-the-query-execution-plan.md)
    - [Introduction to Statistics](sql/statistics.md)
  + Language Structure
    - [Literal Values](sql/literal-values.md)
    - [Schema Object Names](sql/schema-object-names.md)
    - [Keywords and Reserved Words](sql/keywords-and-reserved-words.md)
    - [User-Defined Variables](sql/user-defined-variables.md)
    - [Expression Syntax](sql/expression-syntax.md)
    - [Comment Syntax](sql/comment-syntax.md)
  + Globalization
    - [Character Set Support](sql/character-set-support.md)
    - [Character Set Configuration](sql/character-set-configuration.md)
    - [Time Zone](sql/time-zone.md)
  + Data Types
    - [Numeric Types](sql/datatype.md#numeric-types)
    - [Date and Time Types](sql/datatype.md#date-and-time-types)
    - [String Types](sql/datatype.md#string-types)
    - [JSON Types](sql/datatype.md#json-types)
    - [The ENUM data type](sql/datatype.md#the-enum-data-type)
    - [The SET Type](sql/datatype.md#the-set-type)
    - [Data Type Default Values](sql/datatype.md#data-type-default-values)
  + Functions and Operators
    - [Function and Operator Reference](sql/functions-and-operators-reference.md)
    - [Type Conversion in Expression Evaluation](sql/type-conversion-in-expression-evaluation.md)
    - [Operators](sql/operators.md)
    - [Control Flow Functions](sql/control-flow-functions.md)
    - [String Functions](sql/string-functions.md)
    - [Numeric Functions and Operators](sql/numeric-functions-and-operators.md)
    - [Date and Time Functions](sql/date-and-time-functions.md)
    - [Bit Functions and Operators](sql/bit-functions-and-operators.md)
    - [Cast Functions and Operators](sql/cast-functions-and-operators.md)
    - [Encryption and Compression Functions](sql/encryption-and-compression-functions.md)
    - [Information Functions](sql/information-functions.md)
    - [JSON Functions](sql/json-functions.md)
    - [Aggregate (GROUP BY) Functions](sql/aggregate-group-by-functions.md)
    - [Miscellaneous Functions](sql/miscellaneous-functions.md)
    - [Precision Math](sql/precision-math.md)
  + SQL Statement Syntax
    - [Data Definition Statements](sql/ddl.md)
    - [Data Manipulation Statements](sql/dml.md)
    - [Transactions](sql/transaction.md)
    - [Database Administration Statements](sql/admin.md)
    - [Prepared SQL Statement Syntax](sql/prepare.md)
    - [Utility Statements](sql/util.md)
    - [TiDB SQL Syntax Diagram](https://pingcap.github.io/sqlgram/)
  - [JSON Functions and Generated Column](sql/json-functions-generated-column.md)
  - [Connectors and APIs](sql/connection-and-APIs.md)
  - [Error Codes and Troubleshooting](sql/error.md)
  - [Compatibility with MySQL](sql/mysql-compatibility.md)
  + Advanced Usage
    - [Read Data From History Versions](op-guide/history-read.md)
+ TiDB Operations Guide
  - [Hardware and Software Requirements](op-guide/recommendation.md)
  + Deploy
    - [Ansible Deployment (Recommended)](op-guide/ansible-deployment.md)
    - [Docker Deployment](op-guide/docker-deployment.md)
    - [Cross-Region Deployment](op-guide/location-awareness.md)
  - [Configure](op-guide/configuration.md)
  + Monitor
    - [Overview of the Monitoring Framework](op-guide/monitor-overview.md)
    - [Key Metrics](op-guide/dashboard-overview-info.md)
    - [Monitor a TiDB Cluster](op-guide/monitoring-tidb.md)
  + Scale
    - [Scale a TiDB Cluster](op-guide/horizontal-scale.md)
    - [Use Ansible to Scale](QUICKSTART.md#scale-the-tidb-cluster)
  - [Upgrade](op-guide/ansible-deployment.md#perform-rolling-update)
  - [Tune Performance](op-guide/tune-TiKV.md)
  + Backup and Migrate
    - [Backup and Restore](op-guide/backup-restore.md)
    + Migrate
      - [Migration Overview](op-guide/migration-overview.md)
      - [Migrate All the Data](op-guide/migration.md#using-the-mydumper--loader-tool-to-export-and-import-all-the-data)
      - [Migrate the Data Incrementally](op-guide/migration.md#optional-using-the-syncer-tool-to-import-data-incrementally)
  - [Deploy TiDB Using the Binary](op-guide/binary-deployment.md)
  - [Troubleshoot](trouble-shooting.md)
+ TiDB Utilities
  - [Syncer User Guide](tools/syncer.md)
  - [Loader User Guide](tools/loader.md)
  - [TiDB-Binlog User Guide](tools/tidb-binlog.md)
  - [PD Control User Guide](tools/pd-control.md)
+ The TiDB Connector for Spark
  - [Quick Start Guide](tispark/tispark-quick-start-guide.md)
  - [User Guide](tispark/tispark-user-guide.md)
- [Frequently Asked Questions (FAQ)](FAQ.md)
- [TiDB Best Practices](https://pingcap.github.io/blog/2017/07/24/tidbbestpractice/)
- [Releases](release/rn.md)
- [TiDB Roadmap](https://github.com/pingcap/docs/blob/master/ROADMAP.md)
- [Connect with Us](community.md)
+ More Resources
  - [Frequently Used Tools](https://github.com/pingcap/tidb-tools)
  - [PingCAP Blog](https://pingcap.com/blog/)
  - [Weekly Update](https://pingcap.com/weekly/)

## TiDB Introduction

TiDB (The pronunciation is: /'taɪdiːbi:/ tai-D-B, etymology: titanium) is a Hybrid Transactional/Analytical Processing (HTAP) database. Inspired by the design of Google F1 and Google Spanner, TiDB features infinite horizontal scalability, strong consistency, and high availability. The goal of TiDB is to serve as a one-stop solution for online transactions and analyses.

- __Horizontal scalability__
- __Compatible with MySQL protocol__
- __Automatic Failover and high availability__
- __Consistent distributed transactions__
- __Online DDL__
- __Multiple storage engine support__


Read the following three articles to understand TiDB techniques:

- [Data Storage](https://pingcap.github.io/blog/2017/07/11/tidbinternal1/)
- [Computing](https://pingcap.github.io/blog/2017/07/11/tidbinternal2/)
- [Scheduling](https://pingcap.github.io/blog/2017/07/20/tidbinternal3/)

## Roadmap

Read the [Roadmap](https://github.com/pingcap/docs/blob/master/ROADMAP.md).

## Connect with us

- **Twitter**: [@PingCAP](https://twitter.com/PingCAP)
- **Reddit**: https://www.reddit.com/r/TiDB/
- **Stack Overflow**: https://stackoverflow.com/questions/tagged/tidb
- **Mailing list**: [Google Group](https://groups.google.com/forum/#!forum/tidb-user)

## TiDB Architecture

To better understand TiDB’s features, you need to understand the TiDB architecture.

![image alt text](media/tidb-architecture.png)

The TiDB cluster has three components: the TiDB Server, the PD Server,  and the TiKV server.

### TiDB Server

The TiDB server is in charge of the following operations:

1. Receiving the SQL requests

2. Processing the SQL related logics

3. Locating the TiKV address for storing and computing data through the Placement Driver (PD)

4. Exchanging data with TiKV

5. Returning the result

The TiDB server is stateless. It doesn’t store data and it is for computing only. TiDB is horizontally scalable and provides the unified interface to the outside through the load balancing components such as Linux Virtual Server (LVS), HAProxy, or F5.

### Placement Driver Server

Placement Driver (PD) is the managing component of the entire cluster and is in charge of the following three operations:

1. Storing the metadata of the cluster such as the region location of a specific key.

2. Scheduling and load balancing regions in the TiKV cluster, including but not limited to data migration and Raft group leader transfer.

3. Allocating the transaction ID that is globally unique and monotonic increasing.

As a cluster, PD needs to be deployed to an odd number of nodes. Usually it is recommended to deploy to 3 online nodes at least.

### TiKV Server

TiKV server is responsible for storing data. From an external view, TiKV is a distributed transactional Key-Value storage engine. Region is the basic unit to store data. Each Region stores the data for a particular Key Range which is a left-closed and right-open interval from StartKey to EndKey. There are multiple Regions in each TiKV node. TiKV uses the Raft protocol for replication to ensure the data consistency and disaster recovery. The replicas of the same Region on different nodes compose a Raft Group. The load balancing of the data among different TiKV nodes are scheduled by PD. Region is also the basic unit for scheduling the load balance.

## Features

### Horizontal Scalability

Horizontal scalability is the most important feature of TiDB. The scalability includes two aspects: the computing capability and the storage capacity. The TiDB server processes the SQL requests. As the business grows, the overall processing capability and higher throughput can be achieved by simply adding more TiDB server nodes. Data is stored in TiKV. As the size of the data grows, the scalability of data can be resolved by adding more TiKV server nodes. PD schedules data in Regions among the TiKV nodes and migrates part of the data to the newly added node. So in the early stage, you can deploy only a few service instances. For example, it is recommended to deploy at least 3 TiKV nodes, 3 PD nodes and 2 TiDB nodes. As business grows, more TiDB and TiKV instances can be added on-demand.

### High availability

High availability is another important feature of TiDB. All of the three components, TiDB, TiKV and PD, can tolerate the failure of some instances without impacting the availability of the entire cluster. For each component, See the following for more details about the availability, the consequence of a single instance failure and how to recover.

#### TiDB

TiDB is stateless and it is recommended to deploy at least two instances. The front-end provides services to the outside through the load balancing components. If one of the instances is down, the Session on the instance will be impacted. From the application’s point of view, it is a single request failure but the service can be regained by reconnecting to the TiDB server. If a single instance is down, the service can be recovered by restarting the instance or by deploying a new one.

#### PD

PD is a cluster and the data consistency is ensured using the Raft protocol. If an instance is down but the instance is not a Raft Leader, there is no impact on the service at all. If the instance is a Raft Leader, a new Leader will be elected to recover the service. During the election which is approximately 3 seconds, PD cannot provide service. It is recommended to deploy three instances. If one of the instances is down, the service can be recovered by restarting the instance or by deploying a new one.

#### TiKV

TiKV is a cluster and the data consistency is ensured using the Raft protocol. The number of the replicas can be configurable and the default is 3 replicas. The load of TiKV servers are balanced through PD. If one of the node is down, all the Regions in the node will be impacted. If the failed node is the Leader of the Region, the service will be interrupted and a new election will be initiated. If the failed node is a Follower of the Region, the service will not be impacted. If a TiKV node is down for a period of time (the default value is 10 minutes), PD will move the data to another TiKV node.
