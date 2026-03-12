---
title: Bitmap
sidebar_position: 12
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced: v1.1.45"/>

## Overview

`BITMAP` stores membership information for unsigned 64-bit integers and supports fast set operations (count, union, intersection, etc.). SELECT statements show a binary blob, so use [Bitmap Functions](../../20-sql-functions/01-bitmap-functions/index.md) to interpret the values.

## Examples

### Build Bitmaps

`TO_BITMAP` accepts either a comma-separated string or a `UINT64` value (treated as a single element). `TO_STRING` serializes the bitmap back to readable text.

```sql
SELECT
  TO_BITMAP('1,2,3')                     AS str_input,
  TO_STRING(TO_BITMAP('1,2,3'))          AS round_tripped,
  TO_STRING(TO_BITMAP(123))              AS from_uint64;
```

Result:
```
┌────────────────────────────────┬──────────────────────────────────┬────────────────┐
│ str_input                      │ round_tripped                    │ from_uint64    │
├────────────────────────────────┼──────────────────────────────────┼────────────────┤
│ <bitmap binary>                │ 1,2,3                            │ 123            │
└────────────────────────────────┴──────────────────────────────────┴────────────────┘
```

### Persist Bitmaps

Use `BUILD_BITMAP` to turn an array into a bitmap before inserting it into a table. Aggregate functions such as `BITMAP_COUNT` can then read the stored values quickly.

```sql
CREATE TABLE user_visits (
  user_id INT,
  page_visits BITMAP
);

INSERT INTO user_visits VALUES
  (1, BUILD_BITMAP([2, 5, 8, 10])),
  (2, BUILD_BITMAP([3, 7, 9])),
  (3, BUILD_BITMAP([1, 4, 6, 10]));

SELECT
  user_id,
  BITMAP_COUNT(page_visits) AS distinct_pages,
  BITMAP_HAS_ALL(page_visits, BUILD_BITMAP([10])) AS saw_page_10
FROM user_visits;
```

Result:
```
┌────────┬────────────────┬─────────────┐
│ user_id │ distinct_pages │ saw_page_10 │
├────────┼────────────────┼─────────────┤
│      1 │              4 │        true │
│      2 │              3 │       false │
│      3 │              4 │        true │
└────────┴────────────────┴─────────────┘
```
