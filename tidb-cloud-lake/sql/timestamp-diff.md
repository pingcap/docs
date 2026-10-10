---
title: TIMESTAMP_DIFF
summary: 2 つのタイムスタンプの差を計算し、結果を INTERVAL として返します。
---

# TIMESTAMP_DIFF

2 つのタイムスタンプの差を計算し、結果を INTERVAL として返します。

## 構文 {#syntax}

```sql
TIMESTAMP_DIFF(<timestamp1>, <timestamp2>)
```

## 戻り値の型 {#return-type}

INTERVAL（`hours:minutes:seconds` 形式）。

## 例 {#examples}

この例は、2025 年 2 月 1 日と 2025 年 1 月 1 日の時間差が 744 時間であり、31 日に相当することを示しています。

```sql
SELECT TIMESTAMP_DIFF('2025-02-01'::TIMESTAMP, '2025-01-01'::TIMESTAMP);

┌──────────────────────────────────────────────────────────────────┐
│ timestamp_diff('2025-02-01'::TIMESTAMP, '2025-01-01'::TIMESTAMP) │
├──────────────────────────────────────────────────────────────────┤
│ 744:00:00                                                        │
└──────────────────────────────────────────────────────────────────┘
```