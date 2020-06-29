---
title: TiDB Monitoring Metrics
summary: Learn some key metrics displayed on the Grafana TiDB dashboard.
category: reference
aliases: ['/docs/dev/grafana-tidb-dashboard/','/docs/dev/reference/key-monitoring-metrics/tidb-dashboard/']
---

# TiDB Monitoring Metrics

When deploying a TiDB cluster using TiDB Ansible or TiUP, a one-click deployment monitoring system (Prometheus & Grafana) is used. For the monitoring architecture, see [TiDB Monitoring Framework Overview](/tidb-monitoring-framework.md).

The Grafana dashboard is divided into a series of sub dashboards which include Overview, PD, TiDB, TiKV, Node\_exporter, Disk Performance, and so on. The TiDB dashboard consists of the TiDB panel and the TiDB Summary panel. The differences between the two panels are as follows:

- TiDB Panel: provide as comprehensive information as possible for troubleshooting cluster abnormalities.
- TiDB Summary Panel: extract the parts of the TiDB panel that the user is most concerned about and make some modifications. It is mainly used to provide data (such as QPS, TPS, response delay) that users care about in the daily operation of the database, so as to be used as monitoring information for external display and reporting.

This document describes some key monitoring metrics displayed on the TiDB dashboard.

## Key metrics description

To understand the key metrics displayed on the TiDB dashboard, check the following list:

- Query Summary
    - Duration: execution time
        - The time when the client's network request is sent to TiDB and returned to the client after TiDB is executed. In general, client requests are sent in the form of SQL statements, but can also include the execution time of commands such as `COM_PING`, `COM_SLEEP`, `COM_STMT_FETCH`, `COM_SEND_LONG_DATA`
        - Since TiDB supports Multi-Query, it can accept multiple SQL statements sent by the client at one time, such as `select 1; select 1; select 1;`. At this time, the statistical execution time is the total time after the execution of all SQL statements
    - QPS: the number of SQL statements executed per second on all TiDB instances. According to the success or failure of the execution result (OK/Error) to distinguish.
    - Statement OPS: the number of different types of SQL statements executed per second. According to `SELECT`, `INSERT`, `UPDATE` and other types of statistics
    - QPS By Instance: the QPS on each TiDB instance, which is classified according to the success or failure of command execution results
    - Failed Query OPM: the statistics of error types (such as syntax errors and primary key conflicts) according to the errors happening when executing SQL statements per second on each TiDB instance. It contains the module to which the error belongs and the error code
    - Slow query: the statistics of the processing time of slow queries (the time cost of the entire slow query, the time cost of Coprocessor，and the waiting time for Coprocessor scheduling)
    - 999/99/95/80 Duration: the statistics of the execution time for different types of SQL statements (different percentiles)

- Query Detail
    - Duration 80/95/99/999 By Instance: the statistics of the execution time for SQL statements on each TiDB instance (different percentiles)
    - Failed Query OPM Detail: the statistics of error types (such as syntax errors and primary key conflicts) according to the errors happening when executing SQL statements on each TiDB instance
    - Internal SQL OPS: the QPS executed by internal SQL statements in the entire TiDB cluster. Internal SQL statements are automatically executed SQL statements within TiDB. It is generally triggered by user SQL statements or internally scheduled tasks.

- Server
    - Uptime: the runtime of each TiDB instance
    - Memory Usage: the memory usage statistics of each TiDB instance are divided into the memory occupied by the process and the memory applied by Golang on the heap
    - CPU Usage: the statistics of CPU usage for each TiDB instance
    - Connection Count: the number of clients connected to each TiDB instance
    - Open FD Count: the statistics of opened file descriptors on each TiDB instance
    - Goroutine Count: the number of Goroutines on each TiDB instance
    - Go GC Duration: Golang GC time on each TiDB instance
    - Go Threads: the number of threads on each TiDB instance
    - Go GC Count: the number of times that Golang GC is executed on each TiDB instance
    - Go GC CPU Usage: the statistics of CPU used by Golang GC for each TiDB instance
    - Events OPM: the statistics of key events, such as "start", "close", "graceful-shutdown","kill", "hang", and so on
    - Keep Alive OPM: the number of times that the metrics are refreshed every minute on each TiDB instance. It usually needs no attention.
    - Prepare Statement Count: the number of `Prepare` statements that are executed on each TiDB instance and the total count of them
    - Time Jump Back OPS: the number of times that the time of operating system rewinds every second on each TiDB instance
    - Write Binlog Error：the number of times that binlog failed to write every second on each TiDB instance
    - Handshake Error OPS: the number of times that a handshake error occurs every second on each TiDB instance
    - Get Token Duration: the time cost of getting Token on each connection

- Transaction
    - Transaction OPS: the number of transactions executed per second
    - Duration: the execution time of a transaction
    - Transaction Statement Num: the number of SQL statements in a transaction
    - Transaction Retry Num: the number of times that a transaction retries
    - Session Retry Error OPS: the number of errors encountered during the transaction retry per second
    - KV Transaction OPS: the number of transactions executed per second within each TiDB
        - A user's transaction may trigger multiple transaction executions within TiDB, including internal metadata reading, user transaction atomic retry execution, and so on
        - TiDB's internal scheduled tasks will also operate the database through transactions, this part is also included in this panel
    - KV Transaction Duration: the time spent on executing transactions within each TiDB
    - Commit Token Wait Duration: the flow control queue takes time to wait when the transaction is committed. When there is a long wait, it means that the committed transaction is too large and is limiting the current. If the system still has resources available, you can speed up the committing by increasing the `committer-concurrency` in the TiDB configuration file
    - Transaction Max Write KV Num: the maximum number of key-value pairs written by a single transaction
    - Transaction Max Write Size Bytes: the maximum key-value pair size written by a single transaction
    - Transaction Regions Num 90: 90% of the number of Regions written by a single transaction
    - Send HeartBeat Duration: the interval between transactions sending heartbeats
    - TTL Lifetime Reach Counter: the TTL of the transaction reached the upper limit. The default value of the upper limit of TTL is 10 minutes. It means that the first lock of a pessimistic transaction or the first prewrite of an optimistic transaction exceeds 10 minutes. The default value of the upper limit of TTL is 10 minutes. The upper limit of TTL life can be changed by modifying `max-txn-TTL` in the TiDB configuration file
    - Statement Lock Keys: the number of locks for a single statement
    - Acquire Pessimistic Locks Duration: the time consumed by locking
    - Pessimistic Statement Retry OPS: the number of retry attempts for pessimistic statements. When the statement tries to lock, it may encounter a write conflict error. At this time, the statement will reacquire a new snapshot and lock again
    - Load Safepoint OPS: the number of times that `Safepoint` loads. The function of `Safepoint` is to ensure that the data before `Safepoint` is not read when the transaction reads data, so as to ensure the safety of the data. Because the data before `Safepoint` may be cleaned up by the GC

- Executor
    - Parse Duration: the statistics of the parsing time of SQL statements
    - Compile Duration: the statistics of the time of compiling the parsed SQL AST to the execution plan
    - Execution Duration: the statistics of the execution time for SQL statements
    - Expensive Executor OPS: the statistics of the operators that consume many system resources per second, including `Merge Join`, `Hash Join`, `Index Look Up Join`, `Hash Agg`, `Stream Agg`, `Sort`, `TopN`, and so on
    - Queries Using Plan Cache OPS: the statistics of queries using the Plan Cache per second

- Distsql
    - Distsql Duration: the processing time of Distsql statements
    - Distsql QPS: the statistics of Distsql statements
    - Distsql Partial QPS: the number of Partial results every second
    - Scan Keys Num: the number of keys that each query scans
    - Scan Keys Partial Num: the number of keys that each Partial result scans
    - Partial Num: the number of Partial results for each SQL statement

- KV Errors
    - KV Backoff Duration: the time that a KV retry request lasts
    - TiClient Region Error OPS: the number of Region related error messages returned by TiKV
    - KV Backoff OPS: the number of error messages returned by TiKV
    - Lock Resolve OPS: the number of TiDB cleanup lock operations. When TiDB's read-write request encounters a lock, it will try to clean up the lock
    - Other Errors OPS: the number of other types of errors, including clearing locks and updating `SafePoint`

- KV Duration
    - KV Request OPS: the execution times of a KV request, displayed according to TiKV
    - KV Request Duration 99 by store: the execution time of a KV request, displayed according to TiKV
    - KV Request Duration 99 by type: the execution time of a KV request, displayed according to the request type

- PD Client
    - PD Client CMD OPS: the statistics of commands executed by PD Client per second
    - PD Client CMD Duration: the time it takes PD Client to execute commands
    - PD Client CMD Fail OPS: the statistics of failed commands executed by PD Client per second
    - PD TSO OPS: the number of TSO that TiDB obtains from PD per second
    - PD TSO Wait Duration: the time that TiDB waits to return to TSO from PD
    - PD TSO RPC duration: the time taken by TiDB from sending a request for TSO to PD to receive TSO
    - Start TSO Wait Duration: the time from TiDB sending PD to get start TSO request to waiting for TSO to return

- Schema Load
    - Load Schema Duration: the time it takes TiDB to obtain the schema from TiKV
    - Load Schema OPS: the statistics of the schemas that TiDB obtains from TiKV per second
    - Schema Lease Error OPM: the Schema Lease errors include two types named `change` and `outdate`. `change` means that the schema has changed, and `outdate` means that the schema cannot be updated, which is a more serious error. It will alarm when an `outdate` error occurs
    - Load Privilege OPS: the statistics of the number of privilege information obtained by TiDB from TiKV per second

- DDL
    - DDL Duration 95: 95% quantile of DDL statement processing time
    - Batch Add Index Duration 100: statistics of the maximum time spent by each Batch when creating an index
    - DDL Waiting Jobs Count: the number of DDL tasks that are waiting
    - DDL META OPM: the number of times that a DDL obtains META every minute
    - DDL Worker Duration 99: 99% of the execution time of each DDL worker
    - Deploy Syncer Duration: the time consumed by Schema Version Syncer initialization, restart, and clearing up operations
    - Owner Handle Syncer Duration: the time that it takes the DDL Owner to update, obtain, and check the Schema Version
    - Update Self Version Duration: the time consumed by updating the version information of Schema Version Syncer
    - DDL OPM: the number of executions per second of DDL statements
    - DDL Add Index Progress In Percentage: the progress of adding an index

- Statistics
    - Auto Analyze Duration 95: the time consumed by automatic `ANALYZE`
    - Auto Analyze QPS: the statistics of automatic `ANALYZE`
    - Stats Inaccuracy Rate: the information of the statistics inaccuracy rate
    - Pseudo Estimation OPS: the number of the SQL statements optimized using pseudo statistics
    - Dump Feedback OPS: the number of stored statistical feedbacks
    - Store Query Feedback QPS: the number of operations per second to store the feedback information of the union query, which is performed in TiDB memory
    - Significant Feedback: the number of significant feedback pieces that update the statistics information
    - Update Stats OPS: the number of updating statistics with feedback
    - Fast Analyze Status 100: the status for quickly collecting statistical information

- Owner
    - New ETCD Session Duration 95: the time it takes to create a new etcd session. TiDB connects to etcd in PD through etcd client to save/read some metadata information. This records the time spent creating the session
    - Owner Watcher OPS: the number of operations per second of DDL owner watches PD's etcd metadata

- Meta
    - AutoID QPS: AutoID related statistics, including three operations (global ID allocation, a single table AutoID allocation, a single table AutoID Rebase)
    - AutoID Duration: the time consumed by AutoID related operations
    - Region Cache Error OPS: the number of errors encountered per second by TiDB cached region information
    - Meta Operations Duration 99: the latency of Meta operations

- GC
    - Worker Action OPM: the number of GC related operations, including `run_job`, `resolve_lock`, and `delete\_range`
    - Duration 99: the time consumed by GC related operations
    - Config: the configuration of GC data life time and GC run interval
    - GC Failure OPM: the number of failed GC related operations
    - Delete Range Failure OPM: the number of times the `Delete Range` failed
    - Too Many Locks Error OPM: the number of the error that GC clears up too many locks
    - Action Result OPM: the number of results of GC-related operations
    - Delete Range Task Status: the task status of `Delete Range`, including completion and failure status
    - Push Task Duration 95: the time spent pushing GC subtasks to GC workers

- Batch Client
    - Pending Request Count by TiKV: the number of Batch messages that are pending processing
    - Wait Duration 95: the waiting time of Batch messages that are pending processing
    - Batch Client Unavailable Duration 95: the unavailable time of the Batch client
    - No Available Connection Counter: the number of times the Batch client cannot find an available link
