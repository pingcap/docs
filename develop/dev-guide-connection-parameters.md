---
title: 连接池与连接参数
summary: 本文档说明了如何为 TiDB 配置连接池和参数。内容涵盖连接池大小、探测配置以及实现最佳吞吐量的公式，还讨论了 JDBC API 的使用以及 MySQL Connector/J 参数配置以优化性能。
---

# 连接池与连接参数

本文档描述了在使用驱动程序或 ORM 框架连接到 TiDB 时，如何配置连接池和连接参数。

<CustomContent platform="tidb">

如果你对 Java 应用开发的更多技巧感兴趣，参见 [使用 TiDB 开发 Java 应用的最佳实践](/best-practices/java-app-best-practices.md#connection-pool)

</CustomContent>

<CustomContent platform="tidb-cloud">

如果你对 Java 应用开发的更多技巧感兴趣，参见 [使用 TiDB 开发 Java 应用的最佳实践](https://docs.pingcap.com/tidb/stable/java-app-best-practices)

</CustomContent>

## 连接池

构建 TiDB (MySQL) 连接相对较为昂贵（至少在 OLTP 场景下）。因为除了建立 TCP 连接外，还需要进行连接认证。因此，客户端通常会将 TiDB (MySQL) 连接保存到连接池中以供重用。

Java 有许多连接池实现，例如 [HikariCP](https://github.com/brettwooldridge/HikariCP)、[tomcat-jdbc](https://tomcat.apache.org/tomcat-10.1-doc/jdbc-pool.html)、[druid](https://github.com/alibaba/druid)、[c3p0](https://www.mchange.com/projects/c3p0/) 和 [dbcp](https://commons.apache.org/proper/commons-dbcp/)。TiDB 不限制你使用哪种连接池，因此你可以根据应用需求选择任何一种。

### 配置连接数

合理调整连接池大小以满足应用自身需求是一种常见做法。以 HikariCP 为例：

- **maximumPoolSize**：连接池中的最大连接数。如果此值过大，TiDB 会消耗资源维护无用连接；如果过小，应用会变得响应缓慢。因此，需要根据应用特性配置此值。详细信息请参见 [关于池大小](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing)。
- **minimumIdle**：连接池中的最小空闲连接数，主要用于在应用空闲时预留部分连接以应对突发请求。也需要根据应用特性进行配置。

应用在使用完连接后，应及时归还连接。建议应用使用相应的连接池监控（如 **metricRegistry**）以便及时定位连接池问题。

### 探测配置

连接池会维护客户端到 TiDB 的持久连接，具体如下：

- 在 v5.4 之前，TiDB 默认不会主动关闭客户端连接（除非报告错误）。
- 从 v5.4 开始，TiDB 默认在 28800 秒（即 8 小时）不活动后自动关闭客户端连接。你可以通过 TiDB 和 MySQL 兼容的 `wait_timeout` 变量控制此超时时间。更多信息请参见 [JDBC 查询超时](/develop/dev-guide-timeouts-in-tidb.md#jdbc-query-timeout)。

此外，客户端与 TiDB 之间可能存在网络代理，如 [LVS](https://en.wikipedia.org/wiki/Linux_Virtual_Server) 或 [HAProxy](https://en.wikipedia.org/wiki/HAProxy)。这些代理通常会在一定空闲时间后主动清理连接（由代理的空闲配置决定）。除了监控代理的空闲配置外，连接池还需要维护或探测连接以保持连接的存活。

如果你经常在 Java 应用中看到如下错误：

```
The last packet sent successfully to the server was 3600000 milliseconds ago. The driver has not received any packets from the server. com.mysql.jdbc.exceptions.jdbc4.CommunicationsException: Communications link failure
```

且 `n`（即 `n milliseconds ago` 中的 n）为 `0` 或非常小的值，通常是因为执行的 SQL 操作导致 TiDB 异常退出。建议检查 TiDB 的 stderr 日志以查明原因。

如果 `n` 为非常大的值（如上述示例中的 `3600000`），很可能是连接空闲时间过长后被代理关闭。常见的解决方案是增加代理的空闲配置值，让连接池可以：

- 每次使用连接前检查连接是否可用。
- 通过单独的线程定期检测连接是否可用。
- 定期发送测试查询以保持连接活跃。

不同的连接池实现可能支持上述一种或多种方法。你可以查阅对应的连接池文档以获取相应配置。

### 经验公式

根据 [关于池大小](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing) 文章，如果你不知道如何为数据库连接池设置合适的大小，可以参考 [基于经验的公式](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing#connections--core_count--2--effective_spindle_count)。然后，根据公式计算出的池大小的性能表现，再进行调整以达到最佳效果。

基于经验的公式如下：

```
connections = ((core_count * 2) + effective_spindle_count)
```

公式中各参数的说明如下：

- **connections**：获取的连接数。
- **core_count**：CPU 核心数。
- **effective_spindle_count**：硬盘数（非 [SSD](https://en.wikipedia.org/wiki/Solid-state_drive)）。每个旋转硬盘可以称为一个 spindle。例如，使用 RAID 16 硬盘的服务器，**effective_spindle_count** 应为 16。因为 HDD 通常一次只能处理一个请求，此公式实际上衡量你的服务器能管理的并发 I/O 请求数。

特别注意 [公式](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing#the-formula) 下的说明：

> ```
> A formula which has held up pretty well across a lot of benchmarks for years is
> that for optimal throughput the number of active connections should be somewhere
> near ((core_count * 2) + effective_spindle_count). Core count should not include
> HT threads, even if hyperthreading is enabled. Effective spindle count is zero if
> the active data set is fully cached, and approaches the actual number of spindles
> as the cache hit rate falls. ... There hasn't been any analysis so far regarding
> how well the formula works with SSDs.
> ```

此说明指出：

- **core_count** 为物理核心数，无论是否启用 [超线程](https://en.wikipedia.org/wiki/Hyper-threading)。
- 当数据全部缓存时，应将 **effective_spindle_count** 设为 `0`。随着缓存命中率下降，数值趋近于实际硬盘数。
- **此公式是否适用于 _SSD_ 还未经过测试，未知。**

使用 SSD 时，建议采用以下经验公式：

```
connections = (number of cores * 4)
```

在 SSD 场景下，可以将最大连接数设置为 `cores * 4`，并根据实际性能进行调整。

### 调优方向

如你所见，基于 [经验公式](#formulas-based-on-experience) 计算的大小只是建议的基础值。为了在特定机器上获得最优大小，你需要尝试其他值并进行性能测试。

以下是一些基本规则，帮助你找到最优的连接池大小：

- 如果网络或存储延迟较高，增加最大连接数以减少等待延迟。一旦某个线程因延迟阻塞，其他线程可以接管并继续处理。
- 如果在服务器上部署了多个服务，每个服务有单独的连接池，应考虑所有连接池最大连接数的总和。

## 连接参数

Java 应用可以通过各种框架封装。在大多数框架中，底层都调用 JDBC API 与数据库服务器交互。对于 JDBC，建议关注以下内容：

- JDBC API 的使用选择
- API 实现者的参数配置

### JDBC API

关于 JDBC API 的使用，参见 [JDBC 官方教程](https://docs.oracle.com/javase/tutorial/jdbc/)。本节介绍几个重要 API 的用法。

#### 使用 Prepare API

对于 OLTP（联机事务处理）场景，程序发往数据库的 SQL 语句有多种类型，去除参数变化后可以穷尽。因此，建议使用 [Prepared Statements](https://docs.oracle.com/javase/tutorial/jdbc/basics/prepared.html)，而非普通的 [文本文件执行](https://docs.oracle.com/javase/tutorial/jdbc/basics/processingsqlstatements.html#executing_queries)，并复用 Prepared Statements 直接执行。这可以避免 TiDB 反复解析和生成 SQL 执行计划的开销。

目前，大部分上层框架调用的都是 Prepare API 进行 SQL 执行。如果你直接使用 JDBC API 进行开发，注意选择 Prepare API。

此外，使用 MySQL Connector/J 的默认实现时，只有客户端的语句会被预处理，语句在 `?` 替换后以文本形式发往服务器。因此，除了使用 Prepare API，还需要在 JDBC 连接参数中配置 `useServerPrepStmts = true`，才能在 TiDB 服务器端进行语句预处理。详细参数配置请参见 [MySQL JDBC 参数](#mysql-jdbc-parameters)。

#### 使用 Batch API

对于批量插入，可以使用 [`addBatch`/`executeBatch`](https://www.tutorialspoint.com/jdbc/jdbc-batch-processing)。`addBatch()` 方法用于在客户端缓存多条 SQL 语句，调用 `executeBatch()` 时一次性发送到数据库。

> **注意：**
>
> 在默认的 MySQL Connector/J 实现中，`addBatch()` 添加的 SQL 语句的发送时间会延迟到调用 `executeBatch()` 时，但在实际网络传输中，语句仍会逐个发送。因此，此方法通常不能减少通信开销。
>
> 如果想实现网络批量传输，需要在 JDBC 连接参数中配置 `rewriteBatchedStatements = true`。详细参数配置请参见 [Batch 相关参数](#batch-related-parameters)。

#### 使用 `StreamingResult` 获取执行结果

在大多数场景下，为提高执行效率，JDBC 默认会提前获取查询结果并存入客户端内存。但当返回超大结果集时，客户端通常希望数据库端减少每次返回的记录数，等待客户端内存准备好后再请求下一批。

JDBC 常用的两种处理方式为：

- 第一种： [将 **FetchSize** 设置为 `Integer.MIN_VALUE`](https://dev.mysql.com/doc/connector-j/en/connector-j-reference-implementation-notes.html#ResultSet)，确保不缓存，客户端通过 `StreamingResult` 从网络连接读取执行结果。

    使用流式读取时，必须在继续使用语句进行新查询前，完成对 `resultset` 的读取或关闭，否则会返回错误：

    ```
    No statements may be issued when any streaming result sets are open and in use on a given connection. Ensure that you have called .close() on any active streaming result sets before attempting more queries.
    ```

    为避免此错误，可以在 URL 中添加参数 `clobberStreamingResults=true`，此时 `resultset` 会自动关闭，但会丢失之前流式查询中的结果集。

- 第二种：通过 [设置 `FetchSize`](http://makejavafaster.blogspot.com/2015/06/jdbc-fetch-size-performance.html) 为正整数，并在 JDBC URL 中配置 `useCursorFetch = true` 来实现 Cursor Fetch。

TiDB 支持这两种方式，但建议优先使用第一种，将 `FetchSize` 设置为 `Integer.MIN_VALUE`，因为实现简单且执行效率更高。

第二种方式中，TiDB 会先将所有数据加载到 TiDB 节点，然后根据 `FetchSize` 返回数据，通常会占用更多内存。如果 [`tidb_enable_tmp_storage_on_oom`](/system-variables.md#tidb_enable_tmp_storage_on_oom) 设置为 `ON`，TiDB 可能会临时将结果写入硬盘。

如果 [`tidb_enable_lazy_cursor_fetch`](/system-variables.md#tidb_enable_lazy_cursor_fetch-new-in-v830) 设置为 `ON`，TiDB 会在客户端请求时才逐步读取部分数据，内存占用更少。详细信息和限制请参见 [关于 `tidb_enable_lazy_cursor_fetch` 系统变量的完整描述](/system-variables.md#tidb_enable_lazy_cursor_fetch-new-in-v830)。

### MySQL JDBC 参数

JDBC 通常通过 URL 参数提供实现相关的配置。本节介绍 [MySQL Connector/J 的参数配置](https://dev.mysql.com/doc/connector-j/en/connector-j-reference-configuration-properties.html)（如果你使用 MariaDB，请参见 [MariaDB 的参数配置](https://mariadb.com/kb/en/library/about-mariadb-connector-j/#optional-url-parameters)）。由于本文无法涵盖所有配置项，主要关注可能影响性能的几个参数。

#### Prepare 相关参数

本节介绍与 `Prepare` 相关的参数。

- **useServerPrepStmts**

    **useServerPrepStmts** 默认为 `false`，即使使用 Prepare API，"预处理" 操作也只在客户端完成。为了避免服务器解析开销，如果同一 SQL 语句多次使用 Prepare API，建议将此配置设为 `true`。

    可以通过以下方式验证此设置是否生效：

    - 进入 TiDB 监控面板，通过 **Query Summary** > **CPS By Instance** 查看请求命令类型。
    - 如果请求中 `COM_QUERY` 被替换为 `COM_STMT_EXECUTE` 或 `COM_STMT_PREPARE`，说明此设置已生效。

- **cachePrepStmts**

    虽然 `useServerPrepStmts=true` 允许服务器执行 Prepared Statements，但默认情况下，客户端在每次执行后会关闭 Prepared Statements，不会复用。这意味着“预处理”操作甚至不如文本执行高效。为解决此问题，建议在设置 `useServerPrepStmts=true` 后，同时配置 `cachePrepStmts=true`，以便客户端缓存 Prepared Statements。

    可以通过以下方式验证：

    - 进入 TiDB 监控面板，通过 **Query Summary** > **CPS By Instance** 查看请求命令类型。
    - 如果请求中的 `COM_STMT_EXECUTE` 数量远大于 `COM_STMT_PREPARE`，说明此设置已生效。

    另外，配置 `useConfigs=maxPerformance` 会同时配置多个参数，包括 `cachePrepStmts=true`。

- **prepStmtCacheSqlLimit**

    配置 `cachePrepStmts` 后，还应关注 `prepStmtCacheSqlLimit`（默认值为 `256`）。此参数控制客户端缓存的 Prepared Statements 的最大长度。

    超过此长度的 Prepared Statements 不会被缓存，无法复用。根据实际 SQL 长度，可能需要调整此值。

    如果你发现：

    - 进入 TiDB 监控面板，通过 **Query Summary** > **CPS By Instance** 查看请求命令类型。
    - 并且已配置 `cachePrepStmts=true`，但 `COM_STMT_PREPARE` 仍主要等于 `COM_STMT_EXECUTE` 和存在 `COM_STMT_CLOSE`，可能说明此参数设置过小。

- **prepStmtCacheSize**

    **prepStmtCacheSize** 控制缓存的 Prepared Statements 数量（默认值为 `25`）。如果你的应用需要“预准备”多种 SQL 语句并复用 Prepared Statements，可以增大此值。

    验证方法：

    - 进入 TiDB 监控面板，通过 **Query Summary** > **CPS By Instance** 查看请求命令类型。
    - 如果请求中的 `COM_STMT_EXECUTE` 数量远大于 `COM_STMT_PREPARE`，说明此设置已生效。

#### 批处理相关参数

在处理批量写入时，建议配置 `rewriteBatchedStatements=true`。使用 `addBatch()` 或 `executeBatch()` 后，JDBC 仍会默认逐条发送 SQL 语句，例如：

```java
pstmt = prepare("INSERT INTO `t` (a) values(?)");
pstmt.setInt(1, 10);
pstmt.addBatch();
pstmt.setInt(1, 11);
pstmt.addBatch();
pstmt.setInt(1, 12);
pstmt.executeBatch();
```

虽然调用了批处理方法，但发往 TiDB 的 SQL 语句仍是单条 `INSERT`：

```sql
INSERT INTO `t` (`a`) VALUES(10);
INSERT INTO `t` (`a`) VALUES(11);
INSERT INTO `t` (`a`) VALUES(12);
```

如果设置 `rewriteBatchedStatements=true`，则会将多条 `INSERT` 语句合并为一条：

```sql
INSERT INTO `t` (`a`) values(10),(11),(12);
```

注意，`INSERT` 语句的重写是将多个 `values` 后的值拼接成一条完整的 SQL 语句。如果 `INSERT` 语句存在其他差异，则无法重写，例如：

```sql
INSERT INTO `t` (`a`) VALUES (10) ON DUPLICATE KEY UPDATE `a` = 10;
INSERT INTO `t` (`a`) VALUES (11) ON DUPLICATE KEY UPDATE `a` = 11;
INSERT INTO `t` (`a`) VALUES (12) ON DUPLICATE KEY UPDATE `a` = 12;
```

上述语句不能合并成一条。但如果改为：

```sql
INSERT INTO `t` (`a`) VALUES (10) ON DUPLICATE KEY UPDATE `a` = VALUES(`a`);
INSERT INTO `t` (`a`) VALUES (11) ON DUPLICATE KEY UPDATE `a` = VALUES(`a`);
INSERT INTO `t` (`a`) VALUES (12) ON DUPLICATE KEY UPDATE `a` = VALUES(`a`);
```

则满足重写条件，最终会被重写为：

```sql
INSERT INTO `t` (`a`) VALUES (10), (11), (12) ON DUPLICATE KEY UPDATE a = VALUES(`a`);
```

如果批量更新中有三条或更多的更新语句，SQL 会被重写并作为多条查询发送。这可以有效减少客户端到服务器的请求开销，但会生成更大的 SQL 语句。例如：

```sql
UPDATE `t` SET `a` = 10 WHERE `id` = 1; UPDATE `t` SET `a` = 11 WHERE `id` = 2; UPDATE `t` SET `a` = 12 WHERE `id` = 3;
```

此外，由于 [客户端 bug](https://bugs.mysql.com/bug.php?id=96623)，如果你在批量更新时配置了 `rewriteBatchedStatements=true` 和 `useServerPrepStmts=true`，建议同时配置 `allowMultiQueries=true` 参数，以避免此 bug。

#### 集成参数

通过监控，你可能会发现虽然应用只对 TiDB 集群执行 `INSERT` 操作，但实际上存在大量冗余的 `SELECT` 语句。通常这是因为 JDBC 发送了一些查询设置的 SQL 语句，例如 `select @@session.transaction_read_only`。这些 SQL 语句对 TiDB 来说是无用的，建议配置 `useConfigs=maxPerformance`，以避免额外开销。

`useConfigs=maxPerformance` 包含一组配置。详细配置请参见 [mysql-connector-j 8.0](https://github.com/mysql/mysql-connector-j/blob/release/8.0/src/main/resources/com/mysql/cj/configurations/maxPerformance.properties) 和 [mysql-connector-j 5.1](https://github.com/mysql/mysql-connector-j/blob/release/5.1/src/com/mysql/jdbc/configs/maxPerformance.properties)。

配置后，可以通过监控观察到 `SELECT` 语句的数量减少。

### 超时相关参数

TiDB 提供两个与 MySQL 兼容的参数控制超时：[`wait_timeout`](/system-variables.md#wait_timeout) 和 [`max_execution_time`](/system-variables.md#max_execution_time)。前者控制连接空闲超时，后者控制 SQL 执行超时；也就是说，这两个参数分别控制 TiDB 与 Java 应用之间连接的最长空闲时间和最长繁忙时间。从 TiDB v5.4 开始，`wait_timeout` 的默认值为 `28800` 秒（即 8 小时）。在 v5.4 之前，默认值为 `0`，表示无限超时。`max_execution_time` 的默认值为 `0`，表示 SQL 最大执行时间无限制。

`wait_timeout` 的默认值较大。在事务未提交或回滚时，可能需要更细粒度的控制和更短的超时时间，以防止长时间持有锁。这时可以使用 [`tidb_idle_transaction_timeout`](/system-variables.md#tidb_idle_transaction_timeout-new-in-v760)（在 TiDB v7.6.0 引入）控制会话中事务的空闲超时。

但在实际生产环境中，空闲连接和超长执行时间的 SQL 会对数据库和应用产生负面影响。为了避免空闲连接和超时执行的 SQL，可以在应用的连接字符串中配置这两个参数。例如，设置 `sessionVariables=wait_timeout=3600`（1 小时）和 `sessionVariables=max_execution_time=300000`（5 分钟）。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>