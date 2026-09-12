---
title: BIN
summary: 返回 N 的二进制值的字符串表示。
---

# BIN

返回 N 的二进制值的字符串表示。

## 语法 {#syntax}

```sql
BIN(<expr>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|-----------|-------------|
| `<expr>`  | 该数字。 |

## 返回类型 {#return-type}

`VARCHAR`

## 示例 {#examples}

```sql
SELECT BIN(12);
+---------+
| BIN(12) |
+---------+
| 1100    |
+---------+
```