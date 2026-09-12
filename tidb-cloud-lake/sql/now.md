---
title: NOW
summary: 返回当前日期和时间。
---

# NOW

返回当前日期和时间。

## 语法 {#syntax}

```sql
NOW()
```

## 返回类型 {#return-type}

TIMESTAMP

## 别名 {#aliases}

- [CURRENT_TIMESTAMP](/tidb-cloud-lake/sql/current-timestamp.md)

## 示例 {#examples}

以下示例返回当前日期和时间：

```sql
SELECT CURRENT_TIMESTAMP(), NOW();

┌─────────────────────────────────────────────────────────┐
│     current_timestamp()    │            now()           │
├────────────────────────────┼────────────────────────────┤
│ 2024-01-29 04:38:12.584359 │ 2024-01-29 04:38:12.584417 │
└─────────────────────────────────────────────────────────┘
```