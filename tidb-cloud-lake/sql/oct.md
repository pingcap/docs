---
title: OCT
summary: N の 8 進数値の文字列表現を返します。
---

# OCT

N の 8 進数値の文字列表現を返します。

## 構文 {#syntax}

```sql
OCT(<expr>)
```

## 例 {#examples}

```sql
SELECT OCT(12);
+---------+
| OCT(12) |
+---------+
| 014     |
+---------+
```