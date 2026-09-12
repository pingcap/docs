---
title: TO_MILLISECONDS
summary: 将指定的毫秒数转换为 Interval 类型。
---

# TO_MILLISECONDS

将指定的毫秒数转换为 Interval 类型。

- 接受正整数、零和负整数作为输入。

## 语法 {#syntax}

```sql
TO_MILLISECONDS(<milliseconds>)
```

## 返回类型 {#return-type}

Interval（格式为 `hh:mm:ss.sss`）。

## 示例 {#examples}

```sql
SELECT TO_MILLISECONDS(2), TO_MILLISECONDS(0), TO_MILLISECONDS((- 2));

┌────────────────────────────────────────────────────────────────┐
│ to_milliseconds(2) │ to_milliseconds(0) │ to_milliseconds(- 2) │
├────────────────────┼────────────────────┼──────────────────────┤
│ 0:00:00.002        │ 00:00:00           │ -0:00:00.002         │
└────────────────────────────────────────────────────────────────┘
```