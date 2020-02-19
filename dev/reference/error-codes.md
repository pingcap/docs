---
title: Error Codes and Troubleshooting
summary: Learn about the error codes and solutions in TiDB.
category: reference
---

# Error Codes and Troubleshooting

This document describes the problems encountered during the use of TiDB and provides the solutions.

## Error codes

TiDB is compatible with the error codes in MySQL, and in most cases returns the same error code as MySQL. In addition, TiDB has the following unique error codes:

| Error code | Description | Solution |
| ---- | ------- | --------- |
| 8001 | The memory used by the request exceeds the threshold limit for the TiDB memory usage. | Increase the value of the system variable with the `tidb_mem_quota` prefix. |
| 8002 | To guarantee consistency, a transaction with the `SELECT FOR UPDATE` statement cannot be retried when it encounters a commit conflict. TiDB rolls back the transaction and returns this error. | Retry the failed transaction. |
| 8003 | If the data in a row is not consistent with the index when executing the `ADMIN CHECK TABLE` command, TiDB returns this error. |
| 8004 | A single transaction is too large. | See [the error message `transaction too large`](/dev/faq/tidb.md#the-error-message-transaction-too-large-is-displayed) for the cause and solution.  |
| 8005 | Transactions in TiDB encounter write conflicts. | See [the Troubleshoot section](/dev/faq/tidb.md#troubleshoot) for the cause and solution. |
| 8018 | The plugin cannot be reloaded because it has not been loaded. |
| 8019 | The version of the plugin that are being reloaded is different from the previous version. The plugin cannot be reloaded. |
| 8020 | The table is locked. |
| 8021 | The key does not exist. |
| 8022 | The transaction commit fails. You may retry the process. |
| 8023 | An empty value is not allowed. |
| 8024 | Illegal transactions. |
| 8025 | A single Key-Value pair that are being written is too large. |
| 8026 | The interface is not implemented. |
| 8027 | The table schema version is outdated. |
| 8028 | The table schema has changed. |
| 8029 | Incorrect value. |
| 8030 | |
| 8031 | A negative number is converted to a positive number, when being converted to an unsigned number. |
| 8032 | Illegal `year` format. |
| 8033 | Illegal `year` value. |
| 8034 | Incorrect `datetime` value. |
| 8036 | Illegal `time` format. |
| 8037 | Illegal `week` format. |
| 8038 | The field cannot access a default value. |
| 8039 | The ? of index exceeds boundary. |
| 8042 | The state of table structure is not existing. |
| 8043 | The state of column information is not existing. |
| 8044 | The state of index is not existing. |
| 8045 | Illegal table data. |
| 8046 | The state of column information is hidden. |
| 8047 | The system variable value you set is not supported. This error occurs in the warning after the user sets a variable value that is not supported in the database.
| 8048 | The user sets a database isolation level that is not supported.
| 8049 | The loading of privilege-related table failed. |
| 8050 | The privilege type you set is not supported. |
| 8051 | Unknown field type. |
| 8052 | The serial number of the packet from client is incorrect. |
| 8053 | An illegal `AUTO-INCREMENT` value is obtained. |
| 8055 | The current snapshot is too old. The data may have been garbage collected. |
| 8056 | Illegal table ID. |
| 8057 | Illegal field type. |
| 8058 | You applied an auto variable type that does not exist. |
| 8059 | The obtain of auto random amount failed. |
| 8060 | Illegal auto-increment offset. |
| 8061 | The SQL Hint is not supported. |
| 8062 | An illegal token is used in the SQL Hint. It conflicts with reserved words in Hint. |
| 8063 | The memory usage limited in SQL Hint exceeds the upper limit set by the system. The setting in SQL Hint is ignored. |
| 8064 | 解析 SQL Hint 失败 | The parsing of SQL Hint failed. |
| 8065 | Illegal integer is used in SQL Hint. |
| 8066 | The second parameter in the `JSON_OBJECTAGG` function is illegal. |
| 8101 | The format of plugin ID is incorrect. | The correct format is `[name]-【version]`, and no `-` is allowed in `name` and `version`. |
| 8102 | Unable to read the plugin definition information |
| 8103 | The plugin name is incorrect. |
| 8104 | The plugin version does not match. |
| 8105 | The plugin is repeatedly loaded. |
| 8106 | The system variable name defined by the plugin does not begin with the name of the plugin. |
| 8107 | The loaded plugin does not specify a version, or the version specified is too low. |
| 8108 | Unsupported execution plan type. |
| 8109 | The specified index cannot be found when the index is analyzed.
| 8110 | The Cartesian product operation is not allowed. | Set the `cross-join` in the configuration to `true`. |
| 8111 | When executing the `EXECUTE` statement, the corresponding `Prepare` statement cannot be found.
| 8112 | The number of parameters in the `EXECUTE` statement is not consistent with the `Prepare` statement. |
| 8113 | The table structure involved in the `Execute` statement has changed after the `Prepare` statement is executed. |
| 8114 | Unknown execution plan type. |
| 8115 | Preparing multiple lines of statements is not supported. |
| 8116 | Preparing DDL statements is not supported. |
| 8118 | Executor build failed. |
| 8120 | The `start tso` of transactions cannot be obtained. |
| 8121 | Privilege check failed. |
| 8122 | Wild cards are specified, but no corresponding table name is found. |
| 8123 | An SQL query with aggregate functions returns non-aggregated columns, which violates the `only_full_group_by` mode. |
| 8200 | The DDL syntax is not yet supported. |
| 8201 | TiDB is currently not the DDL owner. |
| 8202 | This index cannot be decoded. |
| 8203 | Illegal DDL worker. |
| 8204 | Illegal DDL job. |
| 8205 | Illegal DDL job mark. |
| 8206 | The DDL operation in `re-organize` phase timed out.
| 8207 | Illegal storage nodes. |
| 8210 | Illegal DDL state. |
| 8211 | Panic occurs during the DDL operation in `re-organize` phase. |
| 8212 | Illegal split range of Region. |
| 8213 | Illegal DDL job version |
| 8214 | The DDL operation is terminated. |
| 8215 | The `ADMIN REPAIR TABLE` command fails. |
| 8216 | Illegal auto random columns. |
| 8221 | The Key encoding is incorrect. |
| 8222 | The indexing of Key encoding is incorrect. |
| 8223 | This error occurs when detecting that the data is not consistent with the index. |
| 8224 | The DDL job cannot be found. |
| 8225 | The DDL operation is completed and cannot be canceled. |
| 8226 | The DDL operation is almost completed and cannot be canceled. |
| 8227 | Unsupported options are used when creating `Sequence`. |
| 9001 | The PD request timed out. | Check the state/monitor/log of the PD server and the network between the TiDB server and the PD server. |
| 9002 | The TiKV request timed out. | Check the state/monitor/log of the TiKV server and the network between the TiDB server and the TiKV server. |
| 9003 | The TiKV server is busy and this usually occurs when the workload is too high. | Check the state/monitor/log of the TiKV server. |
| 9004 | This error occurs when a large number of transactional conflicts exist in the database. | Check the code of application. |
| 9005 | A certain Raft Group is not available, such as the number of replicas is not enough. This error usually occurs when the TiKV server is busy or the TiKV node is down. | Check the state/monitor/log of the TiKV server. |
| 9006 | The interval of GC Life Time is too short and the data that should be read by the long transactions might be cleared. | Extend the interval of GC Life Time. |
| 9500 | A single transaction is too large. | See [the error message `transaction too large`](/dev/faq/tidb.md#the-error-message-transaction-too-large-is-displayed) for the solution. |
| 9007 | Transactions in TiKV encounter write conflicts. | See [the Troubleshoot section](/dev/faq/tidb.md#troubleshoot) for the cause and solution. |
| 9008 | Too many requests are sent to TiKV at the same time. The number exceeds limit. |

## Troubleshooting

See the [troubleshooting](/dev/how-to/troubleshoot/cluster-setup.md) and [FAQ](/dev/faq/tidb.md) documents.
