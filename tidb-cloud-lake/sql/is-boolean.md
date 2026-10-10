---
title: IS_BOOLEAN
summary: 入力された JSON 値が boolean かどうかをチェックします。
---

# IS_BOOLEAN

入力された JSON 値が boolean かどうかをチェックします。

## 構文 {#syntax}

```sql
IS_BOOLEAN( <expr> )
```

## 戻り値の型 {#return-type}

入力された JSON 値が boolean の場合は `true` を返し、それ以外の場合は `false` を返します。

## 例 {#examples}

```sql
SELECT
  IS_BOOLEAN(PARSE_JSON('true')),
  IS_BOOLEAN(PARSE_JSON('[1,2,3]'));

┌────────────────────────────────────────────────────────────────────┐
│ is_boolean(parse_json('true')) │ is_boolean(parse_json('[1,2,3]')) │
├────────────────────────────────┼───────────────────────────────────┤
│ true                           │ false                             │
└────────────────────────────────────────────────────────────────────┘
```