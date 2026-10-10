---
title: MILLENNIUM
summary: 指定された日付またはタイムスタンプの millennium を返します。第1千年紀は 0001～1000 年、第2千年紀は 1001～2000 年、第3千年紀は 2001～3000 年、以降も同様です。
---

# MILLENNIUM

指定された日付またはタイムスタンプの millennium を返します。第1千年紀は 0001～1000 年、第2千年紀は 1001～2000 年、第3千年紀は 2001～3000 年、以降も同様です。

## 構文 {#syntax}

```sql
MILLENNIUM(<date_or_timestamp>)
```

## 戻り値の型 {#return-type}

UInt8 — 1 から始まる millennium 番号です。

## 例 {#examples}

```sql
SELECT
  MILLENNIUM('1992-02-15')       AS millennium_1992,
  MILLENNIUM('2025-04-16 12:34:56')    AS millennium_2025;
```

```sql
┌───────────────────────────────────┐
│ millennium_1992 │ millennium_2025 │
├─────────────────┼─────────────────┤
│               2 │               3 │
└───────────────────────────────────┘
```