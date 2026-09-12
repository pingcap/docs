---
title: 通知
summary: 本页按功能分类，全面概述了 {{{ .lake }}} 中的 Notification 操作，便于参考。
---

# 通知

本页按功能分类，全面概述了 {{{ .lake }}} 中的 Notification 操作，便于参考。

## Notification 管理 {#notification-management}

| Command | 描述 |
|---------|-------------|
| [CREATE NOTIFICATION](/tidb-cloud-lake/sql/create-notification-integration.md) | 为事件告警创建新的通知集成 |
| [ALTER NOTIFICATION](/tidb-cloud-lake/sql/alter-notification-integration.md) | 修改现有的通知集成 |
| [DROP NOTIFICATION](/tidb-cloud-lake/sql/drop-notification-integration.md) | 删除通知集成 |

## Notification 信息 {#notification-information}

| Command | 描述 |
|---------|-------------|
| [DESCRIBE NOTIFICATION](/tidb-cloud-lake/sql/describe-notification-integration.md) | 显示通知集成的属性 |

> **Note:**
>
> {{{ .lake }}} 中的 Notification 允许你配置与电子邮件或 Slack 等外部服务的集成，以接收有关数据库事件和操作的告警。