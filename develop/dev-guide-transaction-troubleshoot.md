---
title: 处理事务错误
summary: 了解如何处理事务错误，例如死锁和应用重试错误。
---

# 处理事务错误

本文介绍了如何处理事务错误，例如死锁和应用重试错误。

## 死锁

在你的应用中出现以下错误，表示存在死锁问题：

```sql
ERROR 1213: Deadlock found when trying to get lock; try restarting transaction
```

死锁发生在两个或多个事务相互等待对方释放已持有的锁，或者由于锁的不一致顺序导致形成循环等待资源。

以下是使用 [`bookshop`](/develop/dev-guide-bookshop-schema-design.md) 数据库中的 `books` 表的死锁示例：

首先，向 `books` 表插入 2 行数据：

```sql
INSERT INTO books (id, title, stock, published_at) VALUES (1, 'book-1', 10, now()), (2, 'book-2', 10, now());
```

在 TiDB 悲观事务模式下，如果两个客户端分别执行以下语句，就会发生死锁：

| 客户端-A                                                    | 客户端-B                                                          |
| --------------------------------------------------------------| -------------------------------------------------------------------|
| BEGIN;                                                        |                                                                     |
|                                                               | BEGIN;                                                              |
| UPDATE books SET stock=stock-1 WHERE id=1;                     |                                                                     |
|                                                               | UPDATE books SET stock=stock-1 WHERE id=2;                          |
| UPDATE books SET stock=stock-1 WHERE id=2; -- 执行将被阻塞        |                                                                     |
|                                                               | UPDATE books SET stock=stock-1 WHERE id=1; -- 发生死锁错误             |

当客户端-B遇到死锁错误后，TiDB 会自动回滚客户端-B中的事务。客户端-A对 `id=2` 的更新将成功执行。你可以随后运行 `COMMIT` 完成事务。

### 解决方案 1：避免死锁

为了获得更好的性能，你可以在应用层通过调整业务逻辑或模式设计来避免死锁。在上述示例中，如果客户端-B也采用与客户端-A相同的更新顺序，即先更新 `id=1` 的书，然后再更新 `id=2` 的书，就可以避免死锁：

| 客户端-A                                                    | 客户端-B                                                          |
| --------------------------------------------------------------| -------------------------------------------------------------------|
| BEGIN;                                                        |                                                                     |
|                                                               | BEGIN;                                                              |
| UPDATE books SET stock=stock-1 WHERE id=1;                     |                                                                     |
|                                                               | UPDATE books SET stock=stock-1 WHERE id=1;  -- 将被阻塞                |
| UPDATE books SET stock=stock-1 WHERE id=2;                     |                                                                     |
| COMMIT;                                                       |                                                                     |
|                                                               | UPDATE books SET stock=stock-1 WHERE id=2;                          |
|                                                               | COMMIT;                                                            |

或者，你也可以用一条 SQL 语句同时更新两个书的库存，从而避免死锁并提高执行效率：

```sql
UPDATE books SET stock=stock-1 WHERE id IN (1, 2);
```

### 解决方案 2：降低事务粒度

如果你每次只更新一本书，也可以避免死锁。但需要注意，过小的事务粒度可能会影响性能。

### 解决方案 3：使用乐观事务

乐观事务模型中不存在死锁问题。但在你的应用中，需要添加乐观事务的重试逻辑，以应对失败情况。详情请参见 [Application retry and error handling](#application-retry-and-error-handling)。

### 解决方案 4：重试

在应用中加入重试逻辑，按照错误信息中的建议进行处理。详情请参见 [Application retry and error handling](#application-retry-and-error-handling)。

## 应用重试和错误处理

虽然 TiDB 与 MySQL 兼容性很高，但其分布式系统的特性导致一些差异。其中之一是事务模型。

开发者用来连接数据库的适配器和 ORM 通常是为传统数据库（如 MySQL 和 Oracle）量身定制的。在这些数据库中，事务在默认隔离级别下很少无法提交，因此不需要重试机制。当事务提交失败时，这些客户端会因错误而中止，视为异常。

不同于传统数据库（如 MySQL），在 TiDB 中，如果你使用乐观事务模型，为了避免提交失败，你需要在应用中添加处理相关异常的机制。

以下是用 Python 伪代码演示如何实现应用层的重试逻辑。它不要求你的驱动或 ORM 实现复杂的重试机制，适用于任何编程语言或环境。

你的重试逻辑必须遵循以下规则：

- 当失败重试次数达到 `max_retries` 限制时，抛出错误。
- 使用 `try ... catch ...` 捕获 SQL 执行异常。遇到以下错误时重试，遇到其他错误则回滚。
    - `Error 8002: can not retry select for update statement`：SELECT FOR UPDATE 写冲突错误
    - `Error 8022: Error: KV error safe to retry`：事务提交失败错误
    - `Error 8028: Information schema is changed during the execution of the statement`：DDL 操作导致的表结构变更错误，影响事务提交
    - `Error 9007: Write conflict`：写冲突错误，通常由多个事务同时修改同一行数据引起（在乐观事务模式下）
- 在 `try` 块结束时执行 `COMMIT`。

<CustomContent platform="tidb">

有关错误码的更多信息，请参见 [Error Codes and Troubleshooting](/error-codes.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

有关错误码的更多信息，请参见 [Error Codes and Troubleshooting](https://docs.pingcap.com/tidb/stable/error-codes)。

</CustomContent>

```python
while True:
    n++
    if n == max_retries:
        raise("did not succeed within #{n} retries")
    try:
        connection.execute("your sql statement here")
        connection.exec('COMMIT')
        break
    catch error:
        if (error.code != "9007" && error.code != "8028" && error.code != "8002" && error.code != "8022"):
            raise error
        else:
            connection.exec('ROLLBACK')

            # 捕获需要在应用端重试的错误类型，
            # 等待一段短时间，
            # 并对每次事务失败的等待时间进行指数增长
            sleep_ms = int(((1.5 ** n) + rand) * 100)
            sleep(sleep_ms) # 确保你的 sleep() 接受毫秒为单位
```

> **Note:**
>
> 如果你经常遇到 `Error 9007: Write conflict`，可能需要检查你的模式设计和工作负载的数据访问模式，找出冲突的根本原因，并通过更好的设计来避免冲突。

<CustomContent platform="tidb">

有关如何排查和解决事务冲突的更多信息，请参见 [Troubleshoot Lock Conflicts](/troubleshoot-lock-conflicts.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

有关如何排查和解决事务冲突的更多信息，请参见 [Troubleshoot Lock Conflicts](https://docs.pingcap.com/tidb/stable/troubleshoot-lock-conflicts)。

</CustomContent>

## 相关链接

<CustomContent platform="tidb">

- [Troubleshoot Write Conflicts in Optimistic Transactions](/troubleshoot-write-conflicts.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

- [Troubleshoot Write Conflicts in Optimistic Transactions](https://docs.pingcap.com/tidb/stable/troubleshoot-write-conflicts)

</CustomContent>

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>