---
title: DROP NOTIFICATION INTEGRATION
summary: DROP NOTIFICATION INTEGRATION 文は、既存の通知を削除するために使用されます。
---

# DROP NOTIFICATION INTEGRATION

DROP NOTIFICATION INTEGRATION 文は、既存の通知を削除するために使用されます。

**NOTICE:** この機能は、{{{ .lake }}} でのみ追加設定なしですぐに利用できます。

## 構文 {#syntax}

```sql
DROP NOTIFICATION INTEGRATION [ IF EXISTS ] <name>
```

| パラメータ                        | 説明                                                                                        |
|----------------------------------|------------------------------------------------------------------------------------------------------|
| IF EXISTS                        | 任意。指定した場合、同じ名前の通知がすでに存在するときにのみ、その通知が削除されます。 |
| name                             | 通知の名前です。これは必須項目です。                                                       |

## 使用例 {#usage-examples}

```sql
DROP NOTIFICATION INTEGRATION IF EXISTS error_notification;
```

このコマンドは、`error_notification` という名前の通知統合が存在する場合に削除します。