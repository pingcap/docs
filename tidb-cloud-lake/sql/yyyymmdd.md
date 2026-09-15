---
title: TO_YYYYMMDD
summary: 将日期或带时间的日期（timestamp/datetime）转换为包含年月日数字的 UInt32 数值（YYYY * 10000 + MM * 100 + DD）。## 语法。
---

# TO_YYYYMMDD

将日期或带时间的日期（timestamp/datetime）转换为包含年月日数字的 UInt32 数值（YYYY * 10000 + MM * 100 + DD）。

## 语法 {#syntax}

```sql
TO_YYYYMMDD(<expr>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|-----------|---------------|
| `<expr>`  | 日期/日期时间 |

## 返回类型 {#return-type}

`INT`，以 `YYYYMMDD` 格式返回。

## 示例 {#examples}

```sql
SELECT
  to_yyyymmdd('2023-11-12 09:38:18.165575');

┌───────────────────────────────────────────┐
│ to_yyyymmdd('2023-11-12 09:38:18.165575') │
├───────────────────────────────────────────┤
│                                  20231112 │
└───────────────────────────────────────────┘
```