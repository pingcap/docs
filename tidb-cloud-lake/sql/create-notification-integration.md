---
title: CREATE NOTIFICATION INTEGRATION
sidebar_position: 1
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.371"/>

Creates a named notification integration that can be used to send notifications to external messaging services.

**NOTICE:** this functionality works out of the box only in Databend Cloud.

## Syntax
### Webhook Notification

```sql
CREATE NOTIFICATION INTEGRATION [ IF NOT EXISTS ] <name>
TYPE = <type>
ENABLED = <bool>
[ WEBHOOK = ( url = <string_literal>, method = <string_literal>, authorization_header = <string_literal> ) ]
[ COMMENT = '<string_literal>' ]
```

| Required Parameters | Description |
|---------------------|-------------|
| name                | The name of the notification integration. This is a mandatory field. |
| type                | The type of the notification integration. Currently, only `webhook` is supported. |
| enabled             | Whether the notification integration is enabled. |

| Optional Parameters [(Webhook)](#webhook-notification) | Description |
|---------------------|-------------|
| url                 | The URL of the webhook. |
| method              | The HTTP method to use when sending the webhook. default is `GET`|
| authorization_header| The authorization header to use when sending the webhook. |

## Examples

### Webhook Notification

```sql
CREATE NOTIFICATION INTEGRATION IF NOT EXISTS SampleNotification type = webhook enabled = true webhook = (url = 'https://example.com', method = 'GET', authorization_header = 'bearer auth')
```

This example creates a notification integration named `SampleNotification` of type `webhook` that is enabled and sends notifications to the `https://example.com` URL using the `GET` method and the `bearer auth` authorization header.

