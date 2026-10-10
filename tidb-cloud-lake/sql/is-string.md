---
title: IS_STRING
summary: 入力 JSON 値が文字列かどうかを確認します。
---

# IS_STRING

入力 JSON 値が文字列かどうかを確認します。

## 構文 {#syntax}

```sql
IS_STRING( <expr> )
```

## 戻り値の型 {#return-type}

入力 JSON 値が文字列の場合は `true` を返し、それ以外の場合は `false` を返します。

## 例 {#examples}

```sql
SELECT
  IS_STRING(PARSE_JSON('"abc"')),
  IS_STRING(PARSE_JSON('123'));

┌───────────────────────────────────────────────────────────────┐
│ is_string(parse_json('"abc"')) │ is_string(parse_json('123')) │
├────────────────────────────────┼──────────────────────────────┤
│ true                           │ false                        │
└───────────────────────────────────────────────────────────────┘
```