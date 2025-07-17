---
title: Locking Functions
summary: 了解 TiDB 中的用户级锁定函数。
---

# Locking Functions

TiDB 支持大部分在 MySQL 8.0 中可用的 [locking functions](https://dev.mysql.com/doc/refman/8.0/en/locking-functions.html)。

## 支持的函数

| Name                                                                                                                 | Description                                                           |
|:---------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------|
| [`GET_LOCK(lockName, timeout)`](https://dev.mysql.com/doc/refman/8.0/en/locking-functions.html#function_get-lock)    | 获取一个建议锁。`lockName` 参数的长度不能超过 64 个字符。等待最多 `timeout` 秒后超时并返回失败。         |
| [`IS_FREE_LOCK(lockName)`](https://dev.mysql.com/doc/refman/8.0/en/locking-functions.html#function_is-free-lock) | 检查锁是否为空闲。 |
| [`IS_USED_LOCK(lockName)`](https://dev.mysql.com/doc/refman/8.0/en/locking-functions.html#function_is-used-lock) | 检查锁是否被使用。如果为 true，则返回对应的连接 ID。 |
| [`RELEASE_ALL_LOCKS()`](https://dev.mysql.com/doc/refman/8.0/en/locking-functions.html#function_release-all-locks)   | 释放当前会话持有的所有锁。                        |
| [`RELEASE_LOCK(lockName)`](https://dev.mysql.com/doc/refman/8.0/en/locking-functions.html#function_release-lock)     | 释放之前获取的锁。`lockName` 参数的长度不能超过 64 个字符。 |

## MySQL 兼容性

* TiDB 允许的最小超时时间为 1 秒，最大超时时间为 1 小时（3600 秒）。这与 MySQL 不同，MySQL 允许超时时间为 0 秒或无限（`timeout=-1`）。TiDB 会自动将超出范围的值转换为最接近的允许值，并将 `timeout=-1` 转换为 3600 秒。
* TiDB 不会自动检测由用户级锁引起的死锁。死锁会在最多 1 小时后超时，但也可以通过对受影响的会话使用 [`KILL`](/sql-statements/sql-statement-kill.md) 来手动解决。你还可以通过始终以相同顺序获取用户级锁来防止死锁。
* 锁在集群中的所有 TiDB 服务器上生效。这与 MySQL Cluster 和 Group Replication 不同，后者的锁是局部于单个服务器的。
* `IS_USED_LOCK()` 如果在另一个会话中调用，则返回 `1`，但无法返回持有锁的进程的 ID。