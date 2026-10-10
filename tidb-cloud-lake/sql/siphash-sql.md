---
title: SIPHASH64
summary: 64 ビットの SipHash ハッシュ値を生成します。
---

# SIPHASH64

64 ビットの [SipHash](https://en.wikipedia.org/wiki/SipHash) ハッシュ値を生成します。

## 構文 {#syntax}

```sql
SIPHASH64(<expr>)
```

## エイリアス {#aliases}

- [SIPHASH](/tidb-cloud-lake/sql/siphash.md)

## 例 {#examples}

```sql
SELECT SIPHASH('1234567890'), SIPHASH64('1234567890');

┌─────────────────────────────────────────────────┐
│ siphash('1234567890') │ siphash64('1234567890') │
├───────────────────────┼─────────────────────────┤
│  18110648197875983073 │    18110648197875983073 │
└─────────────────────────────────────────────────┘
```