---
title: JSON_STRIP_NULLS
summary: JSON オブジェクトから null 値を持つすべてのプロパティを削除します。
---

# JSON_STRIP_NULLS

JSON オブジェクトから null 値を持つすべてのプロパティを削除します。

## 構文 {#syntax}

```sql
JSON_STRIP_NULLS(<variant_expr>)
```

## 引数 {#arguments}

VARIANT 型の式です。

## 戻り値の型 {#return-type}

VARIANT。

## 例 {#examples}

```sql
SELECT JSON_STRIP_NULLS(PARSE_JSON('{"name": "Alice", "age": 30, "city": null}')) AS value;

╭───────────────────────────╮
│           value           │
├───────────────────────────┤
│ {"age":30,"name":"Alice"} │
╰───────────────────────────╯
```