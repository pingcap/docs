---
title: DESCRIBE NOTIFICATION INTEGRATION
summary: Shows the properties of a notification integration.
---

# DESCRIBE NOTIFICATION INTEGRATION

Shows the properties of a notification integration.

> **Note:**
>
> This command requires cloud control to be enabled.

## Syntax

```sql
DESCRIBE NOTIFICATION INTEGRATION <name>
```

`DESC NOTIFICATION INTEGRATION <name>` is accepted as a synonym.

## Output

The result includes the notification's creation time, name, identifier, type, enabled state, webhook options, and comment.

## Example

```sql
DESCRIBE NOTIFICATION INTEGRATION SampleNotification;
```
