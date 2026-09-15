---
title: GEN_RANDOM_UUID
summary: 从 1.2.658 版本开始，基于版本 7 生成随机 UUID。此前，此函数基于版本 4 生成 UUID。
---

# GEN_RANDOM_UUID

从 1.2.658 版本开始，基于版本 7 生成随机 UUID。此前，此函数基于版本 4 生成 UUID。

## 语法 {#syntax}

```sql
GEN_RANDOM_UUID()
```

## 别名 {#aliases}

- [UUID](/tidb-cloud-lake/sql/uuid-sql.md)

## 为什么使用 UUID v7？ {#why-use-uuid-v7}

- **基于时间的排序**：UUID v7 包含时间戳，因此可以按照创建时间对事件或记录进行时间顺序排序。这在需要跟踪操作先后顺序时尤其有用。

- **按时间先后排序**：UUID v7 可确保 UUID 按创建时间有序的，这非常适合需要按时间对事件进行排序的场景，例如事件日志或维护审计追踪。

## 版本信息 {#version-information}

- 1.2.658 及之后的版本：UUID 版本从 v4 升级为 v7。
- 1.2.658 之前的版本：UUID 生成功能基于 v4。

## 示例 {#examples}

在记录事件的应用中，保持操作的正确顺序至关重要。UUID v7 可确保每个事件都按时间有序，便于按时间顺序跟踪操作。

```sql
-- Log a user logging in
SELECT GEN_RANDOM_UUID(), 'User logged in' AS event, CURRENT_TIMESTAMP AS event_time;

-- Log a user making a purchase
SELECT GEN_RANDOM_UUID(), 'User made a purchase' AS event, CURRENT_TIMESTAMP AS event_time;
```

这些查询的结果可能如下所示：

```sql
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│           gen_random_uuid()          │         event        │         event_time         │
├──────────────────────────────────────┼──────────────────────┼────────────────────────────┤
│ 019329e6-26a2-7b01-b9f5-1c3c02600578 │ User logged in       │ 2024-11-14 08:59:29.313906 │
│ 019329e6-329e-73c3-b0a8-a413ce298607 │ User made a purchase │ 2024-11-14 08:59:32.381497 │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

请注意，`gen_random_uuid()` 的值是按照事件发生的顺序生成的，因此可以轻松保持时间顺序。