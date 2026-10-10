---
title: DIV
summary: 1 番目の数値を 2 番目の数値で割った商を返し、最も近い小さい整数に切り捨てます。除算演算子 // と同等です。
---

# DIV

1 番目の数値を 2 番目の数値で割った商を返し、最も近い小さい整数に切り捨てます。除算演算子 `//` と同等です。

関連情報:

- [DIV0](/tidb-cloud-lake/sql/div0.md)
- [DIVNULL](/tidb-cloud-lake/sql/divnull.md)

## 構文 {#syntax}

```sql
<number1> DIV <number2>
```

## エイリアス {#aliases}

- [INTDIV](/tidb-cloud-lake/sql/intdiv.md)

## 例 {#examples}

```sql
-- Equivalent to the division operator "//"
SELECT 6.1 DIV 2, 6.1//2;

┌──────────────────────────┐
│ (6.1 div 2) │ (6.1 // 2) │
├─────────────┼────────────┤
│           3 │          3 │
└──────────────────────────┘

SELECT 6.1 DIV 2, INTDIV(6.1, 2), 6.1 DIV NULL;

┌───────────────────────────────────────────────┐
│ (6.1 div 2) │ intdiv(6.1, 2) │ (6.1 div null) │
├─────────────┼────────────────┼────────────────┤
│           3 │              3 │ NULL           │
└───────────────────────────────────────────────┘

-- Error when divided by 0
root@localhost:8000/default> SELECT 6.1 DIV 0;
error: APIError: ResponseError with 1006: divided by zero while evaluating function `div(6.1, 0)`
```