---
title: TiDB Configuration File Description
summary: Learn the TiDB configuration file options that are not involved in command line options.
category: deployment
---

<!-- markdownlint-disable MD001 -->

# TiDB Configuration File Description

The TiDB configuration file supports more options than command line options. You can download the default configuration file [`config.toml.example`](https://github.com/pingcap/tidb/blob/master/config/config.toml.example) and rename it to `config.toml`. This document describes only the options that are not involved in [command line options](/v2.1/reference/configuration/tidb-server/configuration.md).

### `split-table`

- To create a separate Region for each table
- Default: true
- It is recommended to set it to false if you need to create a large number of tables

### `oom-action`

- To specify the operation when out-of-memory occurs in TiDB
- Default: "log"
- The valid options are "log" and "cancel"; "log" only prints the log, without actual processing; "cancel" cancels the operation and outputs the log

### `mem-quota-query`

- The maximum threshold of memory that a single SQL statement can occupy.
- Default: 34359738368
- Requests that exceed this value are handled by the behavior defined by `oom-action`.

### `enable-streaming`

- To enable the data fetch mode of streaming in Coprocessor
- Default: false

### `lower-case-table-names`

- To configure the value of the `lower_case_table_names` system variable
- Default: 2
- For details, you can see the [MySQL description](https://dev.mysql.com/doc/refman/5.7/en/server-system-variables.html#sysvar_lower_case_table_names) of this variable
- Currently, TiDB only supports setting the value of this option to 2. This means it is case-sensitive when you save a table name, but case-insensitive when you compare table names. The comparison is based on the lower case.

### `lease`

- DDL lease timeout
- Default: 45s
- Unit: second

### `compatible-kill-query`

+ To set the `KILL` statement to be MySQL compatible
+ Default: false
+ The behavior of `KILL xxx` in TiDB differs from the behavior in MySQL. TiDB requires the `TIDB` keyword, as in `KILL TIDB xxx`. If `compatible-kill-query` is set to true, the `TIDB` keyword is not needed.
+ This distinction is important because the default behavior of the MySQL command-line client, when the user hits Ctrl-C, is to create a new connection to the backend and execute the KILL statement in that new connection. If a load balancer or proxy has sent the new connection to a different TiDB server instance than the original session, the wrong session could be terminated, which could cause interruption to applications using the cluster. Only enable `compatible-kill-query` if you are certain that the connection you refer to in your `KILL` statement is on the same server to which you send the `KILL` statement.

### `check-mb4-value-in-utf8`

- Enable the check on the `utf8mb4` character. If it is enabled and the character set is `utf8`, an error occurs when the `mb4` character is inserted into `utf8`.
- Default: true

### `treat-old-version-utf8-as-utf8mb4`

- Treat the `utf8` character set in the old table as a switch for `utf8mb4`.
- Default: true

## Log

Configuration about log.

### `format`

- To specify the log output format
- The valid options are "json", "text" and "console"
- Default: "text"

### `disable-timestamp`

- Whether to disable outputting timestamp in the log
- Default: false
- If you set the value to true, the log does not output timestamp

### `slow-query-file`

- The file name of the slow query log
- Default: "tidb-slow.log"
- The format of the slow log is updated in TiDB v2.1.8, so the slow log is output to the slow log file separately. In versions before v2.1.8, this variable is set to "" by default.
- After you set it, the slow query log is output to this file separately

### `slow-threshold`

- To output the threshold value of consumed time in the slow log
- Default: 300ms
- If the value in a query is larger than the default value, it is a slow query and is output to the slow log

### `expensive-threshold`

- To output the threshold value of the number of rows for the `expensive` operation
- Default: 10000
- When the number of query rows (including the intermediate results based on statistics) is larger than this value, it is an `expensive` operation and outputs log with the `[EXPENSIVE_QUERY]` prefix.

### `query-log-max-len`

- The maximum length of SQL output
- Default: 2048
- When the length of the statement is longer than `query-log-max-len`, the statement is truncated to output

## log.file

### `filename`

- The file name of the general log file
- Default: ""
- If you set it, the log is output to this file

### `max-size`

- The size limit of the log file
- Default: 300MB
- The maximum size is 4GB

### `max-days`

- The maximum number of days that the log is retained
- Default: 0
- The log is retained by default; if you set the value, the expired log is cleaned up after `max-days`

### `max-backups`

- The maximum number of retained logs
- Default: 0
- All the log files are retained by default; if you set it to 7, 7 log files are retained at maximum

### `log-rotate`

- Whether to create a new log file every day
- Default: true
- If you set it to true, a new log file is created every day; if you set it to false, the log is output to a single log file

## Security

Configuration about security.

### `ssl-ca`

- The file path of the trusted CA certificate in the PEM format
- Default: ""
- If you set this option and `--ssl-cert`, `--ssl-key` at the same time, TiDB authenticates the client certificate based on the list of trusted CAs specified by this option when the client presents the certificate. If the authentication fails, the connection is terminated.
- If you set this option but the client does not present the certificate, the secure connection continues without client certificate authentication.

### `ssl-cert`

- The file path of the SSL certificate in the PEM format
- Default: ""
- If you set this option and `--ssl-key` at the same time, TiDB allows (but not forces) the client to securely connect to TiDB using TLS
- If the specified certificate or private key is invalid, TiDB starts as usual but cannot receive secure connection

### `ssl-key`

- The file path of the SSL certificate key in the PEM format, that is the private key of the certificate specified by `--ssl-cert`
- Default: ""
- Currently, TiDB does not support loading the private keys protected by passwords

### `cluster-ssl-ca`

- The CA root certificate for connecting TiKV or PD using TLS
- Default: ""

### `cluster-ssl-cert`

- The SSL certificate file path for connecting TiKV or PD using TLS
- Default: ""

### `cluster-ssl-key`

- The SSL private key file path for connecting TiKV or PD using TLS
- Default: ""

### `skip-grant-table`

+ Whether to skip the permission check
+ Default: false

## Performance

Configuration about performance.

### `max-procs`

- The number of CPUs used by TiDB
- Default: 0
- The default "0" indicates using all CPUs in the machine; you can also set it to n, and then TiDB uses n CPUs.

### `stmt-count-limit`

- The maximum number of statements allowed in a single TiDB transaction
- Default: 5000
- If a transaction does not roll back or commit after the number of statements exceeds `stmt-count-limit`, TiDB returns the `statement count 5001 exceeds the transaction limitation, autocommit = false` error.

### `tcp-keep-alive`

- To enable `keepalive` in the TCP layer
- Default: false

### `cross-join`

- Default: true
- TiDB supports executing the `JOIN` statement without any condition (the `WHERE` field) of both sides tables by default; if you set the value to `false`, the server refuses to execute when such a `JOIN` statement appears.

### `stats-lease`

- The time interval of reloading statistics, updating the number of table rows, checking whether it is needed to perform the automatic analysis, using feedback to update statistics and loading statistics of columns
- Default: 3s
    - At intervals of `stats-lease` time, TiDB checks the statistics for updates and updates them to the memory if updates exist
    - At intervals of `20 * stats-lease` time, TiDB persists the total number of rows generated by DML and the number of modified rows
    - At intervals of `stats-lease`, TiDB checks for tables and indexes that need to be automatically analyzed
    - At intervals of `stats-lease`, TiDB checks for column statistics that need to be loaded to the memory
    - At intervals of `200 * stats-lease`, TiDB writes the feedback cached in the memory to the system table
    - At intervals of `5 * stats-lease`, TiDB reads the feedback in the system table, and updates the statistics
- When `stats-lease` is set to 0, all of the above operations are skipped.

### `run-auto-analyze`

- Whether TiDB executes automatic analysis
- Default: true

### `feedback-probability`

- The probability that TiDB collects the feedback statistics of each query
- Default: 0.05
- TiDB collects the feedback of each query at the probability of `feedback-probability`, to update statistics

### `query-feedback-limit`

- The maximum number of Query feedback cached in memory. Feedback that exceeds this amount will be discarded.
- Default: 1024

### `pseudo-estimate-ratio`

- The ratio of the number of rows modified to the total number of rows in the table. If the value is exceeded, the system assumes that the statistics are outdated and adopts pseudo statistics.
- Default: 0.8
- The minimum value is 0; the maximum value is 1.

### `force-priority`

- Set the priority of all statements to the value of force-priority.
- Default: NO_PRIORITY
- Optional values: NO_PRIORITY, LOW_PRIORITY, HIGH_PRIORITY, DELAYED.

## prepared-plan-cache

The Plan Cache configuration of the `prepare` statement.

### `enabled`

- To enable Plan Cache of the `prepare` statement
- Default: false

### `capacity`

- The number of cached statements
- Default: 100

## tikv-client

### `grpc-connection-count`

- The maximum number of connections established with each TiKV
- Default: 16

### `grpc-keepalive-time`

- The time interval that RPC connects to keepalive between TiDB and TiKV nodes. If this value is exceeded, no network packet exists and the gRPC client pings TiKV to see whether it is alive.
- Default: 10
- Unit: second

### `grpc-keepalive-timeout`

- The RPC keepalive check timeout between TiDB and TiKV nodes
- Default: 3
- Unit: second

### `commit-timeout`

- The maximum timeout time when executing a transaction commit
- Default: 41s
- It is required to set this value larger than twice of the Raft election timeout time

### `max-txn-time-use`

- Maximum execution time allowed for a single transaction.
- Default: 590
- Unit: second

### txn-local-latches

Configuration about the transaction latch. It is recommended to enable it when many local transaction conflicts occur.

### `enable`

- To enable
- Default: false

### `capacity`

- The number of slots corresponding to Hash, which automatically adjusts upward to an exponential multiple of 2. Each slot occupies 32 Bytes of memory. If set too small, it might result in slower running speed and poor performance in the scenario where data writing covers a relatively large range (such as importing data).
- Default: 1024000

## binlog

TiDB Binlog related configuration.

### `enable`

- Enable binlog.
- Default: false

### `write-timeout`

- Writing binlog timeout. It is not recommended to modify this value.
- Default: 15s
- Unit: second

### `ignore-error`

- Determines whether to ignore errors occurred in the process of writing binlog into Pump. It is not recommended to modify this value.
- Default value: `false`
- When the value is set to `true` and an error occurs, TiDB stops writing binlog and add `1` to the count of the `tidb_server_critical_error_total` monitoring item. When the value is set to `false`, the binlog writing fails and the entire TiDB service is stopped.

### `binlog-socket`

+ The network address of Binlog output.
+ Default: ""
