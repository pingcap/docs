---
title: XXHASH32
summary: 文字列の xxHash32 32-bit ハッシュ値を計算します。値は UInt32 として返されます。引数が NULL の場合は NULL を返します。
---

# XXHASH32

文字列の xxHash32 32-bit ハッシュ値を計算します。値は UInt32 として返されます。引数が NULL の場合は NULL を返します。

## 構文 {#syntax}

```sql
XXHASH32(expr)
```

## 例 {#examples}

```sql
SELECT XXHASH32('1234567890');

┌────────────────────────┐
│ xxhash32('1234567890') │
├────────────────────────┤
│             3896585587 │
└────────────────────────┘
```