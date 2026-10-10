---
title: LOCATE
summary: 最初の構文は、文字列 str 内で部分文字列 substr が最初に出現する位置を返します。2 番目の構文は、位置 pos から検索を開始して、文字列 str 内で部分文字列 substr が最初に出現する位置を返します。substr が str に含まれない場合は 0 を返します。いずれかの引数が NULL の場合は NULL を返します。
---

# LOCATE

最初の構文は、文字列 str 内で部分文字列 substr が最初に出現する位置を返します。2 番目の構文は、位置 pos から検索を開始して、文字列 str 内で部分文字列 substr が最初に出現する位置を返します。substr が str に含まれない場合は 0 を返します。いずれかの引数が NULL の場合は NULL を返します。

## 構文 {#syntax}

```sql
LOCATE(<substr>, <str>)
LOCATE(<substr>, <str>, <pos>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|------------|----------------|
| `<substr>` | 部分文字列です。 |
| `<str>`    | 文字列です。 |
| `<pos>`    | 位置です。 |

## 戻り値の型 {#return-type}

`BIGINT`

## 例 {#examples}

```sql
SELECT LOCATE('bar', 'foobarbar')
+----------------------------+
| LOCATE('bar', 'foobarbar') |
+----------------------------+
|                          4 |
+----------------------------+

SELECT LOCATE('xbar', 'foobar')
+--------------------------+
| LOCATE('xbar', 'foobar') |
+--------------------------+
|                        0 |
+--------------------------+

SELECT LOCATE('bar', 'foobarbar', 5)
+-------------------------------+
| LOCATE('bar', 'foobarbar', 5) |
+-------------------------------+
|                             7 |
+-------------------------------+
```