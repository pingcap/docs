---
title: 与第三方工具的已知不兼容问题
summary: 描述在测试过程中发现的 TiDB 与第三方工具的兼容性问题。
---

# 与第三方工具的已知不兼容问题

> **Note:**
>
> [Unsupported features](/mysql-compatibility.md#unsupported-features) 部分列出了 TiDB 不支持的功能，包括：
>
> - 存储过程和函数
> - 触发器
> - 事件
> - 用户定义函数
> - `SPATIAL` 函数、数据类型和索引
> - `XA` 语法
>
> 以上不支持的功能属于预期行为，不在本文档列出。更多详情请参见 [MySQL Compatibility](/mysql-compatibility.md)。

本文档中列出的不兼容问题是在某些 [TiDB 支持的第三方工具](/develop/dev-guide-third-party-tools-compatibility.md) 中发现的。

## 一般不兼容问题

### `SELECT CONNECTION_ID()` 在 TiDB 中返回 64 位整数

**描述**

在 TiDB 中，`SELECT CONNECTION_ID()` 返回一个 64 位整数，例如 `2199023260887`，而在 MySQL 中返回一个 32 位整数，例如 `391650`。

**避免方式**

在 TiDB 应用中，为避免数据溢出，应使用 64 位整数或字符串类型存储 `SELECT CONNECTION_ID()` 的结果。例如，在 Java 中可以使用 `Long` 或 `String`，在 JavaScript 或 TypeScript 中可以使用 `string`。

### TiDB 不维护 `Com_*` 计数器

**描述**

MySQL 维护一系列以 `Com_` 开头的 [服务器状态变量](https://dev.mysql.com/doc/refman/8.0/en/server-status-variables.html#statvar_Com_xxx)，用于统计自上次启动以来执行的操作总数。例如，`Com_select` 记录自上次启动后由 MySQL 发起的 `SELECT` 语句总数（即使这些语句未成功查询）。TiDB 不维护这些变量。你可以使用语句 [<code>SHOW GLOBAL STATUS LIKE 'Com_%'</code>](/sql-statements/sql-statement-show-status.md) 查看 TiDB 和 MySQL 之间的差异。

**避免方式**

<CustomContent platform="tidb">

不要使用这些变量。常见场景之一是监控。TiDB 具有良好的可观察性，无需通过查询服务器状态变量进行监控。对于自定义监控工具，参考 [TiDB 监控框架概述](/tidb-monitoring-framework.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

不要使用这些变量。常见场景之一是监控。TiDB Cloud 具有良好的可观察性，无需通过查询服务器状态变量进行监控。关于 TiDB Cloud 监控服务的更多信息，参考 [监控 TiDB 集群](/tidb-cloud/monitor-tidb-cluster.md)。

</CustomContent>

### TiDB 在错误信息中区分 `TIMESTAMP` 和 `DATETIME`

**描述**

TiDB 的错误信息会区分 `TIMESTAMP` 和 `DATETIME`，而 MySQL 不会，所有类型都返回为 `DATETIME`。也就是说，MySQL 错误信息会错误地将 `TIMESTAMP` 类型的错误转换为 `DATETIME`。

**避免方式**

<CustomContent platform="tidb">

不要使用错误信息进行字符串匹配。建议使用 [Error Codes](/error-codes.md) 进行故障排查。

</CustomContent>

<CustomContent platform="tidb-cloud">

不要使用错误信息进行字符串匹配。建议使用 [Error Codes](https://docs.pingcap.com/tidb/stable/error-codes) 进行故障排查。

</CustomContent>

### TiDB 不支持 `CHECK TABLE` 语句

**描述**

TiDB 不支持 `CHECK TABLE` 语句。

**避免方式**

可以使用 TiDB 中的 [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) 语句来检查数据和索引的一致性。

## 与 MySQL JDBC 的兼容性

测试版本为 MySQL Connector/J 8.0.29。

### 默认字符集排序规则不一致

**描述**

MySQL Connector/J 的字符集排序规则存储在客户端，由服务器版本区分。

下表列出了已知的客户端和服务器端字符集排序规则不一致情况：

| 字符集 | 客户端默认排序规则 | 服务器端默认排序规则 |
| --------- | -------------------- | ------------- |
| `ascii`   | `ascii_general_ci`   | `ascii_bin`   |
| `latin1`  | `latin1_swedish_ci`  | `latin1_bin`  |
| `utf8mb4` | `utf8mb4_0900_ai_ci` | `utf8mb4_bin` |

**避免方式**

手动设置排序规则，不依赖客户端的默认排序规则。客户端默认排序规则存储在 MySQL Connector/J 的配置文件中。

### `NO_BACKSLASH_ESCAPES` 参数不生效

**描述**

在 TiDB 中，不能在不转义 `\` 字符的情况下使用 `NO_BACKSLASH_ESCAPES` 参数。更多详情请跟踪 [此问题](https://github.com/pingcap/tidb/issues/35302)。

**避免方式**

在 TiDB 中不要使用 `NO_BACKSLASH_ESCAPES` 和 `\`，而应在 SQL 语句中使用 `\\`。

### `INDEX_USED` 相关参数不支持

**描述**

TiDB 不在协议中设置 `SERVER_QUERY_NO_GOOD_INDEX_USED` 和 `SERVER_QUERY_NO_INDEX_USED` 参数。这会导致以下参数返回的结果与实际情况不一致：

- `com.mysql.cj.protocol.ServerSession.noIndexUsed()`
- `com.mysql.cj.protocol.ServerSession.noGoodIndexUsed()`

**避免方式**

不要在 TiDB 中使用 `noIndexUsed()` 和 `noGoodIndexUsed()` 函数。

### `enablePacketDebug` 参数不支持

**描述**

TiDB 不支持 [enablePacketDebug](https://dev.mysql.com/doc/connector-j/en/connector-j-connp-props-debugging-profiling.html) 参数。该参数是 MySQL Connector/J 用于调试的参数，会保持数据包缓冲区，可能导致连接意外关闭。**切勿**开启。

**避免方式**

不要在 TiDB 中设置 `enablePacketDebug` 参数。

### UpdatableResultSet 不支持

**描述**

TiDB 不支持 `UpdatableResultSet`。**切勿**在连接中指定 `ResultSet.CONCUR_UPDATABLE`，也不要在 `ResultSet` 内部更新数据。

**避免方式**

为了保证数据一致性，可以使用 `UPDATE` 语句进行数据更新。

## MySQL JDBC 的 Bug

### `useLocalTransactionState` 和 `rewriteBatchedStatements` 同时为 true 会导致事务无法提交或回滚

**描述**

在使用 MySQL Connector/J 8.0.32 或更早版本时，如果同时设置 `useLocalTransactionState` 和 `rewriteBatchedStatements` 为 `true`，事务可能无法提交。可复现代码请参考 [此代码](https://github.com/Icemap/tidb-java-gitpod/tree/reproduction-local-transaction-state-txn-error)。

**避免方式**

> **Note:**
>
> `useConfigs=maxPerformance` 包含一组配置。关于 MySQL Connector/J 8.0 和 5.1 版本的详细配置，请参见 [mysql-connector-j 8.0](https://github.com/mysql/mysql-connector-j/blob/release/8.0/src/main/resources/com/mysql/cj/configurations/maxPerformance.properties) 和 [mysql-connector-j 5.1](https://github.com/mysql/mysql-connector-j/blob/release/5.1/src/com/mysql/jdbc/configs/maxPerformance.properties)。在使用 `maxPerformance` 时，需禁用 `useLocalTransactionState`，即使用 `useConfigs=maxPerformance&useLocalTransactionState=false`。

该问题已在 MySQL Connector/J 8.0.33 中修复。考虑到 8.0.x 系列的更新已停止，强烈建议升级你的 MySQL Connector/J 至 [最新的正式版 (GA)](https://dev.mysql.com/downloads/connector/j/) 以获得更好的稳定性和性能。

### 连接器与早于 5.7.5 版本的服务器不兼容

**描述**

在使用 MySQL Connector/J 8.0.31 或更早版本连接 MySQL 服务器 < 5.7.5 或使用 MySQL 服务器 < 5.7.5 协议的数据库（如 TiDB 早于 v6.3.0）时，可能会导致连接挂起。更多详情请参见 [Bug Report](https://bugs.mysql.com/bug.php?id=106252)。

**避免方式**

该问题已在 MySQL Connector/J 8.0.32 中修复。考虑到 8.0.x 系列的更新已停止，强烈建议升级你的 MySQL Connector/J 至 [最新的正式版 (GA)](https://dev.mysql.com/downloads/connector/j/) 以获得更好的稳定性和性能。

TiDB 也通过以下方式修复了此问题：

- 客户端：此问题已在 **pingcap/mysql-connector-j** 中修复，你可以使用 [pingcap/mysql-connector-j](https://github.com/pingcap/mysql-connector-j) 代替官方的 MySQL Connector/J。
- 服务器端：此兼容性问题自 TiDB v6.3.0 起已修复，你可以将服务器升级到 v6.3.0 或更高版本。

## 与 Sequelize 的兼容性

本节描述的兼容性信息基于 [Sequelize v6.32.1](https://www.npmjs.com/package/sequelize/v/6.32.1)。

根据测试结果，TiDB 支持大部分 Sequelize 功能（[使用 `MySQL` 作为方言](https://sequelize.org/docs/v6/other-topics/dialect-specific-things/#mysql)）。

不支持的功能包括：

- [`GEOMETRY`](https://github.com/pingcap/tidb/issues/6347) 不支持。
- 不支持修改整数主键。
- `PROCEDURE` 不支持。
- 不支持 [READ-UNCOMMITTED]( /system-variables.md#transaction_isolation) 和 [SERIALIZABLE]( /system-variables.md#transaction_isolation) 隔离级别。
- 默认不允许修改列的 `AUTO_INCREMENT` 属性。
- 不支持 `FULLTEXT`、`HASH` 和 `SPATIAL` 索引。
- 不支持 `sequelize.queryInterface.showIndex(Model.tableName);`。
- 不支持 `sequelize.options.databaseVersion`。
- 不支持使用 [`queryInterface.addColumn`](https://sequelize.org/api/v6/class/src/dialects/abstract/query-interface.js~queryinterface#instance-method-addColumn) 添加外键引用。

### 不支持修改整数主键

**描述**

不支持修改整数主键。TiDB 在主键为整数类型时，将主键用作数据组织的索引。详细信息请参见 [Issue #18090](https://github.com/pingcap/tidb/issues/18090) 和 [Clustered Indexes](/clustered-indexes.md)。

### 不支持 `READ-UNCOMMITTED` 和 `SERIALIZABLE` 隔离级别

**描述**

TiDB 不支持 `READ-UNCOMMITTED` 和 `SERIALIZABLE` 隔离级别。如果设置为这两个级别，TiDB 会抛出错误。

**避免方式**

仅使用 TiDB 支持的隔离级别：`REPEATABLE-READ` 或 `READ-COMMITTED`。

如果希望 TiDB 兼容其他应用设置的 `SERIALIZABLE` 隔离级别，但不依赖 `SERIALIZABLE`，可以设置 [`tidb_skip_isolation_level_check`](/system-variables.md#tidb_skip_isolation_level_check) 为 `1`。在这种情况下，TiDB 会忽略不支持的隔离级别错误。

### 不允许修改列的 `AUTO_INCREMENT` 属性（默认）

**描述**

通过 `ALTER TABLE MODIFY` 或 `ALTER TABLE CHANGE` 命令添加或删除列的 `AUTO_INCREMENT` 属性，默认不允许。

**避免方式**

参考 [AUTO_INCREMENT 的限制]( /auto-increment.md#restrictions)。

如果要允许删除 `AUTO_INCREMENT` 属性，可以将 `@@tidb_allow_remove_auto_inc` 设置为 `true`。

### 不支持 `FULLTEXT`、`HASH` 和 `SPATIAL` 索引

**描述**

`FULLTEXT`、`HASH` 和 `SPATIAL` 索引不被支持。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>