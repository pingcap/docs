---
title: KILL
summary: TiDB 数据库中 KILL 语句的使用概况。
---

# KILL

`KILL` 语句用于终止当前 TiDB 集群中任意 TiDB 实例上的连接。从 TiDB v6.2.0 开始，`KILL` 语句还可以终止正在执行的 DDL 作业。

## 语法图

```ebnf+diagram
KillStmt ::= 'KILL' 'TIDB'? ( 'CONNECTION' | 'QUERY' )? CONNECTION_ID
```

## 示例

以下示例展示如何查询当前集群中所有正在执行的查询，并终止其中一个查询所在的连接。

{{< copyable "sql" >}}

```sql
SELECT ID, USER, INSTANCE, INFO FROM INFORMATION_SCHEMA.CLUSTER_PROCESSLIST;
```

```
+---------------------+------+-----------------+-----------------------------------------------------------------------------+
| ID                  | USER | INSTANCE        | INFO                                                                        |
+---------------------+------+-----------------+-----------------------------------------------------------------------------+
| 8306449708033769879 | root | 127.0.0.1:10082 | select sleep(30), 'foo'                                                     |
| 5857102839209263511 | root | 127.0.0.1:10080 | select sleep(50)                                                            |
| 5857102839209263513 | root | 127.0.0.1:10080 | SELECT ID, USER, INSTANCE, INFO FROM INFORMATION_SCHEMA.CLUSTER_PROCESSLIST |
+---------------------+------+-----------------+-----------------------------------------------------------------------------+
```

{{< copyable "sql" >}}

```sql
KILL 5857102839209263511;
```

```
Query OK, 0 rows affected (0.00 sec)
```

## MySQL 兼容性

- MySQL 的 `KILL` 语句只能终止当前连接的 MySQL 实例上的连接，而 TiDB 的 `KILL` 语句可以终止整个集群中任意 TiDB 实例上的连接。
- TiDB v7.2.0 及之前的版本不支持通过 MySQL 命令行中的 <kbd>Control+C</kbd> 终止查询或连接。

## 行为变更说明

<CustomContent platform="tidb">

从 v7.3.0 开始，TiDB 支持生成 32 位 connection ID。该功能默认启用，由 [`enable-32bits-connection-id`](/tidb-configuration-file.md#enable-32bits-connection-id-从-v730-版本开始引入) 配置项控制。同时启用 Global Kill 功能和 32 位 connection ID 后，TiDB 会生成 32 位 connection ID，支持在 MySQL 命令行中通过 <kbd>Control+C</kbd> 终止查询或连接。

> **警告：**
>
> 当集群中的 TiDB 实例数量超过 2048，或者单个 TiDB 实例的并发连接数超过 1048576 时，由于 32 位 connection ID 空间不足，TiDB 会自动升级为 64 位 connection ID。升级过程不会影响现有业务和已建立的连接，但后续新建的连接将无法通过 MySQL 命令行中的 <kbd>Control+C</kbd> 终止。

从 v6.1.0 开始，TiDB 支持 Global Kill 功能。该功能默认启用，由 [`enable-global-kill`](/tidb-configuration-file.md#enable-global-kill-从-v610-版本开始引入) 配置项控制。

</CustomContent>

<CustomContent platform="tidb-cloud">

从 v7.3.0 开始，TiDB 支持生成 32 位 connection ID，且默认启用该功能。同时启用 Global Kill 功能和 32 位 connection ID 后，可以在 MySQL 命令行中通过 <kbd>Control+C</kbd> 终止查询或连接。

从 v6.1.0 开始，TiDB 支持 Global Kill 功能，且默认启用该功能。

</CustomContent>

启用 Global Kill 功能后，`KILL` 和 `KILL TIDB` 语句均可以跨实例终止查询或连接，无需担心误终止其他查询或连接。当你使用客户端连接到任意 TiDB 实例并执行 `KILL` 或 `KILL TIDB` 语句时，该语句会被转发到目标 TiDB 实例。如果客户端与 TiDB 集群之间存在代理，`KILL` 和 `KILL TIDB` 语句也会被转发到目标 TiDB 实例执行。

如果未启用 Global Kill 功能，或者使用的是 v6.1.0 之前的 TiDB 版本，需要注意以下事项：

- 默认情况下，`KILL` 语句与 MySQL 不兼容。由于通常会在负载均衡器后部署多个 TiDB 实例，这种不兼容性有助于防止连接被错误的 TiDB 实例终止。要终止当前连接的 TiDB 实例上的其他连接，需要显式添加 `TIDB` 后缀，即执行 `KILL TIDB` 语句。

<CustomContent platform="tidb">

- **强烈不建议**在配置文件中设置 [`compatible-kill-query = true`](/tidb-configuration-file.md#compatible-kill-query)，**除非**你能确保客户端始终连接到同一个 TiDB 实例。这是因为，在默认的 MySQL 客户端中按下 <kbd>Control+C</kbd> 时，客户端会建立一个新连接，并通过该连接执行 `KILL` 语句。如果客户端与 TiDB 集群之间存在代理，新连接可能会被路由到其他 TiDB 实例，从而误终止其他会话。

</CustomContent>

- `KILL TIDB` 语句是 TiDB 的扩展语法，其功能与 MySQL 的 `KILL [CONNECTION|QUERY]` 命令及 MySQL 命令行中的 <kbd>Control+C</kbd> 类似。在同一个 TiDB 实例上，可以安全地使用 `KILL TIDB` 语句。

## 另请参阅

* [SHOW \[FULL\] PROCESSLIST](/sql-statements/sql-statement-show-processlist.md)
* [CLUSTER_PROCESSLIST](/information-schema/information-schema-processlist.md#cluster_processlist)
