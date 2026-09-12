---
title: ALTER NOTIFICATION INTEGRATION
summary: 修改已命名通知集成的设置，该集成可用于向外部消息服务发送通知。
---

# ALTER NOTIFICATION INTEGRATION

修改已命名通知集成的设置，该集成可用于向外部消息服务发送通知。

**注意：** 此功能开箱即用仅适用于 {{{ .lake }}}。

## 语法 {#syntax}

### Webhook 通知 {#webhook-notification}

```sql
ALTER NOTIFICATION INTEGRATION [ IF NOT EXISTS ] <name> SET
    [ ENABLED = TRUE | FALSE ]
    [ WEBHOOK = ( url = <string_literal>, method = <string_literal>, authorization_header = <string_literal> ) ]
    [ COMMENT = '<string_literal>' ]
```

| 必需参数 | 描述 |
|---------------------|-------------|
| name                | 通知集成的名称。这是一个必填字段。 |

| 可选参数 [(Webhook)](#webhook-notification) | 描述 |
|---------------------|-------------|
| enabled             | 通知集成是否启用。 |
| url                 | webhook 的 URL。 |
| method              | 发送 webhook 时使用的 HTTP 方法。默认值为 `GET`|
| authorization_header| 发送 webhook 时使用的授权请求头。 |
| comment             | 与通知集成关联的注释。 |

## 示例 {#examples}

### Webhook 通知 {#webhook-notification}

```sql
ALTER NOTIFICATION INTEGRATION SampleNotification SET enabled = true
```

此示例启用了名为 `SampleNotification` 的通知集成。