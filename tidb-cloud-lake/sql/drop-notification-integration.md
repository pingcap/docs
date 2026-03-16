---
title: DROP NOTIFICATION INTEGRATION
sidebar_position: 3
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.371"/>

The DROP NOTIFICATION INTEGRATION statement is used to delete an existing notification.

**NOTICE:** this functionality works out of the box only in Databend Cloud.

## Syntax

```sql
DROP NOTIFICATION INTEGRATION [ IF EXISTS ] <name>
```

| Parameter                        | Description                                                                                        |
|----------------------------------|------------------------------------------------------------------------------------------------------|
| IF EXISTS                        | Optional. If specified, the notification will only be dropped if a notification of the same name already exists. |
| name                             | The name of the notification. This is a mandatory field.                                                       |


## Usage Examples

```sql
DROP NOTIFICATION INTEGRATION IF EXISTS error_notification;
```

This command deletes the notification integration named `error_notification` if it exists. 
