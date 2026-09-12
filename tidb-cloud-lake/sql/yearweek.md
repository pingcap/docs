---
title: YEARWEEK
summary: 根据 ISO 周日期，返回 `YYYYWW` 格式的年份和周数。第 1 周是该年中包含第一个星期四的那一周。
---

# YEARWEEK

根据 ISO 周日期，返回 `YYYYWW` 格式的年份和周数。第 1 周是该年中包含第一个星期四的那一周。

## 语法 {#syntax}

```sql
YEARWEEK(<date_or_timestamp>)
```

## 返回类型 {#return-type}

UInt32。

## 示例 {#examples}

```sql
SELECT
  YEARWEEK('2024-01-01') AS yw1,
  YEARWEEK('2024-12-31') AS yw2;
```

```sql
┌─────────────────┐
│   yw1  │   yw2  │
├────────┼────────┤
│ 202401 │ 202501 │
└─────────────────┘
```