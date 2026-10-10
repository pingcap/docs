---
title: Bitmap Functions
summary: このページでは、{{{ .lake }}} の Bitmap 関数について、参照しやすいように機能別に整理して包括的に説明します。
---

# Bitmap Functions

このページでは、{{{ .lake }}} の Bitmap 関数について、参照しやすいように機能別に整理して包括的に説明します。

## Bitmap の演算 {#bitmap-operations}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [BITMAP_AND](/tidb-cloud-lake/sql/bitmap-and.md) | 2 つの bitmap に対してビット単位の AND 演算を実行します | `BITMAP_AND(BUILD_BITMAP([1,4,5]), BUILD_BITMAP([4,5]))` → `{4,5}` |
| [BITMAP_OR](/tidb-cloud-lake/sql/bitmap-or.md) | 2 つの bitmap に対してビット単位の OR 演算を実行します | `BITMAP_OR(BUILD_BITMAP([1,2]), BUILD_BITMAP([2,3]))` → `{1,2,3}` |
| [BITMAP_XOR](/tidb-cloud-lake/sql/bitmap-xor.md) | 2 つの bitmap に対してビット単位の XOR 演算を実行します | `BITMAP_XOR(BUILD_BITMAP([1,2,3]), BUILD_BITMAP([2,3,4]))` → `{1,4}` |
| [BITMAP_NOT](/tidb-cloud-lake/sql/bitmap-not.md) | bitmap に対してビット単位の NOT 演算を実行します | `BITMAP_NOT(BUILD_BITMAP([1,2,3]), 5)` → `{0,4}` |
| [BITMAP_AND_NOT](/tidb-cloud-lake/sql/bitmap-and-not.md) | 1 つ目の bitmap に含まれ、2 つ目の bitmap には含まれない要素を返します | `BITMAP_AND_NOT(BUILD_BITMAP([1,2,3]), BUILD_BITMAP([2,3]))` → `{1}` |
| [BITMAP_UNION](/tidb-cloud-lake/sql/bitmap-union.md) | 複数の bitmap を 1 つに結合します | `BITMAP_UNION([BUILD_BITMAP([1,2]), BUILD_BITMAP([2,3])])` → `{1,2,3}` |
| [BITMAP_INTERSECT](/tidb-cloud-lake/sql/bitmap-intersect.md) | 複数の bitmap の共通部分を返します | `BITMAP_INTERSECT([BUILD_BITMAP([1,2,3]), BUILD_BITMAP([2,3,4])])` → `{2,3}` |

## Bitmap の情報 {#bitmap-information}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [BITMAP_COUNT](/tidb-cloud-lake/sql/bitmap-count.md) | bitmap 内の要素数を返します | `BITMAP_COUNT(BUILD_BITMAP([1,2,3]))` → `3` |
| [BITMAP_CONTAINS](/tidb-cloud-lake/sql/bitmap-contains.md) | bitmap に特定の要素が含まれているかを確認します | `BITMAP_CONTAINS(BUILD_BITMAP([1,2,3]), 2)` → `true` |
| [BITMAP_HAS_ANY](/tidb-cloud-lake/sql/bitmap-has-any.md) | bitmap に別の bitmap の要素が 1 つでも含まれているかを確認します | `BITMAP_HAS_ANY(BUILD_BITMAP([1,2,3]), BUILD_BITMAP([3,4]))` → `true` |
| [BITMAP_HAS_ALL](/tidb-cloud-lake/sql/bitmap-has-all.md) | bitmap に別の bitmap のすべての要素が含まれているかを確認します | `BITMAP_HAS_ALL(BUILD_BITMAP([1,2,3]), BUILD_BITMAP([2,3]))` → `true` |
| [BITMAP_MIN](/tidb-cloud-lake/sql/bitmap-min.md) | bitmap 内の最小要素を返します | `BITMAP_MIN(BUILD_BITMAP([1,2,3]))` → `1` |
| [BITMAP_MAX](/tidb-cloud-lake/sql/bitmap-max.md) | bitmap 内の最大要素を返します | `BITMAP_MAX(BUILD_BITMAP([1,2,3]))` → `3` |
| [BITMAP_CARDINALITY](/tidb-cloud-lake/sql/bitmap-cardinality.md) | bitmap 内の要素数を返します | `BITMAP_CARDINALITY(BUILD_BITMAP([1,2,3]))` → `3` |

## Bitmap のカウント演算 {#bitmap-count-operations}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [BITMAP_AND_COUNT](/tidb-cloud-lake/sql/bitmap-and-count.md) | 2 つの bitmap のビット単位 AND の要素数を返します | `BITMAP_AND_COUNT(BUILD_BITMAP([1,2,3]), BUILD_BITMAP([2,3,4]))` → `2` |
| [BITMAP_OR_COUNT](/tidb-cloud-lake/sql/bitmap-or-count.md) | 2 つの bitmap のビット単位 OR の要素数を返します | `BITMAP_OR_COUNT(BUILD_BITMAP([1,2]), BUILD_BITMAP([2,3]))` → `3` |
| [BITMAP_XOR_COUNT](/tidb-cloud-lake/sql/bitmap-xor-count.md) | 2 つの bitmap のビット単位 XOR の要素数を返します | `BITMAP_XOR_COUNT(BUILD_BITMAP([1,2,3]), BUILD_BITMAP([2,3,4]))` → `2` |
| [BITMAP_NOT_COUNT](/tidb-cloud-lake/sql/bitmap-not-count.md) | bitmap のビット単位 NOT の要素数を返します | `BITMAP_NOT_COUNT(BUILD_BITMAP([1,2,3]), 5)` → `2` |
| [INTERSECT_COUNT](/tidb-cloud-lake/sql/intersect-count.md) | 複数の bitmap の共通部分の要素数を返します | `INTERSECT_COUNT([BUILD_BITMAP([1,2,3]), BUILD_BITMAP([2,3,4])])` → `2` |

## Bitmap の部分集合演算 {#bitmap-subset-operations}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [SUB_BITMAP](/tidb-cloud-lake/sql/sub-bitmap.md) | bitmap の部分集合を抽出します | `SUB_BITMAP(BUILD_BITMAP([1,2,3,4,5]), 1, 3)` → `{2,3,4}` |
| [BITMAP_SUBSET_IN_RANGE](/tidb-cloud-lake/sql/bitmap-subset-in-range.md) | 範囲内の bitmap の部分集合を返します | `BITMAP_SUBSET_IN_RANGE(BUILD_BITMAP([1,2,3,4,5]), 2, 4)` → `{2,3}` |
| [BITMAP_SUBSET_LIMIT](/tidb-cloud-lake/sql/bitmap-subset-limit.md) | 制限付きで bitmap の部分集合を返します | `BITMAP_SUBSET_LIMIT(BUILD_BITMAP([1,2,3,4,5]), 2, 2)` → `{3,4}` |