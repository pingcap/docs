---
title: BITMAP_COUNT
summary: ビットマップ内で 1 に設定されているビット数をカウントします。
---

# BITMAP_COUNT

ビットマップ内で 1 に設定されているビット数をカウントします。

## 構文 {#syntax}

```sql
BITMAP_COUNT( <bitmap> )
```

## エイリアス {#aliases}

- [BITMAP_CARDINALITY](/tidb-cloud-lake/sql/bitmap-cardinality.md)

## 例 {#examples}

```sql
SELECT BITMAP_COUNT(BUILD_BITMAP([1,4,5])), BITMAP_CARDINALITY(BUILD_BITMAP([1,4,5]));

┌─────────────────────────────────────────────────────────────────────────────────────┐
│ bitmap_count(build_bitmap([1, 4, 5])) │ bitmap_cardinality(build_bitmap([1, 4, 5])) │
├───────────────────────────────────────┼─────────────────────────────────────────────┤
│                                     3 │                                           3 │
└─────────────────────────────────────────────────────────────────────────────────────┘
```