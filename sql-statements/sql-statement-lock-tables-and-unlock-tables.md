---
title: LOCK TABLES 和 UNLOCK TABLES
summary: TiDB 数据库中 LOCK TABLES 和 UNLOCK TABLES 的用法概述。
---

# LOCK TABLES 和 UNLOCK TABLES

> **Warning:**
>
> `LOCK TABLES` 和 `UNLOCK TABLES` 是当前版本的实验性特性。不建议在生产环境中使用。

TiDB 允许客户端会话获取表锁，以便与其他会话协作访问表，或防止其他会话修改表。一个会话只能为自身获取或释放锁。一个会话不能为其他会话获取锁，也不能释放其他会话持有的锁。

`LOCK TABLES` 为当前客户端会话获取表锁。如果你对每个要加锁的对象拥有 `LOCK TABLES` 和 `SELECT` 权限，则可以为普通表获取表锁。

`UNLOCK TABLES` 显式释放当前会话持有的所有表锁。在获取新锁之前，`LOCK TABLES` 会隐式释放当前会话持有的所有表锁。

表锁可以防止其他会话对表进行读或写操作。持有 `WRITE` 锁的会话可以执行如 `DROP TABLE` 或 `TRUNCATE TABLE` 等表级操作。

> **Note:**
>
> 表锁功能默认是关闭的。
>
> - 对于 TiDB 自建集群，要启用表锁功能，需要在所有 TiDB 实例的配置文件中将 [`enable-table-lock`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#enable-table-lock-new-in-v400) 设置为 `true`。
> - 对于 TiDB Cloud Dedicated，要启用表锁功能，需要联系 [TiDB Cloud Support](https://docs.pingcap.com/tidbcloud/tidb-cloud-support) 将 [`enable-table-lock`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#enable-table-lock-new-in-v400) 设置为 `true`。
> - 对于 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)，不支持将 [`enable-table-lock`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#enable-table-lock-new-in-v400) 设置为 `true`。

## 语法

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

你可以通过 `LOCK TABLES` 语句在当前会话中获取表锁。可用的锁类型如下：

`READ` 锁：

- 持有该锁的会话可以读取表，但不能写入表。
- 多个会话可以同时对同一张表获取 `READ` 锁。
- 其他会话可以在未显式获取 `READ` 锁的情况下读取该表。

`READ LOCAL` 锁仅用于与 MySQL 语法兼容，TiDB 不支持该锁。

`WRITE` 锁：

- 持有该锁的会话可以读写表。
- 只有持有该锁的会话可以访问该表，其他会话在锁释放前无法访问。

`WRITE LOCAL` 锁：

- 持有该锁的会话可以读写表。
- 只有持有该锁的会话可以访问该表，其他会话可以读取该表，但不能写入。

如果 `LOCK TABLES` 语句需要的锁已被其他会话持有，则 `LOCK TABLES` 语句会等待，并在执行该语句时返回错误，例如：

```sql
> LOCK TABLES t1 READ;
ERROR 8020 (HY000): Table 't1' was locked in WRITE by server: f4799bcb-cad7-4285-8a6d-23d3555173f1_session: 2199023255959
```

上述错误信息表示，TiDB `f4799bcb-cad7-4285-8a6d-23d3555173f1` 中会话 ID 为 `2199023255959` 的会话已经持有了表 `t1` 的 `WRITE` 锁。因此，当前会话无法获取表 `t1` 的 `READ` 锁。

在单条 `LOCK TABLES` 语句中，不能对同一张表多次加锁。

```sql
> LOCK TABLES t WRITE, t READ;
ERROR 1066 (42000): Not unique table/alias: 't'
```

## 释放表锁

当会话持有的表锁被释放时，会同时释放所有锁。会话可以显式或隐式释放其锁。

- 会话可以通过 `UNLOCK TABLES` 显式释放锁。
- 如果会话在已持有锁的情况下再次执行 `LOCK TABLES` 语句获取新锁，则会在获取新锁前隐式释放已有的锁。

如果客户端会话的连接终止（无论是正常还是异常），TiDB 会隐式释放该会话持有的所有表锁。如果客户端重新连接，锁将不再生效。因此，不建议在客户端启用自动重连功能。如果启用自动重连，客户端在重连时不会收到通知，所有表锁或当前事务都会丢失。相反，如果禁用自动重连，当连接断开时，下一条语句会报错。客户端可以检测到该错误，并采取相应措施，如重新获取锁或重做事务。

## 表锁的限制与条件

你可以安全地使用 `KILL` 命令终止持有表锁的会话。

不能对以下数据库中的表加表锁：

- `INFORMATION_SCHEMA`
- `PERFORMANCE_SCHEMA`
- `METRICS_SCHEMA`
- `mysql`

## MySQL 兼容性

### 表锁获取

- 在 TiDB 中，如果会话 A 已经持有表锁，当会话 B 尝试写入该表时会返回错误。而在 MySQL 中，会话 B 的写请求会被阻塞，直到会话 A 释放表锁，其他会话对该表的加锁请求也会被阻塞，直到当前会话释放 `WRITE` 锁。
- 在 TiDB 中，如果 `LOCK TABLES` 语句需要的锁已被其他会话持有，则该语句会等待，并在执行时返回错误。而在 MySQL 中，该语句会被阻塞，直到获取到锁为止。
- 在 TiDB 中，`LOCK TABLES` 语句在整个集群范围内生效。而在 MySQL 中，该语句只在当前 MySQL 实例生效，并且不兼容 NDB 集群。

### 表锁释放

当在 TiDB 会话中显式开启事务（例如使用 `BEGIN` 语句）时，TiDB 不会隐式释放该会话持有的表锁；而 MySQL 会隐式释放。