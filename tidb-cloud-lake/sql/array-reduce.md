---
title: ARRAY_REDUCE
summary: 指定した Lambda 式を適用して JSON 配列を単一の値に縮約します。Lambda 式の詳細については、Lambda Expressions を参照してください。
---

# ARRAY_REDUCE

指定した Lambda 式を適用して JSON 配列を単一の値に縮約します。Lambda 式の詳細については、[ラムダ式](/tidb-cloud-lake/sql/stored-procedure-scripting.md#lambda-expressions) を参照してください。

## 構文 {#syntax}

```sql
ARRAY_REDUCE(<json_array>, <lambda_expression>)
```

## 例 {#examples}

この例では、配列内のすべての要素 `(2, 3, 4)` を掛け合わせます。

```sql
SELECT ARRAY_REDUCE(
    [2, 3, 4],
    (acc, d) -> acc::Int * d::Int
);

-[ RECORD 1 ]-----------------------------------
array_reduce([2, 3, 4], (acc, d) -> acc::Int32 * d::Int32): 24
```