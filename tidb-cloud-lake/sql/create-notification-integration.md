---
title: CREATE NOTIFICATION INTEGRATION
summary: 外部メッセージングサービスに通知を送信するために使用できる、名前付きの通知統合を作成します。
---

# CREATE NOTIFICATION INTEGRATION

外部メッセージングサービスに通知を送信するために使用できる、名前付きの通知統合を作成します。

**注意:** この機能は、{{{ .lake }}} でのみ追加設定なしですぐに利用できます。

## 構文 {#syntax}

### Webhook 通知 {#webhook-notification}

```sql
CREATE NOTIFICATION INTEGRATION [ IF NOT EXISTS ] <name>
TYPE = <type>
ENABLED = <bool>
[ WEBHOOK = ( url = <string_literal>, method = <string_literal>, authorization_header = <string_literal> ) ]
[ COMMENT = '<string_literal>' ]
```

| 必須パラメータ | 説明 |
|---------------------|-------------|
| name                | 通知統合の名前です。これは必須フィールドです。 |
| type                | 通知統合のタイプです。現在は `webhook` のみサポートされています。 |
| enabled             | 通知統合を有効にするかどうかです。 |

| オプションパラメータ [(Webhook)](#webhook-notification) | 説明 |
|---------------------|-------------|
| url                 | webhook の URL です。 |
| method              | webhook の送信時に使用する HTTP メソッドです。デフォルトは `GET` です。|
| authorization_header| webhook の送信時に使用する Authorization ヘッダーです。 |

## 例 {#examples}

### Webhook 通知 {#webhook-notification-1}

```sql
CREATE NOTIFICATION INTEGRATION IF NOT EXISTS SampleNotification type = webhook enabled = true webhook = (url = 'https://example.com', method = 'GET', authorization_header = 'bearer auth')
```

この例では、`SampleNotification` という名前の `webhook` タイプの通知統合を作成します。この統合は有効化されており、`GET` メソッドと `bearer auth` Authorization ヘッダーを使用して `https://example.com` URL に通知を送信します。