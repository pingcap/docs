---
title: LENGTH
summary: 指定された入力文字列またはバイナリ値の長さを返します。文字列の場合、長さは文字数を表し、各 UTF-8 文字は 1 文字として数えられます。バイナリデータの場合、長さはバイト数に対応します。
---

# LENGTH

指定された入力文字列またはバイナリ値の長さを返します。文字列の場合、長さは文字数を表し、各 UTF-8 文字は 1 文字として数えられます。バイナリデータの場合、長さはバイト数に対応します。

## 構文 {#syntax}

```sql
LENGTH(<expr>)
```

## エイリアス {#aliases}

- [CHAR_LENGTH](/tidb-cloud-lake/sql/char-length.md)
- [CHARACTER_LENGTH](/tidb-cloud-lake/sql/character-length.md)
- [LENGTH_UTF8](/tidb-cloud-lake/sql/length-utf8.md)

## 戻り値の型 {#return-type}

BIGINT

## 例 {#examples}

```sql
SELECT LENGTH('Hello'), LENGTH_UTF8('Hello'), CHAR_LENGTH('Hello'), CHARACTER_LENGTH('Hello');

┌───────────────────────────────────────────────────────────────────────────────────────────┐
│ length('hello') │ length_utf8('hello') │ char_length('hello') │ character_length('hello') │
├─────────────────┼──────────────────────┼──────────────────────┼───────────────────────────┤
│               5 │                    5 │                    5 │                         5 │
└───────────────────────────────────────────────────────────────────────────────────────────┘
```