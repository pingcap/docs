---
title: IS_NULL_VALUE
summary: 入力値が JSON null かどうかを確認します。この関数は SQL NULL ではなく、JSON null を判定することに注意してください。値が SQL NULL かどうかを確認するには、IS_NULL を使用します。
---

# IS_NULL_VALUE

入力値が JSON `null` かどうかを確認します。この関数は SQL NULL ではなく、JSON `null` を判定することに注意してください。値が SQL NULL かどうかを確認するには、[IS_NULL](/tidb-cloud-lake/sql/is-null.md) を使用します。

```json title='JSON null Example:'
{
  "name": "John",
  "age": null
}
```

## 構文 {#syntax}

```sql
IS_NULL_VALUE( <expr> )
```

## 戻り値の型 {#return-type}

入力値が JSON `null` の場合は `true` を返し、それ以外の場合は `false` を返します。

## 例 {#examples}

```sql
SELECT
  IS_NULL_VALUE(PARSE_JSON('{"name":"John", "age":null}') :age), --JSON null
  IS_NULL(NULL); --SQL NULL

┌──────────────────────────────────────────────────────────────────────────────┐
│ is_null_value(parse_json('{"name":"john", "age":null}'):age) │ is_null(null) │
├──────────────────────────────────────────────────────────────┼───────────────┤
│ true                                                         │ true          │
└──────────────────────────────────────────────────────────────────────────────┘
```