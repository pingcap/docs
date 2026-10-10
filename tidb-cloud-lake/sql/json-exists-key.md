---
title: JSON_EXISTS_KEY
summary: JSON オブジェクトに 1 つ以上のキーが含まれているかどうかを確認します。
---

# JSON_EXISTS_KEY

JSON オブジェクトに 1 つ以上のキーが含まれているかどうかを確認します。

- `JSON_EXISTS_KEY` は単一のキーをテストします。
- `JSON_EXISTS_ANY_KEYS` はキーの配列を受け取り、少なくとも 1 つのキーが存在する場合に `TRUE` を返します。
- `JSON_EXISTS_ALL_KEYS` は、配列内のすべてのキーが存在する場合にのみ `TRUE` を返します。

## 構文 {#syntax}

```sql
JSON_EXISTS_KEY(<variant>, <key>)
JSON_EXISTS_ANY_KEYS(<variant>, <array_of_keys>)
JSON_EXISTS_ALL_KEYS(<variant>, <array_of_keys>)
```

## 戻り値の型 {#return-type}

`BOOLEAN`

## 例 {#examples}

```sql
SELECT JSON_EXISTS_KEY(PARSE_JSON('{"a":1,"b":2}'), 'b') AS has_b;

┌──────┐
│ has_b│
├──────┤
│ true │
└──────┘
```

```sql
SELECT JSON_EXISTS_ANY_KEYS(PARSE_JSON('{"a":1,"b":2}'), ['x','b']) AS any_key;

┌────────┐
│ any_key│
├────────┤
│ true   │
└────────┘
```

```sql
SELECT JSON_EXISTS_ALL_KEYS(PARSE_JSON('{"a":1,"b":2}'), ['a','b','c']) AS all_keys;

┌────────┐
│ all_keys│
├────────┤
│ false  │
└────────┘
```

```sql
SELECT JSON_EXISTS_ALL_KEYS(PARSE_JSON('{"a":1,"b":2}'), ['a','b']) AS all_keys;

┌────────┐
│ all_keys│
├────────┤
│ true   │
└────────┘
```