---
title: OBJECT_CONSTRUCT
summary: キーと値を持つ JSON オブジェクトを作成します。
---

# OBJECT_CONSTRUCT

キーと値を持つ JSON オブジェクトを作成します。

- 引数は 0 個以上のキーと値のペアです（キーは文字列、値は任意の型です）。
- キーまたは値が NULL の場合、そのキーと値のペアは結果のオブジェクトから省略されます。
- キーは互いに重複してはいけません。また、結果の JSON におけるキーの順序は、指定した順序と異なる場合があります。
- `TRY_OBJECT_CONSTRUCT` は、オブジェクトの構築時にエラーが発生した場合に NULL 値を返します。

## エイリアス {#aliases}

- `JSON_OBJECT`
- `TRY_JSON_OBJECT`

関連情報: [OBJECT_CONSTRUCT_KEEP_NULL](/tidb-cloud-lake/sql/object-construct-keep-null.md)

## 構文 {#syntax}

```sql
OBJECT_CONSTRUCT(key1, value1[, key2, value2[, ...]])

TRY_OBJECT_CONSTRUCT(key1, value1[, key2, value2[, ...]])
```

## 戻り値の型 {#return-type}

JSON オブジェクト。

## 例 {#examples}

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