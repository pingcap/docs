---
title: YEARWEEK
summary: ISO 週日付に従って、`YYYYWW` 形式の年と週番号を返します。第 1 週は、その年の最初の木曜日を含む週です。
---

# YEARWEEK

ISO 週日付に従って、`YYYYWW` 形式の年と週番号を返します。第 1 週は、その年の最初の木曜日を含む週です。

## 構文 {#syntax}

```sql
YEARWEEK(<date_or_timestamp>)
```

## 戻り値の型 {#return-type}

UInt32。

## 例 {#examples}

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