---
title: H3_GET_RESOLUTION
summary: 返回给定 H3 索引的分辨率。
---

# H3_GET_RESOLUTION

返回给定 [H3](https://eng.uber.com/h3/) 索引的分辨率。

## 语法 {#syntax}

```sql
H3_GET_RESOLUTION(h3)
```

## 示例 {#examples}

```sql
SELECT H3_GET_RESOLUTION(644325524701193974);

┌───────────────────────────────────────┐
│ h3_get_resolution(644325524701193974) │
├───────────────────────────────────────┤
│                                    15 │
└───────────────────────────────────────┘
```