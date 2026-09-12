---
title: BIT_LENGTH
summary: 返回字符串的长度（以位为单位）。
---

# BIT_LENGTH

返回字符串的长度（以位为单位）。

## 语法 {#syntax}

```sql
BIT_LENGTH(<expr>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|-----------| ----------- |
| `<expr>`  | 字符串。 |

## 返回类型 {#return-type}

`BIGINT`

## 示例 {#examples}

```sql
SELECT BIT_LENGTH('Word');
+----------------------------+
| SELECT BIT_LENGTH('Word'); |
+----------------------------+
| 32                         |
+----------------------------+
```