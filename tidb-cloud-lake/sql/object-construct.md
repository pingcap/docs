---
title: OBJECT_CONSTRUCT
summary: 创建包含键和值的 JSON 对象。
---

# OBJECT_CONSTRUCT

创建包含键和值的 JSON 对象。

- 参数是零个或多个键值对（其中键为字符串，值可以是任意类型）。
- 如果键或值为 NULL，则该键值对会从结果对象中省略。
- 键之间必须互不相同，并且结果 JSON 中键的顺序可能与您指定的顺序不同。
- `TRY_OBJECT_CONSTRUCT` 在构建对象时如果发生错误，会返回 NULL 值。

## 别名 {#aliases}

- `JSON_OBJECT`
- `TRY_JSON_OBJECT`

另请参阅：[OBJECT_CONSTRUCT_KEEP_NULL](/tidb-cloud-lake/sql/object-construct-keep-null.md)

## 语法 {#syntax}

```sql
OBJECT_CONSTRUCT(key1, value1[, key2, value2[, ...]])

TRY_OBJECT_CONSTRUCT(key1, value1[, key2, value2[, ...]])
```

## 返回类型 {#return-type}

JSON 对象。

## 示例 {#examples}

```sql
SELECT OBJECT_CONSTRUCT();
┌────────────────┐
│ object_construct() │
├────────────────┤
│ {}            │
└────────────────┘

SELECT OBJECT_CONSTRUCT('a', 3.14, 'b', 'xx', 'c', NULL);
┌──────────────────────────────────────────────┐
│ object_construct('a', 3.14, 'b', 'xx', 'c', null) │
├──────────────────────────────────────────────┤
│ {"a":3.14,"b":"xx"}                          │
└──────────────────────────────────────────────┘

SELECT OBJECT_CONSTRUCT('fruits', ['apple', 'banana', 'orange'], 'vegetables', ['carrot', 'celery']);
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│ object_construct('fruits', ['apple', 'banana', 'orange'], 'vegetables', ['carrot', 'celery']) │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│ {"fruits":["apple","banana","orange"],"vegetables":["carrot","celery"]}                  │
└──────────────────────────────────────────────────────────────────────────────────────────┘

SELECT OBJECT_CONSTRUCT('key');
  |
1 | SELECT OBJECT_CONSTRUCT('key')
  |        ^^^^^^^^^^^^^^^^^^ The number of keys and values must be equal while evaluating function `object_construct('key')`

SELECT TRY_OBJECT_CONSTRUCT('key');
┌───────────────────────────┐
│ try_object_construct('key') │
├───────────────────────────┤
│ NULL                   │
└───────────────────────────┘
```