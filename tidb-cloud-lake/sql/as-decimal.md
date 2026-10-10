---
title: AS_DECIMAL
summary: "`VARIANT` 値を DECIMAL データ型に厳密にキャストします。入力データ型が `VARIANT` でない場合、出力は `NULL` です。`VARIANT` 内の値の型が出力値と一致しない場合、出力は `NULL` です。"
---

# AS_DECIMAL

`VARIANT` 値を DECIMAL データ型に厳密にキャストします。入力データ型が `VARIANT` でない場合、出力は `NULL` です。`VARIANT` 内の値の型が出力値と一致しない場合、出力は `NULL` です。

## 構文 {#syntax}

```sql
AS_DECIMAL( <variant> )
```

## 引数 {#arguments}

| 引数 | 説明 |
|-------------|-------------------|
| `<variant>` | VARIANT 値 |

## 戻り値の型 {#return-type}

DECIMAL

## 例 {#examples}

```sql
SELECT as_decimal(parse_json('12.34'));
+---------------------------------+
| as_decimal(parse_json('12.34')) |
+---------------------------------+
| 12.34                           |
+---------------------------------+

SELECT as_decimal(parse_json('123.456789'));
+--------------------------------------+
| as_decimal(parse_json('123.456789')) |
+--------------------------------------+
| 123.456789                           |
+--------------------------------------+

-- Returns NULL for non-decimal values
SELECT as_decimal(parse_json('"abc"'));
+---------------------------------+
| as_decimal(parse_json('"abc"')) |
+---------------------------------+
| NULL                            |
+---------------------------------+
```