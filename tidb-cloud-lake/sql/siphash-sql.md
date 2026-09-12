---
title: SIPHASH64
summary: 生成一个 64 位 SipHash 哈希值。
---

# SIPHASH64

生成一个 64 位 [SipHash](https://en.wikipedia.org/wiki/SipHash) 哈希值。

## 语法 {#syntax}

```sql
SIPHASH64(<expr>)
```

## 别名 {#aliases}

- [SIPHASH](/tidb-cloud-lake/sql/siphash.md)

## 示例 {#examples}

```sql
SELECT SIPHASH('1234567890'), SIPHASH64('1234567890');

┌─────────────────────────────────────────────────┐
│ siphash('1234567890') │ siphash64('1234567890') │
├───────────────────────┼─────────────────────────┤
│  18110648197875983073 │    18110648197875983073 │
└─────────────────────────────────────────────────┘
```