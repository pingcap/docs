---
title: H3_GET_RESOLUTION
summary: 指定された H3 インデックスの解像度を返します。
---

# H3_GET_RESOLUTION

指定された [H3](https://eng.uber.com/h3/) インデックスの解像度を返します。

## 構文 {#syntax}

```sql
H3_GET_RESOLUTION(h3)
```

## 例 {#examples}

```sql
SELECT H3_GET_RESOLUTION(644325524701193974);

┌───────────────────────────────────────┐
│ h3_get_resolution(644325524701193974) │
├───────────────────────────────────────┤
│                                    15 │
└───────────────────────────────────────┘
```