---
title: TO_START_OF_FIVE_MINUTES
summary: 将带时间的日期（timestamp/datetime）向下舍入到五分钟时间间隔的起始时间。## 语法。
---

# TO_START_OF_FIVE_MINUTES

将带时间的日期（timestamp/datetime）向下舍入到五分钟时间间隔的起始时间。

## 语法 {#syntax}

```sql
TO_START_OF_FIVE_MINUTES(<expr>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|-----------|-------------|
| `<expr>`  | 时间戳   |

## 返回类型 {#return-type}

`TIMESTAMP`，以 “YYYY-MM-DD hh:mm:ss.ffffff” 格式返回日期。

## 示例 {#examples}

```sql
SELECT
  to_start_of_five_minutes('2023-11-12 09:38:18.165575')

┌────────────────────────────────────────────────────────┐
│ to_start_of_five_minutes('2023-11-12 09:38:18.165575') │
├────────────────────────────────────────────────────────┤
│ 2023-11-12 09:35:00                                    │
└────────────────────────────────────────────────────────┘
```