---
title: H3_EDGE_LENGTH_KM
summary: 指定した解像度における六角形の平均辺長をキロメートル単位で返します。五角形は含まれません。
---

# H3_EDGE_LENGTH_KM

指定した解像度における六角形の平均辺長をキロメートル単位で返します。五角形は含まれません。

## 構文 {#syntax}

```sql
H3_EDGE_LENGTH_KM(res)
```

## 例 {#examples}

```sql
SELECT H3_EDGE_LENGTH_KM(1);

┌──────────────────────┐
│ h3_edge_length_km(1) │
├──────────────────────┤
│    483.0568390711111 │
└──────────────────────┘
```