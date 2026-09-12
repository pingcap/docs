---
title: BITMAP_COUNT
summary: 统计位图中设置为 1 的位数。
---

# BITMAP_COUNT

统计位图中设置为 1 的位数。

## 语法 {#syntax}

```sql
BITMAP_COUNT( <bitmap> )
```

## 别名 {#aliases}

- [BITMAP_CARDINALITY](/tidb-cloud-lake/sql/bitmap-cardinality.md)

## 示例 {#examples}

```sql
SELECT BITMAP_COUNT(BUILD_BITMAP([1,4,5])), BITMAP_CARDINALITY(BUILD_BITMAP([1,4,5]));

┌─────────────────────────────────────────────────────────────────────────────────────┐
│ bitmap_count(build_bitmap([1, 4, 5])) │ bitmap_cardinality(build_bitmap([1, 4, 5])) │
├───────────────────────────────────────┼─────────────────────────────────────────────┤
│                                     3 │                                           3 │
└─────────────────────────────────────────────────────────────────────────────────────┘
```