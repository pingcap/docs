---
title: POSITION
summary: POSITION(substr IN str) は LOCATE(substr,str) の同義語です。文字列 str 内で部分文字列 substr が最初に出現する位置を返します。substr が str に含まれていない場合は 0 を返します。いずれかの引数が NULL の場合は NULL を返します。
---

# POSITION

POSITION(substr IN str) は LOCATE(substr,str) の同義語です。文字列 str 内で部分文字列 substr が最初に出現する位置を返します。substr が str に含まれていない場合は 0 を返します。いずれかの引数が NULL の場合は NULL を返します。

## 構文 {#syntax}

```sql
POSITION(<substr> IN <str>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|------------|----------------|
| `<substr>` | 部分文字列です。 |
| `<str>`    | 文字列です。    |

## 戻り値の型 {#return-type}

`BIGINT`

## 例 {#examples}

```sql
SELECT POSITION('bar' IN 'foobarbar')
+----------------------------+
| POSITION('bar' IN 'foobarbar') |
+----------------------------+
|                          4 |
+----------------------------+

SELECT POSITION('xbar' IN 'foobar')
+--------------------------+
| POSITION('xbar' IN 'foobar') |
+--------------------------+
|                        0 |
+--------------------------+
```