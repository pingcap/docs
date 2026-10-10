---
title: TRY_TO_BINARY
summary: 入力式をバイナリ値に変換する TO_BINARY の拡張版で、変換に失敗した場合はエラーを返す代わりに NULL を返します。
---

# TRY_TO_BINARY

[TO_BINARY](/tidb-cloud-lake/sql/binary.md) の拡張版で、入力式をバイナリ値に変換します。変換に失敗した場合は、エラーを発生させる代わりに `NULL` を返します。

関連情報: [TO_BINARY](/tidb-cloud-lake/sql/binary.md)

## 構文 {#syntax}

```sql
TRY_TO_BINARY( <expr> )
```

## 例 {#examples}

次の例では、JSON データを正常にバイナリへ変換します。

```sql
SELECT TRY_TO_BINARY(PARSE_JSON('{"key":"value", "number":123}')) AS binary_variant_success;

┌──────────────────────────────────────────────────────────────────────────┐
│                              binary_variant                              │
├──────────────────────────────────────────────────────────────────────────┤
│ 40000002100000031000000610000005200000026B65796E756D62657276616C7565507B │
└──────────────────────────────────────────────────────────────────────────┘
```

次の例は、入力が `NULL` の場合、この関数が変換できないことを示しています。

```sql
SELECT TRY_TO_BINARY(PARSE_JSON(NULL)) AS binary_variant_invalid_json;

┌─────────────────────────────┐
│ binary_variant_invalid_json │
├─────────────────────────────┤
│ NULL                        │
└─────────────────────────────┘
```