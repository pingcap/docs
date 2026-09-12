---
title: H3_NUM_HEXAGONS
summary: 返回给定分辨率下唯一 H3 索引的数量。
---

# H3_NUM_HEXAGONS

返回给定分辨率下唯一 [H3](https://eng.uber.com/h3/) 索引的数量。

## 语法 {#syntax}

```sql
H3_NUM_HEXAGONS(res)
```

## 示例 {#examples}

```sql
SELECT H3_NUM_HEXAGONS(10);

┌─────────────────────┐
│ h3_num_hexagons(10) │
├─────────────────────┤
│         33897029882 │
└─────────────────────┘
```