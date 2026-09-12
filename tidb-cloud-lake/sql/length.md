---
title: LENGTH
summary: 返回给定输入字符串或二进制值的长度。对于字符串，长度表示字符数，其中每个 UTF-8 字符都视为单个字符。对于二进制数据，长度对应于字节数。
---

# LENGTH

返回给定输入字符串或二进制值的长度。对于字符串，长度表示字符数，其中每个 UTF-8 字符都视为单个字符。对于二进制数据，长度对应于字节数。

## 语法 {#syntax}

```sql
LENGTH(<expr>)
```

## 别名 {#aliases}

- [CHAR_LENGTH](/tidb-cloud-lake/sql/char-length.md)
- [CHARACTER_LENGTH](/tidb-cloud-lake/sql/character-length.md)
- [LENGTH_UTF8](/tidb-cloud-lake/sql/length-utf8.md)

## 返回类型 {#return-type}

BIGINT

## 示例 {#examples}

```sql
SELECT LENGTH('Hello'), LENGTH_UTF8('Hello'), CHAR_LENGTH('Hello'), CHARACTER_LENGTH('Hello');

┌───────────────────────────────────────────────────────────────────────────────────────────┐
│ length('hello') │ length_utf8('hello') │ char_length('hello') │ character_length('hello') │
├─────────────────┼──────────────────────┼──────────────────────┼───────────────────────────┤
│               5 │                    5 │                    5 │                         5 │
└───────────────────────────────────────────────────────────────────────────────────────────┘
```