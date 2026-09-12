---
title: Map 函数
summary: 本节提供 {{{ .lake }}} 中 map 函数的参考信息。Map 函数可用于创建、操作以及从 map 数据结构（键值对）中提取信息。
---

# Map 函数

本节提供 {{{ .lake }}} 中 map 函数的参考信息。Map 函数可用于创建、操作以及从 map 数据结构（键值对）中提取信息。

## Map 创建与组合 {#map-creation-and-combination}

| 函数 | 描述 | 示例 |
|----------|-------------|--------|
| [MAP_CAT](/tidb-cloud-lake/sql/map-cat.md) | 将多个 map 合并为一个 map | `MAP_CAT({'a':1}, {'b':2})` → `{'a':1,'b':2}` |

## Map 访问与信息 {#map-access-and-information}

| 函数 | 描述 | 示例 |
|----------|-------------|--------|
| [MAP_KEYS](/tidb-cloud-lake/sql/map-keys.md) | 以数组形式返回 map 中的所有键 | `MAP_KEYS({'a':1,'b':2})` → `['a','b']` |
| [MAP_VALUES](/tidb-cloud-lake/sql/map-values.md) | 以数组形式返回 map 中的所有值 | `MAP_VALUES({'a':1,'b':2})` → `[1,2]` |
| [MAP_SIZE](/tidb-cloud-lake/sql/map-size.md) | 返回 map 中键值对的数量 | `MAP_SIZE({'a':1,'b':2,'c':3})` → `3` |
| [MAP_CONTAINS_KEY](/tidb-cloud-lake/sql/map-contains-key.md) | 检查 map 是否包含指定的键 | `MAP_CONTAINS_KEY({'a':1,'b':2}, 'a')` → `TRUE` |

## Map 修改 {#map-modification}

| 函数 | 描述 | 示例 |
|----------|-------------|--------|
| [MAP_INSERT](/tidb-cloud-lake/sql/map-insert.md) | 向 map 中插入一个键值对 | `MAP_INSERT({'a':1,'b':2}, 'c', 3)` → `{'a':1,'b':2,'c':3}` |
| [MAP_DELETE](/tidb-cloud-lake/sql/map-delete.md) | 从 map 中移除一个键值对 | `MAP_DELETE({'a':1,'b':2,'c':3}, 'b')` → `{'a':1,'c':3}` |

## Map 转换 {#map-transformation}

| 函数 | 描述 | 示例 |
|----------|-------------|--------|
| [MAP_TRANSFORM_KEYS](/tidb-cloud-lake/sql/map-transform-keys.md) | 对 map 中的每个键应用一个函数 | `MAP_TRANSFORM_KEYS({'a':1,'b':2}, x -> UPPER(x))` → `{'A':1,'B':2}` |
| [MAP_TRANSFORM_VALUES](/tidb-cloud-lake/sql/map-transform-values.md) | 对 map 中的每个值应用一个函数 | `MAP_TRANSFORM_VALUES({'a':1,'b':2}, x -> x * 10)` → `{'a':10,'b':20}` |

## Map 过滤与选择 {#map-filtering-and-selection}

| 函数 | 描述 | 示例 |
|----------|-------------|--------|
| [MAP_FILTER](/tidb-cloud-lake/sql/map-filter.md) | 根据谓词过滤键值对 | `MAP_FILTER({'a':1,'b':2,'c':3}, (k,v) -> v > 1)` → `{'b':2,'c':3}` |
| [MAP_PICK](/tidb-cloud-lake/sql/map-pick.md) | 仅使用指定的键创建一个新的 map | `MAP_PICK({'a':1,'b':2,'c':3}, ['a','c'])` → `{'a':1,'c':3}` |