---
title: 数组函数
summary: 本节提供 {{{ .lake }}} 中数组函数的参考信息。数组函数支持创建、操作、搜索和转换数组数据结构。
---

# 数组函数

本节提供 {{{ .lake }}} 中数组函数的参考信息。数组函数支持创建、操作、搜索和转换数组数据结构。

## 数组创建与构造 {#array-creation-construction}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [ARRAY](/tidb-cloud-lake/sql/array.md) | 从表达式构建数组 | `ARRAY(1, 2, 3)` → `[1,2,3]` |
| [ARRAY_CONSTRUCT](/tidb-cloud-lake/sql/array-construct.md) | 从单个值创建数组 | `ARRAY_CONSTRUCT(1, 2, 3)` → `[1,2,3]` |
| [RANGE](/tidb-cloud-lake/sql/range.md) | 生成顺序数字组成的数组 | `RANGE(1, 5)` → `[1,2,3,4]` |
| [ARRAY_GENERATE_RANGE](/tidb-cloud-lake/sql/array-generate-range.md) | 生成可选步长的序列 | `ARRAY_GENERATE_RANGE(0, 6, 2)` → `[0,2,4]` |

## 数组访问与信息 {#array-access-information}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [GET](/tidb-cloud-lake/sql/get.md) | 按索引从数组中获取元素 | `GET([1,2,3], 1)` → `1` |
| [ARRAY_GET](/tidb-cloud-lake/sql/array-get.md) | GET 函数的别名 | `ARRAY_GET([1,2,3], 1)` → `1` |
| [CONTAINS](/tidb-cloud-lake/sql/contains.md) | 检查数组是否包含指定值 | `CONTAINS([1,2,3], 2)` → `true` |
| [ARRAY_CONTAINS](/tidb-cloud-lake/sql/array-contains.md) | 检查数组是否包含指定值 | `ARRAY_CONTAINS([1,2,3], 2)` → `true` |
| [ARRAY_SIZE](/tidb-cloud-lake/sql/array-size.md) | 返回数组长度（别名：`ARRAY_LENGTH`） | `ARRAY_SIZE([1,2,3])` → `3` |
| [ARRAY_COUNT](/tidb-cloud-lake/sql/array-count.md) | 统计非 `NULL` 条目数量 | `ARRAY_COUNT([1,NULL,2])` → `2` |
| [ARRAY_ANY](/tidb-cloud-lake/sql/array-any.md) | 返回第一个非 `NULL` 值 | `ARRAY_ANY([NULL,'a','b'])` → `'a'` |

## 数组修改 {#array-modification}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [ARRAY_APPEND](/tidb-cloud-lake/sql/array-append.md) | 在数组末尾追加元素 | `ARRAY_APPEND([1,2], 3)` → `[1,2,3]` |
| [ARRAY_PREPEND](/tidb-cloud-lake/sql/array-prepend.md) | 在数组开头前置元素 | `ARRAY_PREPEND(0, [1,2])` → `[0,1,2]` |
| [ARRAY_INSERT](/tidb-cloud-lake/sql/array-insert.md) | 在指定位置插入元素 | `ARRAY_INSERT([1,3], 1, 2)` → `[1,2,3]` |
| [ARRAY_REMOVE](/tidb-cloud-lake/sql/array-remove.md) | 删除指定元素的所有出现项 | `ARRAY_REMOVE([1,2,2,3], 2)` → `[1,3]` |
| [ARRAY_REMOVE_FIRST](/tidb-cloud-lake/sql/array-remove-first.md) | 删除数组中的第一个元素 | `ARRAY_REMOVE_FIRST([1,2,3])` → `[2,3]` |
| [ARRAY_REMOVE_LAST](/tidb-cloud-lake/sql/array-remove-last.md) | 删除数组中的最后一个元素 | `ARRAY_REMOVE_LAST([1,2,3])` → `[1,2]` |

## 数组组合与操作 {#array-combination-manipulation}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [ARRAY_CONCAT](/tidb-cloud-lake/sql/array-concat.md) | 连接多个数组 | `ARRAY_CONCAT([1,2], [3,4])` → `[1,2,3,4]` |
| [ARRAY_SLICE](/tidb-cloud-lake/sql/array-slice.md) | 提取数组的一部分 | `ARRAY_SLICE([1,2,3,4], 1, 2)` → `[1,2]` |
| [SLICE](/tidb-cloud-lake/sql/slice.md) | ARRAY_SLICE 函数的别名 | `SLICE([1,2,3,4], 1, 2)` → `[1,2]` |
| [ARRAYS_ZIP](/tidb-cloud-lake/sql/arrays-zip.md) | 按元素位置组合多个数组 | `ARRAYS_ZIP([1,2], ['a','b'])` → `[(1,'a'),(2,'b')]` |
| [ARRAY_SORT](/tidb-cloud-lake/sql/array-sort.md) | 对值进行排序；不同变体可控制顺序和空值 | `ARRAY_SORT([3,1,2])` → `[1,2,3]` |

## 数组集合操作 {#array-set-operations}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [ARRAY_DISTINCT](/tidb-cloud-lake/sql/array-distinct.md) | 返回数组中的唯一元素 | `ARRAY_DISTINCT([1,2,2,3])` → `[1,2,3]` |
| [ARRAY_UNIQUE](/tidb-cloud-lake/sql/array-unique.md) | ARRAY_DISTINCT 函数的别名 | `ARRAY_UNIQUE([1,2,2,3])` → `[1,2,3]` |
| [ARRAY_INTERSECTION](/tidb-cloud-lake/sql/array-intersection.md) | 返回数组之间的公共元素 | `ARRAY_INTERSECTION([1,2,3], [2,3,4])` → `[2,3]` |
| [ARRAY_EXCEPT](/tidb-cloud-lake/sql/array-except.md) | 返回第一个数组中存在但第二个数组中不存在的元素 | `ARRAY_EXCEPT([1,2,3], [2,4])` → `[1,3]` |
| [ARRAY_OVERLAP](/tidb-cloud-lake/sql/array-overlap.md) | 检查数组是否有公共元素 | `ARRAY_OVERLAP([1,2,3], [3,4,5])` → `true` |

## 数组处理与转换 {#array-processing-transformation}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [ARRAY_TRANSFORM](/tidb-cloud-lake/sql/json-array-transform.md) | 对每个数组元素应用函数 | `ARRAY_TRANSFORM([1,2,3], x -> x * 2)` → `[2,4,6]` |
| [ARRAY_FILTER](/tidb-cloud-lake/sql/array-filter.md) | 根据条件过滤数组元素 | `ARRAY_FILTER([1,2,3,4], x -> x > 2)` → `[3,4]` |
| [ARRAY_REDUCE](/tidb-cloud-lake/sql/array-reduce.md) | 使用聚合将数组归约为单个值 | `ARRAY_REDUCE([1,2,3], 0, (acc,x) -> acc + x)` → `6` |
| [ARRAY_AGGREGATE](/tidb-cloud-lake/sql/array-aggregate.md) | 使用函数聚合数组元素 | `ARRAY_AGGREGATE([1,2,3], 'sum')` → `6` |

## 数组聚合与统计 {#array-aggregations-statistics}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [ARRAY_SUM](/tidb-cloud-lake/sql/array-sum.md) | 数值之和 | `ARRAY_SUM([1,2,3])` → `6` |
| [ARRAY_AVG](/tidb-cloud-lake/sql/array-avg.md) | 数值平均值 | `ARRAY_AVG([1,2,3])` → `2` |
| [ARRAY_MEDIAN](/tidb-cloud-lake/sql/array-median.md) | 数值中位数 | `ARRAY_MEDIAN([1,3,2])` → `2` |
| [ARRAY_MIN](/tidb-cloud-lake/sql/array-min.md) | 最小值 | `ARRAY_MIN([3,1,2])` → `1` |
| [ARRAY_MAX](/tidb-cloud-lake/sql/array-max.md) | 最大值 | `ARRAY_MAX([3,1,2])` → `3` |
| [ARRAY_STDDEV_POP](/tidb-cloud-lake/sql/array-stddev-pop.md) | 总体标准差（别名：`ARRAY_STD`） | `ARRAY_STDDEV_POP([1,2,3])` |
| [ARRAY_STDDEV_SAMP](/tidb-cloud-lake/sql/array-stddev-samp.md) | 样本标准差（别名：`ARRAY_STDDEV`） | `ARRAY_STDDEV_SAMP([1,2,3])` |
| [ARRAY_KURTOSIS](/tidb-cloud-lake/sql/array-kurtosis.md) | 值的超额峰度 | `ARRAY_KURTOSIS([1,2,3,4])` |
| [ARRAY_SKEWNESS](/tidb-cloud-lake/sql/array-skewness.md) | 值的偏度 | `ARRAY_SKEWNESS([1,2,3,4])` |
| [ARRAY_APPROX_COUNT_DISTINCT](/tidb-cloud-lake/sql/array-approx-count-distinct.md) | 近似去重计数 | `ARRAY_APPROX_COUNT_DISTINCT([1,1,2])` → `2` |

## 数组格式化 {#array-formatting}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [ARRAY_TO_STRING](/tidb-cloud-lake/sql/array-to-string.md) | 将数组元素连接为字符串 | `ARRAY_TO_STRING(['a','b'], ',')` → `'a,b'` |

## 数组实用函数 {#array-utility-functions}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [ARRAY_COMPACT](/tidb-cloud-lake/sql/array-compact.md) | 从数组中移除空值 | `ARRAY_COMPACT([1,null,2,null,3])` → `[1,2,3]` |
| [ARRAY_FLATTEN](/tidb-cloud-lake/sql/array-flatten.md) | 将嵌套数组展平为单个数组 | `ARRAY_FLATTEN([[1,2],[3,4]])` → `[1,2,3,4]` |
| [ARRAY_REVERSE](/tidb-cloud-lake/sql/array-reverse.md) | 反转数组元素的顺序 | `ARRAY_REVERSE([1,2,3])` → `[3,2,1]` |
| [ARRAY_INDEXOF](/tidb-cloud-lake/sql/array-indexof.md) | 返回元素首次出现的索引 | `ARRAY_INDEXOF([1,2,3,2], 2)` → `1` |
| [UNNEST](/tidb-cloud-lake/sql/unnest.md) | 将数组展开为单独的行 | `UNNEST([1,2,3])` → `1, 2, 3`（作为单独的行） |