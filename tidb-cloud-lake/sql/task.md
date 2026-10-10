---
title: タスク
summary: このページでは、{{{ .lake }}} におけるタスク操作の包括的な概要を、参照しやすいよう機能別に整理して説明します。
---

# タスク

このページでは、{{{ .lake }}} におけるタスク操作の包括的な概要を、参照しやすいよう機能別に整理して説明します。

## タスク管理 {#task-management}

| Command | 説明 |
|---------|-------------|
| [CREATE TASK](/tidb-cloud-lake/sql/create-task.md) | 新しいスケジュール済みタスクを作成します |
| [ALTER TASK](/tidb-cloud-lake/sql/alter-task.md) | 既存のタスクを変更します |
| [DROP TASK](/tidb-cloud-lake/sql/drop-task.md) | タスクを削除します |
| [EXECUTE TASK](/tidb-cloud-lake/sql/execute-task.md) | タスクを手動で実行します |

## タスク情報 {#task-information}

| Command | 説明 |
|---------|-------------|
| [SHOW TASKS](/tidb-cloud-lake/sql/show-tasks.md) | 現在のロールから参照可能なタスクを一覧表示します |
| [TASK HISTORY](/tidb-cloud-lake/sql/task-history.md) | 1 つ以上のタスクの実行履歴を表示します |
| [TASK ERROR INTEGRATION PAYLOAD](/tidb-cloud-lake/sql/task-error-notification-payload.md) | タスクエラー通知のエラーペイロード形式を表示します |

> **Note:**
>
> {{{ .lake }}} のタスクを使用すると、SQL コマンドを指定した間隔で実行するようにスケジュールし、自動化できます。