---
title: DROP NOTIFICATION INTEGRATION
summary: DROP NOTIFICATION INTEGRATION 语句用于删除现有通知。
---

# DROP NOTIFICATION INTEGRATION

`DROP NOTIFICATION INTEGRATION` 语句用于删除现有通知。

**注意：** 此功能开箱即用仅适用于 {{{ .lake }}}。

## 语法 {#syntax}

```sql
DROP NOTIFICATION INTEGRATION [ IF EXISTS ] <name>
```

| 参数                             | 描述                                                                                                 |
|----------------------------------|------------------------------------------------------------------------------------------------------|
| IF EXISTS                        | 可选。如果指定，只有在已存在同名通知时，才会删除该通知。 |
| name                             | 通知的名称。这是必填字段。                                                       |

## 使用示例 {#usage-examples}

```sql
DROP NOTIFICATION INTEGRATION IF EXISTS error_notification;
```

此命令会在 `error_notification` 存在时删除名为 `error_notification` 的通知集成。