---
title: H3_NUM_HEXAGONS
summary: 指定した解像度における一意な H3 インデックスの数を返します。
---

# H3_NUM_HEXAGONS

指定した解像度における一意な [H3](https://eng.uber.com/h3/) インデックスの数を返します。

## 構文 {#syntax}

```sql
H3_NUM_HEXAGONS(res)
```

## 例 {#examples}

```sql
SELECT H3_NUM_HEXAGONS(10);

┌─────────────────────┐
│ h3_num_hexagons(10) │
├─────────────────────┤
│         33897029882 │
└─────────────────────┘
```