---
title: AS_INTEGER
summary: `VARIANT` 値を BIGINT データ型に厳密にキャストします。入力データ型が `VARIANT` でない場合、出力は `NULL` です。`VARIANT` 内の値の型が出力値と一致しない場合、出力は `NULL` です。
---

# AS_INTEGER

`VARIANT` 値を BIGINT データ型に厳密にキャストします。入力データ型が `VARIANT` でない場合、出力は `NULL` です。`VARIANT` 内の値の型が出力値と一致しない場合、出力は `NULL` です。

## 構文 {#syntax}

```sql
AS_INTEGER( <variant> )
```

## 引数 {#arguments}

| 引数 | 説明 |
|-------------|-------------------|
| `<variant>` | VARIANT 値 |

## 戻り値の型 {#return-type}

BIGINT

## 例 {#examples}

```sql
SELECT as_integer(parse_json('123'));
+-------------------------------+
| as_integer(parse_json('123')) |
+-------------------------------+
| 123                           |
+-------------------------------+

SELECT as_integer(parse_json('-456'));
+--------------------------------+
| as_integer(parse_json('-456')) |
+--------------------------------+
| -456                           |
+--------------------------------+

-- Returns NULL for non-integer values
SELECT as_integer(parse_json('12.34'));
+---------------------------------+
| as_integer(parse_json('12.34')) |
+---------------------------------+
| NULL                            |
+---------------------------------+
```