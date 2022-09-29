---
title: Known Incompatibility Issues with Third-Party Tools
summary: List the third-party tools incompatibility issues encountered while testing by PingCAP
---

# Known Incompatibility Issues with Third-Party Tools

> **Note:**
>
> TiDB has listed the [unsupported features](/mysql-compatibility.md#unsupported-features), typically unsupported features:
>
> - Stored procedures and functions
> - Triggers
> - Events
> - User-defined functions
> - `FOREIGN KEY` constraints
> - `SPATIAL` functions, data types and indexes
> - `XA` syntax
>
> Such incompatibilities issues are considered expected behavior and will not be repeated. See the [MySQL Compatibility](/mysql-compatibility.md) for more descriptions.

## General

### `SELECT CONNECTION_ID()` returns a 64-bit integer

**Description**

`SELECT CONNECTION_ID()` return value for TiDB is 64-bit, such as `2199023260887`, while for MySQL it is 32-bit, such as `391650`.

**Ways to Avoid**

Please use each language's 64-bit integer type (or string type) for the reception to prevent overflow. For example, Java should use `Long` or `String` for reception, and JS/TS should use `string` type for the reception.

### TiDB does not set `Com_*` counters

**Description**

MySQL maintains a series of [server status variables starting with `Com_`](https://dev.mysql.com/doc/refman/8.0/en/server-status-variables.html#statvar_Com_xxx) to keep track of the total number of operations you have performed on the database. For example, `Com_select` keeps track of the total number of `SELECT` statements initiated by the MySQL database since it was last started (even if the statements were not queried successfully). TiDB does not maintain this variable. You can use the statement `SHOW GLOBAL STATUS LIKE 'Com_%'` to see the difference between the two databases.

**Ways to Avoid**

Please do not use these variables. Common usage scenarios such as monitoring. TiDB is well observable and does not require querying from server status variables. For custom monitoring tools, read the [TiDB Monitoring Framework Overview](/tidb-monitoring-framework.md) for more information.

### TiDB error messages distinguish between `timestamp` and `datetime`

**Description**

TiDB error messages distinguish between `timestamp` and `datetime`, while MySQL does not, and returns them all as `datetime`. That is, MySQL incorrectly writes `timestamp` type error messages as `datetime` type.

**Ways to Avoid**

Do not use the error messages for string matching, but use [Error Codes](/error-codes.md) for troubleshooting.

### The `CHECK TABLE` statement is not supported

**Description**

TiDB uses the [ADMIN CHECK [TABLE|INDEX]](/sql-statements/sql-statement-admin-check-table-index.md) statement to check the consistency of data and corresponding indexes in tables. The `CHECK TABLE` statement is not supported.

**Ways to Avoid**

Use `ADMIN CHECK [TABLE|INDEX]`.

## MySQL JDBC Incompatibility

- Test Version: MySQL Connector/J `8.0.29`

### Default Collations are inconsistent

**Description**

The collations of MySQL Connector/J are stored in the client and are distinguished by the server version.

Known character sets for which client-side and server-side collations do not match:

| Character Sets | Client Default Collations | Server Default Collations |
| - | - | - |
| `ascii` | `ascii_general_ci` | `ascii_bin` |
| `latin1` | `latin1_swedish_ci` | `latin1_bin` |
| `utf8mb4` | `utf8mb4_0900_ai_ci` | `utf8mb4_bin` |

**Ways to Avoid**

Set the sorting rules manually and do not rely on the client default sorting rules (client default sorting rules are saved by the MySQL Connector/J configuration file).

### Parameter `NO_BACKSLASH_ESCAPES` not effect

**Description**

The `NO_BACKSLASH_ESCAPES` parameter cannot be used so that `\` character is not escaped. Tracking the [issue](https://github.com/pingcap/tidb/issues/35302).

**Ways to Avoid**

Do not use `NO_BACKSLASH_ESCAPES` with `\`, but use normal `\\` for SQL writing.

### Not Support INDEX_USED Parameters

**Description**

TiDB does not set the `SERVER_QUERY_NO_GOOD_INDEX_USED` and `SERVER_QUERY_NO_INDEX_USED` parameters in the protocol. This will cause the following parameters to be returned inconsistently with the actual:

- `com.mysql.cj.protocol.ServerSession.noIndexUsed()`
- `com.mysql.cj.protocol.ServerSession.noGoodIndexUsed()`

**Ways to Avoid**

Do not use the `noIndexUsed()` and `noGoodIndexUsed()` functions.

### Not Support `enablePacketDebug` Parameters

**Description**

TiDB does not support the [enablePacketDebug](https://dev.mysql.com/doc/connector-j/8.0/en/connector-j-connp-props-debugging-profiling.html) parameter, which is a MySQL Connector/J parameter used for debugging that will retain the packet's ring buffer. this will cause the connection to **_UNEXPECTED CLOSE_**, **_DO NOT_** turn it on.

**Ways to Avoid**

Do not set the `enablePacketDebug` parameter.

### Not Support `UpdatableResultSet`

**Description**

TiDB does not support `UpdatableResultSet`, that means **_DO NOT_** specify the `ResultSet.CONCUR_UPDATABLE` parameter and updates data inside the ResultSet.

**Ways to Avoid**

Using additional `UPDATE` statements for data updates, you can use transactions to ensure data consistency.

## MySQL JDBC Bug

### `useLocalTransactionState` and `rewriteBatchedStatements` are true at the same time will cause the transaction to fail to commit

**Description**

When the `useLocalTransactionState` and `rewriteBatchedStatements` parameters turned on at the same time, will cause the transaction to fail to commit. You can reproduce with [this code](https://github.com/Icemap/tidb-java-gitpod/tree/reproduction-local-transaction-state-txn-error).

**Ways to Avoid**

> **Note:**
>
> This bug has been reported to MySQL, you can follow this [Bug Report](https://bugs.mysql.com/bug.php?id=108643) to keep track of the latest news.

**_DO NOT_** turn on `useLocalTransactionState`, as this may prevent transactions from being committed or rolled back.

### Connector Forward Compatibility Issue

**Description**

Newer versions of MySQL Connector/J work with MySQL servers below version **5.7.5**, or databases using MySQL server protocols below version **5.7.5** (e.g. TiDB below version **6.3**).  It will cause the database connection to hang under certain circumstances, see [Bug Report](https://bugs.mysql.com/bug.php?id=106252) for more details.

**Ways to Avoid**

This is a known issue, and MySQL Connector/J has not merged the fix code so far.

PingCAP made two dimensional fixes to it:

- Client side: You can replace the official MySQL Connector/J with [pingcap/mysql-connector-j](https://github.com/pingcap/mysql-connector-j). The bug is fixed in **pingcap/mysql-connector-j**.
- Server side: you can upgrade the server to version **6.3** or above; TiDB has fixed this compatibility issue in version **6.3**.