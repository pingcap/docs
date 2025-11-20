---
title: 连接池与连接参数
summary: 本文档介绍如何为 TiDB 配置连接池和连接参数。内容涵盖连接池大小、探测配置、最佳吞吐量的经验公式，同时讨论 JDBC API 的使用及 MySQL Connector/J 参数配置以优化性能。
---

# 连接池与连接参数

本文档描述了当你使用驱动或 ORM 框架连接 TiDB 时，如何配置连接池和连接参数。

<CustomContent platform="tidb">

如果你对 Java 应用开发有更多兴趣，参见 [使用 TiDB 开发 Java 应用的最佳实践](/best-practices/java-app-best-practices.md#connection-pool)

</CustomContent>

<CustomContent platform="tidb-cloud">

如果你对 Java 应用开发有更多兴趣，参见 [使用 TiDB 开发 Java 应用的最佳实践](https://docs.pingcap.com/tidb/stable/java-app-best-practices)

</CustomContent>

## 连接池

建立 TiDB（MySQL）连接的成本相对较高（至少在 OLTP 场景下如此）。因为除了建立 TCP 连接外，还需要进行连接认证。因此，客户端通常会将 TiDB（MySQL）连接保存在连接池中以复用。

Java 有许多连接池实现，例如 [HikariCP](https://github.com/brettwooldridge/HikariCP)、[tomcat-jdbc](https://tomcat.apache.org/tomcat-10.1-doc/jdbc-pool.html)、[druid](https://github.com/alibaba/druid)、[c3p0](https://www.mchange.com/projects/c3p0/)、[dbcp](https://commons.apache.org/proper/commons-dbcp/)。TiDB 不限制你使用哪种连接池，因此你可以根据应用选择任意实现。

### 配置连接数

通常的做法是根据应用自身需求合理调整连接池大小。以 HikariCP 为例：

- **maximumPoolSize**：连接池中的最大连接数。如果该值过大，TiDB 会消耗资源维护无用连接；如果该值过小，应用获取连接会变慢。因此需要根据应用特性合理配置。详情参见 [About Pool Sizing](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing)。
- **minimumIdle**：连接池中最小空闲连接数。主要用于在应用空闲时预留部分连接以应对突发请求，也需根据应用特性配置。

应用在使用完连接后需要及时归还。建议应用使用相应的连接池监控（如 **metricRegistry**）及时定位连接池问题。

### 配置连接生命周期

当 TiDB 服务端关闭、维护重启，或遇到硬件、网络等异常时，现有客户端连接可能会被重置，导致应用中断。为避免此类问题，建议每天至少关闭并重建一次长时间运行的数据库连接。

大多数连接池库都提供了控制连接最大生命周期的参数：

<SimpleTab>
<div label="HikariCP">

- **`maxLifetime`**：连接在池中的最大生命周期。

</div>

<div label="tomcat-jdbc">

- **`maxAge`**：连接在池中的最大生命周期。

</div>

<div label="c3p0">

- **`maxConnectionAge`**：连接在池中的最大生命周期。

</div>

<div label="dbcp">

- **`maxConnLifetimeMillis`**：连接在池中的最大生命周期。

</div>
</SimpleTab>

### 探测配置

连接池维护客户端到 TiDB 的持久连接，具体如下：

- v5.4 之前，TiDB 默认不会主动关闭客户端连接（除非报错）。
- 从 v5.4 起，TiDB 默认在连接空闲 `28800` 秒（即 `8` 小时）后自动关闭客户端连接。你可以通过 TiDB 及 MySQL 兼容的 `wait_timeout` 变量控制该超时时间。详情参见 [JDBC 查询超时](/develop/dev-guide-timeouts-in-tidb.md#jdbc-query-timeout)。

此外，客户端与 TiDB 之间可能存在如 [LVS](https://en.wikipedia.org/wiki/Linux_Virtual_Server) 或 [HAProxy](https://en.wikipedia.org/wiki/HAProxy) 等网络代理。这些代理通常会在连接空闲一段时间后主动清理连接（由代理的空闲配置决定）。除了关注代理的空闲配置外，连接池还需通过保活或探测机制维护连接。

如果你在 Java 应用中经常看到如下错误：

```
The last packet sent successfully to the server was 3600000 milliseconds ago. The driver has not received any packets from the server. com.mysql.jdbc.exceptions.jdbc4.CommunicationsException: Communications link failure
```

如果 `n milliseconds ago` 中的 `n` 为 `0` 或很小，通常是执行的 SQL 操作导致 TiDB 异常退出。建议检查 TiDB 的 stderr 日志以定位原因。

如果 `n` 很大（如上述例子中的 `3600000`），很可能是该连接长时间空闲后被代理关闭。常见解决方法是增大代理的空闲配置，并让连接池：

- 每次使用连接前检查连接是否可用；
- 定期通过独立线程检查连接可用性；
- 定期发送测试查询以保持连接活跃。

不同连接池实现可能支持上述一种或多种方式。你可以查阅连接池文档，找到对应配置。

### 经验公式

根据 HikariCP 的 [About Pool Sizing](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing) 文章，如果你不清楚如何设置数据库连接池的合适大小，可以先采用 [经验公式](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing#connections--core_count--2--effective_spindle_count) 进行初步配置，再根据实际性能结果进一步调整以获得最佳性能。

经验公式如下：

```
connections = ((core_count * 2) + effective_spindle_count)
```

各参数说明如下：

- **connections**：得到的连接数大小。
- **core_count**：CPU 核心数。
- **effective_spindle_count**：硬盘数量（不包括 [SSD](https://en.wikipedia.org/wiki/Solid-state_drive)）。每个机械硬盘可视为一个 spindle。例如，若服务器为 16 盘 RAID，则 **effective_spindle_count** 为 16。因为 **HDD** 通常一次只能处理一个请求，该公式实际衡量服务器可管理的并发 I/O 请求数。

特别需要注意 [公式](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing#the-formula) 下方的说明：

> ```
> 多年来在大量基准测试中表现良好的经验公式是：为获得最佳吞吐量，活跃连接数应接近 ((core_count * 2) + effective_spindle_count)。core_count 不应包含 HT 线程，即使启用了超线程。若活跃数据集完全缓存，effective_spindle_count 为 0；随着缓存命中率下降，该值趋近于实际硬盘数。……目前尚无该公式对 SSD 适用性的分析。
> ```

该说明指出：

- **core_count** 是物理核心数，无论是否启用 [超线程](https://en.wikipedia.org/wiki/Hyper-threading)。
- 当数据完全缓存时，**effective_spindle_count** 设为 `0`；随着缓存命中率降低，该值接近实际 `HDD` 数量。
- **该公式对 _SSD_ 是否适用尚未验证。**

若使用 SSD，建议采用如下经验公式：

```
connections = (number of cores * 4)
```

因此，在使用 SSD 的情况下，可以将初始连接池最大连接数设置为 `cores * 4`，再根据实际性能进一步调整。

### 调优方向

如你所见，基于 [经验公式](#经验公式) 计算的值只是推荐的基准值。要获得特定机器上的最优值，需要围绕基准值尝试其他数值并测试性能。

以下是一些基本规则，帮助你获得最优连接池大小：

- 如果网络或存储延迟较高，增加最大连接数以减少等待延迟。一旦某线程因延迟阻塞，其他线程可继续处理。
- 若服务器上部署了多个服务且每个服务有独立连接池，需考虑所有连接池最大连接数的总和。

## 连接参数

Java 应用通常会被各种框架封装。在大多数框架中，底层通过 JDBC API 与数据库服务器交互。对于 JDBC，建议关注以下内容：

- JDBC API 的使用选择
- API 实现者的参数配置

### JDBC API

关于 JDBC API 的使用，参见 [JDBC 官方教程](https://docs.oracle.com/javase/tutorial/jdbc/)。本节介绍几个重要 API 的用法。

#### 使用 Prepare API

在 OLTP（联机事务处理）场景下，程序发送到数据库的 SQL 语句类型有限，去除参数变化后可穷举。因此，建议使用 [Prepared Statements](https://docs.oracle.com/javase/tutorial/jdbc/basics/prepared.html) 替代常规的 [文本执行](https://docs.oracle.com/javase/tutorial/jdbc/basics/processingsqlstatements.html#executing_queries)，并复用 Prepared Statements 直接执行。这样可避免 TiDB 反复解析和生成 SQL 执行计划的开销。

目前大多数上层框架执行 SQL 时会调用 Prepare API。如果你直接使用 JDBC API 开发，请注意选择 Prepare API。

此外，MySQL Connector/J 默认实现仅在客户端预处理语句，`?` 替换后以文本方式发送到服务端。因此，除了使用 Prepare API，还需在 JDBC 连接参数中配置 `useServerPrepStmts = true`，才能在 TiDB 服务端进行语句预处理。详细参数配置参见 [MySQL JDBC 参数](#mysql-jdbc-参数)。

#### 使用 Batch API

对于批量插入，可以使用 [`addBatch`/`executeBatch` API](https://www.tutorialspoint.com/jdbc/jdbc-batch-processing)。`addBatch()` 方法用于先在客户端缓存多条 SQL 语句，调用 `executeBatch` 方法时再一并发送到数据库服务器。

> **注意：**
>
> 在 MySQL Connector/J 默认实现中，`addBatch()` 添加到批中的 SQL 语句会延迟到调用 `executeBatch()` 时发送，但实际网络传输时仍是一条条发送。因此通常无法减少通信开销。
>
> 若需批量网络传输，需要在 JDBC 连接参数中配置 `rewriteBatchedStatements = true`。详细参数配置参见 [批量相关参数](#批量相关参数)。

#### 使用 `StreamingResult` 获取执行结果

大多数场景下，为提升执行效率，JDBC 默认会提前获取查询结果并保存在客户端内存。但当查询返回超大结果集时，客户端通常希望数据库服务端每次返回较少记录，待客户端内存准备好并请求下一批时再返回。

JDBC 通常有两种处理方式：

- 第一种方式：[将 **FetchSize** 设置为 `Integer.MIN_VALUE`](https://dev.mysql.com/doc/connector-j/en/connector-j-reference-implementation-notes.html#ResultSet)，确保客户端不做缓存。客户端通过 `StreamingResult` 从网络连接读取执行结果。

    当客户端采用流式读取方式时，需在继续使用该 statement 查询前，先读取完或关闭 `resultset`。否则会报错：`No statements may be issued when any streaming result sets are open and in use on a given connection. Ensure that you have called .close() on any active streaming result sets before attempting more queries.`

    若希望在客户端未读取完或关闭 `resultset` 前避免此类错误，可在 URL 中添加 `clobberStreamingResults=true` 参数。这样会自动关闭 `resultset`，但会丢弃前一次流式查询未读取完的结果集。

- 第二种方式：通过先 [设置 `FetchSize`](http://makejavafaster.blogspot.com/2015/06/jdbc-fetch-size-performance.html) 为正整数，再在 JDBC URL 中配置 `useCursorFetch = true`，实现 Cursor Fetch。

TiDB 支持上述两种方式，但推荐使用第一种将 `FetchSize` 设为 `Integer.MIN_VALUE` 的方式，因为实现更简单且执行效率更高。

对于第二种方式，TiDB 首先会将所有数据加载到 TiDB 节点，然后根据 `FetchSize` 返回给客户端。因此通常比第一种方式消耗更多内存。如果 [`tidb_enable_tmp_storage_on_oom`](/system-variables.md#tidb_enable_tmp_storage_on_oom) 设为 `ON`，TiDB 可能会临时将结果写入硬盘。

如果 [`tidb_enable_lazy_cursor_fetch`](/system-variables.md#tidb_enable_lazy_cursor_fetch-new-in-v830) 系统变量设为 `ON`，TiDB 会在客户端获取数据时才尝试读取部分数据，从而减少内存占用。更多详情及限制，参见 [`tidb_enable_lazy_cursor_fetch` 系统变量完整说明](/system-variables.md#tidb_enable_lazy_cursor_fetch-new-in-v830)。

### MySQL JDBC 参数

JDBC 通常以 JDBC URL 参数的形式提供实现相关配置。本节介绍 [MySQL Connector/J 的参数配置](https://dev.mysql.com/doc/connector-j/en/connector-j-reference-configuration-properties.html)（如使用 MariaDB，参见 [MariaDB 的参数配置](https://mariadb.com/docs/connectors/mariadb-connector-j/about-mariadb-connector-j#optional-url-parameters)）。由于本文无法覆盖所有配置项，主要关注可能影响性能的几个参数。

#### Prepare 相关参数

本节介绍与 `Prepare` 相关的参数。

- **useServerPrepStmts**

    **useServerPrepStmts** 默认设为 `false`，即使你使用 Prepare API，"prepare" 操作也只在客户端完成。为避免服务端解析开销，若同一 SQL 语句多次使用 Prepare API，建议将该配置设为 `true`。

    验证该设置是否生效的方法：

    - 进入 TiDB 监控面板，通过 **Query Summary** > **CPS By Instance** 查看请求命令类型。
    - 若请求中的 `COM_QUERY` 被 `COM_STMT_EXECUTE` 或 `COM_STMT_PREPARE` 替代，说明该设置已生效。

- **cachePrepStmts**

    虽然 `useServerPrepStmts=true` 允许服务端执行 Prepared Statements，但默认情况下，客户端每次执行后都会关闭 Prepared Statements，不做复用。这意味着 "prepare" 操作效率甚至不如文本执行。为解决此问题，建议在设置 `useServerPrepStmts=true` 后，同时配置 `cachePrepStmts=true`，以便客户端缓存 Prepared Statements。

    验证该设置是否生效的方法：

    - 进入 TiDB 监控面板，通过 **Query Summary** > **CPS By Instance** 查看请求命令类型。
    - 若请求中的 `COM_STMT_EXECUTE` 数量远大于 `COM_STMT_PREPARE`，说明该设置已生效。

    此外，配置 `useConfigs=maxPerformance` 会同时配置多个参数，包括 `cachePrepStmts=true`。

- **prepStmtCacheSqlLimit**

    配置了 `cachePrepStmts` 后，还需关注 `prepStmtCacheSqlLimit`（默认值为 `256`）。该配置控制客户端缓存的 Prepared Statements 的最大长度。

    超过该长度的 Prepared Statements 不会被缓存，无法复用。此时可根据应用实际 SQL 长度考虑增大该值。

    若需检查该设置是否过小，可：

    - 进入 TiDB 监控面板，通过 **Query Summary** > **CPS By Instance** 查看请求命令类型。
    - 若已配置 `cachePrepStmts=true`，但 `COM_STMT_PREPARE` 仍与 `COM_STMT_EXECUTE` 数量接近且存在 `COM_STMT_CLOSE`，则需关注该参数。

- **prepStmtCacheSize**

    **prepStmtCacheSize** 控制缓存的 Prepared Statements 数量（默认值为 `25`）。如应用需 "prepare" 多种 SQL 并希望复用 Prepared Statements，可增大该值。

    验证该设置是否生效的方法：

    - 进入 TiDB 监控面板，通过 **Query Summary** > **CPS By Instance** 查看请求命令类型。
    - 若请求中的 `COM_STMT_EXECUTE` 数量远大于 `COM_STMT_PREPARE`，说明该设置已生效。

#### 批量相关参数

处理批量写入时，建议配置 `rewriteBatchedStatements=true`。在使用 `addBatch()` 或 `executeBatch()` 后，JDBC 默认仍会一条条发送 SQL，例如：

```java
pstmt = prepare("INSERT INTO `t` (a) values(?)");
pstmt.setInt(1, 10);
pstmt.addBatch();
pstmt.setInt(1, 11);
pstmt.addBatch();
pstmt.setInt(1, 12);
pstmt.executeBatch();
```

虽然使用了 `Batch` 方法，发送到 TiDB 的 SQL 仍是单条 `INSERT` 语句：

```sql
INSERT INTO `t` (`a`) VALUES(10);
INSERT INTO `t` (`a`) VALUES(11);
INSERT INTO `t` (`a`) VALUES(12);
```

但若设置了 `rewriteBatchedStatements=true`，发送到 TiDB 的 SQL 会变为一条 `INSERT` 语句：

```sql
INSERT INTO `t` (`a`) values(10),(11),(12);
```

注意，`INSERT` 语句的重写是将多条 "values" 后的值拼接为一条 SQL。若 `INSERT` 语句有其他差异，则无法重写，例如：

```sql
INSERT INTO `t` (`a`) VALUES (10) ON DUPLICATE KEY UPDATE `a` = 10;
INSERT INTO `t` (`a`) VALUES (11) ON DUPLICATE KEY UPDATE `a` = 11;
INSERT INTO `t` (`a`) VALUES (12) ON DUPLICATE KEY UPDATE `a` = 12;
```

上述 `INSERT` 语句无法重写为一条。但若将三条语句改为：

```sql
INSERT INTO `t` (`a`) VALUES (10) ON DUPLICATE KEY UPDATE `a` = VALUES(`a`);
INSERT INTO `t` (`a`) VALUES (11) ON DUPLICATE KEY UPDATE `a` = VALUES(`a`);
INSERT INTO `t` (`a`) VALUES (12) ON DUPLICATE KEY UPDATE `a` = VALUES(`a`);
```

则满足重写要求，最终会被重写为：

```sql
INSERT INTO `t` (`a`) VALUES (10), (11), (12) ON DUPLICATE KEY UPDATE a = VALUES(`a`);
```

若批量更新时有三条及以上更新，SQL 会被重写并作为多条查询发送。这样可有效减少客户端到服务端的请求开销，但副作用是生成更大的 SQL 语句。例如：

```sql
UPDATE `t` SET `a` = 10 WHERE `id` = 1; UPDATE `t` SET `a` = 11 WHERE `id` = 2; UPDATE `t` SET `a` = 12 WHERE `id` = 3;
```

此外，由于 [客户端 bug](https://bugs.mysql.com/bug.php?id=96623)，若你在批量更新时配置了 `rewriteBatchedStatements=true` 和 `useServerPrepStmts=true`，建议同时配置 `allowMultiQueries=true` 参数以避免该 bug。

#### 集成参数

通过监控你可能会发现，虽然应用只对 TiDB 集群执行 `INSERT` 操作，但存在大量冗余的 `SELECT` 语句。通常是因为 JDBC 会发送一些查询设置的 SQL，例如 `select @@session.transaction_read_only`。这些 SQL 对 TiDB 无用，建议配置 `useConfigs=maxPerformance` 以避免额外开销。

`useConfigs=maxPerformance` 包含一组配置。MySQL Connector/J 8.0 及 5.1 的详细配置分别见 [mysql-connector-j 8.0](https://github.com/mysql/mysql-connector-j/blob/release/8.0/src/main/resources/com/mysql/cj/configurations/maxPerformance.properties) 和 [mysql-connector-j 5.1](https://github.com/mysql/mysql-connector-j/blob/release/5.1/src/com/mysql/jdbc/configs/maxPerformance.properties)。

配置后，你可以通过监控看到 `SELECT` 语句数量减少。

#### 超时相关参数

TiDB 提供了两个 MySQL 兼容参数用于控制超时：[`wait_timeout`](/system-variables.md#wait_timeout) 和 [`max_execution_time`](/system-variables.md#max_execution_time)。这两个参数分别控制与 Java 应用的连接空闲超时和连接中 SQL 执行的超时，即分别控制 TiDB 与 Java 应用之间连接的最长空闲时间和最长繁忙时间。自 TiDB v5.4 起，`wait_timeout` 默认值为 `28800` 秒（8 小时）；v5.4 之前默认值为 `0`，即无限制。`max_execution_time` 默认值为 `0`，即 SQL 语句最大执行时间无限制，适用于所有 `SELECT` 语句（包括 `SELECT ... FOR UPDATE`）。

[`wait_timeout`](/system-variables.md#wait_timeout) 默认值较大。在事务已开启但未提交或回滚的场景下，可能需要更细粒度、更短的超时以避免长时间持锁。此时可使用 [`tidb_idle_transaction_timeout`](/system-variables.md#tidb_idle_transaction_timeout-new-in-v760)（TiDB v7.6.0 引入）控制用户会话中事务的空闲超时。

但在实际生产环境中，空闲连接和执行时间过长的 SQL 语句会对数据库和应用产生负面影响。为避免空闲连接和长时间执行的 SQL，可在应用连接串中配置这两个参数。例如，设置 `sessionVariables=wait_timeout=3600`（1 小时）和 `sessionVariables=max_execution_time=300000`（5 分钟）。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
