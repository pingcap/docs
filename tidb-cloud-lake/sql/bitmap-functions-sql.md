---
title: Bitmap Functions
---

This page provides a comprehensive overview of Bitmap functions in Databend, organized by functionality for easy reference.

## Bitmap Operations

| Function | Description | Example |
|----------|-------------|---------|
| [BITMAP_AND](bitmap-and.md) | Performs a bitwise AND operation on two bitmaps | `BITMAP_AND(BUILD_BITMAP([1,4,5]), BUILD_BITMAP([4,5]))` → `{4,5}` |
| [BITMAP_OR](bitmap-or.md) | Performs a bitwise OR operation on two bitmaps | `BITMAP_OR(BUILD_BITMAP([1,2]), BUILD_BITMAP([2,3]))` → `{1,2,3}` |
| [BITMAP_XOR](bitmap-xor.md) | Performs a bitwise XOR operation on two bitmaps | `BITMAP_XOR(BUILD_BITMAP([1,2,3]), BUILD_BITMAP([2,3,4]))` → `{1,4}` |
| [BITMAP_NOT](bitmap-not.md) | Performs a bitwise NOT operation on a bitmap | `BITMAP_NOT(BUILD_BITMAP([1,2,3]), 5)` → `{0,4}` |
| [BITMAP_AND_NOT](bitmap-and-not.md) | Returns elements in the first bitmap but not in the second | `BITMAP_AND_NOT(BUILD_BITMAP([1,2,3]), BUILD_BITMAP([2,3]))` → `{1}` |
| [BITMAP_UNION](bitmap-union.md) | Combines multiple bitmaps into one | `BITMAP_UNION([BUILD_BITMAP([1,2]), BUILD_BITMAP([2,3])])` → `{1,2,3}` |
| [BITMAP_INTERSECT](bitmap-intersect.md) | Returns the intersection of multiple bitmaps | `BITMAP_INTERSECT([BUILD_BITMAP([1,2,3]), BUILD_BITMAP([2,3,4])])` → `{2,3}` |

## Bitmap Information

| Function | Description | Example |
|----------|-------------|---------|
| [BITMAP_COUNT](bitmap-count.md) | Returns the number of elements in a bitmap | `BITMAP_COUNT(BUILD_BITMAP([1,2,3]))` → `3` |
| [BITMAP_CONTAINS](bitmap-contains.md) | Checks if a bitmap contains a specific element | `BITMAP_CONTAINS(BUILD_BITMAP([1,2,3]), 2)` → `true` |
| [BITMAP_HAS_ANY](bitmap-has-any.md) | Checks if a bitmap contains any element from another bitmap | `BITMAP_HAS_ANY(BUILD_BITMAP([1,2,3]), BUILD_BITMAP([3,4]))` → `true` |
| [BITMAP_HAS_ALL](bitmap-has-all.md) | Checks if a bitmap contains all elements from another bitmap | `BITMAP_HAS_ALL(BUILD_BITMAP([1,2,3]), BUILD_BITMAP([2,3]))` → `true` |
| [BITMAP_MIN](bitmap-min.md) | Returns the minimum element in a bitmap | `BITMAP_MIN(BUILD_BITMAP([1,2,3]))` → `1` |
| [BITMAP_MAX](bitmap-max.md) | Returns the maximum element in a bitmap | `BITMAP_MAX(BUILD_BITMAP([1,2,3]))` → `3` |
| [BITMAP_CARDINALITY](bitmap-cardinality.md) | Returns the number of elements in a bitmap | `BITMAP_CARDINALITY(BUILD_BITMAP([1,2,3]))` → `3` |

## Bitmap Count Operations

| Function | Description | Example |
|----------|-------------|---------|
| [BITMAP_AND_COUNT](bitmap-and-count.md) | Returns the count of elements in the bitwise AND of two bitmaps | `BITMAP_AND_COUNT(BUILD_BITMAP([1,2,3]), BUILD_BITMAP([2,3,4]))` → `2` |
| [BITMAP_OR_COUNT](bitmap-or-count.md) | Returns the count of elements in the bitwise OR of two bitmaps | `BITMAP_OR_COUNT(BUILD_BITMAP([1,2]), BUILD_BITMAP([2,3]))` → `3` |
| [BITMAP_XOR_COUNT](bitmap-xor-count.md) | Returns the count of elements in the bitwise XOR of two bitmaps | `BITMAP_XOR_COUNT(BUILD_BITMAP([1,2,3]), BUILD_BITMAP([2,3,4]))` → `2` |
| [BITMAP_NOT_COUNT](bitmap-not-count.md) | Returns the count of elements in the bitwise NOT of a bitmap | `BITMAP_NOT_COUNT(BUILD_BITMAP([1,2,3]), 5)` → `2` |
| [INTERSECT_COUNT](intersect-count.md) | Returns the count of elements in the intersection of multiple bitmaps | `INTERSECT_COUNT([BUILD_BITMAP([1,2,3]), BUILD_BITMAP([2,3,4])])` → `2` |

## Bitmap Subset Operations

| Function | Description | Example |
|----------|-------------|---------|
| [SUB_BITMAP](sub-bitmap.md) | Extracts a subset of a bitmap | `SUB_BITMAP(BUILD_BITMAP([1,2,3,4,5]), 1, 3)` → `{2,3,4}` |
| [BITMAP_SUBSET_IN_RANGE](bitmap-subset-in-range.md) | Returns a subset of a bitmap within a range | `BITMAP_SUBSET_IN_RANGE(BUILD_BITMAP([1,2,3,4,5]), 2, 4)` → `{2,3}` |
| [BITMAP_SUBSET_LIMIT](bitmap-subset-limit.md) | Returns a subset of a bitmap with a limit | `BITMAP_SUBSET_LIMIT(BUILD_BITMAP([1,2,3,4,5]), 2, 2)` → `{3,4}` |
