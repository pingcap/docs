---
title: 结构化与半结构化函数
summary: {{{ .lake }}} 中的结构化与半结构化函数可高效处理数组、对象、映射、JSON 以及其他结构化数据格式。这些函数提供了全面的能力，用于创建、解析、查询、转换和操作结构化与半结构化数据。
---

# 结构化与半结构化函数

{{{ .lake }}} 中的结构化与半结构化函数可高效处理数组、对象、映射、JSON 以及其他结构化数据格式。这些函数提供了全面的能力，用于创建、解析、查询、转换和操作结构化与半结构化数据。

## JSON 函数 {#json-functions}

### 解析与校验 {#parsing-validation}

| 函数 | 描述 | 示例 |
|----------|-------------|--------|
| [PARSE_JSON](/tidb-cloud-lake/sql/parse-json.md) | 将 JSON 字符串解析为 variant 值 | `PARSE_JSON('[1,2,3]')` |
| [CHECK_JSON](/tidb-cloud-lake/sql/check-json.md) | 校验字符串是否为有效的 JSON | `CHECK_JSON('{"a":1}')` |
| [JSON_TYPEOF](/tidb-cloud-lake/sql/json-typeof.md) | 返回 JSON 值的类型 | `JSON_TYPEOF(PARSE_JSON('[1,2,3]'))` |

### 基于路径的查询 {#path-based-querying}

| 函数 | 描述 | 示例 |
|----------|-------------|--------|
| [JSON_PATH_EXISTS](/tidb-cloud-lake/sql/json-path-exists.md) | 检查 JSON 路径是否存在 | `JSON_PATH_EXISTS(json_obj, '$.name')` |
| [JSON_PATH_QUERY](/tidb-cloud-lake/sql/json-path-query.md) | 使用 JSONPath 查询 JSON 数据 | `JSON_PATH_QUERY(json_obj, '$.items[*]')` |
| [JSON_PATH_QUERY_ARRAY](/tidb-cloud-lake/sql/json-path-query-array.md) | 查询 JSON 数据并以数组形式返回结果 | `JSON_PATH_QUERY_ARRAY(json_obj, '$.items')` |
| [JSON_PATH_QUERY_FIRST](/tidb-cloud-lake/sql/json-path-query-first.md) | 返回 JSON 路径查询的第一个结果 | `JSON_PATH_QUERY_FIRST(json_obj, '$.items[*]')` |
| [JSON_PATH_MATCH](/tidb-cloud-lake/sql/json-path-match.md) | 将 JSON 值与路径模式进行匹配 | `JSON_PATH_MATCH(json_obj, '$.age')` |
| [JQ](/tidb-cloud-lake/sql/jq.md) | 使用 jq 语法进行高级 JSON 处理 | `JQ('.name', json_obj)` |

### 值提取 {#value-extraction}

| 函数 | 描述 | 示例 |
|----------|-------------|--------|
| [GET](/tidb-cloud-lake/sql/get.md) | 通过键从 JSON 对象中获取值，或通过索引从数组中获取值 | `GET(PARSE_JSON('[1,2,3]'), 0)` |
| [GET_PATH](/tidb-cloud-lake/sql/get-path.md) | 使用路径表达式从 JSON 对象中获取值 | `GET_PATH(json_obj, 'user.name')` |
| [GET_IGNORE_CASE](/tidb-cloud-lake/sql/get-ignore-case.md) | 以不区分大小写的键匹配方式获取值 | `GET_IGNORE_CASE(json_obj, 'NAME')` |
| [JSON_EXTRACT_PATH_TEXT](/tidb-cloud-lake/sql/json-extract-path-text.md) | 使用路径从 JSON 中提取文本值 | `JSON_EXTRACT_PATH_TEXT(json_obj, 'name')` |

### 转换与输出 {#transformation-output}

| 函数 | 描述 | 示例 |
|----------|-------------|--------|
| [JSON_TO_STRING](/tidb-cloud-lake/sql/json-to-string.md) | 将 JSON 值转换为字符串 | `JSON_TO_STRING(PARSE_JSON('{"a":1}'))` |
| [JSON_PRETTY](/tidb-cloud-lake/sql/json-pretty.md) | 使用适当的缩进格式化 JSON | `JSON_PRETTY(PARSE_JSON('{"a":1}'))` |
| [STRIP_NULL_VALUE](/tidb-cloud-lake/sql/strip-null-value.md) | 将 JSON 空值转换为 SQL NULL 值 | `STRIP_NULL_VALUE(parse_json('null'))` → `NULL` |
| [JSON_STRIP_NULLS](/tidb-cloud-lake/sql/json-strip-nulls.md) | 从 JSON 对象中移除空值 | `JSON_STRIP_NULLS(PARSE_JSON('{"a":1,"b":null}'))` → `{"a":1}` |

### 数组/对象展开 {#array-object-expansion}

| 函数 | 描述 | 示例 |
|----------|-------------|--------|
| [JSON_EACH](/tidb-cloud-lake/sql/json-each.md) | 将 JSON 对象展开为键值对 | `JSON_EACH(PARSE_JSON('{"a":1,"b":2}'))` |
| [JSON_ARRAY_ELEMENTS](/tidb-cloud-lake/sql/json-array-elements.md) | 将 JSON 数组展开为单独的元素 | `JSON_ARRAY_ELEMENTS(PARSE_JSON('[1,2,3]'))` |

## 数组函数 {#array-functions}

| 函数 | 描述 | 示例 |
|----------|-------------|--------|
| [ARRAY](/tidb-cloud-lake/sql/array.md) | 从表达式构建数组 | `ARRAY(1, 2, 3)` |
| [ARRAY_CONSTRUCT](/tidb-cloud-lake/sql/array-construct.md) | 从单个值创建数组 | `ARRAY_CONSTRUCT(1, 2, 3)` |
| [RANGE](/tidb-cloud-lake/sql/range.md) | 生成由连续数字组成的数组 | `RANGE(1, 5)` |
| [ARRAY_GENERATE_RANGE](/tidb-cloud-lake/sql/array-generate-range.md) | 生成可选步长的序列 | `ARRAY_GENERATE_RANGE(0, 6, 2)` |
| [GET](/tidb-cloud-lake/sql/get.md) | 通过索引从数组中获取元素 | `GET([1,2,3], 0)` |
| [ARRAY_GET](/tidb-cloud-lake/sql/array-get.md) | GET 函数的别名 | `ARRAY_GET([1,2,3], 1)` |
| [CONTAINS](/tidb-cloud-lake/sql/contains.md) | 检查数组是否包含指定值 | `CONTAINS([1,2,3], 2)` |
| [ARRAY_CONTAINS](/tidb-cloud-lake/sql/array-contains.md) | 检查数组是否包含指定值 | `ARRAY_CONTAINS([1,2,3], 2)` |
| [ARRAY_SIZE](/tidb-cloud-lake/sql/array-size.md) | 返回数组长度（别名：`ARRAY_LENGTH`） | `ARRAY_SIZE([1,2,3])` |
| [ARRAY_COUNT](/tidb-cloud-lake/sql/array-count.md) | 统计非 `NULL` 元素的数量 | `ARRAY_COUNT([1,NULL,2])` |
| [ARRAY_ANY](/tidb-cloud-lake/sql/array-any.md) | 返回第一个非 `NULL` 条目 | `ARRAY_ANY([NULL,'a','b'])` |
| [ARRAY_APPEND](/tidb-cloud-lake/sql/array-append.md) | 在数组末尾追加元素 | `ARRAY_APPEND([1,2], 3)` |
| [ARRAY_PREPEND](/tidb-cloud-lake/sql/array-prepend.md) | 在数组开头前置元素 | `ARRAY_PREPEND([2,3], 1)` |
| [ARRAY_INSERT](/tidb-cloud-lake/sql/array-insert.md) | 在指定位置插入元素 | `ARRAY_INSERT([1,3], 1, 2)` |
| [ARRAY_REMOVE](/tidb-cloud-lake/sql/array-remove.md) | 移除指定元素的所有出现项 | `ARRAY_REMOVE([1,2,2,3], 2)` |
| [ARRAY_REMOVE_FIRST](/tidb-cloud-lake/sql/array-remove-first.md) | 移除数组中的第一个元素 | `ARRAY_REMOVE_FIRST([1,2,3])` |
| [ARRAY_REMOVE_LAST](/tidb-cloud-lake/sql/array-remove-last.md) | 移除数组中的最后一个元素 | `ARRAY_REMOVE_LAST([1,2,3])` |
| [ARRAY_CONCAT](/tidb-cloud-lake/sql/array-concat.md) | 拼接多个数组 | `ARRAY_CONCAT([1,2], [3,4])` |
| [ARRAY_SLICE](/tidb-cloud-lake/sql/array-slice.md) | 提取数组的一部分 | `ARRAY_SLICE([1,2,3,4], 1, 2)` |
| [SLICE](/tidb-cloud-lake/sql/slice.md) | ARRAY_SLICE 函数的别名 | `SLICE([1,2,3,4], 1, 2)` |
| [ARRAYS_ZIP](/tidb-cloud-lake/sql/arrays-zip.md) | 按元素位置组合多个数组 | `ARRAYS_ZIP([1,2], ['a','b'])` |
| [ARRAY_DISTINCT](/tidb-cloud-lake/sql/array-distinct.md) | 返回数组中的唯一元素 | `ARRAY_DISTINCT([1,2,2,3])` |
| [ARRAY_UNIQUE](/tidb-cloud-lake/sql/array-unique.md) | ARRAY_DISTINCT 函数的别名 | `ARRAY_UNIQUE([1,2,2,3])` |
| [ARRAY_INTERSECTION](/tidb-cloud-lake/sql/array-intersection.md) | 返回数组之间的公共元素 | `ARRAY_INTERSECTION([1,2,3], [2,3,4])` |
| [ARRAY_EXCEPT](/tidb-cloud-lake/sql/array-except.md) | 返回第一个数组中存在但第二个数组中不存在的元素 | `ARRAY_EXCEPT([1,2,3], [2,3])` |
| [ARRAY_OVERLAP](/tidb-cloud-lake/sql/array-overlap.md) | 检查数组是否有公共元素 | `ARRAY_OVERLAP([1,2], [2,3])` |
| [ARRAY_TRANSFORM](/tidb-cloud-lake/sql/json-array-transform.md) | 对每个数组元素应用一个函数 | `ARRAY_TRANSFORM([1,2,3], x -> x * 2)` |
| [ARRAY_FILTER](/tidb-cloud-lake/sql/array-filter.md) | 根据条件过滤数组元素 | `ARRAY_FILTER([1,2,3,4], x -> x > 2)` |
| [ARRAY_REDUCE](/tidb-cloud-lake/sql/array-reduce.md) | 使用聚合将数组归约为单个值 | `ARRAY_REDUCE([1,2,3], 0, (acc, x) -> acc + x)` |
| [ARRAY_AGGREGATE](/tidb-cloud-lake/sql/array-aggregate.md) | 使用函数聚合数组元素 | `ARRAY_AGGREGATE([1,2,3], 'sum')` |
| [ARRAY_SUM](/tidb-cloud-lake/sql/array-sum.md) | 数值的总和 | `ARRAY_SUM([1,2,3])` |
| [ARRAY_AVG](/tidb-cloud-lake/sql/array-avg.md) | 数值的平均值 | `ARRAY_AVG([1,2,3])` |
| [ARRAY_MEDIAN](/tidb-cloud-lake/sql/array-median.md) | 数值的中位数 | `ARRAY_MEDIAN([1,3,2])` |
| [ARRAY_MIN](/tidb-cloud-lake/sql/array-min.md) | 最小值 | `ARRAY_MIN([1,2,3])` |
| [ARRAY_MAX](/tidb-cloud-lake/sql/array-max.md) | 最大值 | `ARRAY_MAX([1,2,3])` |
| [ARRAY_STDDEV_POP](/tidb-cloud-lake/sql/array-stddev-pop.md) | 总体标准差 | `ARRAY_STDDEV_POP([1,2,3])` |
| [ARRAY_STDDEV_SAMP](/tidb-cloud-lake/sql/array-stddev-samp.md) | 样本标准差 | `ARRAY_STDDEV_SAMP([1,2,3])` |
| [ARRAY_KURTOSIS](/tidb-cloud-lake/sql/array-kurtosis.md) | 超额峰度 | `ARRAY_KURTOSIS([1,2,3,4])` |
| [ARRAY_SKEWNESS](/tidb-cloud-lake/sql/array-skewness.md) | 偏度 | `ARRAY_SKEWNESS([1,2,3,10])` |
| [ARRAY_APPROX_COUNT_DISTINCT](/tidb-cloud-lake/sql/array-approx-count-distinct.md) | 近似去重计数 | `ARRAY_APPROX_COUNT_DISTINCT([1,1,2])` |
| [ARRAY_SORT](/tidb-cloud-lake/sql/array-sort.md) | 对值进行排序；不同变体可控制顺序/空值处理 | `ARRAY_SORT([3,1,2])` |
| [ARRAY_TO_STRING](/tidb-cloud-lake/sql/array-to-string.md) | 连接数组元素 | `ARRAY_TO_STRING(['a','b'], ',')` |
| [ARRAY_COMPACT](/tidb-cloud-lake/sql/array-compact.md) | 从数组中移除空值 | `ARRAY_COMPACT([1, NULL, 2, NULL, 3])` |
| [ARRAY_FLATTEN](/tidb-cloud-lake/sql/array-flatten.md) | 将嵌套数组展平为单个数组 | `ARRAY_FLATTEN([[1,2], [3,4]])` |
| [ARRAY_REVERSE](/tidb-cloud-lake/sql/array-reverse.md) | 反转数组元素的顺序 | `ARRAY_REVERSE([1,2,3])` |
| [ARRAY_INDEXOF](/tidb-cloud-lake/sql/array-indexof.md) | 返回元素首次出现的索引 | `ARRAY_INDEXOF([1,2,3,2], 2)` |
| [UNNEST](/tidb-cloud-lake/sql/unnest.md) | 将数组展开为多行 | `UNNEST([1,2,3])` |

## 对象函数 {#object-functions}

| 函数 | 描述 | 示例 |
|----------|-------------|--------|
| [OBJECT_CONSTRUCT](/tidb-cloud-lake/sql/object-construct.md) | 从键值对创建 JSON 对象 | `OBJECT_CONSTRUCT('name', 'John', 'age', 30)` |
| [OBJECT_CONSTRUCT_KEEP_NULL](/tidb-cloud-lake/sql/object-construct-keep-null.md) | 创建保留空值的 JSON 对象 | `OBJECT_CONSTRUCT_KEEP_NULL('a', 1, 'b', NULL)` |
| [OBJECT_KEYS](/tidb-cloud-lake/sql/object-keys.md) | 以数组形式返回 JSON 对象中的所有键 | `OBJECT_KEYS(PARSE_JSON('{"a":1,"b":2}'))` |
| [OBJECT_INSERT](/tidb-cloud-lake/sql/object-insert.md) | 在 JSON 对象中插入或修改键值对 | `OBJECT_INSERT(json_obj, 'new_key', 'value')` |
| [OBJECT_DELETE](/tidb-cloud-lake/sql/object-delete.md) | 从 JSON 对象中移除键值对 | `OBJECT_DELETE(json_obj, 'key_to_remove')` |
| [OBJECT_PICK](/tidb-cloud-lake/sql/object-pick.md) | 创建仅包含指定键的新对象 | `OBJECT_PICK(json_obj, 'name', 'age')` |

## Map 函数 {#map-functions}

| 函数 | 描述 | 示例 |
|----------|-------------|--------|
| [MAP_CAT](/tidb-cloud-lake/sql/map-cat.md) | 将多个 map 合并为一个 map | `MAP_CAT({'a':1}, {'b':2})` |
| [MAP_KEYS](/tidb-cloud-lake/sql/map-keys.md) | 以数组形式返回 map 中的所有键 | `MAP_KEYS({'a':1, 'b':2})` |
| [MAP_VALUES](/tidb-cloud-lake/sql/map-values.md) | 以数组形式返回 map 中的所有值 | `MAP_VALUES({'a':1, 'b':2})` |
| [MAP_SIZE](/tidb-cloud-lake/sql/map-size.md) | 返回 map 中键值对的数量 | `MAP_SIZE({'a':1, 'b':2})` |
| [MAP_CONTAINS_KEY](/tidb-cloud-lake/sql/map-contains-key.md) | 检查 map 是否包含指定键 | `MAP_CONTAINS_KEY({'a':1}, 'a')` |
| [MAP_INSERT](/tidb-cloud-lake/sql/map-insert.md) | 向 map 中插入键值对 | `MAP_INSERT({'a':1}, 'b', 2)` |
| [MAP_DELETE](/tidb-cloud-lake/sql/map-delete.md) | 从 map 中移除键值对 | `MAP_DELETE({'a':1, 'b':2}, 'b')` |
| [MAP_TRANSFORM_KEYS](/tidb-cloud-lake/sql/map-transform-keys.md) | 对 map 中的每个键应用一个函数 | `MAP_TRANSFORM_KEYS(map, k -> UPPER(k))` |
| [MAP_TRANSFORM_VALUES](/tidb-cloud-lake/sql/map-transform-values.md) | 对 map 中的每个值应用一个函数 | `MAP_TRANSFORM_VALUES(map, v -> v * 2)` |
| [MAP_FILTER](/tidb-cloud-lake/sql/map-filter.md) | 根据谓词过滤键值对 | `MAP_FILTER(map, (k, v) -> v > 10)` |
| [MAP_PICK](/tidb-cloud-lake/sql/map-pick.md) | 创建仅包含指定键的新 map | `MAP_PICK({'a':1, 'b':2, 'c':3}, 'a', 'c')` |

## 类型转换函数 {#type-conversion-functions}

| 函数 | 描述 | 示例 |
|----------|-------------|---------|
| [AS_BOOLEAN](/tidb-cloud-lake/sql/as-boolean.md) | 将 VARIANT 值转换为 BOOLEAN | `AS_BOOLEAN(PARSE_JSON('true'))` |
| [AS_INTEGER](/tidb-cloud-lake/sql/as-integer.md) | 将 VARIANT 值转换为 BIGINT | `AS_INTEGER(PARSE_JSON('42'))` |
| [AS_FLOAT](/tidb-cloud-lake/sql/as-float.md) | 将 VARIANT 值转换为 DOUBLE | `AS_FLOAT(PARSE_JSON('3.14'))` |
| [AS_DECIMAL](/tidb-cloud-lake/sql/as-decimal.md) | 将 VARIANT 值转换为 DECIMAL | `AS_DECIMAL(PARSE_JSON('12.34'))` |
| [AS_STRING](/tidb-cloud-lake/sql/as-string.md) | 将 VARIANT 值转换为 STRING | `AS_STRING(PARSE_JSON('"hello"'))` |
| [AS_BINARY](/tidb-cloud-lake/sql/as-binary.md) | 将 VARIANT 值转换为 BINARY | `AS_BINARY(TO_BINARY('abcd')::VARIANT)` |
| [AS_DATE](/tidb-cloud-lake/sql/as-date.md) | 将 VARIANT 值转换为 DATE | `AS_DATE(TO_DATE('2025-10-11')::VARIANT)` |
| [AS_ARRAY](/tidb-cloud-lake/sql/as-array.md) | 将 VARIANT 值转换为 ARRAY | `AS_ARRAY(PARSE_JSON('[1,2,3]'))` |
| [AS_OBJECT](/tidb-cloud-lake/sql/as-object.md) | 将 VARIANT 值转换为 OBJECT | `AS_OBJECT(PARSE_JSON('{"a":1}'))` |

## 类型谓词函数 {#type-predicate-functions}

| 函数 | 描述 | 示例 |
|----------|-------------|--------|
| [IS_ARRAY](/tidb-cloud-lake/sql/is-array.md) | 检查 JSON 值是否为数组 | `IS_ARRAY(PARSE_JSON('[1,2,3]'))` |
| [IS_OBJECT](/tidb-cloud-lake/sql/is-object.md) | 检查 JSON 值是否为对象 | `IS_OBJECT(PARSE_JSON('{"a":1}'))` |
| [IS_STRING](/tidb-cloud-lake/sql/is-string.md) | 检查 JSON 值是否为字符串 | `IS_STRING(PARSE_JSON('"hello"'))` |
| [IS_INTEGER](/tidb-cloud-lake/sql/is-integer.md) | 检查 JSON 值是否为整数 | `IS_INTEGER(PARSE_JSON('42'))` |
| [IS_FLOAT](/tidb-cloud-lake/sql/is-float.md) | 检查 JSON 值是否为浮点数 | `IS_FLOAT(PARSE_JSON('3.14'))` |
| [IS_BOOLEAN](/tidb-cloud-lake/sql/is-boolean.md) | 检查 JSON 值是否为布尔值 | `IS_BOOLEAN(PARSE_JSON('true'))` |
| [IS_NULL_VALUE](/tidb-cloud-lake/sql/is-null-value.md) | 检查 JSON 值是否为空值 | `IS_NULL_VALUE(PARSE_JSON('null'))` |