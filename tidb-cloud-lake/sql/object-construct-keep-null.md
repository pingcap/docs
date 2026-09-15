---
title: OBJECT_CONSTRUCT_KEEP_NULL
summary: 创建包含键和值的 JSON 对象。
---

# OBJECT_CONSTRUCT_KEEP_NULL

创建包含键和值的 JSON 对象。

- 参数是零个或多个键值对（其中键为字符串，值可以是任意类型）。
- 如果键为 NULL，则结果对象中会省略该键值对。但是，如果值为 NULL，则会保留该键值对。
- 键之间必须互不相同，并且结果 JSON 中键的顺序可能与您指定的顺序不同。
- `TRY_OBJECT_CONSTRUCT_KEEP_NULL` 在构建对象时如果发生错误，会返回 NULL 值。

## 别名 {#aliases}

- `JSON_OBJECT_KEEP_NULL`
- `TRY_JSON_OBJECT_KEEP_NULL`

另请参阅：[OBJECT_CONSTRUCT](/tidb-cloud-lake/sql/object-construct.md)

## 语法 {#syntax}

```sql
OBJECT_CONSTRUCT_KEEP_NULL(key1, value1[, key2, value2[, ...]])

TRY_OBJECT_CONSTRUCT_KEEP_NULL(key1, value1[, key2, value2[, ...]])
```

## 返回类型 {#return-type}

JSON 对象。

## 示例 {#examples}

```sql
SELECT OBJECT_CONSTRUCT_KEEP_NULL();
┌──────────────────────────────┐
│ object_construct_keep_null() │
├──────────────────────────────┤
│ {}                      │
└──────────────────────────────┘

SELECT OBJECT_CONSTRUCT_KEEP_NULL('a', 3.14, 'b', 'xx', 'c', NULL);
┌───────────────────────────────────────────────────────────┐
│ object_construct_keep_null('a', 3.14, 'b', 'xx', 'c', null) │
├───────────────────────────────────────────────────────────┤
│ {"a":3.14,"b":"xx","c":null}                           │
└───────────────────────────────────────────────────────────┘

SELECT OBJECT_CONSTRUCT_KEEP_NULL('fruits', ['apple', 'banana', 'orange'], 'vegetables', ['carrot', 'celery']);
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ object_construct_keep_null('fruits', ['apple', 'banana', 'orange'], 'vegetables', ['carrot', 'celery']) │
├───────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ {"fruits":["apple","banana","orange"],"vegetables":["carrot","celery"]}                            │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

SELECT OBJECT_CONSTRUCT_KEEP_NULL('key');
  |
1 | SELECT OBJECT_CONSTRUCT_KEEP_NULL('key')
  |        ^^^^^^^^^^^^^^^^^^ The number of keys and values must be equal while evaluating function `object_construct_keep_null('key')`

SELECT TRY_OBJECT_CONSTRUCT_KEEP_NULL('key');
┌─────────────────────────────────────┐
│ try_object_construct_keep_null('key') │
├─────────────────────────────────────┤
│ NULL                             │
└─────────────────────────────────────┘
```