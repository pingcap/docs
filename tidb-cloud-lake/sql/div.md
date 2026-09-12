---
title: DIV
summary: 返回将第一个数字除以第二个数字所得的商，并向下取整到最接近且更小的整数。等价于除法运算符 //。
---

# DIV

返回将第一个数字除以第二个数字所得的商，并向下取整到最接近且更小的整数。等价于除法运算符 `//`。

另请参阅：

- [DIV0](/tidb-cloud-lake/sql/div0.md)
- [DIVNULL](/tidb-cloud-lake/sql/divnull.md)

## 语法 {#syntax}

```sql
<number1> DIV <number2>
```

## 别名 {#aliases}

- [INTDIV](/tidb-cloud-lake/sql/intdiv.md)

## 示例 {#examples}

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