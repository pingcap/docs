---
title: PLUS
summary: 2 つの数値または decimal 値の合計を計算します。
---

# PLUS

2 つの数値または decimal 値の合計を計算します。

## 構文 {#syntax}

```sql
PLUS(<number1>, <number2>)
```

## エイリアス {#aliases}

- [ADD](/tidb-cloud-lake/sql/add.md)

## 例 {#examples}

```sql
SELECT ADD(1, 2.3), PLUS(1, 2.3);

┌───────────────────────────────┐
│  add(1, 2.3)  │  plus(1, 2.3) │
├───────────────┼───────────────┤
│ 3.3           │ 3.3           │
└───────────────────────────────┘
```