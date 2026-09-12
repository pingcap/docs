---
title: 任务
summary: 本页按功能分类，全面概述 {{{ .lake }}} 中的任务操作，便于参考。
---

# 任务

本页按功能分类，全面概述 {{{ .lake }}} 中的任务操作，便于参考。

## 任务管理 {#task-management}

| Command | 描述 |
|---------|-------------|
| [CREATE TASK](/tidb-cloud-lake/sql/create-task.md) | 创建新的定时任务 |
| [ALTER TASK](/tidb-cloud-lake/sql/alter-task.md) | 修改现有任务 |
| [DROP TASK](/tidb-cloud-lake/sql/drop-task.md) | 删除任务 |
| [EXECUTE TASK](/tidb-cloud-lake/sql/execute-task.md) | 手动执行任务 |

## 任务信息 {#task-information}

| Command | 描述 |
|---------|-------------|
| [SHOW TASKS](/tidb-cloud-lake/sql/show-tasks.md) | 列出当前角色可见的任务 |
| [TASK HISTORY](/tidb-cloud-lake/sql/task-history.md) | 显示一个或多个任务的运行历史 |
| [TASK ERROR INTEGRATION PAYLOAD](/tidb-cloud-lake/sql/task-error-notification-payload.md) | 显示任务错误通知的错误负载格式 |

> **Note:**
>
> {{{ .lake }}} 中的任务允许你按指定时间间隔调度并自动执行 SQL 命令。