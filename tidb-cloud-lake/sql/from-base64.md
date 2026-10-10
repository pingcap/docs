---
title: FROM_BASE64
summary: base-64 エンコード規則でエンコードされた文字列を受け取り、デコード結果をバイナリとして返します。引数が NULL の場合、または有効な base-64 文字列でない場合、結果は NULL になります。
---

# FROM_BASE64

base-64 エンコード規則でエンコードされた文字列を受け取り、デコード結果をバイナリとして返します。引数が NULL の場合、または有効な base-64 文字列でない場合、結果は NULL になります。

## 構文 {#syntax}

```sql
FROM_BASE64(<expr>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------|-------------------|
| `<expr>`  | 文字列値。 |

## 戻り値の型 {#return-type}

`BINARY`

## 例 {#examples}

```sql
SELECT TO_BASE64('abc'), FROM_BASE64(TO_BASE64('abc')) as b, b::String;
┌───────────────────────────────────────┐
│ to_base64('abc') │    b   │ b::string │
│      String      │ Binary │   String  │
├──────────────────┼────────┼───────────┤
│ YWJj             │ 616263 │ abc       │
└───────────────────────────────────────┘
```