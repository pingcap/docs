---
title: RIGHT
summary: 文字列 str の右端から len 文字を返します。いずれかの引数が NULL の場合は NULL を返します。
---

# RIGHT

文字列 str の右端から len 文字を返します。いずれかの引数が NULL の場合は NULL を返します。

## 構文 {#syntax}

```sql
RIGHT(<str>, <len>);
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------|----------------------------------------------------------|
| `<str>`   | 文字を抽出する元の文字列 |
| `<len>`   | 文字数 |

## 戻り値の型 {#return-type}

`VARCHAR`

## 例 {#examples}

```sql
SELECT RIGHT('foobarbar', 4);
+-----------------------+
| RIGHT('foobarbar', 4) |
+-----------------------+
| rbar                  |
+-----------------------+
```