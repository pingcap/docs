---
title: 事务
summary: 本页按功能分类，全面概述了 {{{ .lake }}} 中的事务操作，便于参考。
---

# 事务

本页按功能分类，全面概述了 {{{ .lake }}} 中的事务操作，便于参考。

## 事务控制 {#transaction-control}

| Command | 描述 |
|---------|-------------|
| [BEGIN](/tidb-cloud-lake/sql/begin.md) | 启动一个新事务 |
| [COMMIT](/tidb-cloud-lake/sql/commit.md) | 提交当前事务，并使所有更改永久生效 |
| [ROLLBACK](/tidb-cloud-lake/sql/rollback.md) | 退出当前事务并丢弃所有更改 |

## 事务信息 {#transaction-information}

| Command | 描述 |
|---------|-------------|
| [SHOW LOCKS](/tidb-cloud-lake/sql/show-locks.md) | 显示系统中活动锁的信息 |

> **注意：**
>
> {{{ .lake }}} 中的事务通过将 SQL 操作分组为原子单元来确保数据一致性，这些操作要么全部成功，要么全部失败，从而维护数据库完整性。