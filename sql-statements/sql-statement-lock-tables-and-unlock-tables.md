---
title: LOCK TABLES 和 UNLOCK TABLES
summary: 关于 TiDB 数据库中 LOCK TABLES 和 UNLOCK TABLES 的使用概述。
---

# LOCK TABLES 和 UNLOCK TABLES

> **Warning:**
>
> `LOCK TABLES` 和 `UNLOCK TABLES` 是当前版本的实验性功能。不建议在生产环境中使用。

TiDB 允许客户端会话获取表锁，以配合其他会话访问表，或防止其他会话修改表。一个会话只能为自己获取或释放锁。一个会话不能为其他会话获取锁或释放其他会话持有的锁。

`LOCK TABLES` 为当前客户端会话获取表锁。如果你对每个要锁定的对象拥有 `LOCK TABLES` 和 `SELECT` 权限，则可以为普通表获取表锁。

`UNLOCK TABLES` 明确释放当前会话持有的所有表锁。`LOCK TABLES` 在获取新锁之前会隐式释放当前会话持有的所有表锁。

表锁可以防止其他会话进行读取或写入。持有 `WRITE` 锁的会话可以执行诸如 `DROP TABLE` 或 `TRUNCATE TABLE` 等表级操作。

> **Note:**
>
> 表锁功能默认未开启。
>
> - 对于 TiDB 自托管版本，要启用表锁功能，需要在所有 TiDB 实例的配置文件中将 [`enable-table-lock`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#enable-table-lock-new-in-v400) 设置为 `true`。
> - 对于 TiDB Cloud Dedicated，要启用表锁功能，需要联系 [TiDB Cloud Support](https://docs.pingcap.com/tidbcloud/tidb-cloud-support) 设置 [`enable-table-lock`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#enable-table-lock-new-in-v400) 为 `true`。
> - 对于 {{{ .starter }}}，不支持将 [`enable-table-lock`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#enable-table-lock-new-in-v400) 设置为 `true`。

## 概要

```ebnf+diagram
LockTablesDef
         ::= 'LOCK' ( 'TABLES' | 'TABLE' ) TableName LockType ( ',' TableName LockType)*


UnlockTablesDef
         ::= 'UNLOCK' 'TABLES'

LockType
         ::= 'READ' ('LOCAL')?
           | 'WRITE' ('LOCAL')?
```

## 获取表锁

你可以在当前会话中使用 `LOCK TABLES` 语句获取表锁。可用的锁类型包括：

`READ` 锁：

- 持有此锁的会话可以读取表，但不能写入。
- 多个会话可以同时对同一表获取 `READ` 锁。
- 其他会话可以在没有显式获取 `READ` 锁的情况下读取表。

`READ LOCAL` 锁 仅用于与 MySQL 的语法兼容，不支持。

`WRITE` 锁：

- 持有此锁的会话可以读取和写入表。
- 只有持有此锁的会话可以访问该表。在锁释放之前，其他会话不能访问。

`WRITE LOCAL` 锁：

- 持有此锁的会话可以读取和写入表。
- 只有持有此锁的会话可以访问该表。其他会话可以读取，但不能写入。

如果 `LOCK TABLES` 语句需要的锁被其他会话持有，则该语句必须等待，执行时会返回错误，例如：

```sql
> LOCK TABLES t1 READ;
ERROR 8020 (HY000): Table 't1' was locked in WRITE by server: f4799bcb-cad7-4285-8a6d-23d3555173f1_session: 2199023255959
```

上述错误信息表示，TiDB 中 ID 为 `2199023255959` 的会话在 `f4799bcb-cad7-4285-8a6d-23d3555173f1` 实例中已对表 `t1` 持有 `WRITE` 锁。因此，当前会话无法对 `t1` 获取 `READ` 锁。

在单个 `LOCK TABLES` 语句中，不能对同一表多次获取锁。

```sql
> LOCK TABLES t WRITE, t READ;
ERROR 1066 (42000): Not unique table/alias: 't'
```

## 释放表锁

当会话持有的表锁被释放时，全部同时释放。会话可以显式或隐式释放其锁。

- 会话可以通过 `UNLOCK TABLES` 显式释放锁。
- 如果会话在已持有锁的情况下再次执行 `LOCK TABLES`，其现有的锁会在获取新锁之前被隐式释放。

如果客户端会话的连接正常或异常终止，TiDB 会隐式释放该会话持有的所有表锁。如果客户端重新连接，之前的锁将不再生效。因此，不建议开启客户端的自动重连功能。如果开启自动重连，重连时客户端不会收到通知，所有表锁或当前事务将丢失。相反，禁用自动重连后，如果连接断开，下一条语句执行时会出现错误。客户端可以检测到错误并采取相应措施，例如重新获取锁或重做事务。

## 表锁限制与条件

你可以安全地使用 `KILL` 来终止持有表锁的会话。

不能对以下数据库中的表获取表锁：

- `INFORMATION_SCHEMA`
- `PERFORMANCE_SCHEMA`
- `METRICS_SCHEMA`
- `mysql`

## MySQL 兼容性

### 表锁获取

- 在 TiDB 中，如果会话 A 已经持有表锁，则当会话 B 尝试对该表写入时，会返回错误。在 MySQL 中，会话 B 的写请求会被阻塞，直到会话 A 释放表锁；其他会话请求锁定该表也会被阻塞，直到当前会话释放 `WRITE` 锁。
- 在 TiDB 中，如果 `LOCK TABLES` 语句需要的锁被其他会话持有，则该语句必须等待，执行时会返回错误。在 MySQL 中，该语句会被阻塞，直到锁被获取。
- 在 TiDB 中，`LOCK TABLES` 语句在整个集群中生效。在 MySQL 中，该语句仅在当前 MySQL 服务器中生效，不兼容 NDB 集群。

### 表锁释放

当在 TiDB 会话中显式启动事务（例如使用 `BEGIN` 语句）时，TiDB 不会隐式释放会话持有的表锁；而 MySQL 会。