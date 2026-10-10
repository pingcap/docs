---
title: ARRAY_FILTER
summary: 指定した Lambda expression に基づいて JSON 配列から要素をフィルタリングし、条件を満たす要素のみを返します。Lambda expression の詳細については、Lambda Expressions を参照してください。
---

# ARRAY_FILTER

指定した Lambda expression に基づいて JSON 配列から要素をフィルタリングし、条件を満たす要素のみを返します。Lambda expression の詳細については、[ラムダ式](/tidb-cloud-lake/sql/stored-procedure-scripting.md#lambda-expressions) を参照してください。

## 構文 {#syntax}

```sql
ARRAY_FILTER(<json_array>, <lambda_expression>)
```

## 戻り値の型 {#return-type}

JSON 配列。

## 例 {#examples}

この例では、配列をフィルタリングして文字 `a` で始まる文字列のみを返し、結果は `["apple", "avocado"]` になります。

```sql
SELECT ARRAY_FILTER(
    ['apple', 'banana', 'avocado', 'grape'],
    d -> d::String LIKE 'a%'
);

-[ RECORD 1 ]-----------------------------------
array_filter(['apple', 'banana', 'avocado', 'grape'], d -> d::STRING LIKE 'a%'): ["apple","avocado"]
```