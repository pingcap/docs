---
title: JSON_CONTAINS_IN_LEFT
summary: 2 つの VARIANT 値間の包含関係をテストします。
---

# JSON_CONTAINS_IN_LEFT

2 つの `VARIANT` 値間の包含関係をテストします。

- `JSON_CONTAINS_IN_LEFT(left, right)` は、*left* が *right* を含む場合（つまり、*left* が上位集合である場合）に `TRUE` を返します。
- `JSON_CONTAINS_IN_RIGHT(left, right)` は、*right* が *left* を含む場合に `TRUE` を返します。

包含判定は、JSON オブジェクトと配列の両方で機能します。

## 構文 {#syntax}

```sql
JSON_CONTAINS_IN_LEFT(<variant_left>, <variant_right>)
JSON_CONTAINS_IN_RIGHT(<variant_left>, <variant_right>)
```

## 戻り値の型 {#return-type}

`BOOLEAN`

## 例 {#examples}

```sql
SELECT JSON_CONTAINS_IN_LEFT(PARSE_JSON('{"a":1,"b":{"c":2}}'),
                             PARSE_JSON('{"b":{"c":2}}')) AS left_contains;

┌──────────────┐
│ left_contains│
├──────────────┤
│ true         │
└──────────────┘
```

```sql
SELECT JSON_CONTAINS_IN_LEFT(PARSE_JSON('[1,2,3]'),
                             PARSE_JSON('[2,3]')) AS left_contains;

┌──────────────┐
│ left_contains│
├──────────────┤
│ true         │
└──────────────┘
```

```sql
SELECT JSON_CONTAINS_IN_LEFT(PARSE_JSON('[1,2]'),
                             PARSE_JSON('[2,4]')) AS left_contains;

┌──────────────┐
│ left_contains│
├──────────────┤
│ false        │
└──────────────┘
```

```sql
SELECT JSON_CONTAINS_IN_RIGHT(PARSE_JSON('{"a":1}'),
                              PARSE_JSON('{"a":1,"b":2}')) AS right_contains;

┌───────────────┐
│ right_contains│
├───────────────┤
│ true          │
└───────────────┘
```