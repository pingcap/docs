---
title: AS_OBJECT
summary: `VARIANT` 値を OBJECT データ型に厳密にキャストします。入力データ型が `VARIANT` でない場合、出力は `NULL` です。`VARIANT` 内の値の型が出力値と一致しない場合、出力は `NULL` です。
---

# AS_OBJECT

`VARIANT` 値を OBJECT データ型に厳密にキャストします。入力データ型が `VARIANT` でない場合、出力は `NULL` です。`VARIANT` 内の値の型が出力値と一致しない場合、出力は `NULL` です。

## 構文 {#syntax}

```sql
AS_OBJECT( <variant> )
```

## 引数 {#arguments}

| 引数 | 説明 |
|-------------|-------------------|
| `<variant>` | VARIANT 値 |

## 戻り値の型 {#return-type}

Object を含む Variant

## 例 {#examples}

```sql
SELECT as_object(parse_json('{"k":"v","a":"b"}'));
+--------------------------------------------+
| as_object(parse_json('{"k":"v","a":"b"}')) |
+--------------------------------------------+
| {"k":"v","a":"b"}                          |
+--------------------------------------------+

SELECT as_object(parse_json('{"name":"John","age":30}'));
+-----------------------------------------------+
| as_object(parse_json('{"name":"John","age":30}')) |
+-----------------------------------------------+
| {"name":"John","age":30}                      |
+-----------------------------------------------+

-- Returns NULL for non-object values
SELECT as_object(parse_json('[1,2,3]'));
+----------------------------------+
| as_object(parse_json('[1,2,3]')) |
+----------------------------------+
| NULL                             |
+----------------------------------+
```