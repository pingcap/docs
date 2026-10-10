---
title: INSTR
summary: 文字列 str 内で部分文字列 substr が最初に出現する位置を返します。これは LOCATE() の 2 引数形式と同じですが、引数の順序が逆です。
---

# INSTR

文字列 str 内で部分文字列 substr が最初に出現する位置を返します。これは LOCATE() の 2 引数形式と同じですが、引数の順序が逆です。

## 構文 {#syntax}

```sql
INSTR(<str>, <substr>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|------------|----------------|
| `<str>`    | 文字列です。    |
| `<substr>` | 部分文字列です。 |

## 戻り値の型 {#return-type}

`BIGINT`

## 例 {#examples}

```sql
SELECT INSTR('foobarbar', 'bar');
+---------------------------+
| INSTR('foobarbar', 'bar') |
+---------------------------+
|                         4 |
+---------------------------+

SELECT INSTR('xbar', 'foobar');
+-------------------------+
| INSTR('xbar', 'foobar') |
+-------------------------+
|                       0 |
+-------------------------+
```