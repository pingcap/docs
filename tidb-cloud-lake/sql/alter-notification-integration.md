---
title: ALTER NOTIFICATION INTEGRATION
sidebar_position: 2
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.371"/>

Alter the settings of a named notification integration that can be used to send notifications to external messaging services.

**NOTICE:** this functionality works out of the box only in Databend Cloud.

## Syntax
### Webhook Notification

```sql
ALTER NOTIFICATION INTEGRATION [ IF NOT EXISTS ] <name> SET
    [ ENABLED = TRUE | FALSE ]
    [ WEBHOOK = ( url = <string_literal>, method = <string_literal>, authorization_header = <string_literal> ) ]
    [ COMMENT = '<string_literal>' ]
```

| Required Parameters | Description |
|---------------------|-------------|
| name                | The name of the notification integration. This is a mandatory field. |


| Optional Parameters [(Webhook)](#webhook-notification) | Description |
|---------------------|-------------|
| enabled             | Whether the notification integration is enabled. |
| url                 | The URL of the webhook. |
| method              | The HTTP method to use when sending the webhook. default is `GET`|
| authorization_header| The authorization header to use when sending the webhook. |
| comment             | A comment to associate with the notification integration. |

## Examples

### Webhook Notification

```sql
ALTER NOTIFICATION INTEGRATION SampleNotification SET enabled = true
```

This example enables the notification integration named `SampleNotification`.


