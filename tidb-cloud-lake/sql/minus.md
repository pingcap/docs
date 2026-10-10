---
title: MINUS
summary: 数値を負の値にします。
---

# MINUS

数値を負の値にします。

## 構文 {#syntax}

```sql
MINUS( <x> )
```

## エイリアス {#aliases}

- [NEG](/tidb-cloud-lake/sql/neg.md)
- [NEGATE](/tidb-cloud-lake/sql/negate.md)
- [SUBTRACT](/tidb-cloud-lake/sql/subtract.md)

## 例 {#examples}

```sql
SELECT MINUS(PI()), NEG(PI()), NEGATE(PI()), SUBTRACT(PI());

┌───────────────────────────────────────────────────────────────────────────────────┐
│     minus(pi())    │      neg(pi())     │    negate(pi())    │   subtract(pi())   │
├────────────────────┼────────────────────┼────────────────────┼────────────────────┤
│ -3.141592653589793 │ -3.141592653589793 │ -3.141592653589793 │ -3.141592653589793 │
└───────────────────────────────────────────────────────────────────────────────────┘
```