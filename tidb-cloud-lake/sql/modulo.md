---
title: MODULO
summary: x を y で割った余りを返します。y が 0 の場合は、エラーを返します。
---

# MODULO

`x` を `y` で割った余りを返します。`y` が 0 の場合は、エラーを返します。

## 構文 {#syntax}

```sql
MODULO( <x>, <y> )
```

## エイリアス {#aliases}

- [MOD](/tidb-cloud-lake/sql/mod.md)

## 例 {#examples}

```sql
SELECT MOD(9, 2), MODULO(9, 2);

┌──────────────────────────┐
│ mod(9, 2) │ modulo(9, 2) │
├───────────┼──────────────┤
│         1 │            1 │
└──────────────────────────┘
```