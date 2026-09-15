---
title: Bitmap 函数
summary: 本页按功能分类，全面概述 {{{ .lake }}} 中的 Bitmap 函数，便于参考。
---

# Bitmap 函数

本页按功能分类，全面概述 {{{ .lake }}} 中的 Bitmap 函数，便于参考。

## Bitmap 操作 {#bitmap-operations}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [BITMAP_AND](/tidb-cloud-lake/sql/bitmap-and.md) | 对两个 bitmap 执行按位 AND 运算 | `BITMAP_AND(BUILD_BITMAP([1,4,5]), BUILD_BITMAP([4,5]))` → `{4,5}` |
| [BITMAP_OR](/tidb-cloud-lake/sql/bitmap-or.md) | 对两个 bitmap 执行按位 OR 运算 | `BITMAP_OR(BUILD_BITMAP([1,2]), BUILD_BITMAP([2,3]))` → `{1,2,3}` |
| [BITMAP_XOR](/tidb-cloud-lake/sql/bitmap-xor.md) | 对两个 bitmap 执行按位 XOR 运算 | `BITMAP_XOR(BUILD_BITMAP([1,2,3]), BUILD_BITMAP([2,3,4]))` → `{1,4}` |
| [BITMAP_NOT](/tidb-cloud-lake/sql/bitmap-not.md) | 对一个 bitmap 执行按位 NOT 运算 | `BITMAP_NOT(BUILD_BITMAP([1,2,3]), 5)` → `{0,4}` |
| [BITMAP_AND_NOT](/tidb-cloud-lake/sql/bitmap-and-not.md) | 返回第一个 bitmap 中存在但第二个 bitmap 中不存在的元素 | `BITMAP_AND_NOT(BUILD_BITMAP([1,2,3]), BUILD_BITMAP([2,3]))` → `{1}` |
| [BITMAP_UNION](/tidb-cloud-lake/sql/bitmap-union.md) | 将多个 bitmap 合并为一个 | `BITMAP_UNION([BUILD_BITMAP([1,2]), BUILD_BITMAP([2,3])])` → `{1,2,3}` |
| [BITMAP_INTERSECT](/tidb-cloud-lake/sql/bitmap-intersect.md) | 返回多个 bitmap 的交集 | `BITMAP_INTERSECT([BUILD_BITMAP([1,2,3]), BUILD_BITMAP([2,3,4])])` → `{2,3}` |

## Bitmap 信息 {#bitmap-information}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [BITMAP_COUNT](/tidb-cloud-lake/sql/bitmap-count.md) | 返回 bitmap 中的元素个数 | `BITMAP_COUNT(BUILD_BITMAP([1,2,3]))` → `3` |
| [BITMAP_CONTAINS](/tidb-cloud-lake/sql/bitmap-contains.md) | 检查 bitmap 是否包含指定元素 | `BITMAP_CONTAINS(BUILD_BITMAP([1,2,3]), 2)` → `true` |
| [BITMAP_HAS_ANY](/tidb-cloud-lake/sql/bitmap-has-any.md) | 检查一个 bitmap 是否包含另一个 bitmap 中的任意元素 | `BITMAP_HAS_ANY(BUILD_BITMAP([1,2,3]), BUILD_BITMAP([3,4]))` → `true` |
| [BITMAP_HAS_ALL](/tidb-cloud-lake/sql/bitmap-has-all.md) | 检查一个 bitmap 是否包含另一个 bitmap 中的所有元素 | `BITMAP_HAS_ALL(BUILD_BITMAP([1,2,3]), BUILD_BITMAP([2,3]))` → `true` |
| [BITMAP_MIN](/tidb-cloud-lake/sql/bitmap-min.md) | 返回 bitmap 中的最小元素 | `BITMAP_MIN(BUILD_BITMAP([1,2,3]))` → `1` |
| [BITMAP_MAX](/tidb-cloud-lake/sql/bitmap-max.md) | 返回 bitmap 中的最大元素 | `BITMAP_MAX(BUILD_BITMAP([1,2,3]))` → `3` |
| [BITMAP_CARDINALITY](/tidb-cloud-lake/sql/bitmap-cardinality.md) | 返回 bitmap 中的元素个数 | `BITMAP_CARDINALITY(BUILD_BITMAP([1,2,3]))` → `3` |

## Bitmap 计数操作 {#bitmap-count-operations}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [BITMAP_AND_COUNT](/tidb-cloud-lake/sql/bitmap-and-count.md) | 返回两个 bitmap 按位 AND 结果中的元素个数 | `BITMAP_AND_COUNT(BUILD_BITMAP([1,2,3]), BUILD_BITMAP([2,3,4]))` → `2` |
| [BITMAP_OR_COUNT](/tidb-cloud-lake/sql/bitmap-or-count.md) | 返回两个 bitmap 按位 OR 结果中的元素个数 | `BITMAP_OR_COUNT(BUILD_BITMAP([1,2]), BUILD_BITMAP([2,3]))` → `3` |
| [BITMAP_XOR_COUNT](/tidb-cloud-lake/sql/bitmap-xor-count.md) | 返回两个 bitmap 按位 XOR 结果中的元素个数 | `BITMAP_XOR_COUNT(BUILD_BITMAP([1,2,3]), BUILD_BITMAP([2,3,4]))` → `2` |
| [BITMAP_NOT_COUNT](/tidb-cloud-lake/sql/bitmap-not-count.md) | 返回一个 bitmap 按位 NOT 结果中的元素个数 | `BITMAP_NOT_COUNT(BUILD_BITMAP([1,2,3]), 5)` → `2` |
| [INTERSECT_COUNT](/tidb-cloud-lake/sql/intersect-count.md) | 返回多个 bitmap 交集中的元素个数 | `INTERSECT_COUNT([BUILD_BITMAP([1,2,3]), BUILD_BITMAP([2,3,4])])` → `2` |

## Bitmap 子集操作 {#bitmap-subset-operations}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [SUB_BITMAP](/tidb-cloud-lake/sql/sub-bitmap.md) | 提取 bitmap 的一个子集 | `SUB_BITMAP(BUILD_BITMAP([1,2,3,4,5]), 1, 3)` → `{2,3,4}` |
| [BITMAP_SUBSET_IN_RANGE](/tidb-cloud-lake/sql/bitmap-subset-in-range.md) | 返回 bitmap 在指定范围内的子集 | `BITMAP_SUBSET_IN_RANGE(BUILD_BITMAP([1,2,3,4,5]), 2, 4)` → `{2,3}` |
| [BITMAP_SUBSET_LIMIT](/tidb-cloud-lake/sql/bitmap-subset-limit.md) | 返回带限制条件的 bitmap 子集 | `BITMAP_SUBSET_LIMIT(BUILD_BITMAP([1,2,3,4,5]), 2, 2)` → `{3,4}` |