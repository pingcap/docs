---
title: OBJECT_KEYS
summary: 最も外側の JSON オブジェクトのキーを文字列の配列として返します。
---

# OBJECT_KEYS

最も外側の JSON オブジェクトのキーを文字列の配列として返します。

## エイリアス {#aliases}

- `JSON_OBJECT_KEYS`

## 構文 {#syntax}

```sql
OBJECT_KEYS(<variant>)
```

## 戻り値の型 {#return-type}

STRING の ARRAY。

## 例 {#examples}

```sql
SELECT OBJECT_KEYS('{"a":1, "b":2, "c": {"d":3}}'::VARIANT);

-[ RECORD 1 ]-----------------------------------
object_keys('{"a":1, "b":2, "c": {"d":3}}'::VARIANT): ["a","b","c"]

-- Example with a table
CREATE TABLE t (var VARIANT);
INSERT INTO t VALUES ('{"a":1, "b":2}'), ('{"x":10, "y":20}');

SELECT id, object_keys(var), json_object_keys(var) FROM t;

┌───────────┬──────────────────┬───────────────────────┐
│    id     │  object_keys(var) │ json_object_keys(var) │
├───────────┼──────────────────┼───────────────────────┤
│ 1         │ ["a","b"]        │ ["a","b"]           │
│ 2         │ ["x","y"]        │ ["x","y"]           │
└───────────┴──────────────────┴───────────────────────┘
```