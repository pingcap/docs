---
title: AS_ARRAY
summary: "`VARIANT` 値を ARRAY データ型に厳密にキャストします。入力データ型が `VARIANT` でない場合、出力は `NULL` です。`VARIANT` 内の値の型が出力値と一致しない場合、出力は `NULL` です。"
---

# AS_ARRAY

`VARIANT` 値を ARRAY データ型に厳密にキャストします。入力データ型が `VARIANT` でない場合、出力は `NULL` です。`VARIANT` 内の値の型が出力値と一致しない場合、出力は `NULL` です。

## 構文 {#syntax}

```sql
AS_ARRAY( <variant> )
```

## 引数 {#arguments}

| 引数 | 説明 |
|-------------|-------------------|
| `<variant>` | VARIANT 値 |

## 戻り値の型 {#return-type}

Variant には Array が含まれます

## 例 {#examples}

```sql
SELECT as_array(parse_json('[1,2,3]'));
+---------------------------------+
| as_array(parse_json('[1,2,3]')) |
+---------------------------------+
| [1,2,3]                         |
+---------------------------------+

SELECT as_array(parse_json('["a","b","c"]'));
+---------------------------------------+
| as_array(parse_json('["a","b","c"]')) |
+---------------------------------------+
| ["a","b","c"]                         |
+---------------------------------------+

-- Returns NULL for non-array values
SELECT as_array(parse_json('{"key":"value"}'));
+-----------------------------------------+
| as_array(parse_json('{"key":"value"}')) |
+-----------------------------------------+
| NULL                                    |
+-----------------------------------------+
```