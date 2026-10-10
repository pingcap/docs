---
title: ALTER NOTIFICATION INTEGRATION
summary: 外部メッセージングサービスに通知を送信するために使用できる、名前付き通知統合の設定を変更します。
---

# ALTER NOTIFICATION INTEGRATION

外部メッセージングサービスに通知を送信するために使用できる、名前付き通知統合の設定を変更します。

**NOTICE:** この機能は、{{{ .lake }}} でのみ追加設定なしにそのまま利用できます。

## 構文 {#syntax}

### Webhook 通知 {#webhook-notification}

```sql
ALTER NOTIFICATION INTEGRATION [ IF NOT EXISTS ] <name> SET
    [ ENABLED = TRUE | FALSE ]
    [ WEBHOOK = ( url = <string_literal>, method = <string_literal>, authorization_header = <string_literal> ) ]
    [ COMMENT = '<string_literal>' ]
```

| 必須パラメータ | 説明 |
|---------------------|-------------|
| name                | 通知統合の名前です。これは必須フィールドです。 |

| オプションパラメータ [(Webhook)](#webhook-notification) | 説明 |
|---------------------|-------------|
| enabled             | 通知統合を有効にするかどうかを指定します。 |
| url                 | webhook の URL です。 |
| method              | webhook の送信時に使用する HTTP メソッドです。デフォルトは `GET` です。|
| authorization_header| webhook の送信時に使用する認可ヘッダーです。 |
| comment             | 通知統合に関連付けるコメントです。 |

## 例 {#examples}

### Webhook 通知 {#webhook-notification}

```sql
ALTER NOTIFICATION INTEGRATION SampleNotification SET enabled = true
```

この例では、`SampleNotification` という名前の通知統合を有効にします。