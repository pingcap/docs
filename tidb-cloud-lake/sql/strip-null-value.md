---
title: STRIP_NULL_VALUE
summary: JSON の null 値を SQL の NULL 値に変換します。その他の variant 値は変更されずにそのまま渡されます。
---

# STRIP_NULL_VALUE

JSON の null 値を SQL の NULL 値に変換します。その他の variant 値は変更されずにそのまま渡されます。

## 構文 {#syntax}

```sql
STRIP_NULL_VALUE(<variant_expr>)
```

## 引数 {#arguments}

VARIANT 型の式です。

## 戻り値の型 {#return-type}

- 式が JSON の null 値である場合、この関数は SQL の NULL を返します。
- 式が JSON の null 値でない場合、この関数は入力値を返します。

## 例 {#examples}

```sql
SELECT STRIP_NULL_VALUE(PARSE_JSON('null')) AS value;

╭───────╮
│ value │
├───────┤
│ NULL  │
╰───────╯

SELECT STRIP_NULL_VALUE(PARSE_JSON('{"name": "Alice", "age": 30, "city": null}')) AS value;

╭───────────────────────────────────────╮
│                 value                 │
├───────────────────────────────────────┤
│ {"age":30,"city":null,"name":"Alice"} │
╰───────────────────────────────────────╯
```