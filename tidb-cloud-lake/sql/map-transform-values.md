---
title: MAP_TRANSFORM_VALUES
summary: ラムダ式を使用して、JSON オブジェクト内の各値に変換を適用します。
---

# MAP_TRANSFORM_VALUES

[ラムダ式](/tidb-cloud-lake/sql/stored-procedure-scripting.md#lambda-expressions)を使用して、JSON オブジェクト内の各値に変換を適用します。

## 構文 {#syntax}

```sql
MAP_TRANSFORM_VALUES(<json_object>, (<key>, <value>) -> <value_transformation>)
```

## 戻り値の型 {#return-type}

入力 JSON オブジェクトと同じキーを持ち、指定したラムダ変換に従って値が変更された JSON オブジェクトを返します。

## 例 {#examples}

この例では、各数値を 10 倍し、元のオブジェクトを `{"a":10,"b":20}` に変換します。

```sql
SELECT MAP_TRANSFORM_VALUES('{"a":1,"b":2}'::VARIANT, (k, v) -> v * 10) AS transformed_values;

┌────────────────────┐
│ transformed_values │
├────────────────────┤
│ {"a":10,"b":20}    │
└────────────────────┘
```