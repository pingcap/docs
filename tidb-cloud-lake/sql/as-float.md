---
title: AS_FLOAT
summary: "`VARIANT` 値を DOUBLE データ型に厳密にキャストします。入力データ型が `VARIANT` でない場合、出力は `NULL` です。`VARIANT` 内の値の型が出力値と一致しない場合、出力は `NULL` です。"
---

# AS_FLOAT

`VARIANT` 値を DOUBLE データ型に厳密にキャストします。入力データ型が `VARIANT` でない場合、出力は `NULL` です。`VARIANT` 内の値の型が出力値と一致しない場合、出力は `NULL` です。

## 構文 {#syntax}

```sql
AS_FLOAT( <variant> )
```

## 引数 {#arguments}

| 引数 | 説明 |
|-------------|-------------------|
| `<variant>` | VARIANT 値 |

## 戻り値の型 {#return-type}

DOUBLE

## 例 {#examples}

```sql
SELECT as_float(parse_json('12.34'));
+-------------------------------+
| as_float(parse_json('12.34')) |
+-------------------------------+
| 12.34                         |
+-------------------------------+

SELECT as_float(parse_json('123'));
+-----------------------------+
| as_float(parse_json('123')) |
+-----------------------------+
| 123.0                       |
+-----------------------------+

-- Returns NULL for non-numeric values
SELECT as_float(parse_json('"abc"'));
+-------------------------------+
| as_float(parse_json('"abc"')) |
+-------------------------------+
| NULL                          |
+-------------------------------+
```