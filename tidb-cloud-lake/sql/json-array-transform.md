---
title: JSON_ARRAY_TRANSFORM
summary: 指定した変換 Lambda 式を使用して、JSON 配列の各要素を変換します。Lambda 式の詳細については、Lambda Expressions を参照してください。
---

# JSON_ARRAY_TRANSFORM

指定した変換 Lambda 式を使用して、JSON 配列の各要素を変換します。Lambda 式の詳細については、[ラムダ式](/tidb-cloud-lake/sql/stored-procedure-scripting.md#lambda-expressions) を参照してください。

## 構文 {#syntax}

```sql
ARRAY_TRANSFORM(<json_array>, <lambda_expression>)
```

## 戻り値の型 {#return-type}

JSON 配列。

## 例 {#examples}

この例では、配列内の各数値要素に 10 を掛けることで、元の配列を `[10, 20, 30, 40]` に変換します。

```sql
SELECT ARRAY_TRANSFORM(
    [1, 2, 3, 4],
    data -> (data::Int * 10)
);

-[ RECORD 1 ]-----------------------------------
array_transform([1, 2, 3, 4], data -> data::Int32 * 10): [10,20,30,40]
```