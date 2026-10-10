---
title: TASK ERROR NOTIFICATION PAYLOAD
summary: タスクエラー通知のペイロード本文。
---

# TASK ERROR NOTIFICATION PAYLOAD

タスクエラー通知のペイロード本文です。

**NOTICE:** この機能は、{{{ .lake }}} でのみ追加設定なしですぐに利用できます。

以下は、タスクエラーを説明するメッセージペイロードのサンプルです。ペイロードには、1 つ以上のエラーメッセージを含めることができます。

```json
{
  "version": "1.0",
  "messageId": "8389a9c7-7263-4f92-a44a-ba0e23b005cb",
  "messageType": "TASK_FAILED",
  "timestamp": "2024-03-11T10:19:23.965382326Z",
  "tenantId": "tnc7yee14",
  "taskName": "notification_n2",
  "taskId": "56",
  "rootTaskName": "notification_n2",
  "rootTaskId": "56",
  "runId": "unknown",
  "scheduledTime": "2024-03-11T10:19:23.963349422Z",
  "queryStartTime": "2024-03-11T10:19:23.850156389Z",
  "completedTime": "2024-03-11T10:19:23.963348812Z",
  "queryId": "2424b81e-f489-491b-bbab-e3556a27f867",
  "errorKind": "UnexpectedError",
  "errorCode": "500",
  "errorMessage": "query sync failed: All attempts fail: #1: query error: code: 1006, message: divided by zero while evaluating function divide(1, 0)"
}
```