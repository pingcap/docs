---
title: INTERSECT_COUNT
summary: 统计两个 bitmap 列之间相交的位数。
---

# INTERSECT_COUNT

统计两个 bitmap 列之间相交的位数。

## 语法 {#syntax}

```sql
INTERSECT_COUNT( '<bitmap1>', '<bitmap2>' )( <bitmap_column1>, <bitmap_column2> )
```

## 示例 {#examples}

```sql
CREATE TABLE agg_bitmap_test(id Int, tag String, v Bitmap);

INSERT INTO
  agg_bitmap_test(id, tag, v)
VALUES
  (1, 'a', to_bitmap('0, 1')),
  (2, 'b', to_bitmap('0, 1, 2')),
  (3, 'c', to_bitmap('1, 3, 4'));

SELECT id, INTERSECT_COUNT('b', 'c')(v, tag)
FROM agg_bitmap_test GROUP BY id;

┌─────────────────────────────────────────────────────┐
│        id       │ intersect_count('b', 'c')(v, tag) │
├─────────────────┼───────────────────────────────────┤
│               1 │                                 0 │
│               3 │                                 3 │
│               2 │                                 3 │
└─────────────────────────────────────────────────────┘
```