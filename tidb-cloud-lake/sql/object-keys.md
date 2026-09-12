---
title: OBJECT_KEYS
summary: 以字符串数组的形式返回最外层 JSON 对象的键。
---

# OBJECT_KEYS

以字符串数组的形式返回最外层 JSON 对象的键。

## 别名 {#aliases}

- `JSON_OBJECT_KEYS`

## 语法 {#syntax}

```sql
OBJECT_KEYS(<variant>)
```

## 返回类型 {#return-type}

STRING 的 ARRAY。

## 示例 {#examples}

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