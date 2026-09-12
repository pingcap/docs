---
title: CREATE NOTIFICATION INTEGRATION
summary: 创建一个命名的通知集成，可用于向外部消息服务发送通知。
---

# CREATE NOTIFICATION INTEGRATION

创建一个命名的通知集成，可用于向外部消息服务发送通知。

**NOTICE:** 此功能仅在 {{{ .lake }}} 中开箱即用。

## 语法 {#syntax}

### Webhook 通知 {#webhook-notification}

```sql
CREATE NOTIFICATION INTEGRATION [ IF NOT EXISTS ] <name>
TYPE = <type>
ENABLED = <bool>
[ WEBHOOK = ( url = <string_literal>, method = <string_literal>, authorization_header = <string_literal> ) ]
[ COMMENT = '<string_literal>' ]
```

| 必需参数 | 描述 |
|---------------------|-------------|
| name                | 通知集成的名称。这是一个必填字段。 |
| type                | 通知集成的类型。目前仅支持 `webhook`。 |
| enabled             | 通知集成是否启用。 |

| 可选参数 [(Webhook)](#webhook-notification) | 描述 |
|---------------------|-------------|
| url                 | webhook 的 URL。 |
| method              | 发送 webhook 时使用的 HTTP 方法。默认值为 `GET` |
| authorization_header| 发送 webhook 时使用的授权请求头。 |

## 示例 {#examples}

### Webhook 通知 {#webhook-notification}

```sql
CREATE NOTIFICATION INTEGRATION IF NOT EXISTS SampleNotification type = webhook enabled = true webhook = (url = 'https://example.com', method = 'GET', authorization_header = 'bearer auth')
```

此示例创建了一个名为 `SampleNotification`、类型为 `webhook` 的通知集成。该集成已启用，并使用 `GET` 方法和 `bearer auth` 授权请求头向 `https://example.com` URL 发送通知。