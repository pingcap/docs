---
title: NOW
summary: 現在の日付と時刻を返します。
---

# NOW

現在の日付と時刻を返します。

## 構文 {#syntax}

```sql
NOW()
```

## 戻り値の型 {#return-type}

TIMESTAMP

## エイリアス {#aliases}

- [CURRENT_TIMESTAMP](/tidb-cloud-lake/sql/current-timestamp.md)

## 例 {#examples}

この例では、現在の日付と時刻を返します。

```sql
SELECT CURRENT_TIMESTAMP(), NOW();

┌─────────────────────────────────────────────────────────┐
│     current_timestamp()    │            now()           │
├────────────────────────────┼────────────────────────────┤
│ 2024-01-29 04:38:12.584359 │ 2024-01-29 04:38:12.584417 │
└─────────────────────────────────────────────────────────┘
```