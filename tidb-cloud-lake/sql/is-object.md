---
title: IS_OBJECT
summary: 入力値が JSON オブジェクトかどうかを確認します。
---

# IS_OBJECT

入力値が JSON オブジェクトかどうかを確認します。

## 構文 {#syntax}

```sql
IS_OBJECT( <expr> )
```

## 戻り値の型 {#return-type}

入力された JSON 値が JSON オブジェクトの場合は `true` を返し、それ以外の場合は `false` を返します。

## 例 {#examples}

```sql
SELECT
  IS_OBJECT(PARSE_JSON('{"a":"b"}')), -- JSON Object
  IS_OBJECT(PARSE_JSON('["a","b","c"]')); --JSON Array

┌─────────────────────────────────────────────────────────────────────────────┐
│ is_object(parse_json('{"a":"b"}')) │ is_object(parse_json('["a","b","c"]')) │
├────────────────────────────────────┼────────────────────────────────────────┤
│ true                               │ false                                  │
└─────────────────────────────────────────────────────────────────────────────┘
```