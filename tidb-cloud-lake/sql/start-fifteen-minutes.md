---
title: TO_START_OF_FIFTEEN_MINUTES
summary: 将带时间的日期（timestamp/datetime）向下舍入到十五分钟间隔的起始时间。## 语法。
---

# TO_START_OF_FIFTEEN_MINUTES

将带时间的日期（timestamp/datetime）向下舍入到十五分钟间隔的起始时间。

## 语法 {#syntax}

```sql
TO_START_OF_FIFTEEN_MINUTES(<expr>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|-----------|-------------|
| `<expr>`  | 时间戳   |

## 返回类型 {#return-type}

`TIMESTAMP`，返回格式为 “YYYY-MM-DD hh:mm:ss.ffffff” 的日期。

## 示例 {#examples}

```sql
SELECT
  to_start_of_fifteen_minutes('2023-11-12 09:38:18.165575');

┌───────────────────────────────────────────────────────────┐
│ to_start_of_fifteen_minutes('2023-11-12 09:38:18.165575') │
├───────────────────────────────────────────────────────────┤
│ 2023-11-12 09:30:00                                       │
└───────────────────────────────────────────────────────────┘
```