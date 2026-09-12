---
title: TRY_TO_BINARY
summary: TO_BINARY 的增强版本，可将输入表达式转换为二进制值；如果转换失败，则返回 NULL 而不是报错。
---

# TRY_TO_BINARY

[TO_BINARY](/tidb-cloud-lake/sql/binary.md) 的增强版本，可将输入表达式转换为二进制值；如果转换失败，则返回 `NULL` 而不是报错。

另请参阅：[TO_BINARY](/tidb-cloud-lake/sql/binary.md)

## 语法 {#syntax}

```sql
TRY_TO_BINARY( <expr> )
```

## 示例 {#examples}

以下示例成功将 JSON 数据转换为二进制：

```sql
SELECT TRY_TO_BINARY(PARSE_JSON('{"key":"value", "number":123}')) AS binary_variant_success;

┌──────────────────────────────────────────────────────────────────────────┐
│                              binary_variant                              │
├──────────────────────────────────────────────────────────────────────────┤
│ 40000002100000031000000610000005200000026B65796E756D62657276616C7565507B │
└──────────────────────────────────────────────────────────────────────────┘
```

以下示例演示了当输入为 `NULL` 时，该函数无法进行转换：

```sql
SELECT TRY_TO_BINARY(PARSE_JSON(NULL)) AS binary_variant_invalid_json;

┌─────────────────────────────┐
│ binary_variant_invalid_json │
├─────────────────────────────┤
│ NULL                        │
└─────────────────────────────┘
```