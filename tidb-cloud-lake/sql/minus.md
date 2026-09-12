---
title: MINUS
summary: 对数值取负。
---

# MINUS

对数值取负。

## 语法 {#syntax}

```sql
MINUS( <x> )
```

## 别名 {#aliases}

- [NEG](/tidb-cloud-lake/sql/neg.md)
- [NEGATE](/tidb-cloud-lake/sql/negate.md)
- [SUBTRACT](/tidb-cloud-lake/sql/subtract.md)

## 示例 {#examples}

```sql
SELECT MINUS(PI()), NEG(PI()), NEGATE(PI()), SUBTRACT(PI());

┌───────────────────────────────────────────────────────────────────────────────────┐
│     minus(pi())    │      neg(pi())     │    negate(pi())    │   subtract(pi())   │
├────────────────────┼────────────────────┼────────────────────┼────────────────────┤
│ -3.141592653589793 │ -3.141592653589793 │ -3.141592653589793 │ -3.141592653589793 │
└───────────────────────────────────────────────────────────────────────────────────┘
```