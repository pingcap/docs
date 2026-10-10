---
title: Notification
summary: このページでは、{{{ .lake }}} における Notification 操作の包括的な概要を、参照しやすいよう機能別に整理して説明します。
---

# Notification

このページでは、{{{ .lake }}} における Notification 操作の包括的な概要を、参照しやすいよう機能別に整理して説明します。

## Notification の管理 {#notification-management}

| Command | 説明 |
|---------|-------------|
| [CREATE NOTIFICATION](/tidb-cloud-lake/sql/create-notification-integration.md) | イベントアラート用の新しい notification integration を作成します |
| [ALTER NOTIFICATION](/tidb-cloud-lake/sql/alter-notification-integration.md) | 既存の notification integration を変更します |
| [DROP NOTIFICATION](/tidb-cloud-lake/sql/drop-notification-integration.md) | notification integration を削除します |

## Notification 情報 {#notification-information}

| Command | 説明 |
|---------|-------------|
| [DESCRIBE NOTIFICATION](/tidb-cloud-lake/sql/describe-notification-integration.md) | notification integration のプロパティを表示します |

> **Note:**
>
> {{{ .lake }}} の Notifications を使用すると、email や Slack などの外部サービスとの integration を設定し、データベースのイベントや操作に関するアラートを受信できます。