---
title: JSON_PATH_MATCH
summary: 指定した JSON パス式が JSON データ内の特定の条件に一致するかどうかを確認します。`@@` 演算子はこの関数と同義であることに注意してください。詳細は JSON Operators を参照してください。
---

# JSON_PATH_MATCH

指定した JSON パス式が JSON データ内の特定の条件に一致するかどうかを確認します。`@@` 演算子はこの関数と同義であることに注意してください。詳細は [JSON Operators](/tidb-cloud-lake/sql/json-operators.md) を参照してください。

## 構文 {#syntax}

```sql
JSON_PATH_MATCH(<json_data>, <json_path_expression>)
```

- `json_data`: 調べたい JSON データを指定します。JSON オブジェクトまたは配列を指定できます。
- `json_path_expression`: JSON データ内で確認する条件を指定します。この式は、一致対象となる特定のパスまたは条件を記述します。たとえば、JSON 構造内の特定のフィールド値が一定の条件を満たすかどうかを検証できます。`$` 記号は JSON データのルートを表します。これはパス式の開始に使用され、JSON 構造の最上位オブジェクトを示します。

## 戻り値の型 {#return-type}

この関数は次の値を返します。

- 指定した JSON パス式が JSON データ内の条件に一致する場合は `true`
- 指定した JSON パス式が JSON データ内の条件に一致しない場合は `false`
- `json_data` または `json_path_expression` のいずれかが NULL または無効な場合は NULL

## 例 {#examples}

```sql
-- Check if the value at JSON path $.a is equal to 1
SELECT JSON_PATH_MATCH(parse_json('{"a":1,"b":[1,2,3]}'), '$.a == 1');

┌────────────────────────────────────────────────────────────────┐
│ json_path_match(parse_json('{"a":1,"b":[1,2,3]}'), '$.a == 1') │
├────────────────────────────────────────────────────────────────┤
│ true                                                           │
└────────────────────────────────────────────────────────────────┘

-- Check if the first element in the array at JSON path $.b is greater than 1
SELECT JSON_PATH_MATCH(parse_json('{"a":1,"b":[1,2,3]}'), '$.b[0] > 1');

┌──────────────────────────────────────────────────────────────────┐
│ json_path_match(parse_json('{"a":1,"b":[1,2,3]}'), '$.b[0] > 1') │
├──────────────────────────────────────────────────────────────────┤
│ false                                                            │
└──────────────────────────────────────────────────────────────────┘

-- Check if any element in the array at JSON path $.b
-- from the second one to the last are greater than or equal to 2
SELECT JSON_PATH_MATCH(parse_json('{"a":1,"b":[1,2,3]}'), '$.b[1 to last] >= 2');

┌───────────────────────────────────────────────────────────────────────────┐
│ json_path_match(parse_json('{"a":1,"b":[1,2,3]}'), '$.b[1 to last] >= 2') │
├───────────────────────────────────────────────────────────────────────────┤
│ true                                                                      │
└───────────────────────────────────────────────────────────────────────────┘

-- NULL is returned if either the json_data or json_path_expression is NULL or invalid.
SELECT JSON_PATH_MATCH(parse_json('{"a":1,"b":[1,2,3]}'), NULL);

┌──────────────────────────────────────────────────────────┐
│ json_path_match(parse_json('{"a":1,"b":[1,2,3]}'), null) │
├──────────────────────────────────────────────────────────┤
│ NULL                                                     │
└──────────────────────────────────────────────────────────┘

SELECT JSON_PATH_MATCH(NULL, '$.a == 1');

┌───────────────────────────────────┐
│ json_path_match(null, '$.a == 1') │
├───────────────────────────────────┤
│ NULL                              │
└───────────────────────────────────┘
```