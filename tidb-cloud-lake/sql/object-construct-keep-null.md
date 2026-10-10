---
title: OBJECT_CONSTRUCT_KEEP_NULL
summary: キーと値を持つ JSON オブジェクトを作成します。
---

# OBJECT_CONSTRUCT_KEEP_NULL

キーと値を持つ JSON オブジェクトを作成します。

- 引数には、0 個以上のキーと値のペアを指定します（キーは文字列、値は任意の型です）。
- キーが NULL の場合、そのキーと値のペアは結果のオブジェクトから省略されます。ただし、値が NULL の場合、そのキーと値のペアは保持されます。
- キーは互いに重複していてはならず、結果の JSON における順序は、指定した順序と異なる場合があります。
- `TRY_OBJECT_CONSTRUCT_KEEP_NULL` は、オブジェクトの構築中にエラーが発生した場合に NULL 値を返します。

## エイリアス {#aliases}

- `JSON_OBJECT_KEEP_NULL`
- `TRY_JSON_OBJECT_KEEP_NULL`

関連情報: [OBJECT_CONSTRUCT](/tidb-cloud-lake/sql/object-construct.md)

## 構文 {#syntax}

```sql
OBJECT_CONSTRUCT_KEEP_NULL(key1, value1[, key2, value2[, ...]])

TRY_OBJECT_CONSTRUCT_KEEP_NULL(key1, value1[, key2, value2[, ...]])
```

## 戻り値の型 {#return-type}

JSON オブジェクト。

## 例 {#examples}

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