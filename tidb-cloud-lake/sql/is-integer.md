---
title: IS_INTEGER
summary: 入力された JSON 値が整数かどうかを確認します。
---

# IS_INTEGER

入力された JSON 値が整数かどうかを確認します。

## 構文 {#syntax}

```sql
IS_INTEGER( <expr> )
```

## 戻り値の型 {#return-type}

入力された JSON 値が整数の場合は `true` を返し、それ以外の場合は `false` を返します。

## 例 {#examples}

```sql
SELECT
  IS_INTEGER(PARSE_JSON('123')),
  IS_INTEGER(PARSE_JSON('[1,2,3]'));

┌───────────────────────────────────────────────────────────────────┐
│ is_integer(parse_json('123')) │ is_integer(parse_json('[1,2,3]')) │
├───────────────────────────────┼───────────────────────────────────┤
│ true                          │ false                             │
└───────────────────────────────────────────────────────────────────┘
```