---
title: TO_START_OF_TEN_MINUTES
summary: 将带时间的日期（timestamp/datetime）向下舍入到十分钟间隔的开始时间。
---

# TO_START_OF_TEN_MINUTES

将带时间的日期（timestamp/datetime）向下舍入到十分钟间隔的开始时间。

## 语法 {#syntax}

```sql
TO_START_OF_TEN_MINUTES(<expr>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|-----------|-------------|
| `<expr>`  | 时间戳   |

## 返回类型 {#return-type}

`TIMESTAMP`，返回 “YYYY-MM-DD hh:mm:ss.ffffff” 格式的日期。

## 示例 {#examples}

```sql
SELECT
  to_start_of_ten_minutes('2023-11-12 09:38:18.165575');

┌───────────────────────────────────────────────────────┐
│ to_start_of_ten_minutes('2023-11-12 09:38:18.165575') │
├───────────────────────────────────────────────────────┤
│ 2023-11-12 09:30:00                                   │
└───────────────────────────────────────────────────────┘
```