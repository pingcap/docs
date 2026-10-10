---
title: IS_FLOAT
summary: 入力された JSON 値が float かどうかを確認します。
---

# IS_FLOAT

入力された JSON 値が float かどうかを確認します。

## 構文 {#syntax}

```sql
IS_FLOAT( <expr> )
```

## 戻り値の型 {#return-type}

入力された JSON 値が float の場合は `true` を返し、それ以外の場合は `false` を返します。

## 例 {#examples}

```sql
SELECT
  IS_FLOAT(PARSE_JSON('1.23')),
  IS_FLOAT(PARSE_JSON('[1,2,3]'));

┌────────────────────────────────────────────────────────────────┐
│ is_float(parse_json('1.23')) │ is_float(parse_json('[1,2,3]')) │
├──────────────────────────────┼─────────────────────────────────┤
│ true                         │ false                           │
└────────────────────────────────────────────────────────────────┘
```