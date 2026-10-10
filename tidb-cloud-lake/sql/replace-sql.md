---
title: REPLACE
summary: 文字列 str 内の文字列 from_str のすべての出現箇所を文字列 to_str に置き換えて返します。
---

# REPLACE

文字列 str 内の文字列 from_str のすべての出現箇所を文字列 to_str に置き換えて返します。

## 構文 {#syntax}

```sql
REPLACE(<str>, <from_str>, <to_str>)
```

## 引数 {#arguments}

| 引数         | 説明                 |
|--------------|----------------------|
| `<str>`      | 文字列です。         |
| `<from_str>` | 置換元の文字列です。 |
| `<to_str>`   | 置換先の文字列です。 |

## 戻り値の型 {#return-type}

`VARCHAR`

## 例 {#examples}

```sql
SELECT REPLACE('www.mysql.com', 'w', 'Ww');
+-------------------------------------+
| REPLACE('www.mysql.com', 'w', 'Ww') |
+-------------------------------------+
| WwWwWw.mysql.com                    |
+-------------------------------------+
```